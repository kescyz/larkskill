# task +create

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Create a new task in Lark.

## Recommended call

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasks
- body:
  ```json
  {
    "summary": "Quarterly Sales Review",
    "description": "Review the sales performance for the last quarter.",
    "members": [{ "id": "ou_xxx", "type": "open_id", "role": "assignee" }],
    "due": { "time": "2026-03-25T00:00:00+08:00", "is_all_day": false },
    "tasklist_guid": "tl_xxx"
  }
  ```
- params: `{ "user_id_type": "open_id" }`

Simple task (summary only):

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasks
- body:
  ```json
  { "summary": "Buy milk" }
  ```
- params: `{ "user_id_type": "open_id" }`

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `summary` | Yes | The title or summary of the task |
| `description` | No | Detailed description of the task |
| `members` | No | Array of members; each item: `{id, type, role}`. Use `role: "assignee"` to assign |
| `due` | No | Due date object: `{time: "<ISO8601>", is_all_day: false}`. For all-day: `{timestamp: "<ms>", is_all_day: true}` |
| `tasklist_guid` | No | Tasklist GUID to add task to on creation |
| `client_token` | No | Client token for idempotent create requests |

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `user_id_type` | No | User ID type for member fields: `open_id` (default), `union_id`, or `user_id` |

## Workflow

1. Confirm summary, due date, assignee, and tasklist with user.
   - **Crucial assignee rule:** If user explicitly or implicitly asks "create a task for me", you must assign it to current logged-in user. Resolve current user's `open_id` via `lark_api GET /open-apis/contact/v3/users/me`, then include it in `members` with `role: "assignee"`.
2. Call `lark_api POST /open-apis/task/v2/tasks`.
3. Return result including task `guid` and `summary`. Include `url` if present in the response.

> [!CAUTION]
> This is a **Write Operation**. You must confirm user intent before execution.

## References

- [lark-task](../SKILL.md) - All task commands
- [lark-shared](../../lark-shared/SKILL.md) - Authentication and global parameters
