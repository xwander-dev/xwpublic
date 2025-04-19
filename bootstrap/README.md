# XwanderDev Bootstrap Tools

This directory contains tools for rapidly onboarding to XwanderDev projects and streamlining the development workflow.

## Quick Start

Use our ultra-quick setup script to get started in 30 seconds:

```bash
bash <(curl -s https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit.sh)
```

## Available Tools

### xwgit.sh

A one-command shell script for setting up the entire development environment. This script:

- Downloads the necessary Python bootstrap tool
- Prompts for GitHub credentials if needed
- Configures the repository
- Provides next steps for development

### xwgit_bootstrap.py

A comprehensive Python utility that handles:

- Repository setup and configuration
- Project structure generation from templates
- GitHub operations (issues, branches, PRs)
- Automated commit and PR workflows

### setup_api_key.sh

A utility for configuring API keys for any service:

- Interactive prompts for service name and API key
- Configures keys in multiple locations for redundancy
- Sets up environment variables
- Creates local configuration files

## Key Features

- **Ultra-streamlined workflow**: Get from zero to productive in 30 seconds
- **Template-based development**: Auto-generates project structures and files
- **Automated Git operations**: Simplifies branching, committing, and PR creation
- **API key management**: Standardized handling of API credentials 
- **Token optimization**: Built specifically for AI assistants to reduce token usage

## Usage Examples

### One-Step Setup

```bash
bash <(curl -s https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit.sh)
```

### Feature Creation

```bash
./xwgit_bootstrap.py quickstart feature_name --type="search-tool" --issue=42 --description="Feature description"
```

### Project Finalization

```bash
./xwgit_bootstrap.py finalize "Implement feature X" --issue=42
```

## Documentation

For more detailed information, see:
- [Onboarding Guide](../guides/onboarding.md)
- [Tool-specific implementation guides](../guides/)