# table-delete

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

Delete a table.

## Recommended call

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (path param) |

## API request details

```
DELETE /open-apis/base/v3/bases/{base_token}/tables/{table_id}
```

## Key return fields

- Returns `deleted: true` and target `table_id / table_name`.

## Workflow

> This is a **high-risk write operation**. If the user clearly requested deletion and the target is unambiguous, proceed directly. Do not ask again.

1. Prefer confirming the target first with `table-list` or `table-get`.
2. Only ask follow-up questions if the target table is still unclear.

## Pitfalls

- ⚠️ High-risk irreversible operation.
- ⚠️ For delete operations, strongly prefer using `table_id` (`tbl_xxx`) rather than table name.

## References

- [lark-base-table.md](lark-base-table.md) — table index page
- [lark-base-table-list.md](lark-base-table-list.md) — list tables
