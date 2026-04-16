# docs +whiteboard-update (Update Lark whiteboard)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Update whiteboard content in a Lark document.
You must provide whiteboard token and whiteboard DSL input.
For DSL design and usage patterns, see [`../lark-whiteboard/SKILL.md`](../../lark-whiteboard/SKILL.md).

## Recommended call

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/board/v1/whiteboards/{whiteboard_id}/nodes/batch_create
- body:
  {
    "nodes": [ ... whiteboard node objects ... ]
  }
```

To overwrite (delete existing content first):
```
Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/board/v1/whiteboards/{whiteboard_id}/nodes/batch_delete
- body:
  {
    "node_ids": ["<NODE_ID_1>", "<NODE_ID_2>"]
  }
```

## API request details

```
POST   /open-apis/board/v1/whiteboards/{whiteboard_id}/nodes/batch_create
DELETE /open-apis/board/v1/whiteboards/{whiteboard_id}/nodes/batch_delete
GET    /open-apis/board/v1/whiteboards/{whiteboard_id}/nodes
```

## Parameters

| Parameter | Required | Description |
|------|----------|-------------|
| `whiteboard_id` | Yes (path) | Whiteboard token to update. You must have edit permission on the source document |
| `nodes` | Yes (body) | Array of whiteboard node objects per whiteboard DSL |

## Example

No inline example here. Refer to [`../lark-whiteboard/SKILL.md`](../../lark-whiteboard/SKILL.md) for full end-to-end flow.
