# calendar +agenda

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

View recent schedules. Read-only operation that does not modify any event.

Required scopes: ["calendar:calendar.event:read"]

## Recommended call

View today's schedule (default):
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/calendar/v4/calendars/primary/events
- params:
  {
    "start_time": "<today_start_unix_timestamp>",
    "end_time": "<today_end_unix_timestamp>"
  }
```

Custom time range:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/calendar/v4/calendars/primary/events
- params:
  {
    "start_time": "1741564800",
    "end_time": "1742169600"
  }
```

Specify calendar:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/calendar/v4/calendars/{calendar_id}/events
- params:
  {
    "start_time": "<start_unix_timestamp>",
    "end_time": "<end_unix_timestamp>"
  }
```

## API request details

```
GET /open-apis/calendar/v4/calendars/{calendar_id}/events
```

Use `primary` as `calendar_id` for the user's primary calendar.

## Parameters (query)

| Parameter | Required | Description |
|------|------|------|
| `start_time` | No | Start time (Unix second timestamp, default today start) |
| `end_time` | No | End time (Unix second timestamp, defaults to end of same day as `start_time`) |
| `calendar_id` | No (path) | Calendar ID (use `primary` for default) |

## Time Formats

Convert time expressions to Unix second timestamps before passing:

| Format | Example | Description |
|------|------|------|
| ISO 8601 | `2026-03-10T14:00:00+08:00` | Convert to Unix timestamp |
| Date only | `2026-03-10` | start uses 00:00:00, end uses 23:59:59 |
| Unix timestamp | `1741564800` | Use directly |

> **Mandatory**: When converting between date/time strings and timestamps, use external tools or scripts to guarantee accuracy.

## Output Format

**Organize results as a readable schedule table:**

```
## 2026-03-10 Monday

09:00 - 09:30 Stand-up meeting
10:00 - 11:00 Product Review
14:00 - 15:00 1:1 with Alice

## 2026-03-11 Tuesday

(no events)
```

**Note: group by date and sort strictly by start time ascending (earliest to latest timeline).** Show title and duration.

## Tips

- Cancelled events are auto-filtered by the API, no extra handling needed.
- If no events, tell user "agenda is clear".
- Time ranges larger than 40 days should be split into multiple calls and merged.
- To view multiple calendars: list calendars first via `GET /open-apis/calendar/v4/calendars`, then query each one.

## References

- [lark-calendar](../SKILL.md) -- All calendar commands
- [lark-shared](../../lark-shared/SKILL.md) -- Authentication and global parameters
