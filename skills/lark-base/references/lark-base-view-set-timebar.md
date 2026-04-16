# view-set-timebar

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Update the timeline configuration of a view.

## Recommended call

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}/timebar
- body:
  ```json
  {
    "start_time": "fld_start",
    "end_time": "fld_end",
    "title": "fld_title"
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `view_id` | Yes | View ID or view name (path param) |
| body | Yes | Timeline configuration JSON object (body) |

## API request details

```
PUT /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}/timebar
```

## Key return fields

- Returns the updated timeline configuration.

## Structure rules

- `start_time`: required, field ID or field name, length `1–100`
- `end_time`: required, field ID or field name, length `1–100`
- `title`: required, field ID or field name, length `1–100`
- `start_time` / `end_time` must be `datetime` / `created_at` type fields; prefer field IDs
- `title` is typically the primary field, used to display the entry title

## JSON Schema

```json
{"type":"object","properties":{"start_time":{"type":"string","minLength":1,"maxLength":100,"description":"start time field id or name (must be a datetime/created_at field)"},"end_time":{"type":"string","minLength":1,"maxLength":100,"description":"end time field id or name (must be a datetime/created_at field)"},"title":{"type":"string","minLength":1,"maxLength":100,"description":"title datasource field id or name"}},"required":["start_time","end_time","title"],"additionalProperties":false,"$schema":"http://json-schema.org/draft-07/schema#"}
```

## Workflow

1. Pull the current config with `view-get-timebar` first, then modify.

## Pitfalls

- This is a write operation; confirm with the user before execution.
- Only supported on `calendar` and `gantt` views.
- `start_time` and `end_time` cannot be text, select, or link fields.
- If the field does not exist or has the wrong type, the call will fail; do not guess field names.

## References

- [lark-base-view.md](lark-base-view.md) — view index page
- [lark-base-view-get-timebar.md](lark-base-view-get-timebar.md) — read timebar
