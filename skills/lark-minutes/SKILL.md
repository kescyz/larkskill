---
name: lark-minutes
version: 2.0.0
description: "Lark Minutes via LarkSkill MCP: retrieve basic minutes metadata (title, cover, duration) and related AI outputs (summary, todo items, chapters), get media download links. Lark Minutes URL format: http(s)://<host>/minutes/<minute-token>"
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# minutes (v2)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## Core Concepts

- **Minute Token (`minute_token`)**: Unique identifier of a minutes record. Extract from the minutes URL — the final path segment before any query string. Example: from `https://*.feishu.cn/minutes/obcnq3b9jl72l83w4f14xxxx`, the token is `obcnq3b9jl72l83w4f14xxxx`.

## Usage Guide

1. **Extract token**:
   - Only `minute_token` is required.
   - If the URL contains extra query parameters (e.g. `?xxx`), extract only the final path segment as the token.
   - Example: extract `obc123456` from `https://domain.feishu.cn/minutes/obc123456?project=xxx`.

2. **Get minutes info** — core fields returned:
   - `title`: meeting title
   - `cover`: video/audio cover URL
   - `duration`: meeting duration (milliseconds)
   - `owner_id`: owner ID
   - `url`: minutes link

## Typical Scenarios

### Query Minutes Metadata

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/minutes/v1/minutes/{minute_token}
- params: { "minute_token": "obcn***************" }
- as: user
```

### Query Minutes Content Artifacts

This skill only provides **basic minutes metadata** (title, cover, duration). To get minutes **content artifacts** (transcript, AI summary, todos, chapters), use the [lark-vc notes operation](../lark-vc/references/lark-vc-notes.md):

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/minutes/v1/minutes/{minute_token}
- params: { "minute_token": "obcnhijv43vq6bcsl5xasfb2" }
- as: user
```

Then use the returned artifact links to fetch content.

- If the user does not specify what to retrieve from minutes, default to querying both basic metadata and linked note artifacts.
- If the user does not explicitly request reading artifact contents (transcript, summary, todos, chapters), show artifact links only — no need to read the full content.

## Operations

| Operation | Reference |
|-----------|-----------|
| [`download`](references/lark-minutes-download.md) | Get media download link for a minute (audio/video) |

## Permission Table

| Operation | Required Scope |
|-----------|---------------|
| `minutes.get` | `minutes:minutes:readonly` |
| `download` | `minutes:minutes.media:export` |
