# view-delete

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Delete a view.

## Recommended call

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `view_id` | Yes | View ID or view name (path param) |

## API request details

```
DELETE /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}
```

## Key return fields

- Returns deletion success status and the target view ID.

## Workflow

1. Prefer confirming the target with `view-get` first.
2. Confirm with the user before deletion.

## Pitfalls

- High-risk irreversible operation; deletion cannot be undone.

## References

- [lark-base-view.md](lark-base-view.md) — view index page
- [lark-base-view-get.md](lark-base-view-get.md) — get view details
