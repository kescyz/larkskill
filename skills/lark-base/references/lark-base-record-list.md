# record-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

List records in a table with pagination; optionally filter by view.

## Recommended call

All records (first page):

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records
- params:
  ```json
  { "offset": 0, "limit": 100 }
  ```

Filter by view:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records
- params:
  ```json
  { "view_id": "viw_xxx", "offset": 0, "limit": 50 }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `view_id` | No | View ID; when passed, returns only records visible in that view (query param) |
| `offset` | No | Paging offset, default `0` (query param) |
| `limit` | No | Page size, default `100`, range `1-200` (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records
```

## Key return fields

- Returns `items` (record list), `offset`, `limit`, `total`.

## Pitfalls

- `record-list` does not support concurrent calls; multiple views or tables must be fetched serially.
- `limit` maximum is `200`; passing a higher value will cause an error.
- For complex filters, configure a view first and then fetch with `view_id`.

## References

- [lark-base-record.md](lark-base-record.md) — record index page
- [lark-base-view-set-filter.md](lark-base-view-set-filter.md) — set view filter
