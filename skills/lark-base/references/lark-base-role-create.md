# role-create

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.
>
> **Prerequisite:** Base must have advanced permissions enabled. If the API returns that advanced permissions are not enabled, see [`lark-base-advperm-enable.md`](lark-base-advperm-enable.md).

Create a custom role in the specified Base.

## Recommended call

Simple role (name + type only):

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/roles
- body:
  ```json
  { "role_name": "Financial Auditor", "role_type": "custom_role" }
  ```

Role with full permission config:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/roles
- body:
  ```json
  {
    "role_name": "Financial Auditor",
    "role_type": "custom_role",
    "base_rule_map": { "copy": false, "download": false },
    "table_rule_map": {
      "Order Table": {
        "perm": "edit",
        "record_rule": {
          "record_operations": ["add"],
          "edit_filter_rule_group": {
            "conjunction": "and",
            "filter_rules": [{"conjunction": "and", "filters": [{"field_name": "Department", "operator": "is", "filter_values": ["Finance Department"]}]}]
          },
          "other_record_all_read": true
        },
        "field_rule": {
          "field_perm_mode": "specify",
          "field_perms": { "amount": "edit", "remarks": "read", "password": "no_perm" }
        }
      },
      "User Table": { "perm": "read_only" }
    },
    "dashboard_rule_map": { "sales board": { "perm": "read_only" } }
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `role_name` | Yes | Role name (body) |
| `role_type` | Yes | Must be `custom_role` (body) |
| `base_rule_map` | No | Base-level permissions: `copy`, `download` (body) |
| `table_rule_map` | No | Per-table permission config (body) |
| `dashboard_rule_map` | No | Per-dashboard permission config (body) |

## API request details

```
POST /open-apis/base/v3/bases/{base_token}/roles
```

## Key return fields

- Returns `success: true` on success.

## Workflow

1. Confirm `base_token` and role configuration with the user.
2. Execute the call.
3. Confirm the response indicates success.

## Pitfalls

- `role_type` must be `custom_role`; other values return a business error.
- `field_name`, `operator`, `filter_values` are client-supplied; `field_type` / `field_ui_type` / `reference_type` are filled by the server.
- Base must have advanced permissions enabled; user must be a Base administrator.

## References

- [lark-base-advperm-enable.md](lark-base-advperm-enable.md) — enable advanced permissions
- [role-config.md](role-config.md) — complete AdvPermBaseRoleConfig structure
- [lark-base-role-list.md](lark-base-role-list.md) — list roles
