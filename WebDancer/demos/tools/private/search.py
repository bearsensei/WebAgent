import os
import json
import requests
from typing import List
from qwen_agent.tools.base import BaseTool, register_tool
from concurrent.futures import ThreadPoolExecutor

MAX_MULTIQUERY_NUM = os.getenv("MAX_MULTIQUERY_NUM", 3)
GOOGLE_SEARCH_KEY = os.getenv("GOOGLE_SEARCH_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

@register_tool("search", allow_overwrite=True)
class Search(BaseTool):
    name = "search"
    description = "Performs batched web searches: supply an array 'query'; the tool retrieves the top 10 results for each query in one call."
    parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "array",
                    "items": {
                    "type": "string"
                    },
                    "description": "Array of query strings. Include multiple complementary search queries in a single call."
                },
            },
        "required": ["query"],
    }

    def call(self, params: str, **kwargs) -> str:
        # Check if we have the required API credentials
        if not GOOGLE_SEARCH_KEY or not GOOGLE_CSE_ID:
            return "[Search] Please set both GOOGLE_SEARCH_KEY and GOOGLE_CSE_ID environment variables for Google Custom Search API."
        
        # Improved parameter parsing
        try:
            # Handle different parameter formats
            if isinstance(params, str):
                # Try to parse as JSON string
                try:
                    params = json.loads(params)
                except json.JSONDecodeError:
                    # If it's not valid JSON, treat as single query
                    params = {"query": [params]}
            elif isinstance(params, dict):
                # Already a dict, use as is
                pass
            else:
                return "[Search] Invalid parameter format"
            
            # Extract query
            if "query" not in params:
                return "[Search] Missing 'query' field in parameters"
            
            query = params["query"]
            
            # Handle different query formats
            if isinstance(query, str):
                query = [query]
            elif isinstance(query, list):
                query = query[:MAX_MULTIQUERY_NUM]
            else:
                return "[Search] Query must be a string or array of strings"
                
        except Exception as e:
            return f"[Search] Error parsing parameters: {str(e)}"

        # Execute search
        if len(query) == 1:
            response = self.google_custom_search(query[0])
        else:
            with ThreadPoolExecutor(max_workers=3) as executor:
                responses = list(executor.map(self.google_custom_search, query))
            response = "\n=======\n".join(responses)
        
        return response

    def google_custom_search(self, query: str) -> str:
        """Search using Google Custom Search API"""
        url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'key': GOOGLE_SEARCH_KEY,
            'cx': GOOGLE_CSE_ID,
            'q': query,
            'gl': 'cn',
            'num': 10
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                raise Exception(f"Error: {response.status_code} - {response.text}")

            results = response.json()
            
            if "items" not in results:
                return f"No results found for query: '{query}'. Try a more general query."
            
            web_snippets = []
            for idx, page in enumerate(results["items"][:10], 1):
                title = page.get('title', 'No title')
                link = page.get('link', '#')
                snippet = page.get('snippet', 'No description')
                
                result = f"{idx}. [{title}]({link})\n{snippet}"
                web_snippets.append(result)
            
            content = f"Google Custom Search for '{query}' found {len(web_snippets)} results:\n\n## Web Results\n" + "\n\n".join(web_snippets)
            return content
            
        except Exception as e:
            return f"Search error: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    search_tool = Search()
