---
name: lark-openapi-explorer
version: 2.0.0
description: "Feishu/Lark native OpenAPI exploration via LarkSkill MCP: discover and invoke any Lark Open API endpoint using lark_api and lark_api_search. Use when user requirements cannot be satisfied by existing lark-* skills, and direct API discovery and invocation are needed."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# OpenAPI Explorer (v2)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first to understand authentication, identity switching, and safety rules.

In V2, `lark_api` IS the generic API explorer — it proxies any Lark Open API endpoint directly. When user requirements **cannot be covered by existing skills**, use `lark_api_search` to discover the endpoint, then `lark_api` to invoke it.

## MCP Tools

### lark_api_search — discover endpoints

Use to find Lark API endpoints by keyword before calling them.

```
Call MCP tool `lark_api_search`:
- query: "create document"
```

Returns a list of matching endpoints with method, path, and description.

### lark_api — invoke endpoint

Use to call any Lark Open API directly.

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/docx/v1/documents
- body:
  {
    "title": "My Document",
    "folder_token": "fld_xxx"
  }
- as: user
```

## Documentation Structure

Feishu OpenAPI docs are organized in a markdown hierarchy for deeper research:

```
llms.txt ← Top-level index, lists all module documentation links
  └─ llms-<module>.txt ← Module documentation with API links
       └─ <api-doc>.md ← Complete description of a single API
```

Documentation entry points:

| Brand | Entry URL |
|-------|----------|
| Feishu | `https://open.feishu.cn/llms.txt` |
| Lark | `https://open.larksuite.com/llms.txt` |

> All documents are written in **Chinese**. If user is speaking English, translate doc content to English in output.

## Discovery Workflow

Follow these steps strictly. **Do not skip steps or guess APIs**:

### Step 1: Confirm existing skill is insufficient

Check whether an existing lark-* skill covers the use case. If yes, use it directly. **Do not continue exploration**.

### Step 2: Search with lark_api_search

```
Call MCP tool `lark_api_search`:
- query: "<user requirement keyword>"
```

If a matching endpoint is returned, proceed to Step 5.

### Step 3: Locate module from top-level index (if lark_api_search is insufficient)

Use WebFetch to get the top-level index and find module links:

```
WebFetch https://open.feishu.cn/llms.txt
  → Extraction question: "List all module document links related to <user requirement keyword>"
```

- Use `open.feishu.cn` for Feishu brand
- Use `open.larksuite.com` for Lark brand
- If user brand is unclear, default to Feishu

### Step 4: Fetch full API specification

Use WebFetch on the concrete API doc:

```
WebFetch https://open.feishu.cn/document/server-docs/.../<api>.md
  → Extract: HTTP method, URL path, path parameters, query parameters, request body fields (name/type/required/description), response fields, required permissions, error codes
```

### Step 5: Call the API

```
Call MCP tool `lark_api`:
- method: GET | POST | PUT | PATCH | DELETE
- path: /open-apis/<path>
- params: { "key": "value" }   ← query params (GET)
- body: { "key": "value" }     ← request body (POST/PUT/PATCH)
- as: user | bot
```

## Output Format

When presenting exploration results, use this structure:

1. **API name and purpose**: one-sentence description
2. **HTTP method and path**: `METHOD /open-apis/...`
3. **Key parameters**: required + common optional
4. **Required permissions**: scope list
5. **MCP call example**: as shown above
6. **Notes**: rate limits, special constraints, etc.

If user speaks English, translate all content to English.

## Safety Rules

- **Write/delete APIs** (POST/PUT/DELETE) require confirming user intent before execution
- Never guess API paths or parameters — confirm from docs or `lark_api_search`
- For sensitive operations (delete chats, remove members, etc.), explain impact scope to user

## Example Scenarios

### Scenario 1: Add members to a group chat

Step 1 — search for the endpoint:

```
Call MCP tool `lark_api_search`:
- query: "add chat members"
```

Step 2 — invoke it:

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/chats/{chat_id}/members
- params: { "member_id_type": "open_id" }
- body: { "id_list": ["ou_xxx", "ou_yyy"] }
- as: bot
```

### Scenario 2: Set group announcement

```
Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/im/v1/chats/{chat_id}/announcement
- body:
  {
    "revision": "0",
    "requests": ["<html>Announcement Content</html>"]
  }
- as: bot
```

## References

- [lark-shared](../lark-shared/SKILL.md) — Authentication and global parameters
- [lark-skill-maker](../lark-skill-maker/SKILL.md) — If you want to solidify a discovered API into a new skill
