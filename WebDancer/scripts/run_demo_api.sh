#!/bin/bash

cd $(dirname $0) || exit

# API Configuration for web-dancer model
export OPENAI_API_KEY='sk-To4CAwrB7qgWLxmqF0756cF8C21d4a60983a608dEaEcF348'
export OPENAI_API_BASE='https://oneapi.hkgai.net/v1'
export OPENAI_API_KEY2='sk-9t5Zkm3FG7Y4vRUCBc89Ad73B4244eA8B531402f0bFa2c60'
# GOOGLE_SEARCH_KEY (optional - for search functionality)
export GOOGLE_SEARCH_KEY='AIzaSyCNAbYIc7iEOlSpd1r8ziyzFkSSJkcBVa0'
export GOOGLE_CSE_ID='8545488a3237a4d40'
# JINA_API_KEY (optional - for web search)
export JINA_API_KEY='jina_18cc2c86ee1749e1ace765709833fbd7mojT4tFQB_0LLPlUjZYlJNQOWPNE'

cd ..

python -m demos.assistant_api_chat   