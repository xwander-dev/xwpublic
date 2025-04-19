#!/usr/bin/env bash
# setup_api_key.sh - Configures API keys for team use

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

# Service name (to be specified by the user)
SERVICE_NAME="service"

print_styled "${CYAN}${BOLD}" "======================================"
print_styled "${CYAN}${BOLD}" "       API Key Configuration          "
print_styled "${CYAN}${BOLD}" "======================================"
echo ""

# Prompt for service name and API key
read -p "Enter service name (e.g., 'openai', 'github'): " SERVICE_INPUT
SERVICE_NAME=${SERVICE_INPUT:-$SERVICE_NAME}

read -p "Enter API key for ${SERVICE_NAME}: " API_KEY

if [[ -z "$API_KEY" ]]; then
  print_styled "${RED}" "Error: API key is required."
  exit 1
fi

# Create config directory if it doesn't exist
CONFIG_DIR="${HOME}/.config"
mkdir -p "${CONFIG_DIR}"

# Create local config file
CONFIG_FILE="${HOME}/.${SERVICE_NAME}.json"
echo "{\"api_key\": \"${API_KEY}\"}" > "${CONFIG_FILE}"
print_styled "${GREEN}" "✓ API key saved to ${CONFIG_FILE}"

# Convert service name to uppercase for env vars
SERVICE_ENV="${SERVICE_NAME^^}_API_KEY"

# Add to .env file in current directory
if [[ -f ".env" ]]; then
  # Check if the key already exists in .env
  if grep -q "${SERVICE_ENV}=" ".env"; then
    # Replace existing key
    sed -i "s/${SERVICE_ENV}=.*/${SERVICE_ENV}=${API_KEY}/" ".env"
  else
    # Add new key
    echo "${SERVICE_ENV}=${API_KEY}" >> ".env"
  fi
else
  # Create new .env file
  echo "${SERVICE_ENV}=${API_KEY}" > ".env"
fi
print_styled "${GREEN}" "✓ API key added to .env file"

# Create environment variable for current session
export ${SERVICE_ENV}="${API_KEY}"
print_styled "${GREEN}" "✓ Environment variable ${SERVICE_ENV} set for current session"

# Suggest adding to shell profile
print_styled "${YELLOW}" "To make the API key persistent across sessions, add this to your shell profile:"
echo "export ${SERVICE_ENV}=\"${API_KEY}\""

print_styled "${GREEN}${BOLD}" "✓ API key configuration complete!"
echo ""
print_styled "${CYAN}" "The API key is now available to your tools through multiple methods:"
echo "1. Environment variable: ${SERVICE_ENV}"
echo "2. .env file in the current directory"
echo "3. User config file: ${CONFIG_FILE}"
echo ""
print_styled "${CYAN}" "You can now use tools that require this API key without additional configuration."