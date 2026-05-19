---
name: lark-task
version: 2.0.0
description: "Use this skill when operating Lark Task via LarkSkill MCP: create to-do tasks, view and update task status, break down subtasks, organize tasklists, assign collaborators, upload task attachments, register or unregister task agents, update agent home page data, and write agent task records."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# task (v2)

**CRITICAL — Before starting, MUST read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. It contains authentication and permission handling.**

> **Task search tips**: First determine whether the user has **specifically requested the search skill**, and whether they have actually provided a **query keyword** (e.g. task name, keyword, fragment description). If the user specifically requests the search skill, or explicitly provides a task query keyword, prefer `+search` when the target is **tasks**. If the user has not specifically requested the search skill and the intent has no query keyword — only scope conditions (e.g. "since this year", "completed", "created by me", "I'm following") — prefer list-type capabilities. Among those, "related to me / I'm following / created by me" should prioritize `+get-related-tasks`; "assigned to me / I'm responsible for" should prioritize `+get-my-tasks`. Do NOT mistake time-range words (e.g. "since this year") as `query` values for search.

> **Tasklist search tips**: Tasklists follow the same logic. If the user explicitly provides a tasklist query keyword, prefer `+tasklist-search`. Otherwise, prefer the native `tasklists.list` API with local filtering.

> **Intent disambiguation**: Expressions like "search Lark for tasks I'm following since this year" — if there is no actual query keyword and the intent is "related to me + time range" — prefer `+get-related-tasks`. Expressions like "search Lark for tasklists I created" — if there is no tasklist keyword — prefer native `tasklists.list` with local filtering.

> **User identity recognition**: If the user mentions "me" (e.g. "assigned to me", "created by me"), default to fetching the currently logged-in user's `open_id` as the parameter value.

> **Terminology**: If the user mentions "todo", consider whether they mean "task" and use this skill's operations.

> **Friendly output**: When outputting task or tasklist results, also extract and output the `url` field (task link) so the user can click to view details.

> **Create/update notes**:
> 1. `repeat_rule` and `reminder` can only be set if `due` has been set.
> 2. If both `start` and `due` are set, start time must be ≤ due time.
> 3. When using tenant_access_token (application identity), task members cannot be added across tenants.

> **Query notes**:
> 1. When rendering person fields (assignees, creators), in addition to `id`, MUST also fetch and display the person's real name (e.g. via the Contact skill).
> 2. Same rule applies to owner, member, and role member fields in tasklist details.
> 3. Render time fields (created time, due time) using local timezone (format: 2006-01-02 15:04:05).

> **Task GUID definition**:
> The `guid` in Task OpenAPI is the globally unique identifier — NOT the client task number (e.g. `t104121` / `suite_entity_num`).
> For Lark task applinks (e.g. `.../client/todo/task?guid=...`), use the `guid` URL query parameter as the task guid.

## Shortcuts

| Shortcut | MCP call |
|----------|---------|
| Create a task | `lark_api({ tool: 'task', op: '+create', args: { summary: '...', ... } })` |
| Update a task | `lark_api({ tool: 'task', op: '+update', args: { guid: '...', ... } })` |
| Add a comment | `lark_api({ tool: 'task', op: '+comment', args: { guid: '...', content: '...' } })` |
| Complete a task | `lark_api({ tool: 'task', op: '+complete', args: { guid: '...' } })` |
| Reopen a task | `lark_api({ tool: 'task', op: '+reopen', args: { guid: '...' } })` |
| Assign/remove members | `lark_api({ tool: 'task', op: '+assign', args: { guid: '...', members: [...] } })` |
| Manage followers | `lark_api({ tool: 'task', op: '+followers', args: { guid: '...', ... } })` |
| Manage reminders | `lark_api({ tool: 'task', op: '+reminder', args: { guid: '...', ... } })` |
| List my tasks (assigned to me) | `lark_api({ tool: 'task', op: '+get-my-tasks', args: { ... } })` |
| List related tasks | `lark_api({ tool: 'task', op: '+get-related-tasks', args: { ... } })` |
| Search tasks | `lark_api({ tool: 'task', op: '+search', args: { query: '...' } })` |
| Subscribe to events | `lark_api({ tool: 'task', op: '+subscribe-event', args: { ... } })` |
| Set/clear task ancestor | `lark_api({ tool: 'task', op: '+set-ancestor', args: { guid: '...', ... } })` |
| Create tasklist + batch add tasks | `lark_api({ tool: 'task', op: '+tasklist-create', args: { name: '...', ... } })` |
| Search tasklists | `lark_api({ tool: 'task', op: '+tasklist-search', args: { query: '...' } })` |
| Add tasks to a tasklist | `lark_api({ tool: 'task', op: '+tasklist-task-add', args: { tasklist_guid: '...', task_guids: [...] } })` |
| Manage tasklist members | `lark_api({ tool: 'task', op: '+tasklist-members', args: { tasklist_guid: '...', ... } })` |
| Upload task attachment | `lark_api({ tool: 'task', op: '+upload-attachment', args: { guid: '...', file_path: '...' } })` |

For reference docs on each shortcut, see: [`./references/lark-task-create.md`](./references/lark-task-create.md), [`./references/lark-task-update.md`](./references/lark-task-update.md), etc.

## API Resources

For available operations, use:
```
lark_api_search({ query: 'task <resource>' })
```

Key resources and their operations:

### tasks
```
lark_api({ tool: 'task', op: 'tasks.create', args: { ... } })
lark_api({ tool: 'task', op: 'tasks.delete', args: { guid: '...' } })
lark_api({ tool: 'task', op: 'tasks.get', args: { guid: '...' } })
lark_api({ tool: 'task', op: 'tasks.list', args: { ... } })
lark_api({ tool: 'task', op: 'tasks.patch', args: { guid: '...', ... } })
```

### tasklists
```
lark_api({ tool: 'task', op: 'tasklists.add_members', args: { tasklist_guid: '...', members: [...] } })
lark_api({ tool: 'task', op: 'tasklists.create', args: { ... } })
lark_api({ tool: 'task', op: 'tasklists.delete', args: { tasklist_guid: '...' } })
lark_api({ tool: 'task', op: 'tasklists.get', args: { tasklist_guid: '...' } })
lark_api({ tool: 'task', op: 'tasklists.list', args: { ... } })
lark_api({ tool: 'task', op: 'tasklists.patch', args: { tasklist_guid: '...', ... } })
lark_api({ tool: 'task', op: 'tasklists.remove_members', args: { tasklist_guid: '...', members: [...] } })
lark_api({ tool: 'task', op: 'tasklists.tasks', args: { tasklist_guid: '...' } })
```

### subtasks
```
lark_api({ tool: 'task', op: 'subtasks.create', args: { guid: '...', ... } })
lark_api({ tool: 'task', op: 'subtasks.list', args: { guid: '...' } })
```

### members
```
lark_api({ tool: 'task', op: 'members.add', args: { guid: '...', members: [...] } })
lark_api({ tool: 'task', op: 'members.remove', args: { guid: '...', members: [...] } })
```

### sections
```
lark_api({ tool: 'task', op: 'sections.create', args: { ... } })
lark_api({ tool: 'task', op: 'sections.delete', args: { section_guid: '...' } })
lark_api({ tool: 'task', op: 'sections.get', args: { section_guid: '...' } })
lark_api({ tool: 'task', op: 'sections.list', args: { ... } })
lark_api({ tool: 'task', op: 'sections.patch', args: { section_guid: '...', ... } })
lark_api({ tool: 'task', op: 'sections.tasks', args: { section_guid: '...' } })
```

### custom_fields
```
lark_api({ tool: 'task', op: 'custom_fields.create', args: { ... } })
lark_api({ tool: 'task', op: 'custom_fields.get', args: { custom_field_guid: '...' } })
lark_api({ tool: 'task', op: 'custom_fields.patch', args: { custom_field_guid: '...', ... } })
lark_api({ tool: 'task', op: 'custom_fields.list', args: { ... } })
lark_api({ tool: 'task', op: 'custom_fields.add', args: { ... } })
lark_api({ tool: 'task', op: 'custom_fields.remove', args: { ... } })
```

### custom_field_options
```
lark_api({ tool: 'task', op: 'custom_field_options.create', args: { ... } })
lark_api({ tool: 'task', op: 'custom_field_options.patch', args: { ... } })
```

### agent
```
lark_api({ tool: 'task', op: 'agent.update_agent_profile', args: { ... } })
lark_api({ tool: 'task', op: 'agent.register_agent', args: { ... } })
```

### agent_task_step_info
```
lark_api({ tool: 'task', op: 'agent_task_step_info.append_task_steps', args: { ... } })
```

## Permissions

| Method | Required scope |
|------|-----------|
| `tasks.create` | `task:task:write` |
| `tasks.delete` | `task:task:write` |
| `tasks.get` | `task:task:read` |
| `tasks.list` | `task:task:read` |
| `tasks.patch` | `task:task:write` |
| `tasklists.add_members` | `task:tasklist:write` |
| `tasklists.create` | `task:tasklist:write` |
| `tasklists.delete` | `task:tasklist:write` |
| `tasklists.get` | `task:tasklist:read` |
| `tasklists.list` | `task:tasklist:read` |
| `tasklists.patch` | `task:tasklist:write` |
| `tasklists.remove_members` | `task:tasklist:write` |
| `tasklists.tasks` | `task:tasklist:read` |
| `subtasks.create` | `task:task:write` |
| `subtasks.list` | `task:task:read` |
| `members.add` | `task:task:write` |
| `members.remove` | `task:task:write` |
| `sections.create` | `task:section:write` |
| `sections.delete` | `task:section:write` |
| `sections.get` | `task:section:read` |
| `sections.list` | `task:section:read` |
| `sections.patch` | `task:section:write` |
| `sections.tasks` | `task:section:read` |
| `custom_fields.create` | `task:custom_field:write` |
| `custom_fields.get` | `task:custom_field:read` |
| `custom_fields.patch` | `task:custom_field:write` |
| `custom_fields.list` | `task:custom_field:read` |
| `custom_fields.add` | `task:custom_field:write` |
| `custom_fields.remove` | `task:custom_field:write` |
| `custom_field_options.create` | `task:custom_field:write` |
| `custom_field_options.patch` | `task:custom_field:write` |
| `agent.update_agent_profile` | `task:task:write` |
| `agent.register_agent` | `task:task:write` |
| `agent_task_step_info.append_task_steps` | `task:task:write` |
| `+upload-attachment` | `task:attachment:write` |
