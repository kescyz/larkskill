---
name: lark-drive
version: 2.0.0
description: "Use via LarkSkill MCP for Lark Drive (a.k.a. cloud disk / cloud storage / netdisk / my space): upload/download files, create folders, copy/move/delete, manage comments, permissions and secure labels, rename files, and import local Word/Markdown/Excel/CSV/PPTX or .base snapshots as online docx/sheet/bitable/slides. Also routes doubao.com Drive URLs/tokens."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# drive

**CRITICAL — Before starting, you MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling.**

> **Terminology note:** Lark Drive is also commonly called "cloud disk" or "cloud storage"; all three refer to the same product — Lark's official cloud file storage and management center.

> **Import routing rule:** If the user wants to import a local Excel / CSV / `.base` snapshot as Base / Bitable, you MUST use `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })` first. Do not switch to `lark-base` first; `lark-base` only handles in-table operations after import is complete.

## Quick Decision

- To **search docs / Wiki / spreadsheets / Base / Drive (cloud disk / cloud storage) objects**, prefer `lark_api({ tool: 'drive', op: 'search', args: {...} })`. Drive search is now the unified resource-search entry. Natural language phrases like "recently edited by me", "created by me" (→ `mine`, which is actually owner semantics), "the xxx I opened in the past week", "docx files owned by someone" map directly to flat args — avoid hand-writing nested JSON. The older `docs search` is in maintenance mode; do not add new dependencies on it.
- To import a local `.xlsx` / `.csv` / `.base` as Base / Bitable, the first step MUST be `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`.
- To import a local `.md` / `.docx` / `.doc` / `.txt` / `.html` as an online doc, use `lark_api({ tool: 'drive', op: 'import', args: { type: 'docx', ... } })`.
- To import a local `.pptx` as Lark Slides, use `lark_api({ tool: 'drive', op: 'import', args: { type: 'slides', ... } })`; the current PPTX import limit is 500MB.
- To upload, create, read, partially patch, or overwrite-update a **native `.md` file** in Drive (not import as docx), switch to [`lark-markdown`](../lark-markdown/SKILL.md).
- To compare **historical version diffs** of a native `.md` file, or compare a remote Markdown with a local draft, switch to [`lark-markdown`](../lark-markdown/SKILL.md)'s `markdown +diff`; when you need a version number, first use `lark_api({ tool: 'drive', op: 'version-history', args: {...} })`.
- To view, download, roll back, or delete a file's **historical versions**, use `lark_api({ tool: 'drive', op: 'version-history', args: {...} })`, `lark_api({ tool: 'drive', op: 'version-get', args: {...} })`, `lark_api({ tool: 'drive', op: 'version-revert', args: {...} })`, or `lark_api({ tool: 'drive', op: 'version-delete', args: {...} })`; this group supports both user and bot identity, prefer bot identity for automation scenarios.
- To import a local `.xlsx` / `.xls` / `.csv` as a spreadsheet, use `lark_api({ tool: 'drive', op: 'import', args: { type: 'sheet', ... } })`.
- To create a folder in Drive (cloud disk / cloud storage), prefer `lark_api({ tool: 'drive', op: 'create-folder', args: {...} })`.
- To upload a local file under a wiki node in a knowledge base / document library, still use `lark_api({ tool: 'drive', op: 'upload', args: { wiki_token: '<wiki_token>', ... } })`; do not mistakenly switch to `wiki` domain commands.
- To set or downgrade a document's **secure label** (classification), use the `secure-label-list` op to find the label ID, then the `secure-label-update` op. These ops are newer than the current MCP catalog snapshot — discover them with `lark_api_search("drive secure-label")` first (see the Secure Labels section).
- `lark-base` only handles Base internal operations (tables, fields, records, views) after import is complete; do not switch to `lark-base` early in the "local file -> Base" step.

## Rename

Use the Drive `files patch` operation; the `new_title` field renames the title, supporting docx, sheet, bitable, file, wiki, and folder types. Use `lark_api_search("drive files patch")` for the exact shape, then call `lark_api({ tool: 'drive', op: 'files.patch', args: { new_title: '...', ... } })`.

## Core Concepts

### Document Types and Tokens

In the Lark open platform, different document types have different URL formats and token handling. When performing document operations (such as adding comments or downloading files), you must first obtain the correct `file_token`.

### Document URL Format and Token Handling

| URL Format | Example | Token Type | Handling |
|----------|---------------------------------------------------------|-----------|----------|
| `/docx/` | `https://example.larksuite.com/docx/doxcnxxxxxxxxx` | `file_token` | Token in URL path is used directly as `file_token` |
| `/doc/` | `https://example.larksuite.com/doc/doccnxxxxxxxxx` | `file_token` | Token in URL path is used directly as `file_token` |
| `/wiki/` | `https://example.larksuite.com/wiki/wikcnxxxxxxxxx` | `wiki_token` | ⚠️ **Cannot be used directly** — must query first to obtain the real `obj_token` |
| `/sheets/` | `https://example.larksuite.com/sheets/shtcnxxxxxxxxx` | `file_token` | Token in URL path is used directly as `file_token` |
| `/drive/folder/` | `https://example.larksuite.com/drive/folder/fldcnxxxx` | `folder_token` | Token in URL path is used as the folder token |

### Wiki Link Special Handling (Critical!)

Wiki links (`/wiki/TOKEN`) may be backed by different document types such as cloud docs, spreadsheets, or Base. **Do not assume the token in the URL is the `file_token`** — you must query the actual type and real token first.

#### Handling Flow

**Recommended: use `drive inspect` to auto-unwrap**

```javascript
lark_api({ tool: 'drive', op: 'inspect', args: { url: 'https://xxx.feishu.cn/wiki/wikcnXXX' } })
```

The result includes `type` (underlying document type), `token` (real file_token), `title`, `url`, and other fields, for direct use in follow-up operations.

**Manual approach: query node info via the wiki API**

```javascript
lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: 'wiki_token' } })
```

1. **Extract key info from the result**
   - `node.obj_type`: document type (docx/doc/sheet/bitable/slides/file/mindnote)
   - `node.obj_token`: **the real document token** (used for follow-up operations)
   - `node.title`: document title

2. **Use the corresponding tool based on `obj_type`**

   | obj_type | Description | Tool to use |
   |----------|------|-----------|
   | `docx` | New-version cloud doc | `drive` file.comments ops, plus `docs` tool for content |
   | `doc` | Legacy cloud doc | `drive` file.comments ops |
   | `sheet` | Spreadsheet | `sheets` tool |
   | `bitable` | Base | `base` tool |
   | `slides` | Slides | `drive` tool |
   | `file` | File | `drive` tool |
   | `mindnote` | Mind map | `drive` tool |

#### Query Example

```javascript
// Query wiki node
lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: 'wiki_token' } })
```

Example result:
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

Drive Folder (cloud disk / cloud storage folder)
└── File (file/document)
    └── file_token (use directly)
```

### Common Operation Token Requirements

| Operation | Required Token | Notes |
|------|-------------|------|
| Read document content | `file_token` / auto-handled via `docs fetch` | `lark_api({ tool: 'docs', op: 'fetch', args: { api_version: 'v2', ... } })` accepts a URL directly |
| Add inline comment (selection comment) | `file_token` | When `block_id` is passed, `drive add-comment` creates an inline comment; `docx` supports text positioning or block_id, `sheet` uses `<sheetId>!<cell>`, `slides` uses `<slide-block-type>!<xml-id>`, and all support resolving to a wiki URL of the corresponding type; Drive file does not support inline comments |
| Add full-document comment | `file_token` | When `block_id` is not passed, `drive add-comment` creates a full-document comment by default; supports `docx`, legacy `doc` URLs, whitelisted-extension Drive files, and wiki URLs that resolve to `doc`/`docx`/`file` |
| Download file | `file_token` | Extracted directly from the file URL |
| Upload file | `folder_token` / `wiki_node_token` | Token for the target location |
| List document comments | `file_token` | Same as adding comments |

### Comment Capability Boundaries (Critical!)

- `lark_api({ tool: 'drive', op: 'add-comment', args: {...} })` supports two modes.
- Full-document comment: enabled by default when `block_id` is not passed, or explicitly with `full_comment: true`; supports `docx`, legacy `doc` URLs, whitelisted-extension Drive files, and wiki URLs that resolve to `doc`/`docx`/`file`.
- Inline comment: enabled when `block_id` is passed; `docx` supports text positioning or block id, `sheet` supports `<sheetId>!<cell>`, `slides` supports `<slide-block-type>!<xml-id>`, and wiki URLs that resolve to these types also support the corresponding inline comment. Drive file currently supports full-document comments only, not inline comments.
- Drive file comments only support whitelisted extensions: `.md`, `.txt`, `.json`, `.csv`, `.go`, `.js`, `.py`, `.pptx`, `.png`, `.jpg`, `.jpeg`, `.zip`, `.mp3`, `.mp4`. Ordinary files not on the whitelist such as `.pdf`, `.docx`, `.xlsx` are not yet supported; the call will error directly indicating comments are not yet supported for that type.
- For Review / proofreading / point-by-point issue scenarios, prefer inline comments; do not consolidate multiple positionable issues into a single full-document comment. See the [`+add-comment` behavior notes](references/lark-drive-add-comment.md) for specific parameters and positioning methods.
- The `content` for `drive add-comment` requires a `reply_elements` JSON array, e.g. `[{"type":"text","text":"body text"}]`.
- `slides` comments require explicitly passing `block_id` in `<slide-block-type>!<xml-id>` format; the call splits this into `anchor.block_id` and `anchor.slide_block_type`. The `<xml-id>` is the element `id` in the PPT XML protocol; `selection_with_ellipsis` and `full_comment` are not supported.
- Text written into comments (add comment, reply to comment, edit reply) MUST NOT contain raw `<` or `>`; escape before submitting: `<` → `&lt;`, `>` → `&gt;`.
- Using `lark_api({ tool: 'drive', op: 'add-comment', args: {...} })` auto-escapes `type=text` text elements as a fallback; if you call raw `drive file.comments create_v2`, `drive file.comment.replys create`, or `drive file.comment.replys update` directly, you must pass already-escaped content in the request.
- If the wiki resolves to a type other than `doc`/`docx`/`file`/`sheet`/`slides`, do not use `add-comment`.
- If you need lower-level direct calls to the comment V2 protocol, use the raw API: first run `lark_api_search("drive file.comments create_v2")` to view the shape, then call `lark_api({ tool: 'drive', op: 'file.comments', args: { method: 'create_v2', ... } })`. Full-document comments omit `anchor`; inline comments pass `anchor.block_id`.

### Comment Query and Count Conventions (Critical!)

**Mandatory rule**: `drive file.comments list` MUST default to `is_solved: false`, i.e. query only unsolved comments. Even if the user says "all comments", "every comment", or "list out all the comments", as long as they do not explicitly mention including resolved comments, still query unsolved comments by default. Only when the user explicitly asks to include resolved comments may you omit the `is_solved` parameter.

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

- To query document comments, use `drive file.comments list`.
- The `items` returned by `drive file.comments list` should be understood as a list of "comment cards" — each `item` corresponds to one comment card seen in the UI, not a flat list of interaction messages.
- Semantically on the server side, creating the first comment also creates the first reply within that card; therefore the real body content is carried in each `item.reply_list.replies`, where the first reply is, from the user's perspective, the "comment itself" in that card.
- When the user wants to count "comments" or "comment cards", count the length of `items`; for a full count, accumulate the `items` lengths across all paginated comment results.
- When the user wants to count "replies", from the user's perspective you should exclude the first comment in each card; the count is the sum of all `item.reply_list.replies` lengths minus the length of `items`.
- When the user wants to count "total interactions", count the sum of all `item.reply_list.replies` lengths; this measure includes the first comment in each card.
- If some `item.has_more=true`, that comment card has more replies not included in the current result; in that case continue calling `drive file.comment.replys list` to fetch them all before doing the full reply-count / total-interaction count.

### Comment Business Rules and Routing (Critical!)

#### Review Scenario Comment Placement
- The default strategy is "go inline whenever possible": when the user says review, proofread, check the document, flag issues, give edit suggestions, or comment point by point, prefer creating inline comments.
- Multiple independent issues should each get a separate inline comment; do not merge review findings into a full-document comment to save call count.
- Only fall back to a full-document comment when the target type supports full-document comments AND any of the following holds: the user explicitly asks for a full / overall comment, the comment content is genuinely a document-level summary, the target type does not support inline comments, or you cannot reliably position a specific location; otherwise explain the limitation and ask the user for a positionable location.
- See the [`+add-comment` behavior notes](references/lark-drive-add-comment.md) for specific parameters, positioning methods, and constraints across document types.

#### Comment Sort Routing
- A document usually has multiple comments, sorted by `create_time` (creation time).
- **Important**: only sort by `create_time` when the user explicitly mentions "latest comment", "last comment", or "earliest comment":
  - **You MUST first fetch all comments (handle pagination and pull all data)** — do not sort after fetching only one page
  - "latest comment" / "last comment": sort by `create_time` descending and take the first
  - "earliest comment": sort by `create_time` ascending and take the first
- If the user only says "the first comment", just use the first item returned by `drive file.comments list` without additional sorting.

#### Comment Reply Restrictions
- **Before adding a comment reply, check for the following restrictions**
- **Full-document comments do not support replies**: comments with `is_whole=true` (full-document comments) cannot accept replies; for such comments, tell the user "full-document comments do not support replies".
- **Resolved comments do not support replies**: comments with `is_solved=true` cannot accept replies; for such comments, tell the user "this comment has been resolved and cannot be replied to".
- **Note**: when the user wants to reply to a comment that cannot be replied to due to the above restrictions, only inform them it cannot be replied to; **do not automatically find another comment to reply to**, to avoid behavior that does not match the user's expectation.

#### Choosing Between Batch Query and List Query
- `drive file.comments batch_query` is a batch query **after the comment IDs are known**; it requires passing a specific list of comment IDs.
- `drive file.comments list` is for paginated retrieval of the comment list — suitable for counting total comments, traversing all comments, or fetching "the latest/last N comments" scenarios.

#### Reaction Scenarios
- For questions about reactions on comments/replies (emoji, per-emoji counts, who reacted with what, add/remove reaction), **first read [lark-drive-reactions.md](../../skills/lark-drive/references/lark-drive-reactions.md) to learn how to use it**.

### Common Errors and Solutions

| Error message | Cause | Solution |
|----------|------|----------|
| `not exist` | Wrong token used | Check the token type; wiki links must query first to get `obj_token` |
| `permission denied` | No permission for the operation | Guide the user to check whether the current identity has the relevant permission on the document/file; grant the appropriate permission if needed |
| `invalid file_type` | Wrong file_type parameter | Pass the correct file_type based on `obj_type` (docx/doc/sheet/slides) |

#### `permission.public.patch` Error Code Guidance

When `drive permission.public patch` fails to update a document's public permission, if it returns one of the following error codes, give the user a clear next step per the table. Do not simply classify these as missing scopes; they usually mean the tenant, external-sharing, or document-classification policy blocked the request.

| Error code | Meaning | User guidance |
|--------|------------------------|--------------|
| `91009` | External sharing is governed by tenant security policy; the current user cannot enable it | Tell the user: external-sharing capability is centrally governed by tenant security policy and cannot be enabled via API or directly by the current user; they must contact the tenant admin to adjust the org-level external-sharing policy. |
| `91010` | Document external sharing is not enabled | Tell the user: external sharing is not yet enabled for this document; please enable external sharing in the document permission settings first, then retry. |
| `91011` | External sharing is blocked by document classification | Tell the user: external sharing is blocked by the classification policy; they must open the target document and initiate a classification exemption or downgrade in the document, then retry; the reply MUST include the target document URL. |
| `91012` | Permission settings are blocked by document classification | Tell the user: this permission setting is blocked by the classification policy; they must open the target document and initiate a classification exemption or downgrade in the document, then retry; the reply MUST include the target document URL. |

When the user originally provided a document URL, return that URL as-is to the user as the operation entry point on `91011` or `91012`; if the context only has a token, first try to recover the target document URL from existing context, search results, or metadata, then provide a clickable document URL.

### Grant Current App Access to Document

When you need to grant document permission to **the current app (bot) itself**, first get the app's open_id via the bot info API, then call the permission API to grant access:

```javascript
// 1. Get the current app's open_id
lark_api({ method: 'GET', path: '/open-apis/bot/v3/info' })
// Take bot.open_id from the result

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

> **Note**: This approach applies only when granting access to **the current app**. When granting access to other users, just use the other party's open_id directly — no need to call the bot info API.

`<resource_type>` options: `doc`, `docx`, `sheet`, `bitable`, `file`, `folder`, `wiki`, `slides`.

### Secure Labels (Classification)

Both secure-label operations run with user identity. Before changing a document's classification, first list available labels to confirm the target label ID. The `secure-label-list` and `secure-label-update` ops were added in a newer Lark CLI release than the current MCP catalog snapshot, so discover them and their exact arg shape via `lark_api_search` before calling:

```javascript
// 1. List secure labels available to the current user
//    (then call the discovered op; page_size range 1..10, default 10; lang: zh|en|ja)
lark_api_search("drive secure-label list available labels")

// 2. Update the target document's secure label
//    (token + label_id required; then call the discovered op)
lark_api_search("drive secure-label update document classification")
```

- The update op's `token` accepts a document URL or bare token; a URL auto-infers `type`. For a bare token, pass `type` (one of `doc`, `docx`, `sheet`, `file`, `bitable`, `mindnote`, `slides`). Pass the chosen `label_id` from the list step.
- Error code `1063013` (classification downgrade needs approval): tell the user to open the target document and complete the classification-downgrade approval in the document UI, then retry; if the user provided a document URL, include that URL as the operation entry point. Do not keep retrying the API or suggest adding scopes — this is a document-side approval requirement.

## Operations (use via LarkSkill MCP)

Use `lark_api({ tool: 'drive', op: '<op>', args: {...} })` for all shortcut operations. Prefer a Shortcut when one exists.

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'drive', op: 'search', args: {...} })` | Search Lark docs, Wiki, and spreadsheet files with flat filter args (`edited_since`, `mine`, `doc_types`, etc.) — the unified resource-search entry, preferred over `docs search` |
| `lark_api({ tool: 'drive', op: 'upload', args: {...} })` | Upload a local file to a Drive folder or wiki node |
| `lark_api({ tool: 'drive', op: 'create-folder', args: {...} })` | Create a Drive folder, optionally under a parent folder, with bot auto-grant support |
| `lark_api({ tool: 'drive', op: 'download', args: {...} })` | Download a file from Drive to local |
| `lark_api({ tool: 'drive', op: 'status', args: {...} })` | Compare a local directory with a Drive folder by exact SHA-256 hash, or `quick` for a best-effort modified-time diff; reports `new_local` / `new_remote` / `modified` / `unchanged`. Duplicate remote `rel_path` conflicts fail fast. `local_dir` must stay inside cwd. |
| `lark_api({ tool: 'drive', op: 'pull', args: {...} })` | File-level Drive → local mirror. `if_exists` supports `overwrite` / `smart` / `skip`. `delete_local` requires `yes: true`. `local_dir` must stay inside cwd. |
| `lark_api({ tool: 'drive', op: 'sync', args: {...} })` | Two-way local ↔ Drive sync. Resolves `modified` via `on_conflict` (`remote-wins`/`local-wins`/`keep-both`/`ask`). Intentionally non-destructive — no delete on either side. |
| `lark_api({ tool: 'drive', op: 'create-shortcut', args: {...} })` | Create a shortcut to an existing Drive file in another folder |
| `lark_api({ tool: 'drive', op: 'add-comment', args: {...} })` | Add a comment to doc/docx/file/sheet/slides; also supports wiki URL resolving; file targets support selected extensions and full comments only |
| `lark_api({ tool: 'drive', op: 'export', args: {...} })` | Export a doc/docx/sheet/bitable/slides to a local file with limited polling |
| `lark_api({ tool: 'drive', op: 'export-download', args: {...} })` | Download an exported file by file_token |
| `lark_api({ tool: 'drive', op: 'import', args: {...} })` | Import a local file to Drive as a cloud document (docx, sheet, bitable, slides) |
| `lark_api({ tool: 'drive', op: 'version-history', args: {...} })` | List historical versions of a file |
| `lark_api({ tool: 'drive', op: 'version-get', args: {...} })` | Download a specific historical version |
| `lark_api({ tool: 'drive', op: 'version-revert', args: {...} })` | Revert a file to a specific historical version |
| `lark_api({ tool: 'drive', op: 'version-delete', args: {...} })` | Delete a specific historical version |
| `lark_api({ tool: 'drive', op: 'move', args: {...} })` | Move a file or folder to another location in Drive |
| `lark_api({ tool: 'drive', op: 'delete', args: {...} })` | Delete a Drive file or folder with limited polling for folder deletes |
| `lark_api({ tool: 'drive', op: 'push', args: {...} })` | File-level local → Drive mirror. `if_exists` supports `skip` / `smart` / `overwrite`. `delete_remote` requires `yes: true`. `local_dir` must stay inside cwd. |
| `lark_api({ tool: 'drive', op: 'task_result', args: {...} })` | Poll async task result for import, export, move, or delete operations |
| `lark_api({ tool: 'drive', op: 'inspect', args: {...} })` | Inspect a Lark document URL; auto-unwraps wiki URLs to the underlying document |
| `lark_api({ tool: 'drive', op: 'apply-permission', args: {...} })` | Apply to the document owner for view/edit access (user-only; 5/day per document) |
| `secure-label-list` (discover via `lark_api_search("drive secure-label")`) | List secure labels available to the current user — newer than the catalog snapshot, so discover the op shape via `lark_api_search` first |
| `secure-label-update` (discover via `lark_api_search("drive secure-label")`) | Update a Drive file/document secure label; downgrade approval errors require opening the document UI — discover the op shape via `lark_api_search` first |

## API Resources

> **Important**: Use `lark_api_search` to look up the parameter structure before using raw API calls; do not guess field formats.

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
  - `create_v2` — Add full-document / inline (selection) comment
  - `list` — Paginated retrieval of document comments
  - `patch` — Resolve / restore a comment

### file.comment.replys

```javascript
lark_api({ tool: 'drive', op: 'file.comment.replys', args: { method: 'create', ... } })
lark_api({ tool: 'drive', op: 'file.comment.replys', args: { method: 'delete', ... } })
lark_api({ tool: 'drive', op: 'file.comment.replys', args: { method: 'list', ... } })
lark_api({ tool: 'drive', op: 'file.comment.replys', args: { method: 'update', ... } })
```

  - `create` — Add a reply
  - `delete` — Delete a reply
  - `list` — Get replies
  - `update` — Update a reply

### permission.members

```javascript
lark_api({ tool: 'drive', op: 'permission.members', args: { method: 'create', token: '...', type: '...', ... } })
```

  - `auth` — Check user permission
  - `create` — Add collaborator permission
  - `transfer_owner` — Transfer document owner

### metas

> Use `lark_api_search("drive metas batch_query")` to get the exact parameter shape before calling.

  - `batch_query` — Get document metadata

### user

> Use `lark_api_search("drive user <method>")` to get the exact parameter shape before calling.

  - `subscription` — Subscribe to user/app dimension events (includes the comment-added event)
  - `subscription_status` — Query subscription status of a user/app for a given event
  - `remove_subscription` — Unsubscribe from user/app dimension events

### file.statistics

```javascript
lark_api({ tool: 'drive', op: 'file.statistics', args: { method: 'get', file_token: '...', ... } })
```

  - `get` — Get file statistics

### file.view_records

```javascript
lark_api({ tool: 'drive', op: 'file.view_records', args: { method: 'list', file_token: '...', ... } })
```

  - `list` — Get document visitor records

### file.comment.reply.reactions

```javascript
lark_api({ tool: 'drive', op: 'file.comment.reply.reactions', args: { method: 'update_reaction', ... } })
```

  - `update_reaction` — Add / remove a reaction

## Permissions Table

| Method | Required scope |
|------------------------------------------------|-----------------------------------|
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
