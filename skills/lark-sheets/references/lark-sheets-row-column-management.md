# Sheets Row and Column Management

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

这份 reference 汇总行列结构操作：

- `+add-dimension`
- `+insert-dimension`
- `+update-dimension`
- `+move-dimension`
- `+delete-dimension`

<a id="add-dimension"></a>
## `+add-dimension`

对应命令：`lark_api({ tool: 'sheets', op: 'add-dimension' })`

在工作表末尾追加空行或空列，不影响已有数据。

```js
lark_api({ tool: 'sheets', op: 'add-dimension', args: {
  spreadsheet_token: "shtxxxxxxxx",
  sheet_id: "<sheetId>",
  dimension: "ROWS",
  length: 10
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `sheet_id` | 是 | 工作表 ID |
| `dimension` | 是 | `ROWS` 或 `COLUMNS` |
| `length` | 是 | 追加数量（1-5000） |

输出：`addCount`、`majorDimension`

<a id="insert-dimension"></a>
## `+insert-dimension`

对应命令：`lark_api({ tool: 'sheets', op: 'insert-dimension' })`

在指定位置插入空行或空列，已有数据向下或向右移动。

```js
lark_api({ tool: 'sheets', op: 'insert-dimension', args: {
  spreadsheet_token: "shtxxxxxxxx",
  sheet_id: "<sheetId>",
  dimension: "ROWS",
  start_index: 3,
  end_index: 7
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `sheet_id` | 是 | 工作表 ID |
| `dimension` | 是 | `ROWS` 或 `COLUMNS` |
| `start_index` | 是 | 起始位置（0-indexed） |
| `end_index` | 是 | 结束位置（0-indexed，不含） |
| `inherit_style` | 否 | `BEFORE` 或 `AFTER` |

输出：成功时 `data` 为空对象 `{}`

<a id="update-dimension"></a>
## `+update-dimension`

对应命令：`lark_api({ tool: 'sheets', op: 'update-dimension' })`

更新指定范围行/列的显隐状态和行高/列宽。

```js
lark_api({ tool: 'sheets', op: 'update-dimension', args: {
  spreadsheet_token: "shtxxxxxxxx",
  sheet_id: "<sheetId>",
  dimension: "ROWS",
  start_index: 1,
  end_index: 3,
  visible: false
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `sheet_id` | 是 | 工作表 ID |
| `dimension` | 是 | `ROWS` 或 `COLUMNS` |
| `start_index` | 是 | 起始位置（**1-indexed**，含） |
| `end_index` | 是 | 结束位置（**1-indexed**，含） |
| `visible` | 否 | `--visible=true` 或 `--visible=false` |
| `fixed_size` | 否 | 行高或列宽（像素） |

输出：成功时 `data` 为空对象 `{}`

<a id="move-dimension"></a>
## `+move-dimension`

对应命令：`lark_api({ tool: 'sheets', op: 'move-dimension' })`

将指定范围的行/列移动到目标位置。

```js
lark_api({ tool: 'sheets', op: 'move-dimension', args: {
  spreadsheet_token: "shtxxxxxxxx",
  sheet_id: "<sheetId>",
  dimension: "ROWS",
  start_index: 0,
  end_index: 1,
  destination_index: 4
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `sheet_id` | 是 | 工作表 ID |
| `dimension` | 是 | `ROWS` 或 `COLUMNS` |
| `start_index` | 是 | 源起始位置（0-indexed） |
| `end_index` | 是 | 源结束位置（0-indexed，含） |
| `destination_index` | 是 | 目标位置（0-indexed） |

输出：成功时 `data` 为空对象 `{}`

<a id="delete-dimension"></a>
## `+delete-dimension`

对应命令：`lark_api({ tool: 'sheets', op: 'delete-dimension' })`

删除指定范围的行或列。

```js
lark_api({ tool: 'sheets', op: 'delete-dimension', args: {
  spreadsheet_token: "shtxxxxxxxx",
  sheet_id: "<sheetId>",
  dimension: "ROWS",
  start_index: 3,
  end_index: 7
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `sheet_id` | 是 | 工作表 ID |
| `dimension` | 是 | `ROWS` 或 `COLUMNS` |
| `start_index` | 是 | 起始位置（**1-indexed**，含） |
| `end_index` | 是 | 结束位置（**1-indexed**，含） |

输出：`delCount`、`majorDimension`

## 参考

- [spreadsheet-management](lark-sheets-spreadsheet-management.md#info) — 查看当前工作表信息
- [cell-style-and-merge](lark-sheets-cell-style-and-merge.md) — 调整样式或合并单元格
