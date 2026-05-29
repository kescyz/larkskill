# im +flag-create

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for authentication, global parameters, and security rules.

This skill maps to shortcut: `lark_api({ tool: 'im', op: 'flag-create' })`. Underlying API: `POST /open-apis/im/v1/flags`.

## Default Behavior

- **Message-layer flag** (default): `item_type=default, flag_type=message`
- **Feed-layer flag**: Use `flag_type: 'feed'` — automatically detects chat type to determine `item_type`:
  - Topic-style chat (`chat_mode=topic`) → `item_type=thread`
  - Regular chat (`chat_mode=group`) → `item_type=msg_thread`

## Commands

```js
// Flag a message (default: message-layer)
lark_api({ tool: 'im', op: 'flag-create', args: { as: 'user', message_id: 'om_xxx' } })

// Create feed-layer flag (auto-detects chat type)
lark_api({ tool: 'im', op: 'flag-create', args: { as: 'user', message_id: 'om_xxx', flag_type: 'feed' } })

// Explicit item_type override (rarely needed)
lark_api({ tool: 'im', op: 'flag-create', args: { as: 'user', message_id: 'om_xxx', item_type: 'thread', flag_type: 'feed' } })
```

## Parameters

| Parameter | Required | Description |
|------|------|------|
| `message_id` | Required | Message ID |
| `flag_type` | No | `message` (default) or `feed` |
| `item_type` | No | Override auto-detection: `default\|thread\|msg_thread` (rarely needed) |
| `as: 'user'` | Required | Currently only supports user identity |

## Valid Combinations

The server only accepts these `(item_type, flag_type)` pairs:

- `(default, message)` — regular message flag
- `(thread, feed)` — feed flag in topic-style chat
- `(msg_thread, feed)` — feed flag in regular chat

## Permissions

- Required scopes: `im:feed.flag:write`, `im:message.group_msg:get_as_user`, `im:message.p2p_msg:get_as_user`, `im:chat:read`
- The message/chat read scopes are used when `flag_type: 'feed'` is used without explicit `item_type` so the CLI can auto-detect chat type.
- If missing, CLI will prompt with `lark_auth_login({ scope: '...' })`

## Note

- **Do not call flag-list for verification**: If the create API returns success, the flag is created. Calling flag-list to verify is expensive (requires full pagination) and unnecessary.

## Finding Message ID Efficiently

If you have message content but not the message ID:

1. **Use `messages-search`** to find the message by content, then extract `message_id` from the result
2. **Do NOT use `flag-list`** to find the message — it requires full pagination and is very inefficient

```js
// Search by message content, then read message_id from .data.items[0].message_id
lark_api({ tool: 'im', op: 'messages-search', args: { as: 'user', query: 'message content here' } })
```
