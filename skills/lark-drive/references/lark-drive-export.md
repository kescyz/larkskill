# drive +export

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Export a `doc` / `docx` / `sheet` / `bitable` to a local file. This operation creates an export task with built-in limited polling:

- If the export task completes within the polling window, download directly
- If polling ends before completion, returns `ticket` for subsequent querying
- To continue checking the result afterward, use `drive +task_result --scenario export`
- Once you have the `file_token`, use `drive +export-download`

## Recommended call — Create export task

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/export_tasks
- body:
  {
    "file_extension": "pdf",
    "token": "<DOCX_TOKEN>",
    "type": "docx"
  }
```

Export spreadsheet as xlsx:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/export_tasks
- body:
  {
    "file_extension": "xlsx",
    "token": "<SHEET_TOKEN>",
    "type": "sheet"
  }
```

Export spreadsheet sheet as csv (sub_id required):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/export_tasks
- body:
  {
    "file_extension": "csv",
    "token": "<SHEET_TOKEN>",
    "type": "sheet",
    "sub_id": "<SHEET_ID>"
  }
```

## Poll export task result

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/export_tasks/{ticket}
- params: { "token": "<SOURCE_DOC_TOKEN>" }
```

## API request details

```
POST /open-apis/drive/v1/export_tasks
GET  /open-apis/drive/v1/export_tasks/{ticket}
```

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `file_extension` | Yes | Export format: `docx` / `pdf` / `xlsx` / `csv` / `markdown` |
| `token` | Yes | Source document token |
| `type` | Yes | Source document type: `doc` / `docx` / `sheet` / `bitable` |
| `sub_id` | Conditionally required | Required when exporting `sheet` / `bitable` as `csv` |

## Key Constraints

- `markdown` only supports `docx`
- Exporting `sheet` / `bitable` as `csv` requires `sub_id`

## Recommended Follow-up Flow

Step 1 — Create export task (call above).

Step 2 — If not immediately done, poll:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/export_tasks/{ticket}
- params: { "token": "<SOURCE_DOC_TOKEN>" }
```

Step 3 — Once `job_status = 0` (success), get `file_token` and download via `drive +export-download`.

## References

- [lark-drive](../SKILL.md) -- All Drive commands
- [lark-drive-export-download](lark-drive-export-download.md) -- Download exported file
- [lark-drive-task-result](lark-drive-task-result.md) -- Poll async task
- [lark-shared](../../lark-shared/SKILL.md) -- Authentication and global parameters
