#!/usr/bin/env python3
"""
Setup script for WebDancer search APIs
"""

import os
import getpass

def setup_search_apis():
    """Setup search API keys"""
    print("🔧 WebDancer Search API Setup")
    print("=" * 50)
    
    # Check current environment
    current_keys = {
        'GOOGLE_SEARCH_KEY': os.getenv('GOOGLE_SEARCH_KEY', ''),
        'SERPAPI_KEY': os.getenv('SERPAPI_KEY', ''),
        'JINA_API_KEY': os.getenv('JINA_API_KEY', '')
    }
    
    print("Current API keys:")
    for key, value in current_keys.items():
        status = "✅ Set" if value else "❌ Not set"
        print(f"  {key}: {status}")
    
    print("\nChoose which search API to configure:")
    print("1. Serper.dev (Google Search) - Recommended")
    print("2. SerpAPI")
    print("3. Jina API")
    print("4. Skip")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🔍 Setting up Serper.dev (Google Search API)")
        print("Get your API key from: https://serper.dev/")
        api_key = getpass.getpass("Enter your Serper.dev API key: ")
        if api_key:
            os.environ['GOOGLE_SEARCH_KEY'] = api_key
            print("✅ Serper.dev API key set!")
            
    elif choice == "2":
        print("\n🔍 Setting up SerpAPI")
        print("Get your API key from: https://serpapi.com/")
        api_key = getpass.getpass("Enter your SerpAPI key: ")
        if api_key:
            os.environ['SERPAPI_KEY'] = api_key
            print("✅ SerpAPI key set!")
            
    elif choice == "3":
        print("\n🔍 Setting up Jina API")
        print("Get your API key from: https://jina.ai/api-dashboard/")
        api_key = getpass.getpass("Enter your Jina API key: ")
        if api_key:
            os.environ['JINA_API_KEY'] = api_key
            print("✅ Jina API key set!")
    
    elif choice == "4":
        print("Skipping API setup.")
        return
    
    else:
        print("Invalid choice. Skipping API setup.")
        return
    
    # Test the configuration
    print("\n🧪 Testing search configuration...")
    test_search()

def test_search():
    """Test the search functionality"""
    try:
        from simple_webdancer import SimpleWebDancer
        agent = SimpleWebDancer()
        
        # Check which API is configured
        if agent.google_search_key:
            print("✅ Serper.dev API configured")
            api_type = "Serper.dev"
        elif agent.serpapi_key:
            print("✅ SerpAPI configured")
            api_type = "SerpAPI"
        elif agent.jina_api_key:
            print("✅ Jina API configured")
            api_type = "Jina"
        else:
            print("❌ No search API configured")
            return
        
        # Test with a simple query
        print(f"\n🔍 Testing {api_type} with query: 'Python programming'")
        result = agent.search_web("Python programming")
        
        if "Search error" in result or "No search API configured" in result:
            print("❌ Search test failed:")
            print(result)
        else:
            print("✅ Search test successful!")
            print("First few lines of result:")
            lines = result.split('\n')[:5]
            for line in lines:
                print(f"  {line}")
                
    except Exception as e:
        print(f"❌ Error testing search: {e}")

def save_to_env_file():
    """Save API keys to .env file"""
    env_content = []
    
    # Add existing environment variables
    env_content.append("# WebDancer API Configuration")
    env_content.append(f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY', 'sk-To4CAwrB7qgWLxmqF0756cF8C21d4a60983a608dEaEcF348')}")
    env_content.append(f"OPENAI_API_BASE={os.getenv('OPENAI_API_BASE', 'https://oneapi.hkgai.net/v1')}")
    
    # Add search API keys
    google_key = os.getenv('GOOGLE_SEARCH_KEY', '')
    serpapi_key = os.getenv('SERPAPI_KEY', '')
    jina_key = os.getenv('JINA_API_KEY', '')
    
    if google_key:
        env_content.append(f"GOOGLE_SEARCH_KEY={google_key}")
    if serpapi_key:
        env_content.append(f"SERPAPI_KEY={serpapi_key}")
    if jina_key:
        env_content.append(f"JINA_API_KEY={jina_key}")
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write('\n'.join(env_content))
    
    print("✅ Configuration saved to .env file")

if __name__ == "__main__":
    setup_search_apis()
    
    # Ask if user wants to save to .env file
    save_choice = input("\nSave configuration to .env file? (y/n): ").strip().lower()
    if save_choice == 'y':
        save_to_env_file()
    
    print("\n🎉 Setup complete! You can now run:")
    print("  python simple_webdancer.py") 