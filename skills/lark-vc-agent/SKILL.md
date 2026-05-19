---
name: lark-vc-agent
version: 2.0.0
description: "Lark VC Agent: bot joins/leaves an in-progress meeting on behalf of the user and streams real-time events (participants, speech, chat, screen share). Use for meeting bots, silent observers, and proxy attendees. For post-meeting queries (notes, transcripts, recordings), use the lark-vc skill."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# vc-agent (v2)

**CRITICAL — Before starting, MUST read the following two skill documents:**

- [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) — authentication, identity switching, permission handling
- [`../lark-vc/SKILL.md`](../lark-vc/SKILL.md) — core Video Conferencing concepts (Meeting / Note / Minutes, etc.); this skill reuses those definitions directly and does not redefine them

> **Naming convention:** VC agent operations call `lark_api({ tool: 'vc', op: '<op>', args: {...} })`.

## Early Access Notice

- This feature is currently in early access and available to a limited set of users. Ignore the permission-request flow in [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md); follow the guidance below instead.
- If the MCP tool reports `missing required scope(s)` / `permission_violations`, do NOT apply for the corresponding permissions — instead, prompt the user to join the early adopter group: `https://go.larkoffice.com/join-chat/2f4nb0e1-fe00-4f67-bed7-25beaf533fbd`.
- If the MCP tool returns `error.code=20017` / `ErrNotInGray`, prompt the user to join the early adopter group: `https://go.larkoffice.com/join-chat/2f4nb0e1-fe00-4f67-bed7-25beaf533fbd`.

## Positioning

This skill runs alongside [`lark-vc`](../lark-vc/SKILL.md):

- **`lark-vc`** **handles "post-meeting queries"**: searching historical meetings, participant snapshots, notes/transcripts/recordings
- **`lark-vc-agent`** **handles "in-meeting actions"**: bot joins meeting / reads real-time events from an active meeting / bot leaves meeting

Route according to this division to avoid semantic confusion between the two skills.

| User intent example | Route to |
| --- | --- |
| "Join meeting 123456789 for me", "Attend on my behalf", "Have the bot listen in" | **This skill** `meeting-join` |
| "The meeting is still running — who just joined?", "Who is speaking in the meeting?", "Is anyone sharing their screen?" (**active meeting**, **bot already joined**) | **This skill** `meeting-events` |
| "Leave the meeting", "Have the bot exit" | **This skill** `meeting-leave` |
| "Who attended yesterday's meeting?", "Search yesterday's meetings", "Retrieve notes/transcript/recording" | [`lark-vc`](../lark-vc/SKILL.md) |
| "Join the meeting for me, then send the notes to the group afterwards" (cross-phase scenario) | Orchestrate in sequence: this skill (join → read events → leave) → [`lark-vc`](../lark-vc/SKILL.md) / [`lark-minutes`](../lark-minutes/SKILL.md) (fetch notes) → [`lark-im`](../lark-im/SKILL.md) (send to group) |

## Core Scenarios

### 1. Join an in-progress meeting (write operation)

1. Only use `meeting-join` when the user explicitly asks the agent to **actually join** the meeting (meeting bot, in-meeting assistant, silent observer, proxy attendee). Do NOT join just to fetch data.
2. `lark_api({ tool: 'vc', op: 'meeting-join', args: { meeting_number: '<9-digit>' } })` accepts only a **9-digit all-numeric** meeting number — not the full meeting link, and not a `meeting_id`.
3. The `meeting.id` in the response body **MUST be captured immediately** — subsequent `meeting-events` / `meeting-leave` calls depend on it; **the 9-digit meeting number cannot substitute for it**.
4. Joining is visible to all attendees; confirm the 9-digit meeting number source before proceeding to avoid joining the wrong meeting.
5. Only `user` identity is supported; complete the LarkSkill MCP auth flow beforehand: `lark_auth_login({ domain: 'vc' })`, then `lark_auth_poll` to wait for authorization, and confirm via `lark_whoami` / `lark_auth_status`.
6. If joining fails, first consult the error-troubleshooting section of the `meeting-join` reference, focusing on meeting number, password, meeting status, waiting room / approval, and whether the meeting blocks the current identity.

### 2. Observe in-meeting events (read operation)

1. When the user wants to know "what is happening in the meeting right now" (participants joining/leaving, chat, transcript, screen sharing), use `lark_api({ tool: 'vc', op: 'meeting-events', args: { meeting_id: '<meeting_id>' } })`.
2. The input is **`meeting_id`** (a long numeric ID), not the 9-digit meeting number.
3. The bot MUST **have actually joined the meeting** (via `meeting-join` first); otherwise the event stream is typically unavailable. For specific state boundaries, the post-meeting grace window, and error codes (e.g. `10005 / 20001 / 20002`), see the `meeting-events` reference.
4. **Cannot be used for post-meeting review** and **cannot substitute for participant snapshot queries**. If the meeting has ended:
   - To retrieve a notes document or transcript document token: use `lark_api({ tool: 'vc', op: 'notes', args: { meeting_ids: ['<meeting.id>'] } })`
   - To retrieve AI-generated content (summary / todos / chapters) or export a transcript file: first use `lark_api({ tool: 'vc', op: 'recording', args: { meeting_ids: ['<meeting.id>'] } })` to get `minute_token`, then `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: ['<minute_token>'] } })`
   - To view participant snapshots: use `lark_api({ tool: 'vc', op: 'meeting-get', args: { meeting_id: '<meeting_id>', with_participants: true } })` (see [`lark-vc`](../lark-vc/SKILL.md))
5. **MUST use** **`page_all: true`** by default, unless the user explicitly requests "only one page" or there is a specific need to limit the response size.
6. Output format defaults to `format: 'pretty'` (more readable timeline); use `format: 'json'` only when the full raw message stream and structured fields must be preserved.
7. **MUST detect pagination signals**: whenever `has_more=true`, a pretty-format `more available` indicator, or a non-empty `page_token` appears in the response, do NOT treat the current result as the complete event stream; default to continuing pagination, or clearly inform the user that the current result is only partial.
8. Retain the `page_token` from the response; use it directly for incremental fetches next time — do not restart from the beginning.
9. **Whenever answering about the content of an active meeting based on** **`meeting-events`**, do NOT reuse stale results. Whether the user asks about "current / just now / latest" status or asks you to "summarize what this meeting is about", you MUST re-fetch the current event stream first to confirm you have the latest data before answering. Only reuse prior results when the user explicitly asks you to continue analysing a historical snapshot.

### 3. Leave the meeting (write operation)

1. When the task is complete or the user requests exit, use `lark_api({ tool: 'vc', op: 'meeting-leave', args: { meeting_id: '<meeting.id obtained from meeting-join>' } })`.
2. `meeting_id` **MUST** be the long numeric `meeting.id` returned by `meeting-join`; **the 9-digit meeting number is not accepted**.
3. Leaving takes effect immediately — the bot disappears from the participant list and is visible to other attendees. To rejoin, simply call `meeting-join` again (this is not truly irreversible).
4. Only `user` identity is supported.

### 4. Minimal end-to-end agent loop example

```javascript
// 1. Join meeting, capture meeting.id
const joinResult = await lark_api({ tool: 'vc', op: 'meeting-join', args: { meeting_number: '123456789', format: 'json' } });
const meetingId = joinResult.data.meeting.id;

// 2. Poll events during the meeting
//    Use page_all: true by default to fetch all currently visible events; use page_token for incremental polling
//    Typical polling interval: 10–30 seconds
await lark_api({ tool: 'vc', op: 'meeting-events', args: { meeting_id: meetingId, page_all: true, format: 'pretty' } });

// 3. Leave when task is complete or user requests exit
await lark_api({ tool: 'vc', op: 'meeting-leave', args: { meeting_id: meetingId } });

// 4. Optional post-meeting: fetch notes / transcript (crosses into lark-vc)
await lark_api({ tool: 'vc', op: 'notes', args: { meeting_ids: [meetingId] } });
```

## Operations

| Operation | Type | Description |
| --- | --- | --- |
| [`meeting-join`](references/lark-vc-agent-meeting-join.md) | Write | Join an in-progress meeting by 9-digit meeting number |
| [`meeting-events`](references/lark-vc-agent-meeting-events.md) | Read | List bot meeting events (participant joined/left, transcript, chat, share) |
| [`meeting-leave`](references/lark-vc-agent-meeting-leave.md) | Write | Leave a meeting by meeting_id |

- MUST read [references/lark-vc-agent-meeting-join.md](references/lark-vc-agent-meeting-join.md) before calling `meeting-join` — understand the argument format and write-operation visibility risks.
- MUST read [references/lark-vc-agent-meeting-events.md](references/lark-vc-agent-meeting-events.md) before calling `meeting-events` — understand the `meeting_id` source, pagination, error codes (`10005 / 20001 / 20002`), and the "bot still in meeting" hard constraint.
- MUST read [references/lark-vc-agent-meeting-leave.md](references/lark-vc-agent-meeting-leave.md) before calling `meeting-leave` — understand the `meeting_id` source and write-operation visibility.

## Permissions

| Operation | Required scope |
| --- | --- |
| `meeting-join` | `vc:meeting.bot.join:write` |
| `meeting-events` | `vc:meeting.meetingevent:read` |
| `meeting-leave` | `vc:meeting.bot.join:write` |

## See Also

- Query ended meetings, participant snapshots, search historical meetings → [`lark-vc`](../lark-vc/SKILL.md)
- Meeting notes, transcripts → [`lark-vc`](../lark-vc/SKILL.md) `notes`
- Lark Minutes AI content (AI summary / transcription / chapters) → [`lark-minutes`](../lark-minutes/SKILL.md)
- Send post-meeting output to a group / DM → [`lark-im`](../lark-im/SKILL.md)
- Authentication, identity switching, scope management → [`lark-shared`](../lark-shared/SKILL.md)
