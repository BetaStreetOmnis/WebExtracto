#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qwen-agent智能体使用示例
"""

import json
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ai_summary import HTMLContentExtractorAgent

def example_basic_extraction():
    """示例：基本内容提取"""
    print("=== 基本内容提取示例 ===")
    
    # 测试HTML内容
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebExtracto - 智能网站内容提取工具</title>
    </head>
    <body>
        <header>
            <nav>
                <a href="/">首页</a>
                <a href="/features">功能特性</a>
            </nav>
        </header>
        
        <main>
            <article>
                <h1>WebExtracto - 智能网站内容提取工具</h1>
                <p>WebExtracto是一个强大的网站内容提取和分析工具，能够自动从网页中提取有价值的信息。</p>
                
                <h2>主要功能</h2>
                <ul>
                    <li>智能内容提取：自动识别和提取网页中的主要内容</li>
                    <li>AI总结分析：使用人工智能技术对内容进行总结和分析</li>
                    <li>结构化输出：将提取的内容转换为结构化的数据格式</li>
                    <li>批量处理：支持批量处理多个网页</li>
                </ul>
                
                <h2>技术特点</h2>
                <p>WebExtracto采用先进的自然语言处理技术，能够准确识别文章内容、产品信息、公司介绍等多种类型的内容。</p>
            </article>
        </main>
        
        <footer>
            <p>版权所有 © 2024 WebExtracto</p>
        </footer>
    </body>
    </html>
    """
    
    # 创建智能体
    agent = HTMLContentExtractorAgent()
    
    # 提取内容
    result = agent.extract_content(test_html, "https://webextracto.com")
    
    print("提取结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

def example_agent_analysis():
    """示例：智能体分析"""
    print("\n=== 智能体分析示例 ===")
    
    # 测试HTML内容
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Python编程技巧大全</title>
    </head>
    <body>
        <article>
            <h1>Python编程技巧大全</h1>
            <p>Python是一种强大的编程语言，具有简洁的语法和丰富的库。</p>
            <p>本文介绍了一些实用的Python编程技巧，包括列表推导式、装饰器、生成器等高级特性。</p>
            
            <h2>列表推导式</h2>
            <p>列表推导式是Python中非常实用的特性，可以简洁地创建列表。</p>
            
            <h2>装饰器</h2>
            <p>装饰器是Python中的高级特性，可以优雅地修改函数的行为。</p>
        </article>
    </body>
    </html>
    """
    
    # 创建智能体
    agent = HTMLContentExtractorAgent()
    
    # 使用智能体分析
    analysis = agent.analyze_with_agent(
        test_html, 
        "https://example.com/python-tips",
        "请分析这篇文章的主要内容和技术要点"
    )
    
    print("智能体分析结果:")
    print(analysis)

def example_batch_processing():
    """示例：批量处理"""
    print("\n=== 批量处理示例 ===")
    
    # 多个HTML内容
    html_contents = [
        {
            "html_content": """
            <html><head><title>人工智能入门</title></head>
            <body><article><h1>人工智能入门</h1>
            <p>人工智能是计算机科学的一个重要分支，致力于创建能够执行通常需要人类智能的任务的系统。</p>
            <p>机器学习是人工智能的核心技术之一，通过算法让计算机从数据中学习。</p>
            </article></body></html>
            """,
            "url": "https://example.com/ai-intro"
        },
        {
            "html_content": """
            <html><head><title>深度学习基础</title></head>
            <body><article><h1>深度学习基础</h1>
            <p>深度学习是机器学习的一个子集，使用多层神经网络来学习数据的特征。</p>
            <p>深度学习在图像识别、自然语言处理等领域取得了突破性进展。</p>
            </article></body></html>
            """,
            "url": "https://example.com/deep-learning"
        }
    ]
    
    # 创建智能体
    agent = HTMLContentExtractorAgent()
    
    # 批量处理
    results = agent.batch_extract(html_contents)
    
    print("批量处理结果:")
    for i, result in enumerate(results):
        print(f"\n--- 第 {i+1} 个结果 ---")
        print(json.dumps(result, ensure_ascii=False, indent=2))

def example_quality_assessment():
    """示例：内容质量评估"""
    print("\n=== 内容质量评估示例 ===")
    
    # 测试不同类型的HTML内容
    test_contents = [
        {
            "name": "高质量文章",
            "content": """
            <html><head><title>机器学习算法详解</title></head>
            <body><article><h1>机器学习算法详解</h1>
            <p>机器学习是人工智能的一个重要分支，通过算法让计算机从数据中学习。</p>
            <p>本文详细介绍了监督学习、无监督学习、强化学习等主要算法类型。</p>
            <p>每种算法都有其适用场景和优缺点，选择合适的算法对模型性能至关重要。</p>
            </article></body></html>
            """
        },
        {
            "name": "广告页面",
            "content": """
            <html><head><title>限时优惠</title></head>
            <body><div class="ad">
            <h1>限时优惠活动</h1><p>立即购买，享受8折优惠！</p>
            <button>点击购买</button><p>广告推广内容</p></div></body></html>
            """
        },
        {
            "name": "导航页面",
            "content": """
            <html><head><title>网站导航</title></head>
            <body><nav>
            <ul><li><a href="/">首页</a></li><li><a href="/about">关于我们</a></li>
            <li><a href="/contact">联系我们</a></li></ul></nav>
            <div><p>这是一个导航页面</p></div></body></html>
            """
        }
    ]
    
    # 创建智能体
    agent = HTMLContentExtractorAgent()
    
    for test in test_contents:
        print(f"\n--- 评估: {test['name']} ---")
        
        # 获取质量评分
        quality = agent.get_content_quality_score(test['content'])
        
        print("质量评分:")
        print(json.dumps(quality, ensure_ascii=False, indent=2))
        
        # 提取内容
        result = agent.extract_content(test['content'], f"https://example.com/{test['name']}")
        
        if result['success']:
            print("✅ 内容有效")
        else:
            print(f"❌ 内容无效: {result.get('message', '')}")

def example_tool_function():
    """示例：工具函数使用"""
    print("\n=== 工具函数使用示例 ===")
    
    from core.ai_summary import html_content_extractor
    
    # 测试HTML内容
    test_html = """
    <html><head><title>数据科学入门</title></head>
    <body><article><h1>数据科学入门</h1>
    <p>数据科学是一个跨学科领域，结合了统计学、计算机科学和领域知识。</p>
    <p>数据科学家需要掌握数据清洗、探索性数据分析、机器学习等技能。</p>
    </article></body></html>
    """
    
    # 使用工具函数
    result = html_content_extractor(test_html, "https://example.com/data-science")
    
    print("工具函数结果:")
    print(result)

def main():
    """主函数"""
    print("🚀 qwen-agent智能体使用示例")
    
    try:
        # 运行示例
        example_basic_extraction()
        example_agent_analysis()
        example_batch_processing()
        example_quality_assessment()
        example_tool_function()
        
        print("\n🎉 所有示例运行完成!")
        
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        print("请确保已正确配置qwen-agent环境")

if __name__ == "__main__":
    main() 