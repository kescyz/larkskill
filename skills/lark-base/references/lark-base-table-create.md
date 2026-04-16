# table-create

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

Create a table, and optionally create fields and views.

## Recommended call

Minimal (name only):

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables
- body:
  ```json
  {
    "name": "Customer list"
  }
  ```

With fields and view:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables
- body:
  ```json
  {
    "name": "Project Management",
    "fields": [{"name": "Project name", "type": "text"}],
    "view": [{"name": "Default table", "type": "grid"}]
  }
  ```

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `name` | Yes | New table name |
| `fields` | No | Field JSON array |
| `view` | No | View JSON object or array |

## API request details

```
POST /open-apis/base/v3/bases/{base_token}/tables
```

Note: If `fields` or `view` are provided, additional field/view API calls may be needed as separate steps after table creation.

## Key return fields

- Returns at least `table`.
- When `fields` / `view` is provided, response also includes `fields` / `views`.

## Workflow

1. Start with only `name` to create an empty table.
2. If field/view params are complex, create the table first then add fields/views separately.

## Pitfalls

- ⚠️ This is a write operation and must be confirmed before execution.
- ⚠️ The first element in `fields` updates the system default first column. Subsequent elements are newly added fields.
- ⚠️ Do not update the same table in parallel to avoid race conditions.

## References

- [lark-base-table.md](lark-base-table.md) — table index page
- [lark-base-field-create.md](lark-base-field-create.md) — Create fields
- [lark-base-view-create.md](lark-base-view-create.md) — Create views
