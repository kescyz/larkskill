# view-get

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Get basic information about a view.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `view_id` | Yes | View ID or view name (path param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}
```

## Key return fields

- Returns the view's base configuration.

## References

- [lark-base-view.md](lark-base-view.md) — view index page
- [lark-base-view-list.md](lark-base-view-list.md) — list views
