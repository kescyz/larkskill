---
name: lark-doc
version: 2.0.0
description: "Lark Docs: create and edit cloud documents. Supports creating from Markdown, fetching document content, updating content (append/overwrite/replace/insert/delete), uploading and downloading media, and searching cloud docs. For spreadsheet/report discovery by title or keyword, use docs +search first."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# docs

> **Prerequisite:** Read [../lark-shared/SKILL.md](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## Core concepts

### Document types and token handling

Different Lark document types have different URL patterns and token semantics. Always resolve the correct token before operations such as comments, media operations, and API calls.

### URL pattern and token mapping

| URL pattern | Example | Token type | Handling |
|---|---|---|---|
| `/docx/` | `https://example.larksuite.com/docx/doxcnxxxxxxxxx` | `file_token` | Use token from URL path directly |
| `/doc/` | `https://example.larksuite.com/doc/doccnxxxxxxxxx` | `file_token` | Use token from URL path directly |
| `/wiki/` | `https://example.larksuite.com/wiki/wikcnxxxxxxxxx` | `wiki_token` | Do not use directly. Resolve real `obj_token` first |
| `/sheets/` | `https://example.larksuite.com/sheets/shtcnxxxxxxxxx` | `file_token` | Use token from URL path directly |
| `/drive/folder/` | `https://example.larksuite.com/drive/folder/fldcnxxxx` | `folder_token` | Use as folder token |

### Wiki URL special handling

A wiki node can point to docx, doc, sheet, bitable, slides, file, or mindnote. Never assume wiki token equals file token.

#### Resolution flow

1. Query node info via `lark_api`:

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces/get_node
- params: { "token": "<wiki_token>" }
```

2. Extract fields:
   - `node.obj_type`
   - `node.obj_token`
   - `node.title`
3. Route API/tool by `obj_type`.

| obj_type | Type | Typical API |
|---|---|---|
| `docx` | New docs | `drive file.comments.*`, `docx.*` |
| `doc` | Legacy docs | `drive file.comments.*` |
| `sheet` | Sheets | `sheets.*` |
| `bitable` | Base | `bitable.*` |
| `slides` | Slides | `drive.*` |
| `file` | File | `drive.*` |
| `mindnote` | Mind map | `drive.*` |

#### Example Response

```json
{
   "node": {
      "obj_type": "docx",
      "obj_token": "xxxx",
      "title": "title",
      "node_type": "origin",
      "space_id": "12345678910"
   }
}
```

### Resource relationship

```
Wiki Space (Knowledge Space)
└── Wiki Node (knowledge base node)
    ├── obj_type: docx (new version document)
    │ └── obj_token (real document token)
    ├── obj_type: doc (old version document)
    │ └── obj_token (real document token)
    ├── obj_type: sheet (spreadsheet)
    │ └── obj_token (real document token)
    ├── obj_type: bitable (multidimensional table)
    │ └── obj_token (real document token)
    └── obj_type: file/slides/mindnote
        └── obj_token (real document token)

Drive Folder (cloud space folder)
└── File (file/document)
    └── file_token (direct use)
```

## Important: whiteboard editing

> `lark-doc` cannot directly edit existing whiteboard content. `docs +update` can create blank whiteboards.

### Case 1: whiteboard already exists (from `docs +fetch`)

If fetched markdown contains `<whiteboard token="xxx"/>`:
1. Record the whiteboard token.
2. Switch to [`../lark-whiteboard/SKILL.md`](../lark-whiteboard/SKILL.md) for whiteboard content editing.

### Case 2: blank whiteboard was just created

If user created blank whiteboard via `docs +update`:
1. Use `<whiteboard type="blank"></whiteboard>` in the markdown content.
2. For multiple blank whiteboards, repeat the tag in the same markdown.
3. Read `data.board_tokens` from update response.
4. Use returned tokens for next whiteboard edits in `lark-whiteboard`.

## Quick routing

- For requests like "find a spreadsheet", "find report by name", "recently opened table", use `docs +search` first.
- `docs +search` returns `SHEET` and other cloud object types, not only docs/wiki.
- After locating spreadsheet URL/token, switch to `lark-sheets` for object-level reads/writes/filters.

## Additional note

`docs +search` is both a docs/wiki search and a cloud object discovery entrypoint.

## Shortcuts (preferred)

| Shortcut | Description |
|---|---|
| [`+search`](references/lark-doc-search.md) | Search docs/wiki/spreadsheet files (Search v2: doc_wiki/search) |
| [`+create`](references/lark-doc-create.md) | Create a Lark document |
| [`+fetch`](references/lark-doc-fetch.md) | Fetch document content |
| [`+update`](references/lark-doc-update.md) | Update document content |
| [`+media-insert`](references/lark-doc-media-insert.md) | Insert local image/file at end of document |
| [`+media-download`](references/lark-doc-media-download.md) | Download document media or whiteboard thumbnail |
| [`+whiteboard-update`](references/lark-doc-whiteboard-update.md) | Update an existing whiteboard using whiteboard DSL |
