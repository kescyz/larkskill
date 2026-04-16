# mail +reply

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Reply to the specified email and process it automatically:
- Subject prefix `Re: ` (not superimposed if already contains common reply prefixes)
- The default recipient is the sender of the original email
- RFC 2822 session header (`In-Reply-To` / `References`) maintains email sessions

> **Default draft mode**: This operation saves as draft by default and will not be sent immediately. **Prefer using `+reply` over `+draft-create` to create reply drafts** as `+reply` automatically handles subject, recipients and conversation headers.

## CRITICAL — Send workflow (must be followed)

**Step 1** — Get the original email metadata:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}
- as: user
```

**Step 2** — Create a reply draft (using `In-Reply-To` header to maintain conversation thread):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts
- body:
  {
    "subject": "Re: <original subject>",
    "to": [{ "mail_address": "<original sender address>" }],
    "body": "<p>Received, follow up later.</p>",
    "body_type": "html",
    "in_reply_to": "<original smtp_message_id>",
    "thread_id": "<thread_id from original message>"
  }
- as: user
```

→ Returns `draft_id`

**Step 3** — Show the user a summary of the reply (target email, reply content, recipients) and request confirmation to send.

**Step 4** — With the user's explicit consent, send the draft:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts/{draft_id}/send
- as: user
```

**It is forbidden to send without the user's explicit consent.**

## API request details

```
GET  /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/messages/{message_id}
POST /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/drafts
POST /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/drafts/{draft_id}/send
```

## Parameters (draft body)

| Parameter | Required | Description |
|------|------|------|
| `subject` | Yes | Reply subject (prefix with `Re: ` if not already present) |
| `to` | Yes | Original sender address (reply recipient) |
| `body` | Yes | Reply text. HTML recommended |
| `body_type` | No | `html` (recommended) or `plain` |
| `from` | No | Sender email address |
| `cc` | No | Additional CC addresses |
| `bcc` | No | BCC addresses |
| `in_reply_to` | No | `smtp_message_id` of the original email (maintains threading) |
| `thread_id` | No | `thread_id` from the original message (ensures reply lands in same conversation) |

## Follow up after sending

After the reply is sent successfully, check delivery status:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}/send_status
- as: user
```

Status codes: 1=delivering, 2=failed and retry, 3=bounced, 4=delivered, 5=pending approval, 6=approval rejected.

## Notes

- Mail ID can be obtained from the messages list API
- `bcc` only takes effect in the sending link, usually not seen on the recipient side

## Related references

- [`+reply-all`](lark-mail-reply-all.md) — reply all
- [`+forward`](lark-mail-forward.md) — forward mail
