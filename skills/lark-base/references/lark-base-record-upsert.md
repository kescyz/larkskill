# record-upsert

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Create a record, or update an existing record by passing `record_id`.

## Recommended call

Create a record:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records
- body:
  ```json
  {
    "Project Name": "Apollo",
    "Status": "In Progress"
  }
  ```

Update an existing record:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}
- body:
  ```json
  {
    "Project Name": "Apollo",
    "Status": "In Progress",
    "Tag": ["High Quality", "External Dependencies"],
    "Deadline": "2026-03-24 10:00:00"
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `record_id` | No | Record ID (path param, PATCH only); omit for create, include for update |
| body | Yes | JSON object of field name/ID → value pairs |

## API request details

```
POST   /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records          # create
PATCH  /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}  # update
```

## JSON body specification

- Body must be a **JSON object** (not an array).
- Keys can be field names or field IDs; use only one identifier per field per request.
- Value must match the field type; run `field-list` first to confirm types.
- Recommended value shapes:
  - Text: `"Title"`
  - Number: `12.5`
  - Single select: `"Todo"`
  - Multi-select: `["A", "B"]`
  - Checkbox: `true`
  - User: `[{"id": "ou_xxx"}]`
  - Linked record: `[{"id": "rec_xxx"}]`
  - Date: `"YYYY-MM-DD HH:mm:ss"` (e.g. `"2026-03-24 10:00:00"`)
- To clear a field, pass `null` (only if the field allows clearing).
- Do not write to read-only fields: formula, lookup, auto-number, creation time, creator, last modified time, last modifier.

## Key return fields

- Create: returns `record` and `created: true`.
- Update: returns `record` and `updated: true`.

## Workflow

1. First determine whether to create or update.
2. If updating, confirm the target `record_id` via `record-get` or `record-list`.
3. Use `field-list` to confirm field names and types before constructing the body.

## Pitfalls

- This is a write operation; confirm with the user before execution.
- No automatic deduplication: omitting `record_id` always creates a new record.
- Arrays are not valid at the top level; body must be an object.

## References

- [lark-base-record.md](lark-base-record.md) — record index page
- [lark-base-shortcut-record-value.md](lark-base-shortcut-record-value.md) — shortcut record value format (recommended)
- [lark-base-field-list.md](lark-base-field-list.md) — list fields to confirm types
