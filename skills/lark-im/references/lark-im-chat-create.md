# im +chat-create

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Create a group chat. Supports both user identity (`as: user`) and bot identity (`as: bot`). You can specify the group name, description, members (users/bots), owner, and chat type (private/public).

This maps to: `POST /open-apis/im/v1/chats`

- `as: bot` requires the `im:chat:create` scope.
- `as: user` requires the `im:chat:create_by_user` scope.

## Recommended call

Create a private group (default):

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/chats
- body:
  ```json
  { "name": "My Group" }
  ```
- params: `{ "user_id_type": "open_id" }`
- as: bot

Create a public group with members:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/chats
- body:
  ```json
  {
    "name": "Public Group",
    "chat_type": "public",
    "owner_id": "ou_xxx",
    "user_id_list": ["ou_aaa", "ou_bbb"],
    "bot_id_list": ["cli_aaa"]
  }
  ```
- params: `{ "user_id_type": "open_id" }`
- as: bot

## Parameters (body)

| Parameter | Required | Limits | Description |
|-----------|----------|--------|-------------|
| `name` | Required for public groups | Max 60 characters; at least 2 characters for public groups | Group name (`"(no subject)"` for private groups if omitted) |
| `description` | No | Max 100 characters | Group description |
| `user_id_list` | No | Up to 50, format `ou_xxx` | List of user open_ids to invite |
| `bot_id_list` | No | Up to 5, format `cli_xxx` | List of bot app IDs to invite |
| `owner_id` | No | Format `ou_xxx` | Owner open_id |
| `chat_type` | No | `private` (default) or `public` | Group type |

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `user_id_type` | No | User ID type: `open_id` (default) |

## AI Usage Guidance

### When using `as: bot`

Bot may fail to invite users who are mutually invisible to it during group creation (error 232043). Use the **two-step flow**:

1. Get the current user's `open_id`:

   Call MCP tool `lark_api`:
   - method: GET
   - path: /open-apis/contact/v3/users/me

2. Create the group — add the current user by default:

   Call MCP tool `lark_api`:
   - method: POST
   - path: /open-apis/im/v1/chats
   - body:
     ```json
     { "name": "<group name>", "user_id_list": ["<current user open_id>"] }
     ```
   - params: `{ "user_id_type": "open_id" }`
   - as: bot

3. Add other members via user identity:

   Call MCP tool `lark_api`:
   - method: POST
   - path: /open-apis/im/v1/chats/{chat_id}/members
   - body:
     ```json
     { "id_list": ["ou_aaa", "ou_bbb"] }
     ```
   - params: `{ "member_id_type": "open_id", "succeed_type": 1 }`
   - as: user

4. Check `invalid_id_list` in the response. If non-empty, report which members could not be added.

### When using `as: user`

User identity does not have the bot visibility limitation, so you can create the group and invite members in one step.

## Output Fields

| Field | Description |
|-------|-------------|
| `chat_id` | The new group's ID (`oc_xxx` format) |
| `name` | Group name |
| `chat_type` | Group type (`private` / `public`) |
| `owner_id` | Owner ID |
| `external` | Whether the group is external |

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Permission denied (99991672) | Missing `im:chat:create` scope | Enable the required permission for the app |
| `bot is invisible to user` (232043) | Bot and target users are mutually invisible | Use two-step flow above |

## References

- [lark-im](../SKILL.md) - all IM commands
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
