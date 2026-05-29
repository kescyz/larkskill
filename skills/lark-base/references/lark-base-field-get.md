# base +field-get

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

获取一个字段的完整配置。

## 推荐命令

```js
lark_api({ tool: 'base', op: 'field-get', args: {
  base_token: 'app_xxx',
  table_id: 'tbl_xxx',
  field_id: 'fld_xxx'
} })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `base_token` | 是 | Base Token |
| `table_id` | 是 | 表 ID 或表名 |
| `field_id` | 是 | 字段 ID 或字段名 |

## API 入参详情

**HTTP 方法和路径：**

```
GET /open-apis/base/v3/bases/:base_token/tables/:table_id/fields/:field_id
```

## 返回重点

- 返回完整字段配置，适合做更新前的基线。

## 坑点

- ⚠️ 重名字段场景下，建议优先传 `fld_xxx`。

## 参考

- [lark-base-field.md](lark-base-field.md) — field 索引页
