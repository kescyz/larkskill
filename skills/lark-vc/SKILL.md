---
name: lark-vc
version: 2.0.0
description: "Lark Video Conference: query meeting records, fetch meeting-note artifacts (summary, todos, chapters, transcript) via LarkSkill MCP. 1. Use this skill when querying the number or details of ended meetings (e.g. yesterday / last week / today's already-held meetings); for upcoming meeting schedules use the lark-calendar skill. 2. Supports searching meeting records by keyword, time range, organizer, participant, meeting room, and other filters. 3. Use this skill when fetching or organizing meeting notes."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# vc (v2)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## Core concepts

- **Meeting**: Lark video meeting instance identified by `meeting_id`.
- **Meeting Record**: Generated after meeting ends; searchable by keyword, time range, participant, organizer, room, and other filters.
- **Meeting Note**: Structured document generated after a meeting ends, containing the note document (with summary, todos, chapters) and the transcript document.
- **Minutes**: Recording artifact from a Lark video meeting or uploaded audio/video file, supporting video/audio transcription and meeting notes, identified by `minute_token`.
- **MainDoc**: Primary note document containing AI-generated summary and todos.
- **VerbatimDoc**: Line-by-line transcript with speaker and timestamps.

## Core scenarios

### 1) Search meeting records

1. Only ended meetings are searchable here. For future meetings that have not yet started, use the lark-calendar skill.
2. Only supports searching meeting records by keyword, time range, participant, organizer, room, and other filters. For unsupported filters, prompt the user.
3. When search results contain multiple records, handle pagination and do not miss any meeting records.

### 2) Organize meeting notes

1. By default, returning note document and transcript links is enough; no need to read note document or transcript content.
2. Only read the document to get specific content when the user explicitly needs the summary, todos, or chapter artifacts from the note document.
3. When reading smart notes (`note_doc_token`) content, the **first `<whiteboard>`** tag in the note document is the cover image (AI-generated summary visualization); fetch and display it to the user using the docs skill.

> **Artifact directory convention**: All downloaded artifacts for the same meeting (cover image, transcript, etc.) should be kept together, not scattered.

> **`note_doc_token` vs `verbatim_doc_token` — two different documents; choose based on user intent:**
> - `note_doc_token` → **Smart Notes** (AI summary + todos + chapters) — use when user says "notes", "summary", "todos", "note content"
> - `verbatim_doc_token` → **Transcript** (complete line-by-line text record with speaker and timestamps) — use when user says "transcript", "full record", "who said what"
> - When user intent is unclear, show both document links and let the user choose rather than deciding for them

### 3) Note and transcript links

1. Note documents, transcript documents, and associated shared documents are returned as doc tokens by default.
2. To fetch document names and URLs, call:

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/metas/batch_query
- body:
  {
    "request_docs": [{ "doc_type": "docx", "doc_token": "<doc_token>" }],
    "with_url": true
  }
```

3. To fetch document content, use the lark-doc skill.

## Resource relationship

```
Meeting (video conferencing)
├── Note (meeting notes)
│   ├── MainDoc (main note document)
│   ├── VerbatimDoc (transcript)
│   └── SharedDoc (shared documents in meetings)
└── Minutes
    ├── Transcript
    ├── Summary
    ├── Todos
    └── Chapters
```

> **Note**: `search` only queries ended historical meetings. Use [lark-calendar](../lark-calendar/SKILL.md) for future schedules.
>
> **Priority rule**: When user searches historical meetings, prefer `vc search` over calendar events search. Calendar search targets schedules; vc search targets ended meeting records and supports filtering by participant, organizer, room, and other dimensions.
>
> **Routing rule**: If the user is asking about "meetings already held", "what meetings happened today", "recent meetings I attended", "ended meetings", "history records", prefer `vc search`. Only use [lark-calendar](../lark-calendar/SKILL.md) when querying future schedules, upcoming meetings, or agendas.
>
> **Special case**: When the user asks "what meetings are there today", use `vc search` to query today's already-held meetings AND use the lark-calendar skill to query today's not-yet-started meetings, then present the merged output to the user.

## Operations

| Operation | Reference |
|-----------|-----------|
| [`search`](references/lark-vc-search.md) | Search meeting records (requires at least one filter) |
| [`notes`](references/lark-vc-notes.md) | Query meeting notes (via meeting-ids, minute-tokens, or calendar-event-ids) |

## meeting — get

Get meeting details (topic, time, participants, note_id).

Get basic meeting info (no participant list):

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/vc/v1/meetings/{meeting_id}
- params: { "meeting_id": "<meeting_id>" }
- as: user
```

Get meeting info including participant list:

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/vc/v1/meetings/{meeting_id}
- params: { "meeting_id": "<meeting_id>", "with_participants": true }
- as: user
```

## minutes (cross-domain, see [lark-minutes](../lark-minutes/SKILL.md))

Get minutes metadata (title, duration, cover). For note **content**, use the notes operation with `minute_tokens`.

## Permission matrix

| Operation | Required scope |
|-----------|---------------|
| `notes` (meeting-ids path) | `vc:meeting.meetingevent:read`, `vc:note:read` |
| `notes` (minute-tokens path) | `vc:note:read`, `minutes:minutes:readonly`, `minutes:minutes.artifacts:read`, `minutes:minutes.transcript:export` |
| `notes` (calendar-event-ids path) | `calendar:calendar:read`, `calendar:calendar.event:read`, `vc:meeting.meetingevent:read`, `vc:note:read` |
| `search` | `vc:meeting.search:read` |
| `meeting.get` | `vc:meeting.meetingevent:read` |
