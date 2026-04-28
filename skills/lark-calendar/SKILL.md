---
name: lark-calendar
version: 2.0.0
description: "Lark Calendar via LarkSkill MCP: view/search/create/update events, manage attendees, query free/busy, suggest free slots, book meeting rooms. When scheduling or booking rooms, MUST first read references/lark-calendar-schedule-meeting.md. Prefer Shortcuts: +agenda, +create, +freebusy, +rsvp."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# calendar

## Prerequisites

- LarkSkill MCP server connected (install via `/plugin marketplace add kescyz/larkskill` → `/plugin install larkskill`, or see https://portal.larkskill.app/setup)
- MCP tools available: `lark_api`, `lark_api_search`
- Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first for auth, global flags, and safety rules

**CRITICAL — Before executing any Shortcut, always read its corresponding reference doc; do NOT blindly invoke commands.**
**CRITICAL — Whenever the request involves scheduling events/meetings or querying/searching meeting rooms, the first step you MUST take is to read [`references/lark-calendar-schedule-meeting.md`](references/lark-calendar-schedule-meeting.md). DO NOT skip this step and call the API or Shortcut directly!**
**CRITICAL — Terminology constraint: when users colloquially say "help me schedule a calendar" or "check today's calendar", their actual intent is usually to create or query an event (Event), not to operate the calendar (Calendar) container itself. Automatically map colloquial "calendar" intent to "event" operations (such as `+create`, `+agenda`).**
**CRITICAL — Intent routing for meetings vs. events:**
- **Querying past meetings**: if the user explicitly queries past meetings (e.g. "yesterday's meeting", "last week's meeting"), **prefer using [`../lark-vc/SKILL.md`](../lark-vc/SKILL.md) to search meeting records**. Meeting data includes both events-originated video meetings and ad-hoc meetings; querying only event data leads to incomplete results.
- **Querying calendars/events or future meetings**: if the user explicitly mentions "calendar", "event", or any **future-time** arrangement, it falls within this skill's (lark-calendar) domain — continue using this skill.

## Time and date inference rules

To ensure accuracy, strictly follow these rules whenever time inference is involved:
- **Definition of week**: Monday is the first day of the week, and Sunday is the last day. When computing relative dates such as "next Monday", always base the calculation on the current real date and weekday so the date is not miscalculated.
- **Range of a day**: when the user mentions "tomorrow", "today", or any generic single day, the time range should default to the entire day. **DO NOT** unilaterally narrow the query window, otherwise evening arrangements may be missed.
- **Historical-time constraint**: events fully in the past cannot be scheduled. The only exception is "spans the current time" events — events whose start time is in the past but end time is in the future.

## Core scenarios

### 1. Schedule events/meetings, query/search available meeting rooms

**BLOCKING REQUIREMENT: Whenever the user's intent involves "schedule events/meetings" or "query/search available meeting rooms", you MUST stop other thinking immediately and fully read [`references/lark-calendar-schedule-meeting.md`](references/lark-calendar-schedule-meeting.md)! Before reading this file, DO NOT execute any event creation or meeting room query operation.**
**CRITICAL: Subsequent operations MUST strictly follow the workflow defined in the doc above. When handling this scenario, default to acting as an "intelligent assistant", not a "form-filling robot". Auto-fill defaults where possible; only ask back when there is a time conflict, the result cannot be uniquely determined, or there is time-semantic ambiguity.**
**CRITICAL: Execution order MUST be fixed: first auto-fill defaults, then check whether the time is explicit, then enter the "explicit time" or "fuzzy time / no time info" branch. DO NOT skip steps.**
**CRITICAL: When time is explicit and a meeting room is needed, call `+room-find` first, then `+freebusy`; when time is fuzzy or absent, call `+suggestion` first, and if a meeting room is needed, batch-call `+room-find` afterwards.**
**CRITICAL: When the user says "find a meeting room", "look for a meeting room", "search for available meeting rooms", or "recommend a frequently used meeting room", the default intent is to query meeting room availability — NOT to query the meeting room resource directory, and definitely NOT to pull historical events for statistical analysis. The full rules are governed by [lark-calendar-schedule-meeting.md](references/lark-calendar-schedule-meeting.md).**
**BLOCKING REQUIREMENT: Even if the user's core need is "find a meeting room", as long as no explicit start/end time is provided, DO NOT call `+room-find` directly! You MUST first enter the "no time / fuzzy time" branch, call `+suggestion` to get candidate time blocks, and then pass those time blocks to `+room-find`.**
**BLOCKING REQUIREMENT: Whenever a time-plan or meeting-room-plan choice is required (such as fuzzy time, no time, or meeting room needed), before calling `+create` to create the event, you MUST first present the candidate options to the user and wait for explicit confirmation. DO NOT make decisions on behalf of the user.**

## Core concepts

- **Calendar**: container for events. Each user has one primary calendar, and may also create or subscribe to shared calendars.
- **Event**: a single event in a calendar, including start/end time, location, title, attendees, and other attributes. Supports single and recurring events; follows the RFC5545 iCalendar standard.
- ***All-day Event***: an event that only occupies dates, without specific start/end times — the end date is inclusive.
- **Instance**: a concrete time instance of an event; essentially the expansion of an event. A normal or exception event corresponds to 1 Instance, while a recurring event corresponds to N Instances. When querying by time range, the instance view can expand recurring events into independent instances for accurate timeline display and management.
- **Recurrence Rule (Rrule)**: defines the repetition rule of a recurring event. For example, `FREQ=DAILY;UNTIL=20230307T155959Z;INTERVAL=14` means "repeats every 14 days".
- **Exception event**: an event in a recurring series that diverges from the original recurring event.
- **Attendee**: a participant in the event. Can be a user, group, meeting room resource, external email address, etc. Each attendee has independent RSVP status.
- **RSVP**: an attendee's reply status to an event invitation (accept/decline/tentative).
- **FreeBusy**: queries the user's busy/free status within a specified time range, used for meeting time coordination.
- **Room**: "room" does not mean "a generic room" — it specifically means "meeting room". Always map "room" to "meeting room" and its related operations when interpreting and handling intent.
- **Time Slot / Time Block**: a **specific and definite** continuous time segment (e.g. `14:00~15:00`). In this doc it is strictly distinct from a generic "time range/interval" (e.g. "this afternoon", "next week"). For booking, querying available meeting rooms, or any concrete operation, you MUST use a definite "time block", not a fuzzy "time range".

## Resource hierarchy

```
Calendar
└── Event
    ├── Attendee
    └── Reminder
```

## Shortcuts (recommended — prefer these)

A Shortcut is a high-level wrapper for common operations. Prefer the Shortcut whenever one exists for the operation. Each Shortcut maps to a `lark_api` invocation with `tool: 'calendar'` and the op listed below.

| Shortcut | Description |
|----------|------|
| [`+agenda`](references/lark-calendar-agenda.md) | View calendar agenda (defaults to today) |
| [`+create`](references/lark-calendar-create.md) | Create an event and invite attendees (ISO 8601 time) |
| [`+freebusy`](references/lark-calendar-freebusy.md) | Query the user's primary calendar free/busy info and RSVP status |
| [`+room-find`](references/lark-calendar-room-find.md) | Find available meeting rooms for one or more **explicit** time blocks (**when no explicit time is provided, DO NOT call directly — go through `+suggestion` first**) |
| [`+rsvp`](references/lark-calendar-rsvp.md) | Reply to an event (accept/decline/tentative) |
| [`+suggestion`](references/lark-calendar-suggestion.md) | Recommend multiple available time-block candidates based on a fuzzy time or a time range |

### Shortcut invocation examples

```
lark_api({ tool: 'calendar', op: 'agenda', args: { date: '2026-04-28' } })
lark_api({ tool: 'calendar', op: 'create', args: { title: 'Sync', start: '2026-04-29T09:00:00+08:00', end: '2026-04-29T10:00:00+08:00', attendees: ['ou_xxx'] } })
lark_api({ tool: 'calendar', op: 'freebusy', args: { user_ids: ['ou_xxx'], start: '...', end: '...' } })
lark_api({ tool: 'calendar', op: 'room-find', args: { time_blocks: [{ start: '...', end: '...' }] } })
lark_api({ tool: 'calendar', op: 'rsvp', args: { event_id: 'evt_xxx', reply: 'accept' } })
lark_api({ tool: 'calendar', op: 'suggestion', args: { time_range: { start: '...', end: '...' }, duration_minutes: 60 } })
```

## Meeting room rules

- **A meeting room is a resource attendee of an event — it cannot exist or be booked independently of an event.**
- **Whenever the user's intent is "book/query/search available meeting rooms", you MUST enter the `references/lark-calendar-schedule-meeting.md` workflow.**
- The time input of `+room-find` MUST be a **definite time block**, not a time-range search.
- **Mandatory constraint: if the user only asks to "query meeting rooms" but does NOT provide an explicit time, you MUST first call `+suggestion` to get available time blocks, then hand those blocks to `+room-find` for batch query. DO NOT guess a time and blindly call `+room-find`.**

## Native API resources

When a Shortcut does not cover the case, fall back to the native API via `lark_api`. **Always inspect parameter shape before calling — do not guess field formats.**

### calendars

| Op | Description | API |
|----|-------------|-----|
| `create` | Create a shared calendar | `lark_api POST /open-apis/calendar/v4/calendars` |
| `delete` | Delete a shared calendar | `lark_api DELETE /open-apis/calendar/v4/calendars/{calendar_id}` |
| `get` | Query calendar info | `lark_api GET /open-apis/calendar/v4/calendars/{calendar_id}` |
| `list` | Query the calendar list | `lark_api GET /open-apis/calendar/v4/calendars` |
| `patch` | Update calendar info | `lark_api PATCH /open-apis/calendar/v4/calendars/{calendar_id}` |
| `primary` | Query the user's primary calendar | `lark_api POST /open-apis/calendar/v4/calendars/primary` |
| `search` | Search calendars | `lark_api POST /open-apis/calendar/v4/calendars/search` |

### event.attendees

| Op | Description | API |
|----|-------------|-----|
| `batch_delete` | Remove event attendees | `lark_api POST /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees/batch_delete` |
| `create` | Add event attendees | `lark_api POST /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees` |
| `list` | List event attendees | `lark_api GET /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees` |

### events

| Op | Description | API |
|----|-------------|-----|
| `create` | Create an event | `lark_api POST /open-apis/calendar/v4/calendars/{calendar_id}/events` |
| `delete` | Delete an event | `lark_api DELETE /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}` |
| `get` | Get an event | `lark_api GET /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}` |
| `instance_view` | Query event instance view | `lark_api GET /open-apis/calendar/v4/calendars/{calendar_id}/events/instance_view` |
| `patch` | Update an event | `lark_api PATCH /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}` |
| `search` | Search events | `lark_api POST /open-apis/calendar/v4/calendars/{calendar_id}/events/search` |

### freebusys

| Op | Description | API |
|----|-------------|-----|
| `list` | Query primary calendar free/busy info | `lark_api POST /open-apis/calendar/v4/freebusy/list` |

## Permission table

| Method | Required scope |
|------|-----------|
| `calendars.create` | `calendar:calendar:create` |
| `calendars.delete` | `calendar:calendar:delete` |
| `calendars.get` | `calendar:calendar:read` |
| `calendars.list` | `calendar:calendar:read` |
| `calendars.patch` | `calendar:calendar:update` |
| `calendars.primary` | `calendar:calendar:read` |
| `calendars.search` | `calendar:calendar:read` |
| `event.attendees.batch_delete` | `calendar:calendar.event:update` |
| `event.attendees.create` | `calendar:calendar.event:update` |
| `event.attendees.list` | `calendar:calendar.event:read` |
| `events.create` | `calendar:calendar.event:create` |
| `events.delete` | `calendar:calendar.event:delete` |
| `events.get` | `calendar:calendar.event:read` |
| `events.instance_view` | `calendar:calendar.event:read` |
| `events.patch` | `calendar:calendar.event:update` |
| `events.search` | `calendar:calendar.event:read` |
| `freebusys.list` | `calendar:calendar.free_busy:read` |

**Note (mandatory):**
- Whenever converting between date/time strings and timestamps, you MUST call a system command or script-based external tool to perform the conversion, to ensure absolute accuracy. Violations will cause severe logical errors!
