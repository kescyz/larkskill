---
name: lark-doc
version: 2.0.0
description: "Use this skill when operating Lark Docs via LarkSkill MCP: create from Markdown, fetch content, update (append/overwrite/replace/insert/delete), upload/download images and files, and search Drive for docs, Wiki nodes, and spreadsheet files. Also the resource-discovery entry for locating Drive objects by name."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# docs

## Prerequisites

- LarkSkill MCP server connected (install via `/plugin marketplace add kescyz/larkskill` → `/plugin install larkskill`, or see https://portal.larkskill.app/setup)
- MCP tools available: `lark_api`, `lark_api_search`
- Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first for auth, global flags, and safety rules

**CRITICAL — Before starting, you MUST first read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling.**

## Core concepts

### Document types and tokens

In the Lark Open Platform, different document types have different URL formats and token-handling rules. When performing document operations (e.g. adding comments, downloading files), you must first obtain the correct `file_token`.

### Document URL formats and token handling

| URL format | Example                                                  | Token type     | Handling |
|------------|----------------------------------------------------------|----------------|----------|
| `/docx/`   | `https://example.larksuite.com/docx/doxcnxxxxxxxxx`      | `file_token`   | The token in the URL path is used directly as `file_token` |
| `/doc/`    | `https://example.larksuite.com/doc/doccnxxxxxxxxx`       | `file_token`   | The token in the URL path is used directly as `file_token` |
| `/wiki/`   | `https://example.larksuite.com/wiki/wikcnxxxxxxxxx`      | `wiki_token`   | WARNING: **Cannot be used directly** — you must first query for the real `obj_token` |
| `/sheets/` | `https://example.larksuite.com/sheets/shtcnxxxxxxxxx`    | `file_token`   | The token in the URL path is used directly as `file_token` |
| `/drive/folder/` | `https://example.larksuite.com/drive/folder/fldcnxxxx` | `folder_token` | The token in the URL path is used as the folder token |

### Wiki link special handling (critical!)

A Wiki link (`/wiki/TOKEN`) may point to different document types such as a doc, spreadsheet, or Base. **Do NOT assume the token in the URL is the `file_token`** — you must first query the actual type and the real token.

#### Processing flow

1. **Call `lark_api` to query node info via the wiki OpenAPI path**

   ```
   Call MCP tool `lark_api`:
   - method: GET
   - path: /open-apis/wiki/v2/spaces/get_node
   - params: { "token": "<wiki_token>" }
   ```

2. **Extract key fields from the response**
   - `node.obj_type`: document type (`docx`/`doc`/`sheet`/`bitable`/`slides`/`file`/`mindnote`)
   - `node.obj_token`: **the real document token** (use this for follow-up operations)
   - `node.title`: document title

3. **Choose follow-up operation by `obj_type`**

   | obj_type | Meaning | Follow-up |
   |----------|---------|-----------|
   | `docx` | New cloud doc | `lark_api({tool: 'docs', op: 'fetch', ...})` / `lark_api({tool: 'docs', op: 'update', ...})` and `lark-drive` for comments |
   | `doc` | Legacy cloud doc | `lark-drive` for comments |
   | `sheet` | Spreadsheet | switch to `lark-sheets` |
   | `bitable` | Base | switch to `lark-base` |
   | `slides` | Slides | switch to `lark-slides` / `lark-drive` |
   | `file` | File | switch to `lark-drive` |
   | `mindnote` | Mind map | switch to `lark-drive` |

#### Query example

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces/get_node
- params: { "token": "<wiki_token>" }
```

Response example:
```json
{
   "node": {
      "obj_type": "docx",
      "obj_token": "xxxx",
      "title": "Title",
      "node_type": "origin",
      "space_id": "12345678910"
   }
}
```

### Resource relationships

```
Wiki Space
└── Wiki Node
    ├── obj_type: docx (new cloud doc)
    │   └── obj_token (real document token)
    ├── obj_type: doc (legacy cloud doc)
    │   └── obj_token (real document token)
    ├── obj_type: sheet (spreadsheet)
    │   └── obj_token (real document token)
    ├── obj_type: bitable (Base)
    │   └── obj_token (real document token)
    └── obj_type: file/slides/mindnote
        └── obj_token (real document token)

Drive Folder
└── File (file/document)
    └── file_token (use directly)
```

## Diagram intent recognition and discovery

Users rarely explicitly say "whiteboard" — **by default**, render diagrams via Lark Whiteboard. Trigger when any of the following signals match:
- User mentions a chart type: architecture diagram, flowchart, sequence diagram, org chart, roadmap, comparison chart, fishbone diagram, flywheel diagram, mind map, etc.
- User expresses visualization intent: "draw it", "lay out the relationships", "draw a flow", "give me a diagram", "easy to present", etc.
- Document topic involves structural relationships, process flow, timelines, or data comparison.

Do NOT add diagrams in these cases: user explicitly refuses; contracts / legal terms / compliance statements (rigorous continuous text); verbatim transcription tasks.

> [!CAUTION]
> Once triggered, you **MUST** first read the `lark-whiteboard` skill reference and **strictly follow its flow**.
>
> **Strictly forbidden**: rendering a PNG via a local whiteboard tool and then inserting it into the document via `docs +media-insert` — diagrams MUST be written into a whiteboard block via the `whiteboard +update` op (see `lark-whiteboard` skill). This is the only legal path.

## Quick decisions
- When the user says "let me see images/attachments/media in the doc" or "preview media", prefer `lark_api({tool: 'docs', op: 'media-preview', ...})`.
- When the user explicitly says "download media", use `lark_api({tool: 'docs', op: 'media-download', ...})`.
- When the target is clearly a whiteboard / whiteboard thumbnail, use `lark_api({tool: 'docs', op: 'media-download', args: { type: 'whiteboard', ... }})` — do NOT use `media-preview`.
- When the user says "find a spreadsheet", "search a spreadsheet by name", "find a report", "recently opened spreadsheets", first use `lark_api({tool: 'docs', op: 'search', ...})` for resource discovery.
- `docs +search` is not limited to docs / Wiki — results may directly include Drive objects such as `SHEET`.
- After getting a spreadsheet URL / token, switch to `lark-sheets` for object-internal read, filter, and write operations.
- When the user says "add a comment to the doc", "view comments", "reply to a comment", "add a reaction to a comment", or "delete a comment reaction", **do NOT stay in `lark-doc`** — switch to `lark-drive` to handle it.

## Additional notes
Beyond searching docs / Wiki, `docs +search` also serves as the "first locate Drive objects, then switch back to the corresponding business skill" resource-discovery entry. When the user verbally says "spreadsheet / report", also start here first.

## Operation index (Shortcuts — recommended first)

A Shortcut is a high-level wrapper for common operations. Call via `lark_api({tool: 'docs', op: '<verb>', args: {...}})`.

| Op | Description |
|----|-------------|
| `lark_api({tool: 'docs', op: 'search', ...})` | Search Lark docs, Wiki, and spreadsheet files (Search v2: doc_wiki/search) |
| `lark_api({tool: 'docs', op: 'create', ...})` | Create a Lark document |
| `lark_api({tool: 'docs', op: 'fetch', ...})` | Fetch Lark document content |
| `lark_api({tool: 'docs', op: 'update', ...})` | Update a Lark document |
| `lark_api({tool: 'docs', op: 'media-insert', ...})` | Insert a local image or file at the end of a Lark document (4-step orchestration + auto-rollback) |
| `lark_api({tool: 'docs', op: 'media-download', ...})` | Download document media or whiteboard thumbnail (auto-detects extension) |
| `lark_api({tool: 'docs', op: 'media-preview', ...})` | Preview document media file (auto-detects extension) |
| (cross-skill) `lark_api({tool: 'whiteboard', op: 'update', ...})` | Alias of `whiteboard +update`. Update an existing whiteboard with DSL, Mermaid or PlantUML — see `lark-whiteboard` skill for details. |

## Core rules

1. **Use only atomic operations** — call one MCP op per intent; do not chain or aggregate multiple ops into a single request.
2. **Resolve wiki tokens first** — for `/wiki/...` inputs, call the wiki node OpenAPI path before using the token in any docs op.
3. **Match URL pattern to op** — confirm the URL type (`/docx/` vs `/doc/` vs `/wiki/`) before deciding token handling.
4. **For diagrams in documents, route to whiteboard** — never round-trip via PNG insert; use the `lark-whiteboard` skill.
5. **For Drive comments / reactions, switch skill** — comments and reactions live under `lark-drive`, not `lark-doc`.
