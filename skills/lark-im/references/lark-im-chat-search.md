# im +chat-search

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Search the list of group chats visible to a user or bot. Supports keyword matching on chat names and member names, including pinyin and prefix fuzzy search.

This maps to: `POST /open-apis/im/v2/chats/search`

## Recommended call

Search chats by keyword:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v2/chats/search
- body:
  ```json
  { "query": "project", "page_size": 20 }
  ```

Search by keyword and filter by member open_ids:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v2/chats/search
- body:
  ```json
  {
    "query": "project",
    "member_ids_list": ["ou_xxx", "ou_yyy"],
    "page_size": 20
  }
  ```

Search by member open_ids only:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v2/chats/search
- body:
  ```json
  { "member_ids_list": ["ou_xxx", "ou_yyy"] }
  ```

Restrict by search types:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v2/chats/search
- body:
  ```json
  {
    "query": "project",
    "search_types": ["private", "public_joined"],
    "page_size": 10
  }
  ```

Paginate:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v2/chats/search
- body:
  ```json
  { "query": "project", "page_token": "xxx" }
  ```

## Parameters (body)

| Parameter | Required | Limits | Description |
|-----------|----------|--------|-------------|
| `query` | No (at least one of `query`/`member_ids_list` required) | Max 64 characters | Search keyword |
| `search_types` | No | Array: `private`, `external`, `public_joined`, `public_not_joined` | Restrict visible chat types returned |
| `member_ids_list` | No (at least one of `query`/`member_ids_list` required) | Up to 50, format `ou_xxx` | Filter by member open_ids |
| `is_manager` | No | boolean | Only show chats you created or manage |
| `disable_search_by_user` | No | boolean | Disable member-name-based matching |
| `sort_by` | No | `create_time_desc`, `update_time_desc`, `member_count_desc` | Sort field |
| `page_size` | No | 1-100, default 20 | Number of results per page |
| `page_token` | No | — | Pagination token from previous response |

## Output Fields

| Field | Description |
|-------|-------------|
| `chat_id` | Chat ID (`oc_xxx` format) |
| `name` | Chat name |
| `description` | Chat description |
| `owner_id` | Owner ID |
| `external` | Whether the chat is external |
| `chat_status` | Chat status (`normal` / `dissolved` / `dissolved_save`) |

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Empty results | No visible chats matched | Relax keyword or filters and try again |
| Permission denied (99991672) | Bot app missing `im:chat:read` TAT permission | Enable the permission |
| `Bot ability is not activated` (232025) | App does not have bot capability enabled | Enable bot capability in Open Platform console |

## AI Usage Guidance

1. **At least one filter required:** `query` and `member_ids_list` cannot both be empty.
2. **Search scope is limited:** only chats visible to the current user or bot can be found.
3. **NEVER fall back to chats list:** If `+chat-search` returns empty results, do NOT attempt `GET /open-apis/im/v1/chats` as a fallback — it's not a search API. Instead, ask the user to refine the keyword or check visibility.

## References

- [lark-im](../SKILL.md) - all IM commands
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
