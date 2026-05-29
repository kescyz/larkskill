# base +dashboard-update

> **前置条件：** 先阅读 [lark-base-dashboard.md](lark-base-dashboard.md) 了解整体工作流。

更新仪表盘名称或主题。

## 推荐命令

```js
lark_api({ tool: 'base', op: 'dashboard-update', args: {
  base_token: 'VwGhb**************fMnod',
  dashboard_id: 'blkxxxxxxx',
  name: '新名称',
  theme_style: 'default'
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token |
| `dashboard_id` | 是 | 仪表盘 ID |
| `name` | 否 | 新名称 |
| `theme_style` | 否 | 主题风格（见下方枚举） |

### theme-style 枚举

| 值 | 说明 |
|------|------|
| `default` | 默认主题 |
| `SimpleBlue` | 简约蓝 |
| `DarkGreen` | 深绿 |
| `summerBreeze` | 夏日微风 |
| `simplistic` | 简洁 |
| `energetic` | 活力 |
| `deepDark` | 深色 |
| `futuristic` | 未来感 |

## 返回示例

```json
{
  "dashboard": {
    "dashboard_id": "blkxxxxxxxxxxxx",
    "name": "新名称",
    "theme": {
      "theme_style": "default"
    }
  },
  "updated": true
}
```

## 返回重点

| 字段 | 说明 |
|------|------|
| `dashboard` | 更新后的仪表盘对象 |
| `dashboard.name` | 新名称（如果更新了）|
| `dashboard.theme.theme_style` | 新主题（如果更新了）|
| `updated` | 是否更新成功 |

> [!CAUTION]
> 这是**写入操作** — 执行前必须向用户确认。

## 参考

- [lark-base-dashboard.md](lark-base-dashboard.md) — dashboard 模块指引
