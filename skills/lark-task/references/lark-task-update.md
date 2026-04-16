# task +update

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Update an existing task in Lark.

## Recommended call

Update task summary:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/task/v2/tasks/{task_guid}
- body:
  ```json
  {
    "task": { "summary": "New Summary" },
    "update_fields": ["summary"]
  }
  ```
- params: `{ "user_id_type": "open_id" }`

Update due date:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/task/v2/tasks/{task_guid}
- body:
  ```json
  {
    "task": { "due": { "time": "2026-05-01T17:00:00+07:00", "is_all_day": false } },
    "update_fields": ["due"]
  }
  ```
- params: `{ "user_id_type": "open_id" }`

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `task` | Yes | Object containing only the fields to update |
| `task.summary` | No | New summary/title for the task |
| `task.description` | No | New description for the task |
| `task.due` | No | New due date object: `{time: "<ISO8601>", is_all_day: false}` |
| `update_fields` | Yes | Array of field names being updated, e.g. `["summary", "due"]` |

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `user_id_type` | No | User ID type: `open_id` (default), `union_id`, or `user_id` |

## Workflow

1. Confirm with the user the task(s) to update and the fields.
2. Call `lark_api PATCH /open-apis/task/v2/tasks/{task_guid}` with the body above.
3. Report the successful updates.

> [!CAUTION]
> This is a **Write Operation** — you must confirm the user's intent before executing.
