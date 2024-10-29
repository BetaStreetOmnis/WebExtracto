#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn

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
    use_selenium: Optional[bool] = False
    timeout: Optional[int] = 30

class WebsiteRequest(BaseModel):
    url: str
    useai: Optional[int] = 0
    num_level: Optional[int] = 1  
    max_page: Optional[int] = 20
    need_soup: Optional[bool] = False

class WebsiteResponse(BaseModel):
    content: List[Dict[str, Any]]
    job_urls: List[str]

class AnalyzerResponse(BaseModel):
    assets: Dict[str, List[str]]
    links: Dict[str, List[str]]
    company_info: Dict[str, List[str]]
    statistics: Dict[str, int]

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
        content = parser.get_webpage_content(
            request.url,
            use_selenium=request.use_selenium,
            timeout=request.timeout
        )
        return {"content": content}
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

@app.post("/analyze", response_model=AnalyzerResponse)
async def analyze_website(request: WebsiteRequest):
    """分析网站结构"""
    try:
        analyzer = WebsiteAnalyzer(request.url)
        result = analyzer.analyze()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8093, reload=True)
