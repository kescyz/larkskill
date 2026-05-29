# Sheets Spreadsheet Management

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

这份 reference 汇总电子表格对象级操作：

- `+create`：创建电子表格
- `+info`：查看电子表格元信息和工作表列表
- `+export`：导出电子表格

<a id="create"></a>
## `+create`

对应命令：`lark_api({ tool: 'sheets', op: 'create' })`

特性：

- 一步创建表格并返回 URL
- 可选 `--headers/--data` 在创建后自动写入第一个工作表的 A1 开始
- `--as bot` 创建成功后，CLI 会尝试为当前 CLI 用户自动授予 `full_access`

```js
// 只创建表格
lark_api({ tool: 'sheets', op: 'create', args: {
  title: "仓库管理营收报表"
}})

// 创建并写入表头 + 初始数据
lark_api({ tool: 'sheets', op: 'create', args: {
  title: "仓库管理营收报表",
  headers: ["仓库","统计月份","入库金额","出库金额","销售收入","毛利率"],
  data: [["华东一仓","2026-03",125000,98000,168000,"41.7%"]]
}})

// 创建到指定文件夹
lark_api({ tool: 'sheets', op: 'create', args: {
  title: "测试表",
  folder_token: "fldbc_xxx"
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `title` | 是 | 表格标题 |
| `folder_token` | 否 | 创建到指定文件夹 |
| `headers` | 否 | 一维数组 JSON，作为表头写入 |
| `data` | 否 | 二维数组 JSON，作为初始数据写入 |

输出：

- `spreadsheet_token`
- `title`
- `url`
- `permission_grant`（仅 `--as bot` 时返回）

<a id="info"></a>
## `+info`

对应命令：`lark_api({ tool: 'sheets', op: 'info' })`

用于：

- 从表格 URL / token 获取 `spreadsheet_token`
- 获取电子表格标题、URL、所有者等元信息
- 列出工作表的 `sheet_id`、标题、行列数、冻结状态等信息

权限说明：

- 该 shortcut 声明了 `sheets:spreadsheet.meta:read` 和 `sheets:spreadsheet:read`，本地 scope preflight 要求两者同时满足
- `spreadsheet` 元信息来自 `spreadsheets/:token` 查询，工作表列表来自额外的 `spreadsheets/:token/sheets/query` 查询

```js
// 传 URL（支持 wiki URL）
lark_api({ tool: 'sheets', op: 'info', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx"
}})

// 传 spreadsheet_token
lark_api({ tool: 'sheets', op: 'info', args: {
  spreadsheet_token: "shtxxxxxxxx"
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一；支持 wiki URL） |
| `spreadsheet_token` | 否 | 电子表格 token |

输出：

- `spreadsheet.spreadsheet.token`
- `spreadsheet.spreadsheet.url`
- `sheets.sheets[]`

<a id="export"></a>
## `+export`

对应命令：`lark_api({ tool: 'sheets', op: 'export' })`

特性：

- 创建导出任务并轮询完成
- 支持导出 `xlsx` 或 `csv`
- 提供 `--output-path` 时自动下载，否则只返回 `file_token`

```js
// 导出 xlsx 并保存到本地
lark_api({ tool: 'sheets', op: 'export', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx",
  file_extension: "xlsx",
  output_path: "./report.xlsx"
}})

// 导出 csv（必须指定 sheet-id）
lark_api({ tool: 'sheets', op: 'export', args: {
  spreadsheet_token: "shtxxxxxxxx",
  file_extension: "csv",
  sheet_id: "<sheetId>",
  output_path: "./report.csv"
}})

// 只返回导出文件 token
lark_api({ tool: 'sheets', op: 'export', args: {
  spreadsheet_token: "shtxxxxxxxx",
  file_extension: "xlsx"
}})
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 电子表格 token |
| `file_extension` | 是 | `xlsx` 或 `csv` |
| `sheet_id` | 否 | 导出 `csv` 时必填 |
| `output_path` | 否 | 保存到本地的路径 |

输出：

- 提供 `--output-path`：`saved_path`、`file_name`、`file_size`
- 不提供 `--output-path`：`file_token`、`file_name`、`file_size`

## 参考

- [sheet-management](lark-sheets-sheet-management.md) — 管理工作表
- [cell-data](lark-sheets-cell-data.md) — 读写单元格数据
- [float-images](lark-sheets-float-images.md) — 上传和管理浮动图片
