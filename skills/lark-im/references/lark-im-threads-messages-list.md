# im +threads-messages-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand authentication, global parameters, and safety rules.

Fetch the reply message list inside a thread. When `chat-messages-list` returns messages that include a `thread_id` field, use this command to inspect all replies in that thread.

By default each reply also carries a `reactions` block (counts + details from `im.reactions.batch_query`) when the server has reactions for it, and `update_time` for messages that were actually edited. Pass `no_reactions: true` to skip the extra round-trip. See [message enrichment](lark-im-message-enrichment.md) for the full contract.

This skill maps to the shortcut: `lark_api({ tool: 'im', op: 'threads-messages-list' })` (internally calls `GET /open-apis/im/v1/messages` with `container_id_type=thread` to fetch thread messages).

## Commands

```js
// Get thread replies (ascending by time by default)
lark_api({ tool: 'im', op: 'threads-messages-list', args: { thread: 'omt_xxx' } })

// Reverse chronological order (latest first)
lark_api({ tool: 'im', op: 'threads-messages-list', args: { thread: 'omt_xxx', sort: 'desc' } })

// View as a bot
lark_api({ tool: 'im', op: 'threads-messages-list', args: { thread: 'omt_xxx', as: 'bot' } })
```

## Parameters

| Parameter | Required | Description |
|------|------|------|
| `thread` | Yes | Thread ID (`om_xxx` or `omt_xxx` format) |
| `sort` | No | Sort order: `asc` (default) / `desc` |
| `as` | No | Identity type: `user` (default) / `bot` |

## Core Constraints

### 1. Source of `thread_id`

`thread_id` (`omt_xxx` or `om_xxx`) comes from the `thread_id` field in results returned by `chat-messages-list` or `messages-search`. Do not guess a thread ID. Fetch messages first and use the returned value.

### 2. No time filtering support

Thread messages do not support `start_time` / `end_time` filtering because of Feishu API limitations. Use pagination and sort order to control the scope.

### 3. Pagination (`has_more` / `page_token`)

- When the result includes `has_more=true`, use `page_token` to fetch the next page
- If you need the complete thread, keep paginating; if you only need an overview, the first page is often enough

### 4. Recommended expansion strategy

| Scenario | Recommended Parameters |
|------|---------|
| Quickly inspect recent replies | `sort: 'desc'` |
| Read the full thread in chronological order | `sort: 'asc'`, then paginate as needed |
| Just confirm whether replies exist | `sort: 'desc'` |

## Usage Scenarios

### Scenario 1: Expand a thread discovered in group messages

```js
// Step 1: Fetch group messages and find one that contains thread_id
lark_api({ tool: 'im', op: 'chat-messages-list', args: { chat_id: 'oc_xxx' } })

// Step 2: Extract thread_id from the JSON output and fetch thread replies
lark_api({ tool: 'im', op: 'threads-messages-list', args: { thread: 'omt_xxx' } })
```

### Scenario 2: Paginate through a long thread

```js
// First page
lark_api({ tool: 'im', op: 'threads-messages-list', args: { thread: 'omt_xxx' } })

// If has_more=true is returned, continue with page_token
lark_api({ tool: 'im', op: 'threads-messages-list', args: { thread: 'omt_xxx', page_token: '<PAGE_TOKEN>' } })
```

## Resource Rendering

Thread replies are rendered into human-readable text. Image messages appear as placeholders such as `[Image: img_xxx]`; resource binaries are **not** downloaded automatically.

Other resource types (files, audio, video) still need to be downloaded manually through `messages-resources-download`. See [lark-im-messages-resources-download](lark-im-messages-resources-download.md).

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|---------|---------|
| "Invalid thread ID format" | `thread_id` does not start with `om_` or `omt_` | Use a valid `om_xxx` or `omt_xxx` value |
| Empty thread result | Wrong thread_id or no replies in the thread | Confirm the thread_id came from `chat-messages-list` output |
| Permission denied | The user is not authorized or is not a conversation member | Make sure OAuth authorization is complete and the identity is a chat member |

## References

- [lark-im](../SKILL.md) - all message-related commands
- [lark-im-chat-messages-list](lark-im-chat-messages-list.md) - fetch conversation messages (source of `thread_id`)
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
