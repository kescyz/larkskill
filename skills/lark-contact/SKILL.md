---
name: lark-contact
version: 1.0.0
description: "Use this skill when operating Lark Contact via LarkSkill MCP: get current or specified user info, and search employees by name / email / phone. Use it to view personal info, look up a colleague open_id, or search staff by keyword."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# contact

## Prerequisites

- LarkSkill MCP server connected (install via `/plugin marketplace add kescyz/larkskill` → `/plugin install larkskill`, or see https://portal.larkskill.app/setup)
- MCP tools available: `lark_api`, `lark_api_search`
- Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first for auth, global flags, and safety rules

## Shortcuts (prefer these)

Shortcuts are high-level wrappers around common operations. When a shortcut exists, use it first.

| Shortcut | Description |
|----------|-------------|
| [`+search-user`](references/lark-contact-search-user.md) | Search users (results sorted by relevance) |
| [`+get-user`](references/lark-contact-get-user.md) | Get user info (omit user_id for self; provide user_id for specific user) |

## Intent → MCP call index

| Intent | MCP call |
|--------|----------|
| Get current user info (self) | `lark_api({ tool: 'contact', op: 'get-user' })` |
| Get specified user info | `lark_api({ tool: 'contact', op: 'get-user', args: { user_id: 'ou_xxx' } })` |
| Search users by keyword (name / email / phone) | See [`references/lark-contact-search-user.md`](references/lark-contact-search-user.md) |
