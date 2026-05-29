---
name: lark-doc
version: 2.0.0
description: "Lark Docs / Docx / Wiki (v2): create, read, update, summarize, and edit document content via LarkSkill MCP. Use when given a Lark doc URL/token (route doubao.com /docx/ and /wiki/ URLs by path, not domain) or asked to fetch, append, replace, move, or insert/download media. Always carry api_version v2; DocxXML default."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# docs (v2)

> **⚠️ API Version: This skill uses the v2 API. All `docs create`, `docs fetch`, and `docs update` calls via `lark_api` MUST include `api_version: "v2"`.**

```javascript
// Common examples
lark_api({ tool: 'docs', op: 'fetch', args: { doc: '<doc URL or token>', api_version: 'v2' } })
lark_api({ tool: 'docs', op: 'create', args: { api_version: 'v2', content: '<title>Title</title><p>Content</p>' } })
lark_api({ tool: 'docs', op: 'update', args: { doc: '<doc URL or token>', api_version: 'v2', command: 'append', content: '<p>Content</p>' } })
```

## Prerequisites — MUST read before executing operations

**CRITICAL — Before executing the corresponding operation, MUST use the Read tool to read the following files. None may be skipped:**
1. [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) — authentication, permission handling, global parameters (applies to all operations)
2. **Reading a document (`docs fetch --api-version v2`)** → MUST read [`lark-doc-fetch.md`](references/lark-doc-fetch.md) (`--scope` / `--detail` selection, partial read strategy, `<fragment>` / `<excerpt>` output structure)
3. **Creating or editing document content** → MUST read [`lark-doc-xml.md`](references/lark-doc-xml.md) (XML syntax rules; only read [`lark-doc-md.md`](references/lark-doc-md.md) when the user explicitly requests Markdown); for creating from scratch also read [`lark-doc-create-workflow.md`](references/style/lark-doc-create-workflow.md); for editing an existing document also read [`lark-doc-update-workflow.md`](references/style/lark-doc-update-workflow.md)

**Executing the corresponding operation without first reading the above files will result in incorrect parameter selection, format errors, or substandard styling.**

> **Format selection rules (global):**
> - **Create / import scenarios** (`docs create`, or whole-block writes via `docs update` with `command: "append"/"overwrite"`): XML and Markdown are both supported. When the user provides a local `.md` file or explicitly says "import Markdown", use Markdown directly; otherwise default to XML (supports callout, grid, checkbox and other rich blocks).
> - **Precise edit scenarios** (`docs update` with `str_replace` / `block_insert_after` / `block_replace` / `block_delete` / `block_move_after` and similar targeted commands): prefer XML (`doc_format: "xml"`, which is the default). XML reliably expresses block structure and styles, giving more control for targeted edits; do not switch to Markdown just because it seems simpler.

## Quick decisions
- When the user needs a "direct link / anchor link to a specific block": return `<doc base URL>#block_id`. If you currently have only the document URL and no block_id, first use `lark_api({ tool: 'docs', op: 'fetch', args: { doc: '<token>', api_version: 'v2', detail: 'with-ids' } })` to obtain the target block's id
- Example:
  - Known document URL = `https://xxx.feishu.cn/docx/doxcn123`
  - Known block_id = `blkcn456`
  - Should return `https://xxx.feishu.cn/docx/doxcn123#blkcn456`
- When the user needs to **create, copy, or move** resource blocks in a document (whiteboards, Sheets, Base, etc.), MUST first read the "III. Resource Blocks" section of [`lark-doc-xml.md`](references/lark-doc-xml.md)
- When writing documents, important information (core workflows, architecture, comparisons, risks, roadmaps, key metrics, causal relationships) should be planned as whiteboards first — do not rely only on text or tables
- New whiteboards MUST be isolated to a SubAgent: simple diagrams have the SubAgent insert `<whiteboard type="svg">full SVG</whiteboard>` directly without reading `lark-whiteboard`; only complex diagrams have the main Agent first create `<whiteboard type="blank"></whiteboard>`, then launch a SubAgent to read `lark-whiteboard` and write into it
- User says "view images/attachments/media in the document" or "preview media" → use `lark_api({ tool: 'docs', op: 'media-preview', args: { doc: '<token>' } })`
- User explicitly says "download media" → use `lark_api({ tool: 'docs', op: 'media-download', args: { ... } })`
- If the target is a whiteboard/whiteboard thumbnail → MUST use `lark_api({ tool: 'docs', op: 'media-download', args: { type: 'whiteboard', token: '<whiteboard_token>' } })` (do NOT use `media-preview`)
- User says "find a table", "search a spreadsheet by name", "find a report", "recently opened spreadsheet", "recently edited xxx" → use `lark_api({ tool: 'drive', op: 'search', args: { ... } })` directly (see [`lark-drive`](../lark-drive/references/lark-drive-search.md)). **The old `docs search` is in maintenance mode and will be retired; do not add new dependencies on it.**
- `drive search` results directly return `SHEET` / `Base` / `FOLDER` and other Drive objects — it is the unified entry point for resource discovery
- After obtaining a spreadsheet URL/token → switch to `lark-sheets` for in-object operations
- User says "add a comment to the document", "view comments", "reply to a comment", "add/remove an emoji reaction on a comment" → switch to `lark-drive` to handle
- When document content contains embedded `<sheet>`, `<bitable>`, or `<cite file-type="sheets|bitable">` tags → **MUST proactively extract the token and switch to the corresponding skill to drill into the internal data; do not present only the tag itself**

| Tag / attribute | Field to extract | Switch to skill |
|-|-|-|
| `<sheet token="..." sheet-id="...">` | `token` -> spreadsheet_token, `sheet-id` | [`lark-sheets`](../lark-sheets/SKILL.md) |
| `<bitable token="..." table-id="...">` | `token` -> app_token, `table-id` | [`lark-base`](../lark-base/SKILL.md) |
| `<cite type="doc" file-type="sheets" token="..." sheet-id="...">` | same as `<sheet>` | [`lark-sheets`](../lark-sheets/SKILL.md) |
| `<cite type="doc" file-type="bitable" token="..." table-id="...">` | same as `<bitable>` | [`lark-base`](../lark-base/SKILL.md) |
| `<synced_reference src-token="..." src-block-id="...">` | `src-token` -> doc_token, `src-block-id` -> block_id | Use `lark_api({ tool: 'docs', op: 'fetch', args: { doc: '<src-token>', api_version: 'v2' } })` to read the src-token document and locate the block |

**Note:** Unified Drive resource discovery uses `lark_api({ tool: 'drive', op: 'search', args: { ... } })`; when the user verbally says "table/report/recently edited xxx", also start with `drive search`. The old `docs search` is retained only in existing scripts; it will be retired going forward.

## Shortcuts (use these first)

Shortcuts are high-level wrappers for common operations via the LarkSkill MCP tool. When a shortcut exists for an operation, use it first.

| Shortcut | Description |
|----------|------|
| [`search`](references/lark-doc-search.md) | ⚠️ **Deprecated — use `lark_api({ tool: 'drive', op: 'search', args: { ... } })`**. Search Lark docs, Wiki, and spreadsheet files. Kept for back-compat only. |
| [`create`](references/lark-doc-create.md) | `lark_api({ tool: 'docs', op: 'create', args: { api_version: 'v2', ... } })` — Create a Lark document (XML / Markdown) |
| [`fetch`](references/lark-doc-fetch.md) | `lark_api({ tool: 'docs', op: 'fetch', args: { doc: '<token>', api_version: 'v2', ... } })` — Fetch Lark document content (XML / Markdown) |
| [`update`](references/lark-doc-update.md) | `lark_api({ tool: 'docs', op: 'update', args: { doc: '<token>', api_version: 'v2', ... } })` — Update a Lark document (str_replace / block_insert_after / block_replace / ...) |
| [`media-insert`](references/lark-doc-media-insert.md) | `lark_api({ tool: 'docs', op: 'media-insert', args: { ... } })` — Insert a local image or file at the end of a Lark document (4-step orchestration + auto-rollback). Prefer `from_clipboard: true` when the image is already on the system clipboard (screenshots, copy from Lark/browser); use `file: '<path>'` only for on-disk sources. |
| [`media-download`](references/lark-doc-media-download.md) | `lark_api({ tool: 'docs', op: 'media-download', args: { ... } })` — Download document media or whiteboard thumbnail (auto-detects extension) |
| [`media-preview`](references/lark-doc-media-preview.md) | `lark_api({ tool: 'docs', op: 'media-preview', args: { ... } })` — Preview document media file (auto-detects extension) |
| [`whiteboard-update`](../lark-whiteboard/references/lark-whiteboard-update.md) | `lark_api({ tool: 'whiteboard', op: 'update', args: { ... } })` — Update an existing whiteboard with DSL, Mermaid or PlantUML. Refer to lark-whiteboard skill for details. |
