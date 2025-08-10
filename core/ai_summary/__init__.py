#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI智能总结模块
用于对爬取的网页内容进行AI整理和总结
"""

from .content_processor import ContentProcessor, ProcessedContent
from .html_cleaner import HTMLCleaner
from .content_validator import ContentValidator
from .html_content_agent import HTMLContentExtractorAgent, html_content_extractor

__all__ = [
    'ContentProcessor',
    'ProcessedContent',
    'HTMLCleaner',
    'ContentValidator',
    'HTMLContentExtractorAgent',
    'html_content_extractor'
]

__version__ = "1.0.0"
__author__ = "WebExtracto Team" 