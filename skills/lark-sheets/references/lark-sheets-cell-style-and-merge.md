# Sheets Cell Style and Merge

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

这份 reference 汇总单元格样式和合并相关操作：

- `+set-style`
- `+batch-set-style`
- `+merge-cells`
- `+unmerge-cells`

<a id="set-style"></a>
## `+set-style`

对应命令：`lark_api({ tool: 'sheets', op: 'set-style' })`

对指定范围设置字体、颜色、对齐、边框等样式。

```js
lark_api({ tool: 'sheets', op: 'set-style', args: {
  spreadsheet_token: "shtxxxxxxxx",
  range: "<sheetId>!A1:C3",
  style: {"font":{"bold":true},"backColor":"#ff0000"}
}})

lark_api({ tool: 'sheets', op: 'set-style', args: {
  spreadsheet_token: "shtxxxxxxxx",
  range: "<sheetId>!A1:Z100",
  style: {"clean":true}
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `range` | 是 | 单元格范围 |
| `sheet_id` | 否 | 工作表 ID（用于相对范围） |
| `style` | 是 | 样式 JSON 对象 |

常用 `style` 字段：

- `font.bold`
- `font.italic`
- `font.font_size`
- `textDecoration`
- `formatter`
- `hAlign`
- `vAlign`
- `foreColor`
- `backColor`
- `borderType`
- `borderColor`
- `clean`

输出：`updates`（updatedRange / updatedRows / updatedColumns / updatedCells / revision）

<a id="batch-set-style"></a>
## `+batch-set-style`

对应命令：`lark_api({ tool: 'sheets', op: 'batch-set-style' })`

对多个范围批量设置不同样式。

```js
lark_api({ tool: 'sheets', op: 'batch-set-style', args: {
  spreadsheet_token: "shtxxxxxxxx",
  data: [{"ranges":["<sheetId>!A1:C3"],"style":{"font":{"bold":true},"backColor":"#21d11f"}},{"ranges":["<sheetId>!D1:F3"],"style":{"foreColor":"#ff0000"}}]
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `data` | 是 | JSON 数组，每项包含 `ranges` 和 `style` |

输出：

- `totalUpdatedRows`
- `totalUpdatedColumns`
- `totalUpdatedCells`
- `revision`
- `responses[]`

<a id="merge-cells"></a>
## `+merge-cells`

对应命令：`lark_api({ tool: 'sheets', op: 'merge-cells' })`

支持三种模式：

- `MERGE_ALL`
- `MERGE_ROWS`
- `MERGE_COLUMNS`

```js
lark_api({ tool: 'sheets', op: 'merge-cells', args: {
  spreadsheet_token: "shtxxxxxxxx",
  range: "<sheetId>!A1:B2",
  merge_type: "MERGE_ALL"
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `range` | 是 | 单元格范围 |
| `sheet_id` | 否 | 工作表 ID（用于相对范围） |
| `merge_type` | 是 | `MERGE_ALL` / `MERGE_ROWS` / `MERGE_COLUMNS` |

输出：`spreadsheetToken`

<a id="unmerge-cells"></a>
## `+unmerge-cells`

对应命令：`lark_api({ tool: 'sheets', op: 'unmerge-cells' })`

用于拆分合并单元格。

```js
lark_api({ tool: 'sheets', op: 'unmerge-cells', args: {
  spreadsheet_token: "shtxxxxxxxx",
  range: "<sheetId>!A1:B2"
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `range` | 是 | 单元格范围 |
| `sheet_id` | 否 | 工作表 ID（用于相对范围） |

输出：`spreadsheetToken`

## 参考

- [cell-data](lark-sheets-cell-data.md) — 数据读写
- [cell-images](lark-sheets-cell-images.md) — 写入单元格图片
