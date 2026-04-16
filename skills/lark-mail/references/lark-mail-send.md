# mail +send

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Send new emails, supporting:
- Plain text or HTML body
- CC/BCC
- Inline images (CID references)

## CRITICAL — Send workflow (must be followed)

By default, this operation saves a draft and does NOT send the email. When you need to send, you **must** follow these steps:

**Step 1** — Create a draft:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts
- body:
  {
    "subject": "Meeting notes",
    "to": [{ "mail_address": "alice@example.com" }],
    "body": "<p>See attached</p>",
    "body_type": "html"
  }
- as: user
```

→ Returns `draft_id`

**Step 2** — Show the user the recipients, subject, and body summary, and request confirmation to send.

**Step 3** — With the user's explicit consent, send the draft:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts/{draft_id}/send
- as: user
```

**It is forbidden to send without user's explicit consent.**

## API request details

```
POST /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/drafts
POST /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/drafts/{draft_id}/send
```

## Parameters (draft body)

| Parameter | Required | Description |
|------|------|------|
| `subject` | Yes | Email subject |
| `body` | Yes | Email body. HTML recommended for rich text |
| `body_type` | No | `html` (default) or `plain` |
| `to` | Yes | Recipient list: `[{ "mail_address": "...", "name": "..." }]` |
| `from` | No | Sender address (defaults to current user primary email) |
| `cc` | No | CC list, same format as `to` |
| `bcc` | No | BCC list, same format as `to` |

## After sending: confirm delivery status

After the email is sent successfully, check delivery:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}/send_status
- as: user
```

Status codes: 1=delivering, 2=delivery failed and retry, 3=bounced, 4=delivered, 5=pending approval, 6=approval rejected.

## Related references

- [`+draft-create`](lark-mail-draft-create.md) — create draft from scratch
- [`+reply`](lark-mail-reply.md) — reply to email
- [`+forward`](lark-mail-forward.md) — forward email
