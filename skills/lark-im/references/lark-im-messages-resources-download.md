# im +messages-resources-download

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Download image or file resources from a message. Resources are identified by the combination of `message_id` + `file_key`, both of which come directly from message content returned by `im +chat-messages-list`.

> **Note:** Read-only message commands return resource keys but do not download binaries automatically. Use this operation whenever you need to fetch the actual image/file bytes.

This maps to: `GET /open-apis/im/v1/messages/{message_id}/resources/{file_key}`

## Recommended call

Download an image:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages/{message_id}/resources/{file_key}
- params: `{ "type": "image" }`
- as: user

Download a file:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages/{message_id}/resources/{file_key}
- params: `{ "type": "file" }`
- as: user

## Parameters (path)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `message_id` | Yes | Message ID (`om_xxx` format) |
| `file_key` | Yes | Resource key (`img_xxx` or `file_xxx`) |

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `type` | Yes | Resource type: `image` or `file` |

## `file_key` Sources

| Message Type | Content field | `file_key` Format | `type` |
|-------------|---------------|-------------------|--------|
| Image | `image_key` in content | `img_xxx` | `image` |
| File | `file_key` in content | `file_xxx` | `file` |
| Audio | `file_key` in content | `file_xxx` | `file` |
| Video | `file_key` in content | `file_xxx` | `file` |

## Usage Scenario

### Scenario: Extract and download an image from a message

Step 1: Fetch messages and find one containing an image:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params: `{ "container_id_type": "chat", "container_id": "oc_xxx" }`

Step 2: Download the image using `message_id` and `image_key` from the response:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages/om_xxx/resources/img_v3_xxx
- params: `{ "type": "image" }`
- as: user

## Common Errors and Troubleshooting

| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Download failed | `file_key` does not match `message_id` | Make sure the `file_key` came from that message's content |
| Error code 234002 or 14005 | No permission — not a missing scope | No access to this chat or file was deleted — return error to user |
| Permission denied | `im:message:readonly` not authorized | Authorize the required scope |
| File too large | Over the 100 MB limit | Feishu API limitation — cannot be bypassed |

## References

- [lark-im](../SKILL.md) - all message-related commands
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
