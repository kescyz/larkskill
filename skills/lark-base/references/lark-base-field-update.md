# field-update

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Update an existing field.

## Recommended call

Update a select field:

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields/{field_id}
- body:
  ```json
  {
    "name": "Status",
    "type": "select",
    "multiple": false,
    "options": [
      {"name": "Todo", "hue": "Blue", "lightness": "Lighter"},
      {"name": "Doing", "hue": "Orange", "lightness": "Light"},
      {"name": "Done", "hue": "Green", "lightness": "Light"}
    ]
  }
  ```

Update a user field with description:

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields/{field_id}
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
| `field_id` | Yes | Field ID or field name (path param) |
| `name` | Yes | Field name (body) |
| `type` | Yes | Field type (body) |

## API request details

```
PUT /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields/{field_id}
```

## JSON body specification

- Body must be a **JSON object**; pass field definitions directly at the top level.
- The update semantics is `PUT` (full field configuration update); do not pass only scattered fragments. At minimum, explicitly include `name`, `type`, and fill in the key configuration required for that type.
- To add a field description, pass `description` directly; supports plain text and Markdown links.
- `select` update: `options` is still passed as an object array; avoid mixing in invalid fields.
- `link` update restrictions:
  - Cannot change a non-`link` field to `link`, and cannot change a `link` field to non-`link`.
  - The `bidirectional` setting of an existing `link` field cannot be changed.

## Response highlights

- Returns `field` and `updated: true`.

## Workflow

1. Recommended to use `field-get` to fetch current state first, then make minimal modifications.
2. Read the corresponding guide before updating `formula/lookup` type fields.

## Pitfalls

- This is a full field attribute update (PUT semantics), not a patch.
- This is a write operation; confirm with the user before execution.
- When `type` is `formula` or `lookup`, read the corresponding guide before executing.

## References

- [lark-base-field.md](lark-base-field.md) - field index page
- [lark-base-field-get.md](lark-base-field-get.md) - get field details
- [lark-base-shortcut-field-properties.md](lark-base-shortcut-field-properties.md) - shortcut field JSON spec (recommended)
- [formula-field-guide.md](formula-field-guide.md) - formula guide (must read before updating formulas)
- [lookup-field-guide.md](lookup-field-guide.md) - lookup guide (must read before updating lookup references)
