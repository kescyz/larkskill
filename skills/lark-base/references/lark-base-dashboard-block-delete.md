# dashboard-block-delete

> **Prerequisite:** Read [lark-base-dashboard.md](lark-base-dashboard.md) for the overall workflow.

Delete a block from a dashboard. This action is irreversible.

## Recommended call

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks/{block_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `dashboard_id` | Yes | Dashboard ID (path param) |
| `block_id` | Yes | Block ID (path param) |

## API request details

```
DELETE /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks/{block_id}
```

## Key return fields

| Field | Description |
|-------|-------------|
| `block_id` | Deleted block ID |
| `deleted` | `true` if deletion succeeded |

## Pitfalls

- This is a **write operation and irreversible** — confirm with the user before execution.

## References

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard module guide
- [lark-base-dashboard-block-list.md](lark-base-dashboard-block-list.md) — list blocks to confirm target
