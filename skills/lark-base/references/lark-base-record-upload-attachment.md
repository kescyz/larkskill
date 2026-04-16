# record-upload-attachment

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Upload a local file to the current Base and write it into the attachment field of the specified record.

## Recommended call

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}/attachment
- body:
  ```json
  {
    "field_id": "fld_attach",
    "file_path": "./report.pdf"
  }
  ```

With custom display name:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}/attachment
- body:
  ```json
  {
    "field_id": "attachment",
    "file_path": "./report.pdf",
    "name": "Q1-final.pdf"
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `record_id` | Yes | Record ID (path param) |
| `field_id` | Yes | Attachment field ID or field name (body) |
| `file_path` | Yes | Local file path, maximum 20 MB (body) |
| `name` | No | Display name in the attachment field; defaults to the local filename (body) |

## Workflow

This is a write operation. If the user has clearly stated they want to upload to an attachment field of a record, proceed directly. If `record_id` or the target field is still ambiguous, confirm first.

## Pitfalls

- The target field must be of type `attachment`.

## References

- [lark-base-record.md](lark-base-record.md) — record index page
- [lark-base-shortcut-record-value.md](lark-base-shortcut-record-value.md) — record value format reference
