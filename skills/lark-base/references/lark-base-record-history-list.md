# record-history-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Query the change history of a specific record.

## Recommended call

Latest page:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/record_history
- params:
  ```json
  { "table_id": "tbl_xxx", "record_id": "rec_xxx" }
  ```

With pagination:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/record_history
- params:
  ```json
  { "table_id": "tbl_xxx", "record_id": "rec_xxx", "page_size": 30, "max_version": 123456 }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (query param) |
| `record_id` | Yes | Record ID (query param) |
| `page_size` | No | Items per page, default `30`, max `50` (query param) |
| `max_version` | No | Pagination cursor; use `next_max_version` from previous response (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/record_history
```

## Key return fields

- Returns history entries in descending version order (newest first).
- Each entry includes: `rev` (version), `operator`, `create_time` (Unix seconds), `activity_type`, `field_changes`.
- `field_changes` includes: field ID, field name, field type, `before` value, `after` value.

### activity_type values

| Value | Meaning |
|-------|---------|
| `create` | Record created |
| `update` | Record edited |
| `delete` | Record deleted |

### Field types not tracked in history

Changes to these field types do **not** appear in `field_changes`:
- Calculated fields: formula, lookup
- System fields: auto-number, creation time, creator, last modified time, last modifier

## Pagination workflow

1. First request: omit `max_version` to get the latest page.
2. Check `has_more` in the response.
3. If `has_more = true`, use the returned `next_max_version` as the `max_version` for the next request.
4. Stop when `has_more = false`.

## Workflow

1. Confirm that `table_id` and `record_id` belong to the same table.
2. Fetch the latest page first, then paginate using the workflow above.

## Pitfalls

- `record-history-list` does not support concurrent calls; batch execution must be serial.
- Only single-record history is supported; full-table history scan is not available.

## References

- [lark-base-history.md](lark-base-history.md) — history index page
- [lark-base-record.md](lark-base-record.md) — record index page
