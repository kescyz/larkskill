# dashboard-get

> **Prerequisite:** Read [lark-base-dashboard.md](lark-base-dashboard.md) for the overall workflow.

Get dashboard details: name, theme config, and list of all blocks. Common uses: view what blocks a dashboard has; get block IDs for subsequent edit/delete.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `dashboard_id` | Yes | Dashboard ID (path param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}
```

## Key return fields

| Field | Type | Description |
|-------|------|-------------|
| `dashboard_id` | string | Dashboard ID |
| `name` | string | Dashboard name |
| `theme.theme_style` | string | Theme: `default` / `SimpleBlue` / `DarkGreen` / `summerBreeze` / `simplistic` / `energetic` / `deepDark` / `futuristic` |
| `blocks` | array | Each item: `block_id`, `block_name`, `block_type` (e.g. `column` / `line` / `pie`) |

## References

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard module guide
- [lark-base-dashboard-block-get.md](lark-base-dashboard-block-get.md) — get detailed block config
