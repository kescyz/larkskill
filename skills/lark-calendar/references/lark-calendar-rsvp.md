# calendar +rsvp

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

回复指定的日程，更新当前用户的 RSVP 状态（接受、拒绝或待定）。

需要的scopes: ["calendar:calendar.event:reply"]

## 命令

```js
// 回复日程为接受 (使用主日历)
lark_api({ tool: 'calendar', op: 'rsvp', args: { event_id: 'evt_xxx', rsvp_status: 'accept' } })

// 回复日程为拒绝
lark_api({ tool: 'calendar', op: 'rsvp', args: { event_id: 'evt_xxx', rsvp_status: 'decline' } })

// 回复日程为待定
lark_api({ tool: 'calendar', op: 'rsvp', args: { event_id: 'evt_xxx', rsvp_status: 'tentative' } })

// 指定其他日历下的日程
lark_api({ tool: 'calendar', op: 'rsvp', args: { calendar_id: 'cal_xxx', event_id: 'evt_xxx', rsvp_status: 'accept' } })
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `event_id` | **是** | 日程 ID |
| `rsvp_status` | **是** | 回复状态，可选值：`accept` (接受), `decline` (拒绝), `tentative` (待定) |
| `calendar_id` | 否 | 日历 ID（省略则使用主日历） |

## 提示

- 只能回复你被邀请的日程。
- 调用前通常需要通过 `+agenda` 等命令获取到具体的 `event_id`。

## 参考

- [lark-calendar](../SKILL.md) -- 日历全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
