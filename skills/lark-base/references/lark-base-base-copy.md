# base-copy

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Copy an existing Base. Optionally copy structure only without records.

## Recommended call

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/copy
- body:
  ```json
  {
    "name": "Copied Base"
  }
  ```

With optional params:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/copy
- body:
  ```json
  {
    "name": "Copied Base",
    "folder_token": "fld_xxx",
    "time_zone": "Asia/Shanghai",
    "without_content": true
  }
  ```

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Source Base token (path param) |
| `name` | No | New Base name |
| `folder_token` | No | Target folder token |
| `time_zone` | No | Timezone, for example `Asia/Shanghai` |
| `without_content` | No | If `true`, copy structure only (no records) |

## API request details

```
POST /open-apis/base/v3/bases/{base_token}/copy
```

## Response highlights

- Returns `base`.
- In your reply, proactively return:
  - `base.url` when available
  - new Base token (commonly `base_token` or `app_token`)
  - if `url` missing, at least Base name and token

> [!IMPORTANT]
> If Base is copied with app identity (bot), keep bot identity by default and grant `full_access` (admin) to currently available user identity.
> Recommended flow:
> 1. Call `lark_api GET /open-apis/contact/v3/users/me` to get current user `open_id`
> 2. Use bot identity to call the Base member/permission endpoint with `full_access` for that `open_id`
>
> If no local user identity is available or `open_id` cannot be obtained, clearly state authorization was not completed.
>
> In result reply, always include authorization status:
> - success: user has admin permission
> - no local user identity: explain auth not completed
> - failed: Base copied but auth failed, include reason and next step
>
> If authorization is not completed, suggest retry later or continue with bot identity.
> Do not transfer owner unless user explicitly asks and confirms.

## Workflow

> [!CAUTION]
> This is a write operation. Confirm with the user before execution.

1. Confirm source Base token
2. Optional params should not trigger extra follow-up unless requested
3. Use `without_content: true` when structure-only copy is requested
4. After success, return Base name, token, and accessible link if present

## References

- [lark-base-workspace.md](lark-base-workspace.md) - base/workspace index
- [lark-base-base-create.md](lark-base-base-create.md) - create Base
