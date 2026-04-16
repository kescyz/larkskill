# role-update

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.
>
> **Prerequisite:** Base must have advanced permissions enabled. See [`lark-base-advperm-enable.md`](lark-base-advperm-enable.md).

Update the permission configuration of a role.

## Recommended call

Rename only:

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/roles/{role_id}
- body:
  ```json
  { "role_name": "Senior Auditor", "role_type": "custom_role" }
  ```

Update table permissions (other tables unchanged):

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/roles/{role_id}
- body:
  ```json
  {
    "role_name": "Financial Auditor",
    "role_type": "custom_role",
    "table_rule_map": {
      "Order Table": { "perm": "read_only" }
    }
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `role_id` | Yes | Role ID, format `rol` + 8 alphanumeric chars (path param) |
| `role_name` | Yes | Role name — must always be passed even if unchanged (body) |
| `role_type` | Yes | Role type — must always be passed even if unchanged (body) |
| other fields | No | Only fields to change; omitted fields are left unchanged (body) |

## API request details

```
PUT /open-apis/base/v3/bases/{base_token}/roles/{role_id}
```

## Key return fields

- Returns `success: true` on success.

## Workflow

> This is a **high-risk write operation**. Confirm with the user before execution.

1. Use `role-get` to obtain the current configuration and confirm the scope of changes.
2. Show the user what will change; confirm `base_token`, `role_id`, and the delta JSON.
3. Execute the call.

## Pitfalls

- This is a write operation; confirm with the user before execution.
- Delta merge semantics: only passed fields are updated; omitted fields are unchanged.
- `role_name` and `role_type` are required even if not being modified.
- Body cannot be empty; a PUT with no body returns a server error.

## References

- [lark-base-role-get.md](lark-base-role-get.md) — read current config before updating
- [role-config.md](role-config.md) — complete AdvPermBaseRoleConfig structure
- [lark-base-advperm-enable.md](lark-base-advperm-enable.md) — enable advanced permissions
