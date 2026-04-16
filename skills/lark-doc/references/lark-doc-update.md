# docs +update

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Update document content. Supports append, replace, insert before/after, delete, and overwrite modes.

## Recommended call — Append content

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
- body:
  {
    "children": [ ... block objects ... ],
    "index": -1
  }
```

## Recommended call — Replace/update a block

```
Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}
- body:
  {
    "update_text_elements": {
      "elements": [ ... ]
    }
  }
```

## Recommended call — Delete a block

```
Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
- body:
  {
    "start_index": 0,
    "end_index": 1
  }
```

## API request details

```
GET    /open-apis/docx/v1/documents/{document_id}/blocks                        (list blocks)
POST   /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children    (insert blocks)
PATCH  /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}             (update block)
DELETE /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children    (delete blocks)
PATCH  /open-apis/docx/v1/documents/{document_id}                               (update doc title)
```

## Update modes

| Mode | Description | MCP call |
|------|-------------|----------|
| `append` | Append content to end | POST blocks children with `index: -1` |
| `replace_range` | Replace content in a range | GET blocks to find target, PATCH block |
| `insert_before` | Insert before a target block | POST blocks children with specific index |
| `insert_after` | Insert after a target block | POST blocks children with index+1 |
| `delete_range` | Delete a range of blocks | DELETE blocks children |
| `overwrite` | Replace all content | Delete all blocks, then insert new content |

## Response highlights

Success response:
```json
{
  "success": true,
  "doc_id": "Document ID",
  "mode": "Mode used",
  "board_tokens": ["Optional: newly created whiteboard token list"],
  "message": "Document updated successfully (xxx mode)",
  "warnings": ["optional warning list"],
  "log_id": "Request log ID"
}
```

Async response (for large operations):
```json
{
  "task_id": "async_task_xxxx",
  "message": "The document update has been submitted for asynchronous processing",
  "log_id": "Request log ID"
}
```

Error response:
```json
{
  "error": "[Error code] Error message\nSuggestion: Repair suggestions\nContext: Context information",
  "log_id": "Request log ID"
}
```

## Typical scenarios

### Append content

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
- body:
  {
    "children": [{ "block_type": 2, "text": { "elements": [{"text_run": {"content": "New chapter content"}}] } }],
    "index": -1
  }
```

### Replace content by block ID

```
Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}
- body:
  {
    "update_text_elements": {
      "elements": [{"text_run": {"content": "New title content"}}]
    }
  }
```

### Delete content by block ID

```
Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
- body: { "start_index": 0, "end_index": 1 }
```

### Append blank whiteboard

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
- body:
  {
    "children": [{ "block_type": 22, "board": {} }],
    "index": -1
  }
```

### Update document title

```
Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/docx/v1/documents/{document_id}
- body:
  {
    "title": { "elements": [{"text_run": {"content": "Documentation v2.0"}}] }
  }
```

## References

- [lark-doc](../SKILL.md) — All Docs operations
- [lark-doc-create](lark-doc-create.md) — Create document
- [lark-doc-fetch](lark-doc-fetch.md) — Fetch document content
- [lark-shared](../../lark-shared/SKILL.md) — Authentication and global parameters
