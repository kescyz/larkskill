# dashboard-update

> **Prerequisite:** Read [lark-base-dashboard.md](lark-base-dashboard.md) for the overall workflow.

Update dashboard name or theme.

## Recommended call

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}
- body:
  ```json
  { "name": "New Name", "theme_style": "default" }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `dashboard_id` | Yes | Dashboard ID (path param) |
| `name` | No | New dashboard name (body) |
| `theme_style` | No | New theme style (body, see enum below) |

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
PATCH /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}
```

## Key return fields

| Field | Description |
|-------|-------------|
| `dashboard` | Updated dashboard object |
| `dashboard.name` | New name (if updated) |
| `dashboard.theme.theme_style` | New theme (if updated) |
| `updated` | `true` if update succeeded |

## Pitfalls

- This is a write operation; confirm with the user before execution.

## References

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard module guide
