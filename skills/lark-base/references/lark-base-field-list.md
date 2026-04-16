# field-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

List the fields under a table in pages.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields
- params:
  ```json
  { "offset": 0, "limit": 100 }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `offset` | No | Paging offset, default `0` (query param) |
| `limit` | No | Paging size, default `100`, range `1-200` (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields
```

## Response highlights

- Returns the field list and `offset / limit / count / total`.

## Pitfalls

- ⚠️ Concurrent calls are prohibited; batch listing of multiple table fields must be done serially.

## References

- [lark-base-field.md](lark-base-field.md) — field index page
