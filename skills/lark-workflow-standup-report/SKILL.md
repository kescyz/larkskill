---
name: lark-workflow-standup-report
version: 2.0.0
description: "Schedule and task summary via LarkSkill MCP: orchestrates calendar agenda and task queries to generate a daily schedule plus incomplete-task summary for a specified date. Suitable for checking plans for today/tomorrow/this week."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# Schedule and Task Summary Workflow (v2)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## Applicable Scenarios

- "What is on my schedule today" / "Today's schedule and tasks"
- "What meetings tomorrow" / "Tomorrow's schedule and incomplete tasks"
- "Help me see what I need to do today" / "Morning brief"
- "Kickoff summary" / "standup report"
- "What arrangements remain this week"

## Prerequisites

Only supports **user identity** (`as: "user"`). Required scopes:
- `calendar:calendar.event:read` — for calendar events
- `task:task:read` — for tasks

## Workflow

```
{date} ─┬─► calendar events list [start/end] ──► Agenda list (meeting/event)
        └─► task list [due_end] ──► Unfinished to-do list
                    │
                    ▼
              AI Summary (Time Conversion + Clash Detection + Sorting) ──► Summary
```

### Step 1: Get Schedule

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/calendar/v4/calendars/primary/events
- params:
  {
    "start_time": "<unix_timestamp_or_ISO8601>",
    "end_time": "<unix_timestamp_or_ISO8601>"
  }
- as: user
```

> **Note**: `start_time` / `end_time` accept ISO 8601 (e.g. `2026-01-01` or `2026-01-01T15:04:05+08:00`) and Unix timestamp. They **do not support** natural language like "tomorrow". Compute target dates from the current date.

Output includes: event_id, summary, start_time (timestamp + timezone), end_time, free_busy_status, self_rsvp_status.

### Step 2: Get Incomplete Tasks

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/task/v2/tasks
- params:
  {
    "due_to": "<ISO8601_timestamp>",
    "completed": false,
    "page_size": 20
  }
- as: user
```

> **Note**: without filters, response may contain many historical tasks (30+, 100KB+), which can exceed context limits. For summary scenarios:
> - use `due_to` to filter tasks due before the target date
> - if tasks without due date are also needed, skip filtering, but in AI summary show only tasks **created within past 30 days**, and fold the rest as "other N historical tasks"

### Step 3: AI Summary

Combine results from Step 1 and Step 2, then output in this structure:

```
## {Date} Summary ({YYYY-MM-DD Week X})

### Schedule
| Time | Event | Organizer | Status |
|------|-------|-----------|--------|
| 09:00-10:00 | Product requirements review | Zhang San | Accepted |
| 14:00-15:00 | Technical solution discussion | Li Si | To be confirmed |

### To-do list
- [ ] {task_summary} (due: {due_date})
- [ ] {task_summary}

### Summary
- {n} meetings in total, {m} items to be done
- Conflict reminder: {List schedules with overlapping time}
- Free periods: {free_slots} (calculated based on schedule)
```

**Data processing rules:**

1. **Time conversion**: API returns Unix timestamps. Convert to `HH:mm` based on `timezone` field (typically `Asia/Shanghai`)
2. **RSVP mapping**:
   | API Value | Display |
   |-----------|---------|
   | `accept` | Accepted |
   | `decline` | Declined |
   | `needs_action` | Pending confirmation |
   | `tentative` | Tentative |
3. **Schedule sorting**: sort by start time ascending
4. **Conflict detection**: after sorting by time, check adjacent events for overlap (`previous end_time > next start_time`). If overlaps exist, list conflict groups in summary
5. **Declined events**: mark as "declined" but do not include in busy-slot calculation or conflict detection
6. **Task sorting**: sort by due time ascending. Mark overdue tasks as "overdue". Tasks without due date come last

## Permission Table

| Operation | Required Scope |
|-----------|---------------|
| calendar events list | `calendar:calendar.event:read` |
| task list | `task:task:read` |

## References

- [lark-shared](../lark-shared/SKILL.md) — Authentication and permissions (required)
- [lark-calendar](../lark-calendar/SKILL.md) — Detailed calendar agenda operations
- [lark-task](../lark-task/SKILL.md) — Detailed task list operations
