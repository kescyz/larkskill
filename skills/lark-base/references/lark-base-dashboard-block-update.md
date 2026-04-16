# dashboard-block-update

> **Prerequisite:** Read [lark-base-dashboard.md](lark-base-dashboard.md) for the overall workflow.
> **Key:** Before updating, read [dashboard-block-data-config.md](dashboard-block-data-config.md) for `data_config` structure and update rules.

Update a block's name or data config in a dashboard.

## Key constraints

- **Cannot modify `type` or `layout`** — only `name` and `data_config` can be updated.
- **`data_config` uses top-level key merge** — only pass top-level fields to change; unspecified fields retain original values. However each passed field is fully replaced (e.g. a new `filter` completely overwrites the old one).
- **`series` and `count_all` are mutually exclusive** — at least one must be present.
- **`table_name` uses the display name, not the ID** — e.g. `"Orders"`, not `tbl_xxx`.

## Recommended call

Update name only:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks/{block_id}
- body:
  ```json
  { "name": "New Name" }
  ```

Update filter in data_config:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks/{block_id}
- body:
  ```json
  {
    "data_config": {
      "filter": {
        "conjunction": "and",
        "conditions": [{"field_name": "Status", "operator": "is", "value": "Completed"}]
      }
    }
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `dashboard_id` | Yes | Dashboard ID (path param) |
| `block_id` | Yes | Block ID (path param) |
| `name` | No | New block name (body) |
| `data_config` | No | Partial data config; top-level key merge (body) |
| `user_id_type` | No | User ID type when filter references user fields (query param) |

## API request details

```
PATCH /open-apis/base/v3/bases/{base_token}/dashboards/{dashboard_id}/blocks/{block_id}
```

## Key return fields

| Field | Description |
|-------|-------------|
| `block.block_id` | Block ID |
| `block.name` | Updated name |
| `block.type` | Block type (cannot be modified) |
| `block.data_config` | Updated data config |
| `updated` | `true` if update succeeded |

## Pitfalls

- This is a write operation; confirm with the user before execution.

## References

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard module guide
- [dashboard-block-data-config.md](dashboard-block-data-config.md) — data_config structure, chart types, filter rules
