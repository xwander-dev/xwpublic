# XwGit: AI Developer Guide

Welcome to the XwanderDev team! This guide is designed for AI developers to contribute to our repositories with minimal friction.

## Starting Your Work

Your sysadmin has already prepared a workspace for you with all necessary tools. You should have received:
1. A workspace path (e.g., `/shared/ai-workspace/ecom-agent-workspace`)
2. An access code (e.g., `XGZF6VOC`)

## Simple Workflow (3 Commands Only)

### 1. Initialize Your Session

```bash
# Navigate to your workspace
cd /shared/ai-workspace/ecom-agent-workspace

# Initialize your session with your access code
xwgit init --code XGZF6VOC
```

### 2. Create a New Tool

```bash
# Create a tool using templates
xwgit quickstart my_tool --description="A useful utility for XwanderDev" --type=search
```

This creates:
- A feature branch
- Tool implementation file: `xwtools/search/my_tool.py`
- Documentation: `docs/tools/my_tool.md`
- Tests: `tests/test_my_tool.py`

### 3. Implement and Finalize

Edit the generated files to implement your tool. Once done:

```bash
# Commit your changes
xwgit finalize "Implement my_tool functionality"
```

That's it! Your changes are now committed and ready for review.

## Working with Existing Files

If you need to edit existing files:

```bash
# Edit a file (any text editor works)
nano xwtools/search/existing_tool.py

# When done, commit your changes
xwgit finalize "Fix bug in existing_tool"
```

## Example: Creating a Search Tool

```bash
# Create a new search tool
xwgit quickstart web_search --description="Web search utility using external APIs" --type=search

# Edit the implementation
nano xwtools/search/web_search.py

# Edit the documentation
nano docs/tools/web_search.md

# Run tests (optional)
python tests/test_web_search.py

# Finalize your work
xwgit finalize "Implement web search functionality"
```

## Common Issues

- **Wrong workspace**: Make sure you're in your assigned workspace directory
- **Invalid access code**: Access codes expire after 30 minutes; ask for a new one
- **Permission errors**: Notify your sysadmin if you encounter permission issues