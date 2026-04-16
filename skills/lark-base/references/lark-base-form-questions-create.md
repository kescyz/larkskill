# form-questions-create

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Add questions in bulk to a Base form/questionnaire. Up to 10 questions per call.

## Recommended call

Add a required text question:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
- body:
  ```json
  {
    "questions": [
      {"type": "text", "title": "What is your name?", "required": true}
    ]
  }
  ```

Add multiple questions:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
- body:
  ```json
  {
    "questions": [
      {"type": "text", "title": "What is your name?", "required": true},
      {"type": "text", "title": "What is your contact information?", "required": false}
    ]
  }
  ```

Add a single-choice question with options:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
- body:
  ```json
  {
    "questions": [
      {
        "type": "select",
        "title": "Satisfaction Evaluation",
        "required": true,
        "multiple": false,
        "options": [
          {"name": "Very Satisfied", "hue": "Green"},
          {"name": "Satisfied", "hue": "Blue"},
          {"name": "General", "hue": "Yellow"}
        ]
      }
    ]
  }
  ```

Add a rating question:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
- body:
  ```json
  {
    "questions": [
      {
        "type": "number",
        "title": "Service Rating",
        "style": {"type": "rating", "icon": "star", "min": 1, "max": 5}
      }
    ]
  }
  ```

Add a question with a Markdown link description:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
- body:
  ```json
  {
    "questions": [
      {
        "type": "text",
        "title": "Feedback and Suggestions",
        "description": "For more details, please see [Help Document](https://example.com/help)"
      }
    ]
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (path param) |
| `form_id` | Yes | Form ID (path param) |
| `questions` | Yes | Questions JSON array, up to 10 (body) |

## `questions` item fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Question title (field name) |
| `type` | Yes | Question type: `text`, `number`, `select`, `datetime`, `user`, `attachment`, `location` |
| `description` | No | Description — plain text or Markdown link e.g. `[Text](https://example.com)` |
| `required` | No | Whether required (`true`/`false`) |
| `option_display_mode` | No | Option display mode (only for `select`): `0`=dropdown, `1`=portrait (default), `2`=landscape |
| `multiple` | No | Allow multiple selection (only for `select`/`user` types) |
| `options` | No | Option list (only for `select`): `[{"name":"Option 1","hue":"Blue"}]`; hue: `Red`/`Orange`/`Yellow`/`Green`/`Blue`/`Purple`/`Gray` |
| `style` | No | Field style configuration (see below) |

### `style` field

| Type | Style structure | Description |
|------|-----------------|-------------|
| `text` | `{"type":"plain"}` | type: `plain`, `phone`, `url`, `email`, `barcode` |
| `number` | `{"type":"plain","precision":2}` | `precision` = decimal places |
| `number` (rating) | `{"type":"rating","icon":"star","min":1,"max":5}` | icon: `star`/`heart`/`thumbsup`/`fire`/`smile`/`lightning`/`flower`/`number` |
| `datetime` | `{"type":"plain","format":"yyyy/MM/dd"}` | format: `yyyy/MM/dd`, `yyyy/MM/dd HH:mm`, `MM-dd`, `MM/dd/yyyy`, `dd/MM/yyyy` |

## Key return fields

```json
{
  "data": {
    "items": [
      {"id": "q_001", "title": "What is your name?", "required": true}
    ]
  }
}
```

## Workflow

> This is a **write operation**; confirm with the user before execution.

1. Use `form-questions-list` to review existing questions first.
2. Confirm the questions to be added.
3. Execute and report the newly created question IDs.

## References

- [lark-base-form-questions-list.md](lark-base-form-questions-list.md) — List existing questions
- [lark-base-form-questions-delete.md](lark-base-form-questions-delete.md) — Delete questions
