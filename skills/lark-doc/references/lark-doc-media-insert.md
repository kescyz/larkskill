# docs +media-insert (Insert image/file at document end)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Insert local image/file at the **end** of a document. Combines three steps: create block, upload file, set token.

## Full flow

Step 1 — Create an image or file block at the end of the document:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
- body:
  {
    "children": [
      {
        "block_type": 27,
        "image": {}
      }
    ],
    "index": -1
  }
```

Step 2 — Upload the media file:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/medias/upload_all
- body:
  {
    "file_name": "image.png",
    "parent_type": "docx_image",
    "parent_node": "<DOCUMENT_ID>",
    "size": <FILE_SIZE_BYTES>
  }
```

Returns `file_token`.

Step 3 — Set the block's file token:
```
Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}
- body:
  {
    "update_image": {
      "token": "<FILE_TOKEN>"
    }
  }
```

## API request details

```
POST  /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
POST  /open-apis/drive/v1/medias/upload_all
PATCH /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}
```

## Parameters

| Parameter | Required | Description |
|------|----------|-------------|
| `document_id` | Yes | Document ID or docx URL. Auto extraction supports only `/docx/<document_id>`; `/wiki/...` auto extraction is not supported |
| file path | Yes | Local file path (max 20MB) |
| `block_type` | No | `27` = image, `23` = file |
| `align` | No | For image only: `1`=left, `2`=center (default), `3`=right |
| `caption` | No | For image only: caption text |

> [!IMPORTANT]
> If previous step is [`lark-doc-create`](lark-doc-create.md) and returned `doc_url` is `/wiki/...`, pass `doc_id` instead of that `doc_url`.

## Output

Success response includes: `document_id`, `block_id`, `file_token`, `file_name`, `type`.

> [!CAUTION]
> This is a **write operation**. Confirm user intent before executing.

## References

- [lark-doc-fetch](lark-doc-fetch.md)
- [lark-shared](../../lark-shared/SKILL.md)
