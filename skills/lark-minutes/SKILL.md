---
name: lark-minutes
version: 1.0.0
description: "Use this skill when operating Lark Minutes via LarkSkill MCP: search Minutes (keyword / owner / participant / time range), get basic metadata (title, cover, duration), and download audio/video files. For transcripts, AI summaries, to-dos, and chapters, route to lark-vc."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# minutes (v1)

**CRITICAL — Before starting, you MUST first use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling.**

## Prerequisites

- LarkSkill MCP server connected (install via `/plugin marketplace add kescyz/larkskill` → `/plugin install larkskill`, or see https://portal.larkskill.app/setup)
- MCP tools available: `lark_api`, `lark_api_search`
- Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first for auth, global flags, and safety rules

## Core concepts

- **Minutes**: a recording artifact from a Lark video conference, or an audio/video file uploaded by a user, identified by a `minute_token`.
- **Minutes Token (`minute_token`)**: the unique identifier of a minute. It can be extracted from the tail of a Minutes URL (e.g., `obcnq3b9jl72l83w4f14xxxx` in `https://*.feishu.cn/minutes/obcnq3b9jl72l83w4f14xxxx`). If the URL contains extra parameters (such as `?xxx`), take the last segment of the path.

## Core scenarios

### 1. Search Minutes

1. When the user describes "my Minutes", "Minutes containing some keyword", or "Minutes within a time range", prefer `lark_api({tool: 'minutes', op: 'search', args: {...}})`.
2. Only keyword, time range, participant, owner, and similar filter conditions are supported. For unsupported filters, prompt the user.
3. When the search returns multiple results, you MUST handle pagination — do not miss any Minutes record.
4. If the Minutes belong to a meeting, prefer using `lark_api({tool: 'vc', op: 'search', args: {...}})` (see [vc +search](../lark-vc/references/lark-vc-search.md)) to locate the meeting first, then use `lark_api({tool: 'vc', op: 'recording', args: {...}})` (see [vc +recording](../lark-vc/references/lark-vc-recording.md)) as needed to obtain the `minute_token`.


### 2. View basic Minutes information

1. When the user only needs to confirm a minute's title, cover, duration, owner, URL, or other basic information, call the native API via `lark_api` GET `/open-apis/minutes/v1/minutes/{minute_token}`.
2. If the user provides a Minutes URL, first extract the `minute_token` from the URL tail, then call the API above.
3. When user intent is unclear, default to returning basic metadata first to help confirm whether the target minute is a match.

> Inspect the full return-value structure before invoking. Core fields include: `title`, `cover` (cover URL), `duration` (in milliseconds), `owner_id`, and `url` (Minutes link).

### 3. Download Minutes audio/video file

1. Download the Minutes audio/video file locally, or get a 1-day-valid download link via `lark_api({tool: 'minutes', op: 'download', args: {...}})`. See [minutes +download](references/lark-minutes-download.md).
2. `minutes +download` only handles audio/video media files.
3. Use `--url-only` when the user only wants a shareable download URL; download directly when the user wants the file saved locally.

> **Note**: `+download` only handles audio/video media files. If the user wants the transcript, summary, to-dos, chapters, or other minute artifacts, use `lark_api({tool: 'vc', op: 'notes', args: { 'minute-tokens': '<minute_token>' }})` (see [vc +notes --minute-tokens](../lark-vc/references/lark-vc-notes.md)) instead.

### 4. Get Minutes transcript, summary, to-dos, and chapters

1. When the user says "this minute's transcript", "summary", "to-dos", or "chapters", **this is NOT in the scope of this skill**.
2. Use `lark_api({tool: 'vc', op: 'notes', args: { 'minute-tokens': '<minute_token>' }})` (see [vc +notes --minute-tokens](../lark-vc/references/lark-vc-notes.md)) to fetch the corresponding minute artifacts.
3. If a `minute_token` is already in the current context, pass it directly to `vc +notes`. If only a Minutes URL is available, extract the `minute_token` first.

```js
// Get minute artifacts (transcript, summary, to-dos, chapters) by minute_token
lark_api({ tool: 'vc', op: 'notes', args: { 'minute-tokens': '<minute_token>' } })
```

> **Cross-skill routing**: transcript, AI summary, to-dos, chapters, and other minute artifacts are provided by [lark-vc](../lark-vc/SKILL.md) via the `+notes` command.

## Resource relationships

```text
Minutes ← identified by minute_token
├── Metadata (title, cover, duration, owner, url) → lark_api GET /open-apis/minutes/v1/minutes/{minute_token}
└── MediaFile (audio/video file) → lark_api({tool: 'minutes', op: 'download', ...})
```

> **Capability boundary**: `minutes` handles **searching Minutes, viewing basic metadata, and downloading audio/video files**.
>
> **Routing rules**:
>
> - User says "Minutes list / search Minutes / Minutes with some keyword" → `lark_api({tool: 'minutes', op: 'search', ...})`
> - User just wants to see "my Minutes / Minutes within a time range / Minutes list" — do NOT go through [lark-vc](../lark-vc/SKILL.md) first; use this skill directly.
> - If the user also mentions "meeting / met / had a meeting / a specific meeting", even if "Minutes" is also mentioned, prefer going through [lark-vc](../lark-vc/SKILL.md) first to locate the meeting, then obtain the `minute_token` via `lark_api({tool: 'vc', op: 'recording', ...})` (see [vc +recording](../lark-vc/references/lark-vc-recording.md)).
> - When the user says "my Minutes / Minutes I own / Minutes I participated in", you may map the relevant filter to `me`. `me` represents the current user.
> - When results span multiple pages, keep paginating with `page_token` until you confirm there are no more results.
> - `lark_api({tool: 'minutes', op: 'search', ...})` returns at most `200` records per call; the total result count has no fixed upper bound.
> - User says "this minute's title / duration / cover / link" → `lark_api` GET `/open-apis/minutes/v1/minutes/{minute_token}`
> - User says "download this minute's video / audio / media file" → `lark_api({tool: 'minutes', op: 'download', ...})`
> - User says "this minute's transcript / summary / to-dos / chapters" → use `lark_api({tool: 'vc', op: 'notes', args: { 'minute-tokens': '<minute_token>' } })` (see [vc +notes --minute-tokens](../lark-vc/references/lark-vc-notes.md))

## Shortcuts (recommended — prefer these)

A Shortcut is a high-level wrapper around a common operation, surfaced through `lark_api({tool: 'minutes', op: '<verb>', args: {...}})`. When a Shortcut exists, prefer it.

| Shortcut                                                                          | Description                                                     |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [`+search`](references/lark-minutes-search.md) — `lark_api({tool:'minutes', op:'search', ...})` | Search minutes by keyword, owners, participants, and time range |
| [`+download`](references/lark-minutes-download.md) — `lark_api({tool:'minutes', op:'download', ...})` | Download audio/video media file of a minute                     |

- When using `+search`, you MUST read [references/lark-minutes-search.md](references/lark-minutes-search.md) for search parameters and return-value structure.
- When using `+download`, you MUST read [references/lark-minutes-download.md](references/lark-minutes-download.md) for download parameters and return-value structure.

<!-- AUTO-GENERATED-START — managed by gen-skills.py, do NOT hand-edit -->

## API Resources

```js
// Inspect parameter structure before invoking — never guess field formats.
// Native API call shape:
lark_api({ method: 'GET', path: '/open-apis/minutes/v1/minutes/{minute_token}' })
```

> **Important**: When using the native API, you MUST first inspect the `--data` / `--params` parameter structure — never guess field formats.

### minutes

- `get` — get Minutes information → `lark_api` GET `/open-apis/minutes/v1/minutes/{minute_token}`

## Permission table

| Method                                                              | Required scope                 |
| ------------------------------------------------------------------- | ------------------------------ |
| `lark_api({tool:'minutes', op:'search', ...})`                      | `minutes:minutes.search:read`  |
| `lark_api` GET `/open-apis/minutes/v1/minutes/{minute_token}`       | `minutes:minutes:readonly`     |
| `lark_api({tool:'minutes', op:'download', ...})`                    | `minutes:minutes.media:export` |

<!-- AUTO-GENERATED-END -->
