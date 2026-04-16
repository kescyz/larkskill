# mail +forward

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Forward a specified email with automatic handling:
- Subject prefix `Fwd: ` (not repeated if the message already has a standard forward prefix)
- Automatically include the standard "Forwarded message" block (From/Date/Subject/To + original text)
- Supports plain text and HTML forwarding

> **Default draft**: This operation saves as draft by default and will not be sent immediately. Only send after explicit confirmation by the user.

## CRITICAL — Send workflow (must be followed)

**Step 1** — Get the original email content:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}
- as: user
```

**Step 2** — Create a forward draft (build forwarded content with original email block):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts
- body:
  {
    "subject": "Fwd: <original subject>",
    "to": [{ "mail_address": "alice@example.com" }],
    "body": "<p>FYI, please see the original email below.</p><blockquote>...original content...</blockquote>",
    "body_type": "html"
  }
- as: user
```

→ Returns `draft_id`

**Step 3** — Show the forwarding summary (forwarded email, recipients, additional notes) to the user and request confirmation.

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
| `subject` | Yes | Forward subject (prefix with `Fwd: ` if not already present) |
| `to` | Yes | Recipient email address objects |
| `body` | No | Description text prepended when forwarding, followed by original email block |
| `body_type` | No | `html` (recommended) or `plain` |
| `cc` | No | CC email addresses |
| `bcc` | No | BCC email addresses |

## Forward the entire conversation

Forward the **last message in the conversation** because the mail client nests the complete reply chain in the latest message.

Step 1 — Get messages in the thread:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/threads/{thread_id}
- as: user
```

Step 2 — Get the last `message_id` from the thread, then forward that message.

## Follow up after sending

After forwarding is sent successfully, check delivery status:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}/send_status
- as: user
```

Status codes: 1=delivering, 2=failed and retry, 3=bounced, 4=delivered, 5=pending approval, 6=approval rejected.

## Related references

- [`+send`](lark-mail-send.md) — send new mail
- [`+reply`](lark-mail-reply.md) — reply to email
