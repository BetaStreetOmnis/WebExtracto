import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=10,  # 重试次数
    backoff_factor=2,  # 等待时间，指数增长
    status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的HTTP状态码
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # 需要重试的HTTP方法
)

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("http://", adapter)
http.mount("https://", adapter)

ua = UserAgent()

class RequestsTool:
    def __init__(self):
        self.headers = {'User-Agent': ua.random}

    @staticmethod
    def get_encoding_from_headers(response):
        """尝试从响应头中获取编码"""
        content_type = response.headers.get('Content-Type')
        if 'charset=' in str(content_type):
            return content_type.split('charset=')[-1]
        return None

    def get_url_content_by_requests(self, url):
        """使用requests获取页面内容"""
        try:
            response = http.get(url, headers=self.headers, timeout=(2, 5))
            response.raise_for_status()
            encoding = self.get_encoding_from_headers(response) or response.apparent_encoding
            response.encoding = encoding
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            return soup
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return False
