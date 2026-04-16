# calendar +rsvp

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Reply to a specified event, updating the current user's RSVP status (accept, decline, or tentative).

Required scopes: `["calendar:calendar.event:reply"]`

## When to use

Call this shortcut when the user wants to respond to a calendar invitation — accept, decline, or mark as tentative.

Before calling, obtain the `event_id` (and optionally `calendar_id`) via `+agenda` or another listing shortcut.

## Recommended call

Step 1 — Get primary calendar ID (if no calendar_id in context):

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/calendars/primary
- as: user
```

Response: `data.calendars[0].calendar.calendar_id` is the primary calendar ID.

Step 2 — Submit RSVP reply:

```
Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees/batch_delete
```

> **Note:** The Lark Open API exposes RSVP reply via the attendees sub-resource. Use the reply endpoint below.

```
Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/reply
- body:
  {
    "rsvp_status": "accept"
  }
```

`rsvp_status` values: `accept`, `decline`, `tentative`.

If no `calendar_id` is known, use `primary` as the calendar ID — the API resolves it to the user's primary calendar.

## Parameters

| Field | Required | Description |
|---|---|---|
| `calendar_id` | No | Calendar ID containing the event; defaults to primary calendar |
| `event_id` | Yes | Event ID (obtain from +agenda output) |
| `rsvp_status` | Yes | Reply status: `accept`, `decline`, or `tentative` |

## Tips

- You can only reply to events you have been invited to.
- Obtain `event_id` via `+agenda` or events search before calling.
- Use `as: user` — this is a user-personal operation.

## References

- [lark-calendar](../SKILL.md) — All calendar shortcuts
- [lark-calendar-agenda](lark-calendar-agenda.md) — View agenda and obtain event IDs
- [lark-shared](../../lark-shared/SKILL.md) — Authentication and global parameters
