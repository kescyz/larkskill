# mail +watch

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Watch for incoming mail events. Requires the `mail:event` scope and a configured bot event subscription for `mail.user_mailbox.event.message_received_v1`.

> **Note**: Event watching via MCP is driven by the LarkSkill event subscription mechanism, not a WebSocket connection. Use the event subscription API to configure and manage mail event subscriptions.

## Subscribe to mail events

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/mail/v1/user_mailboxes/me/event/subscribe
- body:
  {
    "event_type": "mail.user_mailbox.event.message_received_v1"
  }
- as: user
```

## Query subscription status

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/mail/v1/user_mailboxes/me/event/subscription
- as: user
```

## Unsubscribe from mail events

```
Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/mail/v1/user_mailboxes/me/event/unsubscribe
- body:
  {
    "event_type": "mail.user_mailbox.event.message_received_v1"
  }
- as: user
```

## API request details

```
POST   /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/event/subscribe
GET    /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/event/subscription
DELETE /open-apis/mail/v1/user_mailboxes/{user_mailbox_id}/event/unsubscribe
```

## Required scope

`mail:event`

## Related references

- [`+triage`](lark-mail-triage.md) — list mail summaries
- [lark-mail](../SKILL.md) — all mail operations
