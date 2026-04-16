# drive +upload

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Upload a local file to Lark Drive.

## Recommended call — Upload file (≤20MB)

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/medias/upload_all
- body:
  {
    "file_name": "report.pdf",
    "parent_type": "explorer",
    "parent_node": "<FOLDER_TOKEN>",
    "size": <FILE_SIZE_BYTES>
  }
```

Returns `file_token`.

## Recommended call — Multipart upload (>20MB)

Step 1 — Pre-upload:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/files/upload_prepare
- body:
  {
    "file_name": "report.pdf",
    "parent_type": "explorer",
    "parent_node": "<FOLDER_TOKEN>",
    "size": <FILE_SIZE_BYTES>
  }
```

Returns `upload_id` and `block_size`.

Step 2 — Upload parts (repeat for each block):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/files/upload_part
- body:
  {
    "upload_id": "<UPLOAD_ID>",
    "seq": 0,
    "size": <BLOCK_SIZE>
  }
```

Step 3 — Complete upload:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/files/upload_finish
- body:
  {
    "upload_id": "<UPLOAD_ID>",
    "block_num": <TOTAL_BLOCKS>
  }
```

## API request details

```
POST /open-apis/drive/v1/medias/upload_all        (≤20MB, simple upload)
POST /open-apis/drive/v1/files/upload_prepare      (>20MB, step 1)
POST /open-apis/drive/v1/files/upload_part         (>20MB, step 2)
POST /open-apis/drive/v1/files/upload_finish       (>20MB, step 3)
```

## Parameters (upload_all body)

| Field | Required | Description |
|------|----------|-------------|
| `file_name` | Yes | File name |
| `parent_type` | Yes | Parent node type, e.g. `"explorer"` |
| `parent_node` | Yes | Parent folder token |
| `size` | Yes | File size in bytes |

> [!IMPORTANT]
> If the file is created with app identity (bot), the agent should keep bot identity and try to grant `full_access` to the current available user identity by default.
>
> Recommended flow:
> 1. Call `GET /open-apis/contact/v3/users/me` to get current user `open_id`.
> 2. Switch back to bot identity and grant `full_access` to that `open_id` on the uploaded file via `POST /open-apis/drive/v1/permissions/{token}/members`.
>
> If no local user identity is available, explicitly state that authorization was not completed.
>
> In result output, besides `file_token`, explicitly report authorization status:
> - Success: current user has admin permission on this file.
> - No local user identity: authorization not completed.
> - Authorization failed: file upload succeeded, permission grant failed, include reason and next-step guidance.
>
> **Do not transfer owner automatically.** Get explicit confirmation first.

> [!CAUTION]
> This is a **write operation**. Confirm user intent before execution.

## References

- [lark-drive](../SKILL.md) - All Drive commands
- [lark-shared](../../lark-shared/SKILL.md) - Authentication and global parameters
