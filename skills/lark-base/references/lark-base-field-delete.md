# field-delete

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

Delete a field.

## Recommended call

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields/{field_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `field_id` | Yes | Field ID or field name (path param) |

## API request details

```
DELETE /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields/{field_id}
```

## Response highlights

- Returns `deleted: true` and the target field ID.

## Workflow

> This is a **high-risk write operation**. If the user explicitly requested deletion and the target is clear, proceed directly without re-confirming.

1. Recommended to use `field-get` or `field-list` to confirm the target field first.
2. Only ask follow-up if the field target is still unclear.

## Pitfalls

- ⚠️ High-risk write operation; cannot be recovered after deletion.

## References

- [lark-base-field.md](lark-base-field.md) — field index page
