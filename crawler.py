#!/usr/bin/env python3
#
# natbot.py
#
# Set OPENAI_API_KEY to your API key, and then run this from a terminal.
#

from playwright.sync_api import sync_playwright
import time
from sys import argv, exit, platform
import openai
import os
import requests
from colorama import Fore, Style, init
from yaspin import yaspin
from terminal_timer import loading_spinner_decorator

init(autoreset=True)


class Crawler:
    def __init__(self, headless=False):
        browser = (
            sync_playwright()
            .start()
            .chromium.launch(
                headless=headless,
            )
        )

        # Define a normal Chrome user agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.3"

        self.context = browser.new_context(
            user_agent=user_agent, viewport={"width": 1280, "height": 1600}
        )

        # On new page callback
        self.context.on("page", self.on_new_page)

        # Load blank page
        self.page = self.context.new_page()

        # Array of dom elements
        self.elements = []

        # Array of text nodes with ID
        self.nodes = []

    @loading_spinner_decorator
    def go_to_page(self, url):
        url = url if "://" in url else "http://" + url
        self.page.goto(url=url)

        # Wait for page to load
        self.page.wait_for_load_state("networkidle")

        # Wait for javascript to load
        time.sleep(1)

        # self.client = self.page.context.new_cdp_session(self.page)
        # self.page_element_buffer = {}

    def on_new_page(self, page):
        # print("New page opened:", page.url)
        self.page = page

    def scroll(self, direction):
        if direction == "up":
            self.page.evaluate(
                "(document.scrollingElement || document.body).scrollTop = (document.scrollingElement || document.body).scrollTop - window.innerHeight;"
            )
        elif direction == "down":
            self.page.evaluate(
                "(document.scrollingElement || document.body).scrollTop = (document.scrollingElement || document.body).scrollTop + window.innerHeight;"
            )

    @loading_spinner_decorator
    def click(self, index):
        # Inject javascript into the page which removes the target= attribute from all links
        js = """
		links = document.getElementsByTagName("a");
		for (var i = 0; i < links.length; i++) {
			links[i].removeAttribute("target");
		}
		"""
        self.page.evaluate(js)

        (element, center) = self.elements[index]

        # CLick on element
        element.click()

    @loading_spinner_decorator
    def select(self, node_index: int, value: str):
        (element, center) = self.elements[node_index]

        # Set the value of the select
        self.page.evaluate(
            f'element => element.value = "{value}"',
            element,
        )

    def get_node(self, id):
        return self.nodes[id]

    @loading_spinner_decorator
    def type(self, id, text):
        self.click(id)
        time.sleep(0.01)

        self.page.keyboard.type(text)

    def enter(self):
        self.page.keyboard.press("Enter")

    def current_url(self):
        return self.page.url

    def page_title(self):
        return self.page.title()

    def _get_color(self, line: str):
        if (
            line.startswith("<select")
            or line.startswith("</select")
            or line.strip().startswith("<option")
        ):
            return Fore.BLUE
        elif line.startswith("<link"):
            return Fore.GREEN
        elif line.startswith("<button"):
            return Fore.CYAN
        elif line.startswith("<input"):
            return Fore.MAGENTA
        else:
            # Default gray color
            return Fore.LIGHTBLACK_EX

    def print_context(self):
        context = self.get_context()

        print("==============Browser Context=================")

        # Print all the lines in context color coded
        for line in context.split("\n"):
            color = self._get_color(line)
            print(f"‖ {color}{line.strip()}")

        print("==============================================")

    def get_context(self):
        nodes_string = "\n".join(self.nodes)

        return f"""Page Title: {self.page_title()[:100]}
Page URL: {self.current_url()[:100]}
Page Nodes:
{nodes_string}"""

    @loading_spinner_decorator
    def crawl(self):
        # Wait for page to load (maximum 5 seconds) (don't throw)

        # Wait 1 second
        time.sleep(1)

        self.page.wait_for_load_state("networkidle", timeout=10000)

        # Wait for javascript to load
        time.sleep(0.3)

        page = self.page

        # Print page html

        # Get all elements on the page
        elements = page.query_selector_all("*")

        # Define the desired element types
        desired_elements = [
            "a",
            "button",
            "input",
            "textarea",
            "select",
            "img",
            "h1",
            "h2",
            "h3",
        ]

        black_listed_elements = set(
            [
                "html",
                "head",
                "title",
                "meta",
                "iframe",
                "body",
                "script",
                "style",
                "path",
                "svg",
                "br",
                "::marker",
            ]
        )

        # Initialize an empty array to store the important elements
        # Stores the raw eleemnts
        important_elements = []

        # <button>text value</button>
        important_nodes = []

        # Add the JavaScript function to check the visibility of an element
        js_visibility_check = """
function isElementVisibleAndNotObscured(element) {
    if (!element) return false;

    const rect = element.getBoundingClientRect();
    const windowHeight = (window.innerHeight || document.documentElement.clientHeight);
    const windowWidth = (window.innerWidth || document.documentElement.clientWidth);

    const inViewport = (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= windowHeight &&
        rect.right <= windowWidth
    );

    if (!inViewport) {
        return false;
    }

    const centerX = rect.left + (rect.width / 2);
    const centerY = rect.top + (rect.height / 2);

    const topElement = document.elementFromPoint(centerX, centerY);
    return element.contains(topElement) || element === topElement;
}
        """

        # Inject the JavaScript function into the page
        page.evaluate(js_visibility_check)

        i = 0
        for element in elements:
            is_visible = page.evaluate(js_visibility_check, element)

            if not is_visible:
                continue

            # Get the element's tag name
            tag_name = page.evaluate("element => element.tagName", element).lower()

            # Check if element has a click handler
            has_click_handler = page.evaluate(
                "element => element.hasAttribute('onclick')", element
            )

            # Check if the tag_name is in the desired_elements and not in the black_listed_elements
            if (
                tag_name in desired_elements or has_click_handler
            ) and tag_name not in black_listed_elements:
                # Get relevant information about the element
                element_info = {
                    "id": i,
                    "aria-label": element.get_attribute("aria-label"),
                    "value": element.get_attribute("value"),
                    "alt": element.get_attribute("alt"),
                    "placeholder": element.get_attribute("placeholder"),
                    "name": element.get_attribute("name"),
                }

                # If it's a select get the selected option value
                if tag_name == "select":
                    element_info["value"] = element.evaluate(
                        "element => element.options[element.selectedIndex]?.value"
                    )

                # Get eleements x and y coordinates to center
                center_x = page.evaluate(
                    "element => element.getBoundingClientRect().left + (element.getBoundingClientRect().width / 2)",
                    element,
                )
                center_y = page.evaluate(
                    "element => element.getBoundingClientRect().top + (element.getBoundingClientRect().height / 2)",
                    element,
                )

                # If tag_name == "img" and there is no alt text, skip this element
                if tag_name == "img" and element_info["alt"] is None:
                    continue

                # Rename a = button
                if tag_name == "a":
                    tag_name = "link"

                # Rename textarea = input
                if tag_name == "textarea":
                    tag_name = "input"

                # Add to Arrays
                important_elements.append(
                    (
                        element,
                        {
                            "x": center_x,
                            "y": center_y,
                        },
                    )
                )

                # Turn element_info into a string key={value} key2={value2}
                element_info_string = " ".join(
                    [
                        f'{key}="{value}"'
                        for key, value in element_info.items()
                        if value is not None and value != ""
                    ]
                )

                # Get children for specific tags
                children = None
                if tag_name == "select":
                    options = element.query_selector_all("option")

                    children = (
                        "\n"
                        + "\n".join(
                            [
                                f'   <option value="{option.get_attribute("value")}">{option.text_content().strip()}</option>'
                                for option in options
                            ]
                        )
                        + "\n"
                    )
                else:
                    children = element.text_content().strip()

                if children:
                    node = f"<{tag_name} {element_info_string}>{children.strip()}</{tag_name}>"
                else:
                    node = f"<{tag_name} {element_info_string}/>"

                important_nodes.append(node)

                # Add the element_info to the important_elements array

                i += 1

        self.elements = important_elements
        self.nodes = important_nodes

        return important_nodes
