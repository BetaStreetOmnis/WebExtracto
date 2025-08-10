#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI功能使用示例
"""

import requests
import json
import os

# API基础URL
BASE_URL = "http://localhost:8093"

def test_ai_extract_and_process():
    """测试提取网站内容并用AI处理"""
    print("=== 测试AI提取和处理功能 ===")
    
    url = "https://www.baidu.com"  # 可以替换为任何网站
    
    data = {
        "url": url,
        "max_page": 5,
        "need_soup": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ai/extract_and_process", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ AI处理成功!")
            print(f"页面数量: {len(result.get('raw_content', []))}")
            
            ai_analysis = result.get('ai_analysis', {})
            if 'summary' in ai_analysis:
                print(f"\n📝 内容总结:")
                print(ai_analysis['summary'])
            
            if 'key_info' in ai_analysis:
                print(f"\n🔍 关键信息:")
                print(json.dumps(ai_analysis['key_info'], ensure_ascii=False, indent=2))
            
            if 'categories' in ai_analysis:
                print(f"\n🏷️ 分类标签:")
                print(ai_analysis['categories'])
            
            if 'insights' in ai_analysis:
                print(f"\n💡 商业洞察:")
                print(ai_analysis['insights'])
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 错误: {e}")

def test_ai_process_content():
    """测试AI处理已有内容"""
    print("\n=== 测试AI处理已有内容 ===")
    
    # 模拟一些网页内容
    content = [
        {
            "title": "公司首页",
            "text": "我们是一家专注于人工智能技术研发的公司，致力于为客户提供最先进的AI解决方案。"
        },
        {
            "title": "产品介绍",
            "text": "我们的主要产品包括智能客服系统、数据分析平台和机器学习工具。"
        }
    ]
    
    data = {
        "content": content,
        "process_type": "all"  # 可以是: all, summary, key_info, categories, insights
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ai/process", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ AI处理成功!")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 错误: {e}")

def test_ai_compare_websites():
    """测试AI比较两个网站"""
    print("\n=== 测试AI网站比较功能 ===")
    
    data = {
        "website1_url": "https://www.baidu.com",
        "website2_url": "https://www.google.com",
        "max_page": 3
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ai/compare", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ 网站比较成功!")
            
            if 'comparison' in result:
                print(f"\n📊 比较分析:")
                print(result['comparison'])
            
            if 'website1' in result and 'website2' in result:
                print(f"\n🏢 网站1总结: {result['website1'].get('summary', '')[:100]}...")
                print(f"🏢 网站2总结: {result['website2'].get('summary', '')[:100]}...")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 错误: {e}")

def test_ai_config():
    """测试AI配置功能"""
    print("\n=== 测试AI配置功能 ===")
    
    # 获取当前状态
    try:
        response = requests.get(f"{BASE_URL}/ai/status")
        if response.status_code == 200:
            result = response.json()
            print("✅ 当前AI状态:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 获取状态失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    # 更新配置
    config_data = {
        "model_name": "gpt-3.5-turbo",
        "max_tokens": 1500,
        "temperature": 0.5,
        "use_local_model": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ai/config", json=config_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ 配置更新成功!")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 配置更新失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 错误: {e}")

def test_different_process_types():
    """测试不同的处理类型"""
    print("\n=== 测试不同处理类型 ===")
    
    content = [
        {
            "title": "测试页面",
            "text": "这是一个测试页面，包含了一些示例内容用于测试AI处理功能。"
        }
    ]
    
    process_types = ["summary", "key_info", "categories", "insights"]
    
    for process_type in process_types:
        print(f"\n--- 测试 {process_type} 处理 ---")
        data = {
            "content": content,
            "process_type": process_type
        }
        
        try:
            response = requests.post(f"{BASE_URL}/ai/process", json=data)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {process_type} 处理成功!")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"❌ {process_type} 处理失败: {response.status_code}")
        except Exception as e:
            print(f"❌ {process_type} 错误: {e}")

def main():
    """主函数"""
    print("🚀 AI功能测试开始...")
    
    # 检查API是否运行
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code != 200:
            print("❌ API服务器未运行，请先启动服务器: python api_server.py")
            return
    except:
        print("❌ 无法连接到API服务器，请确保服务器正在运行")
        return
    
    # 运行测试
    test_ai_extract_and_process()
    test_ai_process_content()
    test_ai_compare_websites()
    test_ai_config()
    test_different_process_types()
    
    print("\n🎉 所有测试完成!")

if __name__ == "__main__":
    main() 