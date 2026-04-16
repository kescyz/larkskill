# field-search-options

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

Search candidates for single/multi-select fields.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields/{field_id}/options
- params:
  ```json
  { "query": "completed", "offset": 0, "limit": 30 }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `field_id` | Yes | Field ID or field name (path param) |
| `query` | No | Query keyword (query param) |
| `offset` | No | Paging offset, default `0` (query param) |
| `limit` | No | Paging size, default `30` (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields/{field_id}/options
```

## Response highlights

- Returns `options`, `total`, and the echoed `field_id / field_name / keyword`.

## Pitfalls

- ⚠️ Only available for fields with option sets; normal text/number fields have no searchable options.

## References

- [lark-base-field.md](lark-base-field.md) — field index page
