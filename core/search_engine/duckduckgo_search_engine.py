from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import logging

import sys
import os
# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.parse_webpage.get_webpage_info import WebPageParser

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DuckDuckGoSearchEngine:
    def __init__(self, keyword, max_results=10):
        self.keyword = keyword
        self.max_results = max_results
        self.webpage_parser = WebPageParser()

    def fetch_duckduckgo_results(self):
        try:
            results = DDGS().text(self.keyword, max_results=self.max_results)
            return results
        except Exception as e:
            logger.error(f"获取DuckDuckGo搜索结果失败: {str(e)}")
            return None

    def parse_html(self, results):
        parsed_results = []
        for result in results:
            parsed_results.append({
                'href': result['url'],
                'title': result['title'], 
                'description': result['snippet']
            })
        return parsed_results

    def search(self):
        results = self.search_from_page()
        print(666, results)
        if results:
            return self.parse_html(results)
        else:
            return []

    def search_from_page(self):
        url = f"https://duckduckgo.com/?q={self.keyword}&t=h_&ia=web"
        try:
            soup = self.webpage_parser.get_webpage_content(url, tool_type='selenium')
            if soup:
                results = []
                # 查找所有搜索结果项
                for result_item in soup.find_all('li', attrs={'data-layout': 'organic'}):
                    # 在每个结果项中查找标题、URL和描述
                    title_elem = result_item.find('a', class_='eVNpHGjtxRBq_gLOfGDr')
                    url_elem = result_item.find('span', class_='Wo6ZAEmESLNUuWBkbMxx')
                    desc_elem = result_item.find('span', class_='kY2IgmnCmOGjharHErah')
                    
                    if title_elem and url_elem and desc_elem:
                        results.append({
                            'url': url_elem.text,
                            'title': title_elem.text.strip(),
                            'snippet': desc_elem.text.strip()
                        })
                return results
            else:
                logger.error("获取页面内容失败")
                return []
        except Exception as e:
            logger.error(f"搜索过程发生错误: {str(e)}")
            return []

# if __name__ == "__main__":
#     query = "python web search"
#     search_engine = DuckDuckGoSearchEngine(query, max_results=5)
#     results = search_engine.search_from_page()
#     if results:
#         print(results)
#     else:
#         print("未获取到搜索结果")
