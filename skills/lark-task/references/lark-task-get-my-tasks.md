# task +get-my-tasks

If the user query only specifies a task name (e.g., "Complete task Lobster No. 1"), use this operation to list and search for the task by its summary.

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.
>
> **⚠️ Note:** This API must be called with a user identity (`as: user`). **Do NOT use bot identity, otherwise the call will fail.**
>
> **Output rendering note:**
> 1. If you need to present user fields (assignee, creator, etc.), do not only output the raw `id` (e.g. open_id). Also try to resolve and display the user's real name (e.g. via the contact skill) for readability.
> 2. When rendering timestamps (e.g. created time, due time), use the local timezone. Format is 2006-01-02 15:04:05

List tasks assigned to the current user, with support for filtering by completion status, creation time, and due date.
Paginate manually using `page_token` from each response; repeat until `has_more` is false (up to your desired page limit).

## Recommended call

Search for a specific task by name:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/task/v2/tasks
- params:
  ```json
  { "page_size": 50, "user_id_type": "open_id" }
  ```
- as: user

(Then filter results client-side by `summary` matching the query string.)

Get incomplete tasks with pagination:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/task/v2/tasks
- params:
  ```json
  { "page_size": 50, "completed": false, "user_id_type": "open_id" }
  ```
- as: user

## Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `page_size` | No | Number of results per page (default 20, max 100) |
| `page_token` | No | Pagination token from previous response |
| `completed` | No | Filter by completion: `true` for completed only, `false` for incomplete only. Omit for all |
| `created_from` | No | Query tasks created after this ms timestamp |
| `created_to` | No | Query tasks created before this ms timestamp |
| `due_from` | No | Query tasks with due date after this ms timestamp |
| `due_to` | No | Query tasks with due date before this ms timestamp |
| `user_id_type` | No | User ID type for member fields: `open_id` (default) |

## Workflow

1. Determine the filters based on the user's request.
2. Call `lark_api GET /open-apis/task/v2/tasks` with `as: user`. The API returns a page of results.
3. If `has_more` is true, repeat with `page_token` until all pages are fetched or page limit is reached.
4. Show the results (task GUID, summary, due time, created date). Include `url` if present.
