---
name: lark-workflow-meeting-summary
version: 2.0.0
description: "Meeting minutes consolidation workflow via LarkSkill MCP: collect meeting notes within a specified time range and generate a structured report. Use when users need to organize meeting notes, generate weekly meeting reports, or review meetings over a period."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# Meeting Minutes Consolidation Workflow (v2)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected. Also read [`../lark-vc/SKILL.md`](../lark-vc/SKILL.md) to understand meeting-note-related operations.

## Applicable Scenarios

- "Help me organize this week's meeting notes" / "Summarize recent meetings" / "Generate a weekly meeting report"
- "What meetings did we have today" / "Review what meetings were held in the past week"

## Prerequisites

Only supports **user identity** (`as: "user"`). Ensure user OAuth is completed before execution. Required scopes:
- `vc:meeting.search:read` — for meeting search
- `vc:note:read` — for meeting notes
- `drive:drive:readonly` — for document metadata (if fetching doc URLs)

## Workflow

```
{time range} ─► vc search ──► Meeting list (meeting_ids)
                   │
                   ▼
               vc notes ──► Note document tokens
                   │
                   ▼
               drive metas batch_query ──► Document metadata + URLs
                   │
                   ▼
               Structured reporting
```

### Step 1: Determine Time Range

Default is **past 7 days**. Inference rules: "today" → same day, "this week" → Monday to now, "last week" → last Monday to last Sunday, "this month" → day 1 to now.

> **Note**: compute dates from the current date using reasoning, not natural language strings. Time parameters must be ISO 8601.

### Step 2: Query Meeting Records

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/vc/v1/meetings/search
- body:
  {
    "start_time": "<YYYY-MM-DDTHH:mm:ss+08:00>",
    "end_time": "<YYYY-MM-DDTHH:mm:ss+08:00>",
    "page_size": 30
  }
- as: user
```

- Max searchable range per query is 1 month. For longer ranges, split into monthly queries.
- `end_time` is **inclusive** (for "today", both start and end should span the full day)
- Max page_size is 30; paginate with `page_token` if `has_more=true`
- Collect all `id` fields (meeting_id) from results

### Step 3: Get Notes Metadata

Query notes for each meeting using the meeting_ids collected in Step 2:

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/vc/v1/meetings/{meeting_id}/notes
- as: user
```

- Call once per meeting_id (batch up to 50 per logical group)
- Some meetings return no notes; mark these as "no notes" in final output
- Record each meeting's `note_doc_token` and `verbatim_doc_token`

To get document URLs in batch:

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/metas/batch_query
- body:
  {
    "request_docs": [{ "doc_type": "docx", "doc_token": "<doc_token>" }],
    "with_url": true
  }
- as: user
```

### Step 4: Produce Minutes Report

Choose output format based on time span:

- **Single-day summary** ("today"/"yesterday"): title "Today Meeting Overview", list each meeting with time, topic, notes link, transcript link.
- **Multi-day/weekly report** ("this week"/"past 7 days", etc.): title "Meeting Minutes Weekly Report", including overview stats and per-meeting details.

### Step 5: Generate Document (Optional, when user requests)

Read [`../lark-doc/SKILL.md`](../lark-doc/SKILL.md) to understand doc creation operations.

Create a new doc:

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/docx/v1/documents
- body:
  {
    "title": "Summary of meeting minutes (<start> - <end>)"
  }
- as: user
```

Then append content blocks using the doc token returned.

## Permission Table

| Operation | Required Scope |
|-----------|---------------|
| vc search | `vc:meeting.search:read` |
| vc notes | `vc:meeting.meetingevent:read`, `vc:note:read` |
| drive metas batch_query | `drive:drive:readonly` |
| doc create | `docx:document:create` |

## References

- [lark-shared](../lark-shared/SKILL.md) — Authentication and permissions (required)
- [lark-vc](../lark-vc/SKILL.md) — Detailed vc search and notes operations
- [lark-doc](../lark-doc/SKILL.md) — Detailed doc create and update operations
