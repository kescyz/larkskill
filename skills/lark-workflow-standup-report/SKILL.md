---
name: lark-workflow-standup-report
version: 2.0.0
description: "Schedule and task summary via LarkSkill MCP: orchestrates calendar agenda and task queries to generate a schedule plus incomplete-task summary for a specified date. Use this skill when you want to understand plans for today/tomorrow/this week."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# Schedule and Task Summary Workflow

**CRITICAL — before you start, you MUST first use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling. The LarkSkill MCP server must be connected.**

## Applicable Scenarios

- "What is on my schedule today" / "Today's schedule and tasks"
- "What meetings tomorrow" / "Tomorrow's schedule and incomplete tasks"
- "Help me see what I need to do today" / "Morning brief"
- "Kickoff summary" / "standup report"
- "What arrangements remain this week"

## Prerequisites

Only supports **user identity** (`as: "user"`). Before executing, ensure you are authorized for these scopes:
- `calendar:calendar.event:read` — for calendar events
- `task:task:read` — for tasks

## Workflow

```
{date} ─┬─► calendar agenda [start/end]                  ──► Schedule list (meeting/event)
        └─► task get-my-tasks (complete: false) [due_end] ──► Incomplete to-do list
                    │
                    ▼
              AI Summary (Time Conversion + Conflict Detection + Sorting) ──► Summary
```

### Step 1: Get Schedule

```
# Today (default, no extra parameters needed)
lark_api({ tool: 'calendar', op: 'agenda', args: {}, as: 'user' })

# Specify a date range (MUST use ISO 8601 format; natural language like "tomorrow" is not supported)
lark_api({
  tool: 'calendar',
  op: 'agenda',
  args: { start: '2026-03-26T00:00:00+08:00', end: '2026-03-26T23:59:59+08:00' },
  as: 'user'
})
```

> **Note**: `start` / `end` only support ISO 8601 format (e.g. `2026-01-01` or `2026-01-01T15:04:05+08:00`) and Unix timestamp. They **do not support** natural language like `"tomorrow"` or `"next monday"`. The AI must compute the target date from the current date.

Output includes: event\_id, summary, start\_time (with timestamp + timezone), end\_time, free\_busy\_status, self\_rsvp\_status.

### Step 2: Get Incomplete Tasks

```
# Default pending summary: MUST explicitly filter for incomplete tasks (complete: false, up to 20)
lark_api({ tool: 'task', op: 'get-my-tasks', args: { complete: false }, as: 'user' })

# Only view incomplete tasks due before a given date (recommended for summary scenarios, reduces data volume)
lark_api({
  tool: 'task',
  op: 'get-my-tasks',
  args: { complete: false, due_end: '2026-03-27T23:59:59+08:00' },
  as: 'user'
})

# Get all incomplete tasks (when there are more than 20)
lark_api({ tool: 'task', op: 'get-my-tasks', args: { complete: false, page_all: true }, as: 'user' })
```

> **Note**: without `complete: false`, `get-my-tasks` returns **both completed and incomplete tasks**, which would show completed tasks as "to-do" items in the summary. For standup / daily-report pending summary scenarios you **MUST** explicitly pass `complete: false`; do not omit it. The summary must list **only incomplete tasks**.
>
> For data-volume reasons, additional filtering is also recommended:
> - use `due_end` to filter tasks due before the target date
> - if you also need tasks without a due date, you can omit `due_end`, but during the AI summary show only tasks **created within the past 30 days**, and fold the rest as "other N historical to-do items"
>
> If you need a task operation not exposed by the `task` tool ops above, discover it with `lark_api_search` before falling back.

### Step 3: AI Summary

Combine the results from Step 1 and Step 2, then output in the following structure:

```
## {Date} Summary ({YYYY-MM-DD Week X})

### Schedule
| Time | Event | Organizer | Status |
|------|-------|-----------|--------|
| 09:00-10:00 | Product requirements review | Zhang San | Accepted |
| 14:00-15:00 | Technical solution discussion | Li Si | Pending confirmation |

### To-do list
- [ ] {task_summary} (due: {due_date})
- [ ] {task_summary}

### Summary
- {n} meetings in total, {m} items to be done
- Conflict reminder: {list schedules with overlapping time}
- Free periods: {free_slots} (calculated based on schedule)
```

**Data processing rules:**

1. **Time conversion**: API returns Unix timestamps; convert to `HH:mm` format based on the `timezone` field (typically `Asia/Shanghai`)
2. **RSVP status mapping**:
   | API Value | Display |
   |-----------|---------|
   | `accept` | Accepted |
   | `decline` | Declined |
   | `needs_action` | Pending confirmation |
   | `tentative` | Tentative |
3. **Schedule sorting**: sort by start time ascending
4. **Conflict detection**: after sorting by time, check whether adjacent schedules overlap (previous end\_time > next start\_time); if so, list the conflict groups in the summary
5. **Declined schedules**: mark as "declined" but do not count them in busy slots or conflict detection
6. **Task sorting**: sort by due time ascending; mark overdue tasks as "overdue"; tasks without a due time come last

## Permission Table

| Operation | Required Scope |
|-----------|---------------|
| `calendar` / `agenda` | `calendar:calendar.event:read` |
| `task` / `get-my-tasks` | `task:task:read` |

## References

- [lark-shared](../lark-shared/SKILL.md) — authentication and permissions (required)
- [lark-calendar](../lark-calendar/SKILL.md) — detailed `agenda` usage
- [lark-task](../lark-task/SKILL.md) — detailed `get-my-tasks` usage
