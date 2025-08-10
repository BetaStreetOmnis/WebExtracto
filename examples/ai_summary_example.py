#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI总结功能使用示例
"""

import requests
import json

def example_html_summary():
    """示例：处理HTML内容并生成总结"""
    print("=== AI总结功能使用示例 ===")
    
    # 示例HTML内容
    html_content = """
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
                <a href="/pricing">价格</a>
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
                <p>WebExtracto采用先进的自然语言处理技术，能够准确识别文章内容、产品信息、公司介绍等多种类型的内容。通过AI技术，可以自动生成内容摘要、提取关键信息、进行分类标签等。</p>
                
                <h2>应用场景</h2>
                <p>适用于企业调研、竞品分析、市场研究、内容监控等多种场景。可以帮助用户快速获取和分析大量网页信息，提高工作效率。</p>
            </article>
        </main>
        
        <footer>
            <p>版权所有 © 2024 WebExtracto</p>
        </footer>
    </body>
    </html>
    """
    
    # 调用API
    data = {
        "html_content": html_content,
        "url": "https://webextracto.com",
        "use_ai": True
    }
    
    try:
        response = requests.post("http://localhost:8093/ai/summary", json=data)
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                data = result['data']
                print("✅ 处理成功!")
                print(f"📝 标题: {data.get('title', 'N/A')}")
                print(f"📄 摘要: {data.get('summary', 'N/A')}")
                print(f"🏷️ 标签: {', '.join(data.get('tags', []))}")
                print(f"📊 内容类型: {data.get('content_type', 'N/A')}")
                print(f"📏 字数: {data.get('word_count', 0)}")
                
                # 显示部分正文内容
                content = data.get('content', '')
                if content:
                    print(f"📖 正文预览: {content[:200]}...")
            else:
                print(f"❌ 处理失败: {result.get('message', '未知错误')}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 错误: {e}")

def example_batch_processing():
    """示例：批量处理多个HTML内容"""
    print("\n=== 批量处理示例 ===")
    
    # 多个HTML内容
    html_contents = [
        {
            "title": "技术文章",
            "content": """
            <html><head><title>Python编程技巧</title></head>
            <body><article><h1>Python编程技巧</h1>
            <p>Python是一种强大的编程语言，具有简洁的语法和丰富的库。</p>
            <p>本文介绍了一些实用的Python编程技巧，包括列表推导式、装饰器等高级特性。</p>
            </article></body></html>
            """
        },
        {
            "title": "产品介绍",
            "content": """
            <html><head><title>智能客服系统</title></head>
            <body><article><h1>智能客服系统</h1>
            <p>我们的智能客服系统采用最新的人工智能技术，能够自动回答用户问题。</p>
            <p>系统支持多种语言，24小时在线服务，大大提高了客户满意度。</p>
            </article></body></html>
            """
        }
    ]
    
    results = []
    
    for i, html_data in enumerate(html_contents):
        print(f"\n--- 处理第 {i+1} 个内容 ---")
        
        data = {
            "html_content": html_data["content"],
            "url": f"https://example.com/content/{i+1}",
            "use_ai": True
        }
        
        try:
            response = requests.post("http://localhost:8093/ai/summary", json=data)
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    data = result['data']
                    print(f"✅ 标题: {data.get('title', 'N/A')}")
                    print(f"📄 摘要: {data.get('summary', 'N/A')}")
                    print(f"🏷️ 标签: {', '.join(data.get('tags', []))}")
                    
                    results.append(data)
                else:
                    print(f"❌ 处理失败: {result.get('message', '')}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    print(f"\n📊 批量处理完成，成功处理 {len(results)} 个内容")

def example_content_validation():
    """示例：内容验证功能"""
    print("\n=== 内容验证示例 ===")
    
    # 测试不同类型的HTML内容
    test_contents = [
        {
            "name": "有效文章",
            "content": """
            <html><head><title>深度学习入门指南</title></head>
            <body><article><h1>深度学习入门指南</h1>
            <p>深度学习是机器学习的一个重要分支，通过多层神经网络来学习数据的特征。</p>
            <p>本文将从基础概念开始，逐步介绍深度学习的核心原理和实践应用。</p>
            </article></body></html>
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
        },
        {
            "name": "广告页面",
            "content": """
            <html><head><title>限时优惠</title></head>
            <body><div class="ad">
            <h1>限时优惠活动</h1><p>立即购买，享受8折优惠！</p>
            <button>点击购买</button><p>广告推广内容</p></div></body></html>
            """
        }
    ]
    
    for test in test_contents:
        print(f"\n--- 测试: {test['name']} ---")
        
        data = {
            "html_content": test["content"],
            "url": f"https://example.com/{test['name']}",
            "use_ai": True
        }
        
        try:
            response = requests.post("http://localhost:8093/ai/summary", json=data)
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    data = result['data']
                    print(f"✅ 有效内容 - 标题: {data.get('title', 'N/A')}")
                    print(f"📄 摘要: {data.get('summary', 'N/A')[:100]}...")
                else:
                    print(f"❌ 无效内容 - {result.get('message', '')}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 错误: {e}")

def main():
    """主函数"""
    print("🚀 AI总结功能使用示例")
    
    # 检查API是否运行
    try:
        response = requests.get("http://localhost:8093/docs")
        if response.status_code != 200:
            print("❌ API服务器未运行，请先启动: python api_server.py")
            return
    except:
        print("❌ 无法连接到API服务器")
        return
    
    # 运行示例
    example_html_summary()
    example_batch_processing()
    example_content_validation()
    
    print("\n🎉 示例运行完成!")

if __name__ == "__main__":
    main() 