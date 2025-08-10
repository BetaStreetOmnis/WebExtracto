
import os
from dotenv import load_dotenv
import sys
# 添加项目根目录到 Python 路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# 加载.env文件中的环境变量
load_dotenv()

#TODO 此部分后期迁移到数据库中管理

# 优先从环境变量中获取 DASHSCOPE_API_KEY
DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', '')
print(DASHSCOPE_API_KEY)

qwen_max_llm_cfg = {
    # 使用 DashScope 提供的模型服务：
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope',
    'api_key': DASHSCOPE_API_KEY,  # 从环境变量读取 api_key
    # 如果这里没有设置 'api_key'，它将读取 `DASHSCOPE_API_KEY` 环境变量。

    # 使用与 OpenAI API 兼容的模型服务，例如 vLLM 或 Ollama：
    # 'model': 'Qwen2.5-7B-Instruct',
    # 'model_server': 'http://localhost:8000/v1',  # base_url，也称为 api_base
    # 'api_key': 'EMPTY',

    # （可选） LLM 的超参数：
    'generate_cfg': {
        'top_p': 0.8
    }
}

# 调用成本较高
qwen_vl_max_llm_cfg = {
    'model': 'qwen-vl-max-latest',
    'model_type': 'qwenvl_dashscope',
    'api_key': DASHSCOPE_API_KEY,  # 从环境变量读取 api_key
    'generate_cfg': {
        'top_p': 0.8
    }
}

# 调用成本低
qwen_vl_plus_llm_cfg = {
    'model': 'qwen-vl-plus-latest',
    'model_type': 'qwenvl_dashscope',
    'api_key': DASHSCOPE_API_KEY,  # 从环境变量读取 api_key
    'generate_cfg': {
        'top_p': 0.8
    }
}