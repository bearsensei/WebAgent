# WebDancer Web Search Setup

这个文档说明如何为 `simple_webdancer.py` 配置真实的web搜索功能。

## 支持的搜索API

### 1. Serper.dev (推荐)
- **提供商**: Serper.dev
- **特点**: 提供真实的Google搜索结果
- **价格**: 每月1000次免费查询
- **获取API密钥**: https://serper.dev/

### 2. SerpAPI
- **提供商**: SerpAPI
- **特点**: 支持多种搜索引擎
- **价格**: 有免费额度
- **获取API密钥**: https://serpapi.com/

### 3. Jina API
- **提供商**: Jina
- **特点**: AI增强搜索
- **价格**: 相对较贵
- **获取API密钥**: https://jina.ai/api-dashboard/

## 快速设置

### 方法1: 使用设置脚本
```bash
python setup_search.py
```

### 方法2: 手动设置环境变量
```bash
# 设置Serper.dev API
export GOOGLE_SEARCH_KEY='your_serper_api_key_here'

# 或者设置SerpAPI
export SERPAPI_KEY='your_serpapi_key_here'

# 或者设置Jina API
export JINA_API_KEY='your_jina_api_key_here'
```

### 方法3: 使用.env文件
```bash
# 复制配置示例
cp config_example.env .env

# 编辑.env文件，填入您的API密钥
nano .env
```

## 运行WebDancer

设置完成后，运行：
```bash
python simple_webdancer.py
```

## 功能特性

### 1. 智能搜索
- 支持多种搜索API
- 自动选择可用的API
- 错误处理和重试机制

### 2. 网站访问
- 自动访问搜索结果中的网站
- 提取网页内容
- 内容清理和格式化

### 3. 工具调用处理
- 解析模型响应中的工具调用
- 执行搜索和访问操作
- 格式化输出结果

## 示例对话

```
👤 You: 什么是人工智能？

🤖 WebDancer is thinking...

🤔 Thinking: 用户询问什么是人工智能，这是一个需要搜索网络信息的问题。我应该使用搜索工具来获取最新的、权威的信息。

🔧 Using tool: search
   Arguments: {'query': '什么是人工智能'}
   Result: Google search for '什么是人工智能' found 10 results:

## Web Results

1. [人工智能 - 维基百科](https://zh.wikipedia.org/wiki/人工智能)
Date published: 2024-01-15
Source: zh.wikipedia.org
人工智能（Artificial Intelligence，AI）是计算机科学的一个分支...

2. [人工智能：定义、类型和应用](https://www.ibm.com/ai)
Source: ibm.com
人工智能是指机器模拟人类智能的能力...

🤔 Thinking: 从搜索结果中，我获得了关于人工智能的基本定义和信息。现在我可以为用户提供一个全面的答案。

💡 Final Answer: 人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。这些任务包括学习、推理、感知、语言理解和问题解决等。人工智能技术已经在各个领域得到广泛应用，包括医疗、金融、教育、交通等。
```

## 故障排除

### 1. 搜索API未配置
```
⚠️  Warning: No search API configured. Web search will be simulated.
```
**解决方案**: 设置搜索API密钥

### 2. API密钥无效
```
❌ Search error: 401 - Unauthorized
```
**解决方案**: 检查API密钥是否正确

### 3. 网络连接问题
```
❌ Search error: Connection timeout
```
**解决方案**: 检查网络连接，或稍后重试

## 高级配置

### 自定义搜索参数
在 `simple_webdancer.py` 中可以修改：
- 搜索结果数量
- 超时时间
- 用户代理字符串

### 添加新的搜索API
1. 在 `SimpleWebDancer` 类中添加新的搜索方法
2. 在 `search_web` 方法中添加新的API检查
3. 更新环境变量检查

## 注意事项

1. **API限制**: 注意各API的查询限制和费用
2. **隐私**: 搜索查询可能被API提供商记录
3. **内容**: 网页内容可能包含不准确或过时的信息
4. **速率限制**: 避免过于频繁的API调用 