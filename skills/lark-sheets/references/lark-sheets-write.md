# sheets +write (Write cells / overwrite)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Write cell values to a specified range (overwrite).

- `values` must be 2D-array JSON
- Built-in size checks: up to 5000 rows, up to 100 columns per row

> [!CAUTION]
> This is a **write operation**. Confirm user intent before execution.

## Recommended call

```
Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}
- body:
  {
    "valueRange": {
      "range": "<sheet_id>!A1:B2",
      "values": [["name", "age"], ["alice", 18]]
    }
  }
```

Write single cell:
```
Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}
- body:
  {
    "valueRange": {
      "range": "<sheet_id>!C2",
      "values": [["hello"]]
    }
  }
```

## API request details

```
PUT /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}
```

## Parameters

| Parameter | Required | Description |
|------|------|------|
| `spreadsheet_token` | Yes (path) | Spreadsheet token |
| `range` | Yes (path) | Write range: `{sheet_id}!A1:D10`, or `{sheet_id}` (auto-expands by values size) |
| `valueRange.range` | Yes (body) | Same range, also specified in body |
| `valueRange.values` | Yes (body) | 2D-array JSON values |

## Output

Response includes:
- `updated_range`
- `updated_rows`
- `updated_columns`
- `updated_cells`
- `revision`

## References

- [lark-sheets-read](lark-sheets-read.md)
- [lark-shared](../../lark-shared/SKILL.md)
