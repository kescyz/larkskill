# im +chat-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand authentication, global parameters, and safety rules.

List groups the current user (or bot, with `as: 'bot'`) is a member of. Useful for enumerating "my chats" without a search keyword, or for bulk operations against the caller's chats. Supports pagination, sort order, and (user identity only) muted-chat filtering.

This skill maps to the shortcut: `lark_api({ tool: 'im', op: 'chat-list' })` (internally calls `GET /open-apis/im/v1/chats`).

## Commands

```js
// List the user's chats (default sort: ByCreateTimeAsc)
lark_api({ tool: 'im', op: 'chat-list' })

// Sort by recent activity (most recently active first)
lark_api({ tool: 'im', op: 'chat-list', args: { sort_type: 'ByActiveTimeDesc' } })

// Drop muted chats (user identity only)
lark_api({ tool: 'im', op: 'chat-list', args: { exclude_muted: true } })
```

## Parameters

| Parameter | Required | Limits | Description |
|------|------|------|------|
| `user_id_type` | No | `open_id` (default), `union_id`, `user_id` | ID type used for `owner_id` in the response |
| `sort_type` | No | `ByCreateTimeAsc` (default), `ByActiveTimeDesc` | Result ordering |
| `exclude_muted` | No | User identity only | Drop chats the current user has muted (do-not-disturb). Under `as: 'bot'`, the flag is silently inactive; see "Filtering muted chats" below |

> **Note:** Supports both `as: 'user'` (default) and `as: 'bot'`. When using bot identity, the app must have bot capability enabled.

## Output Fields

| Field | Description |
|------|------|
| `chat_id` | Chat ID (`oc_xxx` format) |
| `name` | Chat name |
| `description` | Chat description |
| `owner_id` | Owner ID (type controlled by `user_id_type`) |
| `external` | Whether the chat is external |
| `chat_status` | Chat status (`normal` / `dissolved` / `dissolved_save`) |

## Filtering muted chats

`exclude_muted` (user identity only) drops chats the current user has set to do-not-disturb. After the list call, the CLI batches the page's chat_ids through `POST /open-apis/im/v1/chat_user_setting/batch_get_mute_status` and filters client-side. Under `as: 'bot'`, the mute API is UAT-only and the filter is silently skipped.

When the flag is set, the JSON envelope gains a `filter` sub-object (absent otherwise, so existing consumers are unaffected); `fetched_count == returned_count + filtered_count` always holds:

```json
{
  "chats": [...],
  "filter": {
    "applied": "exclude_muted",
    "fetched_count": 20,
    "returned_count": 17,
    "filtered_count": 3,
    "hint": "Filtered out 3 muted chat(s) on this page (17 remaining); use page_token to fetch more."
  }
}
```

## Usage Scenarios

### Scenario 1: List my recent chats

```js
lark_api({ tool: 'im', op: 'chat-list', args: { sort_type: 'ByActiveTimeDesc' } })
```

### Scenario 2: List my non-muted chats sorted by activity

```js
lark_api({ tool: 'im', op: 'chat-list', args: { sort_type: 'ByActiveTimeDesc', exclude_muted: true } })
```

### Scenario 3: Iterate all my chats programmatically

```js
// Read the response's has_more / page_token, then pass page_token back in to fetch the next page
lark_api({ tool: 'im', op: 'chat-list', args: { page_token: '<page_token from previous response>' } })
```

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|---------|---------|
| `page_size must be an integer between 1 and 100` | page_size is out of range or not an integer | Use an integer between 1 and 100 |
| Permission denied (99991672) | The bot app does not have `im:chat:read` TAT permission enabled | Enable the permission for the app in the Open Platform console |
| Permission denied (99991679) with `as: 'user'` | UAT is not authorized for `im:chat:read` | Run `lark_auth_login({ scope: 'im:chat:read' })` |
| `Bot ability is not activated` (232025) | The app does not have bot capability enabled | Enable bot capability in the Open Platform console |
| `exclude_muted` returns all chats unfiltered and `hint` says "no effect under bot identity" | Running under `as: 'bot'` (mute API is UAT-only) | Switch to `as: 'user'` for mute filtering |
