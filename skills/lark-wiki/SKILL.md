---
name: lark-wiki
version: 2.0.0
description: "Use this skill when operating Lark Wiki via LarkSkill MCP: manage wiki spaces, space members, and document nodes. Create and query wiki spaces, view and manage space members, manage node hierarchy, and organize documents and shortcuts in the wiki."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# wiki (v2)

**CRITICAL — Before starting, MUST read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. It contains authentication and permission handling.**

> **Member management hard limits:**
> - If the target is a "department", determine the identity first, then decide whether to proceed.
> - Bot identity (`tenant_access_token`) cannot add wiki space members using a department ID (`opendepartmentid`).
> - When "department + bot identity" is encountered, DO NOT call `lark_api` for `wiki members create` to try it; directly explain that this path is not viable.
> - If the user explicitly requests "run as bot identity" and the target is a department, MUST stop and explain that the bot path cannot complete it — do not silently switch to user identity.

## Identity Selection: Prefer User Identity

Wiki spaces and nodes are the user's personal resources. **Prefer user identity for all wiki operations.** Use `lark_profile_switch` to switch profiles; without explicit switching, the default profile applies.

Only use bot identity when the user explicitly requests "application / bot perspective" (still subject to the member management hard limits above).

## Quick Decisions

- User gives a wiki URL (`.../wiki/<token>`) and needs to query/add/delete members: first call
  ```
  lark_api({ tool: 'wiki', op: 'spaces.get_node', args: { token: '<wiki_token>' } })
  ```
  to get `space_id`; use `space_id` for all subsequent member API calls.

- User wants to **delete** a wiki space (`+delete-space`) but only provided a name or URL: **MUST** first resolve the real `space_id`. Resolution:
  - URL (`.../wiki/<token>`):
    ```
    lark_api({ tool: 'wiki', op: 'spaces.get_node', args: { token: '<wiki_token>' } })
    ```
    Read `data.node.space_id`.
  - Only know the name: paginate through
    ```
    lark_api({ tool: 'wiki', op: 'spaces.list', args: { ... } })
    ```
    Stop as soon as at least 1 exact `name` match is found. Only do loose matching after exhausting all pages with no exact match.
  - **Key safety constraint**: regardless of 1 or multiple matches, MUST list candidates (`name` + `space_id` + `description` + `space_type`) to the user and let them explicitly select one `space_id` before executing. Never auto-delete on a single match.
  - 0 matches: stop and ask the user whether the name is misspelled or caller lacks permissions; do NOT retry with a modified name.
  - After selection:
    ```
    lark_api({ tool: 'wiki', op: '+delete-space', args: { space_id: '<ID>', yes: true } })
    ```

- User wants to create a new node in the wiki, prefer:
  ```
  lark_api({ tool: 'wiki', op: '+node-create', args: { ... } })
  ```

- User says "add member/admin to the wiki": resolve the target into user / group / department first, then determine `member_type`; do not call members.create and infer type from the error.

- User says "department + bot": known unsupported path. Prompt that `--as user` must be used, or clearly state the request cannot be completed.

- User says "user / group + add member": resolve the corresponding ID first, then call members.create.

## Member Addition Flow

- Before calling `wiki members.create`, resolve "person / group / department" to the correct `member_id`.
- User scenarios default to `member_type=openid`:
  ```
  lark_api({ tool: 'contact', op: '+search-user', args: { query: '<name/email/phone>' } })
  ```
  Get `open_id`.
- Group scenarios use `member_type=openchat`:
  ```
  lark_api({ tool: 'im', op: '+chat-search', args: { query: '<group name keyword>' } })
  ```
  Get `chat_id`.
- `userid` / `unionid` only when explicitly required downstream; get `open_id` first, then:
  ```
  lark_api({ method: 'GET', path: '/open-apis/contact/v3/users/<open_id>', params: { user_id_type: 'open_id' } })
  ```
- Department scenarios use `member_type=opendepartmentid`:
  ```
  lark_api({ method: 'POST', path: '/open-apis/contact/v3/departments/search', params: { department_id_type: 'open_department_id' }, data: { query: '<department name>' } })
  ```
  Must use user identity.
- Only call `wiki members.create` after target type and identity are both confirmed viable.

## Target Semantic Constraints

- `My Document Library` / `my wiki` / `personal wiki` / `my_library` → treat as **Wiki personal library**, not Drive root directory
- Resolve `my_library` to the real `space_id` first, then execute wiki write operations
- Do not degrade to `drive +move` just because an explicit `space_id` is missing
- Only enter Drive domain if the user explicitly mentions Drive folder, cloud space root, or "My Space"

## Shortcuts

| Shortcut | MCP call |
|----------|------|
| Move a wiki node | `lark_api({ tool: 'wiki', op: '+move', args: { node_token: '...', ... } })` |
| Create a wiki node | `lark_api({ tool: 'wiki', op: '+node-create', args: { space_id: '...', ... } })` |
| Delete a wiki space | `lark_api({ tool: 'wiki', op: '+delete-space', args: { space_id: '...', yes: true } })` |
| List all wiki spaces | `lark_api({ tool: 'wiki', op: '+space-list', args: { ... } })` |
| Create a wiki space | `lark_api({ tool: 'wiki', op: '+space-create', args: { name: '...', ... } })` |
| List wiki nodes | `lark_api({ tool: 'wiki', op: '+node-list', args: { space_id: '...', ... } })` |
| Copy a wiki node | `lark_api({ tool: 'wiki', op: '+node-copy', args: { node_token: '...', target_space_id: '...' } })` |
| Get wiki node details | `lark_api({ tool: 'wiki', op: '+node-get', args: { node_token: '...' } })` |
| Delete a wiki node | `lark_api({ tool: 'wiki', op: '+node-delete', args: { node_token: '...' } })` |

For full parameter reference, see: [`references/lark-wiki-move.md`](references/lark-wiki-move.md), [`references/lark-wiki-node-create.md`](references/lark-wiki-node-create.md), etc.

## API Resources

For available operations, use:
```
lark_api_search({ query: 'wiki <resource>' })
```

### spaces
```
lark_api({ tool: 'wiki', op: 'spaces.create', args: { ... } })
lark_api({ tool: 'wiki', op: 'spaces.get', args: { space_id: '...' } })
lark_api({ tool: 'wiki', op: 'spaces.get_node', args: { token: '...' } })
lark_api({ tool: 'wiki', op: 'spaces.list', args: { ... } })
```

### members
```
lark_api({ tool: 'wiki', op: 'members.create', args: { space_id: '...', member_type: '...', member_id: '...', member_role: '...' } })
lark_api({ tool: 'wiki', op: 'members.delete', args: { space_id: '...', member_type: '...', member_id: '...' } })
lark_api({ tool: 'wiki', op: 'members.list', args: { space_id: '...' } })
```

### nodes
```
lark_api({ tool: 'wiki', op: 'nodes.copy', args: { space_id: '...', node_token: '...', ... } })
lark_api({ tool: 'wiki', op: 'nodes.create', args: { space_id: '...', ... } })
lark_api({ tool: 'wiki', op: 'nodes.list', args: { space_id: '...' } })
```

## Permissions

| Method | Required scope |
|------|-----------|
| `spaces.create` | `wiki:space:write_only` |
| `spaces.get` | `wiki:space:read` |
| `spaces.get_node` | `wiki:node:read` |
| `spaces.list` | `wiki:space:retrieve` |
| `members.create` | `wiki:member:create` |
| `members.delete` | `wiki:member:update` |
| `members.list` | `wiki:member:retrieve` |
| `nodes.copy` | `wiki:node:copy` |
| `nodes.move` | `wiki:node:move` |
| `nodes.create` | `wiki:node:create` |
| `nodes.list` | `wiki:node:retrieve` |
