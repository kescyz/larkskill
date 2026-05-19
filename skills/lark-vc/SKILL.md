---
name: lark-vc
version: 2.0.0
description: "Lark Video Conferencing: search ended meetings, query note artifacts (summaries, todos, chapters, transcripts), and participant snapshots via LarkSkill MCP. Use for historical meetings; use lark-calendar for future schedules. Use lark-vc-agent for real-time in-meeting events and Agent join/leave."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# vc (v1)

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling.**

## Core Concepts

- **Meeting**: A Lark video conference instance, identified by `meeting_id`. Ended meetings can be searched by keyword, time range, participant, organizer, meeting room, and other criteria (see `vc-search`).
- **Note**: A structured document generated after a video conference ends, containing the note document (with summary, todos, and chapters) and the verbatim transcript document.
- **Minutes**: Recording artifacts from Lark video conferences or user-uploaded audio/video files; supports transcription and meeting notes. Identified by `minute_token`.
- **MainDoc**: The main document of AI-generated meeting notes, containing AI-generated summary and todos. Corresponds to `note_doc_token`.
- **MeetingNotes**: A note document that the user has manually bound to a meeting. Corresponds to `meeting_notes`. Only returned via the `calendar_event_ids` path.
- **VerbatimDoc**: A sentence-by-sentence text record of the meeting, including speaker and timestamp.

## Core Scenarios

### 1. Search Meeting Records
1. Only ended meetings can be searched. For future meetings that have not yet started, use the lark-calendar skill.
2. Only keyword, time range, participant, organizer, meeting room, and similar filters are supported. If a filter is unsupported, inform the user.
3. When search results contain multiple records, pay careful attention to paginated data retrieval — do not miss any meeting records.

### 2. Organize Meeting Notes
1. When organizing notes, providing the note document and verbatim transcript links is sufficient by default — there is no need to read the note document or verbatim transcript content.
2. Only read document content to retrieve the summary, todos, or chapter artifacts when the user explicitly requests them.
3. When reading AI-generated notes (`note_doc_token`), the **first `<whiteboard>`** tag in the note document is the cover image (AI-generated summary visualization) — download and display it to the user simultaneously:
```javascript
// 1. Read note content
lark_api({ tool: 'docs', op: 'fetch', args: { doc: '<note_doc_token>', api_version: 'v2', doc_format: 'markdown' } })
// 2. Extract the token of the first <whiteboard token="xxx"/> from the returned markdown
// 3. Download the cover image to the aggregation directory
//    Not all notes have a cover whiteboard — skip if no <whiteboard> tag is found
lark_api({ tool: 'docs', op: 'media-download', args: { type: 'whiteboard', token: '<whiteboard_token>', output: './minutes/<minute_token>/cover' } })
```
> **Artifact directory convention**: All downloads for the same meeting (recordings, transcripts, cover images, etc.) go under `./minutes/{minute_token}/`. This matches the default output location of `minutes download` and `vc notes`, making it easy for the Agent to aggregate. Explicit paths (e.g. cover image) must be manually aligned to the same directory.

> **Note-related documents — choose based on user intent:**
> - `note_doc_token` → **AI-generated meeting notes** (AI summary + todos + chapters)
> - `meeting_notes` → **User-bound meeting notes** (document the user manually linked to the meeting; only returned via the `calendar_event_ids` path)
> - `verbatim_doc_token` → **Verbatim transcript** (complete sentence-by-sentence record with speaker and timestamp) — use this when the user says "verbatim transcript", "full record", "who said what"
> - When the user says "notes", "summary", "note content", return both `note_doc_token` and `meeting_notes` (if available)
> - When user intent is unclear, present all document links for the user to choose — do not decide for the user
> - If the user provides a **local audio/video file** and says "transcribe to notes" or "transcribe to verbatim", do NOT start from `vc-notes`; first use [minutes upload](../lark-minutes/references/lark-minutes-upload.md) to generate a `minute_url`, then extract the `minute_token` and call `vc-notes` with `minute_tokens`

### 3. Note Document and Verbatim Transcript Links
1. Note documents, verbatim transcript documents, and associated shared documents are returned by default using their document token.
2. When you only need basic information such as document name and URL:

   ```javascript
   // Batch query: get basic metadata (title, url, type) for multiple documents in one call
   lark_api({ tool: 'drive', op: 'metas batch_query', args: { request_docs: [{ doc_token: '<token1>', doc_type: 'docx' }, { doc_token: '<token2>', doc_type: 'sheet' }] } })

   // Single document fallback
   lark_api({ tool: 'drive', op: 'inspect', args: { token: '<doc_token>' } })
   ```
3. When you need to read document content, use `lark_api` with docs fetch:
```javascript
lark_api({ tool: 'docs', op: 'fetch', args: { doc: '<doc_token>', api_version: 'v2', doc_format: 'markdown' } })
```

### 4. Query Participant Snapshots (Read Operation)

When the user asks "who attended this meeting", "what participants were in this meeting", or "did someone attend" — these are **participant snapshot** queries. Use **`vc meeting get` with `with_participants: true`**: this is the server-side participant snapshot API, does not require the bot to join the meeting, and **works for ended meetings too**:

```javascript
lark_api({ tool: 'vc', op: 'meeting-get', args: { meeting_id: '<meeting_id>', with_participants: true } })
```

Decision table:

| User intent | Recommended operation | Skill |
|---------|---------|--------|
| Participant snapshot (who attended, when they joined/left, at any point in time) | `lark_api({ tool: 'vc', op: 'meeting-get', args: { with_participants: true } })` | This skill |
| Speech content of ended meetings | `lark_api({ tool: 'vc', op: 'notes', args: { ... } })` to get `verbatim_doc_token`, then `lark_api({ tool: 'docs', op: 'fetch', ... })` | This skill |
| Real-time event stream of **ongoing meetings** (transcription, chat, sharing, in-meeting join/leave) | `vc meeting-events` | [`lark-vc-agent`](../lark-vc-agent/SKILL.md) |
| **Agent real join / leave** a meeting | `vc meeting-join` / `vc meeting-leave` | [`lark-vc-agent`](../lark-vc-agent/SKILL.md) |

## Resource Relationships

```
Meeting (video conference)
├── Note (meeting notes)
│   ├── MainDoc (AI-generated note document, note_doc_token)
│   ├── MeetingNotes (user-bound note document, meeting_notes)
│   ├── VerbatimDoc (verbatim transcript, verbatim_doc_token)
│   └── SharedDoc (document shared during meeting)
└── Minutes ← identified by minute_token; recording op retrieves from meeting_id
    ├── Transcript (text record)
    ├── Summary (summary)
    ├── Todos (action items)
    └── Chapters (chapters)
```

> **Note**: `vc-search` can only query ended historical meetings. Use [lark-calendar](../lark-calendar/SKILL.md) for future schedules.
>
> **Priority**: When the user searches historical meetings, prefer `lark_api({ tool: 'vc', op: 'search', ... })` over calendar events search. Calendar search targets schedules; vc search targets ended meeting records and supports filtering by participant, organizer, meeting room, and other dimensions.
>
> **Routing rule**: If the user asks about "meetings held", "what meetings happened today", "what meetings have I recently attended", "ended meetings", or "historical meeting records" — prefer vc search. Only use [lark-calendar](../lark-calendar/SKILL.md) when querying future schedules, upcoming meetings, or agendas.
>
> **Minutes boundary**: `vc-notes` handles note content, verbatim transcripts, and AI artifacts. For basic Minutes info, prefer `vc-recording` and [lark-minutes](../lark-minutes/SKILL.md).
>
> **File-to-notes boundary**: If the user provides a local audio/video file and wants notes, transcripts, summaries, todos, or chapters — the entry point should first go through [lark-minutes](../lark-minutes/SKILL.md) upload flow to generate a `minute_url` / `minute_token`, then return to `vc-notes` with `minute_tokens` to retrieve the content artifacts.
>
> **Special case**: When the user asks "what meetings do I have today", use `vc-search` to query meetings already held today, and simultaneously use lark-calendar to query meetings not yet started today; organize and display both together.

## Shortcuts (use these first)

Shortcuts are high-level wrappers for common operations via the LarkSkill MCP tool. When a shortcut exists for an operation, use it first.

| Shortcut | Description |
|----------|------|
| [`vc-search`](references/lark-vc-search.md) | `lark_api({ tool: 'vc', op: 'search', args: { ... } })` — Search meeting records (requires at least one filter) |
| [`vc-notes`](references/lark-vc-notes.md) | `lark_api({ tool: 'vc', op: 'notes', args: { ... } })` — Query meeting notes (via meeting_ids, minute_tokens, or calendar_event_ids) |
| [`vc-recording`](references/lark-vc-recording.md) | `lark_api({ tool: 'vc', op: 'recording', args: { ... } })` — Query minute_token from meeting_ids or calendar_event_ids |

- When using `vc-search`, MUST read [references/lark-vc-search.md](references/lark-vc-search.md) to understand search parameters and return value structure.
- When using `vc-notes`, MUST read [references/lark-vc-notes.md](references/lark-vc-notes.md) to understand query parameters, artifact types, and return value structure.
- When using `vc-recording`, MUST read [references/lark-vc-recording.md](references/lark-vc-recording.md) to understand query parameters and return value structure.

> **Agent meeting commands are now separate**: For meeting join, leave, and event streaming, use the [`lark-vc-agent`](../lark-vc-agent/SKILL.md) skill.

## API Resources

```javascript
lark_api_search({ query: 'vc.<resource>.<method>' })  // Check parameter structure before calling an API
lark_api({ tool: 'vc', op: '<resource>.<method>', args: { ... } })  // Call API
```

> **Important**: When using native APIs, MUST first use `lark_api_search` to check the parameter structure. Do not guess field formats.

### meeting

  - `get` — Get meeting details (topic, time, participants, note_id)

```javascript
// Get basic meeting info: without participant list
lark_api({ tool: 'vc', op: 'meeting-get', args: { meeting_id: '<meeting_id>' } })

// Get basic meeting info: with participant list
lark_api({ tool: 'vc', op: 'meeting-get', args: { meeting_id: '<meeting_id>', with_participants: true } })
```

### minutes (cross-domain, see [lark-minutes](../lark-minutes/SKILL.md))

  - `get` — Get basic Minutes info (title, duration, cover); for querying note **content**, use `vc-notes` with `minute_tokens`

## Permissions

| Method | Required scope |
|------|-----------|
| `vc-notes` with `meeting_ids` | `vc:meeting.meetingevent:read`, `vc:note:read` |
| `vc-notes` with `minute_tokens` | `vc:note:read`, `minutes:minutes:readonly`, `minutes:minutes.artifacts:read`, `minutes:minutes.transcript:export` |
| `vc-notes` with `calendar_event_ids` | `calendar:calendar:read`, `calendar:calendar.event:read`, `vc:meeting.meetingevent:read`, `vc:note:read` |
| `vc-recording` with `meeting_ids` | `vc:record:readonly` |
| `vc-recording` with `calendar_event_ids` | `vc:record:readonly`, `calendar:calendar:read`, `calendar:calendar.event:read` |
| `vc-search` | `vc:meeting.search:read` |
| `meeting.get` | `vc:meeting.meetingevent:read` |

> Agent meeting-related scopes (`vc:meeting.bot.join:write` / `vc:meeting.meetingevent:read`) are documented in [`lark-vc-agent`](../lark-vc-agent/SKILL.md).
