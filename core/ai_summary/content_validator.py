#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容验证器
用于判断HTML内容是否包含有效的文章内容
"""

import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ContentValidator:
    """内容验证器"""
    
    def __init__(self):
        """初始化内容验证器"""
        # 无效内容关键词
        self.invalid_keywords = [
            '404', 'not found', '页面不存在', '访问错误',
            'under construction', '建设中', '维护中',
            'access denied', '访问被拒绝', 'forbidden'
        ]
        
        # 广告关键词
        self.ad_keywords = [
            '广告', 'advertisement', 'sponsored', '推广',
            '点击', '立即购买', '限时优惠', '特价'
        ]
        
        # 导航关键词
        self.nav_keywords = [
            '首页', '关于我们', '联系我们', '服务条款',
            '隐私政策', '网站地图', '返回顶部'
        ]
    
    def is_valid_content(self, content: str) -> bool:
        """
        判断内容是否有效
        Args:
            content: 内容文本
        Returns:
            是否有效
        """
        if not content:
            return False
        
        # 检查内容长度
        if len(content.strip()) < 100:
            return False
        
        # 检查是否包含无效关键词
        if self._contains_invalid_keywords(content):
            return False
        
        # 检查是否主要是广告内容
        if self._is_mainly_ad_content(content):
            return False
        
        # 检查是否主要是导航内容
        if self._is_mainly_nav_content(content):
            return False
        
        # 检查是否有足够的文本内容
        if not self._has_sufficient_text_content(content):
            return False
        
        return True
    
    def _contains_invalid_keywords(self, content: str) -> bool:
        """检查是否包含无效关键词"""
        content_lower = content.lower()
        for keyword in self.invalid_keywords:
            if keyword.lower() in content_lower:
                return True
        return False
    
    def _is_mainly_ad_content(self, content: str) -> bool:
        """检查是否主要是广告内容"""
        content_lower = content.lower()
        ad_count = 0
        
        for keyword in self.ad_keywords:
            if keyword.lower() in content_lower:
                ad_count += 1
        
        # 如果广告关键词超过3个，认为是广告内容
        return ad_count >= 3
    
    def _is_mainly_nav_content(self, content: str) -> bool:
        """检查是否主要是导航内容"""
        content_lower = content.lower()
        nav_count = 0
        
        for keyword in self.nav_keywords:
            if keyword.lower() in content_lower:
                nav_count += 1
        
        # 如果导航关键词超过5个，认为是导航内容
        return nav_count >= 5
    
    def _has_sufficient_text_content(self, content: str) -> bool:
        """检查是否有足够的文本内容"""
        # 移除HTML标签
        text_content = re.sub(r'<[^>]+>', '', content)
        
        # 计算中文字符数
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text_content))
        
        # 计算英文字符数
        english_chars = len(re.findall(r'[a-zA-Z]', text_content))
        
        # 总有效字符数
        total_chars = chinese_chars + english_chars
        
        # 如果有效字符数少于50，认为内容不足
        return total_chars >= 50
    
    def get_content_quality_score(self, content: str) -> Dict[str, Any]:
        """
        获取内容质量评分
        Args:
            content: 内容文本
        Returns:
            质量评分信息
        """
        if not content:
            return {
                'score': 0,
                'is_valid': False,
                'reasons': ['内容为空']
            }
        
        score = 100
        reasons = []
        
        # 检查内容长度
        if len(content.strip()) < 100:
            score -= 30
            reasons.append('内容长度不足')
        
        # 检查无效关键词
        if self._contains_invalid_keywords(content):
            score -= 50
            reasons.append('包含无效关键词')
        
        # 检查广告内容
        if self._is_mainly_ad_content(content):
            score -= 40
            reasons.append('主要是广告内容')
        
        # 检查导航内容
        if self._is_mainly_nav_content(content):
            score -= 30
            reasons.append('主要是导航内容')
        
        # 检查文本内容
        if not self._has_sufficient_text_content(content):
            score -= 25
            reasons.append('文本内容不足')
        
        # 确保分数不为负数
        score = max(0, score)
        
        return {
            'score': score,
            'is_valid': score >= 50,
            'reasons': reasons,
            'content_length': len(content.strip()),
            'chinese_chars': len(re.findall(r'[\u4e00-\u9fff]', content)),
            'english_chars': len(re.findall(r'[a-zA-Z]', content))
        }
    
    def is_article_content(self, content: str) -> bool:
        """
        判断是否为文章内容
        Args:
            content: 内容文本
        Returns:
            是否为文章内容
        """
        if not self.is_valid_content(content):
            return False
        
        # 文章特征关键词
        article_keywords = [
            '文章', '报道', '新闻', '资讯', '博客', '评论',
            '分析', '研究', '调查', '报告', '指南', '教程'
        ]
        
        content_lower = content.lower()
        article_count = 0
        
        for keyword in article_keywords:
            if keyword in content_lower:
                article_count += 1
        
        # 如果包含文章关键词，更可能是文章内容
        return article_count >= 1
    
    def is_product_content(self, content: str) -> bool:
        """
        判断是否为产品内容
        Args:
            content: 内容文本
        Returns:
            是否为产品内容
        """
        if not self.is_valid_content(content):
            return False
        
        # 产品特征关键词
        product_keywords = [
            '产品', '商品', '服务', '解决方案', '功能', '特性',
            '价格', '购买', '订购', '咨询', '试用', '演示'
        ]
        
        content_lower = content.lower()
        product_count = 0
        
        for keyword in product_keywords:
            if keyword in content_lower:
                product_count += 1
        
        # 如果包含产品关键词，更可能是产品内容
        return product_count >= 2 