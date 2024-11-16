from newspaper import Article, build
import logging
import os
import sys
import traceback
# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.parse_webpage.get_webpage_info import WebPageParser

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsParser:
    def __init__(self):
        """初始化NewsParser类"""
        self.webpage_parser = WebPageParser()

    def get_news_urls(self, homepage_url):
        """
        使用newspaper3k获取新闻网站主页上的所有新闻URL
        Args:
            homepage_url: 新闻网站主页URL
        Returns:
            list: 包含所有新闻URL的列表
        """
        try:
            paper = build(homepage_url, memoize_articles=False)
            news_links = [article.url for article in paper.articles]
            print(news_links)
            logger.info(f"成功获取到{len(news_links)}个新闻链接")
            return news_links
        except Exception as e:
            logger.error(f"获取新闻链接失败: {str(e)}")
            logger.error(traceback.format_exc())
            return []

    def parse_article_content(self, url):
        """
        解析文章内容
        Args:
            url: 目标文章URL
        Returns:
            dict: 包含文章标题、作者、发布日期、正文内容等信息的字典
        """
        try:
            # 使用WebPageParser解析页面内容
            webpage_info = self.webpage_parser.get_webpage_info(url)
            print(111, webpage_info)
            if webpage_info and webpage_info.get('content'):
                article_info = {
                    "title": webpage_info.get('title', ''),
                    "authors": [],  # WebPageParser暂不支持作者提取
                    "publish_date": None,  # WebPageParser暂不支持日期提取
                    "text": webpage_info['content'],
                    "summary": '',  # WebPageParser暂不支持摘要生成
                    "keywords": []  # WebPageParser暂不支持关键词提取
                }
                logger.info("使用WebPageParser成功解析文章内容")
                print(article_info)
                return article_info
            else:
                logger.error("页面解析失败")
                return None
                
        except Exception as e:
            logger.error(f"解析文章内容失败: {str(e)}")
            logger.error(traceback.format_exc())
            return None


if __name__ == "__main__":
    parser = NewsParser()
    homepage_url = "http://www.cqnews.net/"
    news_urls = parser.get_news_urls(homepage_url)
    for url in news_urls:
        article_info = parser.parse_article_content(url)
        print(article_info)