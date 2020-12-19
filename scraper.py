from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import requests
import re

import pandas as pd

class Scraper():
    def __init__(self):
        pass

    def scrape(self, links):
        opts = Options()
        # opts.headless = True
        # assert opts.headless
        chrome = Chrome(options=opts)
        filesToDownload = []

        for ix, link in enumerate(links):
            r = requests.get(link)
            html = r.text
            currentPage = 0
            pages = []

            pageCount = re.search("((pages_count&quot;:)\d+)", html)

            if pageCount:
                pageCount = int(pageCount.group(1).removeprefix("pages_count&quot;:"))

            chrome.get(link)

            title = chrome.find_element_by_css_selector("meta[name='twitter:title']").get_attribute("content")

            firstImage = chrome.find_element_by_css_selector(f'img[src*=score_{currentPage}]')
            scrollableContainer = firstImage.find_element_by_xpath("..").find_element_by_xpath("..")

            while len(pages) < pageCount:
                try:
                    image = chrome.find_element_by_css_selector(f'img[src*=score_{currentPage}]')
                    href = image.get_attribute("src")
                    if href not in pages:
                        pages.append(href)
                        currentPage += 1
                        print(pages)
                except NoSuchElementException:
                    chrome.execute_script("arguments[0].scrollTop += 20", scrollableContainer)

            filesToDownload.append({
                "title": title,
                "pages": pages
            })

        chrome.close()
        return filesToDownload