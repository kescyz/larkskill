# drive +download

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Download files from Lark Drive to local storage.

## Recommended call

Get the download URL first, then download:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/drive/v1/files/{file_token}/download_url
```

Then use the returned `download_url` to download the file to local storage.

## API request details

```
GET /open-apis/drive/v1/files/{file_token}/download_url
```

## Parameters

| Parameter | Required | Description |
|------|----------|-------------|
| `file_token` | Yes (path) | File token |

## URL parsing

Extract token from a Lark file URL:

```
https://xxx.feishu.cn/drive/file/boxbc_xxx
                                  ^^^^^^^^^
                                  file_token
```

## References

- [lark-drive](../SKILL.md) - All Drive commands
- [lark-shared](../../lark-shared/SKILL.md) - Authentication and global parameters
