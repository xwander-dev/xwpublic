# XwanderDev AI Developer Onboarding Guide

Welcome to the XwanderDev team! This guide provides a streamlined onboarding process for AI assistants working on XwanderDev projects.

## Ultra-Quick Start (30-Second Setup)

Run our one-command setup script:

```bash
bash <(curl -s https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit.sh)
```

This automated script will:
1. Download all necessary files
2. Prompt for GitHub token (or use from environment)
3. Configure the repository
4. Provide next steps

## Alternative Manual Setup (2-Minute Setup)

### 1. Download Bootstrap Script

```bash
curl -O https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit_bootstrap.py
chmod +x xwgit_bootstrap.py
```

### 2. One-Command Setup

```bash
./xwgit_bootstrap.py init --owner="xwander-dev" --repo="XwDevTools" --token="your_github_token"
```

### 3. Create Your Tool

```bash
./xwgit_bootstrap.py quickstart feature_name --issue=42 --description="Brief description of your tool"
```

### 4. Implement Your Tool

Edit the generated files in the directories created by the quickstart command, such as:
- The main implementation file
- Documentation files
- Test files

### 5. Finalize and Submit

```bash
./xwgit_bootstrap.py finalize "Implement feature with key functionality" --issue=42
```

That's it! Your code is now committed, pushed, and a pull request has been created.

## Key Features

The `xwgit_bootstrap.py` tool streamlines the entire development workflow:

- **One-Command Setup**: Initialize repository with a single command
- **Automatic Project Structure**: Creates directories, files, and templates
- **Simplified Git Operations**: Handles branching, commits, and PRs
- **API Key Management**: Standardized API key handling
- **Consistent Documentation**: Auto-generates documentation templates

## Commands Reference

### Initial Setup

```bash
# Basic setup with token
./xwgit_bootstrap.py init --owner="xwander-dev" --repo="XwDevTools" --token="your_token"

# Setup with token from file
./xwgit_bootstrap.py init --owner="xwander-dev" --repo="XwDevTools" --token-file=".env"
```

### Tool Development

```bash
# Quick start a search tool
./xwgit_bootstrap.py quickstart tool_name --type="search-tool" --issue=42

# Quick start an API client
./xwgit_bootstrap.py quickstart tool_name --type="api-tool" --issue=42
```

### Issue Management

```bash
# Get issue details
./xwgit_bootstrap.py issue get 42

# Comment on an issue
./xwgit_bootstrap.py issue comment 42 "Implementation in progress. Question about X."
```

### Git Operations

```bash
# Create branch for issue
./xwgit_bootstrap.py branch create 42

# Commit changes
./xwgit_bootstrap.py commit "Add feature X" --issue=42 --all

# Push changes
./xwgit_bootstrap.py push
```

### Finalizing Work

```bash
# Finalize (stages, commits, pushes, creates PR)
./xwgit_bootstrap.py finalize "Implement feature X" --issue=42
```

## API Key Configuration

Your human teammate will provide API keys as needed. The tool templates include standardized API key handling:

```python
# Example API key retrieval in generated code
def get_api_key(key_name="service_name"):
    """Get API key from environment or team config."""
    # Try environment variable
    api_key = os.environ.get(key_name.upper() + "_API_KEY")
    
    # Try .env file
    if not api_key and os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith(key_name.upper() + "_API_KEY="):
                    api_key = line.strip().split("=", 1)[1].strip("\"' ")
    
    # ... additional lookup methods ...
    
    return api_key
```

## Tool-Specific Implementation Guides

For specific tools you're assigned to implement, your team lead may provide additional tool-specific guides with detailed requirements and examples. These will be available in the `/guides` directory or provided to you directly.

## Next Steps

1. Explore the template files created by the quickstart command
2. Review the issue details for your assigned task
3. Implement the required functionality
4. Run tests to verify your implementation
5. Use the finalize command to submit your work

We're excited to have you on the team and look forward to your contributions!