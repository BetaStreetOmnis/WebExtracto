# 调用搜索引擎
import sys
import os
import random
import logging
# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.search_engine.duckduckgo_search_engine import DuckDuckGoSearchEngine
from core.search_engine.google_search_engine import GoogleSearchEngine
from core.search_engine.bing_search_engine import BingSearchEngine

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchEngineTool:
    def __init__(self, keyword=None, engine_name='bing', filter_text_len=30):
        """
        初始化搜索引擎工具
        Args:
            keyword: 搜索关键词
            engine_name: 搜索引擎名称,默认为bing
            filter_text_len: 过滤文本长度
        """
        self.engine_name = engine_name.lower()
        self.keyword = keyword
        self.filter_text_len = filter_text_len

    def get_search_engine(self):
        """
        获取搜索引擎实例
        Returns:
            搜索引擎实例
        """
        engine_map = {
            'duckduckgo': DuckDuckGoSearchEngine,
            'google': GoogleSearchEngine,
            'bing': BingSearchEngine
        }
        
        engine_class = engine_map.get(self.engine_name, BingSearchEngine)
        return engine_class(self.keyword, self.filter_text_len)

    def search_answer(self):
        """
        执行搜索并返回结果
        Returns:
            搜索结果列表,包含url和text对应关系的字典
            如果发生错误返回空列表
        """
        try:
            search_tool = self.get_search_engine()
            results = search_tool.search()
            
            if self.engine_name == 'duckduckgo':
                # DuckDuckGo搜索结果已经是正确格式,直接返回
                return results
                
            if not isinstance(results, dict):
                logger.error("搜索结果格式错误: 期望字典类型")
                return []
                
            formatted_results = []
            
            if self.engine_name == 'google':
                # Google搜索结果格式处理
                if not all(key in results for key in ['url', 'title', 'description']):
                    logger.error("Google搜索结果缺少必要的键: url、title 或 description")
                    return []
                    
                for url, title, desc in zip(results['url'], results['title'], results['description']):
                    formatted_results.append({
                        'href': url,
                        'title': title, 
                        'description': desc
                    })
            else:
                # Bing等其他搜索引擎结果格式处理
                if not all(key in results for key in ['url', 'title', 'description']):
                    logger.error("搜索结果缺少必要的键: url、title 或 description")
                    return []
                    
                for url, title, desc in zip(results['url'], results['title'], results['description']):
                    formatted_results.append({
                        'href': url,
                        'title': title,
                        'description': desc
                    })
                    
            return formatted_results
            
        except Exception as e:
            logger.error(f"搜索过程发生错误: {str(e)}")
            return []

if __name__ == "__main__":
    search_tools = SearchEngineTool(keyword="duckduckgo",engine_name="bing", filter_text_len=10)
    res = search_tools.search_answer()
    print(res)