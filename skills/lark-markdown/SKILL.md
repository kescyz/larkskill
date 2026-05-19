---
name: lark-markdown
version: 2.0.0
description: "Use this skill when operating Lark Markdown files via LarkSkill MCP: view, create, upload, and edit native Markdown (.md) files stored in Drive. Use when the user needs to create or edit a Markdown file, or read or modify one."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# markdown

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first.
> **Mandatory before execution:** Before invoking any `markdown` operation, read the corresponding command reference doc, then call the operation via `lark_api`.
> **Naming convention:** Markdown operations call `lark_api({ tool: 'markdown', op: '<op>', args: {...} })`.

## Quick Decision

- To **create a native `.md` file**, use `lark_api({ tool: 'markdown', op: 'create', args: {...} })`
- To **read the content of a `.md` file in Drive**, use `lark_api({ tool: 'markdown', op: 'fetch', args: {...} })`
- To perform **partial text replacement / regex replacement** on a Markdown file, use `lark_api({ tool: 'markdown', op: 'patch', args: {...} })`
- To **overwrite-update the content of a `.md` file in Drive**, use `lark_api({ tool: 'markdown', op: 'overwrite', args: {...} })`
- To **import a local Markdown file as a new-version online doc (docx)**, do not use this skill — switch to [`lark-drive`](../lark-drive/SKILL.md) with `lark_api({ tool: 'drive', op: 'import', args: { type: 'docx', ... } })`
- For **rename / move / delete / search / permissions / comments** and other Drive operations on a Markdown file, switch to [`lark-drive`](../lark-drive/SKILL.md)

## Core Boundaries

- This skill handles **Markdown stored as a regular file in Drive**, not docx documents.
- Both `name` and the local `file` filename MUST explicitly include the `.md` suffix; the operation reports an error otherwise.
- `content` accepts a direct string, a local file path (prefixed with `@`), or stdin (`-`).
- `markdown patch` internally: **downloads the full Markdown first, replaces locally, then uploads the entire file as an overwrite**.
- `markdown patch` is NOT a server-side atomic patch; it is a partial-update capability orchestrated on the MCP tool side.
- `markdown patch` currently supports only a **single** `pattern` / `content` pair.
- The final content after `markdown patch` replacement **must not be empty**; if the replacement results in an empty string, the operation reports an error and does not upload the empty file.
- `file` only accepts local `.md` file paths.

## Operations (use via LarkSkill MCP)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'markdown', op: 'create', args: {...} })` | Create a Markdown file in Drive — see [references/lark-markdown-create.md](references/lark-markdown-create.md) |
| `lark_api({ tool: 'markdown', op: 'fetch', args: {...} })` | Fetch a Markdown file from Drive — see [references/lark-markdown-fetch.md](references/lark-markdown-fetch.md) |
| `lark_api({ tool: 'markdown', op: 'patch', args: {...} })` | Patch a Markdown file in Drive via fetch-local-replace-overwrite — see [references/lark-markdown-patch.md](references/lark-markdown-patch.md) |
| `lark_api({ tool: 'markdown', op: 'overwrite', args: {...} })` | Overwrite an existing Markdown file in Drive — see [references/lark-markdown-overwrite.md](references/lark-markdown-overwrite.md) |

## References

- [lark-shared](../lark-shared/SKILL.md) — authentication and global parameters
- [lark-drive](../lark-drive/SKILL.md) — Drive file management, import as docx, move/delete/search, etc.
