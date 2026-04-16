# task +reopen

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Reopen a previously completed task.

## Recommended call

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasks/{task_guid}/uncomplete
- body: `{}`

## Parameters (path)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `task_guid` | Yes | The GUID of the task to reopen |

## Workflow

1. Confirm the task to reopen.
2. Call `lark_api POST /open-apis/task/v2/tasks/{task_guid}/uncomplete`.
3. Report success.

> [!CAUTION]
> This is a **Write Operation** — you must confirm the user's intent before executing.
