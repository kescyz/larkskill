# vc — notes

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first for authentication, global parameters, and safety rules.

Query meeting notes. Supports retrieving note documents, transcripts, AI summaries, todos, and chapters via meeting IDs, minute tokens, or calendar event IDs. Read-only operation.

## Input modes (mutually exclusive — pick exactly one)

### Mode A: by meeting_id

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/vc/v1/meetings/{meeting_id}/notes
- params: { "meeting_id": "69xxxxxxxxxxxxx28" }
- as: user
```

For batch, call once per meeting_id (up to 50 total).

### Mode B: by minute_token

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/minutes/v1/minutes/{minute_token}
- params: { "minute_token": "obbxxxxxxxxxxxxxxxxxx" }
- as: user
```

### Mode C: by calendar_event_id

First resolve the calendar event to get the associated meeting_id, then use Mode A.

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}
- as: user
```

## Core Constraints

### 1. Three input modes are mutually exclusive

Only one input mode can be specified per call. Passing multiple modes simultaneously will result in an error.

### 2. User identity only

All notes operations require `as: "user"`. Ensure user OAuth is completed before use.

### 3. Batch limit

Up to 50 IDs/tokens per logical batch. Call in serial batches for larger sets.

### 4. Permission checks by input mode

| Input mode | Required scopes |
|------------|----------------|
| meeting_id | `vc:meeting.meetingevent:read`, `vc:note:read` |
| minute_token | `vc:note:read`, `minutes:minutes:readonly`, `minutes:minutes.artifacts:read`, `minutes:minutes.transcript:export` |
| calendar_event_id | `calendar:calendar:read`, `calendar:calendar.event:read`, `vc:meeting.meetingevent:read`, `vc:note:read` |

## Output

### When notes are available

Returns a `notes` array, each record containing:

| Field | Description |
|-------|-------------|
| `note_doc_token` | **Smart notes** document token — contains AI summary, todos, chapters (use when user asks for "notes") |
| `verbatim_doc_token` | **Transcript** document token — complete sentence-by-sentence text record with speakers and timestamps (use only when user asks for "transcript") |
| `shared_doc_tokens` | List of document tokens shared during the meeting |
| `creator_id` | Creator ID |
| `create_time` | Creation time (formatted) |

> **Which token to use?** When user says "meeting notes", "summary", "todos", "notes content" → use `note_doc_token`. When user says "transcript", "full record", "who said what" → use `verbatim_doc_token`. When intent is unclear, show both document links and let the user choose.

### AI artifacts in the minute_token path

When querying via minute_token, the returned `artifacts` field contains built-in AI artifacts:

| Field | Description |
|-------|-------------|
| `artifacts.summary` | AI summary (inline JSON) |
| `artifacts.todos` | Todo items (inline JSON) |
| `artifacts.chapters` | Chapter notes (inline JSON) |
| `artifacts.transcript_file` | Transcript content |

## How to obtain input parameters

| Input parameter | How to get it |
|-----------------|---------------|
| `meeting_id` | `vc search` → `id` field in results |
| `minute_token` | Extract from minutes URL, e.g. `https://sample.feishu.cn/minutes/obbyyyyyyyyyyyyyyyyyy` → `obbyyyyyyyyyyyyyyyyyy` |
| `calendar_event_id` | `calendar +agenda` / lark-calendar skill → `event_id` field in results |

## Common Errors and Troubleshooting

| Symptom | Root Cause | Resolution |
|---------|-----------|------------|
| `no notes available for this meeting` | No notes generated for this meeting | Try minute_token mode for built-in artifacts |
| `121005 no permission` | Non-participant lacks permission to view | Use minute_token mode to fall back to built-in artifacts |
| `missing required scope(s)` | Insufficient permissions | Authorize with required scopes via `lark_auth_login` |
| `too many IDs` | Exceeded batch limit | Split into batches, max 50 per batch |

## Tips

- `meeting_id` and `calendar_event_id` paths use the note details API, requiring `vc:note:read` permission.
- `minute_token` path automatically degrades when note permission is missing — returns built-in artifacts without error.

## References

- [lark-vc](../SKILL.md) — all video conference operations
- [lark-vc-search](lark-vc-search.md) — search historical meetings (get meeting_id)
- [lark-shared](../../lark-shared/SKILL.md) — authentication and global parameters
