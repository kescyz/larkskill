---
name: lark-vc
version: 2.0.0
description: "Lark Video Conferencing via LarkSkill MCP: search ended meetings and retrieve note artifacts (summary, todos, chapters, verbatim transcript). Use for historical meeting queries (yesterday, last week, today already-held); for upcoming agendas use lark-calendar. Filter by keyword, time, organizer, participant, or room."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# vc

## Prerequisites

- LarkSkill MCP server connected (install via `/plugin marketplace add kescyz/larkskill` → `/plugin install larkskill`, or see https://portal.larkskill.app/setup)
- MCP tools available: `lark_api`, `lark_api_search`
- Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first for auth, global flags, and safety rules

## Core concepts

- **Video Conference (Meeting)**: a Lark Video Conferencing instance, identified by `meeting_id`.
- **Meeting Record**: a record generated after a video conference ends; supports searching meetings by keyword, time range, participants, organizer, meeting room, and other filters.
- **Meeting Note (Note)**: a structured document generated after a video conference ends, containing the note document (summary, todos, chapters) and the verbatim transcript document.
- **Minutes**: a recording artifact produced by a Lark video conference, or an audio/video file uploaded by the user; supports transcription and meeting notes for video/audio, identified by `minute_token`.
- **Note Main Doc (MainDoc)**: the main document of the AI smart note, containing AI-generated summary and todos, corresponding to `note_doc_token`.
- **User Meeting Notes (MeetingNotes)**: a note document the user has actively bound to the meeting, corresponding to `meeting_notes`. Returned only via the `calendar-event-ids` path.
- **Verbatim Doc (VerbatimDoc)**: a sentence-by-sentence textual record of the meeting, including speaker and timestamp.

## Core scenarios

### 1. Search meeting records
1. Only meetings that have already ended can be searched. For unstarted future meetings, use the lark-calendar skill.
2. Only keyword, time range, participants, organizer, meeting room, and similar filters are supported. For unsupported filters, prompt the user.
3. When the search results contain multiple records, MUST handle pagination — do not miss any meeting records.

### 2. Organize meeting notes
1. When organizing notes, by default just return the note document and verbatim transcript links — no need to read the note document or verbatim transcript content.
2. Only when the user explicitly asks for the summary, todos, or chapters from the note document, then read the document to retrieve the specific content.
3. When reading the smart note (`note_doc_token`) content, the **first `<whiteboard>`** tag in the note document is the cover image (an AI-generated visualization of the summary), and SHOULD be downloaded and shown to the user at the same time:

```
# 1. Read the note content
lark_api({ tool: 'docs', op: 'fetch', args: { doc: '<note_doc_token>' } })

# 2. From the returned markdown, extract the token of the first <whiteboard token="xxx"/>

# 3. Download the cover image to the artifact directory (same directory as the verbatim transcript, to keep artifacts grouped).
#    Not every note has a cover whiteboard; if there is no <whiteboard> tag, just skip.
lark_api({ tool: 'docs', op: 'media-download', args: { type: 'whiteboard', token: '<whiteboard_token>', output: './artifact-<title>/cover' } })
```

> **Artifact directory convention**: place all downloaded artifacts of the same meeting (cover image, verbatim transcript, etc.) under a unified `artifact-<title>/` directory; do not scatter them in the current working directory.

> **Note-related documents — choose by user intent:**
> - `note_doc_token` → **AI smart note** (AI summary + todos + chapters)
> - `meeting_notes` → **user-bound meeting notes** (a document the user actively associated with the meeting; returned only via the `calendar-event-ids` path)
> - `verbatim_doc_token` → **verbatim transcript** (full sentence-by-sentence textual record with speaker and timestamp) — use this when the user says "verbatim transcript", "full record", or "who said what"
> - When the user says "notes", "summary", or "note content", return both `note_doc_token` and `meeting_notes` (if any) at the same time.
> - When user intent is unclear, show all document links and let the user choose, instead of deciding for the user.

### 3. Note document and verbatim transcript links
1. Note document, verbatim transcript document, and the associated shared document are returned by document Token by default.
2. When only document name and URL basic information are needed, use the Drive metas batch query endpoint.

```
# Batch retrieve basic document info: up to 10 documents per query
lark_api({
  method: 'POST',
  path: '/open-apis/drive/v1/metas/batch_query',
  body: { request_docs: [{ doc_type: 'docx', doc_token: '<doc_token>' }], with_url: true }
})
```

3. When document content is required, use the docs fetch shortcut.

```
lark_api({ tool: 'docs', op: 'fetch', args: { doc: '<doc_token>' } })
```

## Resource relationships

```
Meeting (video conference)
├── Note (meeting note)
│   ├── MainDoc (AI smart note doc, note_doc_token)
│   ├── MeetingNotes (user-bound meeting notes doc, meeting_notes)
│   ├── VerbatimDoc (verbatim transcript, verbatim_doc_token)
│   └── SharedDoc (shared doc during the meeting)
└── Minutes ← identified by minute_token, +recording obtains it from meeting_id
    ├── Transcript (textual record)
    ├── Summary
    ├── Todos
    └── Chapters
```

> **Note**: `vc +search` only queries historical meetings that have already ended. To query future agendas, use [lark-calendar](../lark-calendar/SKILL.md).
>
> **Priority**: when the user searches historical meetings, prefer `vc +search` over `calendar events search`. Calendar search is oriented toward agendas, while vc search is oriented toward meeting records that have already ended, and supports filtering by participants, organizer, meeting room, and other dimensions.
>
> **Routing rule**: if the user asks "meetings I've held", "what meetings did I have today", "what meetings have I joined recently", "ended meetings", or "historical meeting records", prefer `vc +search`. Only when querying future agendas, upcoming meetings, or agenda views, prefer [lark-calendar](../lark-calendar/SKILL.md).
>
> **Special case**: when the user asks "what meetings are there today", use `vc +search` to query meetings that have already happened today, and at the same time use the lark-calendar skill to query meetings that have not yet started today; merge the results and present them to the user.

## Shortcuts (preferred)

A Shortcut is a high-level wrapper for common operations, called via `lark_api({ tool: 'vc', op: '<verb>', args: { ... } })`. Prefer Shortcuts when available.

| Shortcut | Description |
|----------|------|
| [`+search`](references/lark-vc-search.md) | Search meeting records (requires at least one filter) |
| [`+notes`](references/lark-vc-notes.md) | Query meeting notes (via meeting-ids, minute-tokens, or calendar-event-ids) |
| [`+recording`](references/lark-vc-recording.md) | Query minute_token from meeting-ids or calendar-event-ids |

- When using `+search`, MUST read [references/lark-vc-search.md](references/lark-vc-search.md) for search parameters and return value structure.
- When using `+notes`, MUST read [references/lark-vc-notes.md](references/lark-vc-notes.md) for query parameters, artifact types, and return value structure.
- When using `+recording`, MUST read [references/lark-vc-recording.md](references/lark-vc-recording.md) for query parameters and return value structure.

### Examples

```
# Search ended meetings by keyword and time range
lark_api({ tool: 'vc', op: 'search', args: { query: 'roadmap review', 'start-time': 1714521600, 'end-time': 1714608000 } })

# Get notes by meeting ids
lark_api({ tool: 'vc', op: 'notes', args: { 'meeting-ids': '<meeting_id>' } })

# Resolve minute_token from meeting ids
lark_api({ tool: 'vc', op: 'recording', args: { 'meeting-ids': '<meeting_id>' } })
```

## API Resources

> **Important**: when using the raw API, MUST first inspect parameter structure before calling — do not guess field formats. Use `lark_api_search` to discover the right tool/op and its schema:
>
> ```
> lark_api_search({ query: 'vc meeting get' })
> ```

### meeting

  - `vc.meeting.get` — Get meeting details (subject, time, participants, note_id)

```
# Get basic meeting info: does NOT include participant list
lark_api({
  method: 'GET',
  path: '/open-apis/vc/v1/meetings/<meeting_id>'
})

# Get basic meeting info: INCLUDES participant list
lark_api({
  method: 'GET',
  path: '/open-apis/vc/v1/meetings/<meeting_id>',
  params: { with_participants: true }
})
```

### minutes (cross-domain, see [lark-minutes](../lark-minutes/SKILL.md))

  - `minutes.get` — Get basic info of a Minutes (title, duration, cover); to query note **content** use `lark_api({ tool: 'vc', op: 'notes', args: { 'minute-tokens': '<minute_token>' } })`.

## Permissions

| Method | Required scope |
|------|-----------|
| `+notes --meeting-ids` | `vc:meeting.meetingevent:read`, `vc:note:read` |
| `+notes --minute-tokens` | `vc:note:read`, `minutes:minutes:readonly`, `minutes:minutes.artifacts:read`, `minutes:minutes.transcript:export` |
| `+notes --calendar-event-ids` | `calendar:calendar:read`, `calendar:calendar.event:read`, `vc:meeting.meetingevent:read`, `vc:note:read` |
| `+recording --meeting-ids` | `vc:record:readonly` |
| `+recording --calendar-event-ids` | `vc:record:readonly`, `calendar:calendar:read`, `calendar:calendar.event:read` |
| `+search` | `vc:meeting.search:read` |
| `meeting.get` | `vc:meeting.meetingevent:read` |
