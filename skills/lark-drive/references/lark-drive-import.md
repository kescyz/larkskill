# drive +import

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Import a local file (such as Word, TXT, Markdown, Excel, etc.) and convert it into a Lark online cloud document (docx, sheet, bitable). Under the hood, creates an import task via `POST /open-apis/drive/v1/import_tasks` and polls the result.

## Full execution flow

1. Upload the source file to get a `file_token`:
   - 20MB or less: call `POST /open-apis/drive/v1/medias/upload_all`
   - Over 20MB: use multipart upload (`upload_prepare` → `upload_part` → `upload_finish`)
2. Create the import task via `POST /open-apis/drive/v1/import_tasks`
3. Poll the import task status via `GET /open-apis/drive/v1/import_tasks/{ticket}`

## Step 1 — Upload file (≤20MB)

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/medias/upload_all
- body:
  {
    "file_name": "README.md",
    "parent_type": "explorer",
    "parent_node": "<FOLDER_TOKEN>",
    "size": <FILE_SIZE_BYTES>
  }
```

Returns `file_token`.

## Step 2 — Create import task

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/import_tasks
- body:
  {
    "file_extension": "md",
    "file_token": "<FILE_TOKEN>",
    "type": "docx",
    "point": {
      "mount_type": 1,
      "mount_key": "<FOLDER_TOKEN>"
    }
  }
```

When `folder_token` is omitted, leave `point.mount_key` empty to import to the caller's root directory.

## Step 3 — Poll import task

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/import_tasks/{ticket}
```

Returns `job_status`: 0=success, 1=initializing, 2=processing, 3=complete, -1=failed.

## API request details

```
POST /open-apis/drive/v1/medias/upload_all
POST /open-apis/drive/v1/import_tasks
GET  /open-apis/drive/v1/import_tasks/{ticket}
```

## Parameters (import task body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `file_extension` | Yes | File extension of the uploaded file (auto-inferred from filename) |
| `file_token` | Yes | Token from the upload step |
| `type` | Yes | Target cloud document format: `docx` / `sheet` / `bitable` |
| `point.mount_type` | No | Mount type (`1` = folder) |
| `point.mount_key` | No | Target folder token; empty = import to root directory |

### Supported File Type Conversions

| Local File Extension | Can Import As | Description |
|---------------------|---------------|-------------|
| `.docx`, `.doc` | `docx` | Microsoft Word document |
| `.txt` | `docx` | Plain text file |
| `.md`, `.markdown`, `.mark` | `docx` | Markdown document |
| `.html` | `docx` | HTML document |
| `.xlsx` | `sheet`, `bitable` | Microsoft Excel spreadsheet |
| `.xls` | `sheet` | Microsoft Excel 97-2003 spreadsheet |
| `.csv` | `sheet`, `bitable` | CSV data file |

> [!IMPORTANT]
> File extension and target document type must match:
> - Document files (.docx, .doc, .txt, .md, .html) can **only** be imported as `docx`
> - `.xlsx` / `.csv` files can **only** be imported as `sheet` or `bitable`
> - `.xls` files can **only** be imported as `sheet`

### File Size Limits

| Local File Extension | Import Target | Size Limit |
|---------------------|---------------|------------|
| `.docx`, `.doc` | `docx` | 600MB |
| `.txt` | `docx` | 20MB |
| `.md`, `.mark`, `.markdown` | `docx` | 20MB |
| `.html` | `docx` | 20MB |
| `.xlsx` | `sheet`, `bitable` | 800MB |
| `.csv` | `sheet` | 20MB |
| `.csv` | `bitable` | 100MB |
| `.xls` | `sheet` | 20MB |

### Continued Query After Timeout

When polling window ends but the task has not completed, use the `ticket` from the response to continue querying via `drive +task_result`:

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/import_tasks/{ticket}
```

> [!CAUTION]
> `drive +import` is a **write operation** - confirm user intent before executing.

## References

- [lark-drive](../SKILL.md) -- All Drive commands
- [lark-drive-task-result](lark-drive-task-result.md) -- Poll async task
- [lark-shared](../../lark-shared/SKILL.md) -- Authentication and global parameters
