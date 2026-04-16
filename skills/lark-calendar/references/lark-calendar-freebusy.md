# calendar +freebusy

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Query free/busy information on a user's primary calendar and return the list of busy slots and RSVP status in a specified time range.

Required scopes: ["calendar:calendar.free_busy:read"]

## Recommended call

Query the current user's free/busy today (default):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/freebusy/list
- body:
  {
    "time_min": "<today_start_iso8601>",
    "time_max": "<today_end_iso8601>"
  }
```

Custom time range:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/freebusy/list
- body:
  {
    "time_min": "2026-03-11T00:00:00+08:00",
    "time_max": "2026-03-12T00:00:00+08:00"
  }
```

Query for a specific working time period:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/freebusy/list
- body:
  {
    "time_min": "2026-03-11T08:00:00+08:00",
    "time_max": "2026-03-11T18:00:00+08:00"
  }
```

Query a specific user's free/busy (requires `user_id_list`):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/freebusy/list
- body:
  {
    "time_min": "2026-03-11T00:00:00+08:00",
    "time_max": "2026-03-12T00:00:00+08:00",
    "user_id_list": ["ou_xxx"]
  }
```

## API request details

```
POST /open-apis/calendar/v4/freebusy/list
```

## Parameters (body)

| Parameter | Required | Description |
|------|------|------|
| `time_min` | Yes | Query start time (ISO 8601, default is today start) |
| `time_max` | Yes | Query end time (ISO 8601) |
| `user_id_list` | No | Target user ID list (`ou_` prefix). If omitted, queries currently logged-in user. Required when calling as bot identity |

## Time Formats

`time_min` and `time_max` accept ISO 8601 format:

| Format | Example | Description |
|------|------|------|
| ISO 8601 | `2026-03-11T09:00:00+08:00` | Full format with timezone |
| Date only | `2026-03-11` | Interpreted as start of day |

> **Mandatory**: When converting between date/time strings and timestamps, use external tools or scripts to guarantee accuracy.

## Output Examples

### Table format

```
start             end               rsvp_status
----------------  ----------------  -----------
2026-03-11 10:00 2026-03-11 10:30 Accept
2026-03-11 14:00 2026-03-11 15:00 To be determined

2 busy periods in total
```

### JSON format

```json
[
  {
    "start_time": "2026-03-11T10:00:00+08:00",
    "end_time": "2026-03-11T10:30:00+08:00",
    "rsvp_status": "accept"
  },
  {
    "start_time": "2026-03-11T14:00:00+08:00",
    "end_time": "2026-03-11T15:00:00+08:00",
    "rsvp_status": "tentative"
  }
]
```

## Typical Scenarios

### Find available slots for meetings

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/freebusy/list
- body:
  {
    "time_min": "2026-03-11T08:00:00+08:00",
    "time_max": "2026-03-11T18:00:00+08:00"
  }
```

### Check team member availability

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/freebusy/list
- body:
  {
    "time_min": "2026-03-12T00:00:00+08:00",
    "time_max": "2026-03-13T00:00:00+08:00",
    "user_id_list": ["ou_member_a", "ou_member_b"]
  }
```

## Notes

1. **Primary calendar only** - this operation only returns free/busy from the user primary calendar, not other subscribed calendars.
2. **Privacy protection** - only returns busy slot start/end times, not event details such as title/description.
3. **Bot identity** - bot must specify `user_id_list`.

## Comparison with Other Commands

| Command | Purpose | Output |
|------|------|----------|
| `calendar +freebusy` | Query free/busy slots | Returns only busy slot list (no event details) |
| `calendar +agenda` | View agenda | Returns full event list (including title, description, etc.) |

**Selection guidance:**
- **Only need to know if time is available** - use `+freebusy` (faster and privacy-friendly)
- **Need full event details** - use `+agenda`

## References

- [lark-calendar-agenda](lark-calendar-agenda.md) - View agenda
- [lark-calendar-create](lark-calendar-create.md) - Create events
- [lark-calendar-suggestion](lark-calendar-suggestion.md) - Provide multiple recommended time options
- [lark-calendar](../SKILL.md) - Full calendar API
