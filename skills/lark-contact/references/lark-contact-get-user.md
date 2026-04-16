# contact — get-user

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand authentication, global parameters, and safety rules.

Get user info. Supports two modes:

1. **Self (no user_id)**: get current user's own info — calls `GET /open-apis/authen/v1/user_info`
2. **Specific user (with user_id)**: get specified user info — calls `GET /open-apis/contact/v3/users/{user_id}` (default `user_id_type=open_id`)

## Mode 1: Get current user

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/authen/v1/user_info
- as: user
```

## Mode 2: Get specific user by open_id

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/contact/v3/users/{user_id}
- params: { "user_id_type": "open_id" }
- as: user
```

Replace `{user_id}` in the path with the actual `open_id` value.

## Mode 2: Get specific user by user_id type

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/contact/v3/users/{user_id}
- params: { "user_id_type": "user_id" }
- as: user
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `user_id` (path) | No (Mode 2 only) | User ID value to look up |
| `user_id_type` (query) | No | `open_id` (default) / `union_id` / `user_id` |

## Common Error (41050)

If response indicates insufficient permission (error code `41050`), it is usually caused by **org visibility scope** limitation:

- Ask admin to adjust org visibility scope for current user
- Or switch to bot identity (`as: "bot"`) when calling Contact API — bot uses `tenant_access_token` which may have broader org visibility

## References

- [lark-contact-search-user](lark-contact-search-user.md) — Search open_id first, then get details
- [lark-shared](../../lark-shared/SKILL.md) — Authentication and global parameters
