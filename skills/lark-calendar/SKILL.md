---
name: lark-calendar
version: 2.0.0
description: "Feishu Calendar: comprehensive management for calendars and events (meetings). Core scenarios include viewing/searching events, creating/updating events, managing attendees, checking free/busy status, and recommending free slots. For high-frequency tasks, prefer shortcuts: +agenda (quick overview of today/recent schedule), +create (create event and optionally invite attendees), +freebusy (query free/busy and RSVP status on a user's primary calendar), +rsvp (reply to event invitations), +suggestion (for scheduling requests with uncertain time, provide multiple recommended time options)."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# calendar (v4)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

**CRITICAL - Before executing any Shortcut, you must first use Read to read its corresponding reference document. Never call operations blindly.**

## Core Scenarios

The calendar skill includes the following core scenarios:

### 1. Schedule an Event

This is the most important scenario of the calendar skill. The goal is to help users schedule with low effort.

> **💡 Core principle: be an intelligent assistant that supports decision-making, not a form filler or a decision maker for users.**

**Time and Date Inference Rules:**
To ensure accuracy, strictly follow these rules when inferring time:
- **Definition of week**: Monday is the first day of the week, Sunday is the last day. When calculating relative dates like `next Monday`, always compute based on the real current date and weekday baseline.
- **Range of a day**: when users mention broad day expressions like `tomorrow` or `today`, the default time range should cover the full day. **Do not** shrink the query range on your own, to avoid missing evening schedules.
- **Past-time constraint**: do not schedule events that have fully passed. The only exception is an event that spans the current time, where start is in the past but end is in the future.

**Scheduling Workflow:**

1. **Intelligently infer defaults**
   - Title, attendees, and duration all have defaults, so avoid frequent confirmation prompts.
   - **Attendees**: if no one else is explicitly specified, default attendee is **only the user**. When searching specific attendees (person, group, room) returns multiple ambiguous matches, you must ask user to choose and record that preference as long-term memory for future auto recognition.
   - **Meeting room**: proactive room booking is currently unsupported, unless a corresponding room ID (`omm_` prefix) already exists in current context and needs to be added into the event.
   - **Title**: auto-generate based on conversation context. If not inferable, default to "meeting".
   - **Duration**: dynamically infer from meeting type and context. If not inferable, default to 30 minutes.

2. **Time recommendation and decision support (core experience)**
   - **With exact time point** (for example `tomorrow 10am`): call `+freebusy` [lark-calendar-freebusy](references/lark-calendar-freebusy.md) to check free/busy status for attendees first. Note: if an attendee has RSVP status declined for an existing event, treat that slot as free. If no conflicts, proceed directly to confirmation and creation. If conflicts exist, inform user and ask whether to continue or pick another time.
   - **With time range** (for example `tomorrow`, `afternoon`, `this week`): call `+suggestion` [lark-calendar-suggestion](references/lark-calendar-suggestion.md) to get **multiple recommended time options** for all attendees within that range. You **must wait for user confirmation of one option** before creating the event. Once user chooses a recommended option, **do not query free/busy again**.
   - **Without any time info**: infer a reasonable default range (such as "today" or "next two days"), then also provide **multiple recommended time options** for quick selection.
   - **Lifestyle scenarios** (such as gym, swimming, walking, meal plans, milk tea; note "coffee chat" counts as work scenario): expected to **not call** `suggestion`. Infer a suitable non-working time and confirm with user. If not inferable, proactively ask user, then store preference memory for future direct reuse.
   - **Ambiguity resolution and long-term memory building (Aha Moment)**: for user-specific time phrases (such as "after work starts", "before getting off work") or ambiguous 12-hour time contexts (no AM/PM), never assume. Clarify proactively, then persist personalized definitions as long-term preference.

3. **Non-blocking execution**
   - After user confirms a concrete time option, read [`+create`](references/lark-calendar-create.md) and call the create event API.

4. **Friendly feedback**
   - Report result by returning created event summary.

## Core Concepts

- **Calendar**: container of events. Each user has a primary calendar and can create or subscribe to shared calendars.
- **Event**: a single event item in a calendar, with attributes such as start/end time, location, title, and attendees. Supports one-time and recurring events, following RFC5545 iCalendar standard.
- ***All-day Event***: occupies date-only range without specific times, and end date is inclusive.
- **Instance**: a concrete time instance of an event, essentially expanded from events. Normal events and exception events map to one instance, recurring events map to N instances. When querying by time range, instance view can expand recurring events into standalone instances for accurate timeline display and management.
- **Rrule (Recurrence Rule)**: defines recurrence pattern, for example `FREQ=DAILY;UNTIL=20230307T155959Z;INTERVAL=14` means repeats every 14 days.
- **Exception**: an occurrence in a recurring event series that differs from base recurrence.
- **Attendee**: participant of an event, such as user, group, room resource, or external email address. Each attendee has independent RSVP status.
- **RSVP**: attendee response status for an invitation (accept/decline/tentative).
- **FreeBusy**: query user free/busy status in a specific time range for meeting coordination.

## Resource Relationship

```
Calendar
└── Event (schedule)
    ├── Attendee (Participant)
    └── Reminder (reminder)
```

## Shortcuts (Read Reference First)

Read the reference doc before using any shortcut.

| Shortcut | Description |
|----------|------|
| [`+agenda`](references/lark-calendar-agenda.md) | View agenda (today by default) |
| [`+create`](references/lark-calendar-create.md) | Create event and invite attendees (ISO 8601 time) |
| [`+freebusy`](references/lark-calendar-freebusy.md) | Query primary-calendar free/busy and RSVP status |
| [`+rsvp`](references/lark-calendar-rsvp.md) | Reply to an event (accept/decline/tentative) |
| [`+suggestion`](references/lark-calendar-suggestion.md) | For scheduling requests with uncertain time, provide multiple recommended options |

## +suggestion Usage

Before calling `+suggestion`, you must read [lark-calendar-suggestion](references/lark-calendar-suggestion.md). Never call directly.

Recommended call example — get suggestions for a 30-minute meeting:

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/freebusy/list
- body:
  {
    "time_min": "2026-03-10T00:00:00+08:00",
    "time_max": "2026-03-10T11:00:00+08:00",
    "user_id_list": ["ou_xxx", "ou_yyy"]
  }
```

(Full suggestion flow is documented in [lark-calendar-suggestion](references/lark-calendar-suggestion.md))

## API Resources

All calendar APIs use the base path `/open-apis/calendar/v4/`.

### calendars

- `create` — `POST /open-apis/calendar/v4/calendars`
- `delete` — `DELETE /open-apis/calendar/v4/calendars/{calendar_id}`
- `get` — `GET /open-apis/calendar/v4/calendars/{calendar_id}`
- `list` — `GET /open-apis/calendar/v4/calendars`
- `patch` — `PATCH /open-apis/calendar/v4/calendars/{calendar_id}`
- `primary` — `POST /open-apis/calendar/v4/calendars/primary`
- `search` — `POST /open-apis/calendar/v4/calendars/search`

### event.attendees

- `batch_delete` — `DELETE /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees/batch_delete`
- `create` — `POST /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees`
- `list` — `GET /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees`

### events

- `create` — `POST /open-apis/calendar/v4/calendars/{calendar_id}/events`
- `delete` — `DELETE /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}`
- `get` — `GET /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}`
- `instance_view` — `GET /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/instance_view`
- `patch` — `PATCH /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}`
- `search` — `POST /open-apis/calendar/v4/calendars/{calendar_id}/events/search`

### freebusys

- `list` — `POST /open-apis/calendar/v4/freebusy/list`

## Permission Table

| Method | Required Scope |
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

**Note (Mandatory):**
- When converting between date/time strings and timestamps, you must use external tools such as system commands or scripts to guarantee absolute conversion accuracy. Violations will cause severe logic errors.
