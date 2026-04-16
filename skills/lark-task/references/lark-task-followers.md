# task +followers

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Manage task followers. Add or remove followers from an existing task.

## Recommended call

Add a follower:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasks/{task_guid}/add_members
- body:
  ```json
  {
    "members": [{ "id": "ou_aaa", "type": "open_id", "role": "follower" }]
  }
  ```
- params: `{ "user_id_type": "open_id" }`

Remove a follower:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasks/{task_guid}/remove_members
- body:
  ```json
  {
    "members": [{ "id": "ou_aaa", "type": "open_id", "role": "follower" }]
  }
  ```
- params: `{ "user_id_type": "open_id" }`

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `members` | Yes | Array of member objects. Each: `{id: "<open_id>", type: "open_id", role: "follower"}` |

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `user_id_type` | No | User ID type: `open_id` (default), `union_id`, or `user_id` |

## Workflow

1. Confirm the task and followers to add/remove.
2. Call `add_members` or `remove_members` with `role: "follower"`.
3. Report success.

> [!CAUTION]
> This is a **Write Operation** — you must confirm the user's intent before executing.
