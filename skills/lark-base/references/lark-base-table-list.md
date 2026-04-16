# table-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

List tables in a Base with pagination.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables
- params:
  ```json
  { "offset": 0, "limit": 50 }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `offset` | No | Paging offset, default `0` (query param) |
| `limit` | No | Paging size, default `50`, range `1-100` (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables
```

## Key return fields

- Returns `items / offset / limit / count / total`.
- `items` contain `table_id` and `table_name`.

## Pitfalls

- ⚠️ `table-list` does not support concurrency. For multiple Bases, run sequentially.

## References

- [lark-base-table.md](lark-base-table.md) — table index page
