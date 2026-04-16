# role-get

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.
>
> **Prerequisite:** Base must have advanced permissions enabled. See [`lark-base-advperm-enable.md`](lark-base-advperm-enable.md).

Get the complete configuration of a role, including table permissions, field permissions, and record filtering.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/roles/{role_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `role_id` | Yes | Role ID, format `rol` + 8 alphanumeric chars (path param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/roles/{role_id}
```

## Key return fields

Complete `AdvPermBaseRole` object (see [role-config.md](role-config.md) for full structure):

| Field | Type | Description |
|-------|------|-------------|
| `role_id` | string | Role ID |
| `role_name` | string | Role name |
| `role_type` | string | Role type |
| `base_rule_map` | map | Base-level permissions (`copy` / `download`) |
| `table_rule_map` | map | Per-table permission configuration |
| `dashboard_rule_map` | map | Per-dashboard permission configuration |
| `docx_rule_map` | map | Per-document permission configuration |

## Pitfalls

- Unlike `role-list` which returns only summary info, `role-get` returns the full permission config.
- If the role does not exist, `data` is an empty string with no error.

## References

- [lark-base-role-list.md](lark-base-role-list.md) — list roles (summary)
- [role-config.md](role-config.md) — AdvPermBaseRoleConfig structure
