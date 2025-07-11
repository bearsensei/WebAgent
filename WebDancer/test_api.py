#!/usr/bin/env python3
"""
Simple test script for the web-dancer API
"""

import os
import openai

# API Configuration
os.environ['OPENAI_API_KEY'] = 'sk-To4CAwrB7qgWLxmqF0756cF8C21d4a60983a608dEaEcF348'
os.environ['OPENAI_API_BASE'] = 'https://oneapi.hkgai.net/v1'

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    base_url=os.environ['OPENAI_API_BASE']
)

def test_api():
    """Test the API connection"""
    try:
        # Simple test message
        response = client.chat.completions.create(
            model="web-dancer",
            messages=[
                {"role": "user", "content": "Hello! Can you introduce yourself briefly?"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        print("✅ API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def test_function_calling():
    """Test function calling capability"""
    try:
        response = client.chat.completions.create(
            model="web-dancer",
            messages=[
                {"role": "user", "content": "What's the weather like today?"}
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get the current weather for a location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA"
                                }
                            },
                            "required": ["location"]
                        }
                    }
                }
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        print("✅ Function calling test successful!")
        print(f"Response: {response.choices[0].message}")
        return True
        
    except Exception as e:
        print(f"❌ Function calling test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing web-dancer API...")
    print("=" * 50)
    
    # Test basic API connection
    test_api()
    print()
    
    # Test function calling
    test_function_calling() 