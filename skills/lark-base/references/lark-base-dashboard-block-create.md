# dashboard-block-create

> **Prerequisite:** Read [lark-base-dashboard.md](lark-base-dashboard.md) for the overall workflow.
> **Key:** Before creating, read [dashboard-block-data-config.md](dashboard-block-data-config.md) for block types and `data_config` structure.

Create a block in a dashboard.

## Key constraints

- **`type` cannot be changed after creation** — choose correctly at creation time.
- **`data_config` structure varies by `type`** — must read [dashboard-block-data-config.md](dashboard-block-data-config.md).
- **Block creation must be serial** — no concurrent execution.

## Recommended call

KPI card (count records):

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks
- body:
  ```json
  {
    "name": "Total Records",
    "type": "statistics",
    "data_config": { "table_name": "Orders", "count_all": true }
  }
  ```

Line chart with series:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks
- body:
  ```json
  {
    "name": "Sales Trend",
    "type": "line",
    "data_config": {
      "table_name": "Orders",
      "series": [{"field_name": "Amount", "rollup": "SUM"}],
      "group_by": [{"field_name": "Month", "mode": "integrated"}]
    }
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `dashboard_id` | Yes | Dashboard ID (path param) |
| `name` | Yes | Block name (body) |
| `type` | Yes | Block type (body, see enum below) |
| `data_config` | No | Data config JSON; structure varies by type (body) |
| `user_id_type` | No | User ID type when filter references user fields (query param) |

### type enum

| Value | Description |
|-------|-------------|
| `column` | Column chart |
| `bar` | Bar chart |
| `line` | Line chart |
| `pie` | Pie chart |
| `ring` | Donut chart |
| `area` | Area chart |
| `combo` | Combo chart |
| `scatter` | Scatter chart |
| `funnel` | Funnel chart |
| `wordCloud` | Word cloud |
| `radar` | Radar chart |
| `statistics` | KPI card |

## API request details

```
POST /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks
```

## Key return fields

| Field | Description |
|-------|-------------|
| `block.block_id` | Block ID — record this for edit/delete operations |
| `block.name` | Block name |
| `block.type` | Block type |
| `block.data_config` | Actual created data config (may include backend-added defaults) |
| `created` | `true` if creation succeeded |

## Pitfalls

- This is a write operation; confirm with the user before execution.

## References

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard module guide
- [dashboard-block-data-config.md](dashboard-block-data-config.md) — data_config structure, chart types, filter rules
