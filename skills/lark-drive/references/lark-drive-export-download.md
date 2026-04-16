# drive +export-download

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Download a local file using the `file_token` from an export task output. Typically used together with `drive +task_result --scenario export`.

## Recommended call

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/export_tasks/file/{file_token}/download
```

## API request details

```
GET /open-apis/drive/v1/export_tasks/file/{file_token}/download
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `file_token` | Yes (path) | The output `file_token` from the completed export task |

## Usage Order

1. Use `drive +export` to initiate an export
2. If it returns `ticket` / polling needed, use `drive +task_result --scenario export` to continue checking
3. Once you have the `file_token`, use `drive +export-download` to download

## References

- [lark-drive](../SKILL.md) -- All Drive commands
- [lark-drive-export](lark-drive-export.md) -- Initiate export
- [lark-drive-task-result](lark-drive-task-result.md) -- Poll async task
- [lark-shared](../../lark-shared/SKILL.md) -- Authentication and global parameters
