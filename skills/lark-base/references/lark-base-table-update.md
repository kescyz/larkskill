# table-update

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

Rename a table.

## Recommended call

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}
- body:
  ```json
  {
    "name": "key customer list"
  }
  ```

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `name` | Yes | New table name |

## API request details

```
PATCH /open-apis/base/v3/bases/{base_token}/tables/{table_id}
```

## Key return fields

- Returns `table` and `updated: true`.
- Currently only supports updating name.

## Workflow

1. Prefer `table-get` first to confirm the target table.

## Pitfalls

- ⚠️ This is a write operation and must be confirmed before execution.

## References

- [lark-base-table.md](lark-base-table.md) — table index page
- [lark-base-table-get.md](lark-base-table-get.md) — get table details
