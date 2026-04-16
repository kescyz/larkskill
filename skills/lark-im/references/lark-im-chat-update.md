# im +chat-update

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Update a group's name or description. Supports both **TAT (bot)** and **UAT (user)** identity.

This maps to: `PUT /open-apis/im/v1/chats/{chat_id}`

## Recommended call

Update the group name:

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/im/v1/chats/{chat_id}
- body:
  ```json
  { "name": "New Group Name" }
  ```

Update multiple fields at once:

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/im/v1/chats/{chat_id}
- body:
  ```json
  {
    "name": "Q2 Project Team",
    "description": "Owns Q2 goal tracking"
  }
  ```

## Parameters (path)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chat_id` | Yes | Group chat ID (`oc_xxx`) |

## Parameters (body)

| Parameter | Limits | Description |
|-----------|--------|-------------|
| `name` | Max 60 characters | Group name |
| `description` | Max 100 characters | Group description |

> At least one field must be specified to update.

## Usage Scenarios

### Scenario 1: Rename a group and update its description

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/im/v1/chats/oc_xxx
- body:
  ```json
  {
    "name": "Q2 Project Team",
    "description": "Owns Q2 goal tracking"
  }
  ```

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Permission denied (99991679) | Missing `im:chat:update` permission | Enable the permission in the Open Platform console |
| Non-owner/admin cannot update (232016/232002/232017) | Current identity is not the owner/admin | Switch identity with `as: bot` or `as: user` |
| Not in the group (232011) | The current user is not a member of the group | Use a member identity or join the group first |

## AI Usage Guidance

### Identity Selection

`+chat-update` supports both user and bot identity.

Infer the group owner from context whenever possible (for example, if a bot just created the group, the owner is the bot) and use the matching identity directly. If ownership is unclear, query the group first and confirm `owner_id`.

Identity choice should follow [Group Chat Identity Rules](lark-im-chat-identity.md).

## References

- [lark-im](../SKILL.md) - all IM commands
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
