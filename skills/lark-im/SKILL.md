---
name: lark-im
version: 1.0.0
description: "Lark Instant Messaging: send/receive messages and manage group chats. Send and reply to messages, search chat history, manage group members, upload/download images and files (supports large-file chunked download), manage emoji reactions, send in-app/SMS/phone urgent notifications. Use this skill when the user needs to send messages, view or search chat history, download files from chats, view group members, search groups, create group chats or topic chats, or manage flagged data. Use this skill via LarkSkill MCP."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search", "lark_auth_login", "lark_auth_poll", "lark_auth_status", "lark_whoami", "lark_profile_switch", "lark_enable_domain"]
---

# im (v1)

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which contains authentication and permission handling**

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

- `as: 'user'` (passed in `args`) means **user identity** and uses `user_access_token`. Calls run as the authorized end user, so permissions depend on both the app scopes and that user's own access to the target chat/message/resource.
- `as: 'bot'` (passed in `args`) means **bot identity** and uses `tenant_access_token`. Calls run as the app bot, so behavior depends on the bot's membership, app visibility, availability range, and bot-specific scopes.
- If an IM API says it supports both `user` and `bot`, the token type changes who the operator is. The same API can succeed with one identity and fail with the other because owner/admin status, chat membership, tenant boundary, or app availability are checked against the current caller.

### Sender Name Resolution with Bot Identity

When using bot identity to fetch messages (e.g. `lark_api({ tool: 'im', op: 'chat-messages-list' })`, `lark_api({ tool: 'im', op: 'threads-messages-list' })`, `lark_api({ tool: 'im', op: 'messages-mget' })`), sender names may not be resolved (shown as open_id instead of display name). This happens when the bot cannot access the user's contact info.

**Root cause**: The bot's app visibility settings do not include the message sender, so the contact API returns no name.

**Solution**: Check the app's visibility settings in the Lark Developer Console — ensure the app's visible range covers the users whose names need to be resolved. Alternatively, pass `as: 'user'` in `args` to fetch messages with user identity, which typically has broader contact access.

### Default message enrichment (reactions / update_time)

The four message-pulling shortcuts (`messages-mget`, `chat-messages-list`, `messages-search`, `threads-messages-list`) automatically attach a `reactions` block and (for edited messages) `update_time` to each returned message — no separate `lark_api({ tool: 'im', op: 'reactions.batch_query' })` call is needed. Pass `no_reactions: true` in `args` to opt out. For the full contract (output shape, the `im:message.reactions:read` scope requirement, and the "missing field ≠ fetch failure" data rules), read [`references/lark-im-message-enrichment.md`](references/lark-im-message-enrichment.md).

### Card Messages (Interactive)

Card messages (`interactive` type) are not yet supported for compact conversion in event subscriptions. The raw event data will be returned instead, with a hint printed to stderr.

### Flag Types

Flags support two layers:

- **Message-layer flag**: `(ItemTypeDefault, FlagTypeMessage)` — regular message bookmark
- **Feed-layer flag**: `(ItemTypeThread/ItemTypeMsgThread, FlagTypeFeed)` — thread as feed-layer bookmark

Item types for feed-layer flags:
- **ItemTypeThread** (4) = thread in a topic-style chat
- **ItemTypeMsgThread** (11) = thread in a regular chat

## Shortcuts (recommended — use these first)

Shortcuts are high-level wrappers for common operations. Use `lark_api({ tool: 'im', op: '<shortcut>', args: {...} })`. When a Shortcut exists for an operation, use it first.

| Shortcut | Description |
|----------|------|
| [`chat-create`](references/lark-im-chat-create.md) | Create a group chat or topic chat; user/bot; chat_mode group|topic; private/public; invites users/bots; optionally sets bot manager |
| [`chat-list`](references/lark-im-chat-list.md) | List chats the current user/bot is a member of; defaults to groups; pass types=p2p,group to include p2p single chats (user-only); user/bot; supports sorting, pagination, exclude_muted (user-only) |
| [`chat-messages-list`](references/lark-im-chat-messages-list.md) | List messages in a chat or P2P conversation; user/bot; accepts chat_id or user_id, resolves P2P chat_id, supports time range/sort/pagination |
| [`chat-search`](references/lark-im-chat-search.md) | Search visible group chats by query keyword and/or member_ids; user/bot; e.g. look up chat_id by group name; supports type filters, sorting, pagination, and exclude_muted (user identity only) |
| [`chat-update`](references/lark-im-chat-update.md) | Update group chat name or description; user/bot; updates a chat's name or description |
| [`messages-mget`](references/lark-im-messages-mget.md) | Batch get messages by IDs; user/bot; fetches up to 50 om_ message IDs, formats sender names, expands thread replies |
| [`messages-reply`](references/lark-im-messages-reply.md) | Reply to a message (supports thread replies); user/bot; supports text/markdown/post/media replies, reply-in-thread, idempotency key |
| [`messages-resources-download`](references/lark-im-messages-resources-download.md) | Download images/files from a message; user/bot; supports automatic chunked download for large files (8MB chunks), auto-detects file extension from Content-Type |
| [`messages-search`](references/lark-im-messages-search.md) | Search messages across chats (supports keyword, sender, time range filters) with user identity; user-only; filters by chat/sender/attachment/time, supports auto-pagination via page_all / page_limit, enriches results via batched mget and chats batch_query |
| [`messages-send`](references/lark-im-messages-send.md) | Send a message to a chat or direct message; user/bot; sends to chat_id or user_id with text/markdown/post/media, supports idempotency key |
| [`threads-messages-list`](references/lark-im-threads-messages-list.md) | List messages in a thread; user/bot; accepts om_/omt_ input, resolves message IDs to thread_id, supports sort/pagination |
| [`flag-create`](references/lark-im-flag-create.md) | Create a bookmark on a message or thread; user-only; defaults to message-layer flag; feed-layer flag requires explicit item_type + flag_type |
| [`flag-cancel`](references/lark-im-flag-cancel.md) | Cancel (remove) a bookmark. When no flag_type is given, checks if the message is a thread root message; if so, cancels both message and feed layers |
| [`flag-list`](references/lark-im-flag-list.md) | List bookmarks; user-only; auto-enriches feed-type thread entries with message content; supports page_all auto-pagination |

## API Resources

```
lark_api_search({ query: 'im <resource>.<method>' })   # MUST check parameter schema before calling an API
lark_api({ tool: 'im', op: '<resource>.<method>', args: {...} })  # Call an API
```

> **Important**: When using native APIs, you MUST first run `lark_api_search` to view the parameter structure. Do NOT guess field formats.

### chats

  - `chats.create` — Create a group chat. Identity: `bot` only (`tenant_access_token`).
  - `chats.get` — Get group chat info. Identity: supports `user` and `bot`; the caller must be in the target chat to get full details, and must belong to the same tenant for internal chats.
  - `chats.link` — Get a group chat share link. Identity: supports `user` and `bot`; the caller must be in the target chat, must be an owner or admin when chat sharing is restricted to owners/admins, and must belong to the same tenant for internal chats.
  - `chats.update` — Update group chat info. Identity: supports `user` and `bot`.

### chat.members

  - `chat.members.bots` — Get the bot list in a group chat. Identity: supports `user` and `bot`; the caller must be in the target chat and must belong to the same tenant for internal chats.
  - `chat.members.create` — Add users or bots to a group chat. Identity: supports `user` and `bot`; the caller must be in the target chat; for `bot` calls, added users must be within the app's availability; for internal chats the operator must belong to the same tenant; if only owners/admins can add members, the caller must be an owner/admin, or a chat-creator bot with `im:chat:operate_as_owner`.
  - `chat.members.delete` — Remove users or bots from a group chat. Identity: supports `user` and `bot`; only group owner, admin, or creator bot can remove others; max 50 users or 5 bots per request.
  - `chat.members.get` — Get the group member list. Identity: supports `user` and `bot`; the caller must be in the target chat and must belong to the same tenant for internal chats.

### messages

  - `messages.delete` — Recall a message. Identity: supports `user` and `bot`; for `bot` calls, the bot must be in the chat to revoke group messages; to revoke another user's group message, the bot must be the owner, an admin, or the creator; for user P2P recalls, the target user must be within the bot's availability.
  - `messages.forward` — Forward a message. Identity: supports `user` and `bot`.
  - `messages.merge_forward` — Merge-forward messages. Identity: `bot` only (`tenant_access_token`).
  - `messages.read_users` — Query message read status. Identity: `bot` only (`tenant_access_token`); the bot must be in the chat, and can only query read status for messages it sent within the last 7 days.
  - `messages.urgent_app` — Send an in-app urgent notification. Identity: `bot` only (`tenant_access_token`); the bot must be the message sender and must be in the conversation that contains the message.
  - `messages.urgent_phone` — Send a phone urgent notification. Identity: `bot` only (`tenant_access_token`); the bot must be the message sender and must be in the conversation that contains the message.
  - `messages.urgent_sms` — Send an SMS urgent notification. Identity: `bot` only (`tenant_access_token`); the bot must be the message sender and must be in the conversation that contains the message.

### reactions

  - `reactions.batch_query` — Batch get message emoji reactions. Identity: supports `user` and `bot`.[Must-read](references/lark-im-reactions.md)
  - `reactions.create` — Add an emoji reaction to a message. Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message.[Must-read](references/lark-im-reactions.md)
  - `reactions.delete` — Delete an emoji reaction from a message. Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message, and can only delete reactions added by itself.[Must-read](references/lark-im-reactions.md)
  - `reactions.list` — Get emoji reactions on a message. Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message.[Must-read](references/lark-im-reactions.md)

### threads

  - `threads.forward` — Forward a topic thread. Identity: supports `user` and `bot`.

### images

  - `images.create` — Upload an image. Identity: `bot` only (`tenant_access_token`).

### pins

  - `pins.create` — Pin a message. Identity: supports `user` and `bot`.
  - `pins.delete` — Unpin a message. Identity: supports `user` and `bot`.
  - `pins.list` — Get pinned messages in a group chat. Identity: supports `user` and `bot`.

## Permissions Table

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
| `messages.urgent_app` | `im:message.urgent` |
| `messages.urgent_phone` | `im:message.urgent:phone` |
| `messages.urgent_sms` | `im:message.urgent:sms` |
| `reactions.batch_query` | `im:message.reactions:read` |
| `reactions.create` | `im:message.reactions:write_only` |
| `reactions.delete` | `im:message.reactions:write_only` |
| `reactions.list` | `im:message.reactions:read` |
| `threads.forward` | `im:message` |
| `images.create` | `im:resource` |
| `pins.create` | `im:message.pins:write_only` |
| `pins.delete` | `im:message.pins:write_only` |
| `pins.list` | `im:message.pins:read` |
