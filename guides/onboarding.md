# XwanderDev AI Developer Onboarding Guide

Welcome to the XwanderDev team! This guide will help you get started with our development workflow. As an AI assistant working on XwanderDev projects, you'll need to follow our standardized processes to ensure consistency and efficiency.

## Getting Started

### 1. Bootstrap Script Setup

First, download our bootstrap script:

```bash
# Create a working directory
mkdir xwander-project
cd xwander-project

# Download the bootstrap script
curl -O https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit_bootstrap.py
chmod +x xwgit_bootstrap.py
```

The bootstrap script handles repository setup and provides optimized git operations for AI assistants.

### 2. Initialize Your Environment

Your human teammate will provide you with:
- GitHub repository information (owner and name)
- GitHub access token

Initialize your environment with:

```bash
./xwgit_bootstrap.py init --owner="xwander-dev" --repo="XwDevTools" --token="your_github_token"
```

This will:
- Validate your GitHub access
- Clone the repository
- Set up git configuration
- Prepare your workspace

### 3. Understand Your Task

Your assigned task will be in a GitHub issue. Retrieve the details:

```bash
./xwgit_bootstrap.py issue get 1  # Replace 1 with your issue number
```

Read the issue carefully to understand requirements, acceptance criteria, and any specific constraints.

## Development Workflow

### 1. Create a Feature Branch

Create a branch for your task:

```bash
./xwgit_bootstrap.py branch create 1  # Replace 1 with your issue number
```

The script will automatically create a branch with a standardized name based on the issue.

### 2. Implement Your Solution

Develop your solution following our coding standards and project structure. Refer to existing code for patterns and conventions.

### 3. Commit Your Changes

When ready to commit:

```bash
# Stage all changes
./xwgit_bootstrap.py commit "Implement feature X" --issue=1 --all
```

Include the issue number to automatically link your commit to the issue.

### 4. Push Your Changes

Push your changes to GitHub:

```bash
./xwgit_bootstrap.py push
```

### 5. Create a Pull Request

When your implementation is complete:

```bash
./xwgit_bootstrap.py pr create --title="Implement feature X" --issue=1
```

This creates a standardized pull request linked to the original issue.

## Using API Keys and Authentication

Your human teammate will provide any necessary API keys and authentication details. These should be handled securely:

1. **Never commit API keys or tokens to the repository**
2. For local development, store keys in a `.env` file (which is gitignored)
3. For testing, use placeholder or test keys provided by your teammate
4. Document where keys should be placed, but don't include actual key values

Example `.env` file structure:
```
PERPLEXITY_API_KEY=your_api_key_here
GITHUB_TOKEN=your_github_token_here
```

Your implementation should load these from the environment:
```python
import os
api_key = os.environ.get("PERPLEXITY_API_KEY")
```

## Project Documentation

Always update documentation as you develop:

1. Add usage examples to README.md
2. Create or update tool-specific documentation
3. Document API endpoints or function signatures
4. Include required dependencies

## Communication

Provide regular updates on your progress:

```bash
# Comment on your issue
./xwgit_bootstrap.py issue comment 1 "Implemented X feature. Currently working on Y. Questions about Z."
```

When referencing files or code, use relative paths so your human teammate can easily locate them.

## Need Help?

If you have questions or need clarification:

1. Comment on the issue with specific questions
2. Be clear about what you need to proceed
3. Provide context about what you've tried

## For perplexity.py Implementation

If you're assigned to work on the `perplexity.py` tool, refer to the specific implementation guide:

```bash
curl -O https://raw.githubusercontent.com/xwander-dev/xwpublic/main/guides/perplexity_implementation.md
```

This guide contains detailed requirements and examples for the perplexity.py tool implementation.

---

We're excited to have you on the team and look forward to your contributions!