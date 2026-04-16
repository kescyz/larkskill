# im +threads-messages-list

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Fetch the reply message list inside a thread. When `im +chat-messages-list` returns messages that include a `thread_id` field, use this to inspect all replies in that thread.

This maps to: `GET /open-apis/im/v1/messages` with `container_id_type=thread`

## Recommended call

Get thread replies (ascending by time):

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params:
  ```json
  {
    "container_id_type": "thread",
    "container_id": "omt_xxx",
    "page_size": 50,
    "sort_type": "ByCreateTimeAsc"
  }
  ```

Reverse chronological order (latest first):

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params:
  ```json
  {
    "container_id_type": "thread",
    "container_id": "omt_xxx",
    "sort_type": "ByCreateTimeDesc",
    "page_size": 10
  }
  ```

Paginate:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params:
  ```json
  {
    "container_id_type": "thread",
    "container_id": "omt_xxx",
    "page_token": "<PAGE_TOKEN>",
    "page_size": 50
  }
  ```

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `container_id_type` | Yes | Must be `thread` |
| `container_id` | Yes | Thread ID (`om_xxx` or `omt_xxx` format) |
| `sort_type` | No | `ByCreateTimeAsc` (default) or `ByCreateTimeDesc` |
| `page_size` | No | Number of items per page (default 50, range 1-500) |
| `page_token` | No | Pagination token for the next page |

## Core Constraints

### 1. Source of `thread_id`

`thread_id` (`omt_xxx` or `om_xxx`) comes from the `thread_id` field in results returned by `im +chat-messages-list` or `im +messages-search`. Do not guess a thread ID. Fetch messages first and use the returned value.

### 2. No time filtering support

Thread messages do not support `start_time` / `end_time` filtering. Use pagination and sort order to control scope.

### 3. Recommended expansion strategy

| Scenario | Recommended Parameters |
|----------|------------------------|
| Quickly inspect recent replies | `sort_type: ByCreateTimeDesc`, `page_size: 10` |
| Read the full thread in chronological order | `sort_type: ByCreateTimeAsc`, `page_size: 50`, then paginate |
| Just confirm whether replies exist | `sort_type: ByCreateTimeDesc`, `page_size: 1` |

## Usage Scenarios

### Scenario 1: Expand a thread discovered in group messages

Step 1: Fetch group messages and find one that contains `thread_id`:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params: `{ "container_id_type": "chat", "container_id": "oc_xxx" }`

Step 2: Fetch thread replies using the `thread_id`:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params: `{ "container_id_type": "thread", "container_id": "omt_xxx", "page_size": 50 }`

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Empty thread result | Wrong thread_id or no replies | Confirm the thread_id came from `im +chat-messages-list` output |
| Permission denied | User not authorized or not a chat member | Ensure OAuth authorization is complete and identity is a chat member |

## References

- [lark-im](../SKILL.md) - all message-related commands
- [lark-im-chat-messages-list](lark-im-chat-messages-list.md) - fetch conversation messages (source of `thread_id`)
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
