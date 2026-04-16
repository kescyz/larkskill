# view-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

List views under a table with pagination.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views
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
| `limit` | No | Page size, default `100`, range `1-200` (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views
```

## Key return fields

- Returns `items` (view list), `offset`, `limit`, `count`, `total`.

## Pitfalls

- `view-list` does not support concurrent calls; listing views for multiple tables must be done serially.

## References

- [lark-base-view.md](lark-base-view.md) — view index page
