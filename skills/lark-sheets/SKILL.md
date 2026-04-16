---
name: lark-sheets
version: 2.0.0
description: "Lark Sheets: read/write spreadsheet cells, create spreadsheets, search cells, export, append rows, and get sheet metadata. Use when users need to read or write spreadsheet data, create new spreadsheets, search cell values, export to xlsx/csv, or discover spreadsheet files by name/keyword."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# sheets

> **Prerequisite:** Read [../lark-shared/SKILL.md](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## Wiki URL special handling

A wiki node can point to docx, doc, sheet, bitable, slides, file, or mindnote. Never assume wiki token equals spreadsheet token.

#### Resolution flow

Call `lark_api` to resolve wiki token first:

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
      "obj_type": "sheet",
      "obj_token": "xxxx",
      "title": "title",
      "node_type": "origin",
      "space_id": "12345678910"
   }
}
```

When `obj_type = "sheet"`, use `node.obj_token` as `spreadsheet_token` for subsequent operations.

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

## Filter operations (native API)

When using spreadsheet filter operations, call the native API directly via `lark_api`:

Step 1 — Delete existing filters (if any):
```
Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/filter
```

Step 2 — Create filter condition:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/filter
- body:
  {
    "col": "B",
    "condition": { "expected": ["xx"], "filter_type": "multiValue" },
    "range": "<sheet_id>!B1:E200"
  }
```

Step 3 — Add additional filter condition:
```
Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/filter
- body:
  {
    "col": "E",
    "condition": { "expected": ["xx"], "filter_type": "multiValue" }
  }
```

## Shortcuts (read reference first)

Read the reference doc before using any shortcut.

| Shortcut | Description |
|---|---|
| [`+info`](references/lark-sheets-info.md) | View spreadsheet/sheet metadata — resolve token from URL, list sheets |
| [`+read`](references/lark-sheets-read.md) | Read cells from a range |
| [`+write`](references/lark-sheets-write.md) | Write cells / overwrite a range |
| [`+append`](references/lark-sheets-append.md) | Append rows after existing data |
| [`+find`](references/lark-sheets-find.md) | Find cells matching a value or regex within a known spreadsheet |
| [`+create`](references/lark-sheets-create.md) | Create a new spreadsheet |
| [`+export`](references/lark-sheets-export.md) | Export spreadsheet to xlsx or csv |

## API Resources

All sheets APIs use the base paths `/open-apis/sheets/v2/` and `/open-apis/sheets/v3/`.

### spreadsheets (metadata)

- `get` — `GET /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}`
- `create` — `POST /open-apis/sheets/v3/spreadsheets`
- `patch` — `PATCH /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}`

### spreadsheets.sheets

- `list` — `GET /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets`
- `get` — `GET /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}`

### spreadsheets.values (read/write cells)

- `get` (read range) — `GET /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}`
- `update` (write range) — `PUT /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}`
- `append` — `POST /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_append`

### spreadsheets.sheet.filters

- `create` — `POST /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/filter`
- `update` — `PUT /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/filter`
- `delete` — `DELETE /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/filter`
- `get` — `GET /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/filter`

### spreadsheets.sheet.find_replace

- `find` — `POST /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/find`
- `replace` — `POST /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/replace`

## Permission Table

| Operation | Required Scope |
|-----------|---------------|
| Read spreadsheet metadata | `sheets:spreadsheet:readonly` |
| Read cell values | `sheets:spreadsheet:readonly` |
| Write cell values | `sheets:spreadsheet` |
| Create spreadsheet | `sheets:spreadsheet` |
| Manage permissions | `drive:permission:write` |
