---
name: lark-workflow-meeting-summary
version: 1.0.0
description: "Meeting summary workflow: aggregates meeting notes within a specified time range and generates a structured report. Use this skill when the user needs to organize meeting notes, generate a weekly meeting report, or review meetings held over a period of time."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search", "lark_auth_login", "lark_auth_poll", "lark_auth_status", "lark_enable_domain"]
---

# Meeting Summary Workflow

**CRITICAL — Before starting MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling**. Then read [`../lark-vc/SKILL.md`](../lark-vc/SKILL.md) to understand meeting notes-related operations.

**CRITICAL — Before starting MUST use the Read tool to read [`../lark-vc/references/vc-domain-boundaries.md`](../lark-vc/references/vc-domain-boundaries.md)**. Skipping this will cause incorrect command usage, wrong decisions on meeting artifacts, and errors in domain boundary responsibility:
> 1. Understand the relationships and responsibility boundaries between Calendar & VC, and meeting artifacts & documents
> 2. Understand the relationships between meeting artifacts (Minutes and meeting notes), e.g.: **Minutes and meeting notes are generated independently of each other**
> 3. Understand the components of different meeting artifacts in order to decide which artifact's data to use based on requirements
> 4. Understand the standard process for meeting summarization, analysis, and information extraction

## Use this skill when

- "Help me organize this week's meeting notes" / "Summarize recent meetings" / "Generate a weekly meeting report"
- "Show me what meetings happened today" / "Review all meetings from the past week"

## Prerequisites

Only **user identity** is supported. Ensure authorization is complete before executing:

```javascript
// Basic (query + notes)
lark_auth_login({ domain: 'vc' })

// Includes reading note document body + generating documents
lark_auth_login({ domain: 'vc,drive' })
```

## Workflow

```
{time range} ─► vc search ──► meeting list (meeting_ids)
                   │
                   ▼
               vc notes ──► note document tokens
                   │
                   ▼
               drive metas_batch_query note metadata
                   │
                   ▼
               structured report
```

### Step 1: Determine Time Range

Default is **past 7 days**. Inference rules: "today" → current day, "this week" → Monday of current week ~ now, "last week" → last Monday ~ last Sunday, "this month" → 1st ~ now.

> **Note**: Date conversions MUST use system commands (e.g. `date`) — DO NOT calculate mentally. Time range parameters must be formatted per actual CLI requirements (typically `YYYY-MM-DD` or ISO 8601).

### Step 2: Query Meeting Records

```javascript
// page-size maximum is 30
lark_api({ tool: 'vc', op: 'search', args: { start: '<YYYY-MM-DD>', end: '<YYYY-MM-DD>', page_size: 30 } })
```

- Time range splitting: the maximum searchable time range is 1 month. To search a longer range, split into multiple queries each covering one month.
- `end` is **inclusive** of that date (i.e., when querying "today", set both start and end to today)
- `page_size: 30` returns at most 30 records per page.
- When a `page_token` is present, MUST continue paginating to collect all `id` fields (meeting-id)

### Step 3: Retrieve Note Metadata

1. Query note information associated with each meeting

```javascript
lark_api({ tool: 'vc', op: 'notes', args: { meeting_ids: 'id1,id2,...,idN' } })
```

- Query meeting notes using the `meeting-id` values collected in the previous step.
- A single call supports at most 50 note queries; batch calls are required when exceeding 50.
- Some meetings return `no notes available` — mark those as "no notes" in the final output
- Record each meeting's `note_doc_token` (note document token) and `verbatim_doc_token` (verbatim transcript document token)


2. Retrieve note document and verbatim transcript document links

```javascript
// Use lark_api_search to learn the parameter structure before calling
lark_api_search({ query: 'drive metas batch_query' })

// Batch-retrieve note document and verbatim transcript links: max 10 documents per call
lark_api({ tool: 'drive', op: 'metas batch_query', args: { request_docs: [{ doc_type: 'docx', doc_token: '<doc_token>' }], with_url: true } })
```

### Step 4: Compile the Notes Report

Choose the output format based on the time span:

- **Single-day summary** ("today" / "yesterday"): use "Today's Meeting Overview" as the heading; list each meeting's time, topic, notes link, and verbatim transcript link.
- **Multi-day / weekly report** ("this week" / "past 7 days", etc.): use "Weekly Meeting Report" as the heading; include an overview summary and per-meeting details.

### Step 5: Generate Document (Optional — when requested by user)

Read [`../lark-doc/SKILL.md`](../lark-doc/SKILL.md) to learn the Docs skill.

```javascript
// Create a new document
lark_api({ tool: 'docs', op: 'create', args: { api_version: 'v2', doc_format: 'markdown', content: '<title>Meeting Notes Summary (<start> - <end>)</title>\n<content>' } })

// Or append to an existing document
lark_api({ tool: 'docs', op: 'update', args: { api_version: 'v2', doc: '<url_or_token>', command: 'append', doc_format: 'markdown', content: '<content>' } })
```

## References

- [lark-shared](../lark-shared/SKILL.md) — authentication, permissions (required reading)
- [lark-vc](../lark-vc/SKILL.md) — `search`, `notes` detailed usage
- [lark-doc](../lark-doc/SKILL.md) — `fetch`, `create`, `update` detailed usage
