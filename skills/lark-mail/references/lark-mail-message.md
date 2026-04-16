# mail +message

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Read the complete content of the specified email, including headers, body (plain text + optional HTML) and a unified list of `attachments` (covering ordinary attachments and inline images).

## Recommended call

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}
- as: user
```

To read only plain text body (smaller payload, suitable for AI processing), add `fields` param:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}
- params: { "fields": "body_plain_text,subject,head_from,to,date" }
- as: user
```

## API request details

```
GET /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/messages/{message_id}
```

## Parameters (query)

| Parameter | Required | Description |
|------|------|------|
| `user_mailbox_id` | Yes (path) | Mailbox ID. Use `me` for current user |
| `message_id` | Yes (path) | Message ID |

## Response highlights

The response `data` field contains:

| Field | Description |
|------|------|
| `message_id` | Message ID |
| `thread_id` | Thread ID |
| `subject` | Email subject |
| `head_from` | Sender object: `{mail_address, name}` |
| `to` | Recipient list: `[{mail_address, name}]` |
| `cc` | Cc list: `[{mail_address, name}]` |
| `bcc` | Bcc list: `[{mail_address, name}]` |
| `date` | Sending time |
| `internal_date` | Create/receive/send time (milliseconds) |
| `message_state` | Message status: `1` = received, `2` = sent, `3` = draft |
| `folder_id` | Folder ID. Values: `INBOX`, `SENT`, `SPAM`, `ARCHIVED`, `STRANGER`, or custom folder ID |
| `label_ids` | List of label IDs |
| `body_plain_text` | **LLM reading recommended** — decoded and cleaned plain text body |
| `body_preview` | First 100 characters of the plain text body |
| `body_html` | Original HTML body |
| `attachments` | Unified list of normal attachments and inline images |
| `security_level` | Risk metadata when present (see below) |

### security_level fields

| Field | Description |
|------|------|
| `is_risk` | `true` means the message is marked as risky |
| `risk_banner_level` | Risk level: `WARNING`, `DANGER`, `INFO` |
| `risk_banner_reason` | Risk reason: `NO_REASON`, `IMPERSONATE_DOMAIN`, `IMPERSONATE_KP_NAME`, `UNAUTH_EXTERNAL`, `MALICIOUS_URL`, `MALICIOUS_ATTACHMENT`, `PHISHING`, `IMPERSONATE_PARTNER`, `EXTERNAL_ENCRYPTION_ATTACHMENT` |
| `is_header_from_external` | `true` means the sender is from an external domain |
| `spam_banner_type` | Spam reason: `USER_REPORT`, `USER_BLOCK`, `ANTI_SPAM`, `USER_RULE`, `BLOCK_DOMIN`, `BLOCK_ADDRESS` |

## Typical scenario

### Read email → Summary → Reply

Step 1 — Read email (plain text only, smaller payload):
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}
- as: user
```

Step 2 — Analyze `body_plain_text` and draft a reply.

Step 3 — Send reply via [`+reply`](lark-mail-reply.md).

### Obtain attachment download URLs on demand

Step 1 — Get attachment `id` from response `attachments[]`.

Step 2 — Get download URL:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/messages/{message_id}/attachments/{attachment_id}/download_url
- as: user
```

## Related references

- [`+thread`](lark-mail-thread.md) — read all messages in the session
- [`+reply`](lark-mail-reply.md) — reply to email
- [`+forward`](lark-mail-forward.md) — forward mail
