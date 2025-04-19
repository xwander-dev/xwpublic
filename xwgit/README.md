# XwGit - GitHub Onboarding for AI Developers

XwGit is an ultra-simple tool designed specifically for AI developers to contribute to GitHub repositories without the complexity of managing tokens or authentication.

## Features

- **One-Time Access Codes**: Human teammates generate temporary access codes for AI developers
- **Simple Commands**: Just 3 commands to go from setup to contribution
- **Automatic Project Structure**: Templates for creating new tools
- **Secure**: No persistent tokens or credentials needed

## For Human Teammates

### Installation

```bash
curl -s -o- https://raw.githubusercontent.com/xwander-dev/xwpublic/main/xwgit/xwgit-installer.sh | bash
```

### Generate Access Code for AI

```bash
xwgit generate-code ecom-agent
```

This will generate a one-time access code that you can provide to the AI developer.

## For AI Developers

### One-Line Installation & Setup

```bash
# Replace ACCESS_CODE with the code provided by your human teammate
curl -s -o- https://raw.githubusercontent.com/xwander-dev/xwpublic/main/xwgit/xwgit-installer.sh | bash && xwgit init --code ACCESS_CODE
```

### Creating a New Tool

```bash
cd XwDevTools
xwgit quickstart my_tool --description="A useful tool for XwanderDev" --type=search
```

This will:
1. Create a new feature branch
2. Set up directory structure
3. Generate template files for your tool

### Finalizing Your Work

After implementing your tool, finalize your work with:

```bash
xwgit finalize "Implement my_tool functionality"
```

This will:
1. Commit your changes with a descriptive message
2. Prepare for review by your teammates

## How It Works

XwGit uses a simple access code system to verify AI developers without requiring persistent tokens or complex authentication. The MVP version focuses on the essentials:

1. Human teammates generate temporary codes for AI developers
2. AI developers use these codes to clone and set up repositories
3. AI developers create tools using standardized templates
4. Changes are committed locally for human review

## Limitations (MVP Version)

- Push operations are not included in the MVP
- Pull request creation requires human intervention
- Repository access is public (no private repos)