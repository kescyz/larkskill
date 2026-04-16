# mail +reply-all

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

All replies will be processed automatically:
- Automatically aggregate the original email sender, original To, and original Cc
- Automatically exclude the current user's address to avoid returning it to yourself
- Automatically maintain session headers (`In-Reply-To` / `References`)

> **Default Draft**: This operation saves as a draft by default and will not be sent immediately. Only send after explicit user confirmation.

## CRITICAL — Send workflow (must be followed)

**Step 1** — Get the original email metadata (to extract all recipients):
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}
- as: user
```

**Step 2** — Build the reply-all recipient list (original sender → To; original To/Cc → Cc; exclude current user address), then create draft:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts
- body:
  {
    "subject": "Re: <original subject>",
    "to": [{ "mail_address": "<original sender>" }],
    "cc": [{ "mail_address": "<original to[1]>" }, { "mail_address": "<original cc[0]>" }],
    "body": "<p>Completed, see the instructions below for details.</p>",
    "body_type": "html",
    "in_reply_to": "<original smtp_message_id>",
    "thread_id": "<thread_id>"
  }
- as: user
```

→ Returns `draft_id`

**Step 3** — Show the user a summary of the reply (target email, reply content, complete recipient list To/Cc) and request confirmation.

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
| `subject` | Yes | Reply subject (prefix `Re: ` if not already present) |
| `to` | Yes | Original sender (reply recipient) |
| `cc` | No | All original To/Cc recipients (excluding current user) |
| `body` | Yes | Reply text. HTML recommended |
| `body_type` | No | `html` (recommended) or `plain` |
| `from` | No | Sender email address |
| `bcc` | No | Additional BCC addresses |
| `in_reply_to` | No | `smtp_message_id` of the original email |
| `thread_id` | No | `thread_id` from the original message |

## Recipient aggregation rules

- Original sender enters `to` first
- Original `to` and `cc` entries enter `cc`
- Deduplicate addresses (case insensitive)
- Exclude current user's own address

## Follow up after sending

After the reply is sent successfully, check delivery status:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}/send_status
- as: user
```

## Related references

- [`+reply`](lark-mail-reply.md) — reply to sender only
- [`+forward`](lark-mail-forward.md) — forward mail
