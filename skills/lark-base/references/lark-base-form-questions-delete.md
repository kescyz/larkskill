# form-questions-delete

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Batch delete questions from a Base form. **Irreversible — confirm explicitly before execution.**

## Recommended call

Delete a single question:

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
- body:
  ```json
  { "question_ids": ["q_001"] }
  ```

Delete multiple questions:

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
- body:
  ```json
  { "question_ids": ["q_001", "q_002", "q_003"] }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID (path param) |
| `form_id` | Yes | Form ID (path param) |
| `question_ids` | Yes | JSON array of question IDs to delete, up to 10 (body) |

## API request details

```
DELETE /open-apis/base/v3/bases/{base_token}/tables/{table_id}/forms/{form_id}/questions
```

## Key return fields

```json
{
  "data": {
    "deleted": true,
    "question_ids": ["q_001", "q_002"]
  }
}
```

## Workflow

> This is a **high-risk write operation (deletion)** — explicitly confirm with the user that the operation is irreversible before proceeding.

1. Use `form-questions-list` to view the question list and confirm the IDs to delete.
2. Show the user the question titles and IDs to be removed; wait for explicit confirmation.
3. Execute deletion and report the result.

## References

- [lark-base-form-questions-list.md](lark-base-form-questions-list.md) — List questions to find IDs
- [lark-base-form-questions-create.md](lark-base-form-questions-create.md) — Add questions
