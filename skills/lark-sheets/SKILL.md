---
name: lark-sheets
version: 2.0.0
description: "Use this skill when operating Lark Sheets via LarkSkill MCP: create spreadsheets, manage sheets, read/write cells, append rows, find content, and export files. To search for spreadsheet files by name or keyword, use the docs search operation first."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# sheets

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first.
> **Mandatory before execution:** Before invoking any `sheets` operation, read the corresponding command reference doc, then call the operation via `lark_api`.
> **Naming convention:** Sheets operations call `lark_api({ tool: 'sheets', op: '<op>', args: {...} })`; if a Wiki link must be resolved first, call `lark_api` with the HTTP form `{ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_token>' } }` first.

## Quick Decision

- To find spreadsheet files in Drive by title or keyword, use `lark_api({ tool: 'docs', op: 'search', args: {...} })` first.
- `docs search` returns `SHEET` results directly — do not assume it only searches docs or Wikis.
- Once you have a spreadsheet URL or token, proceed to internal object operations such as `lark_api({ tool: 'sheets', op: 'info', args: {...} })`, `lark_api({ tool: 'sheets', op: 'read', args: {...} })`, `lark_api({ tool: 'sheets', op: 'find', args: {...} })`, etc.

## Core Concepts

### Document Types and Tokens

In the Lark open platform, different document types have different URL formats and token handling. Before performing document operations (such as adding comments or downloading files), you must first obtain the correct `file_token`.

### Document URL Format and Token Handling

| URL Format | Example | Token Type | Handling |
|------------|---------|------------|----------|
| `/docx/` | `https://example.larksuite.com/docx/doxcnxxxxxxxxx` | `file_token` | Token in URL path is used directly as `file_token` |
| `/doc/` | `https://example.larksuite.com/doc/doccnxxxxxxxxx` | `file_token` | Token in URL path is used directly as `file_token` |
| `/wiki/` | `https://example.larksuite.com/wiki/wikcnxxxxxxxxx` | `wiki_token` | ⚠️ **Cannot be used directly** — must query first to obtain the real `obj_token` |
| `/sheets/` | `https://example.larksuite.com/sheets/shtcnxxxxxxxxx` | `file_token` | Token in URL path is used directly as `file_token` |
| `/drive/folder/` | `https://example.larksuite.com/drive/folder/fldcnxxxx` | `folder_token` | Token in URL path is used as the folder token |

### Wiki Link Special Handling (Critical!)

Wiki links (`/wiki/TOKEN`) may point to different document types: Docs, Sheets, Base, etc. **Do not assume the token in the URL is the `file_token`** — you must query the actual type and real token first.

#### Handling Flow

1. **Query node info using `wiki.spaces.get_node`**
   ```javascript
   lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: 'wiki_token' } })
   ```

2. **Extract key info from the result**
   - `node.obj_type`: document type (docx/doc/sheet/bitable/slides/file/mindnote)
   - `node.obj_token`: **the real document token** (used for subsequent operations)
   - `node.title`: document title

3. **Use the corresponding API based on `obj_type`**

   | obj_type | Description | API to use |
   |----------|-------------|------------|
   | `docx` | New-version doc | `lark_api({ tool: 'drive', op: '...' })` or `docx.*` |
   | `doc` | Legacy doc | `lark_api({ tool: 'drive', op: '...' })` |
   | `sheet` | Spreadsheet | `lark_api({ tool: 'sheets', op: '...' })` |
   | `bitable` | Base | `lark_api({ tool: 'base', op: '...' })` |
   | `slides` | Slides | `lark_api({ tool: 'drive', op: '...' })` |
   | `file` | File | `lark_api({ tool: 'drive', op: '...' })` |
   | `mindnote` | Mind map | `lark_api({ tool: 'drive', op: '...' })` |

#### Query Example

```javascript
lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: 'wiki_token' } })
```

Sample response:
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

### Resource Relationships

```
Wiki Space
└── Wiki Node
    ├── obj_type: docx (new-version doc)
    │   └── obj_token (real document token)
    ├── obj_type: doc (legacy doc)
    │   └── obj_token (real document token)
    ├── obj_type: sheet (spreadsheet)
    │   └── obj_token (real document token)
    ├── obj_type: bitable (Base)
    │   └── obj_token (real document token)
    └── obj_type: file/slides/mindnote
        └── obj_token (real document token)

Drive Folder
└── File
    └── file_token (use directly)
```

**Filter operation flow (important):**

1. **create** — Create filter
   - Used for initial filter creation
   - ⚠️ range MUST cover all columns to be filtered (e.g. B1:E200)
   - If a filter already exists, calling create again overwrites the entire filter

2. **update** — Update filter
   - Used to add/update conditions on an existing filter for a specified column
   - Only specify col and condition; no range needed

3. **delete** — Delete filter

4. **get** — Get filter state

**Multi-column filter example:**

Create a dual filter on media name (column B) and sentiment analysis (column E):

```
// Use lark_api_search to discover exact parameter shapes for each step:

// Step 1 — delete existing filter
// lark_api_search("sheets spreadsheet.sheet.filters delete")
// Required: spreadsheet_token, sheet_id

// Step 2 — create filter covering all target columns
// lark_api_search("sheets spreadsheet.sheet.filters create")
// Required: spreadsheet_token, sheet_id, col ("B"), condition.expected, condition.filter_type ("multiValue"), range ("<sheet_id>!B1:E200")

// Step 3 — add second filter condition
// lark_api_search("sheets spreadsheet.sheet.filters update")
// Required: spreadsheet_token, sheet_id, col ("E"), condition.expected, condition.filter_type ("multiValue")
```

**Common errors:**
- `Wrong Filter Value`: filter already exists — delete then re-create
- `Excess Limit`: update added the same column condition again

### Cell Data Types

In shortcuts that accept a 2D array (`write`/`append` `values`, `create` `data`), each cell value supports the following types. **Formulas, text-linked URLs, @mentions, @doc references, and dropdown values MUST use the object format** — passing a plain string will store them as plain text.

| Type | Write format | Example |
|------|-------------|---------|
| String | `"text"` | `"hello"` |
| Number | `number` | `123`, `3.14` |
| Date | `number` (days since 1899-12-30; set cell date format first) | `42101` |
| Link (URL only) | `"URL string"` | `"https://example.com"` |
| Link (with text) | `{"type":"url","text":"display text","link":"URL"}` | `{"type":"url","text":"Lark","link":"https://www.feishu.cn"}` |
| Email | `"email string"` | `"user@example.com"` |
| **Formula** | `{"type":"formula","text":"=formula"}` | `{"type":"formula","text":"=SUM(A1:A10)"}` |
| @mention (person) | `{"type":"mention","text":"identifier","textType":"email\|openId\|unionId","notify":false}` | `{"type":"mention","text":"user@example.com","textType":"email","notify":false}` (notify optional, default false; set true only when user explicitly requests notification) |
| @mention (doc) | `{"type":"mention","textType":"fileToken","text":"token","objType":"type"}` | `{"type":"mention","textType":"fileToken","text":"shtXXX","objType":"sheet"}` |
| Dropdown | `{"type":"multipleValue","values":[val1,val2]}` | `{"type":"multipleValue","values":["Option A","Option B"]}` |

**Writing a formula — example:**

```javascript
// Correct: use object format
lark_api({ tool: 'sheets', op: 'write', args: {
  url: 'URL',
  sheet_id: 'sheetId',
  range: 'C6',
  values: [[{ type: 'formula', text: '=SUM(C2:C5)' }]]
}})

// Wrong: passing a string stores as plain text
// values: [['=SUM(C2:C5)']]
```

> **Formula syntax reference**: For ARRAYFORMULA, native array functions, MAP/LAMBDA, date diff, Excel formula rewrites, and other Lark-specific rules, read [`references/lark-sheets-formula.md`](references/lark-sheets-formula.md) first.

**Limitations:**
- Formulas support IMPORTRANGE cross-sheet references (max 5 levels of nesting, max 100 references per sheet)
- @mentions only support users in the same tenant; max 50 per call
- Dropdowns require **pre-configured dropdown options**; otherwise `multipleValue` writes are stored as plain text. See [`references/lark-sheets-dropdown.md#set-dropdown`](references/lark-sheets-dropdown.md#set-dropdown) for setup. Values must not contain commas.

## Operations (use via LarkSkill MCP)

Use `lark_api({ tool: 'sheets', op: '<op>', args: {...} })` for all operations. Always read the corresponding reference doc before executing.

### Spreadsheet Management

Reference doc: [spreadsheet-management](references/lark-sheets-spreadsheet-management.md)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'sheets', op: 'create', args: {...} })` | Create a spreadsheet (optional header row and initial data) |
| `lark_api({ tool: 'sheets', op: 'info', args: {...} })` | View spreadsheet and sheet information |
| `lark_api({ tool: 'sheets', op: 'export', args: {...} })` | Export a spreadsheet (async task polling + optional download) |

### Sheet Management

Reference doc: [sheet-management](references/lark-sheets-sheet-management.md)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'sheets', op: 'create-sheet', args: {...} })` | Create a sheet in an existing spreadsheet |
| `lark_api({ tool: 'sheets', op: 'copy-sheet', args: {...} })` | Copy a sheet within a spreadsheet |
| `lark_api({ tool: 'sheets', op: 'delete-sheet', args: {...} })` | Delete a sheet from a spreadsheet |
| `lark_api({ tool: 'sheets', op: 'update-sheet', args: {...} })` | Update sheet title, position, visibility, freeze, or protection |

### Cell Data

Reference doc: [cell-data](references/lark-sheets-cell-data.md)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'sheets', op: 'read', args: {...} })` | Read spreadsheet cell values |
| `lark_api({ tool: 'sheets', op: 'write', args: {...} })` | Write to spreadsheet cells (overwrite mode) |
| `lark_api({ tool: 'sheets', op: 'append', args: {...} })` | Append rows to a spreadsheet |
| `lark_api({ tool: 'sheets', op: 'find', args: {...} })` | Find cells in a spreadsheet |
| `lark_api({ tool: 'sheets', op: 'replace', args: {...} })` | Find and replace cell values |

### Cell Style and Merge

Reference doc: [cell-style-and-merge](references/lark-sheets-cell-style-and-merge.md)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'sheets', op: 'set-style', args: {...} })` | Set cell style for a range |
| `lark_api({ tool: 'sheets', op: 'batch-set-style', args: {...} })` | Batch set cell styles for multiple ranges |
| `lark_api({ tool: 'sheets', op: 'merge-cells', args: {...} })` | Merge cells in a spreadsheet |
| `lark_api({ tool: 'sheets', op: 'unmerge-cells', args: {...} })` | Unmerge (split) cells in a spreadsheet |

### Cell Images

Reference doc: [cell-images](references/lark-sheets-cell-images.md)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'sheets', op: 'write-image', args: {...} })` | Write an image into a spreadsheet cell |

### Row and Column Management

Reference doc: [row-column-management](references/lark-sheets-row-column-management.md)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'sheets', op: 'add-dimension', args: {...} })` | Add rows or columns at the end of a sheet |
| `lark_api({ tool: 'sheets', op: 'insert-dimension', args: {...} })` | Insert rows or columns at a specified position |
| `lark_api({ tool: 'sheets', op: 'update-dimension', args: {...} })` | Update row or column properties (visibility, size) |
| `lark_api({ tool: 'sheets', op: 'move-dimension', args: {...} })` | Move rows or columns to a new position |
| `lark_api({ tool: 'sheets', op: 'delete-dimension', args: {...} })` | Delete rows or columns |

### Filter Views

Reference doc: [filter-views](references/lark-sheets-filter-views.md)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'sheets', op: 'create-filter-view', args: {...} })` | Create a filter view |
| `lark_api({ tool: 'sheets', op: 'update-filter-view', args: {...} })` | Update a filter view |
| `lark_api({ tool: 'sheets', op: 'list-filter-views', args: {...} })` | List all filter views in a sheet |
| `lark_api({ tool: 'sheets', op: 'get-filter-view', args: {...} })` | Get a filter view by ID |
| `lark_api({ tool: 'sheets', op: 'delete-filter-view', args: {...} })` | Delete a filter view |
| `lark_api({ tool: 'sheets', op: 'list-filter-view-conditions', args: {...} })` | List all filter conditions of a filter view |
| `lark_api({ tool: 'sheets', op: 'get-filter-view-condition', args: {...} })` | Get a filter condition by column |

> **Note**: `create-filter-view-condition`, `update-filter-view-condition`, and `delete-filter-view-condition` are not available as MCP shortcut ops. Use the raw `spreadsheet.sheet.filters` API operations (create/update/delete) to manage filter conditions on sheets directly.

### Dropdown

Reference doc: [dropdown](references/lark-sheets-dropdown.md)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'sheets', op: 'set-dropdown', args: {...} })` | Set dropdown options (prerequisite step for `multipleValue` writes) |
| `lark_api({ tool: 'sheets', op: 'update-dropdown', args: {...} })` | Update dropdown options |
| `lark_api({ tool: 'sheets', op: 'get-dropdown', args: {...} })` | Query dropdown configuration |
| `lark_api({ tool: 'sheets', op: 'delete-dropdown', args: {...} })` | Delete dropdown |

### Float Images

Reference doc: [float-images](references/lark-sheets-float-images.md)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'sheets', op: 'media-upload', args: {...} })` | Upload a local image asset and return a `file_token` (for use with `create-float-image`; files >20 MB are auto-chunked) |
| `lark_api({ tool: 'sheets', op: 'create-float-image', args: {...} })` | Create a floating image |
| `lark_api({ tool: 'sheets', op: 'update-float-image', args: {...} })` | Update floating image properties |
| `lark_api({ tool: 'sheets', op: 'get-float-image', args: {...} })` | Get a floating image |
| `lark_api({ tool: 'sheets', op: 'list-float-images', args: {...} })` | List all floating images |
| `lark_api({ tool: 'sheets', op: 'delete-float-image', args: {...} })` | Delete a floating image |

### Formula

Reference doc: [formula](references/lark-sheets-formula.md)

> Float image read operations only return metadata (including `float_image_token`) — **they do not include image bytes**. To read image content, use `lark_api({ tool: 'docs', op: 'media-preview', args: { token: '<float_image_token>', output: './image.png' } })`.

## API Resources

> **Important**: When using raw API calls, always use `lark_api_search` to look up the parameter structure first. Do not guess field formats.

### spreadsheets

> Use `lark_api_search("sheets spreadsheets <method>")` to get the exact parameter shape before calling.

  - `create` — Create a spreadsheet
  - `get` — Get spreadsheet info
  - `patch` — Modify spreadsheet properties

### spreadsheet.sheet.filters

> Use `lark_api_search("sheets spreadsheet.sheet.filters <method>")` to get the exact parameter shape before calling.

  - `create` — Create a filter
  - `delete` — Delete a filter
  - `get` — Get a filter
  - `update` — Update a filter

### spreadsheet.sheets

> Use `lark_api_search("sheets spreadsheet.sheets find")` to get the exact parameter shape before calling.

  - `find` — Find cells

### spreadsheet.sheet.float_images

> Use `lark_api_search("sheets spreadsheet.sheet.float_images <method>")` to get the exact parameter shape before calling.

  - `create` — Create a floating image
  - `patch` — Update a floating image
  - `get` — Get a floating image
  - `query` — List all floating images
  - `delete` — Delete a floating image

## Permissions Table

| Method | Required scope |
|--------|---------------|
| `spreadsheets.create` | `sheets:spreadsheet:create` |
| `spreadsheets.get` | `sheets:spreadsheet.meta:read` |
| `spreadsheets.patch` | `sheets:spreadsheet.meta:write_only` |
| `spreadsheet.sheet.filters.create` | `sheets:spreadsheet:write_only` |
| `spreadsheet.sheet.filters.delete` | `sheets:spreadsheet:write_only` |
| `spreadsheet.sheet.filters.get` | `sheets:spreadsheet:read` |
| `spreadsheet.sheet.filters.update` | `sheets:spreadsheet:write_only` |
| `spreadsheet.sheets.find` | `sheets:spreadsheet:read` |
| `spreadsheet.sheet.float_images.create` | `sheets:spreadsheet:write_only` |
| `spreadsheet.sheet.float_images.patch` | `sheets:spreadsheet:write_only` |
| `spreadsheet.sheet.float_images.get` | `sheets:spreadsheet:read` |
| `spreadsheet.sheet.float_images.query` | `sheets:spreadsheet:read` |
| `spreadsheet.sheet.float_images.delete` | `sheets:spreadsheet:write_only` |
