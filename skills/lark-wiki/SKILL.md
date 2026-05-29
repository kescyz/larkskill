---
name: lark-wiki
version: 2.0.0
description: "Operate Lark Wiki via LarkSkill MCP: manage wiki spaces, space members, and document nodes; create/query spaces, view/manage members, and organize the node hierarchy. Also use this skill for a doubao.com `/wiki/` URL/token (route by URL path and token, not domain; do not fall back to WebFetch)."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# wiki (v2)

**CRITICAL - Before starting, MUST read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. It contains authentication and permission handling.**

> **Member management hard limits:**
> - If the target is a "department", determine the identity first, then decide whether to proceed.
> - Bot identity (`tenant_access_token`) cannot add wiki space members using a department ID (`opendepartmentid`).
> - When "department + bot identity" is encountered, DO NOT call `members.create` to try it; directly explain that this path is not viable.
> - If the user explicitly requests "run as bot identity" and the target is a department, MUST stop and explain that the bot path cannot complete it, and do not silently switch to user identity.

## Identity Selection: Prefer User Identity

Wiki spaces and nodes are the user's personal resources. **Prefer user identity for all wiki operations.** Use `lark_profile_switch` to switch profiles; without explicit switching, the default profile applies.

Only use bot identity when the user explicitly requests "application / bot perspective" (still subject to the member management hard limits above).

## Quick Decisions

- User gives a wiki URL (`.../wiki/<token>`) and needs to query/add/remove members: first call
  ```
  lark_api({ tool: 'wiki', op: 'spaces.get_node', args: { token: '<wiki_token>' } })
  ```
  to get `space_id`; use `space_id` for all subsequent member API calls.

- User wants to **delete** a wiki space but only provided a name or URL: **MUST** first resolve the real `space_id`. Resolution:
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
  - Deleting a space is a high-risk async operation: use the `+delete-space` shortcut and require explicit confirmation (`yes: true`). Look it up with `lark_api_search({ query: 'wiki delete-space' })` if the op is not yet exposed by your catalog.

- User wants to create a new node in the wiki, prefer the `+node-create` shortcut (auto space resolution); look it up with `lark_api_search({ query: 'wiki node-create' })`, or fall back to:
  ```
  lark_api({ tool: 'wiki', op: 'nodes.create', args: { space_id: '...', ... } })
  ```

- User says "add member/admin to the wiki": resolve the target into user / group / department first, then determine `member_type`; do not call `members.create` and infer type from the error.

- User says "department + bot": known unsupported path. Prompt that user identity must be used, or clearly state the request cannot be completed.

- User says "user / group + add member": resolve the corresponding ID first, then call `members.create`.

- User says "view / list space members": use `members.list` (or the `+member-list` shortcut for auto-pagination); for many-member scenarios fetch all pages.

- User says "remove / delete a space member": use `members.delete` (or the `+member-remove` shortcut), passing the full original `member_type` and `member_role` used when granting (if unknown, list members first to check).

## Member Addition Flow

- Before adding a member, resolve "person / group / department" to the correct `member_id`.
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
- Only add the member after target type and identity are both confirmed viable. For the department scenario this means it must be user identity. Then:
  ```
  lark_api({ tool: 'wiki', op: 'members.create', args: { space_id: '<space_id>', member_id: '<member_id>', member_type: 'openid', member_role: 'member' } })
  ```

## Target Semantic Constraints

- `My Document Library` / `my wiki` / `personal wiki` / `my_library`: treat as the **Wiki personal library**, not the Drive root directory
- Resolve `my_library` to the real `space_id` first, then execute wiki write operations
- Do not degrade to a Drive move just because an explicit `space_id` is missing
- Only enter Drive domain if the user explicitly mentions a Drive folder, the cloud space (also called cloud drive / cloud storage) root, or "My Space"

## Shortcuts

These high-level shortcuts wrap the raw `spaces.*` / `members.*` / `nodes.*` operations with ID resolution, async-task polling, and flattened output. Discover the exact op name your deployment exposes with `lark_api_search({ query: 'wiki <verb>' })`, then invoke it as `lark_api({ tool: 'wiki', op: '<op>', args: { ... } })`.

| Shortcut | Description | Reference |
|----------|-------------|-----------|
| `+move` | Move a wiki node, or move a Drive document into Wiki | [`references/lark-wiki-move.md`](references/lark-wiki-move.md) |
| `+node-create` | Create a wiki node with automatic space resolution | [`references/lark-wiki-node-create.md`](references/lark-wiki-node-create.md) |
| `+delete-space` | Delete a wiki space, polling the async delete task when needed | [`references/lark-wiki-delete-space.md`](references/lark-wiki-delete-space.md) |
| `+space-list` | List all wiki spaces accessible to the caller | [`references/lark-wiki-space-list.md`](references/lark-wiki-space-list.md) |
| `+space-create` | Create a wiki space (user identity only) | [`references/lark-wiki-space-create.md`](references/lark-wiki-space-create.md) |
| `+node-list` | List wiki nodes in a space or under a parent node (supports pagination) | [`references/lark-wiki-node-list.md`](references/lark-wiki-node-list.md) |
| `+node-copy` | Copy a wiki node to a target space or parent node | [`references/lark-wiki-node-copy.md`](references/lark-wiki-node-copy.md) |
| `+node-get` | Get a wiki node's details by `node_token` / `obj_token` / Lark URL | [`references/lark-wiki-node-get.md`](references/lark-wiki-node-get.md) |
| `+node-delete` | Delete a wiki node, polling the async delete task when needed | [`references/lark-wiki-node-delete.md`](references/lark-wiki-node-delete.md) |
| `+member-add` | Add a member to a wiki space | [`references/lark-wiki-member-add.md`](references/lark-wiki-member-add.md) |
| `+member-remove` | Remove a member from a wiki space | [`references/lark-wiki-member-remove.md`](references/lark-wiki-member-remove.md) |
| `+member-list` | List members of a wiki space (supports pagination) | [`references/lark-wiki-member-list.md`](references/lark-wiki-member-list.md) |

> **`+node-get` argument note**: the node-token argument is `node_token` (the underlying CLI flag was renamed from `--token` to `--node-token`; the old `--token` alias still works but is deprecated). The HTTP/raw form also uses `node_token`. Example call:
> ```
> lark_api({ tool: 'wiki', op: 'spaces.get_node', args: { token: 'wikcnXXXXXXXX' } })
> ```

## API Resources

For available operations and exact op names, use:
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
lark_api({ tool: 'wiki', op: 'members.delete', args: { space_id: '...', member_type: '...', member_id: '...', member_role: '...' } })
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
