# im +messages-reply

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Reply to a specific message. Supports both user identity (`as: user`) and bot identity (`as: bot`). Also supports thread replies.

This maps to: `POST /open-apis/im/v1/messages/{message_id}/reply`

## Safety Constraints

Replies sent by this tool are visible to other people. Before calling it, you **must** confirm with the user:

1. Which message to reply to
2. The reply content
3. Which identity to use (user or bot)

**Do not** send a reply without explicit user approval.

## Choose The Right Content Type

| Need | `msg_type` | `content` format |
|------|------------|------------------|
| Reply with plain text | `text` | `{"text":"Received"}` |
| Reply with formatted post | `post` | `{"zh_cn":{"title":"...","content":[[...]]}}` |
| Reply with image | `image` | `{"image_key":"img_xxx"}` |
| Reply with file | `file` | `{"file_key":"file_xxx"}` |

## Recommended call

Reply with plain text:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/{message_id}/reply
- body:
  ```json
  {
    "content": "{\"text\":\"Received\"}",
    "msg_type": "text"
  }
  ```
- as: bot

Reply inside a thread:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/{message_id}/reply
- body:
  ```json
  {
    "content": "{\"text\":\"Let me look into this\"}",
    "msg_type": "text",
    "reply_in_thread": true
  }
  ```
- as: bot

Reply with a post (markdown-style):

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/{message_id}/reply
- body:
  ```json
  {
    "content": "{\"zh_cn\":{\"title\":\"Follow-up\",\"content\":[[{\"tag\":\"text\",\"text\":\"Detail here\"}]]}}",
    "msg_type": "post"
  }
  ```
- as: bot

With idempotency key:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/{message_id}/reply
- body:
  ```json
  {
    "content": "{\"text\":\"Received\"}",
    "msg_type": "text",
    "uuid": "my-unique-id-456"
  }
  ```
- as: bot

## Parameters (path)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `message_id` | Yes | ID of the message being replied to (`om_xxx`) |

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `content` | Yes | JSON string of reply content. Must match `msg_type` format |
| `msg_type` | Yes | Message type: `text`, `post`, `image`, `file`, `audio`, `media`, `interactive` |
| `reply_in_thread` | No | If `true`, reply appears inside the target message's thread instead of the main chat stream |
| `uuid` | No | Idempotency key; same key sends only one reply within 1 hour |

## Usage Scenarios

### Scenario 1: Reply in the main chat stream

Reply appears in the main chat and references the target message.

### Scenario 2: Reply inside a thread

Set `reply_in_thread: true`. Reply appears in the thread and does not show in the main chat stream.

## @Mention Format (text / post)

- Recommended: `<at user_id="ou_xxx">name</at>`
- @all: `<at user_id="all"></at>`

## Notes

- `content` must be a JSON-encoded **string**, not a nested object.
- `as: user` requires `im:message.send_as_user` and `im:message` scopes
- `as: bot` requires `im:message:send_as_bot` scope

## References

- [lark-im](../SKILL.md) - all IM commands
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
