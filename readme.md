# LLM搜索工具 - 智能网站内容分析与提取平台

这是一个基于FastAPI开发的高性能网站内容提取和分析工具。它提供了强大的API接口，能帮助用户自动化获取网站信息，提高信息收集效率，是企业调研、竞品分析、市场研究的得力助手。

## 🚀 主要功能与API接口

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

## 🖼️ 系统架构

![系统架构图](https://your-repo-url.com/path-to-architecture-diagram.png)

*图1：LLM搜索工具系统架构图*

## ⚡ 快速开始

### 系统要求

- Python 3.9或更高版本
- Chrome浏览器（用于Selenium和Playwright渲染）
- 至少2GB可用内存
- 稳定的网络连接

### 🔧 安装步骤

1. 克隆代码库:
   ```bash
   git clone git@github.com:BetaStreetOmnis/WebAIExtracto.git
   ```

2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

3. 启动API服务:
   ```bash
   python api_server.py
   ```
   服务将在 [http://localhost:8093](http://localhost:8093) 启动，可通过Swagger UI查看完整API文档。

## 📝 API调用示例

### 1. 搜索接口调用 `/search`

#### 请求示例
```bash
curl -X POST "http://localhost:8093/search" -H "Content-Type: application/json" -d '{
  "keyword": "人工智能",
  "engine_name": "google",
  "filter_text_len": 50
}'
```

#### 响应示例
```json
[
  {
    "href": "https://example.com/ai",
    "title": "人工智能简介",
    "description": "介绍人工智能的基本概念和发展历史。"
  },
  {
    "href": "https://example.com/ai-applications",
    "title": "人工智能的应用领域",
    "description": "探讨人工智能在各个行业的应用案例。"
  }
]
```

### 2. 网页内容提取 `/webpage_info`

#### 请求示例
```bash
curl -X POST "http://localhost:8093/webpage_info" -H "Content-Type: application/json" -d '{
  "url": "https://www.example.com",
  "tool_type": "playwright"
}'
```

#### 响应示例
```json
{
  "title": "示例网站",
  "text": "这是一个示例网站，用于展示内容提取的功能。",
  "soup": "<!DOCTYPE html>...</html>"
}
```

### 3. 网站分析 `/analyze`

#### 请求示例
```bash
curl -X POST "http://localhost:8093/analyze" -H "Content-Type: application/json" -d '{
  "url": "https://www.example.com",
  "useai": 1,
  "num_level": 2,
  "max_page": 10,
  "need_soup": true
}'
```

#### 响应示例
```json
{
  "assets": {
    "js": ["app.js", "utils.js"],
    "css": ["style.css"],
    "html": ["index.html"],
    "php": [],
    "images": ["logo.png", "banner.jpg"]
  },
  "links": {
    "internal": ["https://www.example.com/about", "https://www.example.com/contact"],
    "external": ["https://www.google.com", "https://www.facebook.com"],
    "directory": ["https://www.example.com/blog/"]
  },
  "company_info": {
    "social_media": ["https://twitter.com/example", "https://linkedin.com/company/example"],
    "emails": ["contact@example.com"],
    "phone_numbers": ["+1234567890"],
    "addresses": ["示例市示例区示例路123号"]
  },
  "statistics": {
    "js_files": 2,
    "css_files": 1,
    "html_files": 1,
    "php_files": 0,
    "images": 2,
    "internal_links": 2,
    "external_links": 2
  }
}
```

### 4. 批量内容提取 `/extract`

#### 请求示例
```bash
curl -X POST "http://localhost:8093/extract" -H "Content-Type: application/json" -d '{
  "url": "https://www.example.com",
  "useai": 1,
  "num_level": 3,
  "max_page": 15,
  "need_soup": false
}'
```

#### 响应示例
```json
{
  "content": [
    {
      "url": "https://www.example.com/page1",
      "title": "页面1标题",
      "text": "页面1的正文内容..."
    },
    {
      "url": "https://www.example.com/page2",
      "title": "页面2标题",
      "text": "页面2的正文内容..."
    }
    // 更多页面内容
  ],
  "job_urls": [
    "https://www.example.com/page1",
    "https://www.example.com/page2"
    // 更多URL
  ]
}
```

# 联系我们

如有任何问题或建议，请通过以下方式联系我们：

- 邮箱: ch824783054@gmail.com
- 电话: +86 18883179204

# 许可协议

本项目采用Apache-2.0许可证，详情请参阅 [LICENSE](./LICENSE)。

