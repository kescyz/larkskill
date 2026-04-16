# workflow-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

List all automated workflows in Base with pagination.

## Recommended call

All workflows:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/workflows/list
- body:
  ```json
  { "page_size": 100 }
  ```

Filter by status:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/workflows/list
- body:
  ```json
  { "status": "enabled", "page_size": 100 }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `page_size` | No | Page size, default `20`, max `100` (body) |
| `page_token` | No | Pagination token from previous response (body) |
| `status` | No | Filter: `enabled` / `disabled`; omit to return all (body) |

## API request details

```
POST /open-apis/base/v3/bases/{base_token}/workflows/list
```

Note: This list endpoint uses **POST**, not GET. `page_token` goes in the request body, not query params.

## Key return fields

| Field | Description |
|-------|-------------|
| `items` | Workflow list; each item has `workflow_id`, `title`, `status`, `trigger_type`, `creator_id`, `create_time` |
| `total` | Total matching count |
| `has_more` | `true` if more pages exist; use `page_token` to continue |

## Pitfalls

- The list endpoint uses POST, not GET; `page_token` is in the body, not query params.
- `workflow_id` starts with `wkf`; do not confuse with `table_id` (starts with `tbl`).

## References

- [lark-base-workflow-get.md](lark-base-workflow-get.md) — get full workflow details
- [lark-base-workflow-enable.md](lark-base-workflow-enable.md) — enable a workflow
- [lark-base-workflow-disable.md](lark-base-workflow-disable.md) — disable a workflow
