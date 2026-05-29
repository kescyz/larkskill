# Sheets Cell Data

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

这份 reference 汇总单元格数据操作：

- `+read`
- `+write`
- `+append`
- `+find`
- `+replace`

<a id="read"></a>
## `+read`

对应命令：`lark_api({ tool: 'sheets', op: 'read' })`

内置能力：

- 支持 `--url` / `--spreadsheet-token` 二选一（URL 支持 wiki）
- 若已传 `--sheet-id`，`--range` 可写 `A1:D10` 或 `C2`
- 默认最多返回 200 行

```js
lark_api({ tool: 'sheets', op: 'read', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx",
  range: "<sheetId>!A1:H20"
}})

lark_api({ tool: 'sheets', op: 'read', args: {
  spreadsheet_token: "shtxxxxxxxx",
  sheet_id: "<sheetId>",
  range: "C2"
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `range` | 否 | `<sheetId>!A1:D10`、`A1:D10` / `C2` 或 `<sheetId>` |
| `sheet_id` | 否 | 工作表 ID |
| `value_render_option` | 否 | `ToString` / `FormattedValue` / `Formula` / `UnformattedValue` |

输出：

- `range`
- `values`
- `truncated`
- `total_rows`

<a id="write"></a>
## `+write`

对应命令：`lark_api({ tool: 'sheets', op: 'write' })`

用于覆盖写入一个矩形区域。

```js
lark_api({ tool: 'sheets', op: 'write', args: {
  spreadsheet_token: "shtxxxxxxxx",
  range: "<sheetId>!A1:B2",
  values: [["name","age"],["alice",18]]
}})

lark_api({ tool: 'sheets', op: 'write', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx",
  sheet_id: "<sheetId>",
  range: "C2",
  values: [["hello"]]
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `range` | 否 | 写入范围；可用相对范围或 `<sheetId>` |
| `sheet_id` | 否 | 工作表 ID |
| `values` | 是 | 二维数组 JSON |

输出：

- `updated_range`
- `updated_rows`
- `updated_columns`
- `updated_cells`
- `revision`

<a id="append"></a>
## `+append`

对应命令：`lark_api({ tool: 'sheets', op: 'append' })`

用于向工作表末尾追加行。

```js
lark_api({ tool: 'sheets', op: 'append', args: {
  spreadsheet_token: "shtxxxxxxxx",
  range: "<sheetId>!A1",
  values: [["华东一仓","2026-03",125000,98000,168000,"41.7%"]]
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `range` | 否 | 追加范围：支持 `<sheetId>`、完整范围、相对范围 |
| `sheet_id` | 否 | 工作表 ID |
| `values` | 是 | 二维数组 JSON |

输出：

- `table_range`
- `updated_range`
- `updated_rows`
- `updated_columns`
- `updated_cells`
- `revision`

<a id="find"></a>
## `+find`

对应命令：`lark_api({ tool: 'sheets', op: 'find' })`

只在一个已知 spreadsheet 内查找单元格内容，不是云空间（云盘/云存储）搜索。

```js
lark_api({ tool: 'sheets', op: 'find', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx",
  sheet_id: "<sheetId>",
  find: "张三",
  range: "A1:H200"
}})

lark_api({ tool: 'sheets', op: 'find', args: {
  spreadsheet_token: "shtxxxxxxxx",
  sheet_id: "<sheetId>",
  find: "仓库管理营收报表",
  ignore_case: true
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `sheet_id` | 是 | 工作表 ID |
| `find` | 是 | 查找内容 |
| `range` | 否 | 范围；不填则搜索整个工作表 |
| `ignore_case` | 否 | 不区分大小写 |
| `match_entire_cell` | 否 | 完全匹配单元格 |
| `search_by_regex` | 否 | 使用正则 |
| `include_formulas` | 否 | 搜索公式 |

输出：

- `matched_cells`
- `matched_formula_cells`
- `rows_count`

<a id="replace"></a>
## `+replace`

对应命令：`lark_api({ tool: 'sheets', op: 'replace' })`

在指定范围内查找并替换单元格内容。

```js
lark_api({ tool: 'sheets', op: 'replace', args: {
  spreadsheet_token: "shtxxxxxxxx",
  sheet_id: "<sheetId>",
  find: "hello",
  replacement: "world"
}})

lark_api({ tool: 'sheets', op: 'replace', args: {
  spreadsheet_token: "shtxxxxxxxx",
  sheet_id: "<sheetId>",
  find: "\\d{4}-\\d{2}-\\d{2}",
  replacement: "DATE",
  search_by_regex: true
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `sheet_id` | 是 | 工作表 ID |
| `find` | 是 | 搜索文本 |
| `replacement` | 是 | 替换文本 |
| `range` | 否 | 搜索范围，不传则搜索整个工作表 |
| `match_case` | 否 | 区分大小写 |
| `match_entire_cell` | 否 | 匹配整个单元格 |
| `search_by_regex` | 否 | 使用正则 |
| `include_formulas` | 否 | 在公式中搜索 |

输出：

- `replace_result.matched_cells`
- `replace_result.matched_formula_cells`
- `replace_result.rows_count`

## 参考

- [spreadsheet-management](lark-sheets-spreadsheet-management.md#info) — 先获取 `sheet_id`
- [dropdown](lark-sheets-dropdown.md#set-dropdown) — 写入 `multipleValue` 前先设置下拉列表
- [formula](lark-sheets-formula.md) — 公式写入规则
