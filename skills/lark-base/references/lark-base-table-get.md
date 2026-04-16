# table-get

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

Get aggregated table info: table metadata, all fields, and all views.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}

Then follow up with fields and views:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}
```

Note: To get the full picture (table + fields + views), make three sequential calls.

## Key return fields

- Table call returns `table` metadata.
- Fields call returns `items` (field list).
- Views call returns `items` (view list).
- Use this to understand table structure before field or view operations.

## Pitfalls

- ⚠️ `table_id` supports passing table names, but prefer `tbl_xxx` IDs in duplicate-name scenarios.

## References

- [lark-base-table.md](lark-base-table.md) — table index page
- [lark-base-field-list.md](lark-base-field-list.md) — list fields
- [lark-base-view-list.md](lark-base-view-list.md) — list views
