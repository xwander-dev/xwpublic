# XwDevTools Contribution Guidelines

These are the official guidelines for contributing to the XwDevTools repository.

## Directory Structure

Place your work in the appropriate locations:

```
XwDevTools/
├── xwtools/            # Tool implementations
│   └── [category]/     # Use existing category or create a new one
├── docs/               # Documentation
│   └── tools/          # Tool-specific documentation
└── tests/              # Test implementations
```

## Implementation Requirements

1. **Follow Standard Patterns**:
   - Use shebang line: `#!/usr/bin/env python3`
   - Make files executable: `chmod +x your_file.py`
   - Add docstrings to describe functionality

2. **Error Handling**:
   - Handle common error cases
   - Provide useful error messages
   - Fail gracefully when possible

3. **API Keys and Configuration**:
   - Read from environment variables in `.env` file
   - Never hardcode credentials

## Documentation

Each tool should have:
- Clear usage examples
- Description of all options
- Installation steps if needed

## Committing Your Work

Use the provided GitHub tool:

```bash
# Navigate to workspace
cd /srv/www/erasoppi.fi/[YOUR_NAME]-workspace

# Clone the repository
./github-tool.sh clone xwander-dev/XwDevTools
cd XwDevTools

# Add your code following guidelines above

# Commit when ready
./github-tool.sh commit "Add [tool-name]: Brief description"
```

## Code Style

- Use clear, descriptive names
- Follow standard conventions for the language
- Comment complex sections

That's it! Keep it simple and focus on delivering value.