---
name: lark-wiki
version: 2.0.0
description: "Lark Wiki via LarkSkill MCP: manage knowledge spaces and document nodes. Create and query knowledge spaces, manage node hierarchies, and organize documents and shortcuts in wiki spaces. Use when users need to find or create docs in a wiki, browse wiki structure, or move/copy nodes."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# wiki (v2)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## spaces

### spaces.get — Get knowledge space info

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces/{space_id}
- as: user
```

### spaces.get_node — Get knowledge space node info

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces/get_node
- params: { "token": "<wiki_node_token>" }
- as: user
```

### spaces.list — Get knowledge space list

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces
- params: { "page_size": 50 }
- as: user
```

## nodes

### nodes.list — Get child node list of a knowledge space

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces/{space_id}/nodes
- params: { "page_size": 50 }
- as: user
```

To list children of a specific node, add `parent_node_token`:

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces/{space_id}/nodes
- params:
  {
    "parent_node_token": "<node_token>",
    "page_size": 50
  }
- as: user
```

### nodes.create — Create a knowledge space node

> Confirm user intent before executing. This is a write operation.

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/wiki/v2/spaces/{space_id}/nodes
- body:
  {
    "obj_type": "doc",
    "parent_node_token": "<parent_token>",
    "node_type": "origin",
    "origin_node_token": "<doc_token>"
  }
- as: user
```

### nodes.copy — Copy a knowledge space node

> Confirm user intent before executing. This is a write operation.

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/wiki/v2/spaces/{space_id}/nodes/{node_token}/copy
- body:
  {
    "target_parent_token": "<target_parent_node_token>",
    "target_space_id": "<target_space_id>"
  }
- as: user
```

## Permission Table

| Operation | Required Scope |
|-----------|---------------|
| `spaces.get` | `wiki:space:read` |
| `spaces.get_node` | `wiki:node:read` |
| `spaces.list` | `wiki:space:retrieve` |
| `nodes.copy` | `wiki:node:copy` |
| `nodes.create` | `wiki:node:create` |
| `nodes.list` | `wiki:node:retrieve` |
