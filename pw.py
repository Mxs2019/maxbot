import time
import requests
import os
from prompt_wrangler import PromptWrangler
from terminal_timer import loading_spinner_decorator
from dotenv import load_dotenv

load_dotenv()

pw = PromptWrangler(base_url="http://localhost:3002/api")


@loading_spinner_decorator
def reason_next_step(
    browser_context: str,
    personal_information: str,
    memory: str,
    objective: str,
):
    reason_next_command_prompt = pw.prompt("maxbot/reason-next-command")

    # Create the body
    args = {
        "browser_context": browser_context,
        "personal_information": personal_information,
        "objective": objective,
        "memory": memory,
    }

    # Get the response
    response = reason_next_command_prompt.run(args=args)
    prediction = response.prediction

    # Print the type of prediction

    return prediction
