# sheets +find (Find cells)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

> **Boundary note:** `sheets +find` is not cloud-drive search. It searches cell values only within one known spreadsheet. If the target spreadsheet is unknown, first use `docs +search` in [`lark-doc`](../../lark-doc/SKILL.md) to locate files, then return to `sheets +info` / `sheets +find`.

Search cell values within a spreadsheet range.

Features:
- `sheet_id` is required
- Case-sensitive by default; use `ignore_case: true` to disable
- Optional regex match

## Recommended call

Search in a specified range (default case sensitive):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/find
- body:
  {
    "find": {
      "search_range": "<sheet_id>!A1:H200",
      "find": "Zhang San"
    }
  }
```

Case-insensitive search:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/find
- body:
  {
    "find": {
      "search_range": "<sheet_id>!H1:H500",
      "find": "Warehouse Management Revenue Report",
      "match_case": false
    }
  }
```

Regex search:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/find
- body:
  {
    "find": {
      "search_range": "<sheet_id>!H1:H500",
      "find": "Warehouse.*Report",
      "regex": true
    }
  }
```

## API request details

```
POST /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/find
```

## Parameters (body)

| Parameter | Required | Description |
|------|------|------|
| `spreadsheet_token` | Yes (path) | Spreadsheet token |
| `sheet_id` | Yes (path) | Sheet ID (use `+info` to obtain) |
| `find.search_range` | No | Range: `{sheet_id}!A1:D200`; omit to search full sheet |
| `find.find` | Yes | Search text or regex |
| `find.match_case` | No | `true` (default) = case-sensitive; `false` = case-insensitive |
| `find.match_entire_cell` | No | Match entire cell only |
| `find.regex` | No | Treat `find` as regex |
| `find.include_formulas` | No | Search formulas too |

## Output

Response includes:
- `find_result.matched_cells`: list of matched cell addresses
- `find_result.matched_formula_cells`: list of formula cells with matches
- `find_result.rows_count`: total matched row count

## References

- [lark-sheets-info](lark-sheets-info.md)
- [lark-shared](../../lark-shared/SKILL.md)
