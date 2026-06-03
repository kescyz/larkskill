
# drive +export

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

把 `doc` / `docx` / `sheet` / `bitable` / `slides` 导出到本地文件。这个 shortcut 内置有限轮询：

- 如果导出任务在轮询窗口内完成，会直接下载到本地目录
- 如果轮询结束仍未完成，会返回 `ticket`、`ready=false`、`timed_out=true` 和 `next_command`
- 后续继续查结果时，改用 `drive +task_result --scenario export`
- 拿到 `file_token` 后，改用 `drive +export-download`

## 命令

```javascript
// 导出新版文档为 pdf，默认保存到当前目录
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<DOCX_TOKEN>',
  doc_type: 'docx',
  file_extension: 'pdf'
} })

// 导出旧版文档为 docx
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<DOC_TOKEN>',
  doc_type: 'doc',
  file_extension: 'docx'
} })

// 导出 docx 为 markdown（Lark-flavored Markdown）
// 注意：markdown 只支持 docx
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<DOCX_TOKEN>',
  doc_type: 'docx',
  file_extension: 'markdown'
} })

// 导出电子表格为 xlsx
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<SHEET_TOKEN>',
  doc_type: 'sheet',
  file_extension: 'xlsx',
  output_dir: './exports'
} })

// 导出幻灯片为 pptx
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<SLIDES_TOKEN>',
  doc_type: 'slides',
  file_extension: 'pptx',
  output_dir: './exports'
} })

// 导出幻灯片为 pdf
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<SLIDES_TOKEN>',
  doc_type: 'slides',
  file_extension: 'pdf',
  output_dir: './exports'
} })

// 指定本地文件名（会按导出格式自动补扩展名）
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<DOCX_TOKEN>',
  doc_type: 'docx',
  file_extension: 'pdf',
  file_name: 'weekly-report.pdf',
  output_dir: './exports'
} })

// 导出电子表格或多维表格为 csv 时，必须传 sub_id
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<SHEET_OR_BITABLE_TOKEN>',
  doc_type: '<sheet|bitable>',
  file_extension: 'csv',
  sub_id: '<SUB_ID>',
  output_dir: './exports'
} })

// 导出多维表格为 .base 快照（只支持 bitable）
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<BITABLE_TOKEN>',
  doc_type: 'bitable',
  file_extension: 'base',
  output_dir: './exports'
} })

// 允许覆盖已存在文件
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<DOCX_TOKEN>',
  doc_type: 'docx',
  file_extension: 'pdf',
  overwrite: true
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--token` | 是 | 源文档 token |
| `--doc-type` | 是 | 源文档类型：`doc` / `docx` / `sheet` / `bitable` / `slides` |
| `--file-extension` | 是 | 导出格式：`docx` / `pdf` / `xlsx` / `csv` / `markdown` / `base` / `pptx` |
| `--sub-id` | 条件必填 | 当 `sheet` / `bitable` 导出为 `csv` 时必填 |
| `--file-name` | 否 | 覆盖默认本地文件名；如未带扩展名，会按 `--file-extension` 自动补齐 |
| `--output-dir` | 否 | 本地输出目录，默认当前目录 |
| `--overwrite` | 否 | 覆盖已存在文件 |

## 关键约束

- `markdown` 只支持 `docx`
- `base` 只支持 `bitable`
- `pptx` 只支持 `slides`
- `slides` 支持导出为 `pptx` / `pdf`
- `sheet` / `bitable` 导出为 `csv` 时必须带 `--sub-id`
- shortcut 内部固定有限轮询：最多 10 次，每次间隔 5 秒
- 轮询超时不是失败；会返回 `ticket`、`timed_out=true` 和 `next_command`，供后续继续查询

## 推荐续跑方式

```javascript
// 第一步：先尝试直接导出
lark_api({ tool: 'drive', op: 'export', args: {
  token: '<DOCX_TOKEN>',
  doc_type: 'docx',
  file_extension: 'pdf',
  file_name: 'weekly-report.pdf'
} })

// 如果返回 ready=false / timed_out=true，再继续查
lark_api({ tool: 'drive', op: 'task_result', args: {
  scenario: 'export',
  ticket: '<TICKET>',
  file_token: '<DOCX_TOKEN>'
} })

// 查到 file_token 后下载
lark_api({ tool: 'drive', op: 'export-download', args: {
  file_token: '<EXPORTED_FILE_TOKEN>',
  file_name: 'weekly-report.pdf',
  output_dir: './exports'
} })
```

## 参考

- [lark-drive](../SKILL.md) -- 云空间（云盘/云存储）全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
