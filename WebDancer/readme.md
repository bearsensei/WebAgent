# WebDancer for HKGAI: Optimized Information Seeking Agent


## 🎯 Overview

**WebDancer for HKGAI** is an enhanced information-seeking agent specifically optimized for Hong Kong context. This version includes several key improvements over the original WebDancer:

### ✨ Key Features

- **Enhanced Web Search**: Google Custom Search API with Hong Kong priority
- **Web Page Access**: Intelligent webpage analysis using Qwen3 model
- **Time Awareness**: Advanced temporal understanding ("today", "yesterday", "recent")
- **🇭🇰 HK-Optimized**: Prioritized Hong Kong websites for local queries
- **Dual Interface**: Command-line (CLI) and Web-based (GUI) interfaces
- **Simplified Architecture**: Removed DashScope dependency, using Qwen3 for content analysis

### Key Improvements

1. **Enhanced Time Awareness**: Better understanding of temporal references
2. **Simplified Model Stack**: Replaced DashScope with Qwen3 for content analysis
3. **Hong Kong Optimization**: Prioritized local websites for better accuracy
4. **Dual Deployment Options**: CLI for debugging, GUI for production use

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Conda** (recommended)
- **API Keys**: Google Search API + CSE ID, Jina API (optional)

### Step 1: Environment Setup

```bash
# Create conda environment
conda create -n webdancer python=3.12
conda activate webdancer

# Clone repository
git clone <repository-url>
cd WebDancer

# Install dependencies
pip install -r requirements.txt
```

> **💡 Tip**: For GPU environments, packages will automatically use GPU versions. For CPU-only environments, CPU versions will be installed.

### Step 2: API Configuration

#### Required APIs

1. **Google Search API**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Enable "Custom Search API"
   - Create API credentials
   - Get your **API Key**

2. **Google CSE ID**
   - Visit [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
   - Create a new search engine
   - Configure search scope (can be entire web)
   - Get your **Search Engine ID**

3. **Jina API** 
   - Visit [Jina AI](https://jina.ai/api-dashboard/)
   - Register and get your **API Key**

#### Configuration Methods

**Option A: Using .env file (Recommended)**

```bash
# Copy example configuration
cp config_example.env .env

# Edit with your API keys
nano .env
```

Add your keys:
```bash
OPENAI_API_KEY=sk-To4CAwrB7qgWLxmqF0756cF8C21d4a60983a608dEaEcF348
OPENAI_API_BASE=https://oneapi.hkgai.net/v1
GOOGLE_SEARCH_KEY=your_google_search_api_key
GOOGLE_CSE_ID=your_google_cse_id
JINA_API_KEY=your_jina_api_key
```

**Option B: Direct environment variables**

```bash
export GOOGLE_SEARCH_KEY="your_google_search_api_key"
export GOOGLE_CSE_ID="your_google_cse_id"
export JINA_API_KEY="your_jina_api_key"
```

### Step 3: Model Deployment

This version uses two models:

- **WebDancer 32B**: Core agent for information searching tasks
- **Qwen3 30B**: Content understanding for webpage analysis

Models are pre-deployed and ready to use.

### Step 4: Running WebDancer

#### Option A: Command Line Interface (CLI) - Recommended for Debugging

```bash
python simple_webdancer_interactive.py
```

**Features:**
- Quick debugging and testing
- Simple model interaction
- Real-time error messages
- Easy configuration testing

#### Option B: Web Interface (GUI) - Recommended for Production

```bash
cd scripts/
bash run_demo_api.sh
```

Then open your browser: `http://127.0.0.1:7860`

**Features:**
- User-friendly web interface
- Chat history
- File upload support
- Better user experience

## 🔧 Configuration Details

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ | OpenAI API key (pre-configured) |
| `OPENAI_API_BASE` | ✅ | API base URL (pre-configured) |
| `GOOGLE_SEARCH_KEY` | ✅ | Google Search API key |
| `GOOGLE_CSE_ID` | ✅ | Google Custom Search Engine ID |
| `JINA_API_KEY` | ✅ | Jina API key (for webpage access) |

### Model Configuration

```python
# WebDancer 32B - Core Agent
model: 'web-dancer'
max_tokens: 10000
temperature: 0.6

# Qwen3 30B - Content Analysis
model: 'HKGAI-Qwen3-32b'
max_tokens: 2000
temperature: 0.1
```
