# workflow-get

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.
> **Must read:** For the `steps` structure and each trigger/action component, see [lark-base-workflow-schema.md](lark-base-workflow-schema.md).

Get the complete definition of a workflow: title, status, all steps and their configuration.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/workflows/{workflow_id}

With user ID type:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/workflows/{workflow_id}
- params:
  ```json
  { "user_id_type": "open_id" }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `workflow_id` | Yes | Workflow ID starting with `wkf` (path param) |
| `user_id_type` | No | Controls format of `creator_id` / `updater_id`: `open_id` (default) / `union_id` / `user_id` (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/workflows/{workflow_id}
```

## Key return fields

| Field | Type | Description |
|-------|------|-------------|
| `workflow_id` | string | Workflow ID (`wkf` prefix) |
| `title` | string | Workflow title |
| `status` | string | `enabled` / `disabled` |
| `creator_id` | string | Creator ID |
| `updater_id` | string | Last modifier ID |
| `create_time` | string | Unix seconds timestamp |
| `update_time` | string | Unix seconds timestamp |
| `steps` | array | Step list (see schema for structure) |

### Step fields

| Field | Description |
|-------|-------------|
| `id` | Step unique ID |
| `type` | Step type (see [lark-base-workflow-schema.md](lark-base-workflow-schema.md)) |
| `title` | Step title |
| `children.links[].kind` | Relationship type: `if_true` / `if_false` / `case` / `loop_start` / `slot` |
| `children.links[].to` | Target node ID |
| `next` | Linear successor node ID; `null` = end |
| `data` | Step config; structure varies by `type` |
| `meta` | Extended metadata (only for `APIHubAction` / `AIAgentLLMAction` / `AIAgentMCPAction`) |

## Pitfalls

- `workflow_id` starts with `wkf`; obtain via `workflow-list`. It is usually not in the URL — do not confuse with `table_id` (starts with `tbl`).
- `steps` may be an empty array for unconfigured workflows — not an error.

## References

- [lark-base-workflow-schema.md](lark-base-workflow-schema.md) — complete step data structure
- [lark-base-workflow-list.md](lark-base-workflow-list.md) — list workflows to get `workflow_id`
- [lark-base-workflow-update.md](lark-base-workflow-update.md) — update workflow
