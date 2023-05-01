# maxbot

Maxbot is a fork of [Natbot](https://github.com/nat/natbot) that improves upon the DOM management and reasoning of the bot.

Overall the goal is to drive a web browser with GPT and perform tasks.

## Prompt Management

This repo uses [Prompt Wrangler]() for prompt management. To get started follow the steps:

1. Create an Prompt Wrangler account
2. Clone the Prompt into your own account.
3. Update the `prompt_wrangler.py` file with your own worksapce
4. Add a .env

## Improvements

### Better DOM Managment

- [ ] Ability to interact with selects
- [x] Only include elements that are visible (hidden elements were currently making it)

### Better Reasoning

- [ ] Add memory that stores past steps
