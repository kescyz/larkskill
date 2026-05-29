# mail +template-update

> **前置条件：** 先阅读 [`../../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

更新已有的个人邮件模板（全量替换式更新）。支持 `inspect` 只读 projection、`print_patch_template` 打印 patch 骨架、`patch` 结构化 patch、以及扁平的 `set_*` 参数。

> **⚠️ 后端无乐观锁 → last-write-wins**。并发更新可能丢失最近的改动；每次成功更新时会附带一条 warning 提示。

如需创建新模板，使用 [`lark_api({ tool: 'mail', op: 'template-create' })`](./lark-mail-template-create.md)。

## 工作模式

| 入口 | 行为 | 是否写库 |
|------|------|---------|
| `print_patch_template` | 打印 `patch` 的 JSON 骨架 | 否（纯本地） |
| `inspect` | 返回当前模板完整 projection | 否（只 GET） |
| `set_*` / `attach` | 扁平参数合并后 PUT | 是 |
| `patch` | 结构化 patch + 扁平参数合并后 PUT | 是 |

## 命令

```js
// 查看当前状态（不修改）
lark_api({ tool: 'mail', op: 'template-update', as: 'user', args: { template_id: '712345', inspect: true } })

// 打印 patch 骨架
lark_api({ tool: 'mail', op: 'template-update', as: 'user', args: { print_patch_template: true } })

// 用扁平参数改 subject + cc
lark_api({ tool: 'mail', op: 'template-update', as: 'user', args: { template_id: '712345',
  set_subject: '每周五发布',
  set_cc: 'manager@example.com' } })

// 用 patch 做结构化更新（支持 is_plain_text_mode 翻回 false 等 tri-state 场景）
lark_api({ tool: 'mail', op: 'template-update', as: 'user', args: { template_id: '712345',
  patch: { /* ...见下方 patch 字段... */ } } })

// 追加新附件
lark_api({ tool: 'mail', op: 'template-update', as: 'user', args: { template_id: '712345',
  attach: './appendix.pdf' } })
```

## 参数

### 定位

| 参数 | 必填 | 说明 |
|------|------|------|
| `template_id` | 是* | 模板 ID，十进制整数字符串 |
| `mailbox` | 否 | 所属邮箱，默认 `me` |

\* `print_patch_template` 场景下可省略。

### 只读 / 输出

| 参数 | 说明 |
|------|------|
| `inspect` | 只 GET，不修改；返回完整模板 projection |
| `print_patch_template` | 打印 patch 骨架（不访问网络），作为 `patch` 的起点 |

### 扁平 set_* 参数（直接指定新值）

| 参数 | 说明 |
|------|------|
| `set_name` | 替换名称，≤100 字符 |
| `set_subject` | 替换默认主题 |
| `set_template_content` | 替换正文。支持 `<img src="./local.png" />` 相对路径自动上传并改写 |
| `set_template_content_file` | 从文件加载替换正文；与 `set_template_content` 互斥 |
| `set_plain_text` | 标为纯文本模式（置 true）。**不提供不会置 false**；要把 HTML 模板翻回 false，请用 `patch` 的 `{"is_plain_text_mode": false}` |
| `set_to` | 替换默认收件人列表 |
| `set_cc` | 替换默认抄送 |
| `set_bcc` | 替换默认密送 |
| `attach` | 追加非 inline 附件（按书写顺序），不替换已有附件 |

### 结构化 patch

| 参数 | 说明 |
|------|------|
| `patch` | JSON patch 对象。结构同 `print_patch_template` 输出；任何 **非空字段**覆盖当前模板对应字段 |

patch 字段（全部可选，未提供的字段保持当前模板原值）：

```json
{
  "name": "string (≤100 chars, optional)",
  "subject": "string (optional)",
  "template_content": "string (HTML 或纯文本；本地 <img src> 会自动上传)",
  "is_plain_text_mode": "bool (optional) — 显式 true/false 都生效",
  "tos": [{"mail_address": "...", "name": "..."}],
  "ccs": [{"mail_address": "...", "name": "..."}],
  "bccs": [{"mail_address": "...", "name": "..."}]
}
```

## 合并策略

1. `GET` 当前模板完整内容
2. 先应用扁平 `set_*` 参数（非空即覆盖）
3. 再应用 `patch`（非空字段覆盖）——patch 优先级高于扁平参数
4. 重新扫描新正文中的 `<img>` 本地路径，上传到 Drive 并改写为 `cid:`
5. `attach` 追加的新附件以新的 `emlProjectedSize` 独立计算 SMALL/LARGE
6. 附件按 `(id, cid)` 去重后 `PUT` 整个模板

> **所有原有附件保留**：只追加 `attach` 新附件；如需删除已有附件，目前只能通过 `patch` 的 `template_content` 改写正文去除相应 `<img>` 引用，或使用原生 API 整块重写。

## 返回值

成功返回：

```json
{
  "template": {
    "template_id": "712345",
    "name": "周报模板",
    "subject": "每周五发布",
    "template_content": "...",
    "is_plain_text_mode": false,
    "tos": [...],
    "attachments": [...],
    "create_time": "1714000000000"
  }
}
```

`--inspect` 返回同样结构；`--print-patch-template` 返回 patch JSON 骨架。

## 错误码速查

| errno | HTTP | 触发 |
|-------|------|------|
| `15080201 InvalidTemplateName` | 400 | `set_name` 为空或超 100 字符 |
| `15080203 TemplateContentSizeLimit` | 400 | 更新后 `template_content` > 3 MB |
| `15080204 InvalidTemplateID` | 404 | `template_id` 不存在或不属于当前用户 |
| `15080207 InvalidTemplateParam` | 400 | 其他参数错误（含 `template_id` 无法 parseInt） |

## 所需 scope

`mail:user_mailbox.message:modify`, `mail:user_mailbox:readonly`

## 相关

- 创建模板：[`+template-create`](./lark-mail-template-create.md)
- 套用模板发信：在 `+send` / `+draft-create` / `+reply` / `+reply-all` / `+forward` 中使用 `template_id`
- 删除模板（原生 API）：`lark_api({ tool: 'mail', op: 'user_mailbox.templates.delete', args: { user_mailbox_id: 'me', template_id: '<id>' } })`
