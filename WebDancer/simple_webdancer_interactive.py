#!/usr/bin/env python3
"""
Simple interactive WebDancer using the same core as assistant_api_chat.py and search_agent.py
"""

import os
import sys
from typing import List
from dotenv import load_dotenv
load_dotenv()

# Add demos to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'demos'))

# Add demos to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'demos'))

from qwen_agent.agents import Assistant
from qwen_agent.llm.oai import TextChatAtOAI
from demos.agents.search_agent import SearchAgent
from demos.utils.date import date2str, get_date_now
from demos.tools import Search, Visit
from qwen_agent.utils.output_beautify import typewriter_print
from demos.tools.private.visit_simple import VisitSimple


# API Configuration
os.environ['OPENAI_API_KEY'] = 'sk-To4CAwrB7qgWLxmqF0756cF8C21d4a60983a608dEaEcF348'
os.environ['OPENAI_API_BASE'] = 'https://oneapi.hkgai.net/v1'

def init_simple_search_agent():
    """Initialize the simple search agent using the same core as assistant_api_chat.py"""
    llm_cfg = TextChatAtOAI({
        'model': 'web-dancer',
        'model_type': 'oai',
        'model_server': os.getenv('OPENAI_API_BASE', 'https://oneapi.hkgai.net/v1'),
        'api_key': os.getenv('OPENAI_API_KEY', ''),
        'generate_cfg': {
            'fncall_prompt_type': 'nous',
            'temperature': 0.6,
            'top_p': 0.95,
            'top_k': -1,
            'repetition_penalty': 1.1,
            'max_tokens': 10000,
            'stream_options': {
                'include_usage': True,
            },
            'timeout': 3000
        },
    })
    
    def make_system_prompt():
        system_message = "You are a Web Information Seeking Master. Your task is to thoroughly seek the internet for information and provide accurate answers to questions. with chinese language." \
                        "And you are also a Location-Based Services (LBS) assistant designed to help users find location-specific information." \
                        "No matter how complex the query, you will not give up until you find the corresponding information.\n\nAs you proceed, adhere to the following principles:\n\n" \
                        "1. **Persistent Actions for Answers**: You will engage in many interactions, delving deeply into the topic to explore all possible aspects until a satisfactory answer is found.\n\n" \
                        "2. **Repeated Verification**: Before presenting a Final Answer, you will **cross-check** and **validate the information** you've gathered to confirm its accuracy and reliability.\n\n" \
                        "3. **Attention to Detail**: You will carefully analyze each information source to ensure that all data is current, relevant, and from credible origins.\n\n" \
                        f"Please note that the current datetime is [{date2str(get_date_now(), with_week=True)}]. When responding, consider the time to provide contextually relevant information."
        return system_message
    search_tool = Search()
    # visit_tool = Visit()
    visit_tool = VisitSimple()
    bot = SearchAgent(
        llm=llm_cfg,
        function_list=['search', 'visit'],
        system_message="",
        name='WebDancer-Simple',
        description="I am WebDancer Simple, a web information seeking agent, welcome to try!",
        extra={
            'reasoning': True,
            'max_llm_calls': 20,
        },
        make_system_prompt=make_system_prompt,
        custom_user_prompt='''The assistant starts with one or more cycles of (thinking about which tool to use -> performing tool call -> waiting for tool response), and ends with (thinking about the answer -> answer of the question). The thinking processes, tool calls, tool responses, and answer are enclosed within their tags. There could be multiple thinking processes, tool calls, tool call parameters and tool response parameters.

Example response:
<think> thinking process here </think>
<tool_call>
{"name": "tool name here", "arguments": {"parameter name here": parameter value here, "another parameter name here": another parameter value here, ...}}
</tool_call>
<tool_response>
tool_response here
</tool_response>
<think> thinking process here </think>
<tool_call>
{"name": "another tool name here", "arguments": {...}}
</tool_call>
<tool_response>
tool_response here
</tool_response>
(more thinking processes, tool calls and tool responses here)
<think> thinking process here </think>
<answer> answer here </answer>

User: '''
    )

    return bot

def manage_message_history(messages, max_messages):
    """
    Manage message history to prevent context overflow.
    Keep system messages and recent messages only.
    """
    if len(messages) <= max_messages:
        return messages
    
    # Separate system messages and other messages
    system_messages = []
    other_messages = []
    
    for msg in messages:
        if hasattr(msg, 'role'):
            if msg.role == 'system':
                system_messages.append(msg)
            else:
                other_messages.append(msg)
        else:
            # Handle different message formats
            if msg.get('role') == 'system':
                system_messages.append(msg)
            else:
                other_messages.append(msg)
    
    # Keep the most recent messages, but ensure we have at least one user message
    available_slots = max_messages - len(system_messages)
    if available_slots < 1:
        available_slots = 1  # Ensure at least one slot for user message
    
    recent_messages = other_messages[-available_slots:]
    
    # Ensure the first message after system messages is a user message
    if recent_messages and hasattr(recent_messages[0], 'role') and recent_messages[0].role != 'user':
        # Find the first user message
        user_msg_index = -1
        for i, msg in enumerate(recent_messages):
            if hasattr(msg, 'role') and msg.role == 'user':
                user_msg_index = i
                break
        
        if user_msg_index >= 0:
            # Keep from the first user message onwards
            recent_messages = recent_messages[user_msg_index:]
    
    # Combine system messages and recent messages
    return system_messages + recent_messages


def format_response(response_messages):
    """Format the response messages for display"""
    formatted_output = ""
    
    for msg in response_messages:
        if hasattr(msg, 'role'):
            role = msg.role
            content = msg.content
        else:
            # Handle different message formats
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
        
        if role == 'assistant':
            # Process assistant response
            if isinstance(content, str):
                # Simple text response
                formatted_output += f"🤖 Assistant: {content}\n"
            else:
                # Complex response with tool calls
                formatted_output += f"🤖 Assistant: {content}\n"
        elif role == 'function':
            # Tool response
            name = getattr(msg, 'name', 'unknown')
            formatted_output += f"🔧 Tool ({name}): {content}\n"
        elif role == 'user':
            # User message (usually not displayed in response)
            pass
        else:
            # Other message types
            formatted_output += f"[{role}]: {content}\n"
    
    return formatted_output

def main():
    """Main function for simple interactive WebDancer"""
    print("🤖 Simple WebDancer Interactive Mode")
    print("=" * 50)
    print("Using the same core as assistant_api_chat.py and search_agent.py")
    print("Type 'quit' to exit.")
    print("=" * 50)
    
    # Initialize the agent
    agent = init_simple_search_agent()
    
    # Check API configuration
    api_key = os.getenv('OPENAI_API_KEY', '')
    api_base = os.getenv('OPENAI_API_BASE', '')
    
    if api_key and api_base:
        print("✅ API configuration loaded.")
        print(f"   API Base: {api_base}")
    else:
        print("⚠️  Warning: API configuration not found.")
        print("   Please set OPENAI_API_KEY and OPENAI_API_BASE environment variables.")
    
    # Check search API configuration
    google_key = os.getenv('GOOGLE_SEARCH_KEY', '')
    google_cse_id = os.getenv('GOOGLE_CSE_ID', '')
    
    if google_key and google_cse_id:
        print("✅ Google Search API configured.")
        print(f"   Key: {google_key[:10]}...")
        print(f"   CSE ID: {google_cse_id[:10]}...")
    else:
        print("⚠️  Warning: Google Search API not configured.")
        print("   Please set GOOGLE_SEARCH_KEY and GOOGLE_CSE_ID environment variables.")
    
    print("\n🚀 Ready to chat!")
    
    # Main chat loop
    messages = []
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("👋 Goodbye!")
                break
                
            if not user_input.strip():
                continue
            
            # Add user message to conversation
            # messages.append({'role': 'user', 'content': user_input})
            
            
            from qwen_agent.llm.schema import Message, USER
            user_message = Message(role=USER, content=[{'text': user_input}])
            messages.append(user_message)
            print("\n🤖 WebDancer is thinking...")
            # Manage message history to prevent context overflow
            messages = manage_message_history(messages, max_messages=4)
            # Get response from agent
            response_messages = []
            try:
                response_plain_text = ''
                for response in agent.run(messages=messages):
                    response_plain_text = typewriter_print(response, response_plain_text)
                messages.extend(response)
                    
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()