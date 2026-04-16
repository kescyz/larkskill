# dashboard-delete

> **Prerequisite:** Read [lark-base-dashboard.md](lark-base-dashboard.md) for the overall workflow.

Delete a dashboard (also deletes all blocks within it; irreversible).

## Recommended call

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `dashboard_id` | Yes | Dashboard ID (path param) |

## API request details

```
DELETE /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}
```

## Key return fields

| Field | Description |
|-------|-------------|
| `dashboard_id` | Deleted dashboard ID |
| `deleted` | `true` if deletion succeeded |

## Pitfalls

- This is a **write operation and irreversible** — confirm with the user before execution.
- Deleting a dashboard also deletes all blocks within it; this cannot be undone.

## References

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard module guide
- [lark-base-dashboard-list.md](lark-base-dashboard-list.md) — list dashboards to confirm target
