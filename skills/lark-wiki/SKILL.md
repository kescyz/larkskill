---
name: lark-wiki
version: 1.0.0
description: "Lark Wiki via LarkSkill MCP: manage knowledge spaces, space members, and document nodes. Use when users need to find or create docs in a wiki, browse space structure, manage members, or move/copy nodes."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# wiki (v2)

## Prerequisites

- LarkSkill MCP server connected (install via `/plugin marketplace add kescyz/larkskill` -> `/plugin install larkskill`, or see https://portal.larkskill.app/setup)
- MCP tools available: `lark_api`, `lark_api_search`
- Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first for auth, identity (user vs bot), and permission handling

> **Member-management hard limits:**
> - If the target is a **department**, decide identity first, then decide whether to continue.
> - The bot identity (`tenant_access_token`) cannot use a department ID (`opendepartmentid`) to add a wiki-space member. This is an official platform limit.
> - When you hit "department + bot identity", DO NOT call the `wiki members create` endpoint to test the error first; state directly that this path is not viable.
> - If the user explicitly requires "run as bot" and the target is a department, you MUST stop and explain the bot path cannot complete the request — do not silently switch to user identity.

## Quick decisions

- User gives a wiki URL (`.../wiki/<token>`) and then wants to query/add/remove members: first call `lark_api` GET `/open-apis/wiki/v2/spaces/get_node` with `params: {"token": "<wiki_token>"}` to retrieve `space_id`; then use `space_id` for all member endpoints.
- User wants to create a new node in a wiki: call `lark_api` POST `/open-apis/wiki/v2/spaces/{space_id}/nodes`. If `space_id` is unknown, resolve it first via `get_node` (from a wiki URL token) or via the spaces `list` endpoint.
- User says "add a member/admin to the wiki": first resolve the target into one of three categories — user / chat / department — then decide `member_type`. DO NOT call the `wiki members create` endpoint first and reverse-engineer the type from the error.
- User says "department + bot": this is a known unsupported path. DO NOT keep trying `wiki members create` under bot identity; state directly that you must switch to user identity, or explicitly tell the user the current request cannot complete.
- User says "user / chat + add member": resolve the corresponding ID first, then call the `wiki members create` endpoint.

## Member-add flow

- Before calling the `wiki members create` endpoint, resolve the natural-language "person / chat / department" into the correct `member_id`. DO NOT guess the format.
- For user scenarios, `member_type=openid` is the default: use `lark_api_search` against the contact domain (search-user shortcut) with `query: "<name/email/phone>"` to fetch `open_id`.
- For chat scenarios, use `member_type=openchat`: use `lark_api_search` against the IM domain (chat-search shortcut) with `query: "<chat name keyword>"` to fetch `chat_id`.
- `userid` / `unionid` are used only when the downstream call explicitly requires them; first obtain `open_id`, then call `lark_api` GET `/open-apis/contact/v3/users/<open_id>` with `params: {"user_id_type": "open_id"}` to read `user_id` / `union_id`.
- For department scenarios, use `member_type=opendepartmentid`: there is no shortcut, so call `lark_api` POST `/open-apis/contact/v3/departments/search` (under user identity) with `params: {"department_id_type": "open_department_id"}` and `data: {"query": "<department name>"}` to fetch `open_department_id`.
- Only after the target type AND the identity have both been confirmed viable, call `lark_api` POST `/open-apis/wiki/v2/spaces/{space_id}/members`. For department scenarios, this means it MUST run under user identity.

## Target semantics constraints

- "My Document Library" / "My Knowledge Base" / "Personal Wiki" / `my_library` should ALL be treated as the **Wiki personal library**, not the Drive root directory.
- For these targets, first resolve `my_library` to its real `space_id`, then run the move flow, the node-create flow, or other Wiki write operations.
- DO NOT degrade to a Drive `move` just because no explicit `space_id` is given.
- Only when the user explicitly says Drive folder, cloud-drive root, or "My Space" (the Drive root) should you enter the Drive domain.

## Shortcuts (recommended — prefer these)

A Shortcut is a high-level wrapper for a common operation. Prefer the shortcut when one exists, invoked via `lark_api({ tool: 'wiki', op: '<verb>', args: { ... } })`.

| Shortcut | Description |
|----------|-------------|
| [`+move`](references/lark-wiki-move.md) | Move a wiki node, or move a Drive document into Wiki |

> Note: a `+node-create` shortcut is documented upstream but is not currently exposed via LarkSkill MCP. Use the raw `lark_api` POST `/open-apis/wiki/v2/spaces/{space_id}/nodes` endpoint instead (see the Intent index below).

Example:

```
lark_api({ tool: 'wiki', op: 'move', args: { space_id: '<space_id>', node_token: '<node_token>', target_parent_token: '<parent_token>' } })
```

For operations without a shortcut (`spaces`, `members`, `nodes` resources below), call `lark_api` with the raw HTTP method + path.

## API resources

> **Important:** when using raw API endpoints, you MUST inspect the request schema first (consult the corresponding `references/*.md` doc) — do not guess field formats for `data` / `params`.

### spaces

- `create` — Create a knowledge space
- `get` — Get knowledge-space info
- `get_node` — Get knowledge-space node info
- `list` — List knowledge spaces

### members

- `create` — Add a knowledge-space member
- `delete` — Remove a knowledge-space member
- `list` — List knowledge-space members

### nodes

- `copy` — Create a copy of a knowledge-space node
- `create` — Create a knowledge-space node
- `list` — List child nodes of a knowledge-space node

## Intent -> MCP call index

| Intent | MCP call |
|--------|----------|
| Resolve wiki URL token | `lark_api` GET `/open-apis/wiki/v2/spaces/get_node` with `params: {"token": "<wiki_token>"}` |
| Create knowledge space | `lark_api` POST `/open-apis/wiki/v2/spaces` |
| Get knowledge-space info | `lark_api` GET `/open-apis/wiki/v2/spaces/{space_id}` |
| List knowledge spaces | `lark_api` GET `/open-apis/wiki/v2/spaces` |
| List child nodes | `lark_api` GET `/open-apis/wiki/v2/spaces/{space_id}/nodes` |
| Create node | `lark_api` POST `/open-apis/wiki/v2/spaces/{space_id}/nodes` |
| Copy node | `lark_api` POST `/open-apis/wiki/v2/spaces/{space_id}/nodes/{node_token}/copy` |
| Move node (or import Drive doc into Wiki) | `lark_api({ tool: 'wiki', op: 'move', args: { ... } })` |
| List members | `lark_api` GET `/open-apis/wiki/v2/spaces/{space_id}/members` |
| Add member | `lark_api` POST `/open-apis/wiki/v2/spaces/{space_id}/members` |
| Remove member | `lark_api` DELETE `/open-apis/wiki/v2/spaces/{space_id}/members/{member_id}` |
| Search user (resolve `open_id`) | `lark_api_search` against contact domain (search-user shortcut) with `query: "<name/email/phone>"` |
| Search chat (resolve `chat_id`) | `lark_api_search` against IM domain (chat-search shortcut) with `query: "<chat name keyword>"` |
| Search department (resolve `open_department_id`) | `lark_api` POST `/open-apis/contact/v3/departments/search` with `data: {"query": "<department name>"}` |

## Permission table

| Method | Required scope |
|--------|----------------|
| `spaces.create` | `wiki:space:write_only` |
| `spaces.get` | `wiki:space:read` |
| `spaces.get_node` | `wiki:node:read` |
| `spaces.list` | `wiki:space:retrieve` |
| `members.create` | `wiki:member:create` |
| `members.delete` | `wiki:member:update` |
| `members.list` | `wiki:member:retrieve` |
| `nodes.copy` | `wiki:node:copy` |
| `nodes.create` | `wiki:node:create` |
| `nodes.list` | `wiki:node:retrieve` |

## Reference docs

- [`references/lark-wiki-move.md`](references/lark-wiki-move.md) — `+move` shortcut details
- [`references/lark-wiki-node-create.md`](references/lark-wiki-node-create.md) — node-create workflow (use raw POST endpoint listed above)
