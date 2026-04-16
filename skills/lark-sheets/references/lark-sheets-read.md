# sheets +read (Read cells)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Read cell values from a specified range.

Built-in behavior:
- With `sheet_id`, `range` can be `A1:D10` or `C2`
- Rich text segments are flattened to plain text for cleaner output
- Default max 200 rows (`truncated=true` when exceeded)

## Recommended call

Read a specified range:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}
```

Where `range` format is `{sheet_id}!A1:H20` (e.g. `0b4f58!A1:H20`).

Read with value render option:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}
- params: { "valueRenderOption": "ToString" }
```

## API request details

```
GET /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}
```

## Parameters

| Parameter | Required | Description |
|------|------|------|
| `spreadsheet_token` | Yes (path) | Spreadsheet token |
| `range` | Yes (path) | Read range: `{sheet_id}!A1:D10`, or just `{sheet_id}` for entire sheet |
| `valueRenderOption` | No (query) | `ToString` (default), `FormattedValue`, `Formula`, `UnformattedValue` |

## Output

Response includes:
- `range`: actual range read
- `values`: 2D array of cell values
- `truncated` / `total_rows`: when row limit exceeded

## References

- [lark-sheets-info](lark-sheets-info.md)
- [lark-shared](../../lark-shared/SKILL.md)
