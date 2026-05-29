# task +search

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.
>
> **⚠️ Note:** This API must be called with a user identity. **Do NOT use an app identity, otherwise the call will fail.**

Search tasks by keyword and optional filters.

## Recommended Commands

```js
// Search by keyword
lark_api({ tool: 'task', op: 'search', args: { query: 'test' } })

// Search incomplete tasks assigned to specific users
lark_api({ tool: 'task', op: 'search', args: { assignee: 'ou_xxx,ou_yyy', completed: false } })

// Search by due time range
lark_api({ tool: 'task', op: 'search', args: { query: 'release', due: '-1d,+7d' } })
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | No | Search keyword. If omitted, at least one filter must be provided. |
| `creator` | No | Creator open_ids, comma-separated. |
| `assignee` | No | Assignee open_ids, comma-separated. |
| `follower` | No | Follower open_ids, comma-separated. |
| `completed` | No | Filter by completion state. |
| `due` | No | Due time range in `start,end` form. Each side supports ISO/date/relative/ms input. |

## Workflow

1. Build the keyword and filters from the user's request.
2. Execute `lark_api({ tool: 'task', op: 'search', args: { ... } })`
3. Report the matched tasks and include the next `page_token` if more results exist.

