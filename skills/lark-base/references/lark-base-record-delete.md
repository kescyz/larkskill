# base +record-delete

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

删除一条或多条记录。

## 推荐命令

```js
lark_api({ tool: 'base', op: 'record-delete', args: {
  base_token: '<base_token>',
  table_id: '<table_id>',
  record_id: '<record_id>',
  yes: true
} })
```

```js
lark_api({ tool: 'base', op: 'record-delete', args: {
  base_token: 'app_xxx',
  table_id: 'tbl_xxx',
  record_id: ['rec_001', 'rec_002'],
  yes: true
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token |
| `table_id` | 是 | 表 ID 或表名 |
| `record_id` | 否 | 与 `json` 二选一；记录 ID，可传数组传多个；这是主推荐用法 |
| `json` | 否 | 与 `record_id` 二选一；脚本/代理场景可传 `{"record_id_list":["rec_xxx"]}` |

## API 入参详情

**HTTP 方法和路径：**

```http
POST /open-apis/base/v3/bases/:base_token/tables/:table_id/records/batch_delete
```

## 返回重点

- 内部统一通过 `batch_delete` 删除记录；单个和多个 `record_id` 使用相同的批量删除输出形态。
- 成功时直接返回接口 `data` 字段内容，通常包含 `record_id_list`。

## 工作流

> 这是**高风险写入操作**。需显式传 `yes: true`；如果用户已经明确要求删除且目标明确，直接执行并带上 `yes: true`，不要再补一次确认。

1. 建议先用 `record-get` 确认目标记录。
2. 只有当目标记录仍不明确时，才继续追问；如果删除意图和目标都明确，直接执行。

## 坑点

- ⚠️ 高风险写操作，删除后不可恢复。
- ⚠️ 忘记带 `yes: true` 会被拦截。

## 参考

- [lark-base-record.md](lark-base-record.md) — record 索引页
