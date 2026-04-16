# form-questions-list

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

List all questions in a Base form/questionnaire. Read-only — no data is modified.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (path param) |
| `form_id` | Yes | Form ID (path param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
```

## Key return fields

Each question contains:

| Field | Description |
|-------|-------------|
| `id` | Question ID (same as `field_id` in the table) |
| `title` | Question title |
| `description` | Question description |
| `required` | Whether the question is required |

```json
{
  "data": {
    "questions": [
      {
        "id": "q_001",
        "title": "What is your name?",
        "description": "Please fill in your real name",
        "required": true
      },
      {
        "id": "q_002",
        "title": "What is your contact information?",
        "description": "Mobile phone number or email address",
        "required": false
      }
    ],
    "total": 2
  }
}
```

## Pitfalls

- Question `id` is the same as `field_id` in the table.
- The returned question list is sorted by display order.

## References

- [lark-base-form-questions-create.md](lark-base-form-questions-create.md) — Add questions
- [lark-base-form-questions-delete.md](lark-base-form-questions-delete.md) — Delete questions
- [lark-base-form-questions-update.md](lark-base-form-questions-update.md) — Update a question
