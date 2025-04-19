# XwGit: Sysadmin Setup Guide

This guide is for system administrators to set up XwGit for AI developers on your team.

## Step 1: Install XwGit Tools

```bash
# Create a dedicated directory for AI development
mkdir -p /shared/ai-workspace
cd /shared/ai-workspace

# Download and install XwGit
curl -s -o- https://raw.githubusercontent.com/xwander-dev/xwpublic/main/xwgit/xwgit-installer.sh | bash

# Ensure it's in the path
export PATH="$HOME/bin:$PATH"
```

## Step 2: Clone and Prepare the Target Repository

```bash
# Clone the repository
git clone https://github.com/xwander-dev/XwDevTools.git
cd XwDevTools

# Set permissions (important!)
chmod -R 775 .
```

## Step 3: Create a Workspace for Each AI Developer

```bash
# For ecom-agent:
cp -r /shared/ai-workspace/XwDevTools /shared/ai-workspace/ecom-agent-workspace
cd /shared/ai-workspace/ecom-agent-workspace

# Initialize git identity for the AI
git config --local user.name "AI-ecom-agent"
git config --local user.email "ecom-agent@ai.xwander.dev"

# Create the required directories if they don't exist
mkdir -p xwtools/search xwtools/api docs/tools tests
```

## Step 4: Generate an Access Code for the AI Developer

```bash
cd /shared/ai-workspace
xwgit generate-code ecom-agent
```

You'll receive an access code to provide to the AI developer.

## Step 5: Provide Instructions to the AI Developer

Give the AI developer the path to the prepared workspace and the access code:

```
Your workspace is ready at: /shared/ai-workspace/ecom-agent-workspace
Your access code is: XGZF6VOC

Please see the AI_DEVELOPER_GUIDE.md file in your workspace for next steps.
```

## Regular Maintenance

After the AI developer commits changes:

```bash
# Review and push changes
cd /shared/ai-workspace/ecom-agent-workspace
git log -p
git push origin main

# Create PR if needed
gh pr create --title "AI contribution from ecom-agent" --body "Work done by ecom-agent"
```