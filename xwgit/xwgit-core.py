#!/usr/bin/env python3
"""
XwGit - Ultra-simple GitHub access for AI developers
v0.1 - Minimal Viable Product
"""

import os
import time
import json
import argparse
import subprocess
import sys
import secrets
import string
from pathlib import Path

# Configuration
CONFIG_DIR = Path.home() / ".xwgit"
CONFIG_FILE = CONFIG_DIR / "config.json"
CODES_FILE = CONFIG_DIR / "codes.json"
CONFIG_DIR.mkdir(exist_ok=True)

# Default values - override with config file
DEFAULT_CONFIG = {
    "organization": "xwander-dev",
    "repository": "XwDevTools",
}

def load_config():
    """Load configuration from file or use defaults."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def load_access_codes():
    """Load existing access codes."""
    if CODES_FILE.exists():
        with open(CODES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_access_codes(codes):
    """Save access codes to file."""
    with open(CODES_FILE, "w") as f:
        json.dump(codes, f, indent=2)

def generate_access_code(name):
    """Generate a simple access code for an AI developer."""
    # Load existing codes
    codes = load_access_codes()
    
    # Generate a random code
    alphabet = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(alphabet) for _ in range(8))
    
    # Store the code with metadata
    codes[code] = {
        "name": name,
        "created_at": time.time(),
        "expires_at": time.time() + 1800  # 30 minutes
    }
    
    save_access_codes(codes)
    return code

def verify_access_code(code):
    """Verify an access code and return developer name if valid."""
    codes = load_access_codes()
    
    if code not in codes:
        return None
    
    code_data = codes[code]
    
    # Check if code is expired
    if time.time() > code_data["expires_at"]:
        del codes[code]
        save_access_codes(codes)
        return None
    
    name = code_data["name"]
    # Remove the code after use
    del codes[code]
    save_access_codes(codes)
    return name

def setup_git_identity(name):
    """Set up git identity for an AI developer."""
    subprocess.run(["git", "config", "--local", "user.name", f"AI-{name}"])
    subprocess.run(["git", "config", "--local", "user.email", f"{name.lower()}@ai.xwander.dev"])
    print(f"✅ Git identity set up for AI-{name}")

def clone_repository(token, organization, repository):
    """Clone a repository using a token."""
    # For MVP, we'll just use the public repo without token
    repo_url = f"https://github.com/{organization}/{repository}.git"
    subprocess.run(["git", "clone", repo_url])
    print(f"✅ Repository cloned: {organization}/{repository}")

def create_tool_files(tool_path, tool_name, tool_type, description):
    """Create tool files from templates."""
    # Ensure directory exists
    Path(tool_path).parent.mkdir(exist_ok=True, parents=True)
    
    # Create tool file
    with open(tool_path, "w") as f:
        f.write(f"""#!/usr/bin/env python3
\"\"\"
{tool_name}.py - {description}
\"\"\"

import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument("query", nargs="+", help="Query to process")
    args = parser.parse_args()
    
    query = " ".join(args.query)
    print(f"Processing: {{query}}")
    
    # TODO: Implement your tool functionality here

if __name__ == "__main__":
    main()
""")
    
    # Make executable
    os.chmod(tool_path, 0o755)
    
    # Create docs file
    docs_path = f"docs/tools/{tool_name}.md"
    Path(docs_path).parent.mkdir(exist_ok=True, parents=True)
    
    with open(docs_path, "w") as f:
        f.write(f"""# {tool_name}.py

## Overview

{description}

## Usage

```bash
./xwtools/{tool_type}/{tool_name}.py "your query"
```

## Features

- Feature 1 (TODO)
- Feature 2 (TODO)
""")
    
    # Create test file
    test_path = f"tests/test_{tool_name}.py"
    Path(test_path).parent.mkdir(exist_ok=True, parents=True)
    
    with open(test_path, "w") as f:
        f.write(f"""#!/usr/bin/env python3
\"\"\"
Test suite for {tool_name}.py
\"\"\"

import unittest
import sys
import os

# Add module to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Test{tool_name.capitalize()}(unittest.TestCase):
    \"\"\"Test suite for {tool_name}.py\"\"\"
    
    def test_basic(self):
        \"\"\"Basic test\"\"\"
        self.assertTrue(True)  # TODO: Replace with actual tests

if __name__ == "__main__":
    unittest.main()
""")
    
    print(f"✅ Created tool files for {tool_name}")
    print(f"  - Tool implementation: {tool_path}")
    print(f"  - Documentation: {docs_path}")
    print(f"  - Tests: {test_path}")

def cmd_generate_code(args):
    """Generate an access code for an AI developer."""
    config = load_config()
    
    # Generate code
    code = generate_access_code(args.name)
    
    # Display code
    print("\n" + "=" * 50)
    print(f"🔑 Access Code for {args.name}")
    print("=" * 50)
    print(f"Code: {code}")
    print(f"Valid for: 30 minutes")
    print("=" * 50)
    print("\nProvide this code to the AI developer with this command:")
    print(f"xwgit init --code {code}")
    print("\nThe code can only be used once and will expire after 30 minutes.")

def cmd_init(args):
    """Initialize repository access with an access code."""
    # Verify the access code
    name = verify_access_code(args.code)
    
    if not name:
        print("❌ Invalid or expired access code")
        return
    
    print(f"✅ Access code verified for {name}")
    
    # Load config
    config = load_config()
    
    # Clone repository
    try:
        clone_repository(None, config["organization"], config["repository"])
        os.chdir(config["repository"])
        setup_git_identity(name)
    except Exception as e:
        print(f"❌ Error setting up repository: {e}")
        return
    
    print("\n✨ Repository initialized successfully!")
    print("\nNext steps:")
    print("1. cd " + config["repository"])
    print("2. xwgit quickstart tool_name --description=\"Your tool description\"")

def cmd_quickstart(args):
    """Create a new tool from templates."""
    # Determine tool type directory
    if args.type == "search":
        tool_dir = "search"
    elif args.type == "api":
        tool_dir = "api"
    else:
        tool_dir = args.type
    
    # Set up paths
    tool_path = f"xwtools/{tool_dir}/{args.name}.py"
    
    # Create a feature branch
    branch_name = f"feature/{args.name}-{int(time.time())}"
    subprocess.run(["git", "checkout", "-b", branch_name])
    print(f"✅ Created branch: {branch_name}")
    
    # Create tool files
    create_tool_files(tool_path, args.name, tool_dir, args.description)
    
    print("\n✨ Tool scaffolding complete!")
    print("\nNext steps:")
    print(f"1. Edit {tool_path} to implement your tool")
    print(f"2. Edit docs/tools/{args.name}.md to document your tool")
    print(f"3. Run tests with: python tests/test_{args.name}.py")
    print("4. When finished, run: xwgit finalize \"Implement tool functionality\"")

def cmd_finalize(args):
    """Finalize changes by committing and pushing."""
    # Stage changes
    subprocess.run(["git", "add", "."])
    print("✅ Changes staged")
    
    # Create commit
    message = args.message
    if args.issue:
        message += f" (#{args.issue})"
    
    subprocess.run(["git", "commit", "-m", message])
    print(f"✅ Changes committed: {message}")
    
    # Get current branch
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    ).decode().strip()
    
    print(f"\n✨ Changes committed to branch: {branch}")
    print("\nNote: In this MVP version, changes are committed locally but not pushed.")
    print("A human teammate will need to push and create a PR.")

def main():
    """Main entry point for xwgit CLI."""
    parser = argparse.ArgumentParser(description="XwGit - GitHub access for AI developers")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Generate access code command
    gen_parser = subparsers.add_parser("generate-code", help="Generate access code for AI developer")
    gen_parser.add_argument("name", help="AI developer name (e.g., claude, ecom-agent)")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize with access code")
    init_parser.add_argument("--code", required=True, help="Access code")
    
    # Quickstart command
    quick_parser = subparsers.add_parser("quickstart", help="Create new tool")
    quick_parser.add_argument("name", help="Tool name")
    quick_parser.add_argument("--description", default="A useful tool", help="Tool description")
    quick_parser.add_argument("--type", default="search", help="Tool type (search, api, etc.)")
    
    # Finalize command
    final_parser = subparsers.add_parser("finalize", help="Finalize changes")
    final_parser.add_argument("message", help="Commit message")
    final_parser.add_argument("--issue", type=int, help="Issue number")
    
    args = parser.parse_args()
    
    if args.command == "generate-code":
        cmd_generate_code(args)
    elif args.command == "init":
        cmd_init(args)
    elif args.command == "quickstart":
        cmd_quickstart(args)
    elif args.command == "finalize":
        cmd_finalize(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()