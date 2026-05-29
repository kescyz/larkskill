# base +dashboard-block-delete

> **前置条件：** 先阅读 [lark-base-dashboard.md](lark-base-dashboard.md) 了解整体工作流。

删除仪表盘中的一个组件（Block），不可恢复。

## 推荐命令

```js
lark_api({ tool: 'base', op: 'dashboard-block-delete', args: {
  base_token: 'bascn***************CtadY',
  dashboard_id: 'blkxxx',
  block_id: 'chtxxxxxxxx'
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token |
| `dashboard_id` | 是 | 仪表盘 ID |
| `block_id` | 是 | Block ID |

## 返回示例

```json
{
  "block_id": "chtxxxxxxxx",
  "deleted": true
}
```

## 返回重点

| 字段 | 说明 |
|------|------|
| `block_id` | 被删除的组件 ID |
| `deleted` | 是否删除成功 |

> [!CAUTION]
> 这是**写入操作**且**不可逆** — 执行前必须向用户确认。

## 参考

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard 模块指引
