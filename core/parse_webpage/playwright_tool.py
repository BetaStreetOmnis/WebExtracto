import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class PlaywrightScraper:
    def __init__(self, headless=True):
        self.headless = headless

    async def _get_page_content(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()
            await page.goto(url)
            content = await page.content()
            await browser.close()
            return content

    def parse_content(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup

    def fetch_and_parse(self, url):
        html_content = asyncio.run(self._get_page_content(url))
        soup = self.parse_content(html_content)
        return soup

    # @staticmethod
    # def rpa_tools(item):
    #     url = item["url"]
    #     scraper = PlaywrightScraper(headless=True)
    #     soup = scraper.fetch_and_parse(url)
    #     return soup
