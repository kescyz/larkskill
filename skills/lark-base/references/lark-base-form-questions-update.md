# form-questions-update

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Batch update questions (title, description, required flag) in a Base form/questionnaire. Up to 10 questions per call.

## Recommended call

Update a question title:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
- body:
  ```json
  {
    "questions": [
      {"id": "q_001", "title": "What is your real name?"}
    ]
  }
  ```

Update multiple questions simultaneously:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
- body:
  ```json
  {
    "questions": [
      {"id": "q_001", "title": "Name (required)", "required": true},
      {"id": "q_002", "title": "Contact information", "required": false}
    ]
  }
  ```

Update description with a Markdown link:

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
- body:
  ```json
  {
    "questions": [
      {"id": "q_001", "description": "For more instructions, see [Help Document](https://example.com/help)"}
    ]
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (path param) |
| `form_id` | Yes | Form ID (path param) |
| `questions` | Yes | Question updates JSON array, up to 10 (body) |

## `questions` item fields

Each item must contain `id`; remaining fields are passed as needed:

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Question ID (same as `field_id`); cannot be changed |
| `title` | No | New question title |
| `description` | No | New description — plain text or Markdown link e.g. `[Text](https://example.com)` |
| `required` | No | Whether required (`true`/`false`) |
| `option_display_mode` | No | Option display mode (only for `select`): `0`=dropdown, `1`=portrait (default), `2`=landscape |

## Key return fields

```json
{
  "data": {
    "items": [
      {"id": "q_001", "title": "Name (required)", "required": true}
    ]
  }
}
```

## Workflow

> This is a **write operation**; confirm with the user before execution.

1. Use `form-questions-list` to get existing questions and their `id` values.
2. Construct the update array containing `id` and desired changes.
3. Execute and report the updated question list.

## References

- [lark-base-form-questions-list.md](lark-base-form-questions-list.md) — List questions to get IDs
- [lark-base-form-questions-create.md](lark-base-form-questions-create.md) — Add questions
