# task +tasklist-members

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Manage tasklist members (editors/owners).

## Recommended call

Add a member:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasklists/{tasklist_guid}/add_members
- body:
  ```json
  {
    "members": [{ "id": "ou_aaa", "type": "open_id", "role": "editor" }]
  }
  ```
- params: `{ "user_id_type": "open_id" }`

Remove a member:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasklists/{tasklist_guid}/remove_members
- body:
  ```json
  {
    "members": [{ "id": "ou_aaa", "type": "open_id", "role": "editor" }]
  }
  ```
- params: `{ "user_id_type": "open_id" }`

Replace all members exactly — call `remove_members` for all existing members first, then `add_members` for the new set.

## Parameters (path)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `tasklist_guid` | Yes | The GUID of the tasklist |

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `members` | Yes | Array of member objects: `{id: "<open_id>", type: "open_id", role: "editor"\|"owner"}` |

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `user_id_type` | No | User ID type: `open_id` (default), `union_id`, or `user_id` |

## Workflow

1. Confirm the tasklist and members to add/remove/set.
2. Call `add_members` or `remove_members` as needed.
3. Report success.

> [!CAUTION]
> This is a **Write Operation** — you must confirm the user's intent before executing.
