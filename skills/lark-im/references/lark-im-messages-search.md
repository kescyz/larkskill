# im +messages-search

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Search Feishu messages across conversations.

> **User identity only** (`as: user`). Bot identity is not supported.

This maps to: `POST /open-apis/im/v1/messages/search`

After searching for message IDs, batch-fetch full content via `GET /open-apis/im/v1/messages/mget`.

## Recommended call

Search by keyword:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/search
- body:
  ```json
  { "query": "project progress", "page_size": 20 }
  ```
- as: user

Restrict to a specific chat with sender filter:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/search
- body:
  ```json
  {
    "query": "weekly report",
    "chat_id_list": ["oc_xxx"],
    "sender_open_id_list": ["ou_xxx"],
    "page_size": 20
  }
  ```
- as: user

With time range:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/search
- body:
  ```json
  {
    "query": "meeting",
    "start_time": "1742140800",
    "end_time": "1742745599",
    "page_size": 20
  }
  ```
- as: user

Paginate with `page_token`:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/search
- body:
  ```json
  { "query": "test", "page_token": "<PAGE_TOKEN>", "page_size": 20 }
  ```
- as: user

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | No | Search keyword (may be empty when used with other filters) |
| `chat_id_list` | No | Restrict to chat IDs (`oc_xxx,oc_yyy`) |
| `sender_open_id_list` | No | Sender open_ids |
| `message_type` | No | Filter by message type |
| `chat_type` | No | Chat type: `group` / `p2p` |
| `sender_type` | No | Sender type: `user` / `bot` |
| `at_me` | No | Only return messages that mention me |
| `start_time` | No | Start time (Unix second timestamp with TZ) |
| `end_time` | No | End time (Unix second timestamp with TZ) |
| `page_size` | No | Page size (default 20, range 1-50) |
| `page_token` | No | Pagination token for next page |

## Core Constraints

### 1. Two-step workflow

The search API returns matching `message_id` values only. Fetch full message content separately:

1. Call `POST /open-apis/im/v1/messages/search` → get `message_id` list
2. Call `GET /open-apis/im/v1/messages/mget` with those IDs → get full content

### 2. Pagination behavior

- Default is single-page.
- When `has_more=true`, use returned `page_token` to continue.
- For report/summary tasks, paginate exhaustively.

### 3. Search results contain follow-up clues

Each result includes `chat_id` and potentially `thread_id`. Use them with other shortcuts:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params: `{ "container_id_type": "chat", "container_id": "<chat_id>" }`

## Work Summary / Report Generation

When the user asks to summarize work or generate a weekly report, paginate through all available results to get a complete picture.

**Strategy:**
1. Use targeted filters (`chat_id_list`, `sender_open_id_list`, `start_time`, `end_time`) to narrow scope.
2. Paginate until `has_more=false` or page limit reached.
3. Collect all pages of messages first, then analyze and summarize.

## AI Usage Guidance

### Resolving chat_id from a chat name

When the user refers to a chat by name, use [`+chat-search`](lark-im-chat-search.md) first:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v2/chats/search
- body: `{ "query": "<chat name keyword>" }`

**Do not use `GET /open-apis/im/v1/chats` — always use the `+chat-search` path.**

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|------------|----------|
| No results | Missing permission or no match | Confirm `search:message` is authorized and relax filters |
| Permission denied | Search scope not authorized | Authorize `search:message` |

## References

- [lark-im](../SKILL.md) - all message-related commands
- [lark-im-threads-messages-list](lark-im-threads-messages-list.md) - inspect thread replies
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
