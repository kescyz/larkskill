# im +messages-send

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Send a message to a group chat or a direct message conversation. Supports both user identity (`as: user`) and bot identity (`as: bot`).

This maps to: `POST /open-apis/im/v1/messages`

## Safety Constraints

Messages sent by this tool are visible to other people. Before calling it, you **must** confirm with the user:

1. The recipient (which person or which group)
2. The message content
3. The sending identity (user or bot)

**Do not** send messages without explicit user approval.

When using `as: bot`, the message is sent in the app's name, so make sure the app has already been added to the target chat.

When using `as: user`, the message is sent as the authorized end user and requires the `im:message.send_as_user` and `im:message` scopes.

## Choose The Right Content Type

| Need | `msg_type` | `content` format |
|------|------------|------------------|
| Send plain text | `text` | `{"text":"Hello"}` |
| Send Markdown-style post | `post` | `{"zh_cn":{"title":"T","content":[[{"tag":"md","text":"..."}]]}}` |
| Send image | `image` | `{"image_key":"img_xxx"}` |
| Send file | `file` | `{"file_key":"file_xxx"}` |
| Send interactive card | `interactive` | Card JSON per Feishu card docs |

## Recommended call

Send plain text to a group chat:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages
- params: `{ "receive_id_type": "chat_id" }`
- body:
  ```json
  {
    "receive_id": "oc_xxx",
    "msg_type": "text",
    "content": "{\"text\":\"Hello\"}"
  }
  ```
- as: bot

Send plain text DM to a user:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages
- params: `{ "receive_id_type": "open_id" }`
- body:
  ```json
  {
    "receive_id": "ou_xxx",
    "msg_type": "text",
    "content": "{\"text\":\"Hello\"}"
  }
  ```
- as: bot

Send a post (markdown-style) message:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages
- params: `{ "receive_id_type": "chat_id" }`
- body:
  ```json
  {
    "receive_id": "oc_xxx",
    "msg_type": "post",
    "content": "{\"zh_cn\":{\"title\":\"Release Notes\",\"content\":[[{\"tag\":\"text\",\"text\":\"Body here\"}]]}}"
  }
  ```
- as: bot

With idempotency key:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages
- params: `{ "receive_id_type": "chat_id" }`
- body:
  ```json
  {
    "receive_id": "oc_xxx",
    "msg_type": "text",
    "content": "{\"text\":\"Hello\"}",
    "uuid": "my-unique-id-123"
  }
  ```
- as: bot

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `receive_id_type` | Yes | Recipient type: `chat_id`, `open_id`, `user_id`, `union_id`, or `email` |

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `receive_id` | Yes | Recipient ID matching `receive_id_type` |
| `msg_type` | Yes | Message type: `text`, `post`, `image`, `file`, `audio`, `media`, `share_chat`, `share_user`, `interactive` |
| `content` | Yes | JSON string of message content. Must match `msg_type` format |
| `uuid` | No | Idempotency key; same key sends only one message within 1 hour |

## `content` Format Reference

| `msg_type` | Example `content` (as JSON string) |
|------------|--------------------------------------|
| `text` | `"{\"text\":\"Hello <at user_id=\\\"ou_xxx\\\">name</at>\"}"` |
| `post` | `"{\"zh_cn\":{\"title\":\"Title\",\"content\":[[{\"tag\":\"text\",\"text\":\"Body\"}]]}}"` |
| `image` | `"{\"image_key\":\"img_xxx\"}"` |
| `file` | `"{\"file_key\":\"file_xxx\"}"` |
| `audio` | `"{\"file_key\":\"file_xxx\"}"` |
| `media` | `"{\"file_key\":\"file_xxx\",\"image_key\":\"img_xxx\"}"` (video; `image_key` is cover — **required**) |
| `share_chat` | `"{\"chat_id\":\"oc_xxx\"}"` |
| `share_user` | `"{\"user_id\":\"ou_xxx\"}"` |
| `interactive` | Card JSON per Feishu interactive card documentation |

> **Note:** `content` must be a JSON-encoded **string**, not a nested object. Double-serialize if needed.

## @Mention Format (text / post)

- Recommended: `<at user_id="ou_xxx">name</at>`
- @all: `<at user_id="all"></at>`

## Return Value

```json
{
  "message_id": "om_xxx",
  "chat_id": "oc_xxx",
  "create_time": "1234567890"
}
```

## Common Mistakes

- Passing `content` as a nested JSON object instead of a serialized string.
- Using `receive_id_type=chat_id` but passing an `open_id`, or vice versa.
- Sending as bot when the bot is not in the target group.

## Notes

- `receive_id_type=chat_id` + `receive_id=oc_xxx` for group chats
- `receive_id_type=open_id` + `receive_id=ou_xxx` for direct messages
- `as: user` requires `im:message.send_as_user` and `im:message` scopes
- `as: bot` requires `im:message:send_as_bot` scope
- For images/files, upload them first with `lark_api POST /open-apis/im/v1/images` (bot only) to get the key, then reference it in `content`

## References

- [lark-im](../SKILL.md) - all IM commands
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
