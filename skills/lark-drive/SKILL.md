---
name: lark-drive
version: 2.0.0
description: "Use this skill when operating Lark Drive via LarkSkill MCP: upload/download files, create folders, copy/move/delete files, view file metadata, manage document comments, manage document permissions, modify file titles (docx, sheet, bitable, file, folder, wiki), subscribe to user comment-change events; also import local Word/Markdown/Excel/CSV as new Lark online cloud documents (docx, sheet, bitable). Use it for uploading or downloading files, organizing Drive directories, viewing file details, managing comments, managing permissions, modifying file titles, subscribing to events, and turning local files into new docs, sheets, or Base."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# drive

## Prerequisites

- LarkSkill MCP server connected (install via `/plugin marketplace add kescyz/larkskill` -> `/plugin install larkskill`, or see https://portal.larkskill.app/setup)
- MCP tools available: `lark_api`, `lark_api_search`
- Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first for auth, global flags, and safety rules

> **Import routing rule:** If the user wants to import a local Excel / CSV as Base / Bitable, the first step MUST be `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`. Do NOT switch to `lark-base` first; `lark-base` only handles in-table operations after the import completes.

## Quick decisions

- User wants to import a local `.xlsx` / `.csv` as Base / Bitable — first step MUST be `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`.
- User wants to import a local `.md` / `.docx` / `.doc` / `.txt` / `.html` as an online doc — use `lark_api({ tool: 'drive', op: 'import', args: { type: 'docx', ... } })`.
- User wants to import a local `.xlsx` / `.xls` / `.csv` as a sheet — use `lark_api({ tool: 'drive', op: 'import', args: { type: 'sheet', ... } })`.
- User wants to create a new folder in Drive — prefer `lark_api({ tool: 'drive', op: 'create-folder', args: { ... } })`.
- `lark-base` only handles in-Base operations after import (tables, fields, records, views); do NOT switch to `lark-base` early in the "local file -> Base" step.

## Modify title

- Use a native `lark_api` call to patch the file title; the `new_title` field modifies the title; supports `docx`, `sheet`, `bitable`, `file`, `wiki`, `folder` types.

   ```
   Call MCP tool `lark_api`:
   - method: PATCH
   - path: /open-apis/drive/v1/files/{file_token}
   - data: { "requests": [ { "title": "<new_title>" } ] }
   ```

   Use `lark_api_search` to inspect `drive.files.patch` schema first if unsure of the exact body shape.

## Core concepts

### Document types and tokens

In the Lark Open Platform, different document types have different URL formats and token handling. Before performing document operations (e.g. add comment, download file), you MUST first obtain the correct `file_token`.

### Document URL formats and token handling

| URL format | Example                                                 | Token type | Handling |
|------------|---------------------------------------------------------|------------|----------|
| `/docx/`   | `https://example.larksuite.com/docx/doxcnxxxxxxxxx`     | `file_token` | Use the token in the URL path directly as `file_token` |
| `/doc/`    | `https://example.larksuite.com/doc/doccnxxxxxxxxx`      | `file_token` | Use the token in the URL path directly as `file_token` |
| `/wiki/`   | `https://example.larksuite.com/wiki/wikcnxxxxxxxxx`     | `wiki_token` | WARNING: Cannot be used directly; you must first query to obtain the real `obj_token` |
| `/sheets/` | `https://example.larksuite.com/sheets/shtcnxxxxxxxxx`   | `file_token` | Use the token in the URL path directly as `file_token` |
| `/drive/folder/` | `https://example.larksuite.com/drive/folder/fldcnxxxx` | `folder_token` | Use the token in the URL path as the folder token |

### Wiki link special handling (critical!)

A wiki link (`/wiki/TOKEN`) may back onto different document types such as a doc, sheet, or Base. **Do NOT assume the URL token is the file_token**; you must first query the actual type and real token.

#### Processing flow

1. **Query the wiki node info via `lark_api`**

   ```
   Call MCP tool `lark_api`:
   - method: GET
   - path: /open-apis/wiki/v2/spaces/get_node
   - params: { "token": "<wiki_token>" }
   ```

2. **Extract key fields from the response**
   - `node.obj_type`: document type (`docx/doc/sheet/bitable/slides/file/mindnote`)
   - `node.obj_token`: **real document token** (used for follow-up operations)
   - `node.title`: document title

3. **Choose follow-up operation per `obj_type`**

   | obj_type | Description | Follow-up |
   |----------|-------------|-----------|
   | `docx` | New cloud doc | Native `lark_api` calls under `/open-apis/drive/v1/files/{file_token}/comments`, plus `docx.*` endpoints |
   | `doc` | Legacy cloud doc | Native `lark_api` calls under `/open-apis/drive/v1/files/{file_token}/comments` |
   | `sheet` | Sheet | `sheets.*` endpoints |
   | `bitable` | Base | `bitable.*` endpoints (use `lark-base` skill) |
   | `slides` | Slides | Native `lark_api` drive endpoints |
   | `file` | File | Native `lark_api` drive endpoints |
   | `mindnote` | Mind map | Native `lark_api` drive endpoints |

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
    ├── obj_type: sheet
    │   └── obj_token (real document token)
    ├── obj_type: bitable (Base)
    │   └── obj_token (real document token)
    └── obj_type: file/slides/mindnote
        └── obj_token (real document token)

Drive Folder
└── File / Document
    └── file_token (used directly)
```

### Token requirements for common operations

| Operation | Required token | Note |
|-----------|----------------|------|
| Read document content | `file_token` / handled automatically via `lark_api({ tool: 'docs', op: 'fetch' })` | The `docs` fetch op accepts a URL directly |
| Add a local (anchored) comment | `file_token` | When `selection_with_ellipsis` or `block_id` is passed, `lark_api({ tool: 'drive', op: 'add-comment' })` creates a local comment; only supported for `docx`, and wiki URLs that resolve to `docx` |
| Add a full-document comment | `file_token` | When neither `selection_with_ellipsis` nor `block_id` is passed, `lark_api({ tool: 'drive', op: 'add-comment' })` creates a full-document comment by default; supported for `docx`, legacy `doc` URLs, and wiki URLs that resolve to `doc`/`docx` |
| Download a file | `file_token` | Extract directly from the file URL |
| Upload a file | `folder_token` / `wiki_node_token` | Token of the destination location |
| List document comments | `file_token` | Same as add comment |

### Comment capability boundaries (critical!)

- `lark_api({ tool: 'drive', op: 'add-comment' })` supports two modes.
- Full-document comment: enabled by default when neither `selection_with_ellipsis` nor `block_id` is passed; you can also pass `full_comment: true` explicitly. Supports `docx`, legacy `doc` URLs, and wiki URLs that resolve to `doc`/`docx`.
- Local (anchored) comment: enabled when `selection_with_ellipsis` or `block_id` is passed; only supported for `docx`, and wiki URLs that resolve to `docx`.
- The `content` arg of `add-comment` requires a `reply_elements` JSON array, e.g. `content: '[{"type":"text","text":"body"}]'`.
- If a wiki URL does not resolve to `doc`/`docx`, do NOT use the `add-comment` op.
- If you need to call the lower-level Comment V2 protocol directly, use `lark_api_search` to inspect the `drive.file.comments.create_v2` schema, then call the native API:

   ```
   Call MCP tool `lark_api`:
   - method: POST
   - path: /open-apis/drive/v1/files/{file_token}/comments
   - data: { ... }   // omit `anchor` for full-document; pass `anchor.block_id` for local
   ```

### Comment query and counting semantics (critical!)

- To query document comments, call `lark_api`:

   ```
   Call MCP tool `lark_api`:
   - method: GET
   - path: /open-apis/drive/v1/files/{file_token}/comments
   - params: { ... pagination ... }
   ```

- The `items` returned should be understood as a list of "comment cards" — each `item` corresponds to one comment card visible in the user interface, NOT a flat list of interaction messages.
- Server-side semantics: when the first comment is created, the first reply inside that card is also created at the same time; therefore the body of a comment is actually carried by `item.reply_list.replies`, where the first reply in user-visible terms is "the comment itself" inside that card.
- When the user wants to count "number of comments" or "number of comment cards", count the length of `items`. For full counts, sum the `items` lengths across all paginated returns.
- When the user wants to count "number of replies", from the user perspective you should exclude the first comment in each card; the count is the sum of all `item.reply_list.replies` lengths minus the length of `items`.
- When the user wants to count "total interactions", count the sum of all `item.reply_list.replies` lengths; this includes the first comment in each card.
- If any `item.has_more=true`, there are more replies under that comment card not included in the current return; you must keep listing replies via `lark_api` against `/open-apis/drive/v1/files/{file_token}/comments/{comment_id}/replies` to fetch them all before computing full reply count / total interaction count.

### Comment business behavior and guidance (critical!)

#### Comment ordering guidance
- A document usually has multiple comments, sorted by `create_time`.
- **Important**: only sort by `create_time` when the user explicitly mentions "latest comment", "last comment", or "earliest comment":
  - **You MUST first fetch ALL comments (paginate through everything)**; do NOT sort after fetching only one page.
  - "Latest" / "Last comment": sort by `create_time` descending and take the first.
  - "Earliest comment": sort by `create_time` ascending and take the first.
- If the user just says "first comment", use the first item returned by listing `/open-apis/drive/v1/files/{file_token}/comments` directly without extra sorting.

#### Comment reply restrictions
- **Before adding a reply, check whether any of the following restrictions apply.**
- **Full-document comments do NOT support replies**: comments with `is_whole=true` (full-document comments) cannot accept replies; in this case, prompt the user "Full-document comments do not support replies".
- **Resolved comments do NOT support replies**: comments with `is_solved=true` cannot accept replies; in this case, prompt the user "This comment has been resolved and cannot be replied to".
- **Note**: when the user wants to reply to a comment that cannot be replied to due to the restrictions above, just prompt that it cannot be replied to. **Do NOT automatically find another comment that can be replied to** — that would be off-expectation.

#### Choosing between batch query and list
- The native batch-query endpoint over `drive.file.comments.batch_query` is for **batch query when you already know comment IDs**; you must pass a concrete comment ID list. Invoke it via `lark_api` against the native API path (use `lark_api_search` to inspect schema first).
- Listing via `GET /open-apis/drive/v1/files/{file_token}/comments` is for paginated retrieval of the comment list; suitable for counting total comments, walking all comments, or fetching the "latest / last N" comments.

#### Reaction / emoji scenarios
- For questions related to reactions on comments / replies (emojis, per-emoji counts, who reacted with what, add/remove reaction), **first read [lark-drive-reactions.md](references/lark-drive-reactions.md) to learn how to use them.** Reaction updates go through the native `drive.file.comment.reply.reactions.update_reaction` API path; call via `lark_api` after inspecting the schema with `lark_api_search`.

### Common errors and resolutions

| Error message | Cause | Resolution |
|---------------|-------|------------|
| `not exist` | Wrong token used | Check token type. For wiki links, you must first query and obtain `obj_token` |
| `permission denied` | Lacks the required permission | Guide the user to verify the current identity has the required permission on the document/file; grant permission if needed |
| `invalid file_type` | `file_type` parameter wrong | Pass the correct `file_type` per `obj_type` (`docx/doc/sheet`) |

### Authorize the current app to access a document

When you need to grant permission on a document to the **current app (bot) itself**, first fetch the app's open_id via the bot info endpoint, then call the permission endpoint:

```
1. Get the current app's open_id
   Call MCP tool `lark_api`:
   - method: GET
   - path: /open-apis/bot/v3/info
   - as: bot
   Take bot.open_id from the response.

2. Grant the current app access to the document
   Call MCP tool `lark_api`:
   - method: POST
   - path: /open-apis/drive/v1/permissions/{doc_token}/members
   - params: { "type": "<resource_type>" }
   - data: { "member_type": "openid", "member_id": "<bot_open_id>", "perm": "view", "type": "user" }
```

> **Note**: this approach only applies when authorizing the **current app**. To authorize another user, just use that user's open_id directly; no need to call the bot info endpoint.

`<resource_type>` can be: `doc`, `docx`, `sheet`, `bitable`, `file`, `folder`, `wiki`.

## Shortcuts (prefer these)

A Shortcut is a high-level wrapper for common operations. Prefer Shortcuts when one exists. Invoke as `lark_api({ tool: 'drive', op: '<verb>', args: { ... } })`.

| Shortcut op | Description |
|-------------|-------------|
| [`upload`](references/lark-drive-upload.md) | Upload a local file to Drive |
| [`create-folder`](references/lark-drive-create-folder.md) | Create a Drive folder, optionally under a parent folder, with bot auto-grant support |
| [`download`](references/lark-drive-download.md) | Download a file from Drive to local |
| [`create-shortcut`](references/lark-drive-create-shortcut.md) | Create a shortcut to an existing Drive file in another folder |
| [`add-comment`](references/lark-drive-add-comment.md) | Add a full-document comment, or a local comment to selected docx text (also supports wiki URL resolving to doc/docx) |
| [`export`](references/lark-drive-export.md) | Export a doc/docx/sheet/bitable to a local file with limited polling |
| [`export-download`](references/lark-drive-export-download.md) | Download an exported file by file_token |
| [`import`](references/lark-drive-import.md) | Import a local file to Drive as a cloud document (docx, sheet, bitable) |
| [`move`](references/lark-drive-move.md) | Move a file or folder to another location in Drive |
| [`delete`](references/lark-drive-delete.md) | Delete a Drive file or folder with limited polling for folder deletes |
| [`task_result`](references/lark-drive-task-result.md) | Poll async task result for import, export, move, or delete operations |

## API Resources

```
For non-Shortcut endpoints (resource.method form), inspect the schema first via `lark_api_search`,
then invoke the API via `lark_api` with method + native /open-apis/drive/v1/... path.

Only the Shortcut ops listed above (upload, download, create-folder, create-shortcut, add-comment,
export, export-download, import, move, delete, task_result) take the high-level
`lark_api({ tool: 'drive', op: '<verb>', args: { ... } })` shape.
```

> **Important**: when using a native API, you MUST first run a schema lookup via `lark_api_search` to inspect the `data` / `params` parameter shape; do NOT guess field formats.

### files

  - `copy` — Copy file
  - `create_folder` — Create folder
  - `list` — List files in a folder
  - `patch` — Modify file title

### file.comments

  - `batch_query` — Batch fetch comments
  - `create_v2` — Add full-document / local (anchored) comment
  - `list` — Paginated fetch of document comments
  - `patch` — Resolve / restore a comment

### file.comment.replys

  - `create` — Add reply
  - `delete` — Delete reply
  - `list` — Fetch replies
  - `update` — Update reply

### permission.members

  - `auth` —
  - `create` — Grant collaborator permission
  - `transfer_owner` —

### metas

  - `batch_query` — Fetch document metadata

### user

  - `remove_subscription` — Cancel user/app-level event subscription
  - `subscription` — Subscribe to user/app-level events (this round opens up comment-add events)
  - `subscription_status` — Query subscription status of a user/app for a given event

### file.statistics

  - `get` — Fetch file statistics

### file.view_records

  - `list` — Fetch document viewer records

### file.comment.reply.reactions

  - `update_reaction` — Add / remove reaction

## Permission table

| Method | Required scope |
|--------|----------------|
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
| `metas.batch_query` | `drive:drive.metadata:readonly` |
| `user.remove_subscription` | `docs:event:subscribe` |
| `user.subscription` | `docs:event:subscribe` |
| `user.subscription_status` | `docs:event:subscribe` |
| `file.statistics.get` | `drive:drive.metadata:readonly` |
| `file.view_records.list` | `drive:file:view_record:readonly` |
| `file.comment.reply.reactions.update_reaction` | `docs:document.comment:create` |
