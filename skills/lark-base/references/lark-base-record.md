# base record operations

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

Index of record-related MCP `lark_api` calls.

## Operation navigation

| Reference doc | Operation | Description |
|---------------|-----------|-------------|
| [lark-base-record-list.md](lark-base-record-list.md) | `record-list` | Paginated record retrieval |
| [lark-base-record-get.md](lark-base-record-get.md) | `record-get` | Get a single record |
| [lark-base-record-upsert.md](lark-base-record-upsert.md) | `record-upsert` | Create or update records |
| [lark-base-record-upload-attachment.md](lark-base-record-upload-attachment.md) | `record-upload-attachment` | Upload a local file to an attachment field and update the record |
| [lark-base-record-delete.md](lark-base-record-delete.md) | `record-delete` | Delete a record |

## Notes

- This index page is directory-only. For detailed call signatures, read the corresponding single-operation doc.
- All list calls must run sequentially. If you need multiple list requests, run them one by one.
- Read [lark-base-shortcut-record-value.md](lark-base-shortcut-record-value.md) before constructing any record write JSON body.
- When writing local files to an attachment field, the `record-upload-attachment` multi-step flow is mandatory — do not attempt to pass a file path directly in a record upsert body.
