---
name: lark-vc
version: 1.0.0
description: "Lark Video Conferencing: search historical meetings, query meeting note artifacts (summaries, to-dos, chapters, verbatim transcripts), query meeting participant snapshots. 1. Use this skill when querying the count or details of already-ended meetings (e.g. historical dates | yesterday | last week | meetings already held today). Use the lark-calendar skill for upcoming unstarted meeting schedules. 2. Supports filtering meeting searches by keyword, time range, organizer, participants, meeting room, and more. 3. Use this skill to retrieve or organize meeting notes, verbatim transcripts, and recording artifacts. 4. For participant snapshot queries such as 'who attended a meeting' or 'attendee list', use vc meeting get --with-participants (queryable at any point in time, including ended meetings). Note: **For Agent real join/leave meetings and sensing real-time events of in-progress meetings**, use the lark-vc-agent skill — this skill does not cover write operations or in-meeting event streams."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search", "lark_auth_login", "lark_auth_poll", "lark_auth_status", "lark_whoami", "lark_enable_domain"]
---

# vc (v1)

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which contains authentication and permission handling**

**CRITICAL — Before starting, MUST use the Read tool to read [`references/vc-domain-boundaries.md`](references/vc-domain-boundaries.md)** — skipping this will cause errors in command usage, meeting artifact decisions, and domain boundary responsibility judgments:
> 1. Understand the relationship and responsibility division between Calendar & VC, and between meeting artifacts & documents
> 2. Understand the relationship between meeting artifacts (Minutes and Notes) — for example: **Minutes and Notes are generated independently of each other**
> 3. Understand the components of different meeting artifacts to decide which artifact's data to use based on requirements
> 4. Understand the standard process for meeting summarization, analysis, and information extraction

## Core Concepts

- **Meeting**: A Lark video conferencing instance, identified by `meeting_id`. Ended meetings support searching by keyword, time range, participants, organizer, meeting room, and other conditions (see `+search`).
- **Note**: A structured document generated after a video meeting ends, containing the note document (with summary and to-dos) and the verbatim transcript document.
- **Minutes**: Recording artifacts from Lark video meetings or audio/video files uploaded by users. Supports video/audio transcription, and contains summaries, to-dos, chapters, and text records. Identified by `minute_token`.
- **MainDoc**: The main document of the AI smart note, containing AI-generated summaries and to-dos. Corresponds to `note_doc_token`.
- **MeetingNotes**: A note document that users actively bind to a meeting. Corresponds to `meeting_notes`. Only returned via the `--calendar-event-ids` path.
- **VerbatimDoc**: A sentence-by-sentence text record of the meeting, including speaker and timestamp information.

## Core Scenarios

### 1. Searching Meeting Records
1. Only ended meetings can be searched. For future meetings that have not started yet, use the lark-calendar skill.
2. Only keyword, time range, participants, organizer, meeting room, and similar filter conditions are supported. For unsupported filter conditions, notify the user.
3. When search results contain multiple records, always handle paginated data carefully — do not miss any meeting records.

### 2. Organizing Meeting Notes

> ⚠️ Before choosing which artifact to read, confirm that you understand the difference between the AI summary pipeline vs. the recording pipeline. If unsure, read the "Independence of the Two Pipelines" section in [`references/vc-domain-boundaries.md`](references/vc-domain-boundaries.md) first.

**⚠️ Artifact selection decision — strictly distinguish by user intent:**

| User Intent | Artifact to Read | Prohibited |
|---------|-------------|------|
| **Extracting / summarizing / re-summarizing / organizing meeting content / reviewing meeting** | Verbatim transcript (`verbatim_doc_token`) or Minutes text record (Transcript) — independently analyze based on original conversation | DO NOT directly copy the AI note (`note_doc_token`) summary as final output |
| **Viewing to-dos / chapters** | AI note (`note_doc_token`) or Minutes artifact — AI to-dos are more user-friendly (includes author and assignee); chapters are more structured by topic | — |
| **Viewing note links / document URLs** | Return document links only, no need to read content | — |
| **Directly viewing AI summary results** | AI note (`note_doc_token`) | — |
| **Who said what / full speech record** | Verbatim transcript (`verbatim_doc_token`) | — |

> **Why must "extract / summarize" start from the verbatim transcript?** The AI note is a secondary compression of the meeting by the model, which may omit discussion details, debate processes, and implicit decisions. When users request "extract" or "re-summarize", they expect independent analysis based on the original conversation, not a reformatting of AI output. The AI note can serve as supplementary reference, but must not be the sole source.

1. When organizing note documents, provide the note document link, verbatim transcript link, and Minutes link by default — no need to read the note document or verbatim transcript content.
2. Only read documents to retrieve specific content when the user explicitly needs summaries, to-dos, or chapter artifacts.
3. When reading AI smart note (`note_doc_token`) content, the **first `<whiteboard>`** tag in the note document is the cover image (AI-generated summary visualization) — download and display it to the user:
```javascript
// 1. Read note content
lark_api({ tool: 'docs', op: '+fetch', args: { 'api-version': 'v2', doc: '<note_doc_token>', 'doc-format': 'markdown' } })
// 2. Extract the token from the first <whiteboard token="xxx"/> in the returned markdown
// 3. Download the cover image to the aggregated directory (same directory as verbatim transcript and recording, to consolidate artifacts)
//    Not all notes have a cover whiteboard — skip if no <whiteboard> tag is present
lark_api({ tool: 'docs', op: '+media-download', args: { type: 'whiteboard', token: '<whiteboard_token>', output: './minutes/<minute_token>/cover' } })
```
> **Artifact directory convention**: All downloaded artifacts for the same meeting (recordings, verbatim transcripts, cover images, etc.) should be placed under `./minutes/{minute_token}/`. This is consistent with the default output location of `vc +recording` and `vc +notes --minute-tokens` operations, making it easier for Agent aggregation. Explicit paths (e.g. cover images) must be manually aligned to the same directory.

> **Note-related documents — select based on user intent:**
> - `note_doc_token` → **AI smart note** (AI summary + to-dos)
> - `meeting_notes` → **User-bound meeting notes** (documents that users actively associate with a meeting; only returned via the `--calendar-event-ids` path)
> - `verbatim_doc_token` → **Verbatim transcript** (complete sentence-by-sentence text record with speaker and timestamp) — use this when users say "verbatim transcript", "complete record", or "who said what"
> - When users say "notes", "summary", or "note content", return both `note_doc_token` and `meeting_notes` (if available)
> - When user intent is unclear, show all document links for the user to choose — do not decide for them
> - If the user provides a **local audio/video file** and says "convert to notes" or "convert to transcript", do NOT start from `vc +notes`; first use [minutes +upload](../lark-minutes/references/lark-minutes-upload.md) to generate a `minute_url`, then extract the `minute_token` and call `vc +notes --minute-tokens`

### 3. Note Documents and Verbatim Transcript Links
1. Note documents, verbatim transcript documents, and associated shared documents are returned using document tokens by default.
2. When only basic information such as document name and URL is needed, use the LarkSkill MCP tool to call `drive metas batch_query`:
```javascript
// Learn about the operation args
lark_api_search({ query: 'drive metas batch_query' })

// Batch-retrieve basic document information: maximum 10 documents per query
lark_api({ tool: 'drive', op: 'metas batch_query', args: { data: { request_docs: [{ doc_type: 'docx', doc_token: '<doc_token>' }], with_url: true } } })
```
3. When document content is needed, use `lark_api` with `docs +fetch`:
```javascript
// Retrieve document content
lark_api({ tool: 'docs', op: '+fetch', args: { 'api-version': 'v2', doc: '<doc_token>', 'doc-format': 'markdown' } })
```

### 4. Querying Participant Snapshots (Read Operation)

When users ask "who attended this meeting", "what are the participants of this meeting", "did so-and-so attend", or similar **participant snapshot** questions, use **`vc meeting get --with-participants`**: this is the participant server-side snapshot API, does not depend on bot attendance, and **supports ended meetings too**:

```javascript
lark_api({ tool: 'vc', op: 'meeting get', args: { params: { meeting_id: '<meeting_id>', with_participants: true } } })
```

Selection decision table:

| User Intent | Recommended Operation | Skill |
|---------|---------|--------|
| Participant snapshot (who attended, join/leave time, any point in time) | `lark_api({ tool: 'vc', op: 'meeting get', args: { params: { meeting_id: '...', with_participants: true } } })` | This skill |
| Speech content of ended meetings | `lark_api({ tool: 'vc', op: '+notes', ... })` to get `verbatim_doc_token`, then `lark_api({ tool: 'docs', op: '+fetch', args: { 'api-version': 'v2', ... } })` | This skill |
| Real-time event stream of **in-progress meetings** (transcription, chat, sharing, in-meeting join/leave) | `lark_api({ tool: 'vc', op: '+meeting-events', ... })` | [`lark-vc-agent`](../lark-vc-agent/SKILL.md) |
| **Agent real join / leave meeting** | `lark_api({ tool: 'vc', op: '+meeting-join', ... })` / `lark_api({ tool: 'vc', op: '+meeting-leave', ... })` | [`lark-vc-agent`](../lark-vc-agent/SKILL.md) |

## Resource Relationships

```
Meeting (Video Conference)
├── Note (Meeting Note)
│   ├── MainDoc (AI smart note document, note_doc_token)
│   ├── MeetingNotes (user-bound meeting note document, meeting_notes)
│   ├── VerbatimDoc (verbatim transcript, verbatim_doc_token)
│   └── SharedDoc (in-meeting shared document)
└── Minutes ← identified by minute_token, +recording retrieves from meeting_id
    ├── Transcript (text record)
    ├── Summary
    ├── Todos
    ├── Chapters
    └── Keywords (recommended keywords)
```

> **Note**: `+search` can only query ended historical meetings. For future schedule queries, use [lark-calendar](../lark-calendar/SKILL.md).
>
> **Priority**: When users search historical meetings, prefer `vc +search` over `calendar events search`. Calendar search targets schedules; vc search targets ended meeting records and supports filtering by participant, organizer, meeting room, and other dimensions.
>
> **Routing rule**: If the user is asking about "meetings held", "which meetings happened today", "what meetings have I recently attended", "ended meetings", or "historical meeting records", prefer `vc +search`. Only use [lark-calendar](../lark-calendar/SKILL.md) preferentially when querying future schedules, upcoming meetings, or agenda.
>
> **Minutes boundary**: `+notes` handles note content, verbatim transcripts, and AI artifacts. For basic Minutes information, prefer [`+recording`](references/lark-vc-recording.md) and [lark-minutes](../lark-minutes/SKILL.md).
>
> **File-to-note boundary**: If the user provides a local audio/video file and wants notes, verbatim transcripts, summaries, to-dos, or chapters, the entry point should first go through the [lark-minutes](../lark-minutes/SKILL.md) upload flow to generate `minute_url` / `minute_token`, then return to `vc +notes --minute-tokens` to retrieve content artifacts.
>
> **Special case**: When the user queries "what meetings are there today", query today's ended meeting records via `vc +search`, while also querying today's unstarted meetings using the lark-calendar skill. Present the consolidated results to the user.

## Shortcuts (recommended — use first)

Shortcuts are high-level wrappers for common operations (`lark_api({ tool: 'vc', op: '+<verb>', args: {...} })`). Prefer Shortcuts when available.

| Shortcut | Description |
|----------|------|
| [`+search`](references/lark-vc-search.md) | Search meeting records (requires at least one filter) |
| [`+notes`](references/lark-vc-notes.md) | Query meeting notes and minutes (via meeting-ids, minute-tokens, or calendar-event-ids) |
| [`+recording`](references/lark-vc-recording.md) | Query minute_token from meeting-ids or calendar-event-ids |

- When using the `+search` operation, MUST read [references/lark-vc-search.md](references/lark-vc-search.md) to understand search parameters and response structure.
- When using the `+notes` operation, MUST read [references/lark-vc-notes.md](references/lark-vc-notes.md) to understand query parameters, artifact types, and response structure.
- When using the `+recording` operation, MUST read [references/lark-vc-recording.md](references/lark-vc-recording.md) to understand query parameters and response structure.

> **Agent attendance-related operations are now separate**: For `+meeting-join` / `+meeting-leave` / `+meeting-events`, use the [`lark-vc-agent`](../lark-vc-agent/SKILL.md) skill.

## API Resources

```javascript
// MUST check parameter structure before calling an API
lark_api_search({ query: 'vc <resource> <method>' })
// Call the API
lark_api({ tool: 'vc', op: '<resource> <method>', args: { ... } })
```

> **Important**: When using native APIs, MUST first run `lark_api_search` to check `args` parameter structure — do not guess field formats.

### meeting

  - `meeting get` — Retrieve meeting details (topic, time, participants, note_id)

```javascript
// Get basic meeting information: does not include participant list
lark_api({ tool: 'vc', op: 'meeting get', args: { params: { meeting_id: '<meeting_id>' } } })

// Get basic meeting information: includes participant list
lark_api({ tool: 'vc', op: 'meeting get', args: { params: { meeting_id: '<meeting_id>', with_participants: true } } })
```

### minutes (cross-domain, see [lark-minutes](../lark-minutes/SKILL.md))

  - `lark_api({ tool: 'minutes', op: 'minutes get', args: { ... } })` — Get basic Minutes information (title, duration, cover); to query Minutes **content**, use `lark_api({ tool: 'vc', op: '+notes', args: { 'minute-tokens': ['<minute-token>'] } })`

## Permissions Table

| Method | Required Scope |
|------|-----------|
| `+notes --meeting-ids` | `vc:meeting.meetingevent:read`, `vc:note:read`, `vc:record:readonly` |
| `+notes --minute-tokens` | `vc:note:read`, `minutes:minutes:readonly`, `minutes:minutes.artifacts:read`, `minutes:minutes.transcript:export` |
| `+notes --calendar-event-ids` | `calendar:calendar:read`, `calendar:calendar.event:read`, `vc:meeting.meetingevent:read`, `vc:note:read`, `vc:record:readonly` |
| `+recording --meeting-ids` | `vc:record:readonly` |
| `+recording --calendar-event-ids` | `vc:record:readonly`, `calendar:calendar:read`, `calendar:calendar.event:read` |
| `+search` | `vc:meeting.search:read` |
| `meeting get` | `vc:meeting.meetingevent:read` |

> Agent attendance-related scopes (`vc:meeting.bot.join:write` / `vc:meeting.meetingevent:read`) are documented in [`lark-vc-agent`](../lark-vc-agent/SKILL.md).
