# task +assign

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Assign or remove members (assignees) from a task.

## Recommended call

Add an assignee:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasks/{task_guid}/add_members
- body:
  ```json
  {
    "members": [{ "id": "ou_aaa", "type": "open_id", "role": "assignee" }]
  }
  ```
- params: `{ "user_id_type": "open_id" }`

Remove an assignee:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasks/{task_guid}/remove_members
- body:
  ```json
  {
    "members": [{ "id": "ou_old", "type": "open_id", "role": "assignee" }]
  }
  ```
- params: `{ "user_id_type": "open_id" }`

Transfer assignee (remove old, add new) — two sequential calls:
1. `remove_members` for old assignee
2. `add_members` for new assignee

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `members` | Yes | Array of member objects. Each: `{id: "<open_id>", type: "open_id", role: "assignee"}` |

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `user_id_type` | No | User ID type: `open_id` (default), `union_id`, or `user_id` |

## Workflow

1. Confirm the task and members to add/remove.
2. Call `add_members` and/or `remove_members` as needed.
3. Report success and the new count of assignees.

> [!CAUTION]
> This is a **Write Operation** — you must confirm the user's intent before executing.
