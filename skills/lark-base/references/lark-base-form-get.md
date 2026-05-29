# base +form-get

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

获取多维表格数据表中指定表单的详情。只读操作，不修改任何数据。

## 命令

```js
// 获取表单详情
lark_api({ tool: 'base', op: 'form-get', args: {
  base_token: '<base_token>',
  table_id: '<table_id>',
  form_id: '<form_id>'
} })

// 使用应用身份（bot）
lark_api({ tool: 'base', op: 'form-get', args: {
  base_token: '<base_token>',
  table_id: '<table_id>',
  form_id: '<form_id>',
  as: 'bot'
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token（base_token） |
| `table_id` | 是 | 数据表 ID |
| `form_id` | 是 | 表单 ID |
| `as` | 否 | 身份：user（默认）\| bot |

## 输出格式

| 字段 | 说明 |
|------|------|
| `id` | 表单 ID |
| `name` | 表单名称 |
| `description` | 表单描述 |

```json
{
  "ok": true,
  "data": {
    "id": "vewX58te9D",
    "name": "用户调研问卷",
    "description": "2024年度用户满意度调研"
  }
}
```

## 提示

- `form_id` 可通过 `lark_api({ tool: 'base', op: 'form-list', args: { base_token: '<token>', table_id: '<id>' } })` 获取

## 参考

- [lark-base](../SKILL.md) — 多维表格全部命令
- [lark-shared](../../lark-shared/SKILL.md) — 认证和全局参数
