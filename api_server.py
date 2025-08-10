#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import json

from core.website_extract import WebInfo
from core.website_analyzer import WebsiteAnalyzer
from core.search_engine.search_engine_tool import SearchEngineTool
from core.parse_webpage.get_webpage_info import WebPageParser
from core.ai_summary import ContentProcessor, ProcessedContent, HTMLContentExtractorAgent

app = FastAPI(title="网站内容提取API")

class SearchEngineRequest(BaseModel):
    keyword: str
    engine_name: Optional[str] = "bing"
    filter_text_len: Optional[int] = 10

class WebpageRequest(BaseModel):
    url: str
    tool_type: Optional[str] = None

class WebsiteRequest(BaseModel):
    url: str
    useai: Optional[int] = 0
    num_level: Optional[int] = 1  
    max_page: Optional[int] = 20
    need_soup: Optional[bool] = False

class WebsiteResponse(BaseModel):
    content: List[Dict[str, Any]]
    job_urls: List[str]

class AIProcessRequest(BaseModel):
    content: List[Dict[str, Any]]
    process_type: Optional[str] = "all"  # all, summary, key_info, categories, insights
    max_summary_length: Optional[int] = 500

class AICompareRequest(BaseModel):
    website1_url: str
    website2_url: str
    max_page: Optional[int] = 20

class AIConfigRequest(BaseModel):
    model_name: Optional[str] = "qwen-max"
    max_tokens: Optional[int] = 2000
    temperature: Optional[float] = 0.7
    use_local_model: Optional[bool] = False
    local_model_path: Optional[str] = None

class HTMLProcessRequest(BaseModel):
    html_content: str
    url: Optional[str] = ""
    use_ai: Optional[bool] = True

class QwenAgentRequest(BaseModel):
    html_content: str
    url: Optional[str] = ""
    user_query: Optional[str] = ""

class QwenAgentBatchRequest(BaseModel):
    html_contents: List[Dict[str, str]]  # 每个元素包含html_content和url

# 新增：HTML内容提取智能体请求模型
class HTMLContentExtractRequest(BaseModel):
    html_content: str
    url: Optional[str] = ""

class HTMLContentAnalyzeRequest(BaseModel):
    html_content: str
    url: Optional[str] = ""
    user_query: Optional[str] = ""

class HTMLContentBatchRequest(BaseModel):
    html_contents: List[Dict[str, str]]  # 每个元素包含html_content和url

# 全局AI处理器
ai_processor = None
content_processor = None
qwen_agent = None
html_content_agent = None

def get_ai_processor():
    """获取AI处理器实例"""
    global ai_processor
    if ai_processor is None:
        from core.ai_processor import AIContentProcessor, AIConfig
        config = AIConfig()
        ai_processor = AIContentProcessor(config)
    return ai_processor

def get_content_processor():
    """获取内容处理器实例"""
    global content_processor
    if content_processor is None:
        content_processor = ContentProcessor(use_ai=True)
    return content_processor

def get_qwen_agent():
    """获取qwen-agent智能体实例"""
    global qwen_agent
    if qwen_agent is None:
        qwen_agent = HTMLContentExtractorAgent()
    return qwen_agent

def get_html_content_agent():
    """获取HTML内容提取智能体实例"""
    global html_content_agent
    if html_content_agent is None:
        html_content_agent = HTMLContentExtractorAgent()
    return html_content_agent

@app.post("/search", response_model=List[Dict[str, str]])
async def search_engine(request: SearchEngineRequest):
    """搜索引擎接口"""
    try:
        search_tool = SearchEngineTool(
            keyword=request.keyword,
            engine_name=request.engine_name,
            filter_text_len=request.filter_text_len
        )
        return search_tool.search_answer()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webpage_info", response_model=Dict[str, Any])
async def get_webpage(request: WebpageRequest):
    """网页内容获取接口"""
    try:
        parser = WebPageParser()
        soup = parser.get_webpage_content(
            request.url,
            tool_type=request.tool_type
        )
        
        result = {
            "title": soup.title.string if soup and soup.title else None,
            "text": soup.get_text() if soup else None,
            "soup": soup.prettify() if hasattr(soup, 'prettify') else None
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract", response_model=WebsiteResponse)
async def extract_website(request: WebsiteRequest):
    """提取网站内容"""
    try:
        webtool = WebInfo(
            url=request.url,
            max_page=request.max_page,
            need_soup=request.need_soup
        )
        content, job_urls = webtool.run()
        return {
            "content": content,
            "job_urls": job_urls
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze", response_model=Dict[str, Any])
async def analyze_website(request: WebsiteRequest):
    """分析网站结构"""
    try:
        analyzer = WebsiteAnalyzer(request.url)
        result = analyzer.analyze()
        
        # 如果结果是字符串，则解析为字典
        if isinstance(result, str):
            result = json.loads(result)
            
        # 确保返回的是字典类型
        if not isinstance(result, dict):
            raise HTTPException(status_code=500, detail="分析结果格式错误")
            
        return result
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"JSON解析错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/process", response_model=Dict[str, Any])
async def ai_process_content(request: AIProcessRequest):
    """AI处理网站内容"""
    try:
        processor = get_ai_processor()
        
        if request.process_type == "summary":
            # 只生成总结
            all_text = ""
            for page in request.content:
                if page.get('text'):
                    all_text += page['text'] + "\n\n"
            
            summary = processor.summarize_content(all_text, request.max_summary_length)
            return {"summary": summary}
            
        elif request.process_type == "key_info":
            # 只提取关键信息
            all_text = ""
            for page in request.content:
                if page.get('text'):
                    all_text += page['text'] + "\n\n"
            
            key_info = processor.extract_key_info(all_text)
            return {"key_info": key_info}
            
        elif request.process_type == "categories":
            # 只进行分类
            all_text = ""
            for page in request.content:
                if page.get('text'):
                    all_text += page['text'] + "\n\n"
            
            categories = processor.categorize_content(all_text)
            return {"categories": categories}
            
        elif request.process_type == "insights":
            # 只生成洞察
            all_text = ""
            for page in request.content:
                if page.get('text'):
                    all_text += page['text'] + "\n\n"
            
            insights = processor.generate_insights(all_text)
            return {"insights": insights}
            
        else:
            # 处理所有类型
            result = processor.process_website_content(request.content)
            return result
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/extract_and_process", response_model=Dict[str, Any])
async def extract_and_process_with_ai(request: WebsiteRequest):
    """提取网站内容并用AI处理"""
    try:
        # 首先提取网站内容
        webtool = WebInfo(
            url=request.url,
            max_page=request.max_page,
            need_soup=request.need_soup
        )
        content, job_urls = webtool.run()
        
        # 然后用AI处理
        processor = get_ai_processor()
        ai_result = processor.process_website_content(content)
        
        return {
            "raw_content": content,
            "job_urls": job_urls,
            "ai_analysis": ai_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/compare", response_model=Dict[str, Any])
async def compare_websites(request: AICompareRequest):
    """比较两个网站"""
    try:
        # 提取两个网站的内容
        webtool1 = WebInfo(url=request.website1_url, max_page=request.max_page)
        content1, _ = webtool1.run()
        
        webtool2 = WebInfo(url=request.website2_url, max_page=request.max_page)
        content2, _ = webtool2.run()
        
        # 用AI比较
        processor = get_ai_processor()
        comparison_result = processor.compare_websites(content1, content2)
        
        return comparison_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/config", response_model=Dict[str, Any])
async def update_ai_config(request: AIConfigRequest):
    """更新AI配置"""
    try:
        global ai_processor
        
        from core.ai_processor import AIConfig
        config = AIConfig(
            model_name=request.model_name,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            use_local_model=request.use_local_model,
            local_model_path=request.local_model_path
        )
        
        # 重新初始化AI处理器
        from core.ai_processor import AIContentProcessor
        ai_processor = AIContentProcessor(config)
        
        return {"message": "AI配置更新成功", "config": {
            "model_name": config.model_name,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "use_local_model": config.use_local_model
        }}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai/status", response_model=Dict[str, Any])
async def get_ai_status():
    """获取AI处理器状态"""
    try:
        processor = get_ai_processor()
        return {
            "status": "ready",
            "config": {
                "model_name": processor.config.model_name,
                "use_local_model": processor.config.use_local_model,
                "max_tokens": processor.config.max_tokens,
                "temperature": processor.config.temperature
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.post("/ai/summary", response_model=Dict[str, Any])
async def process_html_content(request: HTMLProcessRequest):
    """处理HTML内容并生成结构化总结"""
    try:
        processor = get_content_processor()
        
        # 处理HTML内容
        result = processor.process_html_content(
            request.html_content, 
            request.url
        )
        
        # 转换为字典格式
        if result.is_valid:
            return {
                "success": True,
                "data": {
                    "title": result.title,
                    "summary": result.summary,
                    "content": result.content,
                    "tags": result.tags,
                    "content_type": result.content_type,
                    "word_count": result.word_count
                }
            }
        else:
            return {
                "success": False,
                "message": "内容无效或无文章内容",
                "data": None
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qwen/extract", response_model=Dict[str, Any])
async def qwen_extract_content(request: QwenAgentRequest):
    """使用qwen-agent提取HTML内容"""
    try:
        agent = get_qwen_agent()
        
        # 提取内容
        result = agent.extract_content(request.html_content, request.url)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qwen/analyze", response_model=Dict[str, Any])
async def qwen_analyze_content(request: QwenAgentRequest):
    """使用qwen-agent分析HTML内容"""
    try:
        agent = get_qwen_agent()
        
        # 使用智能体分析
        analysis = agent.analyze_with_agent(
            request.html_content, 
            request.url, 
            request.user_query
        )
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qwen/batch", response_model=Dict[str, Any])
async def qwen_batch_extract(request: QwenAgentBatchRequest):
    """使用qwen-agent批量提取HTML内容"""
    try:
        agent = get_qwen_agent()
        
        # 批量处理
        results = agent.batch_extract(request.html_contents)
        
        return {
            "success": True,
            "results": results,
            "total_count": len(results),
            "success_count": len([r for r in results if r.get('success')])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qwen/quality", response_model=Dict[str, Any])
async def qwen_quality_assessment(request: QwenAgentRequest):
    """使用qwen-agent评估内容质量"""
    try:
        agent = get_qwen_agent()
        
        # 获取质量评分
        quality = agent.get_content_quality_score(request.html_content)
        
        return {
            "success": True,
            "quality": quality
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 新增：HTML内容提取智能体接口 ====================

@app.post("/html/extract", response_model=Dict[str, Any])
async def html_content_extract(request: HTMLContentExtractRequest):
    """HTML内容提取接口 - 提取标题、作者、时间、摘要、标签等"""
    try:
        agent = get_html_content_agent()
        
        # 提取内容
        result = agent.extract_content(request.html_content, request.url)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/html/analyze", response_model=Dict[str, Any])
async def html_content_analyze(request: HTMLContentAnalyzeRequest):
    """HTML内容智能分析接口 - 使用AI分析HTML内容"""
    try:
        agent = get_html_content_agent()
        
        # 智能分析
        analysis = agent.analyze_with_agent(
            request.html_content, 
            request.url, 
            request.user_query
        )
        
        return {
            "success": True,
            "data": analysis,
            "message": "HTML内容分析成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/html/batch", response_model=Dict[str, Any])
async def html_content_batch_extract(request: HTMLContentBatchRequest):
    """HTML内容批量提取接口"""
    try:
        agent = get_html_content_agent()
        
        # 批量处理
        results = agent.batch_extract(request.html_contents)
        
        return {
            "success": True,
            "data": results,
            "message": "批量HTML内容提取成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/html/quality", response_model=Dict[str, Any])
async def html_content_quality_assessment(request: HTMLContentExtractRequest):
    """HTML内容质量评估接口"""
    try:
        agent = get_html_content_agent()
        
        # 提取内容并评估质量
        result = agent.extract_content(request.html_content, request.url)
        
        if result['success']:
            data = result['data']
            quality_assessment = {
                "is_valid": data.get('word_count', 0) > 50,
                "word_count": data.get('word_count', 0),
                "has_title": bool(data.get('title')),
                "has_author": bool(data.get('author')),
                "has_publish_time": bool(data.get('publish_time')),
                "has_summary": bool(data.get('summary')),
                "has_tags": len(data.get('tags', [])) > 0,
                "content_type": data.get('content_type', 'unknown'),
                "extraction_status": "成功" if result['success'] else "失败"
            }
        else:
            quality_assessment = {
                "is_valid": False,
                "extraction_status": "失败",
                "error": result.get('message', '未知错误')
            }
        
        return {
            "success": True,
            "quality_assessment": quality_assessment,
            "message": "HTML内容质量评估完成"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/html/metadata", response_model=Dict[str, Any])
async def html_metadata_extract(request: HTMLContentExtractRequest):
    """HTML元数据提取接口 - 专门提取标题、作者、时间等元数据"""
    try:
        agent = get_html_content_agent()
        
        # 提取内容
        result = agent.extract_content(request.html_content, request.url)
        
        if result['success']:
            data = result['data']
            metadata = {
                "title": data.get('title', ''),
                "author": data.get('author', ''),
                "publish_time": data.get('publish_time', ''),
                "content_type": data.get('content_type', 'unknown'),
                "word_count": data.get('word_count', 0),
                "tags": data.get('tags', [])
            }
        else:
            metadata = {
                "title": "",
                "author": "",
                "publish_time": "",
                "content_type": "unknown",
                "word_count": 0,
                "tags": []
            }
        
        return {
            "success": True,
            "metadata": metadata,
            "message": "HTML元数据提取成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/html/summary", response_model=Dict[str, Any])
async def html_summary_generate(request: HTMLContentExtractRequest):
    """HTML内容摘要生成接口"""
    try:
        agent = get_html_content_agent()
        
        # 提取内容
        result = agent.extract_content(request.html_content, request.url)
        
        if result['success']:
            data = result['data']
            summary_info = {
                "summary": data.get('summary', ''),
                "title": data.get('title', ''),
                "word_count": data.get('word_count', 0),
                "content_preview": data.get('content', '')[:200] + ('...' if len(data.get('content', '')) > 200 else '')
            }
        else:
            summary_info = {
                "summary": "",
                "title": "",
                "word_count": 0,
                "content_preview": ""
            }
        
        return {
            "success": True,
            "summary": summary_info,
            "message": "HTML内容摘要生成成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/html/compare", response_model=Dict[str, Any])
async def html_content_compare(request: Dict[str, Any]):
    """HTML内容比较接口 - 比较两个HTML内容"""
    try:
        agent = get_html_content_agent()
        
        html1 = request.get('html_content_1', '')
        html2 = request.get('html_content_2', '')
        url1 = request.get('url_1', '')
        url2 = request.get('url_2', '')
        
        # 提取两个内容
        result1 = agent.extract_content(html1, url1)
        result2 = agent.extract_content(html2, url2)
        
        comparison = {
            "content1": {
                "success": result1['success'],
                "data": result1.get('data', {}) if result1['success'] else {}
            },
            "content2": {
                "success": result2['success'],
                "data": result2.get('data', {}) if result2['success'] else {}
            },
            "comparison": {
                "title_similarity": "相同" if (result1.get('data', {}).get('title') == result2.get('data', {}).get('title')) else "不同",
                "content_type_similarity": "相同" if (result1.get('data', {}).get('content_type') == result2.get('data', {}).get('content_type')) else "不同",
                "word_count_diff": abs((result1.get('data', {}).get('word_count', 0) - result2.get('data', {}).get('word_count', 0))),
                "tags_overlap": len(set(result1.get('data', {}).get('tags', [])) & set(result2.get('data', {}).get('tags', [])))
            }
        }
        
        return {
            "success": True,
            "comparison": comparison,
            "message": "HTML内容比较完成"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8093)
