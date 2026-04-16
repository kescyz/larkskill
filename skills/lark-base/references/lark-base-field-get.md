# field-get

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

Get the complete configuration of a field.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields/{field_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `field_id` | Yes | Field ID or field name (path param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields/{field_id}
```

## Response highlights

- Returns the complete field configuration, suitable for baseline before update.

## Pitfalls

- ⚠️ In scenarios with duplicate field names, prefer passing `fld_xxx` field ID over field name.

## References

- [lark-base-field.md](lark-base-field.md) — field index page
