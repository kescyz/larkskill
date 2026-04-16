---
name: lark-im
version: 2.0.0
description: "Lark Instant Messaging: Send and receive messages and manage group chats via LarkSkill MCP. Send and reply to messages, search chat records, manage group chat members, upload and download images and files, manage emoji reactions. Use when users need to send messages, view or search chat records, download files in chats, or view group members."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# im (v2)

**CRITICAL - Before starting, MUST read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which includes authentication and permission handling. LarkSkill MCP server must be connected.**

## Core Concepts

- **Message**: A single message in a chat, identified by `message_id` (om_xxx). Supports types: text, post, image, file, audio, video, sticker, interactive (card), share_chat, share_user, merge_forward, etc.
- **Chat**: A group chat or P2P conversation, identified by `chat_id` (oc_xxx).
- **Thread**: A reply thread under a message, identified by `thread_id` (om_xxx or omt_xxx).
- **Reaction**: An emoji reaction on a message.

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

- `as: user` means **user identity** and uses `user_access_token`. Calls run as the authorized end user, so permissions depend on both the app scopes and that user's own access to the target chat/message/resource.
- `as: bot` means **bot identity** and uses `tenant_access_token`. Calls run as the app bot, so behavior depends on the bot's membership, app visibility, availability range, and bot-specific scopes.
- If an IM API says it supports both `user` and `bot`, the token type changes who the operator is. The same API can succeed with one identity and fail with the other because owner/admin status, chat membership, tenant boundary, or app availability are checked against the current caller.

### Sender Name Resolution with Bot Identity

When using bot identity (`as: bot`) to fetch messages, sender names may not be resolved (shown as open_id instead of display name). This happens when the bot cannot access the user's contact info.

**Root cause**: The bot's app visibility settings do not include the message sender, so the contact API returns no name.

**Solution**: Check the app's visibility settings in the Lark Developer Console — ensure the app's visible range covers the users whose names need to be resolved. Alternatively, use `as: user` to fetch messages with user identity, which typically has broader contact access.

### Card Messages (Interactive)

Card messages (`interactive` type) may return raw event data. Handle accordingly.

## Shortcuts (recommended, use first)

Shortcuts are high-level operations via MCP `lark_api`. Read the corresponding reference doc before calling.

| Shortcut | Reference | Description |
|----------|-----------|-------------|
| `+chat-create` | [`references/lark-im-chat-create.md`](references/lark-im-chat-create.md) | Create a group chat; user/bot; creates private/public chats, invites users/bots, optionally sets bot manager |
| `+chat-messages-list` | [`references/lark-im-chat-messages-list.md`](references/lark-im-chat-messages-list.md) | List messages in a chat or P2P conversation; user/bot; supports time range/sort/pagination |
| `+chat-search` | [`references/lark-im-chat-search.md`](references/lark-im-chat-search.md) | Search visible group chats by keyword and/or member open_ids; user/bot; supports member/type filters, sorting, and pagination |
| `+chat-update` | [`references/lark-im-chat-update.md`](references/lark-im-chat-update.md) | Update group chat name or description; user/bot |
| `+messages-mget` | [`references/lark-im-messages-mget.md`](references/lark-im-messages-mget.md) | Batch get messages by IDs; user/bot; fetches up to 50 om_ message IDs, formats sender names |
| `+messages-reply` | [`references/lark-im-messages-reply.md`](references/lark-im-messages-reply.md) | Reply to a message; user/bot; supports text/markdown/post/media replies, reply-in-thread, idempotency key |
| `+messages-resources-download` | [`references/lark-im-messages-resources-download.md`](references/lark-im-messages-resources-download.md) | Download images/files from a message; user/bot |
| `+messages-search` | [`references/lark-im-messages-search.md`](references/lark-im-messages-search.md) | Search messages across chats; user-only; filters by chat/sender/attachment/time, supports auto-pagination |
| `+messages-send` | [`references/lark-im-messages-send.md`](references/lark-im-messages-send.md) | Send a message to a chat or direct message; user/bot; sends to chat-id or user-id with text/markdown/post/media |
| `+threads-messages-list` | [`references/lark-im-threads-messages-list.md`](references/lark-im-threads-messages-list.md) | List messages in a thread; user/bot; accepts om_/omt_ input, supports sort/pagination |

## Intent → MCP call index

| Intent | MCP call | Note |
|--------|----------|------|
| Send message to chat | `lark_api POST /open-apis/im/v1/messages` | params: `receive_id_type=chat_id`; body: `{receive_id, msg_type, content}` |
| Send DM to user | `lark_api POST /open-apis/im/v1/messages` | params: `receive_id_type=open_id`; body: `{receive_id, msg_type, content}` |
| Reply to message | `lark_api POST /open-apis/im/v1/messages/{message_id}/reply` | body: `{content, msg_type, reply_in_thread}` |
| List chat messages | `lark_api GET /open-apis/im/v1/messages` | params: `container_id_type=chat&container_id=oc_xxx` |
| List thread messages | `lark_api GET /open-apis/im/v1/messages` | params: `container_id_type=thread&container_id=omt_xxx` |
| Batch get messages | `lark_api GET /open-apis/im/v1/messages/mget` | params: `message_ids=om_aaa,om_bbb` |
| Search messages | `lark_api POST /open-apis/im/v1/messages/search` | body: `{query, chat_id, ...}` |
| Search chats | `lark_api POST /open-apis/im/v2/chats/search` | body: `{query, member_ids_list, ...}` |
| Create group | `lark_api POST /open-apis/im/v1/chats` | body: `{name, user_id_list, bot_id_list, ...}` |
| Update group | `lark_api PUT /open-apis/im/v1/chats/{chat_id}` | body: `{name, description}` |
| Add member to group | `lark_api POST /open-apis/im/v1/chats/{chat_id}/members` | body: `{id_list}` |
| Add reaction | `lark_api POST /open-apis/im/v1/messages/{message_id}/reactions` | body: `{reaction_type:{emoji_type}}` |
| List reactions | `lark_api GET /open-apis/im/v1/messages/{message_id}/reactions` | |
| Delete reaction | `lark_api DELETE /open-apis/im/v1/messages/{message_id}/reactions/{reaction_id}` | |
| Download resource | `lark_api GET /open-apis/im/v1/messages/{message_id}/resources/{file_key}` | params: `type=image\|file` |

## API Resources

### chats

  - `create` - Create a group. Identity: `bot` only (`tenant_access_token`).
  - `get` - Get group information. Identity: supports `user` and `bot`; the caller must be in the target chat to get full details, and must belong to the same tenant for internal chats.
  - `link` - Get group sharing link. Identity: supports `user` and `bot`; the caller must be in the target chat, must be an owner or admin when chat sharing is restricted to owners/admins, and must belong to the same tenant for internal chats.
  - `list` - Get the list of groups the user or bot belongs to. Identity: supports `user` and `bot`.
  - `update` - Update group information. Identity: supports `user` and `bot`.

### chat.members

  - `create` - Add a user or bot to a group chat. Identity: supports `user` and `bot`; the caller must be in the target chat; for `bot` calls, added users must be within the app's availability; for internal chats the operator must belong to the same tenant; if only owners/admins can add members, the caller must be an owner/admin, or a chat-creator bot with `im:chat:operate_as_owner`.
  - `delete` - Remove a user or bot from a group chat. Identity: supports `user` and `bot`; only group owner, admin, or creator bot can remove others; max 50 users or 5 bots per request.
  - `get` - Get group member list. Identity: supports `user` and `bot`; the caller must be in the target chat and must belong to the same tenant for internal chats.

### messages

  - `delete` - Recall a message. Identity: supports `user` and `bot`; for `bot` calls, the bot must be in the chat to revoke group messages; to revoke another user's group message, the bot must be the owner, an admin, or the creator; for user P2P recalls, the target user must be within the bot's availability.
  - `forward` - Forward a message. Identity: `bot` only (`tenant_access_token`).
  - `merge_forward` - Merge forward messages. Identity: `bot` only (`tenant_access_token`).
  - `read_users` - Query message read status. Identity: `bot` only (`tenant_access_token`); the bot must be in the chat, and can only query read status for messages it sent within the last 7 days.

### reactions

  - `batch_query` - Batch get message reactions. Identity: supports `user` and `bot`. [Must-read](references/lark-im-reactions.md)
  - `create` - Add a message reaction. Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message. [Must-read](references/lark-im-reactions.md)
  - `delete` - Delete a message reaction. Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message, and can only delete reactions added by itself. [Must-read](references/lark-im-reactions.md)
  - `list` - Get message reactions. Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message. [Must-read](references/lark-im-reactions.md)

### images

  - `create` - Upload an image. Identity: `bot` only (`tenant_access_token`).

### pins

  - `create` - Pin a message. Identity: supports `user` and `bot`.
  - `delete` - Remove a pinned message. Identity: supports `user` and `bot`.
  - `list` - Get pinned messages in the group. Identity: supports `user` and `bot`.

## Permission Table

| Method | Required Scope |
|--------|---------------|
| `chats.create` | `im:chat:create` |
| `chats.get` | `im:chat:read` |
| `chats.link` | `im:chat:read` |
| `chats.list` | `im:chat:read` |
| `chats.update` | `im:chat:update` |
| `chat.members.create` | `im:chat.members:write_only` |
| `chat.members.delete` | `im:chat.members:write_only` |
| `chat.members.get` | `im:chat.members:read` |
| `messages.delete` | `im:message:recall` |
| `messages.forward` | `im:message` |
| `messages.merge_forward` | `im:message` |
| `messages.read_users` | `im:message:readonly` |
| `reactions.batch_query` | `im:message.reactions:read` |
| `reactions.create` | `im:message.reactions:write_only` |
| `reactions.delete` | `im:message.reactions:write_only` |
| `reactions.list` | `im:message.reactions:read` |
| `images.create` | `im:resource` |
| `pins.create` | `im:message.pins:write_only` |
| `pins.delete` | `im:message.pins:write_only` |
| `pins.list` | `im:message.pins:read` |
