# record-delete

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Delete a record.

## Recommended call

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `record_id` | Yes | Record ID (path param) |

## API request details

```
DELETE /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}
```

## Key return fields

- Returns `deleted: true` and the target `record_id`.

## Workflow

> This is a **high-risk write operation**. If the user clearly requested deletion and the target is unambiguous, proceed directly. Do not ask again.

1. Prefer confirming the target first with `record-get`.
2. Only ask follow-up questions if the target record is still unclear.

## Pitfalls

- High-risk irreversible operation; confirm with the user before execution.
- Prefer using `record_id` rather than searching by field value to avoid accidental deletion.

## References

- [lark-base-record.md](lark-base-record.md) — record index page
- [lark-base-record-get.md](lark-base-record-get.md) — get record details
