# Sheets Float Images

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

这份 reference 汇总浮动图片相关能力：

- `+media-upload`
- `+create-float-image`
- `+update-float-image`
- `+get-float-image`
- `+list-float-images`
- `+delete-float-image`

<a id="media-upload"></a>
## `+media-upload`

对应命令：`lark_api({ tool: 'sheets', op: 'media-upload' })`

把本地图片上传到指定电子表格的素材空间，返回 `file_token`，供 `+create-float-image` 使用。

```js
lark_api({ tool: 'sheets', op: 'media-upload', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx",
  file: "./image.png"
}})
```

说明：

- 内部调用 `drive/v1/medias/upload_all`
- `>20MB` 自动分片上传
- `--file` 只能是当前工作目录下的相对路径

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `url` | 否 | 电子表格 URL（与 `--spreadsheet-token` 二选一） |
| `spreadsheet_token` | 否 | 表格 token |
| `file` | 是 | 本地图片路径，必须是相对路径 |

输出：`file_token`、`file_name`、`size`、`spreadsheet_token`

<a id="create-float-image"></a>
## `+create-float-image`

对应命令：`lark_api({ tool: 'sheets', op: 'create-float-image' })`

```js
lark_api({ tool: 'sheets', op: 'create-float-image', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx",
  sheet_id: "<sheetId>",
  float_image_token: "boxcnXXXX",
  range: "<sheetId>!A1:A1",
  width: 200,
  height: 150
}})
```

关键规则：

- `--float-image-token` 必须来自 `+media-upload`
- `--range` 必须锚定单个单元格
- `width` / `height` 必须 `>=20`
- `offset-x` / `offset-y` 必须 `>=0`

输出：`float_image`

<a id="update-float-image"></a>
## `+update-float-image`

对应命令：`lark_api({ tool: 'sheets', op: 'update-float-image' })`

```js
lark_api({ tool: 'sheets', op: 'update-float-image', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx",
  sheet_id: "<sheetId>",
  float_image_id: "fi12345678",
  width: 400,
  height: 300,
  offset_y: 20
}})
```

至少需要传一个更新字段：`--range` / `--width` / `--height` / `--offset-x` / `--offset-y`

输出：更新后的 `float_image`

<a id="get-float-image"></a>
## `+get-float-image`

对应命令：`lark_api({ tool: 'sheets', op: 'get-float-image' })`

```js
lark_api({ tool: 'sheets', op: 'get-float-image', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx",
  sheet_id: "<sheetId>",
  float_image_id: "fi12345678"
}})
```

输出：`float_image`

<a id="list-float-images"></a>
## `+list-float-images`

对应命令：`lark_api({ tool: 'sheets', op: 'list-float-images' })`

```js
lark_api({ tool: 'sheets', op: 'list-float-images', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx",
  sheet_id: "<sheetId>"
}})
```

输出：`items[]`

<a id="delete-float-image"></a>
## `+delete-float-image`

对应命令：`lark_api({ tool: 'sheets', op: 'delete-float-image' })`

```js
lark_api({ tool: 'sheets', op: 'delete-float-image', args: {
  url: "https://example.larksuite.com/sheets/shtxxxxxxxx",
  sheet_id: "<sheetId>",
  float_image_id: "fi12345678"
}})
```

输出：`code`、`msg`

## 读取图片内容

上述读接口只返回元数据，不返回图片字节。要读取图片内容，用 `float_image_token` 调：

```js
lark_api({ tool: 'docs', op: 'media-preview', args: {
  token: "<float_image_token>",
  output: "./image.png"
}})
```

## 参考

- [cell-images](lark-sheets-cell-images.md) — 写入到单元格的图片
- [spreadsheet-management](lark-sheets-spreadsheet-management.md#info) — 先获取 `sheet_id`
