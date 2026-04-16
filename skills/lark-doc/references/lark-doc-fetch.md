# docs +fetch

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Fetch document content as Markdown text.

## Recommended call

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/docx/v1/documents/{document_id}/raw_content
- params: { "lang": 0 }
```

For paginated fetch of large documents:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/docx/v1/documents/{document_id}/blocks
- params: { "page_size": 50, "page_token": "<PAGE_TOKEN>" }
```

## API request details

```
GET /open-apis/docx/v1/documents/{document_id}/raw_content
GET /open-apis/docx/v1/documents/{document_id}/blocks
```

## Parameters

| Parameter | Required | Description |
|------|------|------|
| `document_id` | Yes (path) | Document ID (extracted from URL or returned by create) |
| `lang` | No (query) | Language for content (0=default) |
| `page_size` | No (query) | Number of blocks per page for block-level fetch |
| `page_token` | No (query) | Pagination token |

## Response highlights

- `content`: Markdown text representation of the document
- For block-level fetch: `items[]` array of block objects, `has_more`, `page_token`

## Media tokens in fetched content

When parsing doc content, the fetched markdown may contain tags including:

  ```html
  <image token="Z1FjxxxxxxxxxxxxxxxxxxxtnAc" width="1833" height="2491" align="center"/>
  ```

  ```html
  <view type="1">
    <file token="Z1FjxxxxxxxxxxxxxxxxxxxtnAc" name="skills.zip"/>
  </view>
  ```

  ```html
  <whiteboard token="Z1FjxxxxxxxxxxxxxxxxxxxtnAc"/>
  ```

To download the media referenced by these tokens, use `+media-download`:

   ```
   Use lark-doc-media-download with --token "Extracted token" --output ./downloaded_media
   ```

## References

- [lark-doc](../SKILL.md) — All Docs operations
- [lark-doc-media-download](lark-doc-media-download.md) — Download media from doc
- [lark-shared](../../lark-shared/SKILL.md) — Authentication and global parameters
