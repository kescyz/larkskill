# task +set-ancestor

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.

Set a parent task for a task, or clear the parent to make it independent.

## Recommended Commands

```js
// Set a parent task
lark_api({ tool: 'task', op: 'set-ancestor', args: { task_id: 'guid_1', ancestor_id: 'guid_2' } })

// Clear the parent task
lark_api({ tool: 'task', op: 'set-ancestor', args: { task_id: 'guid_1' } })
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `task_id` | Yes | The task GUID to update. |
| `ancestor_id` | No | The parent task GUID. Omit it to clear the ancestor. |

## Workflow

1. Confirm the child task and, if applicable, the ancestor task.
2. Execute `lark_api({ tool: 'task', op: 'set-ancestor', args: { ... } })`
3. Report the updated task GUID and whether the ancestor was set or cleared.

> [!CAUTION]
> This is a **Write Operation** -- You must confirm the user's intent before executing.

