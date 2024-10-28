import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import json

class WebsiteAnalyzer:
    def __init__(self, base_url, timeout=10):
        """
        初始化WebsiteAnalyzer类。

        参数:
        - base_url: 目标网站的基础URL。
        - timeout: 请求超时时间，默认为10秒。
        """
        self.base_url = base_url
        self.timeout = timeout
        self.content = ""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 资源和链接相关
        self.assets = {
            'js': [],  # JavaScript文件
            'css': [], # CSS样式表
            'html': [], # HTML文件
            'php': [],  # PHP文件
            'images': [], # 图片文件
        }
        self.links = {
            'internal': set(), # 内部链接
            'external': set()  # 外部链接
        }
        
        # 公司信息相关
        self.social_media_links = []
        self.emails = []
        self.phone_numbers = []
        self.addresses = []

    def _fetch_content(self):
        """
        获取目标网站的HTML内容。

        返回值:
        - 成功时返回True，失败时返回False。
        """
        try:
            response = requests.get(
                self.base_url, 
                timeout=self.timeout,
                headers=self.headers
            )
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            self.content = response.text
            return BeautifulSoup(self.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {self.base_url}: {e}")
            return None

    def _extract_social_media(self):
        """
        从HTML内容中提取社交媒体链接。
        """
        social_patterns = {
            'facebook': r'https?://(?:www\.)?facebook\.com/[^"\'>\s]+',
            'twitter': r'https?://(?:www\.)?twitter\.com/[^"\'>\s]+', 
            'linkedin': r'https?://(?:www\.)?linkedin\.com/[^"\'>\s]+',
            'instagram': r'https?://(?:www\.)?instagram\.com/[^"\'>\s]+',
            'weibo': r'https?://(?:www\.)?weibo\.com/[^"\'>\s]+',
            'wechat': r'https?://(?:www\.)?wechat\.com/[^"\'>\s]+'
        }
        
        for platform, pattern in social_patterns.items():
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            if matches:
                self.social_media_links.extend(matches)

    def _extract_emails(self):
        """
        从HTML内容中提取电子邮件地址。
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.emails = list(set(re.findall(email_pattern, self.content)))

    def _extract_phone_numbers(self):
        """
        从HTML内容中提取电话号码。
        支持国内外多种电话号码格式。
        """
        phone_patterns = [
            r'\+?[1-9][0-9]{1,2}[-\s]?[0-9]{2,3}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}',  # 国际格式
            r'(?:[\+（\(]?86)?1[3-9]\d{9}',  # 中国手机号
            r'(?:[\+（\(]?86)?0\d{2,3}[-\s]?\d{7,8}'  # 中国座机号
        ]
        
        numbers = []
        for pattern in phone_patterns:
            matches = re.findall(pattern, self.content)
            numbers.extend(matches)
        
        self.phone_numbers = list(set(
            num.strip().replace(' ', '').replace('-', '') 
            for num in numbers
        ))

    def _extract_addresses(self):
        """
        从HTML内容中提取地址。
        支持中英文地址格式。
        """
        address_patterns = [
            r'(?:地址|Address)[：:]\s*([^，。,\n<>]{5,100})',
            r'(?:位于|Located)[：:]\s*([^，。,\n<>]{5,100})',
            r'\d{1,5}\s\w+(?:\s\w+){1,3},\s\w+,\s[A-Z]{2}\s\d{5}'  # 美式地址
        ]
        
        addresses = []
        for pattern in address_patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            addresses.extend(matches)
        
        self.addresses = list(set(addr.strip() for addr in addresses))

    def _analyze_assets(self, soup):
        """
        从HTML内容中提取文件和链接。

        参数:
        - soup: BeautifulSoup对象，包含HTML内容。
        """
        file_pattern = r'\.([a-zA-Z0-9]+)$'
        
        # 提取JavaScript文件
        for script in soup.find_all('script', src=True):
            self.assets['js'].append(urljoin(self.base_url, script['src']))

        # 提取CSS文件
        for css in soup.find_all('link', rel='stylesheet', href=True):
            self.assets['css'].append(urljoin(self.base_url, css['href']))

        # 提取链接和其他资源
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(self.base_url, href)
            
            if href.startswith('#'):
                continue
                
            # 检查文件类型
            if match := re.search(file_pattern, href):
                ext = match.group(1).lower()
                if ext in self.assets:
                    self.assets[ext].append(full_url)
                elif ext in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']:
                    self.assets['images'].append(full_url)
            else:
                # 分类链接
                parsed_url = urlparse(full_url)
                if parsed_url.netloc == urlparse(self.base_url).netloc:
                    self.links['internal'].add(full_url)
                else:
                    self.links['external'].add(full_url)

    def scan_directory(self, directory):
        """
        扫描指定目录。

        参数:
        - directory: 要扫描的目录路径。

        返回值:
        - 返回目录中的链接列表。
        """
        directory_url = urljoin(self.base_url, directory)
        if soup := self._fetch_content():
            return [urljoin(directory_url, link['href']) 
                   for link in soup.find_all('a', href=True)]
        return []

    def analyze(self):
        """
        执行网站完整分析。

        返回值:
        - 返回包含分析结果的JSON字符串。
        """
        if soup := self._fetch_content():
            # 分析资源和链接
            self._analyze_assets(soup)
            directory_links = self.scan_directory("/directory")
            
            # 分析公司信息
            self._extract_social_media()
            self._extract_emails()
            self._extract_phone_numbers()
            self._extract_addresses()

            results = {
                "assets": self.assets,
                "links": {
                    "internal": list(self.links['internal']),
                    "external": list(self.links['external']),
                    "directory": directory_links
                },
                "company_info": {
                    "social_media": self.social_media_links,
                    "emails": self.emails,
                    "phone_numbers": self.phone_numbers,
                    "addresses": self.addresses
                },
                "statistics": {
                    "js_files": len(self.assets['js']),
                    "css_files": len(self.assets['css']),
                    "html_files": len(self.assets['html']),
                    "php_files": len(self.assets['php']),
                    "images": len(self.assets['images']),
                    "internal_links": len(self.links['internal']),
                    "external_links": len(self.links['external'])
                }
            }
            return json.dumps(results, indent=4)
        return json.dumps({"error": "无法访问网站。"}, indent=4)

# if __name__ == "__main__":
#     target_website = "https://www.cloudwalk.com"
#     analyzer = WebsiteAnalyzer(target_website)
#     result_json = analyzer.analyze()
#     print(result_json)
