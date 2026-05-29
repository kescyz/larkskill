# base +table-delete

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

删除一张表。

## 推荐命令

```js
lark_api({ tool: 'base', op: 'table-delete', args: {
  base_token: 'app_xxx',
  table_id: 'tbl_xxx',
  yes: true
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token |
| `table_id` | 是 | 表 ID 或表名 |

## API 入参详情

**HTTP 方法和路径：**

```
DELETE /open-apis/base/v3/bases/:base_token/tables/:table_id
```

## 返回重点

- 返回 `deleted: true` 以及删除目标的 `table_id / table_name`。

## 工作流

> 这是**高风险写入操作**。需显式传 `yes: true`；如果用户已经明确要求删除且目标明确，直接执行并带上 `yes: true`，不要再补一次确认。

1. 建议先用 `table-list` 或 `table-get` 确认目标。
2. 只有当目标表仍不明确时，才继续追问；如果删除意图和目标都明确，直接执行。

## 坑点

- ⚠️ 高风险不可逆操作。
- ⚠️ 删除场景强烈建议传 `tbl_xxx`，不要传表名。
- ⚠️ 忘记带 `yes: true` 会被拦截。

## 参考

- [lark-base-table.md](lark-base-table.md) — table 索引页
- [lark-base-table-list.md](lark-base-table-list.md) — 列表
