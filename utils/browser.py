import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

BASE_DIR = Path(__file__).parent.parent
CHROME_DRIVER_NAME = 'chromedriver.exe'
CHROME_DRIVER_PATH = BASE_DIR / 'bin' / CHROME_DRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=str(CHROME_DRIVER_PATH))
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get('http://127.0.0.1:8000/')
