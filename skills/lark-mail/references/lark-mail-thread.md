# mail +thread

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Query a full mail conversation/thread by thread ID. Returns all messages in chronological order, including replies and drafts, with body content and attachments metadata, including inline images.

## Recommended call

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/threads/{thread_id}
- as: user
```

To list messages within a thread (paginated):
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages
- params: { "thread_id": "<thread_id>", "page_size": 50 }
- as: user
```

## API request details

```
GET /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/threads/{thread_id}
GET /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/messages?thread_id={thread_id}
```

## Parameters (query)

| Parameter | Required | Description |
|------|------|------|
| `user_mailbox_id` | Yes (path) | Mailbox ID. Use `me` for current user |
| `thread_id` | Yes (path) | Thread ID |

## Response highlights

- Returns thread metadata and the list of messages in the conversation
- Messages are ordered chronologically (ascending by time)
- Each message item uses the same structure as `+message`

## Typical scenario

### Read thread → Reply to latest message

Step 1 — Get all messages in the conversation:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages
- params: { "thread_id": "<thread_id>", "page_size": 50 }
- as: user
```

Step 2 — Take the last `message_id` in the list.

Step 3 — Use [`+reply`](lark-mail-reply.md) to reply to that message.

## Related references

- [`+message`](lark-mail-message.md) — read a single email
- [`+triage`](lark-mail-triage.md) — list mail summaries to get thread_id
- [`+reply`](lark-mail-reply.md) — reply to email
