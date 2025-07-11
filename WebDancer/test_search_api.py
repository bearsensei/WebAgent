#!/usr/bin/env python3
"""
Test script for Google Custom Search API
"""

import os
import requests
import json

def test_google_custom_search_api():
    """Test Google Custom Search API"""
    api_key = os.getenv('GOOGLE_SEARCH_KEY', 'AIzaSyC3OG0apMunAKiMCoGE0gSXSXZEpx8lBpY')
    search_engine_id = os.getenv('GOOGLE_CSE_ID', '4457fc1ca04294641')
    
    if not api_key:
        print("❌ GOOGLE_SEARCH_KEY not set")
        return False
    
    if not search_engine_id:
        print("❌ GOOGLE_CSE_ID not set")
        print("   Set up a Custom Search Engine at https://cse.google.com/")
        return False
    
    print(f"🔍 Testing Google Custom Search API with key: {api_key[:10]}...")
    print(f"🔍 Search Engine ID: {search_engine_id[:10]}...")
    
    try:
        url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': 'Python programming',
            'num': 3
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            if "items" in results:
                print(f"   ✅ Success! Found {len(results['items'])} results")
                for i, result in enumerate(results['items'][:2], 1):
                    print(f"   {i}. {result.get('title', 'No title')}")
                return True
            else:
                print(f"   ❌ No items found: {results}")
                return False
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def main():
    
    
    """Test Google Custom Search API"""
    print("🧪 Testing Google Custom Search API")
    print("=" * 50)
    
    # Check environment variables
    google_key = os.getenv('GOOGLE_SEARCH_KEY', '')
    cse_id = os.getenv('GOOGLE_CSE_ID', '')
    
    print("Current API configuration:")
    print(f"  GOOGLE_SEARCH_KEY: {'✅ Set' if google_key else '❌ Not set'}")
    print(f"  GOOGLE_CSE_ID: {'✅ Set' if cse_id else '❌ Not set'}")
    print()
    
    # Test API
    if google_key and cse_id:
        success = test_google_custom_search_api()
        print("\n" + "=" * 50)
        print("Test Results:")
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  Google Custom Search API: {status}")
    else:
        print("❌ Missing required configuration")
        print("\nTo configure Google Custom Search API:")
        print("1. Get API key from: https://console.cloud.google.com/")
        print("2. Set up Custom Search Engine at: https://cse.google.com/")
        print("3. Set environment variables:")
        print("   export GOOGLE_SEARCH_KEY='your_api_key'")
        print("   export GOOGLE_CSE_ID='your_search_engine_id'")

if __name__ == "__main__":
    main() 