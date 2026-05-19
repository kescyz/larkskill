---
name: lark-im
version: 2.0.0
description: "Lark Messenger: send and receive messages and manage group chats via LarkSkill MCP. Use when the user needs to send messages, view or search chat history, download files from chat, view group members, search groups, create group chats or topic chats, or manage bookmarked data."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# im (v1)

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling.**

## Core Concepts

- **Message**: A single message in a chat, identified by `message_id` (om_xxx). Supports types: text, post, image, file, audio, video, sticker, interactive (card), share_chat, share_user, merge_forward, etc.
- **Chat**: A group chat or P2P conversation, identified by `chat_id` (oc_xxx).
- **Thread**: A reply thread under a message, identified by `thread_id` (om_xxx or omt_xxx).
- **Reaction**: An emoji reaction on a message.
- **Flag**: A bookmark on a message or thread.

## Resource Relationships

```
Chat (oc_xxx)
├── Message (om_xxx)
│   ├── Thread (reply thread)
│   ├── Reaction (emoji)
│   └── Resource (image / file / video / audio)
└── Member (user / bot)
```

## Important Notes

### Identity and Token Mapping

- `as: "user"` means **user identity** and uses `user_access_token`. Calls run as the authorized end user, so permissions depend on both the app scopes and that user's own access to the target chat/message/resource.
- `as: "bot"` means **bot identity** and uses `tenant_access_token`. Calls run as the app bot, so behavior depends on the bot's membership, app visibility, availability range, and bot-specific scopes.
- If an IM API says it supports both `user` and `bot`, the token type changes who the operator is. The same API can succeed with one identity and fail with the other because owner/admin status, chat membership, tenant boundary, or app availability are checked against the current caller.

### Sender Name Resolution with Bot Identity

When using bot identity (`as: "bot"`) to fetch messages (e.g. `chat-messages-list`, `threads-messages-list`, `messages-mget`), sender names may not be resolved (shown as open_id instead of display name). This happens when the bot cannot access the user's contact info.

**Root cause**: The bot's app visibility settings do not include the message sender, so the contact API returns no name.

**Solution**: Check the app's visibility settings in the Lark Developer Console — ensure the app's visible range covers the users whose names need to be resolved. Alternatively, use `as: "user"` to fetch messages with user identity, which typically has broader contact access.

### Card Messages (Interactive)

Card messages (`interactive` type) are not yet supported for compact conversion in event subscriptions. The raw event data will be returned instead, with a hint printed to stderr.

### Flag Types

Flags support two layers:

- **Message-layer flag**: `(ItemTypeDefault, FlagTypeMessage)` — regular message bookmark
- **Feed-layer flag**: `(ItemTypeThread/ItemTypeMsgThread, FlagTypeFeed)` — thread as feed-layer bookmark

Item types for feed-layer flags:
- **ItemTypeThread** (4) = thread in a topic-style chat
- **ItemTypeMsgThread** (11) = thread in a regular chat

## Shortcuts (use these first)

Shortcuts are high-level wrappers for common operations via the LarkSkill MCP tool. When a shortcut exists for an operation, use it first.

| Shortcut | Description |
|----------|------|
| [`chat-create`](references/lark-im-chat-create.md) | `lark_api({ tool: 'im', op: 'chat-create', args: { ... } })` — Create a group chat or topic chat; user/bot; chat_mode group\|topic; private/public; invites users/bots; optionally sets bot manager |
| [`chat-list`](references/lark-im-chat-list.md) | `lark_api({ tool: 'im', op: 'chat-list', args: { ... } })` — List groups the current user/bot is a member of; user/bot; supports sorting, pagination, and exclude_muted (user identity only) |
| [`chat-messages-list`](references/lark-im-chat-messages-list.md) | `lark_api({ tool: 'im', op: 'chat-messages-list', args: { ... } })` — List messages in a chat or P2P conversation; user/bot; accepts chat_id or user_id, resolves P2P chat_id, supports time range/sort/pagination |
| [`chat-search`](references/lark-im-chat-search.md) | `lark_api({ tool: 'im', op: 'chat-search', args: { query: '...', ... } })` — Search visible group chats by query keyword and/or member_ids; user/bot; e.g. look up chat_id by group name; supports type filters, sorting, pagination |
| [`chat-update`](references/lark-im-chat-update.md) | `lark_api({ tool: 'im', op: 'chat-update', args: { chat_id: '...', ... } })` — Update group chat name or description; user/bot |
| [`messages-mget`](references/lark-im-messages-mget.md) | `lark_api({ tool: 'im', op: 'messages-mget', args: { message_ids: [...] } })` — Batch get messages by IDs; user/bot; fetches up to 50 om_ message IDs, formats sender names, expands thread replies |
| [`messages-reply`](references/lark-im-messages-reply.md) | `lark_api({ tool: 'im', op: 'messages-reply', args: { message_id: '...', ... } })` — Reply to a message (supports thread replies); user/bot; supports text/markdown/post/media replies, reply-in-thread, idempotency key |
| [`messages-resources-download`](references/lark-im-messages-resources-download.md) | `lark_api({ tool: 'im', op: 'messages-resources-download', args: { message_id: '...', file_key: '...' } })` — Download images/files from a message; user/bot; supports automatic chunked download for large files (8MB chunks), auto-detects file extension from Content-Type |
| [`messages-search`](references/lark-im-messages-search.md) | `lark_api({ tool: 'im', op: 'messages-search', args: { query: '...', ... } })` — Search messages across chats (supports keyword, sender, time range filters) with user identity; user-only; supports auto-pagination via page_all / page_limit |
| [`messages-send`](references/lark-im-messages-send.md) | `lark_api({ tool: 'im', op: 'messages-send', args: { ... } })` — Send a message to a chat or direct message; user/bot; sends to chat_id or user_id with text/markdown/post/media, supports idempotency key |
| [`threads-messages-list`](references/lark-im-threads-messages-list.md) | `lark_api({ tool: 'im', op: 'threads-messages-list', args: { thread_id: '...', ... } })` — List messages in a thread; user/bot; accepts om_/omt_ input, resolves message IDs to thread_id, supports sort/pagination |
| [`flag-create`](references/lark-im-flag-create.md) | `lark_api({ tool: 'im', op: 'flag-create', args: { message_id: '...', ... } })` — Create a bookmark on a message or thread; user-only; defaults to message-layer flag; feed-layer flag requires explicit item_type + flag_type |
| [`flag-cancel`](references/lark-im-flag-cancel.md) | `lark_api({ tool: 'im', op: 'flag-cancel', args: { message_id: '...', ... } })` — Cancel (remove) a bookmark. When no flag_type is given, checks if the message is a thread root message; if so, cancels both message and feed layers |
| [`flag-list`](references/lark-im-flag-list.md) | `lark_api({ tool: 'im', op: 'flag-list', args: { ... } })` — List bookmarks; user-only; auto-enriches feed-type thread entries with message content; supports page_all auto-pagination |

## API Resources

```javascript
lark_api_search({ query: 'im.<resource>.<method>' })  // Check parameter structure before calling an API
lark_api({ tool: 'im', op: '<resource>.<method>', args: { ... } })  // Call API
```

> **Important**: When using native APIs, MUST first use `lark_api_search` to check the parameter structure. Do not guess field formats.

### chats

  - `create` — Create a group chat. Identity: `bot` only (`tenant_access_token`).
  - `get` — Get group info. Identity: supports `user` and `bot`; the caller must be in the target chat to get full details, and must belong to the same tenant for internal chats.
  - `link` — Get group share link. Identity: supports `user` and `bot`; the caller must be in the target chat, must be an owner or admin when chat sharing is restricted to owners/admins, and must belong to the same tenant for internal chats.
  - `update` — Update group info. Identity: supports `user` and `bot`.

### chat.members

  - `bots` — Get list of bots in a group. Identity: supports `user` and `bot`; the caller must be in the target chat and must belong to the same tenant for internal chats.
  - `create` — Add users or bots to a group chat. Identity: supports `user` and `bot`; the caller must be in the target chat; for `bot` calls, added users must be within the app's availability; for internal chats the operator must belong to the same tenant; if only owners/admins can add members, the caller must be an owner/admin, or a chat-creator bot with `im:chat:operate_as_owner`.
  - `delete` — Remove users or bots from a group chat. Identity: supports `user` and `bot`; only group owner, admin, or creator bot can remove others; max 50 users or 5 bots per request.
  - `get` — Get group member list. Identity: supports `user` and `bot`; the caller must be in the target chat and must belong to the same tenant for internal chats.

### messages

  - `delete` — Recall a message. Identity: supports `user` and `bot`; for `bot` calls, the bot must be in the chat to revoke group messages; to revoke another user's group message, the bot must be the owner, an admin, or the creator; for user P2P recalls, the target user must be within the bot's availability.
  - `forward` — Forward a message. Identity: supports `user` and `bot`.
  - `merge_forward` — Merge-forward messages. Identity: `bot` only (`tenant_access_token`).
  - `read_users` — Query message read status. Identity: `bot` only (`tenant_access_token`); the bot must be in the chat, and can only query read status for messages it sent within the last 7 days.

### reactions

  - `batch_query` — Batch query message emoji reactions. Identity: supports `user` and `bot`. [Must-read](references/lark-im-reactions.md)
  - `create` — Add an emoji reaction to a message. Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message. [Must-read](references/lark-im-reactions.md)
  - `delete` — Remove an emoji reaction from a message. Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message, and can only delete reactions added by itself. [Must-read](references/lark-im-reactions.md)
  - `list` — Get message emoji reactions. Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message. [Must-read](references/lark-im-reactions.md)

### threads

  - `forward` — Forward a thread. Identity: supports `user` and `bot`.

### images

  - `create` — Upload an image. Identity: `bot` only (`tenant_access_token`).

### pins

  - `create` — Pin a message. Identity: supports `user` and `bot`.
  - `delete` — Remove a pinned message. Identity: supports `user` and `bot`.
  - `list` — Get pinned messages in a group. Identity: supports `user` and `bot`.

## Permissions

| Method | Required scope |
|------|-----------|
| `chats.create` | `im:chat:create` |
| `chats.get` | `im:chat:read` |
| `chats.link` | `im:chat:read` |
| `chats.update` | `im:chat:update` |
| `chat.members.bots` | `im:chat.members:read` |
| `chat.members.create` | `im:chat.members:write_only` |
| `chat.members.delete` | `im:chat.members:write_only` |
| `chat.members.get` | `im:chat.members:read` |
| `messages.delete` | `im:message:recall` |
| `messages.forward` | `im:message` |
| `messages.merge_forward` | `im:message` |
| `messages.read_users` | `im:message:readonly` |
| `threads.forward` | `im:message` |
| `reactions.batch_query` | `im:message.reactions:read` |
| `reactions.create` | `im:message.reactions:write_only` |
| `reactions.delete` | `im:message.reactions:write_only` |
| `reactions.list` | `im:message.reactions:read` |
| `images.create` | `im:resource` |
| `pins.create` | `im:message.pins:write_only` |
| `pins.delete` | `im:message.pins:write_only` |
| `pins.list` | `im:message.pins:read` |
