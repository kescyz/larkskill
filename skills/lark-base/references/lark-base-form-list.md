# form-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

List all forms in a Base table. Returns all results. Read-only — no data is modified.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms

With pagination:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms
- params:
  ```json
  { "page_size": 100 }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (path param) |
| `page_size` | No | Page size, default 100, max 100 (query param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms
```

## Key return fields

Each form contains:

| Field | Description |
|-------|-------------|
| `id` | Form ID (e.g. `vewX58te9D`) |
| `name` | Form name |
| `description` | Form description |

```json
{
  "data": {
    "forms": [
      {"id": "vewX58te9D", "name": "User Survey Questionnaire", "description": "..."},
      {"id": "form_yyyy", "name": "Product Feedback Form", "description": "..."}
    ],
    "total": 2
  }
}
```

## Pitfalls

- If no forms exist, `forms` is an empty array — not an error.

## References

- [lark-base-form-get.md](lark-base-form-get.md) — Get form details
- [lark-base-form-create.md](lark-base-form-create.md) — Create a form
