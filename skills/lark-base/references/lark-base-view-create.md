# view-create

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Create one or more views.

## Recommended call

Single view:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views
- body:
  ```json
  { "name": "In Progress", "type": "grid" }
  ```

Multiple views in one request:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views
- body:
  ```json
  [
    { "name": "In Progress", "type": "grid" },
    { "name": "Calendar", "type": "calendar" }
  ]
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| body | Yes | View JSON object or array of objects (body) |

## API request details

```
POST /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views
```

## Key return fields

- Always returns a `views` array even when only one view is created.

## Key rules

- `type` only supports: `grid`, `kanban`, `gallery`, `calendar`, `gantt`.
- `/views` does not accept `type=form`; form creation uses the `/forms` endpoint.
- `name` is required, length `1–100`, and must be unique within the same table.

## JSON Schema

```json
{"type":"object","properties":{"type":{"type":"string","enum":["grid","kanban","gallery","gantt","calendar"],"default":"grid","description":"view type"},"name":{"type":"string","minLength":1,"maxLength":100,"description":"View name"}},"required":["name"],"additionalProperties":false,"$schema":"http://json-schema.org/draft-07/schema#"}
```

## Workflow

1. When creating multiple views in batch, prefer submitting an array in a single request to reduce API calls.

## Pitfalls

- This is a write operation; confirm with the user before execution.

## References

- [lark-base-view.md](lark-base-view.md) — view index page
