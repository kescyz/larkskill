# drive +move

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Move a file or folder to another location in the user's Drive.

## Recommended call — Move a file

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/files/{file_token}/move
- body:
  {
    "type": "file",
    "folder_token": "<TARGET_FOLDER_TOKEN>"
  }
```

Move a document:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/files/{file_token}/move
- body:
  {
    "type": "docx",
    "folder_token": "<TARGET_FOLDER_TOKEN>"
  }
```

Move to root folder (omit `folder_token`):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/files/{file_token}/move
- body:
  {
    "type": "file"
  }
```

Move a folder (async operation — poll task_id for completion):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/drive/v1/files/{file_token}/move
- body:
  {
    "type": "folder",
    "folder_token": "<TARGET_FOLDER_TOKEN>"
  }
```

## API request details

```
POST /open-apis/drive/v1/files/{file_token}/move
```

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `type` | Yes | File type: `file`, `docx`, `bitable`, `doc`, `sheet`, `mindnote`, `folder`, `slides` |
| `folder_token` | No | Target folder token; if omitted, moves to the root folder |

## File Type Descriptions

| Type | Description |
|------|-------------|
| `file` | Regular file |
| `docx` | New-version cloud document |
| `doc` | Old-version cloud document |
| `sheet` | Spreadsheet |
| `bitable` | Base (multidimensional table) |
| `mindnote` | Mind note |
| `slides` | Slides |
| `folder` | Folder (moving a folder is an async operation — returns `task_id`) |

## Behavior

- **Regular file move**: synchronous operation, completes immediately
- **Folder move**: async operation — returns a `task_id`. Poll via `drive +task_result`:

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/tasks/{task_id}
```

- **Target folder**: if `folder_token` is omitted, moves to the user's root folder ("My Space")
- **Permission requirements**: requires manageable permission on the file, edit permission on source and target locations

## Limitations

- Wiki documents are not supported for moving
- This API does not support concurrent calls
- Rate limit: 5 QPS and 10,000 requests/day

> [!CAUTION]
> This is a **write operation** - confirm user intent before executing.

## References

- [lark-drive](../SKILL.md) -- All Drive commands
- [lark-drive-task-result](lark-drive-task-result.md) -- Poll async task
- [lark-shared](../../lark-shared/SKILL.md) -- Authentication and global parameters
