# calendar +suggestion

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

For scheduling requests where time is not yet fixed, provide multiple recommended time options so users can choose, helping solve meeting-time coordination.

**When to call (Agent Guidance):**
- **When user intent is to schedule but time is not fully specified** (for example `today`, `next three days`, `this week`, `afternoon`, or no time description), call this tool to get recommended time slots for user selection.
- **When user already gives a specific time point** (for example `today at 3pm`), **do not** call this tool. Call `+create` directly to create the event.

Required scopes: `["calendar:calendar.free_busy:read"]`

## Recommended call

Call freebusy list for the time window and all attendees, then compute free slots client-side:

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/freebusy/list
- body:
  {
    "time_min": "2026-03-19T08:00:00+08:00",
    "time_max": "2026-03-19T18:00:00+08:00",
    "user_id_list": ["ou_member_a", "ou_member_b"]
  }
```

Repeat calls as needed to cover the full search range, adjusting `time_min` / `time_max`.

To exclude specific time blocks (e.g., user said "show another batch"), exclude those ranges when computing free slots.

## Algorithm: computing free slots

1. Collect all busy intervals from the `freebusy` response for all attendees.
2. Union and sort busy intervals.
3. Walk the search window; identify gaps ≥ `duration_minutes`.
4. Return the first 3–5 candidate slots as recommended options.

## Parameters

| Parameter | Required | Description |
|---|---|---|
| `time_min` | Yes | Search range start (ISO 8601 with timezone) |
| `time_max` | Yes | Search range end (ISO 8601 with timezone) |
| `user_id_list` | No | Attendee open_id list (`ou_` prefix); include self if checking own availability |
| `duration_minutes` | No | Meeting duration in minutes; infer from context if absent |
| `exclude` | No | Time ranges to exclude when computing slots (e.g., previously shown options) |

## Output format

Present recommendations as a structured list with polished recommendation reasons:

```text
## 2026-03-19 Thursday

- **Option 1: 10:00 - 10:30**
  Reason: All participants are free.

- **Option 2: 14:00 - 14:30**
  Reason: All participants are free.
```

**AI Behavior Guidance:**
- **Show options and reasons in structured form**: present recommended time options in a clear list, then ask user preference directly. Explain the advantage of each time block using both user original requirement and recommendation reason. Keep wording concise, direct, and unambiguous.
- **Truthfully report conflicts**: recommended plans are not always fully free. If a recommendation contains conflicts, clearly state the conflict — never mislead user into thinking it is fully free.
- **Proactively provide optimization suggestions**: when all recommendations are not fully free, provide reasonable alternatives (for example adjust time range, meeting duration, or attendee set).

## Typical scenarios

### 1. Find common free time for multiple people

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/calendar/v4/freebusy/list
- body:
  {
    "time_min": "2026-03-19T08:00:00+08:00",
    "time_max": "2026-03-19T18:00:00+08:00",
    "user_id_list": ["ou_member_a", "ou_member_b"]
  }
```

Compute slots ≥ 45 minutes where all attendees are free.

### 2. User asks to "show another batch"

Re-run freebusy query with same parameters, then exclude the previously shown slots when computing the next batch of candidate options.

## Comparison with other shortcuts

| Shortcut | Purpose | Output |
|---|---|---|
| `+suggestion` | Uncertain time scheduling — provide multiple options | Multiple recommended slots with reasons |
| `+freebusy` | Query free/busy status | Busy slot list and RSVP status (no event details) |

**Selection guidance:**
- Looking for meeting time — prefer `+suggestion` for intelligent recommendations
- Checking personal busy status — use `+freebusy`

## References

- [lark-calendar-create](lark-calendar-create.md) — Create event
- [lark-calendar-freebusy](lark-calendar-freebusy.md) — Query free/busy slots and RSVP status
- [lark-calendar](../SKILL.md) — Full calendar API
