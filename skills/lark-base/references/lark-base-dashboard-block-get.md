# dashboard-block-get

> **Prerequisite:** Read [lark-base-dashboard.md](lark-base-dashboard.md) for the overall workflow.

Get details of a single block including complete `data_config`. Common uses: view full block config; understand current config before editing.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks/{block_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `dashboard_id` | Yes | Dashboard ID (path param) |
| `block_id` | Yes | Block ID (path param) |
| `user_id_type` | No | User ID type: `open_id` / `union_id` / `user_id` (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks/{block_id}
```

## Key return fields

| Field | Description |
|-------|-------------|
| `block.block_id` | Block ID |
| `block.name` | Block name |
| `block.type` | Block type (e.g. `column` / `line` / `pie`) |
| `block.data_config` | Data config — use as basis when editing |
| `block.layout` | Layout info (read-only: x / y / w / h) |

## References

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard module guide
- [dashboard-block-data-config.md](dashboard-block-data-config.md) — data_config structure reference
