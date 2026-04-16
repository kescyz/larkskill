---
name: lark-task
version: 2.0.0
description: "Lark Tasks: manage tasks and tasklists via LarkSkill MCP. Create to-do tasks, view and update task status, split subtasks, organize tasklists, and assign collaborators. Use this skill when users need to create to-do items, view task lists, track task progress, manage project lists, or assign tasks to others."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# task (v2)

**CRITICAL - Before starting, read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which includes authentication and permission handling. LarkSkill MCP server must be connected.**

> **Search tip:** If user query only provides a task name (for example: "complete task Lobster One"), directly use `+get-my-tasks` with a query filter without the complete flag so both open and completed tasks can be matched.
> **Identity mapping:** In user identity mode, if user says "me" (for example: "assign to me"), resolve current logged-in user's `open_id` as the parameter value.
> **Terminology:** If user says "todo", interpret it as a likely "task" request and prefer this skill.
> **Friendly output:** Include task or tasklist `url` in your user-facing response when available.

> **Create/update notes:**
> 1. `repeat_rule` (repeat rule) and `reminder` (reminder time) can only be set when `due` (due time) is set.
> 2. If both `start` (start time) and `due` (due time) are set, start time must be less than or equal to due time.
> 3. When using tenant_access_token (app identity), you cannot add task members across tenants.

> **Query notes:**
> 1. When outputting task details, if you need to render person fields such as assignee or creator, besides showing the `id` (e.g. open_id), you must also attempt to fetch and display the person's real name through other means (e.g. calling the contacts skill) so users can identify them more easily.
> 2. When outputting task details, if you need to render time fields such as created time or due time, use local timezone for rendering (format: 2006-01-02 15:04:05).

## Shortcuts

Read the corresponding reference doc before calling `lark_api`.

- [`+create`](./references/lark-task-create.md) - Create a task
- [`+update`](./references/lark-task-update.md) - Update a task
- [`+comment`](./references/lark-task-comment.md) - Add a comment to a task
- [`+complete`](./references/lark-task-complete.md) - Complete a task
- [`+reopen`](./references/lark-task-reopen.md) - Reopen a task
- [`+assign`](./references/lark-task-assign.md) - Assign or remove members
- [`+followers`](./references/lark-task-followers.md) - Manage followers
- [`+reminder`](./references/lark-task-reminder.md) - Manage reminders
- [`+get-my-tasks`](./references/lark-task-get-my-tasks.md) - List tasks assigned to me
- [`+tasklist-create`](./references/lark-task-tasklist-create.md) - Create a tasklist and batch add tasks
- [`+tasklist-task-add`](./references/lark-task-tasklist-task-add.md) - Add existing tasks to tasklist
- [`+tasklist-members`](./references/lark-task-tasklist-members.md) - Manage tasklist members

## Intent → MCP call index

| Intent | MCP call | Note |
|--------|----------|------|
| Create task | `lark_api POST /open-apis/task/v2/tasks` | body: `{summary, description, due, members, ...}` |
| Get task | `lark_api GET /open-apis/task/v2/tasks/{task_guid}` | |
| Update task | `lark_api PATCH /open-apis/task/v2/tasks/{task_guid}` | body: `{task: {...}, update_fields: [...]}` |
| Delete task | `lark_api DELETE /open-apis/task/v2/tasks/{task_guid}` | |
| List my tasks | `lark_api GET /open-apis/task/v2/tasks` | params: `page_size, page_token, ...` |
| Complete task | `lark_api POST /open-apis/task/v2/tasks/{task_guid}/complete` | |
| Reopen task | `lark_api POST /open-apis/task/v2/tasks/{task_guid}/uncomplete` | |
| Add task members | `lark_api POST /open-apis/task/v2/tasks/{task_guid}/add_members` | body: `{members: [{id, type, role}]}` |
| Remove task members | `lark_api POST /open-apis/task/v2/tasks/{task_guid}/remove_members` | body: `{members: [{id, type, role}]}` |
| Add comment | `lark_api POST /open-apis/task/v2/tasks/{task_guid}/comments` | body: `{content}` |
| Create subtask | `lark_api POST /open-apis/task/v2/tasks/{task_guid}/subtasks` | body: `{summary, ...}` |
| List subtasks | `lark_api GET /open-apis/task/v2/tasks/{task_guid}/subtasks` | |
| Create tasklist | `lark_api POST /open-apis/task/v2/tasklists` | body: `{name, members}` |
| Get tasklist | `lark_api GET /open-apis/task/v2/tasklists/{tasklist_guid}` | |
| Update tasklist | `lark_api PATCH /open-apis/task/v2/tasklists/{tasklist_guid}` | body: `{tasklist: {...}, update_fields: [...]}` |
| Delete tasklist | `lark_api DELETE /open-apis/task/v2/tasklists/{tasklist_guid}` | |
| List tasklists | `lark_api GET /open-apis/task/v2/tasklists` | |
| Add task to tasklist | `lark_api POST /open-apis/task/v2/tasklists/{tasklist_guid}/add_task` | body: `{task_guid}` |
| List tasks in tasklist | `lark_api GET /open-apis/task/v2/tasklists/{tasklist_guid}/tasks` | |
| Add tasklist members | `lark_api POST /open-apis/task/v2/tasklists/{tasklist_guid}/add_members` | body: `{members: [{id, type, role}]}` |
| Remove tasklist members | `lark_api POST /open-apis/task/v2/tasklists/{tasklist_guid}/remove_members` | body: `{members: [{id, type, role}]}` |

## API Resources

### tasks

  - `create` - Create task
  - `delete` - Delete task
  - `get` - Get task detail
  - `list` - List tasks
  - `patch` - Update task

### tasklists

  - `add_members` - Add tasklist members
  - `create` - Create tasklist
  - `delete` - Delete tasklist
  - `get` - Get tasklist detail
  - `list` - List tasklists
  - `patch` - Update tasklist
  - `remove_members` - Remove tasklist members
  - `tasks` - List tasks in tasklist

### subtasks

  - `create` - Create subtask
  - `list` - List subtasks

### members

  - `add` - Add task member
  - `remove` - Remove task member

## Permission matrix

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
