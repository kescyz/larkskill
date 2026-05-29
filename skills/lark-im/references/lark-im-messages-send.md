# im +messages-send

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand authentication, global parameters, and safety rules.

Send a message to a group chat or a direct message conversation. Supports both user identity (`as: 'user'`) and bot identity (`as: 'bot'`).

This skill maps to the shortcut: `lark_api({ tool: 'im', op: 'messages-send' })` (internally calls `POST /open-apis/im/v1/messages`).

## Safety Constraints

Messages sent by this tool are visible to other people. Before calling it, you **must** confirm with the user:

1. The recipient (which person or which group)
2. The message content
3. The sending identity (user or bot)

**Do not** send messages without explicit user approval.

When using `as: 'bot'`, the message is sent in the app's name, so make sure the app has already been added to the target chat.

When using `as: 'user'`, the message is sent as the authorized end user and requires the `im:message.send_as_user` and `im:message` scopes.

## Choose The Right Content Flag

| Need | Recommended arg | Why |
|------|------|------|
| Send plain text exactly as written | `text` | Wrapped directly to `{"text":"..."}`; no Markdown conversion |
| Send simple Markdown and accept Feishu-style rendering | `markdown` | Automatically converted to `post` JSON |
| Precisely control the final payload | `content` | You provide the exact JSON for `text` / `post` / `interactive` / `share_*` / media payloads |
| Send image / file / video / audio | `image` / `file` / `video` / `audio` | Shortcut uploads URLs, or cwd-relative local files automatically |

### `text` vs `markdown`

- Use `text` when the content should stay as plain text, including exact line breaks, indentation, code samples, shell snippets, or Markdown characters that should **not** be reinterpreted.
- Use `markdown` when you want basic Markdown-style rendering and you accept that the shortcut will normalize and rewrite parts of the content before sending.
- Use `content` when `markdown` is not enough, especially if you need exact `post` JSON, a title, multiple locales, cards, or unsupported rich structures.

## What `markdown` Really Does

`markdown` is **not** sent as raw Markdown API content.

The shortcut does all of the following before sending:

1. Forces `msg_type=post`
2. Resolves remote Markdown images like `![x](https://...)` by downloading and uploading them first
3. Normalizes the Markdown for Feishu post rendering
4. Wraps the result as:

```json
{"zh_cn":{"content":[[{"tag":"md","text":"..."}]]}}
```

This means `markdown` is convenient, but it is not a full-fidelity Markdown transport.

### Current Markdown Caveats

- It does **not** promise full CommonMark / GitHub Flavored Markdown support.
- It always becomes a `post` payload with a single `zh_cn` locale.
- It does **not** let you set a `post` title. If you need a title, use `msg_type: 'post'` with `content`.
- Headings are rewritten:
    - `# Title` becomes `#### Title`
    - `##` to `######` are normalized to `#####` when the content contains H1-H3
- Consecutive headings are separated with blank lines after heading normalization.
- Block spacing and line breaks may be normalized during conversion.
- Code blocks are preserved as code blocks.
- Excess blank lines are compressed.
- Already-uploaded `img_xxx` image keys are the most reliable Markdown image input.
- Local paths in Markdown image syntax like `![x](./a.png)` are **not** supported and will not be auto-uploaded.
- Remote URLs (`https://...`) will be auto-downloaded and uploaded at runtime; if the download or upload fails, the image is removed with a warning.

If any of the above is unacceptable, do **not** use `markdown`; use `content` and provide the final JSON yourself.

### Image Constraint for `markdown`

When using `markdown` with images, prefer pre-uploading via `images.create` and referencing `![alt](img_xxx)` for predictable results. Remote URLs may work but are not guaranteed.

**Steps:**

```js
// 1. Upload image to get image_key
lark_api({ tool: 'im', op: 'images.create', args: { data: { image_type: 'message' }, file: './diagram.png' } })
// Returns: {"image_key":"img_v3_xxxx"}

// 2. Use image_key in markdown
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', markdown: '## Report\n\n![diagram](img_v3_xxxx)\n\nSee above for details.' } })
```

## Preserving Formatting

If the message has multiple lines, indentation, code blocks, tabs, or many quotes/backslashes, put explicit `\n` escapes inside the string value.

### When formatting must be preserved

Use `text`:

```js
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', text: 'Build failed\nBranch: feature/im-docs\nAction: please check logs' } })
```

```js
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', text: '```bash\nmake test\nmake lint\n```' } })
```

Use this path when you want the receiver to see the text exactly as entered, not a converted Markdown post.

### When formatting does not need exact preservation

Use `markdown`:

```js
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', markdown: '## Release Notes\n\n- Added send shortcut\n- Added reply shortcut' } })
```

This is better for lightweight readable formatting, but the final content may not match the source text byte-for-byte because the shortcut normalizes headings and spacing before sending.

## Commands

```js
// Send plain text (text is recommended for normal messages)
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', text: 'Hello' } })

// Equivalent manual JSON
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', content: '{"text":"Hello"}' } })

// Send to a direct message (pass open_id)
lark_api({ tool: 'im', op: 'messages-send', args: { user_id: 'ou_xxx', text: 'Hello' } })

// Send multi-line text while preserving formatting
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', text: 'Line 1\nLine 2\n  indented line' } })

// Send basic Markdown (will be converted to post JSON)
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', markdown: '## Update\n\n- item 1\n- item 2' } })

// Send Markdown with an image (must pre-upload via images.create)
lark_api({ tool: 'im', op: 'images.create', args: { data: { image_type: 'message' }, file: './screenshot.png' } })
// Use the returned image_key in the markdown content
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', markdown: '## Status\n\n![screenshot](img_v3_xxxx)\n\nDone.' } })

// If you need exact post structure, send JSON directly
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', msg_type: 'post', content: '{"zh_cn":{"title":"Title","content":[[{"tag":"text","text":"Body"}]]}}' } })

// Send a local image (uploaded automatically before sending)
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', image: './photo.png' } })

// Or send directly with an existing image_key
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', image: 'img_xxx' } })

// Send a local file (uploaded automatically before sending)
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', file: './report.pdf' } })

// Send a video (video_cover is required as the cover)
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', video: './demo.mp4', video_cover: './cover.png' } })
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', video: './demo.mp4', video_cover: 'img_xxx' } })

// Send audio
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', audio: './voice.opus' } })

// Use an idempotency key (same key sends only once within 1 hour)
lark_api({ tool: 'im', op: 'messages-send', args: { chat_id: 'oc_xxx', text: 'Hello', idempotency_key: 'my-unique-id' } })
```

## Media Input Rules

- Media flags accept an existing key (`img_xxx` / `file_xxx`), an `http://` or `https://` URL, or a local file path.
- Local paths must be relative to the current working directory and stay within it after resolving `..` and symlinks.
- Absolute paths such as `/tmp/photo.png` are rejected. Run the command from the file's directory and pass `./photo.png`, or copy the file into the current directory first.

## Parameters

| Parameter | Required | Description                                                                                                                                                                                   |
|------|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `chat_id` | One of two | Group chat ID (`oc_xxx`)                                                                                                                                                                      |
| `user_id` | One of two | User open_id (`ou_xxx`) for direct messages                                                                                                                                                   |
| `text` | One content option | Plain text message. Best default for exact text and preserved formatting. Automatically wrapped as `{"text":"..."}`                                                                           |
| `markdown` | One content option | Convenience Markdown input. Internally converted to `post` JSON with Feishu-specific normalization; not full Markdown passthrough                                                             |
| `content` | One content option | Exact message content JSON string; use this when you need full control over `msg_type` and payload. The JSON must match the effective `msg_type`                                            |
| `image` | One content option | Cwd-relative local image path, URL, or `image_key` (`img_xxx`). Local paths and URLs are uploaded automatically                                                                               |
| `file` | One content option | Cwd-relative local file path, URL, or `file_key` (`file_xxx`). Local paths and URLs are uploaded automatically                                                                                |
| `video` | One content option | Cwd-relative local video path, URL, or `file_key` (`file_xxx`). Local paths and URLs are uploaded automatically. **Must be paired with `video_cover`**                                      |
| `video_cover` | **Required with `video`** | Cwd-relative local cover image path, URL, or `image_key` (`img_xxx`). Local paths and URLs are uploaded automatically                                                                         |
| `audio` | One content option | Cwd-relative local audio path, URL, or `file_key` (`file_xxx`). Local paths and URLs are uploaded automatically                                                                                           |
| `msg_type` | No | Message type (default `text`). If you use `text` / `markdown` / media args, the effective type is inferred automatically. Explicitly setting a conflicting `msg_type` fails validation |
| `idempotency_key` | No | Idempotency key; the same key sends only one message within 1 hour                                                                                                                            |
| `as` | No | Identity type: `bot` or `user` (default `bot`)                                                                                                                                                |

> **Mutual exclusivity rule:** `text`, `markdown`, `content`, and `image`/`file`/`video`/`audio` cannot be used together. Media args are also mutually exclusive with each other.
>
> **Video cover rule:** `video` **must** be accompanied by `video_cover`. Omitting `video_cover` when using `video` will fail validation. `video_cover` cannot be used without `video`.

## Common Mistakes

- Choosing `markdown` when you actually need exact plain text. If exact line breaks and spacing matter, use `text` with explicit `\n` escapes.
- Assuming `markdown` supports all Markdown features. It does not; it is converted into a Feishu `post` payload and rewritten first.
- Putting local image paths inside Markdown like `![x](./a.png)`. `markdown` does not auto-upload those paths.
- **Using local file paths inside Markdown image syntax** (e.g. `![x](./a.png)`) with `markdown`. Local paths are not auto-uploaded and will not render as an image. Pre-upload via `images.create` to get an `image_key` instead.
- Using `content` without making the JSON match the effective `msg_type`.
- Explicitly setting `msg_type` to something that conflicts with `text`, `markdown`, or media args.
- Mixing `text`, `markdown`, or `content` with media args in one call.

## `content` Format Reference

| `msg_type` | Example `content` |
|----------|-------------|
| `text` | `{"text":"Hello <at user_id=\"ou_xxx\">name</at>"}` |
| `post` | `{"zh_cn":{"title":"Title","content":[[{"tag":"text","text":"Body"}]]}}` |
| `image` | `{"image_key":"img_xxx"}` |
| `file` | `{"file_key":"file_xxx"}` |
| `audio` | `{"file_key":"file_xxx"}` |
| `media` | `{"file_key":"file_xxx","image_key":"img_xxx"}` (video; `image_key` is the cover from `video_cover` — **required**) |
| `share_chat` | `{"chat_id":"oc_xxx"}` |
| `share_user` | `{"user_id":"ou_xxx"}` |
| `interactive` | Card JSON (see Feishu interactive card documentation) |

## Return Value

```json
{
  "message_id": "om_xxx",
  "chat_id": "oc_xxx",
  "create_time": "1234567890"
}
```

## @Mention Format (text / post)

- Recommended format: `<at user_id="ou_xxx">name</at>`
- @all: `<at user_id="all"></at>`
- The shortcut normalizes common variants like `<at id=...>` and `<at open_id=...>` into `user_id`, but you should still document examples with `user_id`

## Notes

- `chat_id` and `user_id` are mutually exclusive; you must provide exactly one
- `content` must be valid JSON
- When using `content`, you are responsible for making the JSON structure match the effective `msg_type`
- `image`/`file`/`video`/`audio` support existing keys, URLs, and cwd-relative local file paths; the shortcut uploads local paths and URLs first, then sends the message; both the upload and send steps use the same identity (UAT when `as: 'user'`, TAT when `as: 'bot'`)
- If the provided media value starts with `img_` or `file_`, it is treated as an existing key and used directly
- `markdown` always sends `msg_type=post`, even if you do not explicitly set `msg_type: 'post'`
- If you explicitly set `msg_type` and it conflicts with the chosen content arg, validation fails
- When using `video`, `video_cover` is required as the video cover
- Failures return an error code and message
- `as: 'user'` uses a user access token (UAT) and requires the `im:message.send_as_user` and `im:message` scopes; the message is sent as the authorized end user
- `as: 'bot'` uses a tenant access token (TAT) and requires the `im:message:send_as_bot` scope
- When sending as a bot, the app must already be in the target group or already have a direct-message relationship with the target user
- When using `markdown` with images, pre-uploading via `images.create` to obtain an `image_key` is recommended for reliability; remote URLs may be auto-resolved at runtime, but if download/upload fails the image is removed with a warning; local paths are not supported
