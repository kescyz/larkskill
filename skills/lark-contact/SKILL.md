---
name: lark-contact
version: 2.0.0
description: "Feishu Contacts: query org structure, user information, and search employees via LarkSkill MCP. Retrieve detailed info for current or specified users, and search employees by keywords (name/email/phone). Use when users need to view profile info, find colleague open_id or contact info, search employees by name, or inspect department structure."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# contact (v2)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## Operations

| Operation | Reference |
|-----------|-----------|
| [`get-user`](references/lark-contact-get-user.md) | Get user info (omit user_id for self; provide user_id for specific user) |
| [`search-user`](references/lark-contact-search-user.md) | Search users by keyword (results sorted by relevance) |

## Permission Table

| Operation | Required Scope |
|-----------|---------------|
| `get-user` (self) | `contact:user.base:readonly` |
| `get-user` (specific user) | `contact:user.base:readonly` |
| `search-user` | `contact:user.base:readonly` |
