#!/usr/bin/env bash
# xwgit.sh - One-step onboarding script for XwanderDev projects
# Streamlines the entire setup and initialization process

set -e  # Exit on error

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Print styled message
print_styled() {
  local color=$1
  local message=$2
  echo -e "${color}${message}${NC}"
}

# Configuration
BOOTSTRAP_URL="https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit_bootstrap.py"
DEFAULT_OWNER="xwander-dev"
DEFAULT_REPO="XwDevTools"
CONFIG_FILE="${HOME}/.xwgit.ini"

print_styled "${CYAN}${BOLD}" "==============================================="
print_styled "${CYAN}${BOLD}" "  XwanderDev Project Onboarding - Quick Setup  "
print_styled "${CYAN}${BOLD}" "==============================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
  print_styled "${RED}" "Error: Python 3 is required but not installed."
  exit 1
fi

# Check for pip and install requests if needed
if ! python3 -c "import requests" &> /dev/null; then
  print_styled "${YELLOW}" "The Python 'requests' module is required."
  read -p "Would you like to install it now? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 -m pip install requests
  else
    print_styled "${RED}" "The 'requests' module is required to continue."
    exit 1
  fi
fi

# Download bootstrap script if not present
if [[ ! -f "xwgit_bootstrap.py" ]]; then
  print_styled "${CYAN}" "Downloading xwgit_bootstrap.py..."
  curl -s -O "${BOOTSTRAP_URL}"
  chmod +x xwgit_bootstrap.py
  print_styled "${GREEN}" "✓ Bootstrap script downloaded successfully"
fi

# Check for existing configuration
if [[ -f "${CONFIG_FILE}" ]]; then
  print_styled "${YELLOW}" "Existing configuration found."
  read -p "Would you like to use this configuration? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_styled "${GREEN}" "✓ Using existing configuration"
    USE_EXISTING_CONFIG=true
  fi
fi

if [[ "${USE_EXISTING_CONFIG}" != "true" ]]; then
  # Prompt for GitHub token if not in environment
  if [[ -z "${GITHUB_TOKEN}" ]]; then
    print_styled "${CYAN}" "GitHub access token is required for repository operations."
    read -p "Enter your GitHub token: " GITHUB_TOKEN
    
    # Save token to environment for this session
    export GITHUB_TOKEN
  else
    print_styled "${GREEN}" "✓ GitHub token found in environment"
  fi
  
  # Prompt for repository information
  read -p "Enter repository owner [${DEFAULT_OWNER}]: " OWNER
  OWNER=${OWNER:-$DEFAULT_OWNER}
  
  read -p "Enter repository name [${DEFAULT_REPO}]: " REPO
  REPO=${REPO:-$DEFAULT_REPO}
  
  # Initialize the workspace
  print_styled "${CYAN}" "Initializing workspace..."
  ./xwgit_bootstrap.py init --owner="${OWNER}" --repo="${REPO}" --token="${GITHUB_TOKEN}"
else
  # Just ensure we're in the right directory
  if [[ -d "${DEFAULT_REPO}" ]]; then
    cd "${DEFAULT_REPO}"
  fi
fi

# Onboarding complete
print_styled "${GREEN}${BOLD}" "✓ Onboarding complete!"
echo
print_styled "${CYAN}" "Next steps:"
echo "1. Start a new feature: ./xwgit_bootstrap.py quickstart <name> --description=\"Description\" --issue=<number>"
echo "2. Implement your feature in the created files"
echo "3. Finalize and submit: ./xwgit_bootstrap.py finalize \"Implement feature\" --issue=<number>"
echo
print_styled "${YELLOW}" "For more detailed instructions, see the onboarding guide:"
echo "https://github.com/xwander-dev/xwpublic/blob/main/guides/onboarding.md"