# workflow-update

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Fully replace an existing workflow definition (`title` and/or `steps`). PUT semantics — the incoming content completely overwrites the original.

## Recommended call

Update title only (steps cleared if not included):

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/workflows/{workflow_id}
- body:
  ```json
  { "title": "New Title", "steps": [] }
  ```

Full workflow replacement:

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/workflows/{workflow_id}
- body:
  ```json
  {
    "title": "Automatic notification of new orders (updated)",
    "steps": [
      {
        "id": "trigger_1",
        "type": "AddRecordTrigger",
        "title": "Monitor new orders",
        "children": { "links": [] },
        "next": "action_1",
        "data": { "table_name": "Order Table", "watched_field_name": "Order Number" }
      },
      {
        "id": "action_1",
        "type": "LarkMessageAction",
        "title": "Send notification",
        "children": { "links": [] },
        "next": null,
        "data": {
          "receiver": [{ "value_type": "user", "value": "ou_xxxx" }],
          "send_to_everyone": false,
          "title": [{ "value_type": "text", "value": "New Order Reminder" }],
          "content": [{ "value_type": "text", "value": "New order received" }],
          "btn_list": []
        }
      }
    ]
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `workflow_id` | Yes | Workflow ID starting with `wkf` (path param) |
| `title` | No | Workflow title (body) |
| `steps` | No | Step list — full replacement (body) |
| `user_id_type` | No | User ID type: `open_id` / `union_id` / `user_id`, default `open_id` (body) |

## API request details

```
PUT /open-apis/base/v3/bases/{base_token}/workflows/{workflow_id}
```

## Key return fields

| Field | Description |
|-------|-------------|
| `workflow_id` | Workflow ID |
| `title` | Updated title |
| `status` | Current status (unchanged by this call) |
| `steps` | Updated full step list |
| `update_time` | Unix seconds timestamp |

## Workflow

> This is a **write operation**; confirm with the user before execution. PUT semantics will completely overwrite the original definition.

1. Use `workflow-list` to find the `workflow_id`.
2. Use `workflow-get` to retrieve the current definition as a base for edits.
3. Confirm the complete body with the user — omitting `steps` will clear all steps.
4. Execute and report the returned `workflow_id` and `update_time`.

## Pitfalls

- **PUT is full replacement**: omitting `steps` clears all steps.
- `workflow_id` starts with `wkf`; do not confuse with `table_id` (starts with `tbl`).
- Step `id` values must be unique; `next` and `children.links[].to` must reference existing step IDs.
- This call does not change `enabled/disabled` status; call `workflow-enable` / `workflow-disable` separately.

## References

- [lark-base-workflow-schema.md](lark-base-workflow-schema.md) — full workflow data structure
- [lark-base-workflow-create.md](lark-base-workflow-create.md) — create workflow
- [lark-base-workflow-enable.md](lark-base-workflow-enable.md) — enable workflow
- [lark-base-workflow-list.md](lark-base-workflow-list.md) — list all workflows
