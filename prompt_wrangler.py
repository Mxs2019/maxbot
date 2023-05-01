import time
import requests
import os
from terminal_timer import loading_spinner_decorator


@loading_spinner_decorator
def reason_next_step(
    browser_context: str,
    personal_information: str,
    memory: str,
    objective: str,
):
    # STart timer
    start = time.time()
    # Create the body
    args = {
        "browser_context": browser_context,
        "personal_information": personal_information,
        "objective": objective,
        "memory": memory,
    }

    # Make the request
    response = requests.post(
        "https://prompt-wrangler.com/api/composer-ai/prompts/reason-next-web-command/predict",
        json={
            "args": args,
        },
        headers={
            "x-api-key": os.environ["PROMPT_WRANGLER_API_KEY"],
            "Content-Type": "application/json",
        },
        # 60 second timeout
        timeout=60,
    )

    # Print response body

    # Check if 200
    response.raise_for_status()

    # Get the response
    response_json = response.json()
    prediction = response_json["prediction"]

    return prediction
