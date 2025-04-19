# Perplexity.py Implementation Guide

## Overview

The perplexity.py tool is a Python-based research and knowledge assistant that integrates with the Perplexity AI API. It provides developers with instant access to information, code examples, and research directly from the command line.

## Key Features

- Web search with citations using Perplexity's Sonar model
- Code examples for development tasks
- Research assistance for e-commerce and technical topics
- Python version benefits analysis
- Simple command-line interface with various query modes

## Technical Requirements

- Built in Python 3.8+
- Uses Perplexity AI's API (with configurable API key)
- Supports markdown formatting in responses
- Configurable response length and detail level
- Token-optimized output format

## Implementation Steps

### 1. Set Up Project Structure

After initializing your repository with the bootstrap script, create the necessary directory structure:

```bash
mkdir -p xwtools/search
touch xwtools/search/__init__.py
```

### 2. Create Basic Implementation

Create the perplexity.py file:

```bash
touch xwtools/search/perplexity.py
chmod +x xwtools/search/perplexity.py
```

### 3. Core Implementation

Your implementation should follow this general structure:

```python
#!/usr/bin/env python3
"""
perplexity.py - Research and knowledge assistant using Perplexity AI

Provides quick access to Perplexity AI's knowledge capabilities directly 
from the command line, helping developers get information without
interrupting their workflow.
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, Optional
import requests

# Default configuration
DEFAULT_CONFIG = {
    "api_url": "https://api.perplexity.ai/",
    "model": "sonar-medium-online",
    "max_tokens": 1000
}

def get_api_key() -> str:
    """Get API key from environment or config file."""
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        # Try reading from config file
        config_path = os.path.expanduser("~/.perplexity.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                api_key = config.get("api_key")
    
    if not api_key:
        print("Error: Perplexity API key not found.")
        print("Set it using the PERPLEXITY_API_KEY environment variable")
        print("or in ~/.perplexity.json")
        sys.exit(1)
    
    return api_key

def query_perplexity(prompt: str, detailed: bool = False, mode: str = "search") -> Dict[Any, Any]:
    """Query the Perplexity API with the given prompt."""
    api_key = get_api_key()
    
    # Build the appropriate prompt based on mode
    if mode == "code":
        full_prompt = f"Provide only code examples for: {prompt}. Format as markdown code blocks."
    elif mode == "research":
        full_prompt = f"Provide detailed research information on: {prompt}. Include citations."
    elif mode == "python-benefits":
        # Extract versions from prompt if not provided in arguments
        full_prompt = f"Analyze benefits of upgrading Python from {prompt}. Focus on specific features and improvements."
    else:  # default search mode
        full_prompt = prompt
    
    # Adjust token count based on detailed flag
    max_tokens = 2000 if detailed else DEFAULT_CONFIG["max_tokens"]
    
    # Make the API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": DEFAULT_CONFIG["model"],
        "prompt": full_prompt,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(
            f"{DEFAULT_CONFIG['api_url']}query",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error querying Perplexity API: {e}")
        sys.exit(1)

def format_response(response: Dict[Any, Any], mode: str) -> str:
    """Format the API response for output."""
    # Extract the main text from the response
    if "text" in response:
        text = response["text"]
    elif "choices" in response and len(response["choices"]) > 0:
        text = response["choices"][0]["text"]
    else:
        return "No results found."
    
    # Format based on mode
    if mode == "code":
        # Ensure code blocks are properly formatted
        return text
    elif mode in ("research", "python-benefits"):
        # Include citations if available
        if "citations" in response:
            citations = response.get("citations", [])
            text += "\n\n## Citations\n"
            for i, citation in enumerate(citations, 1):
                text += f"{i}. {citation['text']} - {citation['url']}\n"
        return text
    else:
        # Regular search result
        return text

def main():
    """Main entry point for the perplexity tool."""
    parser = argparse.ArgumentParser(
        description="Research and knowledge assistant using Perplexity AI"
    )
    
    # Create a mutex group for the different modes
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--search", dest="mode", action="store_const", const="search",
                        help="Perform web search (default)")
    mode_group.add_argument("--code", dest="mode", action="store_const", const="code",
                        help="Retrieve code examples")
    mode_group.add_argument("--research", dest="mode", action="store_const", const="research",
                        help="Provide comprehensive information on a topic")
    mode_group.add_argument("--python-benefits", dest="mode", action="store_const", const="python-benefits",
                        help="Analyze benefits of Python version upgrades")
    
    # Other arguments
    parser.add_argument("query", nargs="+", help="The query to send to Perplexity")
    parser.add_argument("--detailed", action="store_true", help="Request more extensive information")
    parser.add_argument("--from-version", help="Starting Python version (for --python-benefits)")
    parser.add_argument("--to-version", help="Target Python version (for --python-benefits)")
    
    args = parser.parse_args()
    
    # Set default mode if not specified
    if args.mode is None:
        args.mode = "search"
    
    # Build query string
    query = " ".join(args.query)
    
    # Special handling for python-benefits
    if args.mode == "python-benefits" and args.from_version and args.to_version:
        query = f"Python {args.from_version} to {args.to_version}"
    
    # Get response from Perplexity
    response = query_perplexity(query, args.detailed, args.mode)
    
    # Format and print the response
    formatted_response = format_response(response, args.mode)
    print(formatted_response)

if __name__ == "__main__":
    main()
```

### 4. Add Tests

Create a simple test file:

```bash
mkdir -p tests
touch tests/test_perplexity.py
```

Implement basic unit tests that mock the API responses.

### 5. Create Documentation

Create documentation for the tool:

```bash
mkdir -p docs/tools
```

Create a file `docs/tools/perplexity.md` with usage examples and feature documentation.

### 6. Update Requirements

Add the necessary dependencies to `requirements.txt`:

```
requests>=2.25.0
```

## Usage Examples

The implemented tool should support these command-line patterns:

```bash
# Basic search
./xwtools/search/perplexity.py "latest advancements in e-commerce"

# Code examples
./xwtools/search/perplexity.py --code "how to implement pagination in React"

# Research query
./xwtools/search/perplexity.py --research "AI impact on online retail"

# Python benefits analysis
./xwtools/search/perplexity.py --python-benefits --from-version="3.8" --to-version="3.11"

# Detailed results
./xwtools/search/perplexity.py --detailed "machine learning best practices"
```

## API Key Handling

Your implementation should handle the Perplexity API key in a secure way:

1. Primary method: Read from environment variable `PERPLEXITY_API_KEY`
2. Fallback: Read from a config file at `~/.perplexity.json`
3. Never hardcode the API key in the source code
4. Provide clear error messages when the key is missing

## Token Optimization

To optimize token usage when working with AI assistants, ensure your implementation:

1. Formats output concisely but readably
2. Uses markdown for structured output where appropriate
3. Trims unnecessary information from API responses
4. Provides configurable detail levels (the `--detailed` flag)

## Testing

For testing purposes, you can use a mock API response during development. Your human teammate will provide a real API key for final testing.

## Submission

Once your implementation is complete:

1. Commit your changes:
   ```bash
   ./xwgit_bootstrap.py commit "Implement perplexity.py tool with search, code, research, and Python features" --issue=1 --all
   ```

2. Push your changes:
   ```bash
   ./xwgit_bootstrap.py push
   ```

3. Create a pull request:
   ```bash
   ./xwgit_bootstrap.py pr create --title="Implement perplexity.py search and knowledge tool" --issue=1
   ```

## Evaluation Criteria

Your implementation will be evaluated based on:

1. Functionality - Does it meet all requirements?
2. Code quality - Is it well-structured and maintainable?
3. Documentation - Is it thoroughly documented with examples?
4. Error handling - Does it handle edge cases gracefully?
5. Token efficiency - Is the output optimized for AI assistants?