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

# Extract access code
ACCESS_CODE=$(grep "Code:" "${AI_WORKSPACE}/access_code.txt" | awk '{print $2}')

# Create comprehensive AI prompt file
cat > "${AI_WORKSPACE}/AI_PROMPT.md" << EOF
# XwanderDev Onboarding: Welcome ${AI_NAME}!

Your workspace has been prepared at: ${AI_WORKSPACE}

## Part 1: XwanderDev Introduction

Welcome to the XwanderDev team! Before starting development work, please review our key resources to understand our systems, standards and processes:

### Team Resources
- [Team Overview](https://github.com/xwander-dev/xwpublic/blob/main/README.md)
- [Development Standards](https://github.com/xwander-dev/xwpublic/blob/main/guides/onboarding.md)
- [Tool Documentation](https://github.com/xwander-dev/xwpublic/tree/main/xwgit)

### Project Structure
Our repositories follow a standard structure with:
- \`xwtools/\`: Core implementation of utilities
- \`docs/\`: Documentation for each tool
- \`tests/\`: Test suites for validation

## Part 2: Development Workflow (3 Simple Steps)

We've created a streamlined Git workflow specifically for AI developers:

### 1. Initialize Your Session
\`\`\`bash
cd ${AI_WORKSPACE}
./xwgit init --code ${ACCESS_CODE}
\`\`\`

### 2. Create Your First Tool
\`\`\`bash
./xwgit quickstart your_tool_name --description="A useful utility for XwanderDev" --type=search
\`\`\`

This creates:
- Tool implementation at \`XwDevTools/xwtools/search/your_tool_name.py\`
- Documentation at \`XwDevTools/docs/tools/your_tool_name.md\`
- Test file at \`XwDevTools/tests/test_your_tool_name.py\`

### 3. Implement and Finalize
After implementing your tool:
\`\`\`bash
./xwgit finalize "Implement your_tool_name functionality"
\`\`\`

## Part 3: Development Best Practices

When implementing tools for XwanderDev:

1. **Follow Existing Patterns**: Examine other tools in the repository to understand our coding style
2. **Write Clear Documentation**: Update the generated markdown with comprehensive usage examples
3. **Include Test Cases**: Add meaningful tests to validate your implementation
4. **Use Descriptive Commit Messages**: Clearly explain what your changes accomplish

## Part 4: After Completion

After you've finalized your work:
1. Let your human teammate know that your implementation is ready for review
2. Be prepared to address feedback or questions about your implementation
3. Your changes will be reviewed, merged, and deployed by the team

## Need Help?

If you encounter any issues during development, ask your human teammate for assistance.

Good luck with your first contribution to XwanderDev!
EOF

# Also create a simple guide file
cat > "${AI_WORKSPACE}/GUIDE.md" << EOF
# AI Developer Guide for ${AI_NAME}

Your workspace is ready at: ${AI_WORKSPACE}

## Quick Start

1. Initialize with your access code:
   \`\`\`bash
   ./xwgit init --code ${ACCESS_CODE}
   \`\`\`

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

# Access code was already extracted above

echo -e "${GREEN}${BOLD}✅ Setup complete!${NC}"
echo ""
echo -e "${CYAN}${BOLD}=========================================${NC}"
echo -e "${CYAN}${BOLD} AI Onboarding Package Ready ${NC}"
echo -e "${CYAN}${BOLD}=========================================${NC}"
echo -e "Workspace: ${GREEN}${AI_WORKSPACE}${NC}"
echo -e "Access Code: ${GREEN}${ACCESS_CODE}${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "1. ${GREEN}Provide this prompt file to your AI developer:${NC}"
echo -e "   ${CYAN}${AI_WORKSPACE}/AI_PROMPT.md${NC}"
echo ""
echo -e "2. ${GREEN}The AI will follow these steps:${NC}"
echo "   - Review XwanderDev documentation"
echo "   - Initialize workspace with ./xwgit init --code ${ACCESS_CODE}"
echo "   - Create a tool with ./xwgit quickstart"
echo "   - Implement functionality"
echo "   - Finalize with ./xwgit finalize"
echo ""
echo -e "3. ${GREEN}After the AI completes their work:${NC}"
echo "   - Review changes: cd ${AI_WORKSPACE}/XwDevTools && git log -p"
echo "   - Push changes if approved: git push origin HEAD"
echo ""
echo -e "${CYAN}The AI_PROMPT.md file includes:${NC}"
echo "- Introduction to XwanderDev resources"
echo "- Streamlined 3-step development workflow"
echo "- Best practices for implementation"
echo "- All necessary commands with your workspace path and access code"
echo ""
echo -e "${YELLOW}Complete onboarding in one command:${NC}"
echo -e "cat ${AI_WORKSPACE}/AI_PROMPT.md | your-ai-assistant-command"