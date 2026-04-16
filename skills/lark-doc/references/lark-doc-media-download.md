# docs +media-download (Download doc media / whiteboard thumbnail)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Download image/file media (`file_token`) from docs, or whiteboard thumbnail (`whiteboard_id`).

## Recommended call — Download image/file media

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/medias/{file_token}/download
```

## Recommended call — Download whiteboard thumbnail

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/board/v1/whiteboards/{whiteboard_id}/nodes
```

## API request details

```
GET /open-apis/drive/v1/medias/{file_token}/download       (media: image/file)
GET /open-apis/board/v1/whiteboards/{whiteboard_id}/nodes  (whiteboard thumbnail)
```

## Parameters

| Parameter | Required | Description |
|------|----------|-------------|
| `file_token` | Yes (for media) | Resource token: obtained from `<image token="...">` or `<file token="...">` tags in fetched doc content |
| `whiteboard_id` | Yes (for whiteboard) | Whiteboard ID: obtained from `<whiteboard token="..."/>` tag in fetched doc content |

## Where token comes from

When parsing doc content from `+fetch`, tags may include:

- Image: `<image token="..." .../>`
- File: `<file token="..." name="..."/>`
- Whiteboard: `<whiteboard token="..."/>`

## References

- [lark-doc-fetch](lark-doc-fetch.md)
- [lark-shared](../../lark-shared/SKILL.md)
