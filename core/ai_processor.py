#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI内容处理模块
用于对爬取的网页内容进行AI整理和总结
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIConfig:
    """AI配置类"""
    model_name: str = "gpt-3.5-turbo"
    max_tokens: int = 2000
    temperature: float = 0.7
    use_local_model: bool = False
    local_model_path: Optional[str] = None

class AIContentProcessor:
    """AI内容处理器"""
    
    def __init__(self, config: AIConfig = None):
        """
        初始化AI内容处理器
        Args:
            config: AI配置参数
        """
        self.config = config or AIConfig()
        self._init_ai_model()
    
    def _init_ai_model(self):
        """初始化AI模型"""
        try:
            if self.config.use_local_model:
                # 使用本地模型
                from transformers import AutoTokenizer, AutoModelForCausalLM
                
                if not self.config.local_model_path:
                    raise ValueError("使用本地模型时必须指定local_model_path")
                
                self.tokenizer = AutoTokenizer.from_pretrained(self.config.local_model_path)
                self.model = AutoModelForCausalLM.from_pretrained(self.config.local_model_path)
                logger.info(f"成功加载本地模型: {self.config.local_model_path}")
                
            else:
                # 使用Qwen API
                api_key = os.getenv("DASHSCOPE_API_KEY")
                if not api_key:
                    raise ValueError("使用Qwen API时必须设置DASHSCOPE_API_KEY环境变量")
                
                # 导入qwen配置
                from core.ai_summary.config import qwen_max_llm_cfg
                self.llm_cfg = qwen_max_llm_cfg
                logger.info("成功初始化Qwen AI模型")
                
        except Exception as e:
            logger.error(f"AI模型初始化失败: {e}")
            raise
    
    def _call_qwen_api(self, prompt: str, system_prompt: str = None) -> str:
        """调用Qwen API"""
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
    
    def _call_local_model(self, prompt: str) -> str:
        """调用本地模型"""
        try:
            response = self.model(prompt, max_length=len(prompt.split()) + 200)
            return response[0]['generated_text']
        except Exception as e:
            logger.error(f"本地模型调用失败: {e}")
            return ""
    
    def summarize_content(self, content: str, max_length: int = 5000) -> str:
        """
        总结内容
        Args:
            content: 原始内容
            max_length: 最大长度
        Returns:
            总结后的内容
        """
        if len(content) <= max_length:
            return content
        
        prompt = f"""
        请对以下网页内容进行简洁的总结，保留重要信息，控制在{max_length}字以内：

        {content[:5000]}  # 限制输入长度避免token超限
        """
        
        system_prompt = "你是一个专业的内容总结助手，擅长提取网页内容的核心信息。"
        
        if self.config.use_local_model:
            return self._call_local_model(prompt)
        else:
            return self._call_qwen_api(prompt, system_prompt)
    
    def extract_key_info(self, content: str) -> Dict[str, Any]:
        """
        提取关键信息
        Args:
            content: 网页内容
        Returns:
            提取的关键信息字典
        """
        prompt = f"""
        请从以下网页内容中提取关键信息，以JSON格式返回：
        - 公司名称
        - 主营业务
        - 联系方式（电话、邮箱、地址）
        - 产品服务
        - 公司简介
        - 其他重要信息

        内容：
        {content[:2000]}
        """
        
        system_prompt = "你是一个专业的信息提取助手，请以JSON格式返回提取的信息。"
        
        if self.config.use_local_model:
            result = self._call_local_model(prompt)
        else:
            result = self._call_qwen_api(prompt, system_prompt)
        
        # 尝试解析JSON结果
        try:
            # 提取JSON部分
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"error": "无法解析AI返回的JSON格式", "raw_result": result}
        except json.JSONDecodeError:
            return {"error": "JSON解析失败", "raw_result": result}
    
    def categorize_content(self, content: str) -> List[str]:
        """
        对内容进行分类
        Args:
            content: 网页内容
        Returns:
            分类标签列表
        """
        prompt = f"""
        请对以下网页内容进行分类，返回3-5个最相关的分类标签：

        {content[:1500]}

        请以JSON数组格式返回，例如：["技术", "互联网", "软件开发"]
        """
        
        system_prompt = "你是一个专业的内容分类助手，请返回准确的分类标签。"
        
        if self.config.use_local_model:
            result = self._call_local_model(prompt)
        else:
            result = self._call_qwen_api(prompt, system_prompt)
        
        try:
            # 提取JSON数组
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return ["未分类"]
        except json.JSONDecodeError:
            return ["未分类"]
    
    def generate_insights(self, content: str) -> str:
        """
        生成洞察分析
        Args:
            content: 网页内容
        Returns:
            洞察分析文本
        """
        prompt = f"""
        请对以下网页内容进行深度分析，生成有价值的洞察：

        {content[:2000]}

        请从以下角度进行分析：
        1. 业务模式分析
        2. 市场定位
        3. 竞争优势
        4. 发展前景
        5. 潜在风险
        """
        
        system_prompt = "你是一个专业的商业分析师，擅长从网页内容中提取商业洞察。"
        
        if self.config.use_local_model:
            return self._call_local_model(prompt)
        else:
            return self._call_qwen_api(prompt, system_prompt)
    
    def process_website_content(self, website_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        处理整个网站的内容
        Args:
            website_data: 网站数据列表，每个元素包含title、text等信息
        Returns:
            处理结果
        """
        if not website_data:
            return {"error": "没有可处理的内容"}
        
        # 合并所有文本内容
        all_text = ""
        titles = []
        
        for page in website_data:
            if page.get('title'):
                titles.append(page['title'])
            if page.get('text'):
                all_text += page['text'] + "\n\n"
        
        # 去重和清理
        all_text = re.sub(r'\s+', ' ', all_text).strip()
        
        if not all_text:
            return {"error": "没有有效的文本内容"}
        
        # 执行AI处理
        try:
            summary = self.summarize_content(all_text)
            key_info = self.extract_key_info(all_text)
            categories = self.categorize_content(all_text)
            insights = self.generate_insights(all_text)
            
            return {
                "summary": summary,
                "key_info": key_info,
                "categories": categories,
                "insights": insights,
                "page_count": len(website_data),
                "total_text_length": len(all_text),
                "titles": titles[:10]  # 只返回前10个标题
            }
            
        except Exception as e:
            logger.error(f"AI处理失败: {e}")
            return {"error": f"AI处理失败: {str(e)}"}
    
    def compare_websites(self, website1_data: List[Dict], website2_data: List[Dict]) -> Dict[str, Any]:
        """
        比较两个网站
        Args:
            website1_data: 第一个网站数据
            website2_data: 第二个网站数据
        Returns:
            比较结果
        """
        # 处理两个网站的内容
        website1_result = self.process_website_content(website1_data)
        website2_result = self.process_website_content(website2_data)
        
        if "error" in website1_result or "error" in website2_result:
            return {"error": "网站处理失败"}
        
        # 生成比较分析
        prompt = f"""
        请比较以下两个网站的特点：

        网站1信息：
        - 总结：{website1_result.get('summary', '')}
        - 关键信息：{json.dumps(website1_result.get('key_info', {}), ensure_ascii=False)}
        - 分类：{website1_result.get('categories', [])}

        网站2信息：
        - 总结：{website2_result.get('summary', '')}
        - 关键信息：{json.dumps(website2_result.get('key_info', {}), ensure_ascii=False)}
        - 分类：{website2_result.get('categories', [])}

        请从以下角度进行比较：
        1. 业务模式差异
        2. 市场定位对比
        3. 竞争优势分析
        4. 发展前景评估
        """
        
        system_prompt = "你是一个专业的商业分析师，擅长比较分析不同企业的特点。"
        
        if self.config.use_local_model:
            comparison = self._call_local_model(prompt)
        else:
            comparison = self._call_qwen_api(prompt, system_prompt)
        
        return {
            "website1": website1_result,
            "website2": website2_result,
            "comparison": comparison
        } 