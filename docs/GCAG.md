# Global Context Awareness Guide (GCAG)

*Version: 0.0.1*  
*Last Updated: April 19, 2025*  
*Maintained by: git-agent*

This document serves as the Global Context Awareness Guide for all Xwander AI agents. It provides shared context, standards, and reference information required by all agents in the ecosystem.

## Team Structure

### Agent Hierarchy

```
claude-root
├── git-agent      ← GCAG Maintainer
├── janitor-agent
├── sysadmin-agent
└── [project-agents]
```

### Agent Responsibilities

| Agent | Primary Role | Secondary Roles | CAG Status |
|-------|-------------|----------------|------------|
| claude-root | System coordination | Inter-agent communication, Task delegation | Consumer |
| git-agent | Git operations | CAG maintenance, GCAG distribution | Maintainer |
| janitor-agent | System cleanup | Log rotation, Resource optimization | Consumer |
| sysadmin-agent | System administration | Service management, Security | Consumer |

## Project Standards

### Repository Structure

All repositories should follow this standard structure:

```
repository/
├── docs/               # Documentation
│   └── README.md       # Project overview
├── src/                # Source code
│   └── [modules]/      # Code modules
├── tests/              # Test implementations
│   └── [test-modules]/ # Test modules
└── tools/              # Utility scripts
```

### Documentation Standards

1. **README.md**: All repositories must have a comprehensive README.md
2. **API Documentation**: All APIs must have OpenAPI/Swagger documentation
3. **Code Comments**: All functions must have docstrings
4. **Implementation Notes**: Complex algorithms must have implementation notes

### Commit Standards

Commit messages must follow this format:
```
[Type]: Brief description

Longer description if needed
```

Types: `Add`, `Update`, `Fix`, `Refactor`, `Docs`, `Test`

Example: `Add: Perplexity search integration`

## Common Workflows

### New Tool Implementation

1. Use `xwgit.py contribute [category]/[name] "Description"`
2. Implement the core functionality
3. Add comprehensive tests
4. Update documentation
5. Commit and push changes

### Issue Resolution

1. Identify the issue scope and impact
2. Create a new branch: `fix/issue-description`
3. Implement the fix with appropriate tests
4. Document the resolution
5. Create a pull request

## Security Policies

1. **API Keys**: All keys must be stored in .env files, never in code
2. **Token Management**: GitHub tokens must be rotated every 30 days
3. **Access Control**: Repositories must use branch protection
4. **Secret Scanning**: All commits must be checked for secrets
5. **Vulnerability Reporting**: Report all security issues to claude-root

## Context Management

### CAG Structure

All agent CAG files must:
1. Be under 50K tokens
2. Have an associated CAG.json with metadata
3. Include version and last updated timestamp
4. Be backed up before major changes

### CAG Optimization Guidelines

1. **Prioritization**: Mark sections as P0 (critical), P1 (important), P2 (useful)
2. **Condensation**: Summarize detailed information, keep examples minimal
3. **Deprecation**: Remove outdated information regularly
4. **Linking**: Use references instead of duplicating information

## Environment Overview

### Development Environment

```
/home/xwander/xwdev/
├── [repositories]/
├── xwdata/
│   ├── memory/       # Agent memory storage
│   └── reports/      # Agent reports
└── valuable_assets/  # Critical resources
```

### Production Environment

```
/srv/www/erasoppi.fi/
├── [ai-name]-workspace/
│   ├── .env          # Environment variables
│   └── github-tool.sh # GitHub helper script
└── [workspaces]/     # Multiple AI workspaces
```

## CAG Implementation Reference

### CAG.md Template

```markdown
# Context Awareness Guide

## Repository Structure
...

## Key Files Index
...

## System Responsibilities
...

## Common Workflows
...

## Recent Updates
...
```

### CAG.json Schema

```json
{
  "version": "0.0.1",
  "lastUpdated": "2025-04-19T14:30:00Z",
  "hash": "sha256:...",
  "tokenCount": 42500,
  "gcagVersion": "0.0.1",
  "gcagHash": "sha256:...",
  "dependencies": [
    {"agent": "claude-root", "version": "0.0.1", "hash": "sha256:..."}
  ],
  "sections": [
    {"name": "Repository Structure", "startLine": 5, "endLine": 30},
    {"name": "Key Files Index", "startLine": 32, "endLine": 120}
  ]
}
```

## Recent Updates

### April 19, 2025
- Created initial GCAG structure
- Added agent hierarchy and responsibilities
- Documented CAG standards and optimization guidelines
- Established common workflows
- Defined security policies