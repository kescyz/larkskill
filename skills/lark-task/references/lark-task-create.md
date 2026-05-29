# task +create

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.

Create a new task in Lark.

## Recommended Commands

```js
// Create a task with all details
lark_api({ tool: 'task', op: 'create', args: {
  summary: 'Quarterly Sales Review',
  description: 'Review the sales performance for the last quarter.',
  assignee: 'ou_xxx',
  due: '2026-03-25',
  tasklist_id: 'https://applink.larkoffice.com/client/todo/task_list?guid=a4b00000-000-000-000-00000000036c'
} })

// Create a task assigned to an app
lark_api({ tool: 'task', op: 'create', args: {
  summary: 'Nightly Sync',
  assignee: 'cli_xxx'
} })

// Create a simple task
lark_api({ tool: 'task', op: 'create', args: {
  summary: 'Buy milk'
} })
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `summary` | Yes | The title or summary of the task |
| `description` | No | Detailed description of the task |
| `assignee` | No | Assignee ID. Use user `open_id` like `ou_xxx` for people, or app ID like `cli_xxx` for apps. |
| `follower` | No | Follower ID. Use user `open_id` like `ou_xxx` for people, or app ID like `cli_xxx` for apps. |
| `due` | No | Due date. Supports ISO 8601, `YYYY-MM-DD`, relative time (e.g., `+2d`), or ms timestamp. `YYYY-MM-DD` and relative time will automatically set it as an all-day task. |
| `tasklist_id` | No | The GUID of the tasklist, or a full AppLink URL (the CLI will automatically extract the `guid` parameter from the URL). |
| `idempotency_key` | No | Client token to ensure idempotency of the request. |

## Workflow

1. Confirm with the user: task summary, due date, assignee, and tasklist if necessary.
   - **Crucial Rule for Assignee**: If the user explicitly or implicitly says "create a task for me" (给我创建一个任务), or "help me create a task" (帮我新建/创建一个任务), you MUST assign the task to the current logged-in user. You can get the current user's `open_id` by calling `lark_auth_status` or `lark_api({ tool: 'contact', op: 'get-user' })` first, extracting `.identities.user.openId` (from `lark_auth_status`) or `.data.user.open_id` (from `contact get-user`), and then passing it to the `assignee` parameter.
2. Execute `lark_api({ tool: 'task', op: 'create', args: { summary: '...', ... } })`
3. Report the result: task ID and summary.

> [!CAUTION]
> This is a **Write Operation** -- You must confirm the user's intent before executing.

## References

- [lark-task](../SKILL.md) -- All task commands
- [lark-shared](../../lark-shared/SKILL.md) -- Authentication and global parameters
