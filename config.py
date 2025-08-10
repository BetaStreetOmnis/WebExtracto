#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
支持从.env文件加载环境变量
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class Config:
    """应用配置类"""
    
    # =============================================================================
    # 服务器配置
    # =============================================================================
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8093"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # =============================================================================
    # AI配置
    # =============================================================================
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "gpt-3.5-turbo")
    AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "2000"))
    AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
    AI_USE_LOCAL_MODEL = os.getenv("AI_USE_LOCAL_MODEL", "false").lower() == "true"
    AI_LOCAL_MODEL_PATH = os.getenv("AI_LOCAL_MODEL_PATH", "")
    
    # =============================================================================
    # qwen-agent配置
    # =============================================================================
    QWEN_MODEL_NAME = os.getenv("QWEN_MODEL_NAME", "qwen-max")
    QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
    QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")
    
    # =============================================================================
    # 爬虫配置
    # =============================================================================
    DEFAULT_MAX_PAGE = int(os.getenv("DEFAULT_MAX_PAGE", "20"))
    DEFAULT_NEED_SOUP = os.getenv("DEFAULT_NEED_SOUP", "false").lower() == "true"
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30"))
    DEFAULT_RETRY_TIMES = int(os.getenv("DEFAULT_RETRY_TIMES", "3"))
    USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # =============================================================================
    # 搜索引擎配置
    # =============================================================================
    DEFAULT_SEARCH_ENGINE = os.getenv("DEFAULT_SEARCH_ENGINE", "bing")
    DEFAULT_FILTER_TEXT_LEN = int(os.getenv("DEFAULT_FILTER_TEXT_LEN", "10"))
    BING_API_KEY = os.getenv("BING_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # =============================================================================
    # 数据库配置
    # =============================================================================
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "webextracto")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    
    # Redis配置
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    
    # =============================================================================
    # 日志配置
    # =============================================================================
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/webextracto.log")
    
    # =============================================================================
    # 安全配置
    # =============================================================================
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key_here")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
    
    # =============================================================================
    # 第三方服务配置
    # =============================================================================
    # 邮件服务
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    
    # 文件存储
    STORAGE_TYPE = os.getenv("STORAGE_TYPE", "local")
    STORAGE_PATH = os.getenv("STORAGE_PATH", "./uploads")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "")
    
    # =============================================================================
    # 开发环境配置
    # =============================================================================
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"
    TEST_API_KEY = os.getenv("TEST_API_KEY", "test_api_key_here")
    
    # =============================================================================
    # 性能配置
    # =============================================================================
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))
    
    # =============================================================================
    # 监控配置
    # =============================================================================
    MONITORING_ENABLED = os.getenv("MONITORING_ENABLED", "false").lower() == "true"
    SENTRY_DSN = os.getenv("SENTRY_DSN", "")
    HEALTH_CHECK_ENABLED = os.getenv("HEALTH_CHECK_ENABLED", "true").lower() == "true"
    HEALTH_CHECK_INTERVAL = int(os.getenv("HEALTH_CHECK_INTERVAL", "300"))
    
    @classmethod
    def get_ai_config(cls):
        """获取AI配置"""
        from core.ai_processor import AIConfig
        return AIConfig(
            model_name=cls.AI_MODEL_NAME,
            max_tokens=cls.AI_MAX_TOKENS,
            temperature=cls.AI_TEMPERATURE,
            use_local_model=cls.AI_USE_LOCAL_MODEL,
            local_model_path=cls.AI_LOCAL_MODEL_PATH if cls.AI_LOCAL_MODEL_PATH else None
        )
    
    @classmethod
    def validate_config(cls):
        """验证配置"""
        errors = []
        
        # 检查必要的AI配置
        if not cls.AI_USE_LOCAL_MODEL and not cls.OPENAI_API_KEY:
            errors.append("未设置OPENAI_API_KEY环境变量，请设置或启用本地模型")
        
        if cls.AI_USE_LOCAL_MODEL and not cls.AI_LOCAL_MODEL_PATH:
            errors.append("启用本地模型但未设置AI_LOCAL_MODEL_PATH")
        
        # 检查qwen-agent配置
        if not cls.QWEN_API_KEY:
            errors.append("未设置QWEN_API_KEY环境变量")
        
        # 检查数据库配置（如果需要）
        if cls.DB_USER and not cls.DB_PASSWORD:
            errors.append("设置了数据库用户但未设置数据库密码")
        
        # 检查Redis配置（如果需要）
        if cls.REDIS_PASSWORD and not cls.REDIS_HOST:
            errors.append("设置了Redis密码但未设置Redis主机")
        
        return errors
    
    @classmethod
    def get_database_url(cls):
        """获取数据库连接URL"""
        if cls.DB_USER and cls.DB_PASSWORD:
            return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        return None
    
    @classmethod
    def get_redis_url(cls):
        """获取Redis连接URL"""
        if cls.REDIS_PASSWORD:
            return f"redis://:{cls.REDIS_PASSWORD}@{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
        else:
            return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
    
    @classmethod
    def is_production(cls):
        """判断是否为生产环境"""
        return cls.ENVIRONMENT.lower() == "production"
    
    @classmethod
    def is_development(cls):
        """判断是否为开发环境"""
        return cls.ENVIRONMENT.lower() == "development"
    
    @classmethod
    def is_testing(cls):
        """判断是否为测试环境"""
        return cls.TEST_MODE or cls.ENVIRONMENT.lower() == "test"

# 创建全局配置实例
config = Config() 