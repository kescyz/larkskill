# drive +add-comment

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Add comments to documents.
Uses `POST /open-apis/drive/v1/files/{file_token}/comments` (create_v2).
- If no position is provided, it creates a full-document comment (no `anchor`).
- If `block_id` is provided, it creates a local comment with `anchor.block_id`.

Supports docx URL/token, legacy doc URL (full comment only), and wiki URL that resolves to doc/docx.

## Recommended call — Full-document comment

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/files/{file_token}/comments
- params: { "file_type": "docx" }
- body:
  {
    "reply_elements": [
      { "type": "text", "text": "Please add release notes" }
    ]
  }
```

## Recommended call — Local (inline) comment with block_id

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/files/{file_token}/comments
- params: { "file_type": "docx" }
- body:
  {
    "anchor": { "block_id": "<BLOCK_ID>" },
    "reply_elements": [
      { "type": "text", "text": "Comment content" }
    ]
  }
```

## Recommended call — Comment with @mention and link elements

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/files/{file_token}/comments
- params: { "file_type": "docx" }
- body:
  {
    "reply_elements": [
      { "type": "text", "text": "Please " },
      { "type": "mention_user", "text": "ou_xxx" },
      { "type": "text", "text": " review, refer to " },
      { "type": "link", "text": "https://example.com" }
    ]
  }
```

## API request details

```
POST /open-apis/drive/v1/files/{file_token}/comments
```

## Parameters

| Parameter | Required | Description |
|------|----------|-------------|
| `file_token` | Yes (path) | Document token |
| `file_type` | Yes (query) | Document type: `docx` or `doc` |
| `reply_elements` | Yes (body) | Array of comment content elements |
| `anchor.block_id` | No (body) | For local comment: target block ID. Omit for full-document comment |

### Supported element types

| `type` | Description |
|--------|-------------|
| `text` | Plain text |
| `mention_user` | @user (value is `open_id`) |
| `link` | Hyperlink |

## Behavior notes

- Full comments support `docx`, legacy `doc` URL, and wiki URLs resolving to `doc`/`docx`.
- Local comments only support `docx` and wiki URLs resolving to `docx`.
- For wiki URLs: first resolve real `file_token` via `GET /open-apis/wiki/v2/spaces/get_node`.

> [!CAUTION]
> This is a **write operation**. Confirm user intent before execution.

## References

- [lark-drive](../SKILL.md) - All Drive commands
- [lark-shared](../../lark-shared/SKILL.md) - Authentication and global parameters
