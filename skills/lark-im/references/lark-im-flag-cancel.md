# im +flag-cancel

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for authentication, global parameters, and security rules.

This skill maps to shortcut: `lark_api({ tool: 'im', op: 'flag-cancel' })`. Underlying API: `POST /open-apis/im/v1/flags/cancel`.

## Double-Cancel Behavior (Important)

A message can have flags on both layers simultaneously:
- Message layer: `(default, message)`
- Feed layer: `(thread, feed)` or `(msg_thread, feed)` depending on chat type

**When no `flag_type` is specified, the shortcut performs double-cancel**: removes both message layer and feed layer flags. The server handles cancel requests for non-existent flags idempotently, so this is safe.

**Feed layer item_type is determined by chat_mode**:
- Topic-style chat (`chat_mode=topic`) → `item_type=thread`
- Regular chat (`chat_mode=group`) → `item_type=msg_thread`

## Commands

```js
// Double-cancel both layers (recommended default)
lark_api({ tool: 'im', op: 'flag-cancel', args: { as: 'user', message_id: 'om_xxx' } })

// Only cancel message layer
lark_api({ tool: 'im', op: 'flag-cancel', args: { as: 'user', message_id: 'om_xxx', flag_type: 'message' } })

// Only cancel feed layer (need to specify item_type)
lark_api({ tool: 'im', op: 'flag-cancel', args: { as: 'user', message_id: 'om_xxx', item_type: 'thread', flag_type: 'feed' } })
```

## Parameters

| Parameter | Required | Description |
|------|------|------|
| `message_id` | Required | Message ID |
| `flag_type` | No | `message` or `feed`; **when omitted, double-cancels both layers** |
| `item_type` | No | `default\|thread\|msg_thread`; required when `flag_type: 'feed'` |
| `as: 'user'` | Required | Currently only supports user identity |

## Idempotency

The server doesn't return an error for cancel requests when the flag doesn't exist, so repeated `flag-cancel` calls are idempotent.

## Permissions

- Required scopes: `im:feed.flag:write`, `im:message.group_msg:get_as_user`, `im:message.p2p_msg:get_as_user`, `im:chat:read`
- The message/chat read scopes are used by the default double-cancel path to auto-detect the feed-layer item type.

## Note

- **Do not call flag-list for verification**: If the cancel API returns success, the flag is removed. Calling flag-list to verify is expensive (requires full pagination) and unnecessary.

## Finding Message ID Efficiently

If you have message content but not the message ID:

1. **Use `messages-search`** to find the message by content, then extract `message_id` from the result
2. **Do NOT use `flag-list`** to find the message — it requires full pagination and is very inefficient

```js
// Search by message content, then read message_id from .data.items[0].message_id
lark_api({ tool: 'im', op: 'messages-search', args: { as: 'user', query: 'message content here' } })
```
