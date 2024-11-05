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

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8093)
