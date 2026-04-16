# sheets +append (Append rows)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Append rows after existing data in a spreadsheet.

- `values` must be 2D-array JSON
- Built-in limit checks: up to 5000 rows, up to 100 columns per row
- `range` can be `{sheet_id}` or `{sheet_id}!A1:D10`

> [!CAUTION]
> This is a **write operation**. Confirm user intent before execution.

## Recommended call

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_append
- body:
  {
    "valueRange": {
      "range": "<sheet_id>!A1",
      "values": [["East China Warehouse", "2026-03", 125000, 98000, 168000, "41.7%"]]
    }
  }
```

Append multiple rows:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_append
- body:
  {
    "valueRange": {
      "range": "<sheet_id>!A1",
      "values": [["A", "B"], ["C", "D"]]
    }
  }
```

## API request details

```
POST /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_append
```

## Parameters (body)

| Parameter | Required | Description |
|------|------|------|
| `valueRange.range` | Yes | Append range: `{sheet_id}!A1:D10`, `A1:D10`, or `{sheet_id}` |
| `valueRange.values` | Yes | 2D-array JSON rows to append |

## Output

Response includes:
- `table_range`
- `updated_range`
- `updated_rows`
- `updated_columns`
- `updated_cells`
- `revision`

## References

- [lark-sheets-read](lark-sheets-read.md)
- [lark-shared](../../lark-shared/SKILL.md)
