# contact — search-user

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand authentication, global parameters, and safety rules.

Search employees by keywords (name/email/phone, etc.). Results are ranked by relevance.

Internally calls `GET /open-apis/search/v1/user`.

## MCP tool call

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/search/v1/user
- params:
  {
    "query": "Alice",
    "page_size": 20
  }
- as: user
```

With pagination:

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/search/v1/user
- params:
  {
    "query": "Alice",
    "page_size": 50,
    "page_token": "<PAGE_TOKEN>"
  }
- as: user
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | Yes | Search keyword (name, email, phone, etc.) |
| `page_size` | No | Page size (default 20, max 200) |
| `page_token` | No | Pagination token for next page |

## Common Usage (for AI)

- Parse response JSON directly to extract `open_id` for downstream calls.
- If result has `has_more=true`, continue with the returned `page_token`. Do not blindly increase `page_size`.
- Use returned `open_id` as input to [get-user](lark-contact-get-user.md) for full user details.

## References

- [lark-contact-get-user](lark-contact-get-user.md) — Get full user details by open_id
- [lark-shared](../../lark-shared/SKILL.md) — Authentication and global parameters
