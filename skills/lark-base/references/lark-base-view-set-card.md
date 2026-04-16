# view-set-card

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Update the card configuration of a view.

## Recommended call

Set cover field:

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}/card
- body:
  ```json
  { "cover_field": "fld_cover" }
  ```

Clear cover field:

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}/card
- body:
  ```json
  { "cover_field": null }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `view_id` | Yes | View ID or view name (path param) |
| body | Yes | Card configuration JSON object (body) |

## API request details

```
PUT /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}/card
```

## Key return fields

- Returns the updated card configuration.

## Structure rules

- `cover_field`: required; field ID or field name, length `1–100`; or `null` to clear
- When not `null`, the field must be an `attachment` field
- Pass `null` to clear the cover configuration

## JSON Schema

```json
{"type":"object","properties":{"cover_field":{"anyOf":[{"type":"string","minLength":1,"maxLength":100,"description":"Field id or name"},{"type":"null"}],"description":"cover field id or name. must be a attachment field"}},"required":["cover_field"],"additionalProperties":false,"$schema":"http://json-schema.org/draft-07/schema#"}
```

## Workflow

1. Pull the current config with `view-get-card` first, then modify.

## Pitfalls

- This is a write operation; confirm with the user before execution.
- Only supported on `gallery` and `kanban` views.
- `cover_field` must be an `attachment` field; text or number fields will cause an error.
- To clear the cover, pass `null` — do not pass an empty string.

## References

- [lark-base-view.md](lark-base-view.md) — view index page
- [lark-base-view-get-card.md](lark-base-view-get-card.md) — read card
