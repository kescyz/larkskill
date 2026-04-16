# dashboard-create

> **Prerequisite:** Read [lark-base-dashboard.md](lark-base-dashboard.md) for the overall workflow.

Create an empty dashboard. Record the returned `dashboard_id` — it is needed for all subsequent operations.

## Recommended call

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/dashboards
- body:
  ```json
  { "name": "Sales Report" }
  ```

With theme:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/dashboards
- body:
  ```json
  { "name": "Sales Report", "theme_style": "default" }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `name` | Yes | Dashboard name (body) |
| `theme_style` | No | Theme style (body, see enum below) |

### theme_style enum

| Value | Description |
|-------|-------------|
| `default` | Default theme |
| `SimpleBlue` | Simple blue |
| `DarkGreen` | Dark green |
| `summerBreeze` | Summer breeze |
| `simplistic` | Minimal |
| `energetic` | Energetic |
| `deepDark` | Dark |
| `futuristic` | Futuristic |

## API request details

```
POST /open-apis/base/v3/bases/{base_token}/dashboards
```

## Key return fields

| Field | Description |
|-------|-------------|
| `dashboard_id` | Dashboard ID (e.g. `blkxxxxxxxxxxxx`); record this for subsequent operations |
| `name` | Dashboard name |
| `theme.theme_style` | Theme style |

## Pitfalls

- This is a write operation; confirm with the user before execution.

## References

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard module guide
