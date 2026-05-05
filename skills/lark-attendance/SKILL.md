---
name: lark-attendance
version: 1.0.0
description: "Use this skill when querying Lark Attendance check-in records via LarkSkill MCP."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api"]
---

# attendance (v1)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first — it covers authentication and permission handling.

## Auto-fill rules for default parameters

When calling any attendance API, the following parameters **MUST be auto-filled — DO NOT ask the user for these values**:

| Parameter | Fixed value | Notes |
|-----------|-------------|-------|
| `employee_type` | `"employee_no"` | Always set `employee_type` to `"employee_no"` |
| `user_ids` | `[]` (empty array) | Always set `user_ids` to `[]` |

### Fill example

When building the `--params` payload, inject the fields above automatically:

- `employee_type` stays `"employee_no"` unchanged

When building the `--data` payload, inject:

```json
{
  "user_ids": [],
  ...user-supplied parameters
}
```

> **Note:** Keep `user_ids` as an empty array `[]` and `employee_type` as `"employee_no"` — do not change these.

## API Resources

Call the attendance API using the raw HTTP form (no shortcut op available for this domain):

```
lark_api({ method: 'POST', path: '/open-apis/attendance/v1/user_tasks/query', params: { employee_type: 'employee_no' }, data: { user_ids: [], ...args } })
```

> **Important:** Before using the raw API, inspect the request schema to understand the `data` / `params` field structure — do not guess field formats.

### user_tasks

- `query` — Query user attendance check-in records

## Permission table

| Method | Required scope |
|--------|----------------|
| `user_tasks.query` | `attendance:task:readonly` |
