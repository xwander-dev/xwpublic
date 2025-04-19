#!/usr/bin/env python3
"""
xwgit_bootstrap.py - Simple bootstrapping tool for XwanderDev repositories

This tool handles initial repository setup and provides basic git operations
optimized for AI assistants to minimize token usage.
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

class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_color(message, color):
    """Print colored message to terminal."""
    print(f"{color}{message}{Colors.RESET}")

class XwGitBootstrap:
    """Bootstrap utility for git repository setup and management."""
    
    def __init__(self):
        self.config = self._load_config()
        self.token = None
        self.owner = None
        self.repo = None
    
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
    
    def _save_config(self):
        """Save configuration to file."""
        with open(CONFIG_FILE, 'w') as f:
            self.config.write(f)
    
    def _get_github_token(self, token_file=None, token_var=None):
        """Get GitHub token from config, environment, file, or direct input."""
        # Try from config
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
            self.token = input("Enter GitHub token: ").strip()
        
        if not self.token:
            print_color("Error: GitHub token is required.", Colors.RED)
            sys.exit(1)
        
        # Store token in config
        self.config['github']['token'] = self.token
        
        # Get and validate the repository information
        self.owner = args.owner
        self.repo = args.repo
        
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
            subprocess.run(["git", "config", "--local", "user.email", args.email or "ai-agent@xwander.dev"])
            subprocess.run(["git", "config", "--local", "user.name", args.name or "AI Agent"])
            print_color("✓ Git configuration set", Colors.GREEN)
        
        print_color(f"Initialization complete! You're now ready to work on {self.owner}/{self.repo}.", Colors.GREEN)
        print("\nNext steps:")
        print("1. Fetch the task details with './xwgit_bootstrap.py issue get <number>'")
        print("2. Create a branch with './xwgit_bootstrap.py branch create <issue_number>'")
        print("3. Implement your solution and commit changes")
    
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
[Describe your changes here]

## Testing
[Describe how you tested these changes]

Closes #{issue}
"""
            else:
                body = f"Closes #{issue}"
        else:
            body = """## Changes
[Describe your changes here]

## Testing
[Describe how you tested these changes]
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
        
        # Get repo info from config
        self.owner = self.config.get('repository', 'owner', fallback=None)
        self.repo = self.config.get('repository', 'name', fallback=None)
    
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
    parser = argparse.ArgumentParser(description="Simple bootstrapping tool for XwanderDev repositories")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize workspace")
    init_parser.add_argument("--repo", required=True, help="Repository name")
    init_parser.add_argument("--owner", required=True, help="Repository owner")
    init_parser.add_argument("--token", help="GitHub token (direct input)")
    init_parser.add_argument("--token-file", help="File containing GitHub token")
    init_parser.add_argument("--token-var", help="Environment variable containing GitHub token")
    init_parser.add_argument("--name", help="Git user name")
    init_parser.add_argument("--email", help="Git user email")
    
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
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    xwgit = XwGitBootstrap()
    
    if args.command == "init":
        xwgit.cmd_init(args)
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