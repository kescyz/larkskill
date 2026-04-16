---
name: lark-approval
version: 2.0.0
description: "Feishu Approval API via LarkSkill MCP: approval instance and approval task management. Use when users need to query, cancel, or CC approval instances, or approve/reject/transfer/query approval tasks."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# approval (v4)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## instances

### instances.get — Get approval instance details

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/approval/v4/instances/{instance_id}
- as: user
```

### instances.cancel — Withdraw an approval instance

> Confirm user intent before executing. This is a write operation.

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/approval/v4/instances/cancel
- body:
  {
    "approval_code": "<approval_code>",
    "instance_code": "<instance_code>",
    "user_id": "<operator_open_id>"
  }
- as: user
```

### instances.cc — CC an approval instance

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/approval/v4/instances/cc
- body:
  {
    "approval_code": "<approval_code>",
    "instance_code": "<instance_code>",
    "user_id": "<operator_open_id>",
    "cc_user_ids": ["<target_open_id>"]
  }
- as: user
```

## tasks

### tasks.approve — Approve an approval task

> Confirm user intent before executing. This is a write operation.

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/approval/v4/tasks/approve
- body:
  {
    "approval_code": "<approval_code>",
    "instance_code": "<instance_code>",
    "user_id": "<operator_open_id>",
    "task_id": "<task_id>"
  }
- as: user
```

### tasks.reject — Reject an approval task

> Confirm user intent before executing. This is a write operation.

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/approval/v4/tasks/reject
- body:
  {
    "approval_code": "<approval_code>",
    "instance_code": "<instance_code>",
    "user_id": "<operator_open_id>",
    "task_id": "<task_id>",
    "reason": "<rejection reason>"
  }
- as: user
```

### tasks.transfer — Transfer an approval task

> Confirm user intent before executing. This is a write operation.

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/approval/v4/tasks/transfer
- body:
  {
    "approval_code": "<approval_code>",
    "instance_code": "<instance_code>",
    "user_id": "<operator_open_id>",
    "task_id": "<task_id>",
    "transfer_user_id": "<target_open_id>"
  }
- as: user
```

### tasks.query — Query a user's approval task list

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/approval/v4/tasks/query
- params:
  {
    "user_id": "<open_id>",
    "topic": "1"
  }
- as: user
```

`topic` values: `1` = pending, `2` = approved, `3` = rejected, `4` = transferred, `5` = completed.

## Permission Table

| Operation | Required Scope |
|-----------|---------------|
| `instances.get` | `approval:instance:read` |
| `instances.cancel` | `approval:instance:write` |
| `instances.cc` | `approval:instance:write` |
| `tasks.approve` | `approval:task:write` |
| `tasks.reject` | `approval:task:write` |
| `tasks.transfer` | `approval:task:write` |
| `tasks.query` | `approval:task:read` |
