---
name: lark-drive
version: 1.0.0
description: "Lark Drive (cloud storage): manage files and folders in Drive. Upload and download files, create folders, copy/move/delete files, view file metadata, manage document comments, manage document permissions, subscribe to user comment change events, modify file titles (docx, sheet, bitable, file, folder, wiki); also imports local Word/Markdown/Excel/CSV/PPTX and Base snapshots (.base) as Lark cloud documents (docx, sheet, bitable, slides). Use this skill when the user needs to upload or download files, organize Drive directories, view file details, manage comments, manage document permissions, modify file titles, subscribe to user comment change events, or import local files as new-format documents, spreadsheets, Base/bitable, or slides. \"Drive\", \"cloud disk\", and \"cloud storage\" are the same concept; when the user says \"cloud disk\", \"cloud storage\", \"network drive\", or \"my space\", route to this skill. When the user provides a doubao.com Drive resource URL/token, or explicitly mentions a file/folder/docx/sheet/bitable/wiki resource in Doubao, use this skill directly — do NOT fall back to WebFetch because the domain is not Lark; routing is based on resource type, URL path pattern, and token, not domain."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search", "lark_auth_login", "lark_auth_logout", "lark_auth_status", "lark_whoami", "lark_enable_domain"]
---

# drive (v1)

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which contains authentication and permission handling.**

> **Terminology note:** Lark Drive is also commonly referred to as "cloud disk" or "cloud storage"; all three refer to the same product — Lark's official cloud file storage and management center.

> **Import routing rule:** If the user wants to import a local Excel / CSV / `.base` snapshot as Base / bitable, MUST use `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })` first. Do NOT switch to `lark-base` first; `lark-base` only handles in-table operations after the import is complete.

## Quick Decision

- User wants to **organize Drive / folders / document library / Wiki / personal document library**, or "audit directory structure, find unarchived/temp/duplicate/empty directories, generate an organization plan": MUST first read [`references/lark-drive-workflow-knowledge-organize.md`](references/lark-drive-workflow-knowledge-organize.md). Default is to generate a plan only; creating directories, moving resources, and requesting permissions all require separate confirmation.
- User wants to **search documents / Wiki / spreadsheets / Base / Drive objects**: prefer `lark_api({ tool: 'drive', op: 'search', args: {...} })`. Natural-language phrases like "recently edited by me", "created by me" (→ `mine`, which is owner semantics), "docs I opened in the last week", "docx owned by someone" map directly to flat flags — avoid hand-writing nested JSON.
- User wants to import a local `.xlsx` / `.csv` / `.base` as Base / bitable: first step MUST use `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`.
- User wants to import a local `.md` / `.docx` / `.doc` / `.txt` / `.html` as an online document: use `lark_api({ tool: 'drive', op: 'import', args: { type: 'docx', ... } })`.
- User wants to import a local `.pptx` as Lark Slides: use `lark_api({ tool: 'drive', op: 'import', args: { type: 'slides', ... } })`; current PPTX import limit is 500MB.
- User wants to upload, create, read, partially patch, or overwrite-update a **native `.md` file** in Drive (not import as docx): switch to [`lark-markdown`](../lark-markdown/SKILL.md).
- User wants to compare **historical version diffs** of native `.md` files, or compare remote Markdown with a local draft: switch to [`lark-markdown`](../lark-markdown/SKILL.md) `lark_api({ tool: 'markdown', op: 'diff', ... })`; use `lark_api({ tool: 'drive', op: 'version-history', ... })` first when version numbers are needed.
- User wants to view, download, revert, or delete **historical versions** of a file: use `drive version-history`, `drive version-get`, `drive version-revert`, `drive version-delete`; this group supports both user and bot identity, prefer bot identity for automation scenarios.
- User wants to import a local `.xlsx` / `.xls` / `.csv` as a spreadsheet: use `lark_api({ tool: 'drive', op: 'import', args: { type: 'sheet', ... } })`.
- User wants to **create a folder** in Drive: prefer `lark_api({ tool: 'drive', op: 'create-folder', args: {...} })`.
- User wants to upload a local file to a wiki node inside a Wiki / document library: still use `lark_api({ tool: 'drive', op: 'upload', args: { wiki_token: '<wiki_token>', ... } })`; do NOT mistakenly switch to `wiki` domain operations.
- `lark-base` only handles internal Base operations (tables, fields, records, views) after import is complete; do NOT switch to `lark-base` at the "local file → Base" step.

## Modifying Titles
- Use the `drive files_patch` operation; the `new_title` field allows modifying the title, supporting docx, sheet, bitable, file, wiki, and folder types.

## Core Concepts

### Document Types and Tokens

In the Lark Open Platform, different document types have different URL formats and token handling. When performing document operations (such as adding comments or downloading files), you MUST first obtain the correct `file_token`.

### Document URL Formats and Token Handling

| URL Format | Example | Token Type | Handling |
|------------|---------|-----------|----------|
| `/docx/` | `https://example.larksuite.com/docx/doxcnxxxxxxxxx` | `file_token` | Token in URL path is used directly as `file_token` |
| `/doc/` | `https://example.larksuite.com/doc/doccnxxxxxxxxx` | `file_token` | Token in URL path is used directly as `file_token` |
| `/wiki/` | `https://example.larksuite.com/wiki/wikcnxxxxxxxxx` | `wiki_token` | ⚠️ **Cannot be used directly** — must query first to get the real `obj_token` |
| `/sheets/` | `https://example.larksuite.com/sheets/shtcnxxxxxxxxx` | `file_token` | Token in URL path is used directly as `file_token` |
| `/drive/folder/` | `https://example.larksuite.com/drive/folder/fldcnxxxx` | `folder_token` | Token in URL path is used as folder token |

### Special Handling for Wiki Links (Critical!)

A Wiki link (`/wiki/TOKEN`) may point to different document types — cloud docs, spreadsheets, Base, etc. **Do NOT assume the token in the URL is the `file_token`** — you MUST first query the actual type and real token.

#### Handling Flow

**Recommended: use `drive inspect` for automatic unwrapping**

```javascript
lark_api({ tool: 'drive', op: 'inspect', args: { url: 'https://xxx.feishu.cn/wiki/wikcnXXX' } })
```

The result contains `type` (underlying document type), `token` (real file_token), `title`, `url`, etc., ready to use in subsequent operations.

**Manual: use `wiki spaces_get_node` to query node info**

1. **Use `wiki spaces_get_node` to query node info**
   ```javascript
   lark_api({ tool: 'wiki', op: 'spaces.get_node', args: { params: { token: 'wiki_token' } } })
   ```

2. **Extract key information from the result**
   - `node.obj_type`: document type (docx/doc/sheet/bitable/slides/file/mindnote)
   - `node.obj_token`: **real document token** (used in subsequent operations)
   - `node.title`: document title

3. **Use the corresponding API based on `obj_type`**

   | obj_type | Description | API to use |
   |----------|-------------|-----------|
   | `docx` | New-format cloud doc | `drive file.comments.*`, `docx.*` |
   | `doc` | Old-format cloud doc | `drive file.comments.*` |
   | `sheet` | Spreadsheet | `sheets.*` |
   | `bitable` | Base | `bitable.*` |
   | `slides` | Slides | `drive.*` |
   | `file` | File | `drive.*` |
   | `mindnote` | Mind map | `drive.*` |

#### Query Example

```javascript
// Query wiki node
lark_api({ tool: 'wiki', op: 'spaces.get_node', args: { params: { token: 'wiki_token' } } })
```

Sample result:
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
    ├── obj_type: docx (new-format document)
    │   └── obj_token (real document token)
    ├── obj_type: doc (old-format document)
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

### Token Requirements for Common Operations

| Operation | Token Required | Notes |
|-----------|---------------|-------|
| Read document content | `file_token` / handled automatically via `lark_api({ tool: 'docs', op: 'fetch', args: { api_version: 'v2', ... } })` | `docs fetch` with `api_version: 'v2'` supports passing URL directly |
| Add inline comment (selection comment) | `file_token` | When `block_id` is passed, `drive add_comment` creates an inline comment; `docx` supports text anchor or block_id, `sheet` uses `<sheetId>!<cell>`, `slides` uses `<slide-block-type>!<xml-id>`, and all support wiki URLs that resolve to the corresponding type; Drive file does not support inline comments |
| Add whole-document comment | `file_token` | When `block_id` is not passed, `drive add_comment` creates a whole-document comment by default; supports `docx`, old `doc` URLs, Drive files with whitelisted extensions, and wiki URLs that resolve to `doc`/`docx`/`file` |
| Download file | `file_token` | Extract directly from file URL |
| Upload file | `folder_token` / `wiki_node_token` | Token of the target location |
| List document comments | `file_token` | Same as adding a comment |

### Comment Capability Boundaries (Critical!)

- `drive add_comment` supports two modes.
- Whole-document comment: enabled by default when `block_id` is not passed; can also be explicitly passed `full_comment: true`; supports `docx`, old `doc` URLs, Drive files with whitelisted extensions, and wiki URLs that resolve to `doc`/`docx`/`file`.
- Inline comment: enabled when `block_id` is passed; `docx` supports text anchor or block id, `sheet` supports `<sheetId>!<cell>`, `slides` supports `<slide-block-type>!<xml-id>`, wiki URLs resolving to these types also support corresponding inline comments. Drive file currently only supports whole-document comments, not inline comments.
- Drive file comments only support whitelisted extensions: `.md`, `.txt`, `.json`, `.csv`, `.go`, `.js`, `.py`, `.pptx`, `.png`, `.jpg`, `.jpeg`, `.zip`, `.mp3`, `.mp4`. Unlisted common files such as `.pdf`, `.docx`, `.xlsx` are not supported — the LarkSkill MCP tool will report an error directly indicating this type of comment is not yet supported.
- Review / proofreading / annotating issues scenarios: prefer inline comments; do NOT aggregate multiple locatable issues into a single whole-document comment. See specific parameters and anchoring methods in [`drive add_comment` behavior notes](references/lark-drive-add-comment.md).
- `drive add_comment`'s `content` requires passing a `reply_elements` JSON array string, e.g. `content: '[{"type":"text","text":"body text"}]'`.
- `slides` comments require explicitly passing `block_id: '<slide-block-type>!<xml-id>'`; the operation splits this and writes it into `anchor.block_id` and `anchor.slide_block_type`. The `<xml-id>` is the element `id` in the PPT XML protocol; `selection_with_ellipsis` and `full_comment` are not supported.

- Text in comment content (adding comments, replying to comments, editing replies) MUST NOT contain raw `<` or `>`; escape before submitting: `<` → `&lt;`, `>` → `&gt;`.
- When using `drive add_comment`, the shortcut auto-escapes the above for `type=text` text elements as a safety net. If calling `drive file.comments.create_v2`, `drive file.comment.replys.create`, or `drive file.comment.replys.update` directly, you must pass pre-escaped content in the request.
- If the wiki URL resolves to something other than `doc`/`docx`/`file`/`sheet`/`slides`, do NOT use `drive add_comment`.
- If you need lower-level direct access to the comment V2 protocol, use the native API: first run `lark_api_search({ query: 'drive file.comments create_v2' })` to check parameter structure, then call `lark_api({ tool: 'drive', op: 'file.comments.create_v2', args: { ... } })`. Whole-document comments omit `anchor`; inline comments pass `anchor.block_id`.

### Comment Query and Count Semantics (Critical!)

**Mandatory rule**: `drive file_comments_list` MUST default to passing `is_solved: false`, i.e., query unsolved comments only. Even when the user says "all comments", "every comment", "list all comments" — as long as they have not explicitly mentioned including solved comments, still query unsolved comments by default. Only when the user explicitly requests including solved comments may the `is_solved` parameter be omitted.

**Correct examples:**

```javascript
// Default query: unsolved comments only (recommended)
lark_api({ tool: 'drive', op: 'file.comments.list', args: { params: { file_token: 'xxx', file_type: 'docx', is_solved: false } } })

// Query all comments (user has not explicitly requested including solved comments)
lark_api({ tool: 'drive', op: 'file.comments.list', args: { params: { file_token: 'xxx', file_type: 'docx', is_solved: false } } })

// Include solved comments (requires explicit user request)
lark_api({ tool: 'drive', op: 'file.comments.list', args: { params: { file_token: 'xxx', file_type: 'docx' } } })
```

**Incorrect example:**

```javascript
// Not recommended: querying all comments without explicit user request
lark_api({ tool: 'drive', op: 'file.comments.list', args: { params: { file_token: 'xxx', file_type: 'docx' } } })
```

- To query document comments, use `lark_api({ tool: 'drive', op: 'file.comments.list', args: {...} })`.
- The `items` returned by `drive file_comments_list` should be understood as a list of "comment cards"; each `item` corresponds to one comment card visible in the UI, not a flat list of interaction messages.
- Semantically on the server side, creating the first comment also creates the first reply inside that card; therefore the actual content is carried in each `item.reply_list.replies`, where the first reply is — from the user's perspective — the "comment itself" on that card.
- When the user wants to count "number of comments" or "number of comment cards", count the length of `items`; for a total count, accumulate the `items` length across all paginated results.
- When the user wants to count "number of replies", from the user's perspective exclude the first comment in each card; the count is the sum of all `item.reply_list.replies` lengths minus the length of `items`.
- When the user wants to count "total interactions", sum the lengths of all `item.reply_list.replies`; this includes the first comment in each card.
- If a given `item.has_more=true`, that card has more replies not included in the current response; call `lark_api({ tool: 'drive', op: 'file.comment.replys.list', args: {...} })` to fetch all, then compute full reply count / total interaction count.

### Comment Business Rules and Guidance (Critical!)

#### Review Scenario Comment Anchoring
- Default strategy is "inline when possible": when the user says review, proofread, check document, annotate issues, give revision suggestions, comment line by line — prefer creating inline comments.
- Multiple independent issues should each get a separate inline comment; do NOT merge review findings into a whole-document comment to save API calls.
- Only fall back to a whole-document comment when the target type supports it AND one of the following applies: user explicitly requests a whole-document/overall comment, the comment is genuinely a document-level summary, the target type does not support inline comments, or a specific location cannot be stably identified; otherwise explain the limitation and ask the user for a locatable position.
- See specific parameters, anchoring methods, and constraints per document type in [`drive add_comment` behavior notes](references/lark-drive-add-comment.md).

#### Comment Sorting Guidance
- A document typically has multiple comments sorted by `create_time` (creation time).
- **Important**: only sort by `create_time` when the user explicitly mentions "latest comment", "last comment", or "earliest comment":
  - **MUST first fetch all comments (paginate to get all data)** — do NOT sort after fetching only one page.
  - "Latest comment" / "last comment": sort by `create_time` descending, take the first entry.
  - "Earliest comment": sort by `create_time` ascending, take the first entry.
- If the user just says "first comment", use the first entry returned by `drive file_comments_list` directly — no extra sorting needed.

#### Comment Reply Restrictions
- **Check for the following restrictions before adding a comment reply**
- **Whole-document comments do not support replies**: comments with `is_whole=true` cannot have replies added; inform the user "whole-document comments do not support replies".
- **Solved comments do not support replies**: comments with `is_solved=true` cannot have replies added; inform the user "this comment has been resolved and cannot be replied to".
- **Note**: when the user wants to reply to a comment but that comment cannot be replied to due to the above restrictions, only inform them it cannot be replied to — **do NOT automatically find other replyable comments** on the user's behalf, as this may not match user intent.

#### Choosing Between Batch Query and List Query
- Use `lark_api({ tool: 'drive', op: 'file.comments.batch_query', args: {...} })` for **bulk querying when comment IDs are already known** — pass a specific list of comment IDs.
- Use `lark_api({ tool: 'drive', op: 'file.comments.list', args: {...} })` for paginated retrieval of the comment list, suitable for counting total comments, iterating all comments, or getting "latest/last N comments".

#### Reaction / Emoji Scenarios
- When encountering questions about reactions on comments/replies (emoji types, emoji counts, who reacted, add/delete reaction), **first read [lark-drive-reactions.md](../../skills/lark-drive/references/lark-drive-reactions.md) to learn how to use them**.

### Common Errors and Solutions

| Error Message | Cause | Solution |
|--------------|-------|---------|
| `not exist` | Wrong token used | Check token type; wiki links must be queried first to get `obj_token` |
| `permission denied` | Insufficient permissions for the operation | Guide user to check if the current identity has the required permissions for the document/file; grant permissions if needed |
| `invalid file_type` | Incorrect file_type parameter | Pass the correct file_type based on `obj_type` (docx/doc/sheet/slides) |

#### `permission_public_patch` Error Code Guidance

When calling `lark_api({ tool: 'drive', op: 'permission.public.patch', args: {...} })` to update public document permissions fails, if the following error codes are returned, give the user a clear next step per the table. Do NOT simply classify these as missing scope; they typically indicate tenant, external sharing, or document security-level policy blocks.

| Error Code | Meaning | Guidance for User |
|-----------|---------|------------------|
| `91009` | External sharing is controlled by tenant security policy; current user cannot enable it | Inform user: external sharing is under unified tenant security policy control and cannot be enabled via API or by the current user; contact the tenant admin to adjust the organization-level external sharing policy. |
| `91010` | External sharing for this document is not enabled | Inform user: external sharing for this document is not yet enabled; please enable external sharing in the document permission settings first, then retry `permission_public_patch`. |
| `91011` | External sharing is blocked by document security level | Inform user: external sharing is blocked by the security-level policy; open the target document and initiate a security-level exemption or downgrade within the document, then retry; the response MUST include the target document URL. |
| `91012` | Permission settings are blocked by document security level | Inform user: this permission setting is blocked by the security-level policy; open the target document and initiate a security-level exemption or downgrade within the document, then retry; the response MUST include the target document URL. |

When the user originally provided a document URL and encounters `91011` or `91012`, return that URL as-is for the user as the action entry point; if only a token is available in context, try to recover the target document URL from existing context, search results, or metadata before providing a clickable document URL.

### Granting the Current App Access to a Document

When granting document permissions to **the current app (bot) itself**, first get the app's open_id via the bot info API, then call the permission API to authorize:

```javascript
// 1. Get the current app's open_id
lark_api({ method: 'GET', path: '/open-apis/bot/v3/info', args: { as: 'bot' } })
// Extract bot.open_id from the response

// 2. Grant the current app access to the document
lark_api({ tool: 'drive', op: 'permission.members.create', args: {
  params: { token: '<doc_token>', type: '<resource_type>' },
  data: { member_type: 'openid', member_id: '<bot_open_id>', perm: 'view', type: 'user' }
} })
```

> **Note**: this approach only applies when granting access to **the current app**. When granting access to another user, use their open_id directly — no need to call the bot info API.

`<resource_type>` valid values: `doc`, `docx`, `sheet`, `bitable`, `file`, `folder`, `wiki`, `slides`.

## Shortcuts (prefer these)

Shortcuts are high-level wrappers for common operations. Use shortcuts when available.

| Shortcut | Description |
|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`drive search`](references/lark-drive-search.md) | Search Lark docs, Wiki, and spreadsheet files with flat filter flags. Natural-language-friendly: `edited_since`, `mine`, `doc_types`, etc. |
| [`drive upload`](references/lark-drive-upload.md) | Upload a local file to a Drive folder or wiki node |
| [`drive create_folder`](references/lark-drive-create-folder.md) | Create a Drive folder, optionally under a parent folder, with bot auto-grant support |
| [`drive download`](references/lark-drive-download.md) | Download a file from Drive to local |
| [`drive status`](references/lark-drive-status.md) | Compare a local directory with a Drive folder by exact SHA-256 hash by default, or use `quick: true` for a best-effort modified-time diff that skips remote downloads; reports `new_local` / `new_remote` / `modified` / `unchanged` plus `detection=exact` or `detection=quick`. Duplicate remote `rel_path` conflicts fail fast with `error.type=duplicate_remote_path` and list every conflicting entry; do not proceed as if one was chosen. `local_dir` must be a relative path inside cwd; out-of-bounds paths are rejected — guide the user to switch the agent working directory instead of secretly changing it. |
| [`drive pull`](references/lark-drive-pull.md) | File-level Drive → local mirror. Duplicate remote `rel_path` conflicts fail by default; for duplicate files, `rename` downloads all copies with stable hashed suffixes, while `newest` / `oldest` pick one. `if_exists` supports `overwrite` / `smart` / `skip` (`smart` is a best-effort modified-time incremental mode for repeat syncs). `delete_local` requires `yes: true`, only removes regular files, and is skipped after item failures. `local_dir` must stay inside cwd. |
| `drive sync` | Two-way local ↔ Drive sync. Reuses `status` diff buckets, pulls `new_remote`, pushes `new_local`, and resolves `modified` via `on_conflict: 'remote-wins'|'local-wins'|'keep-both'|'ask'`. `quick: true` enables best-effort modified-time diffing (timestamp mismatches can still trigger real pull/push actions), `on_duplicate_remote` supports `fail|newest|oldest`, and the command is intentionally non-destructive (no delete on either side). |
| [`drive create_shortcut`](references/lark-drive-create-shortcut.md) | Create a shortcut to an existing Drive file in another folder |
| [`drive add_comment`](references/lark-drive-add-comment.md) | Add a comment to doc/docx/file/sheet/slides, also supports wiki URL resolving to doc/docx/file/sheet/slides; file targets support selected extensions and full comments only |
| [`drive export`](references/lark-drive-export.md) | Export a doc/docx/sheet/bitable/slides to a local file with limited polling; supports `file_name` for local naming |
| [`drive export_download`](references/lark-drive-export-download.md) | Download an exported file by file_token |
| [`drive import`](references/lark-drive-import.md) | Import a local file to Drive as a cloud document (docx, sheet, bitable, slides) |
| [`drive version_history`](references/lark-drive-version-history.md) | List historical versions of a file with only_tag=true and cursor-based pagination |
| [`drive version_get`](references/lark-drive-version-get.md) | Download a specific historical version of a file |
| [`drive version_revert`](references/lark-drive-version-revert.md) | Revert a file to a specific historical version |
| [`drive version_delete`](references/lark-drive-version-delete.md) | Delete a specific historical version of a file |
| [`drive move`](references/lark-drive-move.md) | Move a file or folder to another location in Drive |
| [`drive delete`](references/lark-drive-delete.md) | Delete a Drive file or folder with limited polling for folder deletes |
| [`drive push`](references/lark-drive-push.md) | File-level local → Drive mirror. Duplicate remote `rel_path` conflicts fail by default; `newest` / `oldest` only apply to duplicate files when you explicitly want to target one remote file. `if_exists` supports `skip` / `smart` / `overwrite` (`smart` skips files whose remote `modified_time` is already up to date, but falls through to the same overwrite path when the remote is older, so it inherits overwrite's rollout caveat). `delete_remote` requires `yes: true`. `local_dir` must stay inside cwd. |
| [`drive task_result`](references/lark-drive-task-result.md) | Poll async task result for import, export, move, or delete operations |
| [`drive inspect`](references/lark-drive-inspect.md) | Inspect a Lark document URL to get its type, title, and canonical token; auto-unwraps wiki URLs to the underlying document |
| [`drive apply_permission`](references/lark-drive-apply-permission.md) | Apply to the document owner for view/edit access (user-only; 5/day per document) |
| [`drive secure_label_list`](references/lark-drive-secure-label.md) | List secure labels available to the current user |
| [`drive secure_label_update`](references/lark-drive-secure-label.md) | Update a Drive file/document secure label; downgrade approval errors require opening the document UI |

## API Resources

```javascript
lark_api_search({ query: 'drive <resource> <method>' })  // MUST check parameter structure before calling any API
lark_api({ tool: 'drive', op: '<resource>_<method>', args: { ... } })  // Call API
```

> **Important**: when using native APIs, MUST run `lark_api_search` first to check `data` / `params` parameter structure — do NOT guess field formats.

### files

  - `files_copy` — Copy a file
  - `files_create_folder` — Create a folder
  - `files_list` — List contents of a folder
  - `files_patch` — Modify file title

### file.comments

  - `file_comments_batch_query` — Bulk query comments
  - `file_comments_create_v2` — Add a whole-document or inline (selection) comment
  - `file_comments_list` — Paginated retrieval of document comments
  - `file_comments_patch` — Resolve/restore a comment

### file.comment.replys

  - `file_comment_replys_create` — Add a reply
  - `file_comment_replys_delete` — Delete a reply
  - `file_comment_replys_list` — Get replies
  - `file_comment_replys_update` — Update a reply

### permission.members

  - `permission_members_auth`
  - `permission_members_create` — Add collaborator permission
  - `permission_members_transfer_owner`

### metas

  - `metas_batch_query` — Get document metadata

### user

  - `user_remove_subscription` — Unsubscribe from user/app-level events
  - `user_subscription` — Subscribe to user/app-level events (currently: comment add event)
  - `user_subscription_status` — Query the subscription status of a user/app for a specific event

### file.statistics

  - `file_statistics_get` — Get file statistics

### file.view_records

  - `file_view_records_list` — Get document visitor records

### file.comment.reply.reactions

  - `file_comment_reply_reactions_update_reaction` — Add/delete a reaction

## Permissions Table

| Method | Required Scope |
|--------|---------------|
| `files_copy` | `docs:document:copy` |
| `files_create_folder` | `space:folder:create` |
| `files_list` | `space:document:retrieve` |
| `files_patch` | `docx:document:write_only` |
| `file_comments_batch_query` | `docs:document.comment:read` |
| `file_comments_create_v2` | `docs:document.comment:create` |
| `file_comments_list` | `docs:document.comment:read` |
| `file_comments_patch` | `docs:document.comment:update` |
| `file_comment_replys_create` | `docs:document.comment:create` |
| `file_comment_replys_delete` | `docs:document.comment:delete` |
| `file_comment_replys_list` | `docs:document.comment:read` |
| `file_comment_replys_update` | `docs:document.comment:update` |
| `permission_members_auth` | `docs:permission.member:auth` |
| `permission_members_create` | `docs:permission.member:create` |
| `permission_members_transfer_owner` | `docs:permission.member:transfer` |
| `permission_public_get` | `docs:permission.setting:read` |
| `permission_public_patch` | `docs:permission.setting:write_only` |
| `metas_batch_query` | `drive:drive.metadata:readonly` |
| `user_remove_subscription` | `docs:event:subscribe` |
| `user_subscription` | `docs:event:subscribe` |
| `user_subscription_status` | `docs:event:subscribe` |
| `file_statistics_get` | `drive:drive.metadata:readonly` |
| `file_view_records_list` | `drive:file:view_record:readonly` |
| `file_comment_reply_reactions_update_reaction` | `docs:document.comment:create` |
