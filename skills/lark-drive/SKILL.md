---
name: lark-drive
version: 2.0.0
description: "Use this skill when operating Lark Drive via LarkSkill MCP: manage files and folders, upload/download, create folders, copy/move/delete files, manage comments and permissions, and import local files as online documents (docx, sheet, bitable)."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# drive

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first.
> **Mandatory before execution:** Before invoking any `drive` operation, read the corresponding command reference doc, then call the operation via `lark_api`.
> **Naming convention:** Drive operations call `lark_api({ tool: 'drive', op: '<op>', args: {...} })`; if a Wiki link must be resolved first, call `lark_api` with the HTTP form `{ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_token>' } }` first.
> **Import routing rule:** If the user wants to import a local Excel / CSV / `.base` snapshot as Base / Bitable, the first step is `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`. Do not switch to `lark-base` early; `lark-base` only handles in-table operations after import is complete.

## Quick Decision

- To **search for docs / Wikis / spreadsheets / Base / Drive objects**, use `lark_api({ tool: 'drive', op: 'search', args: {...} })`. Natural language phrases like "recently edited by me", "created by me", "opened in the past week", "docx files created by someone" map directly to flat args. The older `docs search` is in maintenance mode; do not add new dependencies on it.
- To import a local `.xlsx` / `.csv` / `.base` as Base / Bitable, the first step MUST be `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`.
- To import a local `.md` / `.docx` / `.doc` / `.txt` / `.html` as an online doc, use `lark_api({ tool: 'drive', op: 'import', args: { type: 'docx', ... } })`.
- To upload, create, read, partially patch, or overwrite-update a **native `.md` file** in Drive (not import as docx), switch to [`lark-markdown`](../lark-markdown/SKILL.md).
- To view, download, roll back, or delete **historical versions** of a file, use `lark_api({ tool: 'drive', op: 'version-history', args: {...} })`, `lark_api({ tool: 'drive', op: 'version-get', args: {...} })`, `lark_api({ tool: 'drive', op: 'version-revert', args: {...} })`, or `lark_api({ tool: 'drive', op: 'version-delete', args: {...} })`.
- To import a local `.xlsx` / `.xls` / `.csv` as a spreadsheet, use `lark_api({ tool: 'drive', op: 'import', args: { type: 'sheet', ... } })`.
- To create a folder in Drive, use `lark_api({ tool: 'drive', op: 'create-folder', args: {...} })`.
- To upload a local file to a wiki node or document library, use `lark_api({ tool: 'drive', op: 'upload', args: { wiki_token: '<wiki_token>', ... } })`; do not switch to `wiki` domain commands.
- `lark-base` only handles Base internal operations (tables, fields, records, views) after import is complete.

## Rename

Use the Drive `files patch` operation with `new_title` in args (use `lark_api_search("drive files patch")` for exact shape). Supports docx, sheet, bitable, file, wiki, and folder types.

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

Wiki links (`/wiki/TOKEN`) may point to different document types. **Do not assume the token in the URL is the `file_token`** — query the actual type and real token first.

#### Handling Flow

**Recommended: use `drive inspect` to auto-unwrap**

```javascript
lark_api({ tool: 'drive', op: 'inspect', args: { url: 'https://xxx.feishu.cn/wiki/wikcnXXX' } })
```

Returns `type` (underlying document type), `token` (real file_token), `title`, `url` for direct use.

**Manual approach:**

```javascript
lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: 'wiki_token' } })
```

Extract `node.obj_type` and `node.obj_token` from result, then use the corresponding API.

| obj_type | Description | API to use |
|----------|-------------|------------|
| `docx` | New-version doc | `lark_api({ tool: 'drive', op: '...' })` |
| `doc` | Legacy doc | `lark_api({ tool: 'drive', op: '...' })` |
| `sheet` | Spreadsheet | `lark_api({ tool: 'sheets', op: '...' })` |
| `bitable` | Base | `lark_api({ tool: 'base', op: '...' })` |
| `slides` | Slides | `lark_api({ tool: 'drive', op: '...' })` |
| `file` | File | `lark_api({ tool: 'drive', op: '...' })` |
| `mindnote` | Mind map | `lark_api({ tool: 'drive', op: '...' })` |

### Resource Relationships

```
Wiki Space
└── Wiki Node
    ├── obj_type: docx / doc / sheet / bitable / slides / file / mindnote
    │   └── obj_token (real document token)

Drive Folder
└── File
    └── file_token (use directly)
```

### Common Operation Token Requirements

| Operation | Required Token | Notes |
|-----------|---------------|-------|
| Read document content | `file_token` / auto-handled via `docs fetch` | `lark_api({ tool: 'docs', op: 'fetch', args: { api_version: 'v2', ... } })` accepts a URL directly |
| Add inline comment (selection comment) | `file_token` | Passing `block_id` to `drive add-comment` creates an inline comment |
| Add full-document comment | `file_token` | Without `block_id`, `drive add-comment` creates a full-document comment by default |
| Download file | `file_token` | Extracted directly from the file URL |
| Upload file | `folder_token` / `wiki_node_token` | Token for the target location |
| List document comments | `file_token` | Same as adding comments |

### Comment Capability Boundaries (Critical!)

- `lark_api({ tool: 'drive', op: 'add-comment', args: {...} })` supports two modes.
- Full-document comment: enabled by default when `block_id` is not passed; can also be explicit with `full_comment: true`; supports `docx`, legacy `doc` URLs, and wiki URLs that resolve to `doc`/`docx`.
- Inline comment: enabled when `block_id` is passed; only supports `docx` and wiki URLs that resolve to `docx`. Block IDs can be obtained via `lark_api({ tool: 'docs', op: 'fetch', args: { api_version: 'v2', detail: 'with-ids', ... } })`.
- The `content` for `drive add-comment` requires a `reply_elements` JSON array, e.g. `[{"type":"text","text":"body text"}]`.
- `slides` comments require explicit `block_id` in `<slide-block-type>!<xml-id>` format; `selection_with_ellipsis` and `full_comment` are not supported.
- Comment content MUST NOT contain raw `<` or `>`; escape before submitting: `<` → `&lt;`, `>` → `&gt;`.
- Using `lark_api({ tool: 'drive', op: 'add-comment', args: {...} })` auto-escapes `type=text` elements; if calling raw `drive file.comments create_v2`, `drive file.comment.replys create`, or `drive file.comment.replys update`, the payload must already contain escaped content.
- If the wiki resolves to a type other than `doc`/`docx`/`sheet`/`slides`, do not use `add-comment`.

### Comment Query and Count Conventions (Critical!)

**Mandatory rule**: `drive file.comments list` MUST default to `is_solved: false` — query only unsolved comments. Even when the user says "all comments", unless they explicitly ask to include resolved comments, always default to unsolved only.

```javascript
// Default query: unsolved comments only (recommended)
lark_api({ tool: 'drive', op: 'file.comments', args: {
  method: 'list',
  file_token: 'xxx',
  file_type: 'docx',
  is_solved: false
}})

// Include resolved comments (requires explicit user request)
lark_api({ tool: 'drive', op: 'file.comments', args: {
  method: 'list',
  file_token: 'xxx',
  file_type: 'docx'
}})
```

- `drive file.comments list` returns `items` as "comment cards" — each `item` is one card, not a flat interaction list.
- Body content lives in `item.reply_list.replies`; the first reply is the "comment itself" from the user's perspective.
- "Comment count" = length of `items` (all pages accumulated).
- "Reply count" = sum of all `item.reply_list.replies` lengths minus number of `items`.
- "Total interactions" = sum of all `item.reply_list.replies` lengths.
- If `item.has_more=true`, call `drive file.comment.replys list` to retrieve remaining replies before computing totals.

### Comment Business Rules and Routing (Critical!)

#### Comment Sort Routing
- Only sort by `create_time` when the user explicitly mentions "latest", "last", or "earliest" comment.
- MUST retrieve all comments first (paginate fully) before sorting.
- If the user says "the first comment", use the first item returned without additional sorting.

#### Comment Reply Restrictions
- **Full-document comments (`is_whole=true`) do not support replies** — inform the user.
- **Resolved comments (`is_solved=true`) do not support replies** — inform the user.
- When a comment cannot be replied to, only inform the user — **do not automatically find another comment**.

#### Choosing Between Batch Query and List Query
- `drive file.comments batch_query`: for known comment IDs requiring batch retrieval.
- `drive file.comments list`: for paginated listing, counting, or "latest N comments" scenarios.

#### Reaction Scenarios
- For questions about reactions on comments/replies, **read [lark-drive-reactions.md](../../skills/lark-drive/references/lark-drive-reactions.md) first**.

### Common Errors and Solutions

| Error message | Cause | Solution |
|---------------|-------|----------|
| `not exist` | Wrong token used | Check token type; wiki links must query first to get `obj_token` |
| `permission denied` | Insufficient permission | Guide user to check permissions; grant access if needed |
| `invalid file_type` | Incorrect file_type parameter | Pass correct file_type based on `obj_type` (docx/doc/sheet/slides) |

#### `permission.public.patch` Error Code Guidance

| Error code | Meaning | User guidance |
|------------|---------|---------------|
| `91009` | External sharing blocked by tenant policy | Contact tenant admin to adjust org-level external sharing policy |
| `91010` | Document external sharing not enabled | Enable external sharing in document permission settings first |
| `91011` | External sharing blocked by document classification | Open the document and initiate classification exemption or downgrade; return the document URL |
| `91012` | Permission settings blocked by document classification | Open the document and initiate classification exemption or downgrade; return the document URL |

### Grant Current App Access to Document

```javascript
// 1. Get the current app's open_id
lark_api({ method: 'GET', path: '/open-apis/bot/v3/info' })
// Extract bot.open_id from the result

// 2. Grant the current app access to the document
lark_api({ tool: 'drive', op: 'permission.members', args: {
  method: 'create',
  token: '<doc_token>',
  type: '<resource_type>',
  member_type: 'openid',
  member_id: '<bot_open_id>',
  perm: 'view'
}})
```

`<resource_type>` options: `doc`, `docx`, `sheet`, `bitable`, `file`, `folder`, `wiki`, `slides`.

## Operations (use via LarkSkill MCP)

Use `lark_api({ tool: 'drive', op: '<op>', args: {...} })` for all shortcut operations.

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'drive', op: 'search', args: {...} })` | Search Lark docs, Wiki, and spreadsheet files with flat filter args (`edited_since`, `mine`, `doc_types`, etc.) — preferred over `docs search` |
| `lark_api({ tool: 'drive', op: 'upload', args: {...} })` | Upload a local file to a Drive folder or wiki node |
| `lark_api({ tool: 'drive', op: 'create-folder', args: {...} })` | Create a Drive folder, optionally under a parent folder |
| `lark_api({ tool: 'drive', op: 'download', args: {...} })` | Download a file from Drive to local |
| `lark_api({ tool: 'drive', op: 'status', args: {...} })` | Compare a local directory with a Drive folder (SHA-256 exact or `--quick` modified-time diff); reports `new_local` / `new_remote` / `modified` / `unchanged`. `local_dir` must stay inside cwd. |
| `lark_api({ tool: 'drive', op: 'pull', args: {...} })` | File-level Drive → local mirror. `if_exists` supports `overwrite` / `smart` / `skip`. `delete_local` requires `yes: true`. `local_dir` must stay inside cwd. |
| `lark_api({ tool: 'drive', op: 'sync', args: {...} })` | Two-way local ↔ Drive sync. Resolves conflicts via `on_conflict`. Non-destructive — no delete on either side by default. |
| `lark_api({ tool: 'drive', op: 'create-shortcut', args: {...} })` | Create a shortcut to an existing Drive file in another folder |
| `lark_api({ tool: 'drive', op: 'add-comment', args: {...} })` | Add a comment to doc/docx/sheet/slides; also supports wiki URL resolving |
| `lark_api({ tool: 'drive', op: 'export', args: {...} })` | Export a doc/docx/sheet/bitable to a local file |
| `lark_api({ tool: 'drive', op: 'export-download', args: {...} })` | Download an exported file by file_token |
| `lark_api({ tool: 'drive', op: 'import', args: {...} })` | Import a local file to Drive as a cloud document (docx, sheet, bitable) |
| `lark_api({ tool: 'drive', op: 'version-history', args: {...} })` | List historical versions of a file |
| `lark_api({ tool: 'drive', op: 'version-get', args: {...} })` | Download a specific historical version |
| `lark_api({ tool: 'drive', op: 'version-revert', args: {...} })` | Revert a file to a specific historical version |
| `lark_api({ tool: 'drive', op: 'version-delete', args: {...} })` | Delete a specific historical version |
| `lark_api({ tool: 'drive', op: 'move', args: {...} })` | Move a file or folder to another location in Drive |
| `lark_api({ tool: 'drive', op: 'delete', args: {...} })` | Delete a Drive file or folder |
| `lark_api({ tool: 'drive', op: 'push', args: {...} })` | File-level local → Drive mirror. `if_exists` supports `skip` / `smart` / `overwrite`. `delete_remote` requires `yes: true`. |
| `lark_api({ tool: 'drive', op: 'task_result', args: {...} })` | Poll async task result for import, export, move, or delete operations |
| `lark_api({ tool: 'drive', op: 'inspect', args: {...} })` | Inspect a Lark document URL; auto-unwraps wiki URLs |
| `lark_api({ tool: 'drive', op: 'apply-permission', args: {...} })` | Apply to the document owner for view/edit access (user-only; 5/day per document) |

## API Resources

> **Important**: Use `lark_api_search` to look up parameter structure before using raw API calls.

### files

> Use `lark_api_search("drive files <method>")` to get the exact parameter shape before calling.

  - `copy` — Copy a file
  - `create_folder` — Create a folder
  - `list` — List contents of a folder
  - `patch` — Rename a file (pass `new_title` in args)

### file.comments

```javascript
lark_api({ tool: 'drive', op: 'file.comments', args: { method: 'batch_query', file_token: '...', ... } })
lark_api({ tool: 'drive', op: 'file.comments', args: { method: 'create_v2', file_token: '...', ... } })
lark_api({ tool: 'drive', op: 'file.comments', args: { method: 'list', file_token: '...', is_solved: false, ... } })
lark_api({ tool: 'drive', op: 'file.comments', args: { method: 'patch', ... } })
```

  - `batch_query` — Batch fetch comments
  - `create_v2` — Add full-document / inline comment
  - `list` — Paginated retrieval of document comments
  - `patch` — Resolve / restore a comment

### file.comment.replys

```javascript
lark_api({ tool: 'drive', op: 'file.comment.replys', args: { method: 'create', ... } })
lark_api({ tool: 'drive', op: 'file.comment.replys', args: { method: 'delete', ... } })
lark_api({ tool: 'drive', op: 'file.comment.replys', args: { method: 'list', ... } })
lark_api({ tool: 'drive', op: 'file.comment.replys', args: { method: 'update', ... } })
```

### permission.members

```javascript
lark_api({ tool: 'drive', op: 'permission.members', args: { method: 'create', token: '...', type: '...', ... } })
```

### metas

> Use `lark_api_search("drive metas batch_query")` to get the exact parameter shape before calling.

### user

> Use `lark_api_search("drive user <method>")` to get the exact parameter shape before calling.

  - `subscription` — Subscribe to user/app dimension events
  - `subscription_status` — Query subscription status
  - `remove_subscription` — Unsubscribe from events

### file.statistics

```javascript
lark_api({ tool: 'drive', op: 'file.statistics', args: { method: 'get', file_token: '...', ... } })
```

### file.view_records

```javascript
lark_api({ tool: 'drive', op: 'file.view_records', args: { method: 'list', file_token: '...', ... } })
```

### file.comment.reply.reactions

```javascript
lark_api({ tool: 'drive', op: 'file.comment.reply.reactions', args: { method: 'update_reaction', ... } })
```

## Permissions Table

| Method | Required scope |
|--------|---------------|
| `files.copy` | `docs:document:copy` |
| `files.create_folder` | `space:folder:create` |
| `files.list` | `space:document:retrieve` |
| `files.patch` | `docx:document:write_only` |
| `file.comments.batch_query` | `docs:document.comment:read` |
| `file.comments.create_v2` | `docs:document.comment:create` |
| `file.comments.list` | `docs:document.comment:read` |
| `file.comments.patch` | `docs:document.comment:update` |
| `file.comment.replys.create` | `docs:document.comment:create` |
| `file.comment.replys.delete` | `docs:document.comment:delete` |
| `file.comment.replys.list` | `docs:document.comment:read` |
| `file.comment.replys.update` | `docs:document.comment:update` |
| `permission.members.auth` | `docs:permission.member:auth` |
| `permission.members.create` | `docs:permission.member:create` |
| `permission.members.transfer_owner` | `docs:permission.member:transfer` |
| `permission.public.get` | `docs:permission.setting:read` |
| `permission.public.patch` | `docs:permission.setting:write_only` |
| `metas.batch_query` | `drive:drive.metadata:readonly` |
| `user.remove_subscription` | `docs:event:subscribe` |
| `user.subscription` | `docs:event:subscribe` |
| `user.subscription_status` | `docs:event:subscribe` |
| `file.statistics.get` | `drive:drive.metadata:readonly` |
| `file.view_records.list` | `drive:file:view_record:readonly` |
| `file.comment.reply.reactions.update_reaction` | `docs:document.comment:create` |
