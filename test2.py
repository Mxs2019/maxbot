from playwright.sync_api import sync_playwright


def on_new_page(page):
    print("New page opened:", page.url)
    page.wait_for_load_state("load")

    # Wait for page to finish loading
    page.wait_for_timeout(1000)

    # Get page title
    title = page.title()
    print("Page title:", title)

    # Perform actions on the new page
    # ...
    # Close the page after you're done
    # try:
    #     page.close()
    # except Exception as e:
    #     print("Error closing page:", e)


def main():
    with sync_playwright() as p:
        # Launch a browser
        browser = p.chromium.launch()
        # Create a context
        context = browser.new_context()

        # Set up event listener for new pages
        context.on("page", on_new_page)

        # Open an initial page
        page = context.new_page()
        page.goto("https://example.com")
        # Simulate clicking a link that opens in a new tab
        page.evaluate("window.open('https://google.com', '_blank')")

        # Wait for a while to let the new tab open and perform actions
        page.wait_for_timeout(5000)

        # Close the browser
        browser.close()


main()
