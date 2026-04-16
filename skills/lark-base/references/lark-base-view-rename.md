# view-rename

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Rename a view.

## Recommended call

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}
- body:
  ```json
  { "name": "Customer in progress" }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `view_id` | Yes | View ID or view name (path param) |
| `name` | Yes | New view name (body) |

## API request details

```
PATCH /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}
```

## Key return fields

- Returns updated `view` data.

## Pitfalls

- This is a write operation; confirm with the user before execution.

## References

- [lark-base-view.md](lark-base-view.md) — view index page
- [lark-base-view-get.md](lark-base-view-get.md) — get view details
