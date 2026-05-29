# +get-user

按 ID 取用户基本信息(姓名等)。

```js
// 取自己
lark_api({ tool: 'contact', op: 'get-user', args: { as: 'user' } })

// bot 按 ID 取他人
lark_api({ tool: 'contact', op: 'get-user', args: { user_id: 'ou_xxx', as: 'bot' } })

// 按 union_id / user_id 取(默认 open_id)
lark_api({ tool: 'contact', op: 'get-user', args: { user_id: '<id>', user_id_type: 'union_id', as: 'bot' } })
```

## 注意事项

- **user 身份按 ID 取他人请用 `lark_api({ tool: 'contact', op: 'search-user' })` 的 `user_ids` 参数**,字段比本命令多(部门 / 邮箱 / 是否激活等)。本命令的 user 模式只回很少字段。
- **`as: 'bot'` 必须传 `user_id`**:不传会直接报错(只有 user 身份能省略 `user_id` 取自己)。
