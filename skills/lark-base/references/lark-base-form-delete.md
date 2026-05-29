# base +form-delete

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

删除多维表格数据表中的指定表单。**不可逆操作**，执行前务必确认。

## 命令

```js
// 删除表单
lark_api({ tool: 'base', op: 'form-delete', args: {
  base_token: '<base_token>',
  table_id: '<table_id>',
  form_id: '<form_id>'
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token（base_token） |
| `table_id` | 是 | 数据表 ID |
| `form_id` | 是 | 要删除的表单 ID |
| `as` | 否 | 身份：user（默认）\| bot |

## 输出格式

```json
{
  "ok": true,
  "data": {
    "deleted": true,
    "form_id": "vewX58te9D"
  }
}
```

## 工作流

> [!CAUTION]
> 这是**高风险写入操作（删除）** — 执行前必须明确向用户确认，告知此操作不可逆。

1. 先用 `lark_api({ tool: 'base', op: 'form-list' })` 或 `lark_api({ tool: 'base', op: 'form-get' })` 确认目标表单存在
2. 向用户展示将要删除的表单名称和 ID，等待明确确认
3. 执行删除
4. 报告删除结果

## 提示

- 删除前建议先用 `lark_api({ tool: 'base', op: 'form-questions-list' })` 了解表单内容，避免误删
- `form_id` 可通过 `lark_api({ tool: 'base', op: 'form-list' })` 查询

## 参考

- [lark-base](../SKILL.md) — 多维表格全部命令
- [lark-shared](../../lark-shared/SKILL.md) — 认证和全局参数
