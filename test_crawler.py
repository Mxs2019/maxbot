#!/usr/bin/env python3
#
# natbot.py
#
# Set OPENAI_API_KEY to your API key, and then run this from a terminal.
#
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright
import time
from sys import argv, exit, platform
import openai
import os
import requests
from crawler import Crawler
import json

load_dotenv()

personal_information = """
Name: Max Shaw
Phone Number: 2032738840
Email: maxdshaw@gmail.com
"""


if __name__ == "__main__":
    _crawler = Crawler(headless=True)
    url = "https://www.opentable.com/"
    _crawler.go_to_page(url)

    _crawler.crawl()

    _crawler.print_context()

    # print("\n".join(crawl))


# <link id=0>About</link>
# <link id=1>Store</link>
# <link id=2 aria-label="Gmail (opens a new tab)">Gmail</link>
# <link id=3 aria-label="Search for Images (opens a new tab)">Images</link>
# <link id=4 aria-label="Google apps"/>
# <link id=5>Sign in</link>
# <img id=6 Google/>
# <textarea id=7 Search search Search/>
# <button id=8 Search by voice/>
# <button id=9 Search by image/>
# <button id=10 Google Search/>
# <button id=11 I'm Feeling Lucky/>
# <link id=12>Advertising</link>
# <link id=13>Business</link>
# <link id=14>How Search works</link>
# <link id=15>Carbon neutral since 2007</link>
# <link id=16>Privacy</link>
# <link id=17>Terms</link>
# <text id=18>Settings</text>
