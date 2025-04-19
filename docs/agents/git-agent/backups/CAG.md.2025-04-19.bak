# Git Agent Context Awareness Guide (CAG)

*Last Updated: April 19, 2025*

## Repository Structure

### Organization: xwander-dev
https://github.com/xwander-dev

#### Active Repositories

| Repository | Description | Main Branch | Purpose | Git Policies |
|------------|-------------|------------|---------|--------------|
| [xwpublic](https://github.com/xwander-dev/xwpublic) | Public bootstrapping and onboarding | main | Onboarding tools, documentation | main protected |
| [XwDevTools](https://github.com/xwander-dev/XwDevTools) | Shared tools and utilities | main | Tool implementations | main protected |

### Git Worktree Layout

```
/home/xwander/xwdev/ ← Primary development directory
  ├── xwpublic/      ← Public documentation and tools
  ├── XwDevTools/    ← Development tools repository
  └── xwander-repos/ ← Read-only repository mirrors
      ├── xwpublic/  ← Mirrored repository for context
      └── XwDevTools/ ← Mirrored repository for context
```

## Key Files Index

### Core System Files

| File | Path | Purpose | Key Sections |
|------|------|---------|-------------|
| [GCAG.md](https://github.com/xwander-dev/xwpublic/blob/main/docs/GCAG.md) | /docs/GCAG.md | Global Context Awareness Guide | Repository structure, Team standards, Bot responsibilities |
| [XwCAG.md](https://github.com/xwander-dev/xwpublic/blob/main/docs/XwCAG.md) | /docs/XwCAG.md | CAG system documentation | Concept, Structure, Responsibilities, Process |

### Core Implementation Files

| File | Path | Purpose | Key Functions |
|------|------|---------|--------------|
| [xwgit.py](https://github.com/xwander-dev/xwpublic/blob/main/xwgit/xwgit.py) | /xwpublic/xwgit/xwgit.py | Git workflow automation | contribute, fetch, checkout, add-tool, commit, status |
| [cag-tools.py](https://github.com/xwander-dev/xwpublic/blob/main/tools/cag-tools.py) | /xwpublic/tools/cag-tools.py | CAG management tools | generate_json, verify_hash, backup_cag, distribute_gcag |

## System Responsibilities

### Git Operations

- Repository management (clone, fetch, status)
- Commit and push operations
- Pull request management
- Branch operations
- Code review facilitation

### CAG Maintenance

- Maintain CAG.md under 50K tokens
- Generate and verify CAG.json after edits
- Back up CAG.md to /backups/ directory
- Monitor for GCAG changes and misalignments
- Generate diffs between CAG versions

### GCAG Responsibilities

- Publish Global CAG to /docs/GCAG.md
- Ensure GCAG.json contains accurate metadata
- Distribute GCAG updates to all agent instances
- Validate agent CAG health and compliance

## Common Workflows

### CAG Backup Process

```bash
# Generate backup
cp CAG.md backups/CAG.md.$(date +%Y-%m-%d).bak

# Generate diff
diff -u backups/CAG.md.$(date -d "yesterday" +%Y-%m-%d).bak CAG.md > backups/CAG.diff.$(date -d "yesterday" +%Y-%m-%d)-to-$(date +%Y-%m-%d).txt

# Update JSON
python3 tools/cag-tools.py generate-json --input=CAG.md --output=CAG.json
```

### GCAG Update Process

```bash
# Update GCAG
cp CAG.md ../shared/GCAG.md

# Generate GCAG.json
python3 tools/cag-tools.py generate-json --input=../shared/GCAG.md --output=../shared/GCAG.json

# Commit and push to GitHub
cd /home/xwander/xwdev/xwpublic
./xwgit/xwgit.py commit "Update GCAG to version $(cat ../shared/GCAG.json | jq -r .version)" --push
```

### Agent CAG Health Check

```bash
# Verify agent CAG hash
for agent in git-agent claude-root janitor-agent; do
  python3 tools/cag-tools.py verify-hash --agent=$agent
done

# Notify if misaligned
if [ $? -ne 0 ]; then
  echo "CAG misalignment detected, notifying claude-root"
fi
```

## Patch Standards

Patches to CAG.md follow this naming convention:
`YYYY-MM-DD_cag_patch_NN.md`

Example patch structure:
```
# CAG Patch: 2025-04-19_01

## Section: Repository Structure

### Add
- New repository: xw-examples

### Update
- XwDevTools: Update branch protection rules

### Remove
- Legacy repository references
```

## Recent Updates

### April 19, 2025
- Added XwGit v0.3.1 implementation details
- Updated GCAG with CAG concept documentation
- Created initial CAG.json schema

### April 18, 2025
- Established git-agent as GCAG maintainer
- Added repository structure documentation
- Implemented backup rotation mechanism