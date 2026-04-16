# task +comment

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Add a comment to an existing task.

## Recommended call

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/task/v2/tasks/{task_guid}/comments
- body:
  ```json
  { "content": "Looks good!" }
  ```

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `content` | Yes | The text content of the comment |

## Workflow

1. Confirm the task and comment content.
2. Call `lark_api POST /open-apis/task/v2/tasks/{task_guid}/comments`.
3. Report success and comment ID.

> [!CAUTION]
> This is a **Write Operation** — you must confirm the user's intent before executing.
