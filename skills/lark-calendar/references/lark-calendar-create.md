# calendar +create

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Create an event and invite attendees as needed.

Required scopes: ["calendar:calendar.event:create","calendar:calendar.event:update"]

## Recommended call

Create event + invite attendees:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/calendars/primary/events
- body:
  {
    "summary": "product review",
    "start_time": { "timestamp": "1741586400" },
    "end_time": { "timestamp": "1741593600" },
    "attendee_ability": "can_modify_event",
    "free_busy_status": "busy",
    "reminders": [{ "minutes": 5 }]
  }
```

No attendees:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/calendars/primary/events
- body:
  {
    "summary": "lunch",
    "start_time": { "timestamp": "1741586400" },
    "end_time": { "timestamp": "1741590000" }
  }
```

Specify calendar:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/calendars/{calendar_id}/events
- body:
  {
    "summary": "team sync",
    "start_time": { "timestamp": "1741586400" },
    "end_time": { "timestamp": "1741590000" }
  }
```

## Add attendees (Step 2, using calendar_id and event_id from Step 1)

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees
- body:
  {
    "attendees": [
      { "type": "user", "user_id": "ou_xxx" },
      { "type": "user", "user_id": "ou_yyy" }
    ]
  }
```

## Rollback — Delete empty event if attendee add fails

```
Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}
- params: { "need_notification": false }
```

## API request details

```
POST   /open-apis/calendar/v4/calendars/{calendar_id}/events
POST   /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees
DELETE /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}
```

Use `primary` as `calendar_id` for the user's primary calendar.

## Parameters (event body)

| Parameter | Required | Description |
|------|------|------|
| `summary` | No | Event title. Note: title should not include time, location, or people info |
| `start_time` | Yes | Start time object: `{ "timestamp": "<unix_second_string>" }` for specific time, or `{ "date": "2026-03-12" }` for all-day |
| `end_time` | Yes | End time object, same format as `start_time` |
| `description` | No | Detailed event description |
| `location` | No | Location object: `{ "name": "5F-Large Conference Room" }` |
| `attendee_ability` | No | `can_modify_event` (attendees can see each other and edit) |
| `free_busy_status` | No | `busy` (default) or `free` |
| `reminders` | No | Array of reminder objects: `[{ "minutes": 5 }]` |
| `rrule` | No | Recurrence rule per RFC5545. Example: `"FREQ=DAILY;INTERVAL=1"`. COUNT and UNTIL cannot appear together |

> Full API command time parameters are **Unix second strings** (not ISO 8601).
> When manually splitting into two steps, keep the rollback-delete third step to avoid leaving empty events.

## Attendee Types

| `type` | `user_id` Format | Description |
|--------|---------------|------|
| `user` | `ou_xxx` (open_id) | Feishu user |
| `group` | `oc_xxx` | Feishu group |
| `resource` | `omm_xxx` | Meeting room |
| `third_party` | Email address | External attendee |

> [!CAUTION]
> This is a **write operation** - user intent must be confirmed before execution.

## References

- [lark-calendar](../SKILL.md) -- All calendar commands
- [lark-shared](../../lark-shared/SKILL.md) -- Authentication and global parameters
- [lark-calendar-suggestion](lark-calendar-suggestion.md) -- Smart free-slot recommendations
