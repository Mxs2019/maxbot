# maxbot

Maxbot is a fork of [Natbot](https://github.com/nat/natbot) that improves upon the DOM management and reasoning of the bot.

Overall the goal is to drive a web browser with GPT and perform tasks. PRs welcome for any improvements or bug fixes!

## Usage

### Environment Variables

Add a `.env` file with teh following variables

```
OPENAI_API_KEY=XXXX
```

### CLI Usage

Run the following command with an objective to get started

```
python ./maxbot.py --objective="Buy airpods"
```

#### Args

| Argument        | Description                                                        | Default Value                                                               |
| --------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| `--objective`   | The objective you want to complete                                 | "Book a reservation at Dos Caminos in New York City for 4 people on Friday" |
| `--max-steps`   | The max number of steps to take                                    | 20                                                                          |
| `--interactive` | Manually press continue to run each command. Helpful for debugging | False                                                                       |
| `--headless`    | Runs in headless mode                                              | False                                                                       |

#### Personal Information

You can add any "personal information" into the personal.txt file. This will be injected into the prompt and should contain things like your name, phone number, email etc. If you add sensitive information like your credit card you should run in `--interactive` mode to be cafeful. Use at your own risk ☢️☢️☢️

## Improvements

Overall this works is the same concept as Natbot but has a bunch of improvements.

### Better DOM Managment

- [x] Ability to interact with selects
- [x] Only include elements that are visible (hidden elements were currently making it)
- [x] More reliable clicking
- [ ] Handles opening new tabs

### Better Reasoning

- [x] Add memory that stores past steps
- [ ] Knows when to stop

## Prompt Management

This repo uses [Prompt Wrangler](https://prompt-wrangler.com/) for prompt management. If you want to view the prompt or make modifications you should fork the prompt and create a Prompt Wrangler account.

[View Prompt on Prompt Wrangler](https://prompt-wrangler.com/p/maxbot/reason-next-command)

> If you don't want to use Prompt Wrangler you can copy and paste the prompt from Prompt Wrangler and hit the OpenAI API directly from this repo.
