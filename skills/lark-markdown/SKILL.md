---
name: lark-markdown
version: 1.0.0
description: "Use this skill when creating, fetching, or overwriting Markdown files in Lark Drive via LarkSkill MCP. Handles native .md files stored in Drive — not docx documents."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api"]
---

# markdown (v1)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first — it covers authentication and permission handling.

## Quick decision guide

- User wants to **upload or create a native `.md` file** → use `lark_api({ tool: 'markdown', op: 'create', ... })`
- User wants to **read a `.md` file from Drive** → use `lark_api({ tool: 'markdown', op: 'fetch', ... })`
- User wants to **overwrite an existing `.md` file in Drive** → use `lark_api({ tool: 'markdown', op: 'overwrite', ... })`
- User wants to **import Markdown as an online Docs document (docx)** — do NOT use this skill; use [`lark-drive`](../lark-drive/SKILL.md) with `lark_api({ tool: 'drive', op: 'import', args: { type: 'docx', ... } })`
- User wants to **rename / move / delete / search / manage permissions / add comments** on a Markdown file — do NOT stay in this skill; switch to [`lark-drive`](../lark-drive/SKILL.md)

## Core boundaries

- This skill handles **Markdown files stored as ordinary files in Drive** — not docx documents.
- `--name` and the local `--file` filename MUST explicitly include the `.md` extension; if absent, the shortcut will error immediately.
- `--content` accepts:
  - A direct string value
  - `@file` to read content from a local file
  - `-` to read content from stdin
- `--file` accepts only local `.md` file paths.

## Shortcuts (use these first)

Shortcuts are high-level wrappers for common operations (`lark_api({ tool: 'markdown', op: '<verb>', args: {...} })`). Prefer shortcuts when available.

| Shortcut | Description |
|----------|-------------|
| [`+create`](references/lark-markdown-create.md) | Create a Markdown file in Drive |
| [`+fetch`](references/lark-markdown-fetch.md) | Fetch a Markdown file from Drive |
| [`+overwrite`](references/lark-markdown-overwrite.md) | Overwrite an existing Markdown file in Drive |

### Usage examples

```
// Create a new Markdown file in Drive
lark_api({ tool: 'markdown', op: 'create', args: { name: 'notes.md', content: '# Hello\n\nContent here.' } })

// Fetch an existing Markdown file
lark_api({ tool: 'markdown', op: 'fetch', args: { file_token: '<token>' } })

// Overwrite an existing Markdown file
lark_api({ tool: 'markdown', op: 'overwrite', args: { file_token: '<token>', content: '# Updated\n\nNew content.' } })
```

## References

- [lark-shared](../lark-shared/SKILL.md) — authentication and global parameters
- [lark-drive](../lark-drive/SKILL.md) — Drive file management, docx import, move/delete/search, etc.
