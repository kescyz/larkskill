# dashboard-block-list

> **Prerequisite:** Read [lark-base-dashboard.md](lark-base-dashboard.md) for the overall workflow.

List all blocks in a dashboard with pagination.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks
- params:
  ```json
  { "page_size": 20 }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `dashboard_id` | Yes | Dashboard ID (path param) |
| `page_size` | No | Page size, default `20`, max `100` (query param) |
| `page_token` | No | Pagination token from previous response (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks
```

## Key return fields

| Field | Description |
|-------|-------------|
| `items` | Block list; each item has `block_id`, `name`, `type` |
| `total` | Total block count |
| `has_more` | `true` if more pages exist; use `page_token` to continue |

## Pitfalls

- `dashboard-block-list` does not support concurrent calls; batch calls must be serial.

## References

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard module guide
- [lark-base-dashboard-block-get.md](lark-base-dashboard-block-get.md) — get detailed block config
