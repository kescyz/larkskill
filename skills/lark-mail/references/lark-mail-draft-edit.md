# mail +draft-edit

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Edit an existing draft email. The operation reads the current draft, applies changes, and writes back the updated draft.

Simple metadata editing (subject, recipients) uses direct body fields in a PUT call. Body editing requires passing the complete new body.

### Body editing: choosing the right approach

| Situation | Approach |
|------|-----|
| Normal draft (no quoted content) | PUT with full `body` replacement |
| Reply/forward draft, edit user-written part | Replace `body` with user text + re-append quoted block |
| Reply/forward draft, edit quoted content | Replace `body` with complete new HTML (including modified quoted content) |
| Remove quoted content | Replace `body` with user text only, omit quoted block |

**How to determine quoted content:** Call `GET .../drafts/{draft_id}` first. If `has_quoted_content: true`, the draft contains quoted content.

## Security constraints

This operation updates the real draft. You must confirm with the user before calling:
1. Draft ID
2. Final recipient range (To/Cc/Bcc)
3. Final subject and body

## Recommended call — Update draft metadata

```
Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/mail/v1/user_mailboxes/me/drafts/{draft_id}
- body:
  {
    "subject": "Updated subject",
    "to": [{ "mail_address": "alice@example.com" }, { "mail_address": "bob@example.com" }]
  }
- as: user
```

## Recommended call — Update draft body

```
Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/mail/v1/user_mailboxes/me/drafts/{draft_id}
- body:
  {
    "body": "<p>Updated body content</p>",
    "body_type": "html"
  }
- as: user
```

## API request details

```
GET  /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/drafts/{draft_id}
PUT  /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/drafts/{draft_id}
```

## Parameters (PUT body)

| Parameter | Required | Description |
|------|------|------|
| `subject` | No | Replace subject with this value |
| `to` | No | Replace the entire To recipient list |
| `cc` | No | Replace the entire Cc list |
| `bcc` | No | Replace the entire Bcc list |
| `body` | No | New body content (HTML recommended) |
| `body_type` | No | `html` or `plain` |

## Typical scenario

### Get Draft → Edit → Send

Step 1 — View current state of the draft:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/drafts/{draft_id}
- as: user
```

Step 2 — Edit the draft:
```
Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/mail/v1/user_mailboxes/me/drafts/{draft_id}
- body:
  {
    "subject": "Final Version",
    "body": "<p>Updated content</p>",
    "body_type": "html"
  }
- as: user
```

Step 3 — Send draft (only after user confirmation):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/drafts/{draft_id}/send
- as: user
```

## Related references

- [`+draft-create`](lark-mail-draft-create.md) — create a new draft
- [`+reply`](lark-mail-reply.md) — reply to email
