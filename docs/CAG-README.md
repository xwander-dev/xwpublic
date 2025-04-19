# 🧠 CAG: Context-Aware Generation  
### Version 0.0.2 — MVP Agent Knowledge System

---

## 📌 Summary

**Context-Aware Generation (CAG)** replaces traditional RAG systems by embedding each Claude Code agent's operational knowledge directly into the context window at runtime.

Rather than fetching knowledge from external sources, each agent operates using:
- A clean, **bounded `CAG.md` file** under ~50K tokens  
- A `CAG.json` manifest to track metadata, integrity, and dependencies  
- An optional `GCAG.md` (Global CAG) for shared teamwide context

This MVP version (v0.0.2) enables:
- Context-aware agent execution
- Safe memory compaction with `CAG.md` backups
- Global knowledge mounting via GCAG
- Deterministic behavior without retrieval overhead

---

## 🧩 Core Structure

Each agent maintains the following:

```
agents/<agent-name>/
├── CLAUDE.md            ← Personality, responsibilities, boundaries
├── CAG.md               ← Context memory: agent's working knowledge (≤50K tokens)
├── CAG.json             ← Manifest: metadata, structure, dependencies
├── backups/
│   └── CAG.md.2025-04-20.bak
└── shared/
    ├── GCAG.md          ← Shared global knowledge (mounted)
    └── GCAG.json
```

---

## 🧠 CAG.md

This is the **core memory** of the agent. It includes:

- High-level responsibilities
- API usage, environment variables, authentication schemes
- Key file paths, scripts, and runtime behaviors
- Common commands and patterns (e.g. Slack formatting, script templates)
- Current implementation status (optional)

### ✅ Key Rules
- Must be concise, token-optimized, and readable
- Maintained manually
- Backed up after meaningful edits

---

## 🧾 CAG.json

This file describes the **structure and integrity** of the agent's CAG. It helps with:

- Tracking dependencies (scripts, .env, etc.)
- Logging hash/version for rotation
- Indexing sections of `CAG.md`
- Noting recovery instructions

### Example:
```json
{
  "version": "0.0.2",
  "agent_role": "ecom-agent",
  "updated": "2025-04-20T08:42:00Z",
  "hash": "",
  "dependencies": [
    ".env",
    "scripts/hubspot/hubspot.py",
    "scripts/slack/pick_pack_report.php"
  ],
  "includes": [
    "section::responsibilities",
    "section::authentication",
    "section::file_paths"
  ],
  "backup": "backups/CAG.md.2025-04-20.bak",
  "diff_since": null,
  "context_saturation_warning": false,
  "recovery_instructions": "See CAG Compaction Plan in CLAUDE.md"
}
```

---

## 🌍 GCAG: Global Context-Aware Generation

GCAG is a **shared context file** available to all agents. It is typically mounted from:

```
/shared/GCAG.md
```

It contains:
- Team values and protocol rules
- Shared tools (XwDevTools)
- Git strategy, logging conventions
- Handover specs and message formats

### Rules:
- Each agent may reference `GCAG.md` in its `CAG.md`
- Managed primarily by `git-agent`
- Synced semi-automatically by human or system supervision

---

## 🔁 CAG Lifecycle in v0.0.2

### Agent Start
- Load `CLAUDE.md`, `CAG.md`, and `GCAG.md`
- Check `CAG.json` for integrity and hash status

### Agent Use
- Operates within memory window defined by `CAG.md`

### Agent Exit
- Save `CAG.md` backup to `backups/`
- Update `CAG.json` (timestamp, hash if available)

---

## 👁 CAG Philosophy

CAG means:
- **No guessing** — all essential knowledge is present
- **No fetching** — you already know what matters
- **No forgetting** — you back up memory before overflow
- **Fast cold starts** — just load your CAG and go

CAG agents are deterministic, testable, restartable — **exactly how production systems should behave**.

---

## 📂 Contribution Guidelines

- Back up `CAG.md` before edits
- Use structured sections with anchors (e.g. `## 3. Authentication`)
- Keep GCAG references up to date
- Avoid hardcoding tokens or passwords into `CAG.md`
- Prefer "what to do" over "how I did it" unless documenting a confirmed fix
- Implement token optimization strategies to keep CAG files under limits

---

## 🔄 Implementation Roadmap

- **v0.0.1**: Git Agent CAG Prototype (Completed)
- **v0.0.2**: MVP Agent Knowledge System (Current)
- **v0.1.0**: Multi-Agent CAG Implementation
- **v1.0.0**: Production-Ready CAG System

---

© 2025 — Xwander AI Agent System  
CAG v0.0.2 MVP by Joni Kautto & Claude Code