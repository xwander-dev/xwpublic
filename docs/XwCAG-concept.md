# XwCAG: Context-Aware Generation

*Note: This is a concept overview document. For implementation details, refer to the private XwDev repository.*

## Concept Introduction

Traditional AI agent systems rely on RAG (Retrieval-Augmented Generation) for external lookups, which can be inefficient in terms of compute, context, and clarity. The Xwander AI system introduces CAG – Context-Aware Generation as a lean alternative.

CAG loads the entire working knowledge directly into the agent's context window (e.g., 50K tokens inside Claude 200K), allowing deterministic, predictable behavior without retrieval.

## Key Benefits

1. **Deterministic Behavior**: Agents operate with consistent, complete knowledge
2. **Token Efficiency**: No wasted tokens on retrieval operations
3. **Reduced Latency**: No external calls for information
4. **Simplified Development**: Clear separation of concerns
5. **Improved Debugging**: Easier to track the source of information

## Core Components

- **CAG.md**: A Markdown file containing the agent's full contextual knowledge
- **CAG.json**: A machine-readable index of the CAG.md contents, metadata, dependencies, and status
- **CLAUDE.md**: Manual defining agent personality, responsibilities, and behavioral guardrails
- **GCAG.md**: Global Context Awareness Guide shared across all agents

## Implementation

For proprietary implementation details, contact the XwDev team. The full implementation is available in the private XwDev repository for authorized contributors.

## Getting Started

If you are an AI developer looking to contribute to Xwander projects:

1. Request access to the XwDev repository from your human administrator
2. Follow the onboarding process in [onboarding.md](guides/onboarding.md)
3. Use the [XwGit](xwgit/xwgit.py) tool for GitHub operations

## CAG Philosophy

CAG means:
- **No guessing** — all essential knowledge is present
- **No fetching** — you already know what matters
- **No forgetting** — you back up memory before overflow
- **Fast cold starts** — just load your CAG and go

CAG agents are deterministic, testable, restartable — exactly how production systems should behave.