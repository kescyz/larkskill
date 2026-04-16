# mail +draft-create

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Create a completely new email draft from scratch. Suitable for scenarios where the recipient, subject and body are known.

Do not use this for reply or forward scenarios. Replies and forwards should use their corresponding dedicated shortcuts (these also create drafts by default but don't send them).

If you need to modify an existing draft, do not use this — use `+draft-edit` instead.

## Security constraints

This operation creates a draft — it **doesn't** send the email. Therefore:

- **When the user requests to "draft" an email, directly create the draft** without pre-displaying content and asking for confirmation.
- **Omit `to`** if recipients are not specified — the draft will be created without recipients, the user can add them later.
- **Confirmation is only required if the user request is truly ambiguous**.
- **Sending** a draft is a separate operation and requires explicit confirmation from the user.

## Recommended call

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts
- body:
  {
    "subject": "weekly report",
    "to": [{ "mail_address": "alice@example.com" }],
    "body": "<p>Progress this week:</p><ul><li>Complete Module A</li></ul>",
    "body_type": "html"
  }
- as: user
```

Draft without recipients (user adds later):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts
- body:
  {
    "subject": "weekly report",
    "body": "<p>Draft content</p>",
    "body_type": "html"
  }
- as: user
```

## API request details

```
POST /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/drafts
```

## Parameters (body)

| Parameter | Required | Description |
|------|------|------|
| `subject` | Yes | Draft subject |
| `body` | Yes | The body of the email. HTML is recommended for rich text layout |
| `body_type` | No | `html` (recommended) or `plain` |
| `to` | No | Recipient objects `[{ "mail_address": "...", "name": "..." }]`. When omitted, draft has no recipients |
| `from` | No | Sender email address. When omitted, primary email of the currently logged in user is used |
| `cc` | No | CC list, same format as `to` |
| `bcc` | No | BCC list, same format as `to` |

## Response highlights

Returns `draft_id` on success.

## Typical scenario

### Compose new message → Create draft → Preview → Send

Step 1 — Create a draft:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts
- body:
  {
    "subject": "Q1 Report",
    "to": [{ "mail_address": "alice@example.com" }],
    "body": "Please check the attached report.",
    "body_type": "html"
  }
- as: user
```

Step 2 — Preview draft:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/drafts/{draft_id}
- as: user
```

Step 3 — Send draft (only after explicit user confirmation):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts/{draft_id}/send
- as: user
```

## Related references

- [`+draft-edit`](lark-mail-draft-edit.md) — edit an existing draft
- [`+reply`](lark-mail-reply.md) / [`+reply-all`](lark-mail-reply-all.md) / [`+forward`](lark-mail-forward.md) — create reply/forward draft
