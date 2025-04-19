#!/usr/bin/env python3
"""
xwgit.py - Streamlined GitHub workflow for AI developers (v0.3.1)

Token-efficient workflow tool for AI developers to contribute to GitHub repositories.
"""

import os
import sys
import json
import time
import re
import glob
import shutil
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

VERSION = "0.3.1"
WORKSPACE_PATH = os.path.expanduser("/srv/www/erasoppi.fi")
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
ENV_FILE = os.path.join(os.getcwd(), ".env")

# File templates for tool creation
TEMPLATES = {
    "tool": """#!/usr/bin/env python3
\"\"\"
{name}.py - {description}

A {category} tool for the XwDevTools repository.
\"\"\"

import os
import sys
import argparse
from typing import Dict, Any, Optional

def main():
    \"\"\"Main entry point for the {name} tool.\"\"\"
    parser = argparse.ArgumentParser(
        description="{description}"
    )
    
    # Add arguments here
    parser.add_argument("--example", help="Example argument")
    
    args = parser.parse_args()
    
    # Your implementation here
    print(f"Hello from {name}!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
""",
    
    "doc": """# {name_title}

## Description

{description}

## Installation

No special installation required. Ensure you have access to the XwDevTools repository.

## Usage

```bash
./xwtools/{category}/{name}.py --example value
```

## Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| --example | Example argument | No | None |

## Examples

Basic usage:

```bash
./xwtools/{category}/{name}.py --example test
```

## Configuration

This tool reads configuration from environment variables:

```
# Required in .env file
API_KEY=your_api_key_here
```

## Notes

- Handles errors gracefully
- Returns non-zero exit code on failure
""",
    
    "test": """#!/usr/bin/env python3
\"\"\"
Test suite for {name}.py
\"\"\"

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path to import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module to test
from xwtools.{category}.{name} import main

class Test{name_title}(unittest.TestCase):
    \"\"\"Test cases for {name}.py\"\"\"
    
    def setUp(self):
        \"\"\"Set up test fixtures\"\"\"
        pass
    
    def tearDown(self):
        \"\"\"Tear down test fixtures\"\"\"
        pass
    
    def test_main_function(self):
        \"\"\"Test that the main function runs without errors\"\"\"
        with patch('sys.argv', ['xwtools/{category}/{name}.py', '--example', 'test']):
            result = main()
            self.assertEqual(result, 0)
    
    # Add more test cases here

if __name__ == "__main__":
    unittest.main()
"""
}

# ==================== HELPER FUNCTIONS ====================

def get_github_token() -> Optional[str]:
    """Get GitHub token from .env file."""
    if not os.path.exists(ENV_FILE):
        return None
    
    with open(ENV_FILE, "r") as f:
        for line in f:
            if line.strip().startswith("GITHUB_TOKEN="):
                return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    
    return None

def ensure_directories(dirs: List[str]) -> bool:
    """Ensure specified directories exist."""
    for d in dirs:
        try:
            os.makedirs(d, exist_ok=True)
        except Exception as e:
            print(f"❌ Failed to create directory {d}: {e}")
            return False
    return True

def run_git_command(command: List[str], cwd: Optional[str] = None) -> Tuple[bool, str, str]:
    """Run a git command and return success status and output."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return True, result.stdout.strip(), ""
        else:
            return False, "", f"{result.stderr.strip()}\n{result.stdout.strip()}"
    except Exception as e:
        return False, "", str(e)

def configure_git() -> bool:
    """Configure git with token-based authentication."""
    # Check if git is already configured
    status, output, _ = run_git_command(["git", "config", "--get", "user.name"])
    if status and output:
        return True
    
    # Configure git
    try:
        subprocess.run(["git", "config", "--global", "user.name", "AI Developer"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "ai@xwander.dev"], check=True)
        subprocess.run(["git", "config", "--global", "--add", "safe.directory", "*"], check=True)
        return True
    except Exception as e:
        print(f"❌ Failed to configure git: {e}")
        return False

def check_and_configure_github_token() -> bool:
    """Check if GitHub token is available and configure if needed."""
    token = get_github_token()
    if not token:
        print("❌ GitHub token not found in .env file.")
        print("Please create a .env file with your GitHub token:")
        print('echo "GITHUB_TOKEN=your_token_here" > .env')
        return False
    
    return configure_git()

def find_repo_root() -> Optional[str]:
    """Find the repository root directory."""
    current_dir = os.getcwd()
    
    while current_dir != "/":
        if os.path.exists(os.path.join(current_dir, ".git")):
            return current_dir
        
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break
        
        current_dir = parent_dir
        
    return None

# ==================== COMMAND HANDLERS ====================

def fetch_command(args) -> bool:
    """Fetch a specific file or directory from a repository."""
    print(f"🔍 Fetching {args.type}/{args.path}...")
    
    # Ensure GitHub token is available
    if not check_and_configure_github_token():
        return False
    
    # Determine repository URL
    repo = args.repo if args.repo else "xwander-dev/XwDevTools"
    token = get_github_token()
    repo_url = f"https://{token}@github.com/{repo}.git"
    
    # Create a temporary directory
    temp_dir = os.path.join(os.getcwd(), f".xwgit-temp-{int(time.time())}")
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Initialize git in the temporary directory
        status, _, error = run_git_command(["git", "init"], cwd=temp_dir)
        if not status:
            print(f"❌ Failed to initialize git repository: {error}")
            shutil.rmtree(temp_dir)
            return False
        
        # Add remote
        status, _, error = run_git_command(
            ["git", "remote", "add", "origin", repo_url], 
            cwd=temp_dir
        )
        if not status:
            print(f"❌ Failed to add remote: {error}")
            shutil.rmtree(temp_dir)
            return False
        
        # Set up sparse checkout
        status, _, error = run_git_command(
            ["git", "config", "core.sparseCheckout", "true"], 
            cwd=temp_dir
        )
        if not status:
            print(f"❌ Failed to configure sparse checkout: {error}")
            shutil.rmtree(temp_dir)
            return False
        
        # Determine paths to fetch based on type
        sparse_checkout_path = os.path.join(temp_dir, ".git", "info", "sparse-checkout")
        
        if args.type == "tool":
            checkout_paths = [
                f"xwtools/{args.path}*",
                f"docs/tools/{os.path.basename(args.path)}*",
                f"tests/test_{os.path.basename(args.path)}*"
            ]
        else:
            checkout_paths = [args.path]
        
        # Write sparse checkout paths
        with open(sparse_checkout_path, "w") as f:
            f.write("\n".join(checkout_paths))
        
        # Fetch and checkout
        print("📥 Downloading files (sparse checkout)...")
        status, _, error = run_git_command(
            ["git", "fetch", "--depth=1", "origin", "main"], 
            cwd=temp_dir
        )
        if not status:
            print(f"❌ Failed to fetch repository: {error}")
            shutil.rmtree(temp_dir)
            return False
        
        status, _, error = run_git_command(
            ["git", "checkout", "FETCH_HEAD"], 
            cwd=temp_dir
        )
        if not status:
            print(f"❌ Failed to checkout files: {error}")
            shutil.rmtree(temp_dir)
            return False
        
        # Copy files to current directory
        files_found = False
        for path in checkout_paths:
            path = path.replace("*", "")
            source_path = os.path.join(temp_dir, path)
            if os.path.exists(source_path):
                dest_path = os.path.join(os.getcwd(), os.path.basename(path))
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(source_path, dest_path)
                files_found = True
                print(f"✅ Copied: {os.path.basename(path)}")
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        if files_found:
            print("✅ Fetch completed successfully!")
            return True
        else:
            print(f"❌ No files found for {args.path}")
            return False
            
    except Exception as e:
        print(f"❌ Error during fetch: {e}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return False

def clone_command(args) -> bool:
    """Clone a repository efficiently."""
    print(f"📥 Cloning {args.repo}...")
    
    # Check if GitHub token is available
    if not check_and_configure_github_token():
        return False
    
    # Check if repository already exists locally
    repo_name = args.repo.split("/")[-1]
    if os.path.exists(os.path.join(os.getcwd(), repo_name)):
        print(f"⚠️ Repository {repo_name} already exists locally.")
        return True
    
    # Clone the repository
    token = get_github_token()
    repo_url = f"https://{token}@github.com/{args.repo}.git"
    
    # Determine clone options
    clone_cmd = ["git", "clone"]
    
    if args.sparse:
        clone_cmd.extend(["--filter=blob:none", "--sparse"])
    
    if args.depth:
        clone_cmd.extend(["--depth", str(args.depth)])
    
    clone_cmd.append(repo_url)
    
    # Clone the repository
    status, _, error = run_git_command(clone_cmd)
    if not status:
        print(f"❌ Failed to clone repository: {error}")
        return False
    
    # Configure sparse checkout if requested
    if args.sparse and args.paths:
        try:
            # Set up sparse checkout
            os.chdir(repo_name)
            run_git_command(["git", "sparse-checkout", "init", "--cone"])
            
            # Add sparse checkout paths
            for path in args.paths.split(","):
                run_git_command(["git", "sparse-checkout", "add", path.strip()])
                
            os.chdir("..")
            
        except Exception as e:
            print(f"⚠️ Warning: Failed to configure sparse checkout: {e}")
    
    print(f"✅ Repository {repo_name} cloned successfully!")
    return True

def add_tool_command(args) -> bool:
    """Add a new tool to the repository."""
    print(f"🚀 Creating {args.name} tool in category {args.category}...")
    
    # Validate the tool name
    if not re.match(r'^[a-z0-9_-]+$', args.name):
        print(f"❌ Invalid tool name: {args.name}")
        print("Tool names can only contain lowercase letters, numbers, hyphens, and underscores.")
        return False
    
    # Validate the category
    valid_categories = ["utility", "search", "integration", "analysis"]
    if args.category not in valid_categories:
        print(f"❌ Invalid category: {args.category}")
        print(f"Valid categories: {', '.join(valid_categories)}")
        return False
    
    # Create necessary directories
    dirs = [
        f"xwtools/{args.category}", 
        "docs/tools", 
        "tests"
    ]
    
    if not ensure_directories(dirs):
        return False
    
    # Format template variables
    template_vars = {
        "name": args.name,
        "name_title": args.name.replace("-", " ").replace("_", " ").title(),
        "description": args.description,
        "category": args.category
    }
    
    # Create the files
    created_files = []
    
    # Tool implementation
    impl_file = f"xwtools/{args.category}/{args.name}.py"
    try:
        with open(impl_file, "w") as f:
            f.write(TEMPLATES["tool"].format(**template_vars))
        os.chmod(impl_file, 0o755)  # Make executable
        created_files.append(impl_file)
        print(f"✅ Created: {impl_file}")
    except Exception as e:
        print(f"❌ Failed to create {impl_file}: {e}")
        return False
    
    # Documentation
    doc_file = f"docs/tools/{args.name}.md"
    try:
        with open(doc_file, "w") as f:
            f.write(TEMPLATES["doc"].format(**template_vars))
        created_files.append(doc_file)
        print(f"✅ Created: {doc_file}")
    except Exception as e:
        print(f"❌ Failed to create {doc_file}: {e}")
        return False
    
    # Test file
    test_file = f"tests/test_{args.name}.py"
    try:
        with open(test_file, "w") as f:
            f.write(TEMPLATES["test"].format(**template_vars))
        os.chmod(test_file, 0o755)  # Make executable
        created_files.append(test_file)
        print(f"✅ Created: {test_file}")
    except Exception as e:
        print(f"❌ Failed to create {test_file}: {e}")
        return False
    
    # Commit the changes if requested
    if args.commit:
        # Check if in repository
        repo_root = find_repo_root()
        if not repo_root:
            print("⚠️ Not in a git repository. Cannot commit files.")
            print(f"✅ Files created successfully at: {', '.join(created_files)}")
            return True
            
        # Ensure git is configured
        if not check_and_configure_github_token():
            print("⚠️ Git is not properly configured. Cannot commit files.")
            print(f"✅ Files created successfully at: {', '.join(created_files)}")
            return True
            
        # Add and commit the files
        status, _, error = run_git_command(["git", "add"] + created_files)
        if not status:
            print(f"❌ Failed to stage files: {error}")
            print(f"✅ Files created successfully at: {', '.join(created_files)}")
            return True
            
        commit_message = f"Add {args.name}: {args.description}"
        status, _, error = run_git_command(["git", "commit", "-m", commit_message])
        if not status:
            print(f"❌ Failed to commit files: {error}")
            print(f"✅ Files created successfully, but not committed.")
            return True
            
        print(f"✅ Changes committed with message: {commit_message}")
        
        # Push if requested
        if args.push:
            status, _, error = run_git_command(["git", "push"])
            if not status:
                print(f"❌ Failed to push changes: {error}")
                print("✅ Changes committed successfully, but not pushed.")
                return True
                
            print("✅ Changes pushed to remote repository!")
    
    print(f"\n✅ Tool {args.name} created successfully!")
    return True

def checkout_command(args) -> bool:
    """Check out a specific tool from the repository."""
    print(f"🔍 Checking out {args.type}/{args.path}...")
    
    if args.type == "tool":
        # Determine if this is a local checkout or remote checkout
        tool_path = f"xwtools/{args.path}.py"
        
        if os.path.exists(tool_path):
            print(f"✅ Tool already exists locally: {tool_path}")
            tool_name = os.path.basename(args.path)
            doc_path = f"docs/tools/{tool_name}.md"
            test_path = f"tests/test_{tool_name}.py"
            
            print(f"Documentation: {doc_path if os.path.exists(doc_path) else 'Not found'}")
            print(f"Tests: {test_path if os.path.exists(test_path) else 'Not found'}")
            return True
            
        # Not found locally, try to fetch from remote
        return fetch_command(args)
    else:
        # Generic file checkout
        return fetch_command(args)

def commit_command(args) -> bool:
    """Commit changes to the repository."""
    print("📦 Committing changes...")
    
    # Check if in repository
    repo_root = find_repo_root()
    if not repo_root:
        print("❌ Not in a git repository.")
        return False
        
    # Ensure git is configured
    if not check_and_configure_github_token():
        return False
    
    # Get repository status
    status, output, error = run_git_command(["git", "status", "--porcelain"])
    if not status:
        print(f"❌ Failed to get repository status: {error}")
        return False
        
    if not output:
        print("ℹ️ No changes to commit.")
        return True
    
    # Determine which files to commit
    commit_files = []
    
    if args.all:
        # Commit all changes
        commit_files = ["--all"]
    else:
        # Parse output to get changed files
        for line in output.split("\n"):
            if line:
                if args.pattern:
                    # Only add files matching the pattern
                    file_path = line[3:]  # Skip status and space
                    if re.search(args.pattern, file_path):
                        commit_files.append(file_path)
                else:
                    # Add all changed files
                    commit_files = ["--all"]
                    break
    
    if not commit_files or (len(commit_files) == 1 and commit_files[0] != "--all" and not os.path.exists(commit_files[0])):
        if args.pattern:
            print(f"❌ No files matching pattern '{args.pattern}' to commit.")
        else:
            print("❌ No files to commit.")
        return False
    
    # Add files to staging
    if commit_files[0] != "--all":
        status, _, error = run_git_command(["git", "add"] + commit_files)
        if not status:
            print(f"❌ Failed to stage files: {error}")
            return False
    
    # Commit the changes
    if commit_files[0] == "--all":
        status, _, error = run_git_command(["git", "add", "--all"])
        if not status:
            print(f"❌ Failed to stage files: {error}")
            return False
    
    # Create the commit
    status, _, error = run_git_command(["git", "commit", "-m", args.message])
    if not status:
        print(f"❌ Failed to commit changes: {error}")
        return False
    
    print("✅ Changes committed successfully!")
    
    # Push changes if requested
    if args.push:
        print("📤 Pushing changes to remote repository...")
        status, _, error = run_git_command(["git", "push"])
        if not status:
            print(f"❌ Failed to push changes: {error}")
            print("✅ Changes committed successfully, but not pushed.")
            return True
        
        print("✅ Changes pushed to remote repository!")
    
    return True

def status_command(args) -> bool:
    """Show the status of the repository."""
    print("📊 Repository Status:")
    
    # Check if in repository
    repo_root = find_repo_root()
    if not repo_root:
        print("❌ Not in a git repository.")
        return False
    
    # Get repository information
    status, output, _ = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    current_branch = output if status else "unknown"
    
    status, output, _ = run_git_command(["git", "config", "--get", "remote.origin.url"])
    remote_url = output if status else "unknown"
    
    if "http" in remote_url:
        remote_url = re.sub(r"https://[^@]+@", "https://", remote_url)
    
    print(f"📂 Repository: {os.path.basename(repo_root)}")
    print(f"🌿 Branch: {current_branch}")
    print(f"🔗 Remote: {remote_url}")
    
    # Get uncommitted changes
    status, output, _ = run_git_command(["git", "status", "--porcelain"])
    
    if output:
        print("\n📝 Uncommitted Changes:")
        
        # Parse the output
        for line in output.split("\n"):
            if not line:
                continue
                
            status_code = line[:2]
            file_path = line[3:]
            
            if status_code == "??":
                print(f"  • New file: {file_path}")
            elif status_code == " M":
                print(f"  • Modified: {file_path}")
            elif status_code == "MM":
                print(f"  • Modified (staged and unstaged): {file_path}")
            elif status_code == "M ":
                print(f"  • Staged: {file_path}")
            elif status_code == "D ":
                print(f"  • Deleted (staged): {file_path}")
            elif status_code == " D":
                print(f"  • Deleted (unstaged): {file_path}")
            else:
                print(f"  • {file_path} ({status_code})")
    else:
        print("\n✅ Working tree clean")
    
    # Show recent commits
    status, output, _ = run_git_command(["git", "log", "--oneline", "--max-count=3"])
    
    if status and output:
        print("\n🕒 Recent Commits:")
        for line in output.split("\n")[:3]:
            if line:
                print(f"  • {line}")
    
    return True

def contribute_command(args) -> bool:
    """Complete end-to-end contribution workflow."""
    print(f"🚀 Contributing {args.path}...")
    
    # Split path into category and name
    parts = args.path.split("/")
    if len(parts) != 2:
        print("❌ Invalid path format. Expected 'category/name'.")
        print("Example: search/perplexity")
        return False
    
    category, name = parts
    
    # First, clone the repository if needed
    repo_root = find_repo_root()
    if not repo_root or os.path.basename(repo_root) != "XwDevTools":
        # Clean up any old clone
        if os.path.exists("XwDevTools"):
            print("ℹ️ XwDevTools repository already exists.")
            
            # Check if it has a .git directory
            if not os.path.exists(os.path.join("XwDevTools", ".git")):
                print("⚠️ But it's not a git repository. Cleaning up...")
                shutil.rmtree("XwDevTools")
                clone_args = argparse.Namespace(
                    repo="xwander-dev/XwDevTools",
                    sparse=True,
                    depth=1,
                    paths=f"xwtools/{category},docs/tools,tests"
                )
                if not clone_command(clone_args):
                    return False
            else:
                # Just to be safe, verify remote
                os.chdir("XwDevTools")
                status, output, _ = run_git_command(["git", "config", "--get", "remote.origin.url"])
                if not status or "xwander-dev/XwDevTools" not in output:
                    print("⚠️ Repository doesn't point to xwander-dev/XwDevTools.")
                    os.chdir("..")
                    shutil.rmtree("XwDevTools")
                    clone_args = argparse.Namespace(
                        repo="xwander-dev/XwDevTools",
                        sparse=True,
                        depth=1,
                        paths=f"xwtools/{category},docs/tools,tests"
                    )
                    if not clone_command(clone_args):
                        return False
                else:
                    # Update the repository
                    run_git_command(["git", "pull"])
                    os.chdir("..")
        else:
            # Clone the repository
            clone_args = argparse.Namespace(
                repo="xwander-dev/XwDevTools",
                sparse=True,
                depth=1,
                paths=f"xwtools/{category},docs/tools,tests"
            )
            if not clone_command(clone_args):
                return False
        
        # Change to the repository directory
        os.chdir("XwDevTools")
        
    # Now create the tool
    add_args = argparse.Namespace(
        category=category,
        name=name,
        description=args.description,
        commit=True,
        push=args.push
    )
    
    success = add_tool_command(add_args)
    
    print("\n✨ Contribution workflow summary:")
    print(f"- Tool: {name} in category {category}")
    print(f"- Description: {args.description}")
    print(f"- Committed: {'Yes' if success else 'No'}")
    print(f"- Pushed: {'Yes' if success and args.push else 'No'}")
    
    return success

def help_command(args) -> bool:
    """Show help information."""
    print(f"XwGit v{VERSION} - Streamlined GitHub workflow for AI developers")
    print("\nCommands:")
    print("  clone        Clone a repository efficiently")
    print("  fetch        Fetch a specific file or directory")
    print("  checkout     Check out a tool or file locally")
    print("  add-tool     Create a new tool with proper structure")
    print("  commit       Commit changes to the repository")
    print("  status       Show repository status")
    print("  contribute   Complete end-to-end contribution workflow")
    print("  help         Show this help message")
    print("\nExamples:")
    print("  ./xwgit.py clone xwander-dev/XwDevTools --sparse")
    print("  ./xwgit.py fetch tool search/perplexity")
    print("  ./xwgit.py add-tool search new-tool --description=\"A tool description\"")
    print("  ./xwgit.py contribute search/tool-name \"Tool description\" --push")
    print("  ./xwgit.py commit \"Add new feature\"")
    
    return True

# ==================== MAIN ENTRYPOINT ====================

def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(
        description=f"XwGit v{VERSION} - Streamlined GitHub workflow for AI developers"
    )
    subparsers = parser.add_subparsers(dest="command")
    
    # clone command
    clone_parser = subparsers.add_parser("clone", help="Clone a repository efficiently")
    clone_parser.add_argument("repo", help="Repository name (e.g., xwander-dev/XwDevTools)")
    clone_parser.add_argument("--sparse", action="store_true", help="Use sparse checkout")
    clone_parser.add_argument("--depth", type=int, help="Limit fetch depth")
    clone_parser.add_argument("--paths", help="Comma-separated paths for sparse checkout")
    
    # fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch a specific file or directory")
    fetch_parser.add_argument("type", choices=["tool", "file", "dir"], help="Type of item to fetch")
    fetch_parser.add_argument("path", help="Path to fetch (e.g., search/perplexity)")
    fetch_parser.add_argument("--repo", help="Repository name (defaults to xwander-dev/XwDevTools)")
    
    # checkout command
    checkout_parser = subparsers.add_parser("checkout", help="Check out a tool or file locally")
    checkout_parser.add_argument("type", choices=["tool", "file", "dir"], help="Type of item to checkout")
    checkout_parser.add_argument("path", help="Path to checkout (e.g., search/perplexity)")
    checkout_parser.add_argument("--repo", help="Repository name (defaults to xwander-dev/XwDevTools)")
    
    # add-tool command
    add_tool_parser = subparsers.add_parser("add-tool", help="Create a new tool with proper structure")
    add_tool_parser.add_argument("category", help="Tool category")
    add_tool_parser.add_argument("name", help="Tool name")
    add_tool_parser.add_argument(
        "--description", 
        default="A tool for XwDevTools",
        help="Tool description"
    )
    add_tool_parser.add_argument("--commit", action="store_true", help="Commit changes")
    add_tool_parser.add_argument("--push", action="store_true", help="Push changes to remote")
    
    # commit command
    commit_parser = subparsers.add_parser("commit", help="Commit changes to the repository")
    commit_parser.add_argument("message", help="Commit message")
    commit_parser.add_argument("--all", action="store_true", help="Commit all changes")
    commit_parser.add_argument("--pattern", help="Only commit files matching pattern")
    commit_parser.add_argument("--push", action="store_true", help="Push changes to remote")
    
    # status command
    subparsers.add_parser("status", help="Show repository status")
    
    # contribute command
    contribute_parser = subparsers.add_parser("contribute", help="Complete end-to-end contribution workflow")
    contribute_parser.add_argument("path", help="Tool path (category/name)")
    contribute_parser.add_argument("description", help="Tool description")
    contribute_parser.add_argument("--push", action="store_true", help="Push changes to remote")
    
    # help command
    subparsers.add_parser("help", help="Show help information")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "clone":
        return 0 if clone_command(args) else 1
    elif args.command == "fetch":
        return 0 if fetch_command(args) else 1
    elif args.command == "checkout":
        return 0 if checkout_command(args) else 1
    elif args.command == "add-tool":
        return 0 if add_tool_command(args) else 1
    elif args.command == "commit":
        return 0 if commit_command(args) else 1
    elif args.command == "status":
        return 0 if status_command(args) else 1
    elif args.command == "contribute":
        return 0 if contribute_command(args) else 1
    elif args.command == "help" or args.command is None:
        return 0 if help_command(args) else 1
    else:
        print(f"Unknown command: {args.command}")
        help_command(args)
        return 1

if __name__ == "__main__":
    sys.exit(main())