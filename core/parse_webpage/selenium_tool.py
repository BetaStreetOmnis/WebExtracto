from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import logging
import time
import shutil
import platform

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeleniumTool:
    def __init__(self):
        """初始化SeleniumTool类"""
        self.driver = None
        
    def init_browser(self) -> webdriver.Firefox:
        """
        初始化Firefox浏览器
        Returns:
            webdriver.Firefox: Firefox浏览器实例
        """
        try:
            # 检查Firefox是否安装
            self._check_firefox_installation()
            
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')  # 无头模式
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--marionette-port=2828')  # 指定marionette端口
            options.set_preference('marionette.port', 2828)
            
            driver_path = GeckoDriverManager().install()
            service = FirefoxService(driver_path)
            
            # 增加重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.driver = webdriver.Firefox(service=service, options=options)
                    return self.driver
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"第{attempt + 1}次尝试初始化浏览器失败，等待重试: {str(e)}")
                        time.sleep(2)  # 等待2秒后重试
                    else:
                        raise
                        
        except Exception as e:
            logger.error(f"初始化浏览器失败: {str(e)}")
            raise

    def _check_firefox_installation(self):
        """检查Firefox浏览器是否已安装"""
        system = platform.system()
        if system == "Windows":
            firefox_path = shutil.which("firefox.exe")
        else:  # Linux 和 MacOS
            firefox_path = shutil.which("firefox")
            
        if not firefox_path:
            error_msg = (
                "未检测到Firefox浏览器。请先安装Firefox浏览器。\n"
                "Windows: https://www.mozilla.org/zh-CN/firefox/windows/\n"
                "Linux: 使用包管理器安装 firefox\n"
                "MacOS: https://www.mozilla.org/zh-CN/firefox/mac/"
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def get_page_soup(self, url: str) -> BeautifulSoup:
        """
        从URL获取页面内容并返回BeautifulSoup对象
        Args:
            url: 目标网页URL
        Returns:
            BeautifulSoup: 页面内容的BeautifulSoup对象
            None: 如果获取失败
        """
        try:
            if not self.driver:
                self.init_browser()
            
            # 增加页面加载超时设置
            self.driver.set_page_load_timeout(30)
            self.driver.get(url)
            
            # 等待页面加载完成
            time.sleep(2)
            
            page_content = self.driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            return soup
            
        except Exception as e:
            logger.error(f"获取页面内容失败: {str(e)}")
            return None
            
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except Exception as e:
                    logger.warning(f"关闭浏览器失败: {str(e)}")
                finally:
                    self.driver = None

# if __name__ == "__main__":
#     selenium_tool = SeleniumTool()
#     soup = selenium_tool.get_page_soup('http://www.flag-ms.com')
#     if soup:
#         print(soup.get_text())
#     else:
#         print("获取页面内容失败")
