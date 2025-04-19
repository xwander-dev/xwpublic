# Perplexity.py Implementation Guide for ecom-agent

## Welcome, ecom-agent!

This guide provides a step-by-step workflow for implementing the Perplexity.py search tool using our new streamlined process. The implementation follows the XwanderDev standards and leverages the Perplexity AI API for enhanced search capabilities.

## Ultra-Quick Setup (30 seconds)

```bash
# One-command setup
bash <(curl -s https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit.sh)
```

This will download the necessary tools, prompt for your GitHub token, and set up the repository.

## Project Setup (10 seconds)

After the onboarding script completes, you can immediately create the perplexity tool structure:

```bash
./xwgit_bootstrap.py quickstart perplexity --type="search-tool" --issue=42 --description="Search and knowledge utility using Perplexity AI" --api="perplexity"
```

This single command will:
1. Create the appropriate directory structure
2. Generate templated files with the correct imports
3. Set up the API key handling mechanism
4. Create a feature branch linked to the issue

## Working with Generated Files

The quickstart command will generate several files:

```
xwtools/search/perplexity.py       # Main implementation file
docs/tools/perplexity.md           # Documentation
tests/test_perplexity.py           # Test suite
```

### Core Implementation

Edit `xwtools/search/perplexity.py` to implement the Perplexity API integration. The file already includes:

- API key handling with multiple fallback paths
- Command-line argument parsing
- Basic structure for making API requests

### Key Implementation Requirements

#### 1. API Integration

Use the Perplexity API key provided for the team:

```python
# API key provided for the team
# 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
```

The API key handling is already in place through the template. You can use it directly:

```python
api_key = get_api_key("perplexity")
```

#### 2. Query Modes

Implement these specific query modes:
- `search`: General web search (default)
- `code`: Code examples only
- `research`: Detailed information with citations
- `python-benefits`: Analysis of Python version upgrades

#### 3. API Request Structure

```python
def query_perplexity(prompt, detailed=False, mode="search"):
    api_key = get_api_key("perplexity")
    
    # Adjust prompt based on mode
    if mode == "code":
        full_prompt = f"Provide only code examples for: {prompt}. Format as markdown code blocks."
    elif mode == "research":
        full_prompt = f"Provide detailed research information on: {prompt}. Include citations."
    elif mode == "python-benefits":
        full_prompt = f"Analyze benefits of upgrading Python from {prompt}. Focus on specific features and improvements."
    else:  # default search mode
        full_prompt = prompt
    
    # Make API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "sonar-medium-online",  # Perplexity's recommended model
        "prompt": full_prompt,
        "max_tokens": 2000 if detailed else 1000
    }
    
    response = requests.post(
        "https://api.perplexity.ai/query",
        headers=headers,
        json=data
    )
    response.raise_for_status()
    return response.json()
```

#### 4. Response Formatting

Implement a function to format the API response:

```python
def format_response(response, mode):
    # Extract the main text
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
```

#### 5. Command-line Interface

The template already provides a basic CLI structure. Enhance it with the specific modes:

```python
def main():
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
    
    # Set default mode
    if args.mode is None:
        args.mode = "search"
    
    # Build query string
    query = " ".join(args.query)
    
    # Special handling for python-benefits
    if args.mode == "python-benefits" and args.from_version and args.to_version:
        query = f"Python {args.from_version} to {args.to_version}"
    
    # Query Perplexity and format response
    response = query_perplexity(query, args.detailed, args.mode)
    formatted_response = format_response(response, args.mode)
    print(formatted_response)
```

## Testing Your Implementation

You can test your implementation with:

```bash
# Basic search
./xwtools/search/perplexity.py "latest advancements in e-commerce"

# Code examples
./xwtools/search/perplexity.py --code "implement pagination in React"

# Research query
./xwtools/search/perplexity.py --research "AI impact on online retail"

# Python benefits analysis
./xwtools/search/perplexity.py --python-benefits --from-version="3.8" --to-version="3.11"
```

## Finalizing Your Work (5 seconds)

Once implementation is complete, a single command will finalize everything:

```bash
./xwgit_bootstrap.py finalize "Implement Perplexity search utility with web, code, and research capabilities" --issue=42
```

This command will:
1. Stage all your changes
2. Create a commit with the message
3. Push changes to the remote repository
4. Create a pull request linked to the issue

## Token Optimization for AI Agents

As an AI assistant, your implementation should focus on token optimization:

1. Use the provided template structure which is already optimized
2. Maintain concise code with minimal comments
3. Format output in a readable yet compact way
4. Use the `--detailed` flag to allow users to control verbosity

## Questions?

If you have any questions during implementation, please refer to:
- The API documentation in the template files
- The main onboarding guide at `/guides/onboarding.md`
- Issue #42 for specific requirements

Good luck with your implementation, ecom-agent! This streamlined workflow should make the process smooth and efficient.