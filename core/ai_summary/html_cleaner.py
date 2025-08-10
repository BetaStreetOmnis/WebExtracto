#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML清理器
用于清理和预处理HTML内容
"""

import re
import logging
from bs4 import BeautifulSoup
from typing import List

logger = logging.getLogger(__name__)

class HTMLCleaner:
    """HTML清理器"""
    
    def __init__(self):
        """初始化HTML清理器"""
        # 需要移除的标签
        self.remove_tags = [
            'script', 'style', 'noscript', 'iframe', 'embed', 'object',
            'applet', 'canvas', 'svg', 'math', 'form', 'input', 'textarea',
            'select', 'button', 'label', 'fieldset', 'legend'
        ]
        
        # 需要移除的类名关键词
        self.remove_classes = [
            'ad', 'advertisement', 'banner', 'popup', 'modal', 'overlay',
            'sidebar', 'widget', 'comment', 'social', 'share', 'like',
            'menu', 'navigation', 'breadcrumb', 'pagination', 'footer',
            'header', 'logo', 'search', 'login', 'register', 'cookie'
        ]
        
        # 需要移除的ID关键词
        self.remove_ids = [
            'ad', 'advertisement', 'banner', 'popup', 'modal', 'overlay',
            'sidebar', 'widget', 'comment', 'social', 'share', 'like',
            'menu', 'navigation', 'breadcrumb', 'pagination', 'footer',
            'header', 'logo', 'search', 'login', 'register', 'cookie'
        ]
    
    def clean_html(self, html_content: str) -> str:
        """
        清理HTML内容
        Args:
            html_content: 原始HTML内容
        Returns:
            清理后的HTML内容
        """
        if not html_content:
            return ""
        
        try:
            # 解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 移除不需要的标签
            self._remove_unwanted_tags(soup)
            
            # 移除不需要的元素
            self._remove_unwanted_elements(soup)
            
            # 清理空白字符
            self._clean_whitespace(soup)
            
            # 移除重复内容
            self._remove_duplicates(soup)
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"HTML清理失败: {e}")
            return html_content
    
    def _remove_unwanted_tags(self, soup: BeautifulSoup):
        """移除不需要的标签"""
        for tag_name in self.remove_tags:
            for tag in soup.find_all(tag_name):
                tag.decompose()
    
    def _remove_unwanted_elements(self, soup: BeautifulSoup):
        """移除不需要的元素"""
        # 移除包含特定类名的元素
        for class_keyword in self.remove_classes:
            for element in soup.find_all(class_=re.compile(class_keyword, re.I)):
                element.decompose()
        
        # 移除包含特定ID的元素
        for id_keyword in self.remove_ids:
            for element in soup.find_all(id=re.compile(id_keyword, re.I)):
                element.decompose()
        
        # 移除隐藏元素
        for element in soup.find_all(style=re.compile(r'display:\s*none', re.I)):
            element.decompose()
        
        # 移除position: absolute的元素（通常是广告）
        for element in soup.find_all(style=re.compile(r'position:\s*absolute', re.I)):
            element.decompose()
    
    def _clean_whitespace(self, soup: BeautifulSoup):
        """清理空白字符"""
        # 移除多余的空白字符
        for element in soup.find_all(text=True):
            if element.parent.name not in ['script', 'style']:
                element.replace_with(re.sub(r'\s+', ' ', element.string).strip())
    
    def _remove_duplicates(self, soup: BeautifulSoup):
        """移除重复内容"""
        # 移除重复的段落
        paragraphs = soup.find_all('p')
        seen_texts = set()
        
        for p in paragraphs:
            text = p.get_text().strip()
            if text in seen_texts or len(text) < 10:  # 太短的段落可能是重复的
                p.decompose()
            else:
                seen_texts.add(text)
    
    def extract_text_content(self, html_content: str) -> str:
        """
        提取纯文本内容
        Args:
            html_content: HTML内容
        Returns:
            纯文本内容
        """
        if not html_content:
            return ""
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 移除脚本和样式
            for script in soup(["script", "style"]):
                script.decompose()
            
            # 获取文本
            text = soup.get_text(separator='\n', strip=True)
            
            # 清理多余的空白字符
            text = re.sub(r'\n\s*\n', '\n\n', text)
            text = re.sub(r' +', ' ', text)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"文本提取失败: {e}")
            return ""
    
    def extract_links(self, html_content: str) -> List[dict]:
        """
        提取链接
        Args:
            html_content: HTML内容
        Returns:
            链接列表
        """
        links = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text().strip()
                
                if href and text:
                    links.append({
                        'url': href,
                        'text': text,
                        'title': link.get('title', '')
                    })
            
        except Exception as e:
            logger.error(f"链接提取失败: {e}")
        
        return links
    
    def extract_images(self, html_content: str) -> List[dict]:
        """
        提取图片
        Args:
            html_content: HTML内容
        Returns:
            图片列表
        """
        images = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for img in soup.find_all('img'):
                src = img.get('src')
                alt = img.get('alt', '')
                title = img.get('title', '')
                
                if src:
                    images.append({
                        'src': src,
                        'alt': alt,
                        'title': title
                    })
            
        except Exception as e:
            logger.error(f"图片提取失败: {e}")
        
        return images 