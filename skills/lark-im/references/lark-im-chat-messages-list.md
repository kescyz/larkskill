# im +chat-messages-list

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Fetch the message list for a conversation. Supports both group chats and direct messages.

This maps to: `GET /open-apis/im/v1/messages` (with `container_id_type=chat` or resolved p2p `chat_id`).

## Recommended call

Get group chat messages:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params:
  ```json
  {
    "container_id_type": "chat",
    "container_id": "oc_xxx",
    "page_size": 50,
    "sort_type": "ByCreateTimeDesc"
  }
  ```

Get messages in a time range:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params:
  ```json
  {
    "container_id_type": "chat",
    "container_id": "oc_xxx",
    "start_time": "1741536000",
    "end_time": "1741622400",
    "page_size": 50
  }
  ```

Paginate:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params:
  ```json
  {
    "container_id_type": "chat",
    "container_id": "oc_xxx",
    "page_token": "xxx",
    "page_size": 50
  }
  ```

For direct messages: first resolve the p2p `chat_id` by calling `POST /open-apis/im/v1/chats` or searching, then use `container_id_type=chat` with the resolved `chat_id`.

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `container_id_type` | Yes | `chat` for group/p2p chat |
| `container_id` | Yes | The `chat_id` (`oc_xxx`) |
| `start_time` | No | Start time (Unix second timestamp) |
| `end_time` | No | End time (Unix second timestamp) |
| `sort_type` | No | `ByCreateTimeDesc` (default) or `ByCreateTimeAsc` |
| `page_size` | No | Page size (default 50, max 50) |
| `page_token` | No | Pagination token |

## Resource Rendering

Images are referenced by `image_key` in message content. Files, audio, and video are referenced by `file_key`. Resource binaries are **not** downloaded automatically.

Use [lark-im-messages-resources-download](lark-im-messages-resources-download.md) when you need to download an image or file.

## Thread Expansion (`thread_id`)

A message may contain a `thread_id` (`omt_xxx`) field, which means the message has replies in a thread. Use [`im +threads-messages-list`](lark-im-threads-messages-list.md) to inspect replies.

## Output Fields

| Field | Description |
|-------|-------------|
| `items` | Message array |
| `has_more` | Whether additional pages are available |
| `page_token` | Pagination token for the next page |

Each message contains:

| Field | Description |
|-------|-------------|
| `message_id` | Message ID |
| `msg_type` | Message type: `text`, `image`, `file`, `interactive`, `post`, `audio`, `video`, `system`, etc. |
| `create_time` | Creation time |
| `sender` | Sender information |
| `body.content` | Message content (JSON string) |
| `deleted` | Whether the message has been recalled |
| `updated` | Whether the message has been edited |
| `mentions` | Array of @mentions (when present) |
| `thread_id` | Thread ID (when replies exist) |

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Permission denied | Message read permissions missing | Ensure app has `im:message:readonly` and `im:chat:read` |

## AI Usage Guidance

1. **Resolving chat_id from a chat name:** Use [`+chat-search`](lark-im-chat-search.md) first to find `chat_id`.
2. **For direct messages:** Resolve the p2p `chat_id` first, then use `container_id_type=chat`.
3. **For full content:** The `body.content` field is a JSON string — parse it to access nested fields.

## References

- [lark-im](../SKILL.md) - all IM commands
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
