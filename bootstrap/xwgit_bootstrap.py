#!/usr/bin/env python3
"""
xwgit_bootstrap.py - Streamlined git utility for XwanderDev projects

This tool provides a simplified workflow for XwanderDev projects with
automated repository setup, branch management, and project initialization.
"""

import os
import sys
import re
import json
import configparser
import argparse
from typing import List, Dict, Optional, Union, Tuple, Any
from pathlib import Path
import subprocess
from datetime import datetime
import tempfile
import shutil

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: 'requests' module not found. Install with: pip install requests")

# Configuration
CONFIG_FILE = os.path.expanduser("~/.xwgit.ini")
TEAM_CONFIG_PATH = "/shared/xwdev/config/team_config.json"

# Tool templates
TOOL_TEMPLATES = {
    "search-tool": {
        "files": {
            "xwtools/search/{name}.py": """#!/usr/bin/env python3
\"\"\"
{name}.py - Search utility for XwanderDev projects

{description}
\"\"\"

import os
import sys
import json
import argparse
from typing import Dict, Any, Optional
import requests

def get_api_key(key_name="{key_name}"):
    \"\"\"Get API key from environment or team config.\"\"\"
    # Try environment variable
    api_key = os.environ.get(key_name.upper() + "_API_KEY")
    
    # Try .env file
    if not api_key and os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith(key_name.upper() + "_API_KEY="):
                    api_key = line.strip().split("=", 1)[1].strip("\"' ")
    
    # Try team config
    if not api_key and os.path.exists(os.path.expanduser("~/.{key_name}.json")):
        with open(os.path.expanduser("~/.{key_name}.json"), "r") as f:
            config = json.load(f)
            api_key = config.get("api_key")
    
    # Try shared team config
    if not api_key and os.path.exists("/shared/xwdev/config/api_keys.json"):
        with open("/shared/xwdev/config/api_keys.json", "r") as f:
            config = json.load(f)
            api_key = config.get(key_name + "_api_key")
    
    return api_key

def main():
    \"\"\"Main entry point for the tool.\"\"\"
    parser = argparse.ArgumentParser(
        description="{description}"
    )
    
    parser.add_argument("query", nargs="+", help="The search query")
    parser.add_argument("--format", choices=["text", "json", "markdown"], 
                      default="text", help="Output format")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = get_api_key("{key_name}")
    if not api_key:
        print("Error: {key_name} API key not found")
        print("Set it using the {key_name.upper()}_API_KEY environment variable")
        sys.exit(1)
    
    # Process the query
    query = " ".join(args.query)
    print(f"Searching for: {query}")
    
    # Implement your search logic here
    
if __name__ == "__main__":
    main()
""",
            
            "docs/tools/{name}.md": """# {name}.py

## Overview

{description}

## Installation

```bash
# Make sure you're in the project root directory
chmod +x xwtools/search/{name}.py
```

## Usage

```bash
# Basic search
./xwtools/search/{name}.py "your search query"

# Specify output format
./xwtools/search/{name}.py "your search query" --format=json
```

## API Key Configuration

The tool requires an API key, which can be configured in several ways:

1. Environment variable: `{key_name.upper()}_API_KEY=your_api_key`
2. In a `.env` file: `{key_name.upper()}_API_KEY=your_api_key`
3. In `~/.{key_name}.json`: `{"api_key": "your_api_key"}`
4. In the team config: `/shared/xwdev/config/api_keys.json`

## Features

- Fast and efficient search
- Multiple output formats
- Integration with other XwanderDev tools
""",
            
            "tests/test_{name}.py": """#!/usr/bin/env python3
\"\"\"
Test suite for {name}.py
\"\"\"

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import module to test
from xwtools.search import {name}

class Test{name_title}(unittest.TestCase):
    \"\"\"Test suite for {name}.py\"\"\"
    
    def test_api_key_handling(self):
        \"\"\"Test API key retrieval\"\"\"
        # Mock environment variable
        with patch.dict(os.environ, {{"{key_name.upper()}_API_KEY": "test_key"}}):
            self.assertEqual({name}.get_api_key("{key_name}"), "test_key")
    
    # Add more tests here

if __name__ == "__main__":
    unittest.main()
"""
        },
        "directories": [
            "xwtools/search",
            "docs/tools",
            "tests"
        ]
    },
    
    "api-tool": {
        "files": {
            "xwtools/api/{name}.py": """#!/usr/bin/env python3
\"\"\"
{name}.py - API client for XwanderDev projects

{description}
\"\"\"

import os
import sys
import json
import argparse
import requests
from typing import Dict, Any, Optional

def get_api_key(key_name="{key_name}"):
    \"\"\"Get API key from environment or team config.\"\"\"
    # Try environment variable
    api_key = os.environ.get(key_name.upper() + "_API_KEY")
    
    # Try .env file
    if not api_key and os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith(key_name.upper() + "_API_KEY="):
                    api_key = line.strip().split("=", 1)[1].strip("\"' ")
    
    # Try team config
    if not api_key and os.path.exists(os.path.expanduser("~/.{key_name}.json")):
        with open(os.path.expanduser("~/.{key_name}.json"), "r") as f:
            config = json.load(f)
            api_key = config.get("api_key")
    
    # Try shared team config
    if not api_key and os.path.exists("/shared/xwdev/config/api_keys.json"):
        with open("/shared/xwdev/config/api_keys.json", "r") as f:
            config = json.load(f)
            api_key = config.get(key_name + "_api_key")
    
    return api_key

def main():
    \"\"\"Main entry point for the API client.\"\"\"
    parser = argparse.ArgumentParser(
        description="{description}"
    )
    
    parser.add_argument("action", choices=["get", "post", "list"], 
                      help="API action to perform")
    parser.add_argument("--data", help="JSON data for POST requests")
    parser.add_argument("--id", help="Resource ID for GET requests")
    parser.add_argument("--format", choices=["text", "json"], 
                      default="text", help="Output format")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = get_api_key("{key_name}")
    if not api_key:
        print("Error: {key_name} API key not found")
        print("Set it using the {key_name.upper()}_API_KEY environment variable")
        sys.exit(1)
    
    # Implement your API logic here
    
if __name__ == "__main__":
    main()
"""
        },
        "directories": [
            "xwtools/api",
            "docs/tools",
            "tests"
        ]
    }
}

class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_color(message, color, end="\n"):
    """Print colored message to terminal."""
    print(f"{color}{message}{Colors.RESET}", end=end)

class XwGitBootstrap:
    """Bootstrap utility for git repository setup and management."""
    
    def __init__(self):
        self.config = self._load_config()
        self.token = None
        self.owner = None
        self.repo = None
        self.team_config = self._load_team_config()
    
    def _load_config(self) -> configparser.ConfigParser:
        """Load configuration from file."""
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE)
        
        # Ensure essential sections exist
        if 'github' not in config:
            config['github'] = {}
        if 'agent' not in config:
            config['agent'] = {}
        if 'repository' not in config:
            config['repository'] = {}
        
        return config
    
    def _load_team_config(self) -> dict:
        """Load team configuration from shared location."""
        if os.path.exists(TEAM_CONFIG_PATH):
            try:
                with open(TEAM_CONFIG_PATH, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Also check for .env file in current directory
        if os.path.exists(".env"):
            config = {}
            with open(".env", "r") as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        config[key.lower()] = value.strip('"\'')
            return config
                
        return {}
    
    def _save_config(self):
        """Save configuration to file."""
        with open(CONFIG_FILE, 'w') as f:
            self.config.write(f)
    
    def _get_github_token(self, token_file=None, token_var=None):
        """Get GitHub token from config, environment, file, or direct input."""
        # Try from team config
        token = self.team_config.get('github_token')
        
        # Try from config
        if not token:
            token = self.config.get('github', 'token', fallback=None)
        
        # Try from specified environment variable
        if not token and token_var:
            token = os.environ.get(token_var)
        
        # Try from default environment variable
        if not token:
            token = os.environ.get('GITHUB_TOKEN')
        
        # Try from token file
        if not token and token_file:
            try:
                with open(token_file, 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            if key in ('GITHUB_TOKEN', 'token'):
                                token = value.strip('"\'')
                                break
            except Exception as e:
                print_color(f"Error reading token file: {e}", Colors.RED)
        
        return token
    
    def _github_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make a request to the GitHub API."""
        if not HAS_REQUESTS:
            print_color("Error: 'requests' module is required. Install with: pip install requests", Colors.RED)
            return {}
        
        if not self.token:
            print_color("Error: GitHub token not set.", Colors.RED)
            return {}
        
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        url = f"https://api.github.com/{endpoint}"
        
        try:
            response = requests.request(method, url, headers=headers, json=data)
            
            if response.status_code >= 400:
                error_msg = response.json().get('message', 'Unknown error')
                print_color(f"GitHub API error ({response.status_code}): {error_msg}", Colors.RED)
                return {}
            
            return response.json()
        except Exception as e:
            print_color(f"Error making GitHub request: {e}", Colors.RED)
            return {}
    
    def cmd_init(self, args):
        """Initialize the workspace with repository info and GitHub token."""
        # Get and validate the token
        self.token = self._get_github_token(args.token_file, args.token_var)
        
        if not self.token and args.token:
            self.token = args.token
            
        if not self.token:
            token_from_env = os.environ.get('GITHUB_TOKEN')
            if token_from_env:
                self.token = token_from_env
            else:
                self.token = input("Enter GitHub token: ").strip()
        
        if not self.token:
            print_color("Error: GitHub token is required.", Colors.RED)
            sys.exit(1)
        
        # Store token in config
        self.config['github']['token'] = self.token
        
        # Get and validate the repository information
        self.owner = args.owner or self.team_config.get('github_owner') or self.config.get('repository', 'owner', fallback=None)
        self.repo = args.repo or self.team_config.get('github_repo') or self.config.get('repository', 'name', fallback=None)
        
        if not self.owner or not self.repo:
            print_color("Error: Repository owner and name are required.", Colors.RED)
            sys.exit(1)
            
        # Validate repo access
        print_color(f"Validating access to {self.owner}/{self.repo}...", Colors.CYAN)
        repo_info = self._github_request("GET", f"repos/{self.owner}/{self.repo}")
        
        if not repo_info:
            print_color(f"Error: Could not access repository {self.owner}/{self.repo}.", Colors.RED)
            sys.exit(1)
        
        print_color(f"✓ Repository access confirmed: {repo_info.get('full_name')}", Colors.GREEN)
        
        # Store repo info in config
        self.config['repository']['owner'] = self.owner
        self.config['repository']['name'] = self.repo
        
        # Save config
        self._save_config()
        
        # Clone repository if not present
        repo_dir = os.path.join(os.getcwd(), self.repo)
        if not os.path.exists(repo_dir):
            print_color(f"Cloning repository to {repo_dir}...", Colors.CYAN)
            try:
                subprocess.run(
                    ["git", "clone", f"https://{self.token}@github.com/{self.owner}/{self.repo}.git"],
                    check=True
                )
                print_color("✓ Repository cloned successfully", Colors.GREEN)
                
                # Change to repo directory
                os.chdir(repo_dir)
            except Exception as e:
                print_color(f"Error cloning repository: {e}", Colors.RED)
                sys.exit(1)
        else:
            print_color("Repository directory already exists. Using existing directory.", Colors.YELLOW)
            os.chdir(repo_dir)
        
        # Configure git
        try:
            user_email = subprocess.check_output(["git", "config", "user.email"]).decode().strip()
        except:
            user_email = ""
        
        if not user_email:
            print_color("Setting up git configuration...", Colors.CYAN)
            email = args.email or self.team_config.get('git_email') or "ai-agent@xwander.dev"
            name = args.name or self.team_config.get('git_name') or "AI Agent"
            subprocess.run(["git", "config", "--local", "user.email", email])
            subprocess.run(["git", "config", "--local", "user.name", name])
            print_color("✓ Git configuration set", Colors.GREEN)
        
        print_color(f"Initialization complete! You're now ready to work on {self.owner}/{self.repo}.", Colors.GREEN)
        print("\nNext steps:")
        print("1. Use quickstart to set up a new feature: ./xwgit_bootstrap.py quickstart [feature]")
        print("2. Or fetch an issue with: ./xwgit_bootstrap.py issue get [number]")
    
    def cmd_quickstart(self, args):
        """Quick start a new feature with automated setup."""
        self._init_from_config()
        
        if not self._validate_setup():
            return
        
        feature_name = args.name
        issue_number = args.issue
        tool_type = args.type
        description = args.description or f"{feature_name} utility for XwanderDev projects"
        api_name = args.api or feature_name
        
        # Validate the template type
        if tool_type not in TOOL_TEMPLATES:
            print_color(f"Unknown tool type: {tool_type}", Colors.RED)
            print_color(f"Available types: {', '.join(TOOL_TEMPLATES.keys())}", Colors.YELLOW)
            return
        
        # Create branch if issue specified
        if issue_number:
            print_color(f"Creating branch for issue #{issue_number}...", Colors.CYAN)
            try:
                self.cmd_branch_create(argparse.Namespace(issue_number=issue_number))
            except Exception as e:
                print_color(f"Error creating branch: {e}", Colors.RED)
        
        # Create directories
        print_color("Creating directory structure...", Colors.CYAN)
        template = TOOL_TEMPLATES[tool_type]
        for directory in template["directories"]:
            os.makedirs(directory, exist_ok=True)
        
        # Create files from templates
        print_color("Creating files from templates...", Colors.CYAN)
        for file_path, content in template["files"].items():
            # Format file path with name
            path = file_path.format(name=feature_name)
            
            # Format content with name, description, etc.
            formatted_content = content.format(
                name=feature_name,
                name_title=feature_name.title(),
                description=description,
                key_name=api_name
            )
            
            # Create the file
            with open(path, "w") as f:
                f.write(formatted_content)
            
            # Make executable if it's a Python file
            if path.endswith(".py"):
                os.chmod(path, 0o755)
            
            print_color(f"Created {path}", Colors.GREEN)
        
        print_color("\nQuickstart complete! Your feature is ready for implementation.", Colors.GREEN)
        print("\nNext steps:")
        print(f"1. Edit the files in the created directories")
        print(f"2. Run tests when ready")
        print(f"3. Finalize with: ./xwgit_bootstrap.py finalize \"Implement {feature_name} utility\"")
    
    def cmd_finalize(self, args):
        """Finalize a feature by committing, pushing, and creating a PR."""
        self._init_from_config()
        
        if not self._validate_setup():
            return
        
        message = args.message
        issue = args.issue
        
        # Stage all files
        print_color("Staging all changes...", Colors.CYAN)
        try:
            subprocess.run(["git", "add", "."], check=True)
            print_color("✓ All changes staged", Colors.GREEN)
        except Exception as e:
            print_color(f"Error staging changes: {e}", Colors.RED)
            return
        
        # Commit changes
        print_color("Committing changes...", Colors.CYAN)
        try:
            commit_message = message
            if issue:
                commit_message = f"{message} (#{issue})"
            
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print_color(f"✓ Changes committed: {commit_message}", Colors.GREEN)
        except Exception as e:
            print_color(f"Error committing changes: {e}", Colors.RED)
            return
        
        # Push changes
        print_color("Pushing changes to remote...", Colors.CYAN)
        try:
            branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
            subprocess.run(["git", "push", "-u", "origin", branch], check=True)
            print_color(f"✓ Changes pushed to origin/{branch}", Colors.GREEN)
        except Exception as e:
            print_color(f"Error pushing changes: {e}", Colors.RED)
            return
        
        # Create PR if issue specified
        if issue:
            print_color(f"Creating pull request for issue #{issue}...", Colors.CYAN)
            try:
                self.cmd_pr_create(argparse.Namespace(
                    title=message,
                    issue=issue
                ))
            except Exception as e:
                print_color(f"Error creating pull request: {e}", Colors.RED)
                return
        
        print_color("Finalization complete! Your feature is now ready for review.", Colors.GREEN)
    
    def cmd_issue_get(self, args):
        """Get details for a specific GitHub issue."""
        self._init_from_config()
        
        if not self._validate_setup():
            return
        
        issue_number = args.issue_number
        endpoint = f"repos/{self.owner}/{self.repo}/issues/{issue_number}"
        
        issue = self._github_request("GET", endpoint)
        
        if not issue:
            print_color(f"Issue #{issue_number} not found.", Colors.RED)
            return
        
        # Format issue details
        print_color("===========================================", Colors.CYAN)
        print_color(f"Issue #{issue['number']}: {issue['title']}", Colors.CYAN)
        print_color("===========================================", Colors.CYAN)
        print_color("Status:", Colors.BOLD, end=" ")
        print(issue['state'])
        print_color("Created:", Colors.BOLD, end=" ")
        print(issue['created_at'])
        print_color("Author:", Colors.BOLD, end=" ")
        print(issue['user']['login'])
        print_color("Assignee:", Colors.BOLD, end=" ")
        print(issue['assignee']['login'] if issue.get('assignee') else 'Unassigned')
        print_color("Labels:", Colors.BOLD, end=" ")
        print(', '.join(label['name'] for label in issue.get('labels', [])))
        print("\n" + issue['body'] + "\n")
        
        # Get comments
        comments_endpoint = f"repos/{self.owner}/{self.repo}/issues/{issue_number}/comments"
        comments = self._github_request("GET", comments_endpoint)
        
        if comments:
            print_color("Comments:", Colors.CYAN)
            for comment in comments:
                print_color(f"{comment['user']['login']} - {comment['created_at']}", Colors.YELLOW)
                print(f"{comment['body']}\n")
    
    def cmd_issue_comment(self, args):
        """Add a comment to a GitHub issue."""
        self._init_from_config()
        
        if not self._validate_setup():
            return
        
        issue_number = args.issue_number
        comment = args.comment
        
        endpoint = f"repos/{self.owner}/{self.repo}/issues/{issue_number}/comments"
        
        data = {"body": comment}
        result = self._github_request("POST", endpoint, data)
        
        if result:
            print_color(f"Comment added to issue #{issue_number}.", Colors.GREEN)
        else:
            print_color(f"Failed to add comment to issue #{issue_number}.", Colors.RED)
    
    def cmd_branch_create(self, args):
        """Create a branch for an issue."""
        self._init_from_config()
        
        if not self._validate_setup():
            return
        
        issue_number = args.issue_number
        
        # Get issue details
        endpoint = f"repos/{self.owner}/{self.repo}/issues/{issue_number}"
        issue = self._github_request("GET", endpoint)
        
        if not issue:
            print_color(f"Issue #{issue_number} not found.", Colors.RED)
            return
        
        # Create branch name from issue
        title_part = re.sub(r'[^a-zA-Z0-9]', '-', issue['title'].lower())
        title_part = re.sub(r'-+', '-', title_part)  # Replace multiple dashes with single
        title_part = title_part.strip('-')  # Remove trailing dashes
        branch_name = f"feature/issue-{issue_number}-{title_part}"
        
        # Check if the branch already exists
        try:
            existing_branches = subprocess.check_output(["git", "branch"]).decode()
            if branch_name in existing_branches or f"* {branch_name}" in existing_branches:
                print_color(f"Branch {branch_name} already exists.", Colors.YELLOW)
                
                # Switch to the branch if not already on it
                if f"* {branch_name}" not in existing_branches:
                    print_color(f"Switching to branch {branch_name}...", Colors.CYAN)
                    subprocess.run(["git", "checkout", branch_name], check=True)
                    print_color(f"✓ Switched to branch {branch_name}", Colors.GREEN)
                
                return
        except Exception as e:
            print_color(f"Error checking branches: {e}", Colors.RED)
            return
        
        # Create new branch
        try:
            # Make sure we're up to date with main
            print_color("Updating main branch...", Colors.CYAN)
            subprocess.run(["git", "checkout", "main"], check=True)
            subprocess.run(["git", "pull"], check=True)
            
            # Create branch
            print_color(f"Creating new branch: {branch_name}", Colors.CYAN)
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            
            print_color(f"Created branch {branch_name} for issue #{issue_number}", Colors.GREEN)
        except Exception as e:
            print_color(f"Error creating branch: {e}", Colors.RED)
    
    def cmd_commit(self, args):
        """Create a commit with standardized message."""
        message = args.message
        issue = args.issue
        
        # Expand message with issue reference if provided
        if issue:
            message = f"{message} (#{issue})"
        
        # Stage files if specified
        if args.all:
            try:
                subprocess.run(["git", "add", "."], check=True)
                print_color("Staged all files", Colors.GREEN)
            except Exception as e:
                print_color(f"Error staging files: {e}", Colors.RED)
                return
        
        # Create commit
        try:
            subprocess.run(["git", "commit", "-m", message], check=True)
            print_color(f"Created commit: {message}", Colors.GREEN)
        except Exception as e:
            print_color(f"Error creating commit: {e}", Colors.RED)
    
    def cmd_push(self, args):
        """Push changes to remote."""
        try:
            # Get current branch
            branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
            
            print_color(f"Pushing branch {branch} to remote...", Colors.CYAN)
            subprocess.run(["git", "push", "-u", "origin", branch], check=True)
            
            print_color("✓ Changes pushed successfully", Colors.GREEN)
        except Exception as e:
            print_color(f"Error pushing changes: {e}", Colors.RED)
    
    def cmd_pr_create(self, args):
        """Create a pull request."""
        self._init_from_config()
        
        if not self._validate_setup():
            return
        
        title = args.title
        issue = args.issue
        
        # Get current branch
        try:
            current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        except Exception as e:
            print_color(f"Error getting current branch: {e}", Colors.RED)
            return
        
        # Create body from issue if provided
        body = ""
        if issue:
            # Get issue details
            endpoint = f"repos/{self.owner}/{self.repo}/issues/{issue}"
            issue_data = self._github_request("GET", endpoint)
            
            if issue_data:
                body = f"""## Related Issue
#{issue} - {issue_data['title']}

## Changes
{args.body or f"Implements features requested in issue #{issue}"}

## Testing
{args.testing or "Basic testing completed"}

Closes #{issue}
"""
            else:
                body = args.body or f"Closes #{issue}"
        else:
            body = args.body or """## Changes
[Describe changes here]

## Testing
[Describe testing here]
"""
        
        # Create PR
        endpoint = f"repos/{self.owner}/{self.repo}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": current_branch,
            "base": "main"
        }
        
        result = self._github_request("POST", endpoint, data)
        
        if result:
            print_color(f"Pull request created: {result['html_url']}", Colors.GREEN)
        else:
            print_color("Failed to create pull request.", Colors.RED)
    
    def _init_from_config(self):
        """Initialize from saved configuration."""
        # Get token from config
        self.token = self.config.get('github', 'token', fallback=None)
        
        # Try from team config if not in user config
        if not self.token:
            self.token = self.team_config.get('github_token')
        
        # Try from environment if not in config
        if not self.token:
            self.token = os.environ.get('GITHUB_TOKEN')
        
        # Get repo info from config
        self.owner = self.config.get('repository', 'owner', fallback=None)
        self.repo = self.config.get('repository', 'name', fallback=None)
        
        # Try from team config if not in user config
        if not self.owner:
            self.owner = self.team_config.get('github_owner')
        if not self.repo:
            self.repo = self.team_config.get('github_repo')
    
    def _validate_setup(self):
        """Validate that the tool is properly set up."""
        if not self.token:
            print_color("GitHub token not found. Run init first.", Colors.RED)
            return False
        
        if not self.owner or not self.repo:
            print_color("Repository information not found. Run init first.", Colors.RED)
            return False
        
        return True


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Streamlined git utility for XwanderDev projects")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize workspace")
    init_parser.add_argument("--repo", help="Repository name")
    init_parser.add_argument("--owner", help="Repository owner")
    init_parser.add_argument("--token", help="GitHub token (direct input)")
    init_parser.add_argument("--token-file", help="File containing GitHub token")
    init_parser.add_argument("--token-var", help="Environment variable containing GitHub token")
    init_parser.add_argument("--name", help="Git user name")
    init_parser.add_argument("--email", help="Git user email")
    
    # Quickstart command
    quickstart_parser = subparsers.add_parser("quickstart", help="Quick start a new feature")
    quickstart_parser.add_argument("name", help="Feature name (e.g., perplexity)")
    quickstart_parser.add_argument("--type", default="search-tool", help="Tool type template to use")
    quickstart_parser.add_argument("--issue", type=int, help="Related issue number")
    quickstart_parser.add_argument("--description", help="Feature description")
    quickstart_parser.add_argument("--api", help="API name for key configuration")
    
    # Finalize command
    finalize_parser = subparsers.add_parser("finalize", help="Finalize a feature (commit, push, PR)")
    finalize_parser.add_argument("message", help="Commit and PR title")
    finalize_parser.add_argument("--issue", type=int, help="Related issue number")
    
    # Issue commands
    issue_parser = subparsers.add_parser("issue", help="Issue management")
    issue_subparsers = issue_parser.add_subparsers(dest="issue_command", help="Issue subcommand")
    
    get_parser = issue_subparsers.add_parser("get", help="Get issue details")
    get_parser.add_argument("issue_number", type=int, help="Issue number")
    
    comment_parser = issue_subparsers.add_parser("comment", help="Comment on issue")
    comment_parser.add_argument("issue_number", type=int, help="Issue number")
    comment_parser.add_argument("comment", help="Comment text")
    
    # Branch commands
    branch_parser = subparsers.add_parser("branch", help="Branch management")
    branch_subparsers = branch_parser.add_subparsers(dest="branch_command", help="Branch subcommand")
    
    create_parser = branch_subparsers.add_parser("create", help="Create branch for issue")
    create_parser.add_argument("issue_number", type=int, help="Issue number")
    
    # Commit command
    commit_parser = subparsers.add_parser("commit", help="Create a commit")
    commit_parser.add_argument("message", help="Commit message")
    commit_parser.add_argument("--issue", type=int, help="Related issue number")
    commit_parser.add_argument("--all", "-a", action="store_true", help="Stage all changes")
    
    # Push command
    push_parser = subparsers.add_parser("push", help="Push changes to remote")
    
    # PR commands
    pr_parser = subparsers.add_parser("pr", help="Pull request management")
    pr_subparsers = pr_parser.add_subparsers(dest="pr_command", help="PR subcommand")
    
    create_pr_parser = pr_subparsers.add_parser("create", help="Create a pull request")
    create_pr_parser.add_argument("--title", required=True, help="PR title")
    create_pr_parser.add_argument("--issue", type=int, help="Related issue number")
    create_pr_parser.add_argument("--body", help="PR description")
    create_pr_parser.add_argument("--testing", help="Testing description")
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    xwgit = XwGitBootstrap()
    
    if args.command == "init":
        xwgit.cmd_init(args)
    elif args.command == "quickstart":
        xwgit.cmd_quickstart(args)
    elif args.command == "finalize":
        xwgit.cmd_finalize(args)
    elif args.command == "issue":
        if args.issue_command == "get":
            xwgit.cmd_issue_get(args)
        elif args.issue_command == "comment":
            xwgit.cmd_issue_comment(args)
        else:
            print_color(f"Unknown issue subcommand: {args.issue_command}", Colors.RED)
    elif args.command == "branch":
        if args.branch_command == "create":
            xwgit.cmd_branch_create(args)
        else:
            print_color(f"Unknown branch subcommand: {args.branch_command}", Colors.RED)
    elif args.command == "commit":
        xwgit.cmd_commit(args)
    elif args.command == "push":
        xwgit.cmd_push(args)
    elif args.command == "pr":
        if args.pr_command == "create":
            xwgit.cmd_pr_create(args)
        else:
            print_color(f"Unknown PR subcommand: {args.pr_command}", Colors.RED)
    else:
        print_color(f"Unknown command: {args.command}", Colors.RED)
        print("Run with --help for usage information.")


if __name__ == "__main__":
    main()