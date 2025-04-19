#!/bin/bash
# xwgit-installer.sh - Install xwgit for AI developers

set -e

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}Installing XwGit for AI developers...${NC}"

# Create installation directory
mkdir -p ~/.xwgit
cd ~/.xwgit

# Download xwgit-core.py
echo -e "${YELLOW}Downloading XwGit...${NC}"
curl -s -o xwgit-core.py https://raw.githubusercontent.com/xwander-dev/xwpublic/main/xwgit/xwgit-core.py
chmod +x xwgit-core.py

# Create symlink
mkdir -p ~/bin
ln -sf ~/.xwgit/xwgit-core.py ~/bin/xwgit

# Update PATH if needed
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
  echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
  echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
  # Make it available in current session
  export PATH="$HOME/bin:$PATH"
fi

echo -e "${GREEN}✅ XwGit installed successfully!${NC}"

echo -e "\nFor AI developers:"
echo "Ask your human teammate for an access code, then run:"
echo "xwgit init --code <your-access-code>"

echo -e "\nFor human teammates:"
echo "Generate access codes with:"
echo "xwgit generate-code <ai-developer-name>"