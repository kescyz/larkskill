# dashboard-list

> **Prerequisite:** Read [lark-base-dashboard.md](lark-base-dashboard.md) for the overall workflow.

List all dashboards under a Base with pagination.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/dashboards
- params:
  ```json
  { "page_size": 20 }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `page_size` | No | Page size (query param) |
| `page_token` | No | Pagination token from previous response (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/dashboards
```

## Key return fields

| Field | Description |
|-------|-------------|
| `items` | Dashboard list; each item has `dashboard_id` and `name` |
| `total` | Total count |
| `has_more` | `true` if more pages exist; use `page_token` to continue |

## Pitfalls

- `dashboard-list` does not support concurrent calls; multiple Bases must be listed serially.

## References

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard module guide
