# 网站内容提取与分析工具

本工具是一个高效的网站内容提取与分析平台。用户可以自动化地获取企业官网信息，提升信息收集效率，是企业调研、竞品分析和市场研究的理想选择。

[English](./readme_en.md) | [中文](./readme.md)

## 🖼️ 系统架构

![系统架构图](./images/architecture.png)

*图1：LLM搜索工具系统架构图*

## 🎯 效果展示

![效果展示](./images/demo.png)

*图2：系统效果展示*

## 项目初衷
本项目初衷是我开发的一个公司官网导航的自动化采集工具，能够通过搜索引擎获取公司官网，进行内容提取和分析，最终生成公司官网导航，目前，整个自动化采集官网信息提取功能已开源，公司官网导航信息生成功能正在开发中。大模型能力的代码整理后也将开源。
目前demo的项目地址：
http://yxxt.haomiaodata.com/
内容是采集的公司信息并基于模型提取的，目前还是demo版本，新版本的公司官网导航仍在开发中。

## 🤖 AI功能特性

### 🧠 智能内容处理
- **内容总结**: 自动生成网页内容的简洁总结
- **关键信息提取**: 智能提取公司名称、主营业务、联系方式等关键信息
- **内容分类**: 自动对网页内容进行分类标签
- **商业洞察**: 生成深度的商业分析和洞察

### 🔄 多种AI模型支持
- **OpenAI GPT**: 支持GPT-3.5-turbo、GPT-4等模型
- **本地模型**: 支持ChatGLM2、LLaMA等本地部署模型
- **灵活配置**: 可自定义模型参数和配置

### 📊 网站比较分析
- **竞品分析**: 自动比较两个网站的特点和差异
- **业务模式对比**: 分析不同企业的业务模式
- **市场定位**: 评估企业的市场定位和竞争优势

## 🚀 主要功能与API接口
本项目的API接口基于FastAPI框架构建，提供高效、灵活的接口服务。

### 🔍 智能搜索引擎集成 `/search`
- 支持Google、Bing、DuckDuckGo等主流搜索引擎
- 可配置搜索引擎类型 (`engine_name`) 和过滤文本长度 (`filter_text_len`)
- 返回结构化的搜索结果，包含URL、标题和描述
- 自动过滤无关内容，精准定位目标信息
- 支持关键词搜索和高级搜索语法

### 📄 网页内容智能提取 `/webpage_info`
- 支持多种解析工具 (`requests`/`selenium`/`playwright`)
- 自动提取网页标题、正文内容
- 可选返回完整的HTML结构
- 智能处理动态渲染页面
- 内置错误处理和重试机制
- 支持自定义解析规则和内容过滤

### 🔎 深度网站分析 `/analyze`
- 全面分析网站结构和资源分布
- 自动收集并分类内部/外部链接
- 智能提取公司信息（社交媒体、邮箱、电话、地址）
- 统计JS、CSS、图片等资源分布
- 生成详细的JSON格式分析报告
- 支持网站地图生成和目录结构分析
- 提供SEO相关数据分析

### 🚄 批量内容提取 `/extract`
- 支持多页面并行处理
- 可配置最大抓取页数 (`max_page`)
- 可控制是否返回HTML结构 (`need_soup`)
- 自动递归抓取相关页面
- 内置限速和负载均衡
- 支持自定义抓取规则和过滤条件
- 提供断点续传功能

### 🤖 AI智能处理接口

#### `/ai/extract_and_process` - 一键提取+AI处理
```bash
POST /ai/extract_and_process
{
    "url": "https://example.com",
    "max_page": 20,
    "need_soup": false
}
```
- 自动提取网站内容并用AI处理
- 返回原始内容和AI分析结果
- 包含总结、关键信息、分类、洞察等

#### `/ai/process` - AI内容处理
```bash
POST /ai/process
{
    "content": [{"title": "...", "text": "..."}],
    "process_type": "all",  # all, summary, key_info, categories, insights
    "max_summary_length": 500
}
```
- 对已有内容进行AI处理
- 支持多种处理类型
- 可自定义处理参数

#### `/ai/compare` - 网站比较分析
```bash
POST /ai/compare
{
    "website1_url": "https://company1.com",
    "website2_url": "https://company2.com",
    "max_page": 20
}
```
- 自动比较两个网站的特点
- 生成详细的对比分析报告
- 支持竞品分析和市场研究

#### `/ai/config` - AI配置管理
```bash
POST /ai/config
{
    "model_name": "gpt-3.5-turbo",
    "max_tokens": 2000,
    "temperature": 0.7,
    "use_local_model": false
}
```
- 动态配置AI模型参数
- 支持切换不同AI模型
- 实时调整处理参数

#### `/ai/status` - AI状态查询
```bash
GET /ai/status
```
- 查询当前AI处理器状态
- 显示当前配置信息
- 检查模型可用性

## ⚡ 快速开始

### 系统要求

- Python 3.9或更高版本
- Chrome浏览器（用于Selenium和Playwright渲染）
- 至少2GB可用内存
- 稳定的网络连接
- OpenAI API密钥（可选，用于AI功能）

### 🔧 安装步骤

1. 克隆代码库:
   ```bash
   git clone git@github.com:BetaStreetOmnis/WebAIExtracto.git
   ```

2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量:
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，设置你的OpenAI API密钥
   ```

4. 启动API服务:
   ```bash
   python api_server.py
   ```
   服务将在 [http://localhost:8093](http://localhost:8093) 启动，可通过Swagger UI查看完整API文档。

### 🤖 AI功能配置

#### 使用OpenAI API
1. 获取OpenAI API密钥
2. 在 `.env` 文件中设置：
   ```
   OPENAI_API_KEY=your_api_key_here
   AI_USE_LOCAL_MODEL=false
   ```

#### 使用本地模型
1. 下载本地模型（如ChatGLM2）
2. 在 `.env` 文件中设置：
   ```
   AI_USE_LOCAL_MODEL=true
   AI_LOCAL_MODEL_PATH=/path/to/your/model
   ```

### 📝 使用示例

#### 基本AI处理
```python
import requests

# 提取网站内容并用AI处理
response = requests.post("http://localhost:8093/ai/extract_and_process", json={
    "url": "https://example.com",
    "max_page": 10
})

result = response.json()
print("内容总结:", result['ai_analysis']['summary'])
print("关键信息:", result['ai_analysis']['key_info'])
```

#### 网站比较
```python
# 比较两个网站
response = requests.post("http://localhost:8093/ai/compare", json={
    "website1_url": "https://company1.com",
    "website2_url": "https://company2.com"
})

comparison = response.json()
print("比较分析:", comparison['comparison'])
```

运行完整示例：
```bash
python examples/ai_usage_example.py
```

## 🔧 配置说明

### 环境变量配置
- `OPENAI_API_KEY`: OpenAI API密钥
- `AI_MODEL_NAME`: AI模型名称（默认: gpt-3.5-turbo）
- `AI_MAX_TOKENS`: 最大token数（默认: 2000）
- `AI_TEMPERATURE`: 模型温度参数（默认: 0.7）
- `AI_USE_LOCAL_MODEL`: 是否使用本地模型（默认: false）
- `AI_LOCAL_MODEL_PATH`: 本地模型路径

### API参数说明
- `process_type`: 处理类型（all/summary/key_info/categories/insights）
- `max_summary_length`: 总结最大长度
- `max_page`: 最大抓取页面数
- `temperature`: AI模型温度参数

## 📊 性能优化

### AI处理优化
- 支持批量处理多个页面
- 智能文本去重和清理
- 可配置的处理参数
- 错误重试机制

### 内存管理
- 分页处理大量内容
- 智能缓存机制
- 内存使用监控

## 🔒 安全考虑

- API密钥安全存储
- 请求频率限制
- 内容过滤和清理
- 错误信息脱敏

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

本项目采用MIT许可证，详见 [LICENSE](LICENSE) 文件。

