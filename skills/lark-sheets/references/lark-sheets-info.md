# sheets +info (View spreadsheet/sheet metadata)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Use this to:
- resolve `spreadsheet_token` from URL/token
- list sheets (`sheet_id`, title, row/column count) for follow-up `+read/+write/+find/+export`

## Recommended call

Get spreadsheet metadata (from URL token):
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}
```

List all sheets in the spreadsheet:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets
```

## API request details

```
GET /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}
GET /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets
```

## Parameters

| Parameter | Required | Description |
|------|------|------|
| `spreadsheet_token` | Yes (path) | Spreadsheet token (extracted from URL: `https://example.larksuite.com/sheets/{spreadsheet_token}`) |

## Output

Spreadsheet metadata includes:
- `spreadsheet_token`
- `title`
- `url`

Sheet list includes items with:
- `sheet_id`
- `title`
- `row_count`
- `column_count`

## Wiki URL handling

For wiki URLs, first resolve the real token:
```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces/get_node
- params: { "token": "<wiki_token>" }
```

Then use `node.obj_token` as `spreadsheet_token`.

## References

- [lark-shared](../../lark-shared/SKILL.md)
