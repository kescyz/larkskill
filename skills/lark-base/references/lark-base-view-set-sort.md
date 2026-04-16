# view-set-sort

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Update the sort configuration of a view.

## Recommended call

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}/sort
- body:
  ```json
  [
    { "field": "fld_priority", "desc": true }
  ]
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `view_id` | Yes | View ID or view name (path param) |
| body | Yes | Array of sort config items (body) |

## API request details

```
PUT /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}/sort
```

## Key return fields

- Returns the updated sort configuration.

## Structure rules

- Body is an array (`sort_config`), length `0–10`.
- Each item:
  - `field`: field ID or field name, length `1–100`
  - `desc`: optional, default `false`
- Pass the array directly at the top level of the body.

## JSON Schema

```json
{"type":"array","items":{"type":"object","properties":{"field":{"type":"string","minLength":1,"maxLength":100,"description":"Field id or name"},"desc":{"type":"boolean","default":false,"description":"define how to sort records"}},"required":["field"],"additionalProperties":false},"minItems":0,"maxItems":10,"$schema":"http://json-schema.org/draft-07/schema#"}
```

## Workflow

1. Prefer field IDs over names to avoid issues with duplicate or renamed fields.

## Pitfalls

- This is a write operation; confirm with the user before execution.
- Sorting only supported on `grid`, `kanban`, `gallery`, `gantt` views.
- `sort_config` max 10 items; exceeding this will cause a failure.

## References

- [lark-base-view.md](lark-base-view.md) — view index page
- [lark-base-view-get-sort.md](lark-base-view-get-sort.md) — read sort
