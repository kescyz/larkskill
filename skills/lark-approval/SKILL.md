---
name: lark-approval
version: 2.0.0
description: "Use this skill when operating Lark Approval via LarkSkill MCP: approval instance and task management."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# approval (v4)

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling.**

## API Resources

Use the LarkSkill MCP tool to call approval operations:

```
lark_api({ tool: 'approval', op: 'instances.get', args: { ... } })
lark_api_search({ query: 'approval instances', domain: 'approval' })  // discover available ops
```

> **Important**: always use `lark_api_search` to discover the exact args shape for an operation before invoking it — do not guess field formats.

### instances

  - `instances.get` — Get details of a single approval instance
  - `instances.cancel` — Cancel an approval instance
  - `instances.cc` — CC an approval instance
  - `instances.initiated` — Query the list of approval instances initiated by a user

### tasks

  - `tasks.remind` — Send a reminder to an approver
  - `tasks.approve` — Approve an approval task
  - `tasks.reject` — Reject an approval task
  - `tasks.transfer` — Transfer an approval task
  - `tasks.query` — Query the task list for a user
  - `tasks.add_sign` — Add a countersignature to an approval task
  - `tasks.rollback` — Roll back an approval task

## Permissions

| Method | Required scope |
|---|---|
| `instances.get` | `approval:instance:read` |
| `instances.cancel` | `approval:instance:write` |
| `instances.cc` | `approval:instance:write` |
| `instances.initiated` | `approval:instance:read` |
| `tasks.remind` | `approval:instance:write` |
| `tasks.approve` | `approval:task:write` |
| `tasks.reject` | `approval:task:write` |
| `tasks.transfer` | `approval:task:write` |
| `tasks.query` | `approval:task:read` |
| `tasks.add_sign` | `approval:task:write` |
| `tasks.rollback` | `approval:task:write` |
