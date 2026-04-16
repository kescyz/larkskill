# drive +task_result

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Query async task results. Aggregates result queries for various async tasks — import, export, move/delete folders — into a unified interface.

## Recommended call — Query import task

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/import_tasks/{ticket}
```

## Recommended call — Query export task

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/export_tasks/{ticket}
- params: { "token": "<SOURCE_DOC_TOKEN>" }
```

## Recommended call — Query move/delete folder task

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/tasks/{task_id}
```

## API request details

```
GET /open-apis/drive/v1/import_tasks/{ticket}
GET /open-apis/drive/v1/export_tasks/{ticket}?token={source_token}
GET /open-apis/drive/v1/tasks/{task_id}
```

## Scenario Descriptions

| Scenario | Description | API path |
|----------|-------------|----------|
| `import` | Document import task | `GET /open-apis/drive/v1/import_tasks/{ticket}` |
| `export` | Document export task | `GET /open-apis/drive/v1/export_tasks/{ticket}?token=...` |
| `task_check` | Folder move/delete task | `GET /open-apis/drive/v1/tasks/{task_id}` |

## Response Results

### Import Scenario Response

```json
{
  "ticket": "<IMPORT_TICKET>",
  "type": "sheet",
  "job_status": 0,
  "job_error_msg": "success",
  "token": "<IMPORTED_DOC_TOKEN>",
  "url": "https://example.feishu.cn/sheets/<IMPORTED_DOC_TOKEN>",
  "extra": ["2000"]
}
```

- `job_status`: 0=success, 1=initializing, 2=processing, -1=failed
- `token`: token of the imported document
- `url`: link to the imported document

### Export Scenario Response

```json
{
  "ticket": "<EXPORT_TICKET>",
  "file_extension": "pdf",
  "type": "doc",
  "file_name": "docName",
  "file_token": "<EXPORTED_FILE_TOKEN>",
  "file_size": 34356,
  "job_error_msg": "success",
  "job_status": 0
}
```

- `job_status`: 0=success
- `file_token`: token of the exported file, used for downloading

### Task_check Scenario Response

```json
{
  "task_id": "<TASK_ID>",
  "status": "success"
}
```

- `status`: `success` / `failed` / `pending`

## Usage Scenarios

### Used with +import

```
# 1. Create import task
POST /open-apis/drive/v1/import_tasks

# 2. Poll import result
GET /open-apis/drive/v1/import_tasks/{ticket}
```

### Used with +move (folder)

```
# 1. Move folder (returns task_id)
POST /open-apis/drive/v1/files/{file_token}/move

# 2. Poll move result
GET /open-apis/drive/v1/tasks/{task_id}
```

### Used with +export

```
# 1. Create export task (returns ticket)
POST /open-apis/drive/v1/export_tasks

# 2. Poll export result
GET /open-apis/drive/v1/export_tasks/{ticket}?token=<SOURCE_TOKEN>

# 3. Download once file_token is available
GET /open-apis/drive/v1/export_tasks/file/{file_token}/download
```

## Permission Requirements

| Scenario | Required Scope |
|----------|---------------|
| import | `drive:drive.metadata:readonly` |
| export | `drive:drive.metadata:readonly` |
| task_check | `drive:drive.metadata:readonly` |

## References

- [lark-drive](../SKILL.md) -- All Drive commands
- [lark-shared](../../lark-shared/SKILL.md) -- Authentication and global parameters
