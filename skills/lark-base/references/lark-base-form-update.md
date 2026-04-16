# form-update

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Update the name or description of a specified form in a Base table.

## Recommended call

Update name only:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}
- body:
  ```json
  { "name": "New Form Name" }
  ```

Update description only:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}
- body:
  ```json
  { "description": "New description content" }
  ```

Update both name and description:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}
- body:
  ```json
  {
    "name": "New Form Name",
    "description": "New description, [Learn more](https://example.com)"
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (path param) |
| `form_id` | Yes | Form ID (path param) |
| `name` | No | New form name (body) |
| `description` | No | New form description — plain text or Markdown link e.g. `[Text](https://example.com)` (body) |

> Pass at least one of `name` or `description`; otherwise no actual change is made.

## Key return fields

```json
{
  "data": {
    "id": "vewX58te9D",
    "name": "New Form Name",
    "description": "New description content"
  }
}
```

## Workflow

> This is a **write operation**; confirm with the user before execution.

1. Confirm `form_id` (available via `form-list`).
2. Confirm the fields to modify.
3. Execute and report the updated values.

## References

- [lark-base-form-list.md](lark-base-form-list.md) — List forms to find `form_id`
- [lark-base-form-get.md](lark-base-form-get.md) — Get current form details
