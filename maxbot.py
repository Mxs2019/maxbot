#!/usr/bin/env python3
#
# natbot.py
#
# Set OPENAI_API_KEY to your API key, and then run this from a terminal.
#
from dotenv import load_dotenv


from sys import argv, exit, platform
from crawler import Crawler
from mind import Mind
from pw import reason_next_step
import argparse

load_dotenv()

personal_information = """Name: Max Shaw
Phone Number: 2032738840
Email: maxdshaw@gmail.com"""

default_objective = (
    "Book a reservation at Dos Caminos in New York City for 4 people on Friday"
)
# objective = "Book a flight from New York to San Francisco on Friday"

if __name__ == "__main__":
    # Check if debug mode is turned on
    parser = argparse.ArgumentParser()

    # max-stpes argument that defautls to 10
    parser.add_argument(
        "--max-steps", type=int, default=20, help="Maximum number of steps to run"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Allow use to confirm each command before running",
    )
    parser.add_argument(
        "--headless", action="store_true", default=False, help="Run in headless mode"
    )
    parser.add_argument(
        "--objective", type=str, default=default_objective, help="Objective to complete"
    )

    args = parser.parse_args()

    max_steps = args.max_steps
    objective = args.objective
    step_number = 0
    interactive = args.interactive
    headless = args.headless

    _crawler = Crawler(headless=headless)
    _mind = Mind()

    _crawler.go_to_page("google.com")

    try:
        while step_number < max_steps:
            _crawler.crawl()

            browser_context = _crawler.get_context()

            _crawler.print_context()

            next_step = reason_next_step(
                browser_context=browser_context[:4500],
                personal_information=personal_information,
                memory=_mind.getMemories(),
                objective=objective,
            )

            thought = next_step.get("thought")

            _mind.addThought(thought)

            command = next_step.get("command")

            element_id = int(next_step.get("element_id", -1))
            text = next_step.get("text")
            option_value = next_step.get("option_value", None)

            node = _crawler.get_node(element_id)

            _mind.addCommand(command=command, node=node, text=text, value=option_value)

            # If debug then wait for user to press enter before continuing
            if interactive:
                # Wait for user to press enter
                input("Press enter to continue...")

            if command == "CLICK":
                _crawler.click(element_id)
            elif command == "TYPE":
                _crawler.type(element_id, text)
            elif command == "TYPE_AND_SUBMIT":
                _crawler.type(element_id, text)
                _crawler.enter()
            elif command == "SCROLL_UP":
                _crawler.scroll("up")
            elif command == "SCROLL_DOWN":
                _crawler.scroll("down")
            elif command == "SELECT_OPTION":
                _crawler.select(node_index=element_id, value=option_value)
            else:
                print(f"Unknown command: {command}")

            #            time.sleep(1)

            step_number += 1

    except KeyboardInterrupt:
        print("\n[!] Ctrl+C detected, exiting gracefully.")
        exit(0)
