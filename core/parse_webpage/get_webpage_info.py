import os
import sys
# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

from core.parse_webpage.selenium_tool import SeleniumTool 
from core.parse_webpage.playwright_tool import PlaywrightScraper
from core.parse_webpage.requests_tool import RequestsTool
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebPageParser:
    def __init__(self):
        """初始化三种解析工具"""
        self.requests_tool = RequestsTool()
        self.selenium_tool = SeleniumTool()
        self.rpa_tool = PlaywrightScraper()

    def get_webpage_content(self, url, tool_type=None):
        """
        获取网页内容,可指定解析工具或按默认顺序尝试
        Args:
            url: 目标网页URL
            tool_type: 指定解析工具类型,可选值:'requests','selenium','playwright',默认None表示按顺序尝试
        Returns:
            BeautifulSoup对象或None
        """
        if tool_type == 'requests':
            logger.info("使用requests获取页面内容...")
            soup = self.requests_tool.get_url_content_by_requests(url)
            if soup:
                logger.info("使用requests成功获取页面内容")
                return soup
            logger.error("使用requests获取页面失败")
            return None
            
        elif tool_type == 'selenium':
            logger.info("使用selenium获取页面内容...")
            soup = self.selenium_tool.get_page_soup(url)
            if soup:
                logger.info("使用selenium成功获取页面内容")
                return soup
            logger.error("使用selenium获取页面失败")
            return None
            
        elif tool_type == 'playwright':
            logger.info("使用playwright获取页面内容...")
            try:
                soup = self.rpa_tool.fetch_and_parse(url)
                if soup:
                    logger.info("使用playwright成功获取页面内容")
                    return soup
            except Exception as e:
                logger.error(f"使用playwright获取页面失败: {str(e)}")
                return None
                
        else:
            # 按默认顺序尝试
            # 1. 首先尝试requests
            logger.info("尝试使用requests获取页面内容...")
            soup = self.requests_tool.get_url_content_by_requests(url)
            if soup:
                logger.info("使用requests成功获取页面内容")
                return soup

            # 2. requests失败则尝试selenium
            logger.info("requests失败,尝试使用selenium获取页面内容...")
            soup = self.selenium_tool.get_page_soup(url)
            if soup:
                logger.info("使用selenium成功获取页面内容")
                return soup

            # 3. selenium失败则尝试playwright
            logger.info("selenium失败,尝试使用playwright获取页面内容...")
            try:
                soup = self.rpa_tool.fetch_and_parse(url)
                if soup:
                    logger.info("使用playwright成功获取页面内容")
                    return soup
            except Exception as e:
                logger.error(f"使用playwright获取页面失败: {str(e)}")
                return None

        logger.error("所有方法均未能成功获取页面内容")
        return None
