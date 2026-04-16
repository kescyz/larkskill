# mail +messages

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Read the complete contents of multiple emails at once by passing in a list of `message_id`.

This is a bulk version of `+message`. Use it in preference to the native batch_get API because the output structure of each email is normalized and unavailable message IDs are explicitly listed.

## Recommended call

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/messages/batch_get
- body:
  {
    "message_ids": ["<id1>", "<id2>", "<id3>"]
  }
- as: user
```

## API request details

```
POST /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/messages/batch_get
```

## Parameters (body)

| Parameter | Required | Description |
|------|------|------|
| `message_ids` | Yes | Array of message IDs to fetch |

## Response highlights

The response contains:

| Field | Description |
|------|------|
| `messages` | Returned mail list, same structure as `+message` output per item |
| `total` | Number of emails successfully returned |
| `unavailable_message_ids` | IDs requested but not returned by the API |

Each `messages[]` item uses the same structure as [`+message`](./lark-mail-message.md). See `+message` field descriptions for the complete list of fields.

## Notes

- Use `+message` when only reading one message.
- `message_ids` has no hard cap; split large lists into multiple batched calls if needed.
- Both normal attachments and inline images appear in `messages[].attachments[]`.

## Typical scenario

### Batch digest multiple known emails

Step 1 — Read multiple emails at once:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/messages/batch_get
- body: { "message_ids": ["<id1>", "<id2>", "<id3>"] }
- as: user
```

Step 2 — Analyze `messages[].body_plain_text` and generate grouped summaries.

## Related references

- [`+message`](lark-mail-message.md) — read a single email
- [`+thread`](lark-mail-thread.md) — read all messages in the session
