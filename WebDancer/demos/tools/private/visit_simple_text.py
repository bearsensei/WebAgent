import os
import requests
from qwen_agent.tools.base import BaseTool, register_tool
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

MAX_MULTIQUERY_NUM = os.getenv("MAX_MULTIQUERY_NUM", 3)
JINA_API_KEY = os.getenv("JINA_API_KEY")

def jina_readpage(url: str) -> str:
    """Read webpage content using Jina service."""
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
    }
    max_retries = 3
    timeout = 10
    
    for attempt in range(max_retries):
        try:
            response = requests.get(
                f"https://r.jina.ai/{url}",
                headers=headers,
                timeout=timeout
            )
            if response.status_code == 200:
                webpage_content = response.text
                return webpage_content
            else:
                print(response.text)
                raise ValueError("jina readpage error")
        except Exception as e:
            if attempt == max_retries - 1:
                return "[visit] Failed to read page."
            
    return "[visit] Failed to read page."

def simple_text_processing(content: str, goal: str) -> str:
    """Simple text processing without LLM"""
    # 移除HTML标签
    content = re.sub(r'<[^>]+>', '', content)
    
    # 移除多余的空白字符
    content = re.sub(r'\s+', ' ', content).strip()
    
    # 限制长度
    if len(content) > 2000:
        content = content[:2000] + "..."
    
    # 简单的关键词匹配
    goal_keywords = goal.lower().split()
    relevant_lines = []
    
    for line in content.split('\n'):
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in goal_keywords):
            relevant_lines.append(line)
    
    if relevant_lines:
        return "\n".join(relevant_lines[:10])  # 最多10行相关内容
    else:
        return content[:1000]  # 返回前1000个字符

@register_tool('visit', allow_overwrite=True)
class VisitSimpleText(BaseTool):
    name = 'visit'
    description = 'Visit webpage(s) and return the content summary using simple text processing.'
    parameters = {
        "type": "object",
        "properties": {
            "url": {
                "type": ["string", "array"],
                "items": {
                    "type": "string"
                },
                "minItems": 1,
                "description": "The URL(s) of the webpage(s) to visit. Can be a single URL or an array of URLs."
            },
            "goal": {
                "type": "string",
                "description": "The goal of the visit for webpage(s)."
            }
        },
        "required": ["url", "goal"]
    }

    def call(self, params: str, **kwargs) -> str:
        try:
            if isinstance(params, str):
                import json
                params = json.loads(params)
            
            url = params["url"]
            goal = params["goal"]
        except:
            return "[Visit] Invalid request format: Input must be a JSON object containing 'url' and 'goal' fields"
        
        if isinstance(url, str):
            response = self.readpage(url, goal)
        else:
            response = []
            assert isinstance(url, List)
            with ThreadPoolExecutor(max_workers=MAX_MULTIQUERY_NUM) as executor:
                futures = {executor.submit(self.readpage, u, goal): u for u in url}
                for future in as_completed(futures):
                    try:
                        response.append(future.result())
                    except Exception as e:
                        response.append(f"Error fetching {futures[future]}: {str(e)}")
            response = "\n=======\n".join(response)
        return response.strip()

    def readpage(self, url: str, goal: str) -> str:
        """Read webpage content using Jina and process with simple text processing."""
        content = jina_readpage(url)
        
        if content and not content.startswith("[visit] Failed to read page.") and content != "[visit] Empty content.":
            processed_content = simple_text_processing(content, goal)
            
            useful_information = f"Content from {url} for goal '{goal}':\n\n"
            useful_information += processed_content
            
            return useful_information
        else:
            return f"Failed to read content from {url}. Please check the URL or try again later."

if __name__ == '__main__':
    print(VisitSimpleText().readpage("https://github.com/callanwu/WebWalker-1?tab=readme-ov-file", "who are you?"))