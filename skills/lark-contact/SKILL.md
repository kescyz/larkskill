---
name: lark-contact
version: 2.0.0
description: "Use this skill when operating Lark Contacts via LarkSkill MCP: look up an employee's profile, name, department, email, or contact info by open_id, or look up self. Note: name/email → open_id resolution (search-user) is not available via MCP catalog — only get-user (by open_id) is supported. Does NOT handle department tree traversal, listing employees by department, or org chart."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# lark-contact

## Which Command to Use

**User identity and bot identity are two completely separate paths.** Determine the current identity first, then choose the operation per the table below:

| Intent | User identity | Bot identity |
|---|---|---|
| Resolve name / email → open_id | `lark_api({ tool: 'contact', op: 'search-user', args: { query: '<name or email>' } })` | Not supported (requires user identity) |
| Already have open_id, look up another person's profile | `lark_api({ tool: 'contact', op: 'get-user', args: { user_id: '<id>' } })` | `lark_api({ tool: 'contact', op: 'get-user', args: { user_id: '<id>' } })` |
| Look up self | `lark_api({ tool: 'contact', op: 'get-user', args: {} })` | Not supported |

If you already have an open_id and only want to send a message or schedule a meeting, you do NOT need to go through contact — go directly to [`lark-im`](../lark-im/SKILL.md) / [`lark-calendar`](../lark-calendar/SKILL.md).

## Typical Scenarios

```
// Resolve a person by name or email to get their open_id (user identity required):
lark_api({ tool: 'contact', op: 'search-user', args: { query: 'Alice Nguyen' } })

// Look up a specific user by open_id (either identity):
lark_api({ tool: 'contact', op: 'get-user', args: { user_id: 'ou_xxx' } })

// Look up self (user identity):
lark_api({ tool: 'contact', op: 'get-user', args: {} })
```

If the user only provides a name and you need to message them: first call `search-user` to get the open_id, then hand off to `lark-im`.

## Notes

- **41050 / Permission denied** is restricted by the visible scope of the current identity. Switch to bot identity or ask an admin to adjust the visible scope; see [`lark-shared`](../lark-shared/SKILL.md) for details.
- **Cross-tenant users** (`is_cross_tenant=true`): most business fields are empty strings — this is a Lark visibility rule; handle empty values gracefully downstream.
- **ID type**: defaults to `open_id`. `get-user` can accept `user_id_type: 'union_id'` or `'user_id'` in args.

## Out of Scope

- Send messages / query chat history → [`lark-im`](../lark-im/SKILL.md)
- Schedule meetings / invite to calendar events → [`lark-calendar`](../lark-calendar/SKILL.md)
- Department tree / list employees by department / org chart — find the native API via [`lark-openapi-explorer`](../lark-openapi-explorer/SKILL.md)
- Name/email → open_id search — not available via MCP catalog (see note above)
