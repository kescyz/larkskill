# record-get

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Get a single record, optionally filtering the returned fields.

## Recommended call

Full record:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}

Specific fields only:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}
- params:
  ```json
  { "fields": ["Project Name", "Status"] }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `record_id` | Yes | Record ID (path param) |
| `fields` | No | Field name array; limits which fields are returned (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}
```

## Key return fields

- Returns `record` containing the field values.

## References

- [lark-base-record.md](lark-base-record.md) — record index page
- [lark-base-record-list.md](lark-base-record-list.md) — list records
