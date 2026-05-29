# mail +thread

> **前置条件：** 先阅读 [`../../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

读取指定会话中的所有邮件，按发送时间升序排列。每条邮件结构与 `+message` 相同。

在实现上，每个 `messages[]` 项与 `mail +message` 的构建方式一致：安全元数据字段直接透传，正文/附件辅助字段由 shortcut 派生。每条邮件使用统一的 `attachments[]` 列表，涵盖普通附件和内嵌图片。

本 skill 对应 shortcut `lark_api({ tool: 'mail', op: 'thread' })`，内部调用：
- `GET /open-apis/mail/v1/user_mailboxes/{mailbox}/threads/{thread_id}` — 获取会话中所有邮件的完整内容

## 命令

```js
// 读取完整会话
lark_api({ tool: 'mail', op: 'thread', args: { thread_id: '<thread-id>' } })

// 仅纯文本正文（更小的负载，适合 AI 处理）
lark_api({ tool: 'mail', op: 'thread', args: { thread_id: '<thread-id>', html: false } })

// 指定邮箱
lark_api({ tool: 'mail', op: 'thread', args: { mailbox: 'user@example.com', thread_id: '<thread-id>' } })
```

## 参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `thread_id` | 是 | — | 会话 ID（`thread_id`） |
| `mailbox` | 否 | 当前用户 | 邮箱地址（`user_mailbox_id`） |
| `html` | 否 | true | 是否返回 HTML 正文（`false` 仅返回纯文本，减少带宽） |

## 返回值

成功时返回 `{"ok": true, "data": ...}` 结构，`data` 字段包含：

```json
{
  "thread_id":     "会话 ID",
  "message_count": 2,
  "messages": [
    { "...与 +message 输出结构相同（最早的在前）..." },
    { "......" }
  ]
}
```

顶层字段：

| 字段 | 说明 |
|------|------|
| `thread_id` | `--thread-id` 请求的会话 ID |
| `message_count` | 成功获取的邮件数量 |
| `messages` | 按 `internal_date` 升序排列的邮件列表（最早的在前） |

每个 `messages[]` 项使用与 [`mail +message`](./lark-mail-message.md#返回值) 相同的结构。完整字段列表参见 [`+message` 字段说明](./lark-mail-message.md#字段说明) 和 [`+message` security_level](./lark-mail-message.md#security_level)。

> 注意：使用 `--format json` 获取结构化输出。所有 JSON 输出统一包裹在 `{"ok": true, "data": ...}` 结构中。

## 注意事项

- **JSON 输出可直接使用**，可直接读取，无需额外编码转换。
- JSON 输出中 `messages[].body_html` 里的 `<` / `>` 可能显示为 `\u003c` / `\u003e`（JSON 安全转义，内容不变，`jq -r` 可还原）。
- `mail +thread` 不再在读取会话时获取附件/图片下载 URL。如后续步骤需要 URL，请针对特定的 `message_id` 和 `attachment_ids` 调用原生附件 URL API。
- 与 `+message` 一样，普通附件和内嵌图片都出现在 `messages[].attachments[]` 中，使用同一个 `user_mailbox.message.attachments.download_url` API。
- 查看某条邮件的原始 HTML：从返回结果的 `data.messages[0].body_html` 字段读取。

## 典型场景

### 查看会话时间线 → 生成摘要

```js
// 1. 从某封邮件获取 thread_id（读取 .data.thread_id）
lark_api({ tool: 'mail', op: 'message', args: { message_id: '<id>', html: false } })

// 2. 读取完整会话（仅纯文本）
lark_api({ tool: 'mail', op: 'thread', args: { thread_id: '<thread_id>', html: false } })

// 3. 让 LLM 分析 messages[].body_plain_text 并生成会话摘要
```

### 回复会话中最新一封邮件

```js
// 获取最新一封邮件的 message_id（读取 .data.messages[-1].message_id）
lark_api({ tool: 'mail', op: 'thread', args: { thread_id: '<thread_id>', html: false } })

// 回复
lark_api({ tool: 'mail', op: 'reply', args: { message_id: '<last_message_id>', body: '...' } })
```

## 相关命令

- `lark_api({ tool: 'mail', op: 'message' })` — 读取单封邮件
- `lark_api({ tool: 'mail', op: 'reply' })` — 回复邮件
- `lark_api({ tool: 'mail', op: 'forward' })` — 转发邮件
- `lark_api({ tool: 'mail', op: 'user_mailbox.message.attachments.download_url' })` — 按需获取邮件附件/图片下载 URL
- `lark_api({ tool: 'mail', op: 'user_mailbox.messages.list' })` — 列出收件箱邮件（获取 `thread_id`）
