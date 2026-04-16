# field-create

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Create a field.

## Agent minimal workflow

1. First determine whether it is `formula` / `lookup`.
2. If yes: read the corresponding guide first.
3. Do not create formula / lookup fields directly without reading the guide.
4. After reading the guide, construct the body JSON and create the field.
5. If it is a cross-table formula / lookup, also check the **target table** schema.

## Recommended call

Simple number field:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields
- body:
  ```json
  {
    "name": "Budget",
    "type": "number",
    "precision": 2
  }
  ```

Select field with options:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields
- body:
  ```json
  {
    "name": "Status",
    "type": "select",
    "multiple": false,
    "options": [
      {"name": "Todo", "hue": "Blue", "lightness": "Lighter"},
      {"name": "Done", "hue": "Green", "lightness": "Light"}
    ]
  }
  ```

User field with description:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields
- body:
  ```json
  {
    "name": "Owner",
    "type": "user",
    "multiple": false,
    "description": "Marks the direct owner of the record; see [Team Field Conventions](https://example.com/field-spec) for collaboration guidelines"
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `name` | Yes | Field name (body) |
| `type` | Yes | Field type (body) |
| `description` | No | Plain text or Markdown links (body) |

## API request details

```
POST /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields
```

## JSON body specification

- Body must be a **JSON object**; pass field definitions directly at the top level without nesting.
- Top level must contain at minimum: `name`, `type`.
- To add a field description, pass `description` directly; supports plain text and Markdown links.
- Different `type` values require different sub-fields:
  - `select`: use `multiple` + `options` (only pass `name/hue/lightness` in `options`, do not pass `id`).
  - `link`: must have `link_table`, optionally `bidirectional`, `bidirectional_link_field_name`.
  - `formula`: must have `expression`; read the formula guide first, then create.
  - `lookup`: must have `from`, `select`, `where`; read the lookup guide first, then create.

## Response highlights

- Returns `field` and `created: true`.

## Workflow

1. For formula / lookup fields, you must read the corresponding guide first; do not create directly without reading it.

## Pitfalls

- This is a write operation; confirm with the user before execution.
- When `type` is `formula` or `lookup`, read the corresponding guide first, then create.

## References

- [lark-base-field.md](lark-base-field.md) - field index page
- [lark-base-shortcut-field-properties.md](lark-base-shortcut-field-properties.md) - shortcut field JSON spec (recommended)
- [formula-field-guide.md](formula-field-guide.md) - formula guide (must read when creating formulas)
- [lookup-field-guide.md](lookup-field-guide.md) - lookup guide (must read when creating lookup references)
