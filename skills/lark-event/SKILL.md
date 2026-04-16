---
name: lark-event
version: 2.0.0
description: "Feishu event subscription reference: WebSocket long-connection event listening for Feishu events (messages, contact changes, calendar changes, etc.). NOTE: V2 MCP does not expose live event subscription — this skill documents the underlying Lark Open Platform event model for reference. Live event handling will ship in a future LarkSkill release. Use when users need to understand Lark event types, scopes, or design event-driven integrations."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api"]
---

# event (v2)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

> **V2 MCP LIMITATION**: The LarkSkill MCP server does not currently expose WebSocket event subscription. This skill documents the underlying Lark Open Platform event model for reference and design purposes. Live event handling (real-time push via WebSocket) will ship in a future LarkSkill release.
>
> For event-driven workflows today, consider polling with `lark_api` on a schedule (e.g. periodically GET messages, calendar events, or task updates) as an alternative to push events.

## Event Model Overview

Lark Open Platform delivers events via WebSocket long connection (server-push model). Events are structured NDJSON payloads.

**Platform-side configuration** (must be done in the Lark Open Platform console before any subscription):
1. Events & Callbacks → Subscription method → Select "Use long connection to receive events"
2. Add the events you need (e.g. `im.message.receive_v1`)
3. Enable the corresponding permissions (e.g. `im:message:receive_as_bot`)

**Identity**: bot-only — WebSocket connections use App ID + App Secret. No user OAuth needed.

## Supported Event Types

### IM

| Event Type | Description | Required Scope |
|-----------|-------------|---------------|
| `im.message.receive_v1` | Receive message | `im:message:receive_as_bot` |
| `im.message.message_read_v1` | Message read | `im:message:receive_as_bot` |
| `im.message.reaction.created_v1` | Reaction added | `im:message:receive_as_bot` |
| `im.message.reaction.deleted_v1` | Reaction removed | `im:message:receive_as_bot` |
| `im.chat.member.bot.added_v1` | Bot added to chat | `im:chat:readonly` |
| `im.chat.member.bot.deleted_v1` | Bot removed from chat | `im:chat:readonly` |
| `im.chat.member.user.added_v1` | User added to chat | `im:chat:readonly` |
| `im.chat.member.user.withdrawn_v1` | User add withdrawn | `im:chat:readonly` |
| `im.chat.member.user.deleted_v1` | User removed from chat | `im:chat:readonly` |
| `im.chat.updated_v1` | Chat info updated | `im:chat:readonly` |
| `im.chat.disbanded_v1` | Chat disbanded | `im:chat:readonly` |

### Contact

| Event Type | Description | Required Scope |
|-----------|-------------|---------------|
| `contact.user.created_v3` | User created | `contact:user.base:readonly` |
| `contact.user.updated_v3` | User updated | `contact:user.base:readonly` |
| `contact.user.deleted_v3` | User deleted | `contact:user.base:readonly` |
| `contact.department.created_v3` | Department created | `contact:department.base:readonly` |
| `contact.department.updated_v3` | Department updated | `contact:department.base:readonly` |
| `contact.department.deleted_v3` | Department deleted | `contact:department.base:readonly` |

### Calendar

| Event Type | Description | Required Scope |
|-----------|-------------|---------------|
| `calendar.calendar.acl.created_v4` | Calendar ACL created | `calendar:calendar.acl:readonly` |
| `calendar.calendar.event.changed_v4` | Calendar event changed | `calendar:calendar:readonly` |

### Approval

| Event Type | Description | Required Scope |
|-----------|-------------|---------------|
| `approval.approval.updated` | Approval status updated | `approval:approval:readonly` |

### Task

| Event Type | Description | Required Scope |
|-----------|-------------|---------------|
| `task.task.update_tenant_v1` | Task updated (tenant) | `task:task:readonly` |
| `task.task.comment_updated_v1` | Task comment updated | `task:task:readonly` |

### Drive

| Event Type | Description | Required Scope |
|-----------|-------------|---------------|
| `drive.notice.comment_add_v1` | Drive comment added | `drive:drive:readonly` |

See the full list at [Lark Event List](https://open.feishu.cn/document/server-docs/event-subscription-guide/event-list).

## Polling Alternative (Available Now via MCP)

Until live event subscription is available, use polling with `lark_api` for common use cases:

**Poll for new IM messages:**

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages
- params:
  {
    "container_id_type": "chat",
    "container_id": "<chat_id>",
    "start_time": "<unix_timestamp>"
  }
- as: bot
```

**Poll for calendar event changes:**

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/calendar/v4/calendars/{calendar_id}/events
- params: { "sync_token": "<sync_token>" }
- as: user
```

## Event Payload Structure

Event payloads follow this schema:

```json
{
  "schema": "2.0",
  "header": {
    "event_id": "xxx",
    "event_type": "im.message.receive_v1",
    "create_time": "1773491924409",
    "app_id": "cli_xxx"
  },
  "event": { ... }
}
```

## References

- [lark-event-subscribe](references/lark-event-subscribe.md) — Full event subscription reference (for future implementation)
- [lark-im](../lark-im/SKILL.md) — Messaging commands
- [lark-shared](../lark-shared/SKILL.md) — Authentication and global parameters
