import sys
import os
# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from bs4 import BeautifulSoup
from newspaper import Article# pip install --upgrade lxml_html_clean
import re



class BingSearchEngine:
    def __init__(self, keyword, filter_text_len=30):
        print('bing')
        self.keyword = keyword
        self.filter_text_len = filter_text_len

    def fetch_bing_results(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, verify=True)
        if response.status_code == 200:
            response.encoding = 'utf-8'  # Ensure UTF-8 encoding
            return response.text
        else:
            return None

    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        links = [link for link in links if link.startswith('https')]
        links = [link for link in links if 'bing.com' not in link]
        links = [link for link in links if 'microsoft' not in link]
        
        titles = [a.get_text() for a in soup.find_all('a', href=True) if a['href'].startswith('https') and 'bing.com' not in a['href'] and 'microsoft' not in a['href']]
        texts = [p.get_text() for p in soup.find_all('p')]
        
        return links, titles, texts

    def clean_text(self, text):
        text = text.replace('\u3000', ' ')  # 将全角空格替换为标准空格
        text = text.replace('\xa0', ' ')  # 将NO-BREAK SPACE也替换为标准空格
        cleaned_text = re.sub(r'[^\x00-\x7F\u4e00-\u9fff。？！，、；：""（）《》【】\s]+', '', text)  # 保留基本ASCII和中文字符及常见标点
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text

    def search_keyword_by_bing(self):
        url = f"https://www.bing.com/search?q={self.keyword}&FORM=R5FD2"
        try:
            html_content = self.fetch_bing_results(url)
        except Exception as e:
            html_content = self.fetch_bing_results(url)
        try:
            na_cnt_urls, titles, texts = self.parse_html(html_content)
        except:
            na_cnt_urls, titles, texts = [], [], []
            html_content = self.fetch_bing_results(url)
        if html_content:
            na_cnt_urls, titles, texts = self.parse_html(html_content)
            return na_cnt_urls, titles, texts
        return [], [], []

    def get_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('div')
        if content:
            return content.get_text()

    def search(self):
        url_list, titles, texts = self.search_keyword_by_bing()
        return {'url':url_list, 'title':titles, 'description':texts}
