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
        "expires_at": time.time() + 86400  # 24 hours (increased from 30 minutes)
    }
    
    save_access_codes(codes)
    return code

def verify_access_code(code):
    """Verify an access code and return developer name if valid."""
    try:
        codes = load_access_codes()
        
        if code not in codes:
            print(f"Access code '{code}' not found. Please check your code or ask for a new one.")
            return None
        
        code_data = codes[code]
        
        # Check if code is expired
        if time.time() > code_data["expires_at"]:
            print(f"Access code expired. It was valid until {time.ctime(code_data['expires_at'])}")
            print("Please ask for a new access code.")
            del codes[code]
            save_access_codes(codes)
            return None
        
        name = code_data["name"]
        # Remove the code after use
        del codes[code]
        save_access_codes(codes)
        return name
    except Exception as e:
        print(f"Error verifying access code: {e}")
        print("Please contact your system administrator.")
        return None

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
    try:
        # Ensure directory exists
        Path(tool_path).parent.mkdir(exist_ok=True, parents=True)
        print(f"Created directory: {os.path.dirname(tool_path)}")
        
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
        print(f"Created file: {tool_path}")
    except Exception as e:
        print(f"Error creating tool file: {e}")
        raise
    
    # Make executable
    try:
        os.chmod(tool_path, 0o755)
        print(f"Made executable: {tool_path}")
    except Exception as e:
        print(f"Warning: Could not make file executable: {e}")
    
    # Create docs file
    try:
        docs_path = f"docs/tools/{tool_name}.md"
        Path(docs_path).parent.mkdir(exist_ok=True, parents=True)
        print(f"Created directory: {os.path.dirname(docs_path)}")
        
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
        print(f"Created file: {docs_path}")
    except Exception as e:
        print(f"Error creating docs file: {e}")
    
    # Create test file
    try:
        test_path = f"tests/test_{tool_name}.py"
        Path(test_path).parent.mkdir(exist_ok=True, parents=True)
        print(f"Created directory: {os.path.dirname(test_path)}")
        
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
        print(f"Created file: {test_path}")
    except Exception as e:
        print(f"Error creating test file: {e}")
    
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
    try:
        # Check if we're in XwDevTools directory
        current_dir = os.getcwd()
        if not os.path.exists(os.path.join(current_dir, "XwDevTools")):
            # Try to change to XwDevTools if it exists
            if os.path.exists("XwDevTools"):
                os.chdir("XwDevTools")
                print("✅ Changed to XwDevTools directory")
            else:
                print("❌ XwDevTools directory not found. Please run 'xwgit init' first.")
                return
        
        # Determine tool type directory
        tool_dir = "search"  # Default
        if hasattr(args, 'type'):
            if args.type == "search":
                tool_dir = "search"
            elif args.type == "api":
                tool_dir = "api"
            else:
                tool_dir = args.type
        
        # Set up paths
        tool_path = f"xwtools/{tool_dir}/{args.name}.py"
        
        # Make sure xwtools directory exists
        if not os.path.exists("xwtools"):
            os.makedirs("xwtools", exist_ok=True)
            print("✅ Created xwtools directory")
        
        if not os.path.exists(f"xwtools/{tool_dir}"):
            os.makedirs(f"xwtools/{tool_dir}", exist_ok=True)
            print(f"✅ Created xwtools/{tool_dir} directory")
        
        # Try to create a feature branch
        try:
            branch_name = f"feature/{args.name}-{int(time.time())}"
            subprocess.run(["git", "checkout", "-b", branch_name], check=False)
            print(f"✅ Created branch: {branch_name}")
        except Exception as e:
            print(f"⚠️ Could not create git branch: {e}")
            print("Continuing without branch creation...")
        
        # Create tool files
        create_tool_files(tool_path, args.name, tool_dir, args.description)
        
        print("\n✨ Tool scaffolding complete!")
        print("\nNext steps:")
        print(f"1. Edit {tool_path} to implement your tool")
        print(f"2. Edit docs/tools/{args.name}.md to document your tool")
        print(f"3. Run tests with: python tests/test_{args.name}.py")
        print("4. When finished, run: xwgit finalize \"Implement tool functionality\"")
    except Exception as e:
        print(f"❌ Error during quickstart: {e}")
        print("Please check error message and try again, or contact your administrator.")

def validate_changes(quiet=False):
    """Validate that changes are ready to commit."""
    issues = []
    warnings = []
    
    # Check git status to make sure there are changes
    git_status = subprocess.check_output(["git", "status", "--porcelain"], text=True)
    if not git_status.strip():
        issues.append("No changes to commit. Make some changes first.")
    
    # Check for Python syntax errors in changed files
    changed_py_files = []
    for line in git_status.splitlines():
        if line[0] != 'D' and line[-3:] == '.py':  # Not deleted and is Python
            file_path = line[3:].strip()
            changed_py_files.append(file_path)
    
    for file_path in changed_py_files:
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            compile(code, file_path, 'exec')  # Check for syntax errors
        except SyntaxError as e:
            issues.append(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            warnings.append(f"Warning: Could not check {file_path}: {e}")
    
    # Check for missing documentation
    tool_files = []
    doc_files = []
    for line in git_status.splitlines():
        if line[0] != 'D':  # Not deleted
            file_path = line[3:].strip()
            if file_path.startswith('xwtools/') and file_path.endswith('.py'):
                tool_name = os.path.basename(file_path)[:-3]  # Remove .py extension
                tool_files.append(tool_name)
            elif file_path.startswith('docs/tools/') and file_path.endswith('.md'):
                doc_name = os.path.basename(file_path)[:-3]  # Remove .md extension
                doc_files.append(doc_name)
    
    for tool in tool_files:
        if tool not in doc_files:
            warnings.append(f"Warning: Documentation missing for {tool}. Create docs/tools/{tool}.md.")
    
    # Report validation results
    if not quiet:
        if issues:
            print("\n❌ Validation found issues that must be fixed:")
            for issue in issues:
                print(f"  - {issue}")
            
        if warnings:
            print("\n⚠️ Validation found items to consider:")
            for warning in warnings:
                print(f"  - {warning}")
            
        if not issues and not warnings:
            print("\n✅ Validation passed! Changes look good.")
    
    return len(issues) == 0  # Return True if no issues

def cmd_finalize(args):
    """Finalize changes by committing and pushing."""
    # Validate changes first
    print("Validating changes...")
    if not validate_changes():
        print("\n❌ Please fix the issues before finalizing.")
        
        if args.force:
            print("\n⚠️ --force option used. Continuing despite issues...")
        else:
            print("\nTip: Run ./xwgit status to see current state.")
            print("     Use --force to override validation if needed.")
            return
    
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

def cmd_status(args):
    """Display the current status of the workspace."""
    print("XwGit Workspace Status")
    print("=====================")
    
    # Check git status
    try:
        git_status = subprocess.check_output(["git", "status", "--porcelain"], text=True)
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        
        print(f"Current branch: {branch}")
        
        if git_status.strip():
            print("\nUncommitted changes:")
            for line in git_status.splitlines():
                print(f"  {line}")
        else:
            print("\nWorking directory clean. No uncommitted changes.")
            
        # Check last commit
        last_commit = subprocess.check_output(
            ["git", "log", "-1", "--pretty=format:%h - %s (%ar)"], 
            text=True
        ).strip()
        print(f"\nLast commit: {last_commit}")
        
        # Show tool files
        try:
            tools_path = "xwtools"
            if os.path.exists(tools_path):
                print("\nTools in workspace:")
                for root, dirs, files in os.walk(tools_path):
                    for file in files:
                        if file.endswith(".py"):
                            rel_path = os.path.join(root, file)
                            print(f"  {rel_path}")
            else:
                print("\nNo tools directory found.")
        except Exception:
            pass
            
    except subprocess.CalledProcessError:
        print("Not in a git repository or git is not installed.")
    except Exception as e:
        print(f"Error checking status: {e}")
        
    print("\nNext steps:")
    print("1. Create a tool: ./xwgit quickstart tool_name")
    print("2. Edit the tool files")
    print("3. Finalize changes: ./xwgit finalize \"Implement functionality\"")

def cmd_help(args):
    """Show detailed help for a specific command."""
    command = args.command if hasattr(args, 'command') and args.command else "general"
    
    help_text = {
        "general": """
XwGit - Streamlined GitHub Workflow for AI Developers

Commands:
  init        Initialize workspace with access code
  quickstart  Create a new tool from templates
  status      Show current workspace status
  finalize    Commit changes with a message
  help        Show help for specific commands

Example workflow:
  ./xwgit init --code YOUR_ACCESS_CODE
  ./xwgit quickstart my_tool --description="Useful utility"
  # Edit the generated files
  ./xwgit status
  ./xwgit finalize "Implement my_tool functionality"
""",
        "init": """
Initialize the workspace with your access code.

Usage:
  ./xwgit init --code YOUR_ACCESS_CODE

This command will:
1. Verify your access code
2. Set up your development environment
3. Prepare for tool creation

After initialization, use 'quickstart' to create your first tool.
""",
        "quickstart": """
Create a new tool from templates.

Usage:
  ./xwgit quickstart tool_name --description="Tool description" --type=search

Options:
  --description  Brief description of the tool
  --type         Tool type (search, api, etc.)

This command will:
1. Create a feature branch
2. Generate tool implementation file
3. Generate documentation file
4. Generate test file

Example:
  ./xwgit quickstart web_search --description="Web search utility" --type=search
""",
        "status": """
Show the current status of your workspace.

Usage:
  ./xwgit status

This command will display:
1. Current branch
2. Uncommitted changes
3. Last commit
4. Tools in your workspace
5. Suggested next steps
""",
        "finalize": """
Commit your changes with a message.

Usage:
  ./xwgit finalize "Your commit message" [--issue=NUMBER]

Options:
  --issue  Associated issue number

This command will:
1. Stage all changes
2. Create a commit with your message
3. Prepare for review

Example:
  ./xwgit finalize "Implement web search functionality" --issue=42
"""
    }
    
    print(help_text.get(command, "Help topic not found."))

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
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show current workspace status")
    
    # Finalize command
    final_parser = subparsers.add_parser("finalize", help="Finalize changes")
    final_parser.add_argument("message", help="Commit message")
    final_parser.add_argument("--issue", type=int, help="Issue number")
    final_parser.add_argument("--force", action="store_true", help="Force finalization even with validation issues")
    
    # Help command
    help_parser = subparsers.add_parser("help", help="Show detailed help for commands")
    help_parser.add_argument("command", nargs="?", help="Command to get help on")
    
    args = parser.parse_args()
    
    if args.command == "generate-code":
        cmd_generate_code(args)
    elif args.command == "init":
        cmd_init(args)
    elif args.command == "quickstart":
        cmd_quickstart(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "finalize":
        cmd_finalize(args)
    elif args.command == "help":
        cmd_help(args)
    else:
        cmd_help(argparse.Namespace(command="general"))

if __name__ == "__main__":
    main()