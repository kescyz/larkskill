# im +messages-mget

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Fetch message details in batch. Given a list of message IDs, returns full content for multiple messages in one call.

This maps to: `GET /open-apis/im/v1/messages/mget`

Supports both `as: user` and `as: bot`.

## Recommended call

Fetch a single message:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages/mget
- params: `{ "message_ids": "om_xxx" }`

Fetch multiple messages in batch (comma-separated):

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages/mget
- params: `{ "message_ids": "om_aaa,om_bbb,om_ccc" }`

## Parameters (query)

| Parameter | Required | Limits | Description |
|-----------|----------|--------|-------------|
| `message_ids` | Yes | At least one, max 50, `om_xxx` format, comma-separated | Message ID list |

## Output Fields

| Field | Description |
|-------|-------------|
| `items` | Message array |

Each message contains:

| Field | Description |
|-------|-------------|
| `message_id` | Message ID |
| `msg_type` | Message type (`text`, `image`, `file`, etc.) |
| `create_time` | Creation time |
| `sender` | Sender information |
| `body.content` | Message content (JSON string) |

## Usage Scenarios

### Scenario 1: Fetch the full content of a specific message

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages/mget
- params: `{ "message_ids": "om_xxx" }`

### Scenario 2: Use together with the message list command

First get message IDs via `+chat-messages-list`, then fetch full content via `+messages-mget`.

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Permission denied | Message read permission missing | Ensure app has `im:message:readonly` and `contact:user.base:readonly` |
| Empty result | Message IDs do not exist or not accessible | Verify the IDs and access permissions |

## AI Usage Guidance

1. **Images are rendered as keys:** image messages appear as `image_key`. Use `+messages-resources-download` when you need the binary.
2. **Batching is more efficient:** fetching multiple IDs in one request is better than calling the API repeatedly.

## References

- [lark-im](../SKILL.md) - all IM commands
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
