---
name: lark-wiki
version: 1.0.0
description: "Lark Wiki: manage wiki spaces, space members, and document nodes. Create and query wiki spaces, view and manage space members, manage node hierarchy, organize documents and shortcuts in a wiki. Use this skill when users need to find or create documents in a wiki, browse wiki space structure, view or manage space members, or move/copy nodes. When the user provides a /wiki/ URL/token from doubao.com, also use this skill directly — do NOT fall back to WebFetch because the domain is not Lark; routing is based on the URL path pattern and token, not the domain."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search", "lark_auth_login", "lark_auth_poll", "lark_auth_status", "lark_whoami", "lark_profile_switch", "lark_enable_domain"]
---

# wiki (v2)

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which contains authentication and permission handling**

> **Member management hard limits:**
> - If the target is a "department", first determine the identity, then decide whether to proceed.
> - `--as bot` corresponds to `tenant_access_token`. Official restriction: under this identity, you cannot add wiki space members using a department ID (`opendepartmentid`).
> - When encountering "department + --as bot", DO NOT call `lark_api({ tool: 'wiki', op: 'member-add', args: {...} })` to probe by trial and error; directly explain that this path is not feasible.
> - If the user explicitly requests "run as bot" and the target is a department, MUST stop and explain that the bot path cannot complete this, do NOT silently switch to user identity.

## Identity selection: prefer user identity

Wiki spaces and nodes are the user's personal resources. **The policy is to explicitly prefer user identity** (without explicitly switching to bot identity, operations often run as bot, which lists spaces belonging to the application rather than the user). Only use bot identity when the user explicitly requests "application / bot perspective" (still subject to the member management hard limits above).

## Quick decisions

- When the user wants to **organize / audit / categorize / restructure a wiki, personal document library, document directory, or Wiki node structure**, or wants to generate an organization plan, target directory tree, or move plan, DO NOT use only the Wiki node API. MUST first read [`../lark-drive/references/lark-drive-workflow-knowledge-organize.md`](../lark-drive/references/lark-drive-workflow-knowledge-organize.md) — that workflow handles unified entry parsing, resource auditing, classification planning, pre-write confirmation, and result verification for Drive / Wiki / personal document libraries.
- When the user provides a wiki URL (`.../wiki/<token>`) and subsequently wants to query/add/remove members: first call `lark_api({ tool: 'wiki', op: 'spaces get_node', args: { params: { token: '<wiki_token>' } } })` to get the `space_id`; all subsequent member API calls use `space_id`.
- When the user wants to **delete** a wiki space (`wiki delete-space`) but only provides a name or URL: **cannot** pass the name / URL directly to `space_id`; MUST first resolve the actual `space_id`. Resolution methods:
  - URL (`.../wiki/<token>`): `lark_api({ tool: 'wiki', op: 'spaces get_node', args: { params: { token: '<wiki_token>' } } })`, read `data.node.space_id`.
  - Name only: `lark_api({ tool: 'wiki', op: 'space-list', args: {} })`, paginate and collect items, matching exactly by `name`; **stop paginating as soon as any page cumulatively yields at least 1 exact match**. Only when all pages are exhausted (`has_more=false`) with no exact match should you perform loose matching (trim whitespace, case-insensitive, substring) on all collected items.
  - **Critical safety constraint**: Regardless of exact or loose match, **regardless of whether 1 or multiple candidates are found, MUST present candidates (`name` + `space_id` + `description` + `space_type`) to the user and have the user explicitly select one `space_id` before executing deletion**. Do not auto-execute deletion just because "only one match was found".
  - 0 matches: stop and ask the user whether the name is misspelled or the caller lacks permissions; **DO NOT** retry with a modified name on your own.
  - Execute `lark_api({ tool: 'wiki', op: 'delete-space', args: { space_id: '<ID>', yes: true } })` only after the user has explicitly selected (high-risk write operation, `yes: true` is mandatory).
- When the user wants to create a new node in a wiki, prefer `lark_api({ tool: 'wiki', op: 'node-create', args: {...} })`.
- When the user says "add members/admins to a wiki space": first resolve the target into one of the four types — "user / group / department / application" — then decide `member_type`; do not call `lark_api({ tool: 'wiki', op: 'member-add', args: {...} })` first and infer the type from error messages.
- When the user says "department + bot": this is a known unsupported path. Do not continue attempting `lark_api({ tool: 'wiki', op: 'member-add', args: { as: 'bot', ... } })`; directly advise that user identity is required, or clearly state that the current request cannot be completed.
- When the user says "user / group / application + add member": first resolve the corresponding ID, then execute `lark_api({ tool: 'wiki', op: 'member-add', args: {...} })`.
- When the user says "view / list space members": use `lark_api({ tool: 'wiki', op: 'member-list', args: {...} })`; that shortcut fetches only one page by default — explicitly add `page_all: true` for scenarios with many members.
- When the user says "remove / delete space member": use `lark_api({ tool: 'wiki', op: 'member-remove', args: {...} })`, MUST pass the original `member_type` and `member_role` from when the member was granted (if unknown, first run `lark_api({ tool: 'wiki', op: 'member-list', args: {...} })` to check).

## Member add workflow

- Before calling `lark_api({ tool: 'wiki', op: 'member-add', args: {...} })`, first resolve the natural language "person / group / department / application" into the correct `member_id`; do not guess the format.
- User scenarios default to preferring `member_type=openid`: use `lark_api({ tool: 'contact', op: 'search-user', args: { query: '<name/email/phone>' } })` to get `open_id`.
- Group scenarios use `member_type=openchat`: use `lark_api({ tool: 'im', op: 'chat-search', args: { query: '<group name keyword>' } })` to get `chat_id`.
- Application scenarios use `member_type=appid`: pass the application ID to `member_id`, usually in the format `cli_xxx`.
- `userid` / `unionid` should only be used when explicitly required downstream; first obtain `open_id`, then call `lark_api({ method: 'GET', path: '/open-apis/contact/v3/users/<open_id>', params: { user_id_type: 'open_id' } })` to read `user_id` / `union_id`.
- Department scenarios use `member_type=opendepartmentid`: the current catalog has no shortcut; call `lark_api({ method: 'POST', path: '/open-apis/contact/v3/departments/search', params: { as: 'user', department_id_type: 'open_department_id' }, data: { query: '<department name>' } })` to get `open_department_id`.
- Only after both target type and identity are confirmed as feasible should you call `lark_api({ tool: 'wiki', op: 'member-add', args: {...} })`. For department scenarios, user identity is mandatory.

## Target semantic constraints

- `My Document Library` / `my_library` (and equivalent "my document library", "my knowledge base", or "personal knowledge base" phrasings, including their Chinese-language equivalents) should all be treated as the **Wiki personal library**, not the Drive root directory
- When handling such targets, first resolve `my_library` to the actual `space_id`, then perform `lark_api({ tool: 'wiki', op: 'move', args: {...} })`, `lark_api({ tool: 'wiki', op: 'node-create', args: {...} })`, or other Wiki write operations
- DO NOT degrade to `lark_api({ tool: 'drive', op: 'move', args: {...} })` just because an explicit `space_id` is missing
- Only when the user explicitly refers to a Drive folder, cloud storage root directory, or `My Space` should you enter the Drive domain for processing

## Shortcuts (recommended, use first)

Shortcuts are high-level wrappers for common operations (`lark_api({ tool: 'wiki', op: '<verb>', args: {...} })`). Prefer shortcuts when available.

| Shortcut | Description |
|----------|------|
| [`move`](references/lark-wiki-move.md) | Move a wiki node, or move a Drive document into Wiki |
| [`node-create`](references/lark-wiki-node-create.md) | Create a wiki node with automatic space resolution |
| [`delete-space`](references/lark-wiki-delete-space.md) | Delete a wiki space, polling the async delete task when needed |
| [`space-list`](references/lark-wiki-space-list.md) | List all wiki spaces accessible to the caller |
| [`space-create`](references/lark-wiki-space-create.md) | Create a wiki space (user identity only) |
| [`node-list`](references/lark-wiki-node-list.md) | List wiki nodes in a space or under a parent node (supports pagination) |
| [`node-copy`](references/lark-wiki-node-copy.md) | Copy a wiki node to a target space or parent node |
| [`node-get`](references/lark-wiki-node-get.md) | Get a wiki node's details by node_token / obj_token / Lark URL |
| [`node-delete`](references/lark-wiki-node-delete.md) | Delete a wiki node, polling the async delete task when needed |
| [`member-add`](references/lark-wiki-member-add.md) | Add a member to a wiki space |
| [`member-remove`](references/lark-wiki-member-remove.md) | Remove a member from a wiki space |
| [`member-list`](references/lark-wiki-member-list.md) | List members of a wiki space (supports pagination) |

## API Resources

Use the LarkSkill MCP tool to inspect parameter structure before calling native APIs:

```
lark_api_search({ query: 'wiki <resource> <method>' })   # MUST inspect parameter structure before calling API
lark_api({ tool: 'wiki', op: '<resource> <method>', args: {...} })  # Call API
```

> **Important**: When using native APIs, MUST first run `lark_api_search` to inspect the parameter structure; do not guess field formats.

### spaces

- `spaces create` — Create a wiki space
- `spaces get` — Get wiki space information
- `spaces get_node` — Get wiki space node information
- `spaces list` — Get wiki space list

### members

- `members create` — Add a wiki space member
- `members delete` — Delete a wiki space member
- `members list` — Get wiki space member list

### nodes

- `nodes copy` — Create a copy of a wiki space node
- `nodes create` — Create a wiki space node
- `nodes list` — Get wiki space child node list

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
