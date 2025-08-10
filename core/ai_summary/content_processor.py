#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容处理器
处理HTML内容并返回结构化的结果
"""

import os
import json
import logging
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from bs4 import BeautifulSoup

# 导入其他模块
try:
    from .html_cleaner import HTMLCleaner
    from .content_validator import ContentValidator
except ImportError:
    # 如果相对导入失败，使用绝对导入
    from core.ai_summary.html_cleaner import HTMLCleaner
    from core.ai_summary.content_validator import ContentValidator

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProcessedContent:
    """处理后的内容结构"""
    title: str = ""
    author: str = ""  # 新增：作者信息
    publish_time: str = ""  # 新增：发布时间
    summary: str = ""
    content: str = ""
    tags: List[str] = None
    is_valid: bool = False
    content_type: str = "unknown"
    word_count: int = 0
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class ContentProcessor:
    """内容处理器"""
    
    def __init__(self, use_ai: bool = True):
        """
        初始化内容处理器
        Args:
            use_ai: 是否使用AI处理
        """
        self.use_ai = use_ai
        self.html_cleaner = HTMLCleaner()
        self.content_validator = ContentValidator()
        
        if use_ai:
            self._init_ai_model()
    
    def _init_ai_model(self):
        """初始化AI模型"""
        try:
            # 使用qwen配置
            from .config import qwen_max_llm_cfg
            
            # 检查是否有有效的API密钥
            api_key = os.getenv("DASHSCOPE_API_KEY")
            if api_key:
                self.ai_available = True
                self.llm_cfg = qwen_max_llm_cfg
                logger.info("成功初始化Qwen AI模型")
            else:
                logger.warning("未设置DASHSCOPE_API_KEY，将使用规则处理")
                self.ai_available = False
        except Exception as e:
            logger.error(f"AI模型初始化失败: {e}")
            self.ai_available = False
    
    def _call_qwen_api(self, prompt: str, system_prompt: str = None) -> str:
        """调用Qwen API"""
        if not self.ai_available:
            return ""
        
        try:
            # 直接使用dashscope调用，避免qwen-agent的复杂配置
            import dashscope
            from dashscope import Generation
            
            # 设置API密钥
            api_key = os.getenv("DASHSCOPE_API_KEY")
            if not api_key:
                return ""
            
            dashscope.api_key = api_key
            
            # 构建完整的提示
            full_prompt = f"{system_prompt or '你是一个内容处理专家，请根据用户的要求处理内容。'}\n\n用户: {prompt}\n助手:"
            
            # 调用API
            response = Generation.call(
                model='qwen-max',
                prompt=full_prompt,
                max_tokens=2000,
                temperature=0.7,
                top_p=0.8,
                result_format='message'
            )
            
            if response.status_code == 200:
                # 提取响应文本
                if hasattr(response, 'output') and hasattr(response.output, 'choices'):
                    for choice in response.output.choices:
                        if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                            return choice.message.content.strip()
                
                # 备用提取方法
                if hasattr(response, 'output') and hasattr(response.output, 'text'):
                    return response.output.text.strip()
                
                # 如果上述方法都失败，返回原始响应
                return str(response)
            else:
                logger.error(f"API调用失败: {response.status_code} - {response.message}")
                return ""
                
        except Exception as e:
            logger.error(f"Qwen API调用失败: {e}")
            return ""
    
    def process_html_content(self, html_content: str, url: str = "") -> ProcessedContent:
        """
        处理HTML内容
        Args:
            html_content: HTML内容
            url: 页面URL
        Returns:
            处理后的内容
        """
        # 清理HTML内容
        cleaned_content = self.html_cleaner.clean_html(html_content)
        
        # 验证内容是否有效
        if not self.content_validator.is_valid_content(cleaned_content):
            return ProcessedContent(is_valid=False)
        
        # 提取标题
        title = self._extract_title(html_content)
        
        # 提取作者信息
        author = self._extract_author(html_content)
        
        # 提取发布时间
        publish_time = self._extract_publish_time(html_content)
        
        # 提取正文内容
        content = self._extract_main_content(cleaned_content)
        
        # 生成摘要
        summary = self._generate_summary(content)
        
        # 生成标签
        tags = self._generate_tags(content, title)
        
        # 确定内容类型
        content_type = self._determine_content_type(content, title)
        
        # 计算字数
        word_count = len(content.strip())
        
        return ProcessedContent(
            title=title,
            author=author,
            publish_time=publish_time,
            summary=summary,
            content=content,
            tags=tags,
            is_valid=True,
            content_type=content_type,
            word_count=word_count
        )
    
    def _extract_title(self, html_content: str) -> str:
        """提取页面标题"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 尝试多种标题选择器
            title_selectors = [
                'title',
                'h1',
                '.title',
                '.headline',
                '[class*="title"]',
                '[class*="headline"]'
            ]
            
            for selector in title_selectors:
                element = soup.select_one(selector)
                if element and element.get_text().strip():
                    title = element.get_text().strip()
                    if len(title) > 10 and len(title) < 200:  # 合理的标题长度
                        return title
            
            return ""
        except Exception as e:
            logger.error(f"提取标题失败: {e}")
            return ""
    
    def _extract_author(self, html_content: str) -> str:
        """提取作者信息"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 尝试多种作者选择器
            author_selectors = [
                'meta[name="author"]',
                'meta[property="article:author"]',
                'meta[property="og:author"]',
                '.author',
                '.byline',
                '.writer',
                '[class*="author"]',
                '[class*="byline"]',
                '[class*="writer"]',
                'span[class*="author"]',
                'div[class*="author"]',
                'p[class*="author"]'
            ]
            
            for selector in author_selectors:
                element = soup.select_one(selector)
                if element:
                    # 如果是meta标签，获取content属性
                    if element.name == 'meta':
                        author = element.get('content', '').strip()
                    else:
                        author = element.get_text().strip()
                    
                    if author and len(author) < 100:  # 合理的作者名长度
                        # 清理作者名（移除"作者："、"by"等前缀）
                        author = re.sub(r'^(作者|作者：|by|BY|By)\s*', '', author)
                        return author
            
            return ""
        except Exception as e:
            logger.error(f"提取作者失败: {e}")
            return ""
    
    def _extract_publish_time(self, html_content: str) -> str:
        """提取发布时间"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 尝试多种时间选择器
            time_selectors = [
                'meta[name="publish_date"]',
                'meta[property="article:published_time"]',
                'meta[property="og:published_time"]',
                'time[datetime]',
                '.publish-time',
                '.publish-date',
                '.post-time',
                '.post-date',
                '[class*="time"]',
                '[class*="date"]',
                '[class*="publish"]'
            ]
            
            for selector in time_selectors:
                element = soup.select_one(selector)
                if element:
                    # 如果是meta标签，获取content属性
                    if element.name == 'meta':
                        time_str = element.get('content', '').strip()
                    # 如果是time标签，获取datetime属性
                    elif element.name == 'time':
                        time_str = element.get('datetime', '').strip()
                    else:
                        time_str = element.get_text().strip()
                    
                    if time_str:
                        # 尝试解析和格式化时间
                        formatted_time = self._format_time(time_str)
                        if formatted_time:
                            return formatted_time
            
            return ""
        except Exception as e:
            logger.error(f"提取发布时间失败: {e}")
            return ""
    
    def _format_time(self, time_str: str) -> str:
        """格式化时间字符串"""
        try:
            import re
            from datetime import datetime
            
            # 移除多余的空格
            time_str = time_str.strip()
            
            # 尝试解析ISO格式时间
            iso_patterns = [
                r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
                r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
                r'\d{4}-\d{2}-\d{2}'
            ]
            
            for pattern in iso_patterns:
                match = re.search(pattern, time_str)
                if match:
                    time_part = match.group()
                    try:
                        if 'T' in time_part:
                            dt = datetime.fromisoformat(time_part.replace('T', ' '))
                        else:
                            dt = datetime.fromisoformat(time_part)
                        return dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        continue
            
            # 尝试解析中文时间格式
            chinese_patterns = [
                r'(\d{4})年(\d{1,2})月(\d{1,2})日',
                r'(\d{4})-(\d{1,2})-(\d{1,2})',
                r'(\d{4})/(\d{1,2})/(\d{1,2})'
            ]
            
            for pattern in chinese_patterns:
                match = re.search(pattern, time_str)
                if match:
                    year, month, day = match.groups()
                    try:
                        dt = datetime(int(year), int(month), int(day))
                        return dt.strftime('%Y-%m-%d')
                    except:
                        continue
            
            # 如果无法解析，返回原始字符串
            return time_str
            
        except Exception as e:
            logger.error(f"格式化时间失败: {e}")
            return time_str
    
    def _extract_main_content(self, cleaned_content: str) -> str:
        """提取主要内容"""
        try:
            soup = BeautifulSoup(cleaned_content, 'html.parser')
            
            # 移除不需要的元素
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # 尝试找到主要内容区域
            main_selectors = [
                'main',
                'article',
                '.content',
                '.main-content',
                '.post-content',
                '.entry-content',
                '[class*="content"]',
                '[class*="article"]'
            ]
            
            for selector in main_selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text(separator='\n', strip=True)
                    if len(text) > 100:  # 确保有足够的内容
                        return text
            
            # 如果没有找到主要内容区域，使用整个body
            body = soup.find('body')
            if body:
                return body.get_text(separator='\n', strip=True)
            
            return cleaned_content
        except Exception as e:
            logger.error(f"提取主要内容失败: {e}")
            return cleaned_content
    
    def _generate_summary(self, content: str) -> str:
        """生成摘要"""
        if not content or len(content) < 50:
            return ""
        
        if self.use_ai and self.ai_available:
            prompt = f"""
            请对以下内容生成简洁的摘要，控制在100字以内：

            {content[:2000]}
            """
            
            system_prompt = "你是一个专业的内容总结助手，请生成简洁准确的摘要。"
            
            summary = self._call_qwen_api(prompt, system_prompt)
            if summary:
                return summary
        
        # 如果AI不可用，使用规则生成摘要
        return self._rule_based_summary(content)
    
    def _rule_based_summary(self, content: str) -> str:
        """基于规则的摘要生成"""
        # 取前200个字符作为摘要
        summary = content[:200].strip()
        
        # 如果内容以句号结尾，取到句号
        if '.' in summary:
            summary = summary.rsplit('.', 1)[0] + '.'
        
        return summary
    
    def _generate_tags(self, content: str, title: str) -> List[str]:
        """生成标签"""
        if not content:
            return []
        
        if self.use_ai and self.ai_available:
            prompt = f"""
            请为以下内容生成3-5个相关标签：

            标题：{title}
            内容：{content[:1000]}

            请以JSON数组格式返回，例如：["技术", "互联网", "软件开发"]
            """
            
            system_prompt = "你是一个专业的内容分类助手，请返回准确的标签。"
            
            result = self._call_qwen_api(prompt, system_prompt)
            
            try:
                # 提取JSON数组
                json_match = re.search(r'\[.*\]', result, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
        
        # 如果AI不可用，使用规则生成标签
        return self._rule_based_tags(content, title)
    
    def _rule_based_tags(self, content: str, title: str) -> List[str]:
        """基于规则的标签生成"""
        tags = []
        
        # 预定义的标签关键词
        tag_keywords = {
            "技术": ["技术", "软件", "编程", "开发", "IT", "互联网"],
            "商业": ["商业", "企业", "公司", "业务", "营销", "销售"],
            "教育": ["教育", "学习", "培训", "课程", "学校"],
            "新闻": ["新闻", "资讯", "报道", "事件", "时事"],
            "娱乐": ["娱乐", "游戏", "电影", "音乐", "休闲"]
        }
        
        # 检查内容中的关键词
        full_text = f"{title} {content}".lower()
        for tag, keywords in tag_keywords.items():
            if any(keyword in full_text for keyword in keywords):
                tags.append(tag)
        
        # 如果没有找到标签，添加默认标签
        if not tags:
            tags = ["其他"]
        
        return tags[:5]  # 最多返回5个标签
    
    def _determine_content_type(self, content: str, title: str) -> str:
        """确定内容类型"""
        full_text = f"{title} {content}".lower()
        
        # 内容类型关键词
        type_keywords = {
            "article": ["文章", "报道", "新闻", "资讯", "博客"],
            "product": ["产品", "商品", "服务", "解决方案"],
            "company": ["公司", "企业", "关于我们", "简介"],
            "help": ["帮助", "指南", "教程", "说明", "FAQ"],
            "contact": ["联系", "地址", "电话", "邮箱"]
        }
        
        for content_type, keywords in type_keywords.items():
            if any(keyword in full_text for keyword in keywords):
                return content_type
        
        return "unknown" 