# event — subscribe (Reference)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand authentication, global parameters, and safety rules.

> **V2 MCP LIMITATION**: WebSocket event subscription is not exposed via the LarkSkill MCP server in V2. This document describes the underlying Lark Open Platform event subscription model for reference and future implementation planning. Live event handling will ship in a future LarkSkill release.

Subscribe to Lark events via WebSocket long connection, outputting NDJSON. Supports compact (agent-friendly) format, regex-based routing, and file output.

**Identity / Risk:**
- **Identity**: bot-only — uses App ID + App Secret to establish the WebSocket connection. No user OAuth needed.
- **Risk**: read-only — receives events but does not modify any resources.

**Platform-side configuration** (must be done in the Lark Open Platform console):
1. Events & Callbacks → Subscription method → Select "Use long connection to receive events"
2. Add the events you need (e.g. `im.message.receive_v1`)
3. Enable the corresponding permissions (e.g. `im:message:receive_as_bot`)

## Conceptual Parameters

| Parameter | Description |
|-----------|-------------|
| `event_types` | Comma-separated event types to register. Omit for catch-all mode (24 common types) |
| `filter` | Client-side regex filter on event_type, applied after SDK delivers events |
| `compact` | Agent-friendly output: flatten structure, extract human-readable content, strip noise fields |
| `output_dir` | Write each event as an individual file: `{type}_{id}_{ts}.json` |
| `route` | Regex-based event routing. Format: `regex=dir:./path`. Unmatched events fall through to `output_dir` or stdout |

## Output Formats

### Default (raw NDJSON)

One event per line, all fields included:

```json
{"schema":"2.0","header":{"event_id":"xxx","event_type":"im.message.receive_v1","create_time":"1773491924409","app_id":"cli_xxx"},"event":{"message":{"chat_id":"oc_xxx","content":"{\"text\":\"Hello\"}","message_id":"om_xxx","message_type":"text"},"sender":{"sender_id":{"open_id":"ou_xxx"},"sender_type":"user"}}}
```

### Compact (agent-friendly)

Flattened key-value output with semantic fields. The exact fields depend on the event type.

**IM message events** (`im.message.receive_v1`):

```json
{"type":"im.message.receive_v1","id":"om_xxx","message_id":"om_xxx","chat_id":"oc_xxx","chat_type":"p2p","message_type":"text","content":"Hello","sender_id":"ou_xxx","create_time":"1773491924409","timestamp":"1773491924409"}
```

- `event.message.content` (double-encoded JSON) is parsed and converted to human-readable text → output as `content`
- `event.sender.sender_id.open_id` → flattened to `sender_id`
- `schema`, `token`, `tenant_key`, `app_id` stripped
- Supports all message types: text, post, image, file, card, etc.

**Non-IM events** (contact, calendar, approval, task, drive, application) use generic compact processing:
- Parses the event payload as a flat map
- Injects `type` (event_type), `event_id`, and `timestamp` from the event header
- All original event fields are preserved as-is

## Notes

- **Events must be configured in the Open Platform console** — subscriptions cannot be dynamically added at runtime
- Event types not registered are silently dropped even if the server sends them
- Only one WebSocket connection per app is recommended; multiple connections cause the server to split events randomly across connections
- WebSocket auto-reconnects on disconnection (SDK built-in)

## Conceptual Pipeline: Listen for messages and reply

In a future LarkSkill release supporting live events, the pattern would be:

1. Receive `im.message.receive_v1` event with `message_id` and `content`
2. Generate reply content
3. Reply via:

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/{message_id}/reply
- body:
  {
    "msg_type": "text",
    "content": "{\"text\": \"<reply text>\"}"
  }
- as: bot
```

## References

- [lark-im](../../lark-im/SKILL.md) — Messaging commands
- [lark-shared](../../lark-shared/SKILL.md) — Authentication and global parameters
