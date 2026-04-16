# task +reminder

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.
> **Priority:** For creating or modifying task reminder times, prioritize using this `+reminder` approach over other task update methods. It provides a more reliable and direct way to manage reminders.

Manage task reminders. Set new reminders or remove existing ones. Note that setting a task reminder requires a due date.

## Recommended call

Set a reminder (e.g., 30 minutes before due):

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/task/v2/tasks/{task_guid}
- body:
  ```json
  {
    "task": {
      "reminders": [{ "relative_fire_minute": 30 }]
    },
    "update_fields": ["reminders"]
  }
  ```

Set a reminder 1 hour before due (`relative_fire_minute: 60`):

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/task/v2/tasks/{task_guid}
- body:
  ```json
  {
    "task": {
      "reminders": [{ "relative_fire_minute": 60 }]
    },
    "update_fields": ["reminders"]
  }
  ```

Remove all reminders:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/task/v2/tasks/{task_guid}
- body:
  ```json
  {
    "task": { "reminders": [] },
    "update_fields": ["reminders"]
  }
  ```

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `task.reminders` | Yes | Array of reminder objects. Each: `{relative_fire_minute: <int>}` — minutes before due time. Pass empty array to remove all reminders |
| `update_fields` | Yes | Must include `"reminders"` |

## Unit conversion

| User input | `relative_fire_minute` value |
|-----------|------------------------------|
| 15m / 15 minutes | 15 |
| 30m / 30 minutes | 30 |
| 1h / 1 hour | 60 |
| 1d / 1 day | 1440 |

## Workflow

1. Confirm the task and reminder action.
2. Call `lark_api PATCH /open-apis/task/v2/tasks/{task_guid}` with `reminders` in `update_fields`.
3. Report success.

> [!CAUTION]
> This is a **Write Operation** — you must confirm the user's intent before executing.
