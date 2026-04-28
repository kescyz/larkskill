---
name: lark-workflow-meeting-summary
version: 1.0.0
description: "Meeting minutes summarization workflow via LarkSkill MCP. Aggregate Lark Video Conferencing minutes within a time range and generate a structured report (single-day overview or weekly digest). Use when the user asks to organize, summarize, or review meetings."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search", "lark_auth_login", "lark_auth_status", "lark_whoami", "lark_enable_domain"]
---

# Meeting Minutes Summary Workflow

**CRITICAL — Before starting, MUST first use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling.** Then read [`../lark-vc/SKILL.md`](../lark-vc/SKILL.md) for meeting minutes related operations.

## Use this skill when

- "Help me organize this week's meeting minutes" / "Summarize recent meetings" / "Generate a meeting weekly report"
- "Show me what meetings happened today" / "Review meetings from the past week"

## Prerequisites

- LarkSkill MCP server connected (install via `/plugin marketplace add kescyz/larkskill` → `/plugin install larkskill`, or see https://portal.larkskill.app/setup)
- MCP tools available: `lark_api`, `lark_api_search`, `lark_auth_login`, `lark_auth_status`, `lark_whoami`, `lark_enable_domain`
- Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first for auth, global flags, and safety rules

Only **user identity** is supported. Before execution, ensure authorization for the required domains:

```
lark_auth_login({ domain: 'vc' })          // Basic (search + minutes)
lark_auth_login({ domain: 'vc,drive' })    // Includes reading minutes doc body, generating docs
```

## Workflow

```
{time range} ─► vc +search ──► meeting list (meeting_ids)
                   │
                   ▼
               vc +notes ──► minutes doc tokens
                   │
                   ▼
               drive metas batch_query minutes metadata
                   │
                   ▼
               structured report
```

### Step 1: Determine time range

Default is **the past 7 days**. Inference rules: "today" → today, "this week" → Monday of this week ~ now, "last week" → last Monday ~ last Sunday, "this month" → 1st ~ now.

> **Note**: Date conversion MUST call a system command (e.g. `date`); do not compute mentally. Time range parameters must be formatted per the underlying API requirements (typically `YYYY-MM-DD` or ISO 8601).

### Step 2: Query meeting records

```
lark_api({ tool: 'vc', op: 'search', args: { start: '<YYYY-MM-DD>', end: '<YYYY-MM-DD>', format: 'json', 'page-size': 30 } })
```

- Time range splitting: max search range is 1 month. For longer spans, split into multiple one-month queries.
- `end` is **inclusive of that day** (i.e. when querying "today", both `start` and `end` are today)
- `format: 'json'` returns JSON, which you parse better.
- `page-size` max is 30 entries per page.
- When `page_token` is present, MUST continue paginating and collect every `id` field (meeting-id)

### Step 3: Fetch minutes metadata

1. Query meeting-related minutes info
```
lark_api({ tool: 'vc', op: 'notes', args: { 'meeting-ids': 'id1,id2,...,idN' } })
```
- Use `meeting-id` collected in the previous step to query meeting minutes.
- Up to 50 minutes per call; if more than 50, split into batches.
- Some meetings return `no notes available`; mark "no minutes" in the final output.
- Record each meeting's `note_doc_token` (minutes doc token) and `verbatim_doc_token` (verbatim transcript doc token)


2. Get minutes doc and verbatim transcript doc links
```
// Discover the operation shape via search — confirm exact op token before calling
lark_api_search({ query: 'drive metas batch_query' })

// Batch fetch minutes doc and verbatim transcript links: max 10 docs per call
lark_api({ tool: 'drive', op: 'metas.batch_query', args: { request_docs: [{ doc_type: 'docx', doc_token: '<doc_token>' }], with_url: true } })
```

### Step 4: Compose minutes report

Choose output format based on time span:

- **Single-day summary** ("today" / "yesterday"): use the heading "Today's Meeting Overview"; for each meeting list time, topic, minutes link, verbatim transcript link.
- **Multi-day / weekly report** ("this week" / "past 7 days" etc.): use the heading "Meeting Minutes Weekly Report"; include overview stats and per-meeting details.

### Step 5: Generate document (optional, when user asks)

Read [`../lark-doc/SKILL.md`](../lark-doc/SKILL.md) for cloud doc skills.

```
lark_api({ tool: 'docs', op: 'create', args: { title: 'Meeting Minutes Summary (<start> - <end>)', markdown: '<content>' } })

// Or append to an existing doc
lark_api({ tool: 'docs', op: 'update', args: { doc: '<url_or_token>', mode: 'append', markdown: '<content>' } })
```

## References

- [lark-shared](../lark-shared/SKILL.md) — auth, permissions (mandatory)
- [lark-vc](../lark-vc/SKILL.md) — `+search`, `+notes` detailed usage
- [lark-doc](../lark-doc/SKILL.md) — `+fetch`, `+create`, `+update` detailed usage
