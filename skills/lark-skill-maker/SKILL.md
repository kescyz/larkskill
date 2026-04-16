---
name: lark-skill-maker
version: 2.0.0
description: "Create a LarkSkill V2 plugin (MCP workflow skill). Use when users need to encapsulate Lark API operations into reusable skills that call lark_api MCP tools — packaging atomic APIs or orchestrating multi-step processes."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# Skill Maker (v2)

Create a new LarkSkill V2 plugin. A plugin = a `SKILL.md` file (and optional `references/*.md` files) that teaches Claude to call `lark_api` MCP tool to complete tasks.

## Plugin Structure

Plugins live in the `kescyz/larkskill` monolith under `skills/<domain>/`:

```
skills/
└── lark-<name>/
    ├── SKILL.md              ← Main skill file (required)
    └── references/           ← Optional: one file per operation
        ├── lark-<name>-<op1>.md
        └── lark-<name>-<op2>.md
```

See the canonical pilot for reference: `skills/lark-base/`

## Research: Finding the Right API

### Step 1: Search with lark_api_search

```
Call MCP tool `lark_api_search`:
- query: "<domain or operation keyword>"
```

### Step 2: Discover via Feishu docs (if needed)

Use WebFetch on the official docs hierarchy:

```
WebFetch https://open.feishu.cn/llms.txt
  → find relevant module link

WebFetch https://open.feishu.cn/llms-docs/zh-CN/llms-<module>.txt
  → find specific API doc link

WebFetch <api-doc-url>
  → extract: method, path, params, body, response, scopes, error codes
```

### Step 3: Prototype with lark_api

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/vc/v1/rooms
- params: { "page_size": "50" }
- as: bot
```

Use this process to determine which APIs, parameters, and scopes are required.

## SKILL.md Template

```markdown
---
name: lark-<name>
version: 2.0.0
description: "<Function description>. Use when the user needs <trigger scenario>."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# <title>

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## Operations

| Operation | Reference |
|-----------|-----------|
| [`<op>`](references/lark-<name>-<op>.md) | Description |

## Permission Table

| Operation | Required Scope |
|-----------|---------------|
| `<op>` | `scope:name` |
```

## Reference File Template (`references/lark-<name>-<op>.md`)

```markdown
# <name> — <op>

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first.

Brief description of the operation.

## MCP tool call

\```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/xxx/v1/yyy
- body:
  {
    "field": "value"
  }
- as: user
\```

## Parameters (body / params)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `field` | Yes | Description |

## Response highlights

- Key fields returned and their meaning.

## References

- [lark-<name>](../SKILL.md)
- [lark-shared](../../lark-shared/SKILL.md)
```

## Key Principles

- **description determines the trigger** — include function keywords + "Use when the user needs..."
- **Authentication** — specify required scopes; guide user through `lark_auth_login` MCP tool flow for user identity
- **Identity** — specify `as: "user"` or `as: "bot"` per operation based on resource access pattern
- **Security** — confirm user intent before write operations; describe impact before executing destructive calls
- **Orchestration** — document data flow between steps, failure handling, and which steps can run in parallel
- **No guessing** — all API paths and parameters must come from `lark_api_search` or official docs, never guessed

## References

- [lark-openapi-explorer](../lark-openapi-explorer/SKILL.md) — discover API endpoints before building a skill
- [lark-base](../lark-base/SKILL.md) — canonical pilot showing V2 skill structure at scale
- [lark-shared](../lark-shared/SKILL.md) — authentication and global parameters
