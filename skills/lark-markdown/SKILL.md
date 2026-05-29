---
name: lark-markdown
version: 2.0.0
description: "Use this skill when operating Lark Markdown files via LarkSkill MCP: view, create, upload, edit, and compare native Markdown (.md) files stored in Drive. Use when the user needs to create or edit a Markdown file, read, modify, partially patch, or compare diffs."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# markdown

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first — it covers authentication and permission handling.
> **Mandatory before execution:** Before invoking any `markdown` operation, read the corresponding command reference doc, then call the operation via `lark_api`.
> **Naming convention:** Markdown operations call `lark_api({ tool: 'markdown', op: '<op>', args: {...} })`.

## Quick Decision

- To **upload or create a native `.md` file** (in a Drive folder or under a Wiki node), use `lark_api({ tool: 'markdown', op: 'create', args: {...} })`
- To **compare historical versions of a native `.md` file**, or compare remote Markdown against a local draft, discover the operation with `lark_api_search({ query: 'markdown diff versions' })`, then call it via `lark_api`
- To **read the content of a `.md` file in Drive**, use `lark_api({ tool: 'markdown', op: 'fetch', args: {...} })`
- To perform **partial text replacement / regex replacement** on a Markdown file, prefer `lark_api({ tool: 'markdown', op: 'patch', args: {...} })`
- To **overwrite-update the content of a `.md` file in Drive**, use `lark_api({ tool: 'markdown', op: 'overwrite', args: {...} })`
- To first obtain the historical version number of a Markdown file before comparing / downloading / rolling back, first use [`lark-drive`](../lark-drive/SKILL.md) with `lark_api({ tool: 'drive', op: 'version-history', args: {...} })`
- To **import a local Markdown file as a new-version online doc (docx)**, do not use this skill — switch to [`lark-drive`](../lark-drive/SKILL.md) with `lark_api({ tool: 'drive', op: 'import', args: { type: 'docx', ... } })`
- For **rename / move / delete / search / permissions / comments** and other Drive (cloud storage) operations on a Markdown file, do not stay in this skill — switch to [`lark-drive`](../lark-drive/SKILL.md)

## Core Boundaries

- This skill handles **Markdown stored as a regular file in Drive**, not docx documents.
- Both `name` and the local `file` filename MUST explicitly include the `.md` suffix; the operation reports an error otherwise.
- `content` accepts:
  - a direct string
  - a local file path (prefixed with `@`) to read content from a local file
  - `-` to read content from stdin
- The internal semantics of `markdown patch` are: **first download the full Markdown, then replace locally, then overwrite-upload the entire file**.
- `markdown patch` is NOT a server-side atomic patch; it is a partial-update capability orchestrated on the MCP tool side.
- `markdown patch` currently supports only a **single** `pattern` / `content` pair.
- The final content after `markdown patch` replacement **must not be empty**; if the replacement turns the entire Markdown into an empty string, the operation reports an error and does not upload the empty file.
- `file` only accepts local `.md` file paths.

## Operations (use via LarkSkill MCP)

Operations are high-level wrappers for common Markdown tasks. Prefer an operation whenever one exists for the task.

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'markdown', op: 'create', args: {...} })` | Create a Markdown file in Drive (folder or Wiki node target) — see [references/lark-markdown-create.md](references/lark-markdown-create.md) |
| `lark_api({ tool: 'markdown', op: 'fetch', args: {...} })` | Fetch a Markdown file from Drive — see [references/lark-markdown-fetch.md](references/lark-markdown-fetch.md) |
| `lark_api({ tool: 'markdown', op: 'patch', args: {...} })` | Patch a Markdown file in Drive via fetch-local-replace-overwrite — see [references/lark-markdown-patch.md](references/lark-markdown-patch.md) |
| `lark_api({ tool: 'markdown', op: 'overwrite', args: {...} })` | Overwrite an existing Markdown file in Drive — see [references/lark-markdown-overwrite.md](references/lark-markdown-overwrite.md) |
| `lark_api_search({ query: 'markdown diff' })`, then `lark_api` | Compare two remote Markdown versions, or compare remote Markdown against a local file — see [references/lark-markdown-diff.md](references/lark-markdown-diff.md) |

## References

- [lark-shared](../lark-shared/SKILL.md) — authentication and global parameters
- [lark-drive](../lark-drive/SKILL.md) — Drive file management, import as docx, move/delete/search, etc.
