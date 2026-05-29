# im +flag-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for authentication, global parameters, and security rules.

This skill maps to shortcut: `lark_api({ tool: 'im', op: 'flag-list' })`. Underlying API: `GET /open-apis/im/v1/flags`.

## Sorting Rules (Important)

The API returns data sorted by `update_time` in **ascending order**, meaning **oldest first, newest last**. When `has_more=true`, you cannot simply take the first page's items as the latest flags — you must paginate through all pages and take the last item on the last page as the newest.

Recommended: page through the full list, then read `.data.flag_items[-1]` from the merged result to get the latest item.

## Commands

```js
// Fetch flags
lark_api({ tool: 'im', op: 'flag-list', args: { as: 'user' } })

// Disable auto-enrichment of message content (enabled by default)
lark_api({ tool: 'im', op: 'flag-list', args: { as: 'user', enrich_feed_thread: false } })
```

## Parameters

| Parameter | Default | Description |
|------|------|------|
| `enrich_feed_thread` | true | Auto-enrich feed-layer thread entries with message content (calls `im.messages.mget`) |
| `as: 'user'` | Required | Currently only supports user identity |

## Response Structure

The response has `data` as the main body, with fields described below:

| Field | Type | Description |
|------|------|------|
| `flag_items` | array | List of currently existing (not canceled) flags, sorted by `update_time` ascending |
| `delete_flag_items` | array | List of previously canceled flags, sorted by `update_time` ascending |
| `messages` | array | Message content inlined by the server for `(default, message)` type flags |
| `has_more` | boolean | Whether there's a next page |
| `page_token` | string | Pagination token for the next page |

Note: `(thread, feed)` / `(msg_thread, feed)` entries are automatically enriched via `mget` by the shortcut, and written to the corresponding entry's `message` field.

## Limitations

- **delete_flag_items are not enriched**: Message content is only fetched for active flags (`flag_items`), not canceled flags (`delete_flag_items`). If you need message content for a canceled flag, query the message separately using `lark_api({ tool: 'im', op: 'messages-mget', args: { message_ids: '<item_id>' } })`.

## Response Example (Sanitized)

```json
{
  "data": {
    "delete_flag_items": [
      {
        "create_time": "xxx",
        "flag_type": "xxx",
        "item_id": "xxx",
        "item_type": "xxx",
        "update_time": "xxx"
      }
    ],
    "flag_items": [
      {
        "create_time": "xxx",
        "flag_type": "xxx",
        "item_id": "xxx",
        "item_type": "xxx",
        "update_time": "xxx"
      }
    ],
    "has_more": false,
    "messages": [],
    "page_token": "xxx"
  }
}
```

## Permissions

- Base scope: `im:feed.flag:read`
- Additional scopes only when `enrich_feed_thread: true` needs to fetch missing message content: `im:message.group_msg:get_as_user`, `im:message.p2p_msg:get_as_user`
