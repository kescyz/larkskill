# form-delete

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Delete a specified form from a Base table. **Irreversible — confirm explicitly before execution.**

## Recommended call

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (path param) |
| `form_id` | Yes | Form ID to delete (path param) |

## API request details

```
DELETE /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}
```

## Key return fields

| Field | Description |
|-------|-------------|
| `deleted` | `true` on success |
| `form_id` | ID of the deleted form |

```json
{
  "data": {
    "deleted": true,
    "form_id": "vewX58te9D"
  }
}
```

## Workflow

> This is a **high-risk write operation (deletion)** — explicitly confirm with the user that the operation is irreversible before proceeding.

1. Use `form-list` or `form-get` to confirm the target form exists.
2. Show the user the form name and ID to be deleted; wait for explicit confirmation.
3. Execute delete.
4. Report the result.

## Pitfalls

- Before deleting, use `form-questions-list` to review form content to avoid accidental deletion.
- `form_id` can be obtained via `form-list`.

## References

- [lark-base-form-list.md](lark-base-form-list.md) — List forms to find `form_id`
- [lark-base-form-questions-list.md](lark-base-form-questions-list.md) — Preview questions before deletion
