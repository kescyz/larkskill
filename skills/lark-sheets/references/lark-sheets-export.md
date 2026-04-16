# sheets +export (Export spreadsheet)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Export spreadsheet to xlsx or csv. Creates an export task and polls until completion.

## Recommended call — Create export task

Export to xlsx:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/export_tasks
- body:
  {
    "file_extension": "xlsx",
    "token": "<SPREADSHEET_TOKEN>",
    "type": "sheet"
  }
```

Export to csv (sheet_id required):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/export_tasks
- body:
  {
    "file_extension": "csv",
    "token": "<SPREADSHEET_TOKEN>",
    "type": "sheet",
    "sub_id": "<SHEET_ID>"
  }
```

## Recommended call — Poll export task

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/export_tasks/{ticket}
- params: { "token": "<SPREADSHEET_TOKEN>" }
```

## Recommended call — Download exported file

Once `job_status = 0` and `file_token` is available:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/export_tasks/file/{file_token}/download
```

## API request details

```
POST /open-apis/drive/v1/export_tasks
GET  /open-apis/drive/v1/export_tasks/{ticket}?token={spreadsheet_token}
GET  /open-apis/drive/v1/export_tasks/file/{file_token}/download
```

## Parameters (body)

| Parameter | Required | Description |
|------|------|------|
| `file_extension` | Yes | `xlsx` or `csv` |
| `token` | Yes | Spreadsheet token |
| `type` | Yes | `sheet` |
| `sub_id` | No | Sheet ID (required for `csv`) |

## Output

- Export task: `ticket` for polling
- Completed task: `file_token`, `file_name`, `file_size`

## References

- [lark-sheets-info](lark-sheets-info.md)
- [lark-shared](../../lark-shared/SKILL.md)
