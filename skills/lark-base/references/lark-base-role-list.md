# role-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.
>
> **Prerequisite:** Base must have advanced permissions enabled. See [`lark-base-advperm-enable.md`](lark-base-advperm-enable.md).

List all roles under the specified Base (system roles and custom roles), returning `role_id` / `role_name` / `role_type`.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/roles

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/roles
```

## Key return fields

- Returns `base_roles` (array of role summaries) and `total`.
- Each role: `role_id`, `role_name`, `role_type` (`editor` / `reader` / `custom_role`).

## Pitfalls

- Returns summary only (`role_id` / `role_name` / `role_type`); use `role-get` for full permission config.
- Result includes system roles (`editor` / `reader`).

## References

- [lark-base-role-get.md](lark-base-role-get.md) — get full role config
- [lark-base-advperm-enable.md](lark-base-advperm-enable.md) — enable advanced permissions
