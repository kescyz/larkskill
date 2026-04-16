# role-delete

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.
>
> **Prerequisite:** Base must have advanced permissions enabled. See [`lark-base-advperm-enable.md`](lark-base-advperm-enable.md).

Delete a custom role. System roles (`editor` / `reader`) cannot be deleted.

## Recommended call

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/roles/{role_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `role_id` | Yes | Role ID, format `rol` + 8 alphanumeric chars (path param) |

## API request details

```
DELETE /open-apis/base/v3/bases/{base_token}/roles/{role_id}
```

## Key return fields

- Returns `success: true` on success.

## Workflow

> This is a **high-risk irreversible operation**. Confirm with the user before execution.

1. Use `role-list` to confirm the role exists.
2. Confirm `base_token` and `role_id` with the user.
3. Execute the call.

## Pitfalls

- Only custom roles can be deleted; attempting to delete system roles (`editor` / `reader`) returns a business error.
- Irreversible: the role and all associated member configurations cannot be restored.
- Obtain `role_id` via `role-list`; format is `rol` + 8 alphanumeric characters.

## References

- [lark-base-role-list.md](lark-base-role-list.md) — list roles
- [lark-base-advperm-enable.md](lark-base-advperm-enable.md) — enable advanced permissions
