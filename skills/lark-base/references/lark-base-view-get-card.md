# base +view-get-card

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

获取卡片配置。

## 推荐命令

```js
lark_api({ tool: 'base', op: 'view-get-card', args: {
  base_token: 'app_xxx',
  table_id: 'tbl_xxx',
  view_id: 'viw_xxx'
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token |
| `table_id` | 是 | 表 ID 或表名 |
| `view_id` | 是 | 视图 ID 或视图名 |

## API 入参详情

**HTTP 方法和路径：**

```
GET /open-apis/base/v3/bases/:base_token/tables/:table_id/views/:view_id/card
```

## 返回重点

- 返回原始卡片配置。

## 参考

- [lark-base-view.md](lark-base-view.md) — view 索引页
