#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""获取单个html中所有的页面元素"""

import sys
import os

from urllib.parse import urlparse, urljoin
import re
import logging
from collections import Counter

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.clear_html import cleanup_html
from core.search_engine.search_engine_tool import SearchEngineTool
from core.parse_webpage.get_webpage_info import WebPageParser

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebInfo:
    def __init__(self, url='https://baidu.com', name=None, max_page=20, need_soup=False):
        """
        初始化WebInfo类
        Args:
            url: 目标网站URL,默认为百度
            name: 网站名称,可选
            max_page: 最大爬取页面数,默认20
            need_soup: 是否需要保存soup对象,默认False
        """
        self.url = url
        self.base_url = re.match(r'^(?:https?://)?(?:[^@/]+@)?(?:www\.)?([^:/]+)', self.url).group(1)
        self.url_json = dict()
        self.url_list = []
        self.url_list_no_parse = []
        self.images_list = []
        self.save_content = []
        self.seen_texts = set()
        self.soup_list = [] if need_soup else None
        self.same_tag = []
        self.max_page = max_page
        self.need_soup = need_soup
        self.webpage_parser = WebPageParser()
        self.job_urls = []  # 新增:存储工作职位相关URL
        self.common_text_counter = Counter()  # 用于统计重复文本

    def _clean_html(self, soup, base_url):
        """清理HTML内容"""
        title, body, link_urls, image_urls, text = cleanup_html(str(soup), base_url)
        
        # 将文本分段并过滤掉重复内容
        text_segments = text.split('\n')
        filtered_segments = []
        
        for segment in text_segments:
            segment = segment.strip()
            if not segment:
                continue
                
            # 更新文本计数
            self.common_text_counter[segment] += 1
            
            # 如果这段文本出现次数小于页面总数的一半,则保留
            if self.common_text_counter[segment] < len(self.url_list) / 2:
                filtered_segments.append(segment)
                
        # 重新组合过滤后的文本
        filtered_text = '\n'.join(filtered_segments)
        
        result = {
            'title': title,
            'link_urls': link_urls, 
            'image_urls': image_urls,
            'text': filtered_text
        }
        if self.need_soup:
            result['soup'] = soup
        return result

    def get_url(self, name, engine_name="bing"):
        """通过搜索引擎获取URL"""
        search_tool = SearchEngineTool(keyword=name, engine_name=engine_name, filter_text_len=10)
        search_results = search_tool.search_answer()
        if search_results and len(search_results) > 0:
            return search_results[0]['href']
        logger.warning(f"无法找到 {name} 的官网URL")
        return None

    def get_page_info(self, url):
        """获取单个页面信息"""
        self.url_list.append(url)
        soup = self.webpage_parser.get_webpage_content(url)
        if not soup:
            return {}
        if self.need_soup:
            self.soup_list.append(soup)
        return self._clean_html(soup, url)

    def _extract_files_and_links(self, soup):
        """提取页面中的文件和链接"""
        file_extension_pattern = r'\.([a-zA-Z0-9]+)$'
        
        for script_tag in soup.find_all('script', src=True):
            self.js_files.append(urljoin(self.base_url, script_tag['src']))

        for link_tag in soup.find_all('link', rel='stylesheet', href=True):
            self.css_files.append(urljoin(self.base_url, link_tag['href']))

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(self.base_url, href)
            if re.search(file_extension_pattern, href):
                extension = re.search(file_extension_pattern, href).group(1)
                if extension == 'html':
                    self.html_files.append(full_url)
                elif extension == 'php':
                    self.php_files.append(full_url)
                else:
                    self.image_files.append(full_url)
            else:
                if href.startswith('#'):
                    continue
                parsed_url = urlparse(full_url)
                if parsed_url.netloc == urlparse(self.base_url).netloc:
                    self.internal_links.add(full_url)
                else:
                    self.external_links.add(full_url)

    def _page_classes(self, url):
        """页面分类"""
        page_classes = {
            "product": ['product'],
            "company_info": ['about', 'xw'],
            "job": ['job', 'join', 'zp', 'career', 'recruit', 'position', 'zhaopin'],
            "concat": ['concat'],
            "history": ['history'],
            "business": ['business'],
            "news": ['news'],
            "first_page": ['index']
        }
        url_part_list = [part.lower() for part in url.split('/')]

        for category, keywords in page_classes.items():
            if any(keyword in url_part_list for keyword in keywords):
                if category == "job":  # 如果是工作职位相关页面
                    self.job_urls.append(url)  # 添加到工作职位URL列表
                return category
        return "other"

    def is_need_parse(self, url):
        pass

    def get_common_parts(self, page1, page2):
        """获取两个页面的共同部分"""
        if not self.need_soup:
            return
        for tag1 in page1.find_all(True):
            for tag2 in page2.find_all(True):
                if tag1.name == tag2.name and tag1.text.strip() == tag2.text.strip():
                    if tag1 not in self.same_tag:
                        self.same_tag.append(tag1)

    def categorize_url(self, url):
        """URL分类"""
        if "http" not in url:
            return "None"
            
        extension = url.split('.')[-1].lower()
        url_types = {
            'Image': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'pdf'],
            'Zip': ['zip', 'rar'],
            'CSS': ['css'],
            'JavaScript': ['js'],
            'PHP': ['php'],
            'JSON': ['json']
        }
        
        for type_name, extensions in url_types.items():
            if extension in extensions:
                return type_name
                
        return "HTML" if self.base_url in url else "Other"

    def get_all_page_info(self, need_num_level=1):
        """获取所有页面信息"""
        while self.url_list_no_parse:
            if len(self.seen_texts) > self.max_page:
                break
                
            url_no_parse = self.url_list_no_parse.pop(0)
            link_url, num_level = list(url_no_parse.items())[0]
            
            if num_level > need_num_level or link_url in self.url_list:
                continue
                
            url_type = self.categorize_url(link_url)
            if url_type != "HTML":
                continue
                
            try:
                res = self.get_page_info(link_url)
                if not res:
                    continue
                    
                page_type = self._page_classes(link_url)
                if self.need_soup and len(self.soup_list) == 2:
                    self.get_common_parts(self.soup_list[0], self.soup_list[1])
                    
                res.update({
                    'page_type': page_type,
                    'url': link_url,
                    'images': [img for img in res['image_urls'] if img not in self.images_list]
                })
                
                self.images_list.extend(res['images'])
                for new_link in res['link_urls']:
                    if new_link not in self.url_list_no_parse:
                        self.url_list_no_parse.append({new_link: num_level + 1})
                        
                self.save_content.append(res)
                
            except Exception as e:
                logger.error(f"解析页面 {link_url} 时发生错误: {str(e)}")
                continue

    def run(self):
        """运行爬虫"""
        self.url_list_no_parse.append({self.url: 0})
        self.get_all_page_info(need_num_level=1)
        return self.save_content, self.job_urls  # 返回所有内容和工作职位URL

def json_to_text(json_data):
    """JSON转文本"""
    if 'id' in json_data:
        del json_data['id']
    text = '-'.join(f"{key}:{value}" for key, value in json_data.items())
    json_data['text'] = text
    return json_data

# def get_website_content(item):
#     """获取网站内容"""
#     url = item.get('url', '')
#     useai = item.get('useai', 0)
#     num_level = item.get('num_level', 1)
#     max_page = item.get('max_page', 20)
#     need_soup = item.get('need_soup', False)
    
#     webtool = WebInfo(url, max_page=max_page, need_soup=need_soup)
#     webtool.url_list_no_parse.append({webtool.url: 0})
#     webtool.get_all_page_info(need_num_level=num_level)
#     content = [{'text': x['text'], 'title': x['title']} for x in webtool.save_content]
#     return content, webtool.job_urls  # 返回内容和工作职位URL

# def soup_explare(item):
#     """解析soup对象"""
#     soup = item['soup']
#     base_url = item.get("base_url", "")
#     webtool = WebInfo(need_soup=True)
#     return webtool._clean_html(soup, base_url)

if __name__ == "__main__":
    target_website = "https://www.cloudwalk.com"
    webtool = WebInfo(target_website)
    content, job_urls = webtool.run()
    print("所有内容:", content)
    print("工作职位URL:", job_urls)