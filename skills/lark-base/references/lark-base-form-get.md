# form-get

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Get details of a specified form in a Base table. Read-only — no data is modified.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (path param) |
| `form_id` | Yes | Form ID (path param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}
```

## Key return fields

| Field | Description |
|-------|-------------|
| `id` | Form ID |
| `name` | Form name |
| `description` | Form description |

```json
{
  "data": {
    "id": "vewX58te9D",
    "name": "User Research Questionnaire",
    "description": "2024 User Satisfaction Survey"
  }
}
```

## Pitfalls

- `form_id` can be obtained via `form-list`.

## References

- [lark-base-form-list.md](lark-base-form-list.md) — List forms to find `form_id`
- [lark-base-form-update.md](lark-base-form-update.md) — Update form name/description
