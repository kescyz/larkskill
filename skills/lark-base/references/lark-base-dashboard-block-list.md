# base +dashboard-block-list

> **前置条件：** 先阅读 [lark-base-dashboard.md](lark-base-dashboard.md) 了解整体工作流。

分页列出仪表盘中的所有组件（Block）。常用于：1) 查看仪表盘有哪些组件；2) 获取组件 ID 和类型用于后续编辑/删除。

## 推荐命令

```js
lark_api({ tool: 'base', op: 'dashboard-block-list', args: {
  base_token: 'bascn***************CtadY',
  dashboard_id: 'blkxxx'
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token |
| `dashboard_id` | 是 | 仪表盘 ID |

## 返回示例

```json
{
  "items": [
    {"block_id": "chtxxxxxxxx", "name": "图表", "type": "column"},
    {"block_id": "chtxxxxxxxx", "name": "总利润", "type": "statistics"}
  ],
  "total": 4,
  "has_more": false
}
```

## 返回重点

| 字段 | 说明 |
|------|------|
| `items` | 组件列表，每项包含 `block_id`（ID）、`name`（名称）、`type`（类型）|
| `total` | 组件总数 |
| `has_more` | 是否有更多组件（为 `true` 时需用 `page_token` 继续获取）|

## 坑点

- `dashboard-block-list` 禁止并发调用；批量执行时只能串行。

## 参考

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard 模块指引
