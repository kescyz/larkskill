# sheets +create (Create spreadsheet)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Create a new spreadsheet and optionally write initial headers and data.

> [!CAUTION]
> This is a **write operation**. Confirm user intent before execution.

> [!IMPORTANT]
> If created by bot identity, try to grant `full_access` to current available user identity by default.
>
> Suggested flow:
> 1. Call `GET /open-apis/contact/v3/users/me` and read user `open_id`.
> 2. Switch back to bot and call `POST /open-apis/drive/v1/permissions/{token}/members` to grant `full_access` to that user.
>
> If no local user identity is available, explicitly report authorization not completed.
>
> In result output, besides `spreadsheet_token` and `url`, explicitly report authorization result.

## Recommended call — Create spreadsheet

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/sheets/v3/spreadsheets
- body:
  {
    "title": "Warehouse Management Revenue Report",
    "folder_token": "<FOLDER_TOKEN>"
  }
```

## Recommended call — Write headers after creation

After getting `spreadsheet_token` from creation response, write headers:
```
Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}
- body:
  {
    "valueRange": {
      "range": "<sheet_id>!A1:F1",
      "values": [["Warehouse", "Statistical month", "Inbound amount", "Outbound amount", "Sales revenue", "Gross profit margin"]]
    }
  }
```

## Recommended call — Write initial data after headers

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_append
- body:
  {
    "valueRange": {
      "range": "<sheet_id>!A2",
      "values": [["East China Warehouse", "2026-03", 125000, 98000, 168000, "41.7%"]]
    }
  }
```

## API request details

```
POST /open-apis/sheets/v3/spreadsheets
```

## Parameters (body)

| Parameter | Required | Description |
|------|------|------|
| `title` | Yes | Spreadsheet title |
| `folder_token` | No | Target Drive folder token |

## Output

Response includes:
- `spreadsheet_token`
- `title`
- `url`

## References

- [lark-sheets-write](lark-sheets-write.md)
- [lark-sheets-append](lark-sheets-append.md)
- [lark-shared](../../lark-shared/SKILL.md)
