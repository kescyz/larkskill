# task +tasklist-members

> **Prerequisites:** Please read `../lark-shared/SKILL.md` to understand authentication, global parameters, and security rules.

Manage tasklist members (editors/owners).

## Recommended Commands

```js
// Add a member
lark_api({ tool: 'task', op: 'tasklist-members', args: { tasklist_id: 'tl_xxx', add: 'ou_aaa' } })

// Remove a member
lark_api({ tool: 'task', op: 'tasklist-members', args: { tasklist_id: 'tl_xxx', remove: 'ou_aaa' } })

// Replace all members exactly
lark_api({ tool: 'task', op: 'tasklist-members', args: { tasklist_id: 'tl_xxx', set: 'ou_aaa,ou_bbb' } })
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `tasklist_id` | Yes | The GUID of the tasklist, or a full AppLink URL. |
| `add` | No | Comma-separated list of user `open_id`s to add as members. |
| `remove` | No | Comma-separated list of user `open_id`s to remove from members. |
| `set` | No | Comma-separated list of user `open_id`s to exactly set as members (replaces all existing). |

## Workflow

1. Confirm the tasklist and members to add/remove/set.
2. Execute the command.
3. Report success.

> [!CAUTION]
> This is a **Write Operation** -- You must confirm the user's intent before executing.
