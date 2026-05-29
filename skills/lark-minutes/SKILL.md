---
name: lark-minutes
version: 2.0.0
description: "Use this skill when operating Lark Minutes via LarkSkill MCP: search Minutes, get basic info, download audio/video, get AI outputs (summary, to-dos, chapters), upload audio/video to generate Minutes, rename a Minute, and replace a speaker. Prefer over local tools like ffmpeg or whisper."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# minutes

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first.
> **Mandatory before execution:** Before invoking any `minutes` operation, read the corresponding command reference doc, then call the operation via `lark_api`.
> **Naming convention:** Minutes operations call `lark_api({ tool: 'minutes', op: '<op>', args: {...} })`.

## Core Concepts

- **Minutes**: originates from Lark video conference recordings or user-uploaded audio/video files, identified by `minute_token`.
- **Minute Token (`minute_token`)**: the unique identifier for a Minute, extracted from the end of the Minutes URL (e.g. `obcnxxxxxxxxxxxxxxxxxxxx` from `https://*.feishu.cn/minutes/obcnxxxxxxxxxxxxxxxxxxxx`). If the URL contains extra parameters (e.g. `?xxx`), take the last path segment.

## Core Scenarios

### 1. Search Minutes

1. When the user describes "my Minutes", "Minutes containing a keyword", or "Minutes from a time period", use `lark_api({ tool: 'minutes', op: 'search', args: {...} })`.
2. Only keyword, time range, participant, and owner filters are supported; for unsupported filters, inform the user.
3. When search results contain multiple records, always paginate to ensure no Minutes are missed.
4. For meeting Minutes, prefer using `lark_api({ tool: 'vc', op: 'search', args: {...} })` to locate the meeting first, then retrieve the `minute_token` via `lark_api({ tool: 'vc', op: 'recording', args: {...} })`.
5. Meeting-context Minutes routing and how "participated Minutes" is interpreted follow [minutes search](references/lark-minutes-search.md) as the authority.


### 2. View Minutes Basic Info

1. When the user only needs basic info (title, cover, duration, owner, URL) for a Minute, use `lark_api({ tool: 'minutes', op: 'minutes.get', args: { minute_token: '...' } })`.
2. If the user provides a Minutes URL, extract the `minute_token` from the end of the URL first.
3. For Minutes basic info in a meeting or calendar context, first get the `minute_token` via the VC path.
4. When user intent is unclear, default to providing basic metadata first to confirm the correct Minute.

> Use `lark_api_search` with `minutes.minutes.get` to view the complete return value structure. Core fields: `title`, `cover`, `duration` (milliseconds), `owner_id`, `url`.

### 3. Download Minutes Audio/Video Files

1. Download Minutes audio/video files locally, or obtain a download link valid for 1 day. See [minutes download](references/lark-minutes-download.md).
2. `minutes download` handles audio/video media files only.
3. When the user only wants a shareable download URL, pass `url_only: true`; when they want the file saved locally, download directly.
4. When no path is specified, files default to `./minutes/{minute_token}/<server-filename>`, sharing the same directory as `vc notes` transcripts for easy aggregation.

> **Note**: `minutes download` handles audio/video media files only. For transcript, summary, to-dos, or chapters, use `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: ['...'] } })`.

### 4. Get Transcript, Summary, To-dos, and Chapters

1. When the user asks for "transcript", "summary", "to-dos", or "chapters" from a Minute, **this is NOT handled by this skill**.
2. Use `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: ['<minute_token>'] } })`.
3. If a `minute_token` is already in context, pass it directly; if only a Minutes URL is available, extract `minute_token` first.
4. If the user provides a **local audio/video file** to convert to notes/transcript/text draft/written content, first upload per section 5 below, then use `vc notes`.
5. If the user directly gives a local file name or path and asks to "convert to transcript", "convert to text draft", or "organize into written content", this is also a clear trigger signal for this skill.

```javascript
// Get notes output (transcript, summary, to-dos, chapters) via minute_token
lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: ['<minute_token>'] } })
```

> **Cross-skill routing**: transcript, AI summary, to-dos, and chapters are provided by the `notes` operation in [lark-vc](../lark-vc/SKILL.md).

### 5. Upload Audio/Video to Generate Minutes (and optionally continue to get notes / transcript)

1. Use when the user needs to generate Minutes from a local audio/video file.
2. Also use when the user says "convert audio/video to notes", "convert recording to transcript/text draft/written content", or "convert mp4/mp3 to summary/to-dos/chapters".
3. **Processing flow**:
   - **Upload audio/video to get `file_token`**: use `lark_api({ tool: 'drive', op: 'upload', args: {...} })` to upload the local file to Lark Drive and get `file_token`.
   - **Generate Minutes**: call `lark_api({ tool: 'minutes', op: 'upload', args: { file_token: '...' } })` to generate Minutes and get `minute_url`.
   - **Continue to get notes (as needed)**: extract `minute_token` from `minute_url`, then call `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: ['<minute_token>'] } })`.

> **Note**: you MUST obtain the Lark Drive `file_token` before conversion.
>
> **Do not use local transcription tools**: when the goal is to convert a local audio/video file into notes, transcript, text draft, or written content, do not switch to `ffmpeg`, `whisper`, or other local ASR/transcoding commands; the standard path is `drive upload → minutes upload → vc notes`.

### 6. Edit Minutes (rename, replace speaker)

Minutes also supports two edit operations — renaming a Minute and replacing a speaker in its transcript. These are not part of the fixed operation set above, so discover the exact operation with `lark_api_search` first, then invoke the resolved operation via `lark_api`.

1. **Rename a Minute** — when the user says "rename a Minute", "change a Minute's title", or "modify a Minute's name", run `lark_api_search` for the Minutes title-update operation (e.g. query `"minutes update title"`), then call the resolved operation via `lark_api` with the `minute_token` and new title.
2. **Replace a speaker** — when the user says "replace a speaker", "change A's remarks to B", or "reassign the speaker", run `lark_api_search` for the Minutes speaker-replace operation (e.g. query `"minutes speaker replace"`), then call the resolved operation via `lark_api`. This operation supports user IDs only; names are not supported, so resolve names to user IDs first.

> **Note**: the rename and speaker-replace operations require the `minutes:minutes:update` scope. If `lark_api_search` returns nothing, the operation may not be enabled for the current profile — inform the user.

## Resource Relationships

```text
Minutes ← identified by minute_token
├── Metadata (title, cover, duration, owner, url) → lark_api({ tool: 'minutes', op: 'minutes.get', ... })
└── MediaFile (audio/video file) → lark_api({ tool: 'minutes', op: 'download', ... })
```

> **Capability boundaries**: `minutes` handles **searching Minutes, viewing basic metadata, downloading audio/video files, uploading audio/video to generate Minutes, renaming Minutes, and replacing speakers in a transcript**.
>
> **Routing rules**:
>
> - "Minutes list / search Minutes / Minutes with keyword" → `lark_api({ tool: 'minutes', op: 'search', args: {...} })`
> - "My Minutes / Minutes from a time period" → use this skill directly, do not go to lark-vc first
> - User mentions "meeting / conference / a specific meeting" with "Minutes" → use lark-vc to locate meeting first, get `minute_token` via `lark_api({ tool: 'vc', op: 'recording', args: {...} })`
> - "Title / duration / cover / link of this Minute" → `lark_api({ tool: 'minutes', op: 'minutes.get', args: {...} })`
> - "Download video / audio / media file of this Minute" → `lark_api({ tool: 'minutes', op: 'download', args: {...} })`
> - "Transcript / text draft / written content / summary / to-dos / chapters of this Minute" → `lark_api({ tool: 'vc', op: 'notes', args: { minute_tokens: ['...'] } })`
> - "Generate Minutes from a file / convert audio/video to Minutes" → `drive upload` → `lark_api({ tool: 'minutes', op: 'upload', args: {...} })`
> - "Convert audio/video to notes / transcript / text draft / written content / summary / to-dos / chapters" → `drive upload` → `minutes upload` → `vc notes`
> - When results have multiple pages, use `page_token` to paginate until no more results
> - `minutes search` returns at most `200` results per call; total results have no fixed upper bound
> - "Rename a Minute / change a Minute's title / modify a Minute's name" → discover via `lark_api_search` ("minutes update title"), then invoke the resolved operation via `lark_api`
> - "Replace a speaker / change A's remarks to B / reassign the speaker" → discover via `lark_api_search` ("minutes speaker replace"), then invoke the resolved operation via `lark_api` (user IDs only)

## Operations (use via LarkSkill MCP)

| Operation | Description |
|-----------|-------------|
| `lark_api({ tool: 'minutes', op: 'search', args: {...} })` | Search Minutes by keyword, owners, participants, and time range — read [references/lark-minutes-search.md](references/lark-minutes-search.md) first |
| `lark_api({ tool: 'minutes', op: 'download', args: {...} })` | Download audio/video media file of a Minute — read [references/lark-minutes-download.md](references/lark-minutes-download.md) first |
| `lark_api({ tool: 'minutes', op: 'upload', args: { file_token: '...' } })` | Upload a media file token to generate a Minute — read [references/lark-minutes-upload.md](references/lark-minutes-upload.md) first |
| `lark_api_search` → rename operation | Update a Minute's title (rename); discover the exact op with `lark_api_search`, then invoke via `lark_api` — read [references/lark-minutes-update.md](references/lark-minutes-update.md) first |
| `lark_api_search` → speaker-replace operation | Replace a speaker in a Minute's transcript (rebind from one user to another; user IDs only); discover the exact op with `lark_api_search`, then invoke via `lark_api` — read [references/lark-minutes-speaker-replace.md](references/lark-minutes-speaker-replace.md) first |

## API Resources

> **Important**: Use `lark_api_search` to look up parameter structure before raw API calls.

### minutes.get

```javascript
lark_api({ tool: 'minutes', op: 'minutes.get', args: { minute_token: '<minute_token>' } })
```

  - `get` — Get Minute info (title, cover, duration, owner_id, url)

## Permissions Table

| Method | Required scope |
|--------|---------------|
| `search` | `minutes:minutes.search:read` |
| `minutes.get` | `minutes:minutes:readonly` |
| `download` | `minutes:minutes.media:export` |
| rename (via `lark_api_search`) | `minutes:minutes:update` |
| speaker-replace (via `lark_api_search`) | `minutes:minutes:update` |
