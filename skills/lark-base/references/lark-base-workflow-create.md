# workflow-create

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Create a new automation workflow in a Base. New workflows start as `disabled`; call `workflow-enable` to activate.

## Recommended call

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/workflows
- body:
  ```json
  {
    "client_token": "1704067200",
    "title": "Automatic notification of new orders",
    "steps": [
      {
        "id": "trigger_1",
        "type": "AddRecordTrigger",
        "title": "Monitor new orders",
        "children": { "links": [] },
        "next": "action_1",
        "data": {
          "table_name": "Order Table",
          "watched_field_name": "Order Number"
        }
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
          "content": [
            { "value_type": "text", "value": "New order received, customer:" },
            { "value_type": "ref", "value": { "path": "$.trigger_1.Customer name" } }
          ],
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
| `client_token` | Yes | Idempotency key; unique per call (e.g. Unix timestamp string) (body) |
| `title` | No | Workflow title (body) |
| `steps` | No | Step list (body) |
| `user_id_type` | No | User ID type: `open_id` / `union_id` / `user_id`, default `open_id` (body) |

## API request details

```
POST /open-apis/base/v3/bases/{base_token}/workflows
```

## Key return fields

| Field | Description |
|-------|-------------|
| `workflow_id` | Created workflow ID (`wkf` prefix) |
| `title` | Workflow title |
| `status` | Always `disabled` for new workflows |
| `steps` | Full step list |
| `creator_id` | Creator OpenID |
| `create_time` | Unix seconds timestamp |

## Workflow

1. Confirm `base_token` and workflow JSON with the user.
2. For complex workflows, prefer passing JSON from a file.
3. After creation, report the `workflow_id`.
4. Inform the user that the workflow starts as `disabled`; call `workflow-enable` to activate.

## Pitfalls

- `client_token` is **required**; missing it returns error `[code=800004006] client token is empty`.
- New workflows are `disabled` by default; do not report them as auto-enabled.
- Step `id` values must be unique within the workflow; `next` and `children.links[].to` must reference existing step IDs.
- For user values (`value_type: "user"`), `value` is OpenID by default; set `user_id_type` in body to change.

## References

- [lark-base-workflow-schema.md](lark-base-workflow-schema.md) — full workflow data structure
- [lark-base-workflow-enable.md](lark-base-workflow-enable.md) — enable workflow after creation
- [lark-base-workflow-list.md](lark-base-workflow-list.md) — list all workflows
