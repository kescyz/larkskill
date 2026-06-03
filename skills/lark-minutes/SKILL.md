---
name: lark-minutes
version: 1.0.0
description: "Lark Minutes: core functionality for Minutes via LarkSkill MCP. 1. Search Minutes list (by keyword / owner / participant / time range); 2. Get basic Minutes info (title, cover, duration, etc.); 3. Download audio/video media files from a Minute; 4. Retrieve AI artifacts from a Minute (summary, to-dos, chapters); 5. Upload audio/video to generate a Minute — also supports converting local audio/video files into transcripts, verbatim transcripts, text drafts, or written content; 6. Update a Minute's title (rename); 7. Replace a speaker in a Minute's verbatim transcript. When requests of this type are encountered, this skill MUST be prioritized. Lark Minutes URL format: http(s)://<host>/minutes/<minute-token>"
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search", "lark_auth_login", "lark_auth_poll", "lark_auth_status", "lark_whoami", "lark_enable_domain"]
---

# minutes (v1)

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling**

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-vc/references/vc-domain-boundaries.md`](../lark-vc/references/vc-domain-boundaries.md)**. Skipping this will cause incorrect command usage, meeting artifact decisions, and domain boundary responsibility errors:
> 1. Understand the relationships and responsibilities between Calendar & VC, meeting artifacts & documents
> 2. Understand the relationships between meeting artifacts (Minutes and meeting notes), e.g.: **Minutes and meeting notes are generated independently of each other**
> 3. Understand the components of different meeting artifacts to decide which artifact's data to use based on requirements
> 4. Understand the standard process for meeting summaries, analysis, and information extraction

## Core Concepts

- **Minutes**: Originate from Lark Video Conference recordings or user-uploaded audio/video files; identified by `minute_token`.
- **Minute Token (`minute_token`)**: The unique identifier for a Minute, extractable from the end of a Minutes URL (e.g. `obcnxxxxxxxxxxxxxxxxxxxx` from `https://*.feishu.cn/minutes/obcnxxxxxxxxxxxxxxxxxxxx`). If the URL contains extra parameters (e.g. `?xxx`), extract the last segment of the path.

## Core Scenarios

### 1. Search Minutes

1. When the user describes "my Minutes", "Minutes containing a keyword", or "Minutes within a time range", prefer `lark_api({ tool: 'minutes', op: 'search', args: {...} })`.
2. Only filtering by keyword, time range, participants, and owner is supported; for unsupported filter conditions, notify the user.
3. When search results contain multiple records, pay careful attention to pagination — do not miss any Minute records.
4. For Minutes from a meeting, prefer using [vc +search](../lark-vc/references/lark-vc-search.md) to locate the meeting first, then retrieve the `minute_token` via [vc +recording](../lark-vc/references/lark-vc-recording.md) as needed.
5. Routing for meeting-context Minutes, and how "Minutes I participated in" is interpreted, are governed by [minutes +search](references/lark-minutes-search.md).


### 2. View Basic Minute Info

1. When the user only needs to confirm basic info such as title, cover, duration, owner, or URL of a Minute, use `lark_api({ tool: 'minutes', op: 'minutes-get', args: { minute_token: '<token>' } })`.
2. If the user provides a Minutes URL, first extract the `minute_token` from the end of the URL, then call `lark_api({ tool: 'minutes', op: 'minutes-get', args: { minute_token: '<token>' } })`.
3. For basic Minute info in a meeting / calendar context, first obtain the `minute_token` via the VC path, then call `lark_api({ tool: 'minutes', op: 'minutes-get', args: { minute_token: '<token>' } })`.
4. When user intent is unclear, default to providing basic metadata first to help confirm whether the target Minute has been identified.

> Use `lark_api_search({ query: 'minutes minutes-get' })` to view the full response structure. Core fields: `title` (title), `cover` (cover URL), `duration` (duration in milliseconds), `owner_id` (owner ID), `url` (Minutes link).

### 3. Download Minute Audio/Video Files

1. Download a Minute's audio/video file locally, or obtain a download link valid for 1 day. See [minutes +download](references/lark-minutes-download.md).
2. `lark_api({ tool: 'minutes', op: 'download', args: {...} })` handles audio/video media files only.
3. If the user only wants a shareable download URL, use `url_only: true`; if the user wants the file saved locally, download directly.
4. When no path is explicitly specified, the file defaults to `./minutes/{minute_token}/<server-filename>`, sharing the same directory as `vc +notes` verbatim transcripts for easy aggregation.

> **Note**: `lark_api({ tool: 'minutes', op: 'download', args: {...} })` handles audio/video media files only. If the user needs verbatim transcripts, summaries, to-dos, chapters, or other meeting note content, use `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: '<token>' } })`.

### 4. Retrieve Verbatim Transcript, Summary, To-Dos, and Chapters from a Minute

1. When the user says "verbatim transcript of this Minute", "summary", "to-dos", or "chapters", **this is NOT handled by this skill**.
2. Use `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: '<token>' } })` to retrieve the corresponding meeting note artifacts.
3. If the current context already has a `minute_token`, pass it directly; if only a Minutes URL is available, extract the `minute_token` first.
4. If the user provides a **local audio/video file** but the goal is "convert to meeting notes", "convert to verbatim transcript", "convert to text draft", or "convert to written content", this is also supported; first upload the file to generate a Minute per section 5 below, then extract `minute_token` from the returned `minute_url` and call `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: '<token>' } })`.
5. If the user provides a local filename or path directly and requests "convert to verbatim transcript", "convert to text draft", or "organize into written content", this is also an explicit trigger for this skill.

```javascript
// Retrieve meeting note artifacts (verbatim transcript, summary, to-dos, chapters) via minute_token
lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: '<minute_token>' } })
```

> **Cross-skill routing**: Verbatim transcripts, AI summaries, to-dos, chapters, and other meeting note content are provided by the `notes` operation in [lark-vc](../lark-vc/SKILL.md)

### 5. Upload Audio/Video File to Generate a Minute (and optionally retrieve meeting notes / verbatim transcript)

1. Use when the user needs to upload a local audio/video file to generate a Minute.
2. When the user says "convert audio/video file to meeting notes", "convert recording to verbatim transcript / text draft / written content", or "convert mp4/mp3 to summary / to-dos / chapters", also enter via this path.
3. **Workflow**:
   - **Upload audio/video to obtain `file_token`**: Use `lark_api({ tool: 'drive', op: 'upload', args: {...} })` to upload the local file to Drive (cloud storage) and obtain the `file_token`.
   - **Generate the Minute**: Once `file_token` is obtained, call `lark_api({ tool: 'minutes', op: 'upload', args: { file_token: '<token>', ... } })` to convert the file into a Minute and obtain the `minute_url` link.
   - **Retrieve meeting notes / verbatim transcript (as needed)**: If the user's goal is not just the Minutes link but meeting notes, verbatim transcript, summary, to-dos, or chapters, extract `minute_token` from `minute_url` and call `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: '<token>' } })` to retrieve the corresponding artifacts.

> **Note**: You MUST obtain the `file_token` from Lark Drive (cloud storage) before conversion.
>
> **DO NOT fall back to local transcription tools**: When the user's goal is to convert a local audio/video file to meeting notes, verbatim transcript, text draft, or written content, do NOT substitute `ffmpeg`, `whisper`, or any other local ASR/transcoding command; the standard path is `lark_api drive upload -> lark_api minutes upload -> lark_api vc notes`.

## Resource Relationships

```text
Minutes (Minute) ← identified by minute_token
├── Metadata (title, cover, duration, owner, url) → lark_api({ tool: 'minutes', op: 'minutes-get' })
└── MediaFile (audio/video file) → lark_api({ tool: 'minutes', op: 'download' })
```

> **Capability boundary**: `minutes` handles **searching Minutes, viewing basic metadata, downloading audio/video files, uploading audio/video to generate Minutes**.
>
> **Routing rules**:
>
> - User says "Minutes list / search Minutes / Minutes with a keyword" → `lark_api({ tool: 'minutes', op: 'search', args: {...} })`
> - User simply wants "my Minutes / Minutes within a time range / Minutes list" — do NOT route to [lark-vc](../lark-vc/SKILL.md) first; use this skill directly
> - If the user simultaneously mentions "meeting / a meeting / a specific meeting", even if they also mention "Minutes", prefer routing to [lark-vc](../lark-vc/SKILL.md) to locate the meeting first, then retrieve `minute_token` via `lark_api({ tool: 'vc', op: 'recording', args: {...} })`
> - If the user wants basic Minute info, use `lark_api({ tool: 'minutes', op: 'minutes-get', args: { minute_token: '<token>' } })` after obtaining `minute_token`; if the user wants verbatim transcript, text draft, written content, summary, to-dos, or chapters, proceed with `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: '<token>' } })`
> - Natural-language mappings for "my Minutes", "Minutes I participated in", etc. are governed by [minutes +search](references/lark-minutes-search.md)
> - When results span multiple pages, use `page_token` to paginate until confirmed no more results
> - `lark_api({ tool: 'minutes', op: 'search' })` returns at most `200` results per call; there is no fixed cap on total results
> - User says "title / duration / cover / link of this Minute" → `lark_api({ tool: 'minutes', op: 'minutes-get', args: { minute_token: '<token>' } })`
> - User says "download video / audio / media file of this Minute" → `lark_api({ tool: 'minutes', op: 'download', args: { minute_token: '<token>' } })`
> - User says "verbatim transcript / text draft / written content / summary / to-dos / chapters of this Minute" → use `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: '<token>' } })`
> - User says "generate a Minute from a file / convert audio/video to Minutes" → upload first to get `file_token`, then use `lark_api({ tool: 'minutes', op: 'upload', args: { file_token: '<token>', ... } })`
> - User says "convert audio/video file to meeting notes / verbatim transcript / text draft / written content / summary / to-dos / chapters" → upload to get `file_token`, call `lark_api({ tool: 'minutes', op: 'upload' })` to get `minute_url`, extract `minute_token`, then call `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: '<token>' } })`
> - User says "rename Minute / change Minute title / modify Minute name" → `lark_api({ tool: 'minutes', op: 'update', args: { minute_token: '<token>', ... } })`
> - User says "replace speaker / change speaker A's lines to B / re-attribute speaker" → `lark_api({ tool: 'minutes', op: 'speaker-replace', args: { minute_token: '<token>', ... } })`

## Shortcuts (use these first when available)

Shortcuts are high-level wrappers for common operations. When a Shortcut exists, use it first via `lark_api({ tool: 'minutes', op: '<verb>', args: {...} })`.

| Shortcut                                           | MCP Op                                              | Description                                                              |
| -------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------ |
| [`+search`](references/lark-minutes-search.md)     | `lark_api({ tool: 'minutes', op: 'search' })`       | Search minutes by keyword, owners, participants, and time range |
| [`+download`](references/lark-minutes-download.md) | `lark_api({ tool: 'minutes', op: 'download' })`     | Download audio/video media file of a minute                     |
| [`+upload`](references/lark-minutes-upload.md)     | `lark_api({ tool: 'minutes', op: 'upload' })`       | Upload a media file token to generate a minute                  |
| [`+update`](references/lark-minutes-update.md)     | `lark_api({ tool: 'minutes', op: 'update' })`       | Update a minute's title                                         |
| [`+speaker-replace`](references/lark-minutes-speaker-replace.md) | `lark_api({ tool: 'minutes', op: 'speaker-replace' })` | Replace a speaker in a minute's transcript (rebind from one user to another) |

- When using the `search` op, MUST read [references/lark-minutes-search.md](references/lark-minutes-search.md) to understand search parameters and response structure.
- When using the `download` op, MUST read [references/lark-minutes-download.md](references/lark-minutes-download.md) to understand download parameters and response structure.
- When using the `upload` op, MUST read [references/lark-minutes-upload.md](references/lark-minutes-upload.md) to understand generation parameters and response structure.
- When using the `update` op, MUST read [references/lark-minutes-update.md](references/lark-minutes-update.md) to understand update parameters and response structure.
- When using the `speaker-replace` op, MUST read [references/lark-minutes-speaker-replace.md](references/lark-minutes-speaker-replace.md) to understand parameters and limitations (user ID only; names not supported).

<!-- AUTO-GENERATED-START — managed by gen-skills.py, do not edit manually -->

## API Resources

```javascript
lark_api_search({ query: 'minutes <resource> <method>' })   // MUST check parameter structure before calling the API
lark_api({ tool: 'minutes', op: '<resource>-<method>', args: {...} })  // Call the API
```

> **Important**: When using native APIs, MUST run `lark_api_search` first to view parameter structure. Do not guess field formats.

### minutes

- `minutes-get` — Get Minute info — `lark_api({ tool: 'minutes', op: 'minutes-get', args: { minute_token: '<token>' } })`

> **Permission error**: If `[2091005] permission deny` is returned, the user does not have read access to the Minute file; prompt the user to contact the Minute owner to request access.

## Permission Table

| Method          | Required scope                   |
| --------------- | -------------------------------- |
| `+search`       | `minutes:minutes.search:read`    |
| `minutes.get`   | `minutes:minutes:readonly`       |
| `+download`     | `minutes:minutes.media:export`   |
| `+update`       | `minutes:minutes:update`         |
| `+speaker-replace` | `minutes:minutes:update`      |

<!-- AUTO-GENERATED-END -->
