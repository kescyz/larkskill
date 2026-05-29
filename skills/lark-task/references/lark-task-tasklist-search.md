# task +tasklist-search

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.
>
> **⚠️ Note:** This shortcut uses tasklist search followed by tasklist detail queries to render the final output.

Search tasklists by keyword and optional filters.

## Recommended Commands

```js
// Search by keyword
lark_api({ tool: 'task', op: 'tasklist-search', args: { query: '测试' } })

// Search tasklists created by specific users
lark_api({ tool: 'task', op: 'tasklist-search', args: { creator: 'ou_xxx,ou_yyy' } })

// Search by creation time range
lark_api({ tool: 'task', op: 'tasklist-search', args: { query: 'Q2', create_time: '-30d,+0d' } })
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | No | Search keyword. If omitted, at least one filter must be provided. |
| `creator` | No | Creator open_ids, comma-separated. |
| `create_time` | No | Creation time range in `start,end` form. Each side supports ISO/date/relative/ms input. |

## Workflow

1. Build the search keyword and filters from the user's request.
2. Execute `lark_api({ tool: 'task', op: 'tasklist-search', args: { ... } })`
3. Report the matched tasklists and the next `page_token` if more results exist.

