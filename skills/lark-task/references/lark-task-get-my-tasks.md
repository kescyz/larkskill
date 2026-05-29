# task +get-my-tasks

If the user query only specifies a task name (e.g., "Complete task Lobster No. 1"), use this command to list and search for the task by its summary.

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.
> 
> **⚠️ Note:** This API must be called with a user identity. **Do NOT use an app identity, otherwise the call will fail.**
>
> **Output rendering note:**
> 1. If you need to present user fields (assignee, creator, etc.), do not only output the raw `id` (e.g. open_id). Also try to resolve and display the user's real name (e.g. via the contact skill) for readability.
> 2. When rendering timestamps (e.g. created time, due time), use the local timezone. Format is 2006-01-02 15:04:05

List tasks assigned to the current user, with support for filtering by completion status, creation time, and due date.
By default, the call will automatically paginate up to 20 times to fetch records.

> **Pending vs all tasks:** When `complete` is not provided, the result contains **both completed and incomplete tasks**.
> For standup / daily-summary / pending-todo scenarios, you **must** pass `complete: false`; otherwise completed tasks will be surfaced as if they were still pending.

## Recommended Commands

```js
// Search for a specific task by name
lark_api({ tool: 'task', op: 'get-my-tasks', args: { query: 'Lobster No. 1' } })

// Get all my tasks, both completed and incomplete (fetches up to 20 pages by default)
lark_api({ tool: 'task', op: 'get-my-tasks', args: {} })

// Pending-only: my incomplete tasks (use this for standup/daily-summary)
lark_api({ tool: 'task', op: 'get-my-tasks', args: { complete: false } })

// Pending-only with a due-date upper bound (e.g. end of today / this week)
lark_api({ tool: 'task', op: 'get-my-tasks', args: { complete: false, due_end: '2026-03-27T23:59:59+08:00' } })
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | No | Search for tasks by summary. Returns exact matches if any; otherwise returns partial matches. |
| `complete` | No | Optional. If not provided, it fetches all tasks (both incomplete and completed). Set to `true` to fetch only completed tasks, or `false` for incomplete tasks. |
| `created_at` | No | Query tasks created after this time. Supports date: `YYYY-MM-DD`, relative: `-2d`, or ms timestamp. |
| `due_start` | No | Query tasks with a due date after this time. Supports date: `YYYY-MM-DD`, relative: `-2d`, or ms timestamp. |
| `due_end` | No | Query tasks with a due date before this time. Supports date: `YYYY-MM-DD`, relative: `-2d`, or ms timestamp. |

## Workflow

1. Determine the filters based on the user's request.
2. Execute the call. It will automatically loop up to the page limit (default 20) to fetch records.
3. Show the results (ID, summary, due time, and created date).
