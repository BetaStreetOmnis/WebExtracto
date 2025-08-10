#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试qwen-agent响应格式
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_qwen_response():
    """调试qwen-agent响应格式"""
    try:
        from qwen_agent.agents import Assistant
        from core.ai_summary.config import qwen_max_llm_cfg
        
        print("🔍 调试qwen-agent响应格式...")
        
        # 创建临时智能体
        temp_agent = Assistant(
            llm=qwen_max_llm_cfg,
            name="调试智能体",
            description="用于调试的临时智能体",
            system_message="你是一个测试助手，请简单回复。",
            function_list=[],
            files=[]
        )
        
        # 测试简单调用
        test_prompt = "请简单介绍一下人工智能"
        print(f"📝 测试提示: {test_prompt}")
        
        # 调用智能体
        response_generator = temp_agent.run(test_prompt)
        
        print("🔍 分析响应生成器...")
        print(f"   生成器类型: {type(response_generator)}")
        
        # 逐个分析响应块
        chunk_count = 0
        for chunk in response_generator:
            chunk_count += 1
            print(f"\n📦 响应块 {chunk_count}:")
            print(f"   类型: {type(chunk)}")
            print(f"   内容: {chunk}")
            
            # 分析对象的属性
            if hasattr(chunk, '__dict__'):
                print(f"   属性: {chunk.__dict__}")
            
            # 检查是否有content属性
            if hasattr(chunk, 'content'):
                print(f"   content属性: {chunk.content}")
            
            # 检查是否有text属性
            if hasattr(chunk, 'text'):
                print(f"   text属性: {chunk.text}")
            
            # 检查是否有message属性
            if hasattr(chunk, 'message'):
                print(f"   message属性: {chunk.message}")
            
            # 如果是字典类型
            if isinstance(chunk, dict):
                print(f"   字典键: {list(chunk.keys())}")
                for key, value in chunk.items():
                    print(f"     {key}: {value}")
            
            # 只分析前3个块，避免输出过多
            if chunk_count >= 3:
                break
        
        print(f"\n✅ 总共分析了 {chunk_count} 个响应块")
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_qwen_response() 