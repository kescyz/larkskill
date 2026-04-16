---
name: lark-drive
version: 2.0.0
description: "Lark Drive: Manage files and folders in Drive. Upload and download files, create folders, copy/move/delete files, view file metadata, manage document comments, manage document permissions, subscribe to user comment change events. Use when users need to upload or download files, organize Drive directories, view file details, manage comments, manage document permissions, or subscribe to user comment change events."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# drive

> **Prerequisite:** Read [../lark-shared/SKILL.md](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## Core Concepts

### Document Types and Tokens

In the Lark Open Platform, different document types have different URL formats and token handling methods. When performing document operations (such as adding comments, downloading files, etc.), you must first obtain the correct `file_token`.

### Document URL Formats and Token Handling

| URL Format | Example | Token Type | Handling |
|------------|---------|------------|----------|
| `/docx/` | `https://example.larksuite.com/docx/doxcnxxxxxxxxx` | `file_token` | Token in URL path can be used directly as `file_token` |
| `/doc/` | `https://example.larksuite.com/doc/doccnxxxxxxxxx` | `file_token` | Token in URL path can be used directly as `file_token` |
| `/wiki/` | `https://example.larksuite.com/wiki/wikcnxxxxxxxxx` | `wiki_token` | **Cannot be used directly** - must query to get the real `obj_token` first |
| `/sheets/` | `https://example.larksuite.com/sheets/shtcnxxxxxxxxx` | `file_token` | Token in URL path can be used directly as `file_token` |
| `/drive/folder/` | `https://example.larksuite.com/drive/folder/fldcnxxxx` | `folder_token` | Token in URL path is used as folder token |

### Wiki Link Special Handling (Critical!)

Wiki links (`/wiki/TOKEN`) may point to different document types behind the scenes - cloud docs, spreadsheets, multidimensional tables, etc. **You cannot assume the token in the URL is the file_token** - you must query the actual type and real token first.

#### Handling Flow

1. **Call `lark_api` to query node info**

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces/get_node
- params: { "token": "<wiki_token>" }
```

2. **Extract key info from the response**
   - `node.obj_type`: document type (docx/doc/sheet/bitable/slides/file/mindnote)
   - `node.obj_token`: **real document token** (used for subsequent operations)
   - `node.title`: document title

3. **Use the corresponding API based on `obj_type`**

   | obj_type | Description | API to Use |
   |----------|-------------|-----------|
   | `docx` | New version cloud doc | `drive file.comments.*`, `docx.*` |
   | `doc` | Old version cloud doc | `drive file.comments.*` |
   | `sheet` | Spreadsheet | `sheets.*` |
   | `bitable` | Base (multidimensional table) | `bitable.*` |
   | `slides` | Slides | `drive.*` |
   | `file` | File | `drive.*` |
   | `mindnote` | Mind map | `drive.*` |

#### Query Example

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces/get_node
- params: { "token": "wiki_token" }
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

### Resource Relationships

```
Wiki Space
└── Wiki Node (knowledge base node)
    ├── obj_type: docx (new version document)
    │   └── obj_token (real document token)
    ├── obj_type: doc (old version document)
    │   └── obj_token (real document token)
    ├── obj_type: sheet (spreadsheet)
    │   └── obj_token (real document token)
    ├── obj_type: bitable (Base / multidimensional table)
    │   └── obj_token (real document token)
    └── obj_type: file/slides/mindnote
        └── obj_token (real document token)

Drive Folder
└── File (file/document)
    └── file_token (use directly)
```

### Common Operation Token Requirements

| Operation | Required Token | Notes |
|-----------|---------------|-------|
| Read document content | `file_token` / auto-handled via `docs +fetch` | `docs +fetch` supports passing URL directly |
| Add inline comment (text selection comment) | `file_token` | When `selection_with_ellipsis` or `block_id` is passed, creates an inline comment; only supports `docx`, and wiki URLs that resolve to `docx` |
| Add full-document comment | `file_token` | When no position params are provided, creates a full-document comment by default; supports `docx`, old `doc` URLs, and wiki URLs that resolve to `doc`/`docx` |
| Download file | `file_token` | Extract directly from the file URL |
| Upload file | `folder_token` / `wiki_node_token` | Token of the target location |
| List document comments | `file_token` | Same as adding comments |

### Comment Capability Boundaries (Critical!)

- Full-document comment: enabled by default when no position params are passed; supports `docx`, old `doc` URLs, and wiki URLs that resolve to `doc`/`docx`.
- Inline comment: enabled when `selection_with_ellipsis` or `block_id` is provided; only supports `docx`, and wiki URLs that resolve to `docx`.
- The `reply_elements` JSON array is required for comment content, e.g. `[{"type":"text","text":"body text"}]`.
- If wiki resolution does not yield `doc`/`docx`, do not use comment creation.

### Comment Query and Counting Logic (Critical!)

- To query document comments, use `GET /open-apis/drive/v1/files/{file_token}/comments`.
- The `items` returned should be understood as a list of "comment cards" - each `item` corresponds to a comment card seen in the UI.
- On the server side, the actual content is in each `item.reply_list.replies`, where the first reply is the "comment itself" within the card.
- When users want to count "number of comments" or "comment cards", count the length of `items`.
- When users want to count "replies", exclude the first comment in each card.
- When users want to count "total interactions", count the sum of all `item.reply_list.replies` lengths.
- If an `item.has_more=true`, it means that comment card has more replies not included; continue calling replies list to fetch all.

### Comment Business Features and Guidance (Critical!)

#### Comment Sorting Guidance
- **Important**: Only when the user explicitly mentions "latest comment", "last comment", or "earliest comment" do you need to sort by `create_time`:
  - **Must first fetch all comments (handle pagination)**
  - "Latest comment" / "last comment": sort by `create_time` descending, take the first
  - "Earliest comment": sort by `create_time` ascending, take the first
- If user simply says "first comment", use the first item returned directly.

#### Comment Reply Restrictions
- **Full-document comments do not support replies**: comments with `is_whole=true` cannot have replies added.
- **Resolved comments do not support replies**: comments with `is_solved=true` cannot have replies added.
- **Note**: When a user wants to reply but it cannot be replied to, inform them — **do not automatically find another comment**.

#### Choosing Between Batch Query and List Query
- Use batch query `POST /open-apis/drive/v1/files/{file_token}/comments/batch_query` when you already have comment IDs.
- Use list `GET /open-apis/drive/v1/files/{file_token}/comments` for paginated retrieval of comment lists.

### Common Errors and Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `not exist` | Wrong token used | Check token type - wiki links must first query to get `obj_token` |
| `permission denied` | No permission for the operation | Guide user to check if current identity has the required permission; grant permission if needed |
| `invalid file_type` | Wrong file_type parameter | Pass the correct file_type based on `obj_type` (docx/doc/sheet) |

## Shortcuts (read reference first)

Read the reference doc before using any shortcut.

| Shortcut | Description |
|----------|-------------|
| [`+upload`](references/lark-drive-upload.md) | Upload a local file to Drive |
| [`+download`](references/lark-drive-download.md) | Download a file from Drive to local |
| [`+add-comment`](references/lark-drive-add-comment.md) | Add a full-document comment, or an inline comment to selected docx text |
| [`+export`](references/lark-drive-export.md) | Export a doc/docx/sheet/bitable to a local file |
| [`+export-download`](references/lark-drive-export-download.md) | Download an exported file by file_token |
| [`+import`](references/lark-drive-import.md) | Import a local file to Drive as a cloud document |
| [`+move`](references/lark-drive-move.md) | Move a file or folder to another location in Drive |
| [`+task_result`](references/lark-drive-task-result.md) | Poll async task result for import, export, move, or delete operations |

## API Resources

All drive APIs use the base path `/open-apis/drive/v1/`.

### files

- `copy` — `POST /open-apis/drive/v1/files/{file_token}/copy`
- `create_folder` — `POST /open-apis/drive/v1/files/create_folder`
- `list` — `GET /open-apis/drive/v1/files`

### file.comments

- `batch_query` — `POST /open-apis/drive/v1/files/{file_token}/comments/batch_query`
- `create_v2` — `POST /open-apis/drive/v1/files/{file_token}/comments`
- `list` — `GET /open-apis/drive/v1/files/{file_token}/comments`
- `patch` — `PATCH /open-apis/drive/v1/files/{file_token}/comments/{comment_id}`

### file.comment.replys

- `create` — `POST /open-apis/drive/v1/files/{file_token}/comments/{comment_id}/replies`
- `delete` — `DELETE /open-apis/drive/v1/files/{file_token}/comments/{comment_id}/replies/{reply_id}`
- `list` — `GET /open-apis/drive/v1/files/{file_token}/comments/{comment_id}/replies`
- `update` — `PUT /open-apis/drive/v1/files/{file_token}/comments/{comment_id}/replies/{reply_id}`

### permission.members

- `auth` — `POST /open-apis/drive/v1/permissions/{token}/members/auth`
- `create` — `POST /open-apis/drive/v1/permissions/{token}/members`
- `transfer_owner` — `POST /open-apis/drive/v1/permissions/{token}/members/transfer_owner`

### metas

- `batch_query` — `POST /open-apis/drive/v1/metas/batch_query`

### file.statistics

- `get` — `GET /open-apis/drive/v1/files/{file_token}/statistics`

### file.view_records

- `list` — `GET /open-apis/drive/v1/files/{file_token}/view_records`

## Permission Table

| Method | Required Scope |
|--------|---------------|
| `files.copy` | `docs:document:copy` |
| `files.create_folder` | `space:folder:create` |
| `files.list` | `space:document:retrieve` |
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
