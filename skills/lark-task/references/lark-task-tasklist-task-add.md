# task +tasklist-task-add

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Add existing tasks to a tasklist.

## Recommended call

Add a single task to a tasklist:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasklists/{tasklist_guid}/add_task
- body:
  ```json
  { "task_guid": "t_aaa" }
  ```

Add multiple tasks — call sequentially for each task:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasklists/{tasklist_guid}/add_task
- body:
  ```json
  { "task_guid": "t_bbb" }
  ```

## Parameters (path)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `tasklist_guid` | Yes | The GUID of the tasklist |

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `task_guid` | Yes | The GUID of the task to add |

## Workflow

1. Confirm the tasklist and the tasks to add.
2. For each task, call `lark_api POST /open-apis/task/v2/tasklists/{tasklist_guid}/add_task`.
3. Report the result (successful vs failed tasks).

> [!CAUTION]
> This is a **Write Operation** — you must confirm the user's intent before executing.
