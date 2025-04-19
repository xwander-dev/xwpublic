# XwanderDev Public Resources

This repository contains public resources for XwanderDev projects, primarily focused on onboarding and bootstrap utilities for AI assistants and developers.

## Contents

### Bootstrap Tools

- [xwgit.sh](bootstrap/xwgit.sh) - One-command onboarding script with interactive prompts
- [xwgit_bootstrap.py](bootstrap/xwgit_bootstrap.py) - Comprehensive Python utility for repository setup and AI workflow
- [setup_api_key.sh](bootstrap/setup_api_key.sh) - Script to configure API keys for any service

### Guides

- [Onboarding Guide](guides/onboarding.md) - Streamlined onboarding guide for AI developers
- [Tool Implementation Guides](guides/) - Specific guides for implementing various tools

### Tools

- [API Config Generator](tools/generate_api_config.py) - Generate configuration files for API keys

## Getting Started

If you're a new AI developer joining the XwanderDev team, start with the [Onboarding Guide](guides/onboarding.md).

### Ultra-Quick Start (30-Second Setup)

```bash
# One-command setup
bash <(curl -s https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit.sh)
```

### Alternative Manual Setup

```bash
# Download the bootstrap script
curl -O https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit_bootstrap.py
chmod +x xwgit_bootstrap.py

# Initialize with your GitHub token (provided by your human teammate)
./xwgit_bootstrap.py init --owner="xwander-dev" --repo="XwDevTools" --token="your_github_token"
```

## For Human Teammates

When onboarding a new AI assistant:

1. Direct them to this repository
2. Provide them with a GitHub token with appropriate permissions
3. Assign them a specific issue to work on
4. Share any necessary API keys securely

You can use the [API Config Generator](tools/generate_api_config.py) to create configuration files:

```bash
# Generate all config files
python tools/generate_api_config.py --all

# Generate specific config
python tools/generate_api_config.py --perplexity --perplexity-key="your_api_key"
```

## Security Notes

- Never commit API keys or tokens to repositories
- Use environment variables or config files for sensitive information
- The tools in this repository are designed to handle keys securely