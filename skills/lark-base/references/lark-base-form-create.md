# form-create

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Create a new form in a Base table.

## Notes

- **Form selection:** Before creating a form, consider whether this is a new business area. If so, create a new table with `table-create` first.
- **Naming consistency:** Form names should match the form's purpose. Avoid creating unrelated forms in shared tables.

## Recommended call

Create form (required parameters only):

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms
- body:
  ```json
  { "name": "User Research Questionnaire" }
  ```

Create with description:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms
- body:
  ```json
  {
    "name": "User Survey Questionnaire",
    "description": "2024 User Satisfaction Survey"
  }
  ```

Create with Markdown link in description:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms
- body:
  ```json
  {
    "name": "User Survey Questionnaire",
    "description": "2024 annual survey, [please view details](https://example.com)"
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (path param) |
| `name` | Yes | Form name (body) |
| `description` | No | Form description — plain text or Markdown link e.g. `[Text](https://example.com)` (body) |

## Key return fields

| Field | Description |
|-------|-------------|
| `id` | Newly created form ID |
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

## Workflow

> This is a **write operation**; confirm with the user before execution.

1. Confirm `base_token` and `table_id`.
2. Confirm form name and description.
3. Execute and report the returned `id` — it can be used to add questions later (`form-questions-create`).

## References

- [lark-base-form.md](lark-base-form.md) — Form operation index
- [lark-base-form-questions-create.md](lark-base-form-questions-create.md) — Add questions to a form
