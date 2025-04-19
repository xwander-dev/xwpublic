#!/bin/bash
# sysadmin-setup.sh - Complete setup script for AI developer workspaces
# Usage: curl -s -o- https://raw.githubusercontent.com/xwander-dev/xwpublic/main/xwgit/sysadmin-setup.sh | bash -s AI_NAME

set -e

# Colors for output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Get AI developer name from args
AI_NAME="${1:-ai-developer}"
if [ "$AI_NAME" == "" ]; then
  echo -e "${RED}Error: AI developer name required${NC}"
  echo "Usage: curl -s -o- https://raw.githubusercontent.com/xwander-dev/xwpublic/main/xwgit/sysadmin-setup.sh | bash -s AI_NAME"
  exit 1
fi

echo -e "${CYAN}${BOLD}=========================================${NC}"
echo -e "${CYAN}${BOLD} Setting up XwGit for AI developer: ${AI_NAME} ${NC}"
echo -e "${CYAN}${BOLD}=========================================${NC}"
echo ""

# Create base workspace directory
WORKSPACE_DIR="/tmp/ai-workspace"
AI_WORKSPACE="${WORKSPACE_DIR}/${AI_NAME}-workspace"

echo -e "${YELLOW}Creating workspace directories...${NC}"
mkdir -p "${WORKSPACE_DIR}"
mkdir -p "${AI_WORKSPACE}"

# Download XwGit core script
echo -e "${YELLOW}Downloading XwGit tools...${NC}"
mkdir -p "${WORKSPACE_DIR}/bin"
curl -s -o "${WORKSPACE_DIR}/bin/xwgit" https://raw.githubusercontent.com/xwander-dev/xwpublic/main/xwgit/xwgit-core.py
chmod +x "${WORKSPACE_DIR}/bin/xwgit"

# Clone the repository
echo -e "${YELLOW}Cloning target repository...${NC}"
cd "${AI_WORKSPACE}"
if [ ! -d "XwDevTools" ]; then
  git clone https://github.com/xwander-dev/xwpublic.git XwDevTools
  cd XwDevTools
else
  cd XwDevTools
  git pull
fi

# Set up git identity for the AI
git config --local user.name "AI-${AI_NAME}"
git config --local user.email "${AI_NAME,,}@ai.xwander.dev"

# Create required directories
echo -e "${YELLOW}Creating project structure...${NC}"
mkdir -p xwtools/search xwtools/api docs/tools tests

# Generate access code
echo -e "${YELLOW}Generating access code...${NC}"
cd "${WORKSPACE_DIR}"
"${WORKSPACE_DIR}/bin/xwgit" generate-code "${AI_NAME}" > "${AI_WORKSPACE}/access_code.txt"

# Create easy-to-use command file
cat > "${AI_WORKSPACE}/xwgit" << 'EOF'
#!/bin/bash
# Simple wrapper for xwgit
/tmp/ai-workspace/bin/xwgit "$@"
EOF
chmod +x "${AI_WORKSPACE}/xwgit"

# Create helpful guide file
cat > "${AI_WORKSPACE}/GUIDE.md" << EOF
# AI Developer Guide for ${AI_NAME}

Your workspace is ready at: ${AI_WORKSPACE}

## Getting Started

1. Use your access code to initialize your session:
   \`\`\`bash
   ./xwgit init --code YOUR_ACCESS_CODE
   \`\`\`
   (Your access code can be found in access_code.txt)

2. Create a new tool:
   \`\`\`bash
   ./xwgit quickstart my_tool --description="A useful utility" --type=search
   \`\`\`

3. Implement your tool by editing the generated files.

4. Finalize your work:
   \`\`\`bash
   ./xwgit finalize "Implement my_tool functionality"
   \`\`\`

That's it! Your changes will be committed and ready for review.
EOF

# Extract access code for the output
ACCESS_CODE=$(grep "Code:" "${AI_WORKSPACE}/access_code.txt" | awk '{print $2}')

echo -e "${GREEN}${BOLD}✅ Setup complete!${NC}"
echo ""
echo -e "${CYAN}${BOLD}=========================================${NC}"
echo -e "${CYAN}${BOLD} AI Developer Information ${NC}"
echo -e "${CYAN}${BOLD}=========================================${NC}"
echo -e "Workspace: ${GREEN}${AI_WORKSPACE}${NC}"
echo -e "Access Code: ${GREEN}${ACCESS_CODE}${NC}"
echo ""
echo -e "${YELLOW}Instructions for AI developer:${NC}"
echo "1. cd ${AI_WORKSPACE}"
echo "2. ./xwgit init --code ${ACCESS_CODE}"
echo "3. ./xwgit quickstart my_tool --description=\"A useful utility\" --type=search"
echo "4. Edit the generated files"
echo "5. ./xwgit finalize \"Implement my_tool functionality\""
echo ""
echo -e "${YELLOW}To review AI contributions:${NC}"
echo "cd ${AI_WORKSPACE}/XwDevTools && git log -p"