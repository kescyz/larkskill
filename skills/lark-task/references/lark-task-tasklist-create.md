# task +tasklist-create

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Create a new tasklist, and optionally batch create tasks within it.

## Recommended call

Create an empty tasklist:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasklists
- body:
  ```json
  { "name": "Q1 Goals" }
  ```
- params: `{ "user_id_type": "open_id" }`

Create a tasklist and add members:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasklists
- body:
  ```json
  {
    "name": "Project A",
    "members": [
      { "id": "ou_xxx", "type": "open_id", "role": "editor" },
      { "id": "ou_yyy", "type": "open_id", "role": "editor" }
    ]
  }
  ```
- params: `{ "user_id_type": "open_id" }`

To batch create tasks within the tasklist after creation, call `lark_api POST /open-apis/task/v2/tasks` for each task with the `tasklist_guid` field set.

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | The name of the tasklist |
| `members` | No | Array of member objects: `{id: "<open_id>", type: "open_id", role: "editor"}` |

## Workflow

1. Confirm the tasklist name, members, and tasks (if any).
2. Call `lark_api POST /open-apis/task/v2/tasklists`.
3. If tasks need to be created, call `lark_api POST /open-apis/task/v2/tasks` for each with `tasklist_guid` from step 2.
4. Report success, including the new tasklist GUID and URL if available.

> [!CAUTION]
> This is a **Write Operation** — you must confirm the user's intent before executing.
