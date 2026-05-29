# base +field-list

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

分页列出一张表下的字段。

## 推荐命令

```js
lark_api({ tool: 'base', op: 'field-list', args: {
  base_token: 'app_xxx',
  table_id: 'tbl_xxx',
  offset: 0,
  limit: 100
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token |
| `table_id` | 是 | 表 ID 或表名 |
| `offset` | 否 | 分页偏移，默认 `0` |
| `limit` | 否 | 分页大小，默认 `100`，范围 `1-200` |

## API 入参详情

**HTTP 方法和路径：**

```
GET /open-apis/base/v3/bases/:base_token/tables/:table_id/fields
```

## 返回重点

- 返回字段列表及 `offset / limit / count / total`。

## 坑点

- ⚠️ `field-list` 禁止并发调用；批量列多个表字段时只能串行。

## 参考

- [lark-base-field.md](lark-base-field.md) — field 索引页
