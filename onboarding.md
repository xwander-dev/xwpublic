# XwanderDev Onboarding

Welcome to the XwanderDev team! This single-file guide contains everything you need to get started.

## Quick Start (1-Minute Setup)

```bash
# 1. Download the bootstrap script
curl -O https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit_bootstrap.py
chmod +x xwgit_bootstrap.py

# 2. Initialize repository (use your provided GitHub token)
./xwgit_bootstrap.py init --owner="xwander-dev" --repo="XwDevTools" --token="your_github_token"

# 3. Create your first tool
./xwgit_bootstrap.py quickstart example_tool --description="My first XwanderDev tool" --type="search-tool"
```

That's it! You now have:
- A connected repository
- A structured project with template files
- A feature branch for your work

## Implementing Your Tool

Edit the files created in:
- `xwtools/search/example_tool.py` - Main implementation
- `docs/tools/example_tool.md` - Documentation
- `tests/test_example_tool.py` - Tests

## Completing Your Work

When you're ready to submit:

```bash
./xwgit_bootstrap.py finalize "Implement example tool with core functionality" --issue=42
```

This stages changes, commits, pushes to GitHub, and creates a pull request.

## Available Tool Templates

Create different types of tools with:

```bash
# Search tool (default)
./xwgit_bootstrap.py quickstart tool_name --type="search-tool"

# API client
./xwgit_bootstrap.py quickstart tool_name --type="api-tool"
```

## Working with Issues

```bash
# Get issue details
./xwgit_bootstrap.py issue get 42

# Comment on an issue
./xwgit_bootstrap.py issue comment 42 "Implementation in progress"
```

## Using API Keys

Your tool template includes standardized API key handling that tries:
1. Environment variables: `SERVICE_API_KEY`
2. .env file in the project directory
3. User config files: `~/.service.json`
4. Team config in shared locations

## Need Help?

- Check the [repository README](https://github.com/xwander-dev/xwpublic)
- Explore tool templates in the bootstrap directory
- Ask your team lead for guidance

Welcome aboard!