# mail +triage

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

List mail summaries (date/from/subject/message_id). Use `query` for full-text search, `filter` for exact-match conditions.

## Recommended call

List inbox messages (default):
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages
- params: { "folder_id": "INBOX", "page_size": 20 }
- as: user
```

Filter by label (e.g. unread):
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages
- params: { "label_id": "UNREAD", "page_size": 20 }
- as: user
```

Full-text search:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/messages/search
- body:
  {
    "query": "quarterly report",
    "page_size": 20
  }
- as: user
```

## API request details

```
GET  /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/messages
POST /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/messages/search
```

## Parameters (list query)

| Parameter | Required | Description |
|------|------|------|
| `folder_id` | No | Folder to list: `INBOX`, `SENT`, `DRAFT`, `TRASH`, `SPAM`, or custom folder ID |
| `label_id` | No | Filter by label (mutually exclusive with `folder_id`) |
| `page_size` | No | Number of results per page (default 20) |
| `page_token` | No | Pagination token from previous response |

## Response highlights

- `items[]` — list of message summaries, each with `message_id`, `thread_id`, `subject`, `head_from`, `date`, `label_ids`, `folder_id`
- `has_more` — whether more results exist
- `page_token` — use for next page

## Typical scenario

### Browse inbox → Read a message

Step 1 — List inbox:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages
- params: { "folder_id": "INBOX", "page_size": 20 }
- as: user
```

Step 2 — Get `message_id` from the result.

Step 3 — Use [`+message`](lark-mail-message.md) to read full content.

## Related references

- [`+message`](lark-mail-message.md) — read a single email
- [`+thread`](lark-mail-thread.md) — read full conversation
