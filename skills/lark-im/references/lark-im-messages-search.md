# im +messages-search

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand authentication, global parameters, and safety rules.

Search Feishu messages across conversations. This shortcut automatically performs a multi-step workflow: search for message IDs, batch fetch message details, then enrich the results with chat context.

By default each result message also carries a `reactions` block (counts + details from `im.reactions.batch_query`) when the server has reactions for it, and `update_time` for messages that were actually edited. Pass `no_reactions: true` to skip the extra round-trip. See [message enrichment](lark-im-message-enrichment.md) for the full contract.

> **User identity only** (`as: 'user'`). Bot identity is not supported.

This skill maps to the shortcut: `lark_api({ tool: 'im', op: 'messages-search' })` (internally calls `POST /open-apis/im/v1/messages/search` + batched `GET /open-apis/im/v1/messages/mget`, then batch-fetches chat context).

## Commands

```js
// Search by keyword
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'project progress' } })

// Restrict search to a specific group chat
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'weekly report', chat_id: 'oc_xxx' } })

// Filter by sender (comma-separated)
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'requirement', sender: 'ou_xxx,ou_yyy' } })

// Filter by attachment type
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'report', include_attachment_type: 'file' } })

// Filter by chat type (group / p2p)
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'progress', chat_type: 'group' } })

// Filter by sender type (user / bot)
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'reminder', sender_type: 'bot' } })

// Exclude bot senders
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'reminder', exclude_sender_type: 'bot' } })

// Only messages that @me
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'announcement', is_at_me: true } })

// Only messages that @mention specific users (results also include messages that @all)
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'release', at_chatter_ids: 'ou_xxx,ou_yyy' } })

// Combined filters + time range
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'meeting', sender: 'ou_xxx', chat_type: 'group', start: '2026-03-13T00:00:00+08:00', end: '2026-03-20T23:59:59+08:00' } })

// Specific time range (ISO 8601)
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'release', start: '2026-03-01T00:00:00+08:00', end: '2026-03-10T00:00:00+08:00' } })
```

## Parameters

| Parameter | Required | Description |
|------|------|------|
| `query` | No | Search keyword (may be empty when used with other filters) |
| `chat_id` | No | Restrict to chat IDs, comma-separated (`oc_xxx,oc_yyy`) |
| `sender` | No | Sender open_ids, comma-separated (`ou_xxx`) |
| `include_attachment_type` | No | Attachment filter: `file` / `image` / `video` / `link` |
| `chat_type` | No | Chat type: `group` / `p2p` |
| `sender_type` | No | Sender type: `user` / `bot` |
| `exclude_sender_type` | No | Exclude messages from `user` or `bot` senders |
| `is_at_me` | No | Only return messages that mention `@me` |
| `at_chatter_ids` | No | Filter by @mentioned user open_ids, comma-separated (`ou_xxx,ou_yyy`). Matched results also include messages that `@all` |
| `start` | No | Start time with local timezone offset required (e.g. `2026-03-24T00:00:00+08:00`) |
| `end` | No | End time with local timezone offset required (e.g. `2026-03-25T23:59:59+08:00`) |
| `as` | No | Identity type (defaults to and only supports `user`) |

## Core Constraints

### 1. Provide at least one filter whenever possible

All parameters are optional, but you should usually provide at least one filter (`query`, `sender`, `chat_id`, etc.). Otherwise the search scope may be too broad and return low-signal results.

### 2. Two-step orchestration is automatic

The shortcut automatically performs:

1. The **search API** returns matching `message_id` values
2. The **mget API** fetches full message content for those message IDs in batch
3. Chat context lookup is fetched in batch and attached to each message

The user does not need to manage the orchestration manually. When search results span multiple pages, continue with the `page_token` returned in the response.

### 3. Conversation context is enriched automatically

In JSON output, each message automatically includes conversation context:

| Field | Description |
|------|------|
| `chat_type` | Conversation type: `p2p` / `group` |
| `chat_name` | Group name (for groups) or the other participant's name (for p2p chats) |
| `chat_partner` | For p2p only: the other participant's `open_id` and `name` |

In pretty output, the `chat` column shows the chat name for groups, or `"p2p"` for direct messages.

Each message in JSON output contains:

| Field | Description |
|------|------|
| `message_id` | Message ID |
| `msg_type` | Message type: `text`, `image`, `file`, `interactive`, `post`, `audio`, `video`, `system`, etc. |
| `create_time` | Creation time |
| `sender` | Sender information (includes `name` for user senders) |
| `content` | Message content |
| `chat_id` | ID of the conversation the message belongs to |
| `deleted` | Whether the message has been recalled (`true` = recalled) |
| `updated` | Whether the message has been edited after sending |
| `mentions` | Array of @mentions in the message; each item contains `{id, key, name}`. Present only when the message contains @mentions |
| `thread_id` | Thread ID (`omt_xxx`) if the message has replies in a thread. Present only when replies exist |

### 4. Pagination behavior

- Default behavior is **single-page**.
- `page_token` is the manual continuation mechanism when you already have a token from a previous response.
- The response includes the last `has_more` / `page_token` so you can continue fetching the next page.

### 5. Search results contain follow-up clues

In JSON output, each message includes `chat_id` and `thread_id` (when present). Use them with other shortcuts for deeper inspection:

```js
// View the full message stream for the conversation that contains the search result
lark_api({ tool: 'im', op: 'chat-messages-list', args: { chat_id: '<chat_id>' } })

// View replies in the thread that contains the search result
lark_api({ tool: 'im', op: 'threads-messages-list', args: { thread: '<thread_id>' } })
```

## Resource Rendering

Search results reuse the same content formatter as other read commands. Image messages are rendered as placeholders such as `[Image: img_xxx]`; resource binaries are **not** downloaded automatically.

Use `messages-resources-download` if you need to fetch the underlying image or file bytes from a specific message.

## AI Usage Guidance

### Query boundary for activity review

Use `query` only for real message keywords. If the user asks for activity review such as "最近一周我和哪些 Bot 有过交互" or "整理我和某人的聊天记录", and the useful constraints are sender type, chat, person, or time range, keep `query: ''` and rely on those filters. Do not put generic instruction words such as "看看", "总结", "交互内容", or "聊天记录" into `query`; those words often over-constrain message search and hide the relevant messages.

This guidance applies only when using user identity. `messages-search` is user-only; if the user explicitly asks for application/bot identity, do not try `as: 'bot'`. For bot identity with a named group and history/listing intent, resolve the group with `chat-search` (`as: 'bot'`), then list messages with `chat-messages-list` (`as: 'bot'`, `chat_id: '<chat_id>'`).

```js
// Review recent bot interactions without forcing a keyword
lark_api({ tool: 'im', op: 'messages-search', args: { query: '', sender_type: 'bot', start: '<YYYY-MM-DDT00:00:00+08:00>', end: '<YYYY-MM-DDT23:59:59+08:00>' } })
```

Replace the time placeholders at execution time. For example, "最近一周" means computing the start date and end date from the current day before running the command; do not copy date literals from this reference into answers for relative requests.

For activity summaries, validate evidence by message IDs and chat context. The final answer should cite or retain the `message_id`, sender, chat, and create time for each important item. If the row's source data contains concrete `om_...` message IDs or `ou_...` user IDs, treat those IDs as strong recall targets during verification; do not rely only on a high-level keyword match.

### Resolving chat_id from a chat name

When the user refers to a chat by name and you need its `chat_id` for the `chat_id` filter, use [`chat-search`](lark-im-chat-search.md) first:

```js
// Step 1: Find the chat_id by name
lark_api({ tool: 'im', op: 'chat-search', args: { query: '<chat name keyword>' } })

// Step 2: Use the chat_id to narrow down message search
lark_api({ tool: 'im', op: 'messages-search', args: { query: 'keyword', chat_id: '<chat_id>' } })
```

**Do not use `chats.search` or `chat-list` — always use the `chat-search` shortcut.**

## Work Summary / Report Generation

When the user asks you to summarize work, generate a weekly report, or compile activity from chat messages, you should **paginate through all available results** to get a complete picture. A single page is rarely enough for thorough summarization.

### Strategy

1. **Start with targeted filters** — use `chat_id`, `sender`, `start`, `end` to narrow the scope as much as possible before paginating.
2. **Accumulate before summarizing** — collect all pages of messages first, then analyze and summarize. Do not summarize after the first page alone — you will miss important context.
3. **Continue with `page_token` when resuming** — if the response has `has_more=true`, continue from the returned `page_token`.
4. **The response includes `has_more` and `page_token`** — use those fields to drive pagination.

### Example: Weekly work summary from a project chat

```js
// Fetch the first page
lark_api({ tool: 'im', op: 'messages-search', args: { query: '', chat_id: 'oc_xxx', sender: 'ou_me', start: '2026-03-18T00:00:00+08:00', end: '2026-03-25T23:59:59+08:00' } })

// If the response returns has_more=true, continue with the returned page_token
lark_api({ tool: 'im', op: 'messages-search', args: { query: '', chat_id: 'oc_xxx', sender: 'ou_me', start: '2026-03-18T00:00:00+08:00', end: '2026-03-25T23:59:59+08:00', page_token: '<token_from_previous_run>' } })
```

### Key points

- **Always paginate exhaustively** for summary tasks. A single page of 20-50 messages is usually insufficient for a meaningful work summary.
- Continue with `page_token` until `has_more=false`.
- If the user does not specify a time range, default to the current week (Monday to today) for weekly reports, or ask for clarification.
- When summarizing, group messages by topic/thread rather than by chronological order for better readability.

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|---------|---------|
| Too few results | The time range is too narrow or the keyword is too specific | Expand the time range and try broader keywords |
| No results | Missing permission or no match | Confirm `search:message` is authorized and relax the filters |
| Permission denied | Search scope not authorized | Run `lark_auth_login({ scope: 'search:message' })` |

## References

- [lark-im](../SKILL.md) - all message-related commands
- [lark-im-threads-messages-list](lark-im-threads-messages-list.md) - inspect thread replies
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
