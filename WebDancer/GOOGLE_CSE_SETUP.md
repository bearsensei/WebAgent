# Google Custom Search Engine 设置指南

## 步骤 1: 创建 Custom Search Engine

1. 访问 https://cse.google.com/
2. 点击 "Create a search engine"
3. 在 "Sites to search" 中输入：
   - 要搜索特定网站：输入网站URL
   - 要搜索整个网络：输入 `www.google.com`
4. 点击 "Create"
5. 复制生成的 **Search engine ID** (以 `012345678901234567890:abcdefghijk` 格式)

## 步骤 2: 配置环境变量

```bash
# 设置API密钥
export GOOGLE_SEARCH_KEY='AIzaSyC3OG0apMunAKiMCoGE0gSXSXZEpx8lBpY'

# 设置Custom Search Engine ID
export GOOGLE_CSE_ID='4457fc1ca04294641'
```

## 步骤 3: 测试配置

```bash
python test_search_api.py
```

## 步骤 4: 运行WebDancer

```bash
python simple_webdancer.py
```

## 注意事项

- Google Custom Search API 每天有100次免费查询限制
- 如果需要更多查询，需要升级到付费计划
- Custom Search Engine 可以配置为搜索特定网站或整个网络
- 建议为不同用途创建不同的Custom Search Engine

## 故障排除

如果遇到 "403 Forbidden" 错误：
1. 检查API密钥是否正确
2. 确保Custom Search Engine ID正确
3. 检查是否启用了Custom Search API
4. 验证配额是否用完 