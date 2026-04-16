---
name: lark-shared
version: 2.0.0
description: "LarkSkill MCP shared fundamentals: MCP server connection, identity concepts (user vs bot/tenant), permission scope management, permission denied troubleshooting, rate limits, and safety rules. Activate when users need first-time setup, encounter insufficient permissions, need to switch between user/bot identity, configure scopes, or start using LarkSkill MCP for the first time."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search", "lark_auth_login", "lark_auth_poll", "lark_auth_status", "lark_auth_logout", "lark_profile_list", "lark_profile_switch", "lark_whoami"]
---

# LarkSkill MCP Shared Rules

This skill explains how to operate Feishu/Lark resources via LarkSkill MCP and what to watch out for.

## Connecting MCP to Claude

### Option 1: Local Install (Claude Code / Claude Desktop)

Run in your terminal:

```
npx larkskill install
```

This installs the MCP server and registers it with Claude. Follow the interactive prompts to authenticate your Lark app.

Setup portal and documentation: https://larkskill-portal.pages.dev/setup

### Option 2: Claude.ai Web OAuth

Open https://larkskill-portal.pages.dev/setup and follow the OAuth device flow. Once authorized, the MCP server is available in Claude.ai Cowork sessions.

## MCP Tools Overview

| Tool | Purpose |
|------|---------|
| `lark_api` | Primary proxy — call any Lark Open API |
| `lark_api_search` | Discover endpoints by keyword |
| `lark_enable_domain` | Enable API domain on profile |
| `lark_auth_login` | Start OAuth device flow |
| `lark_auth_poll` | Poll authorization status |
| `lark_auth_status` | Check current auth status |
| `lark_auth_logout` | Log out current profile |
| `lark_profile_list` | List configured profiles |
| `lark_profile_switch` | Switch active profile |
| `lark_whoami` | Show current identity info |

### lark_api Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `method` | Yes | HTTP method: `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| `path` | Yes | API path, e.g. `/open-apis/contact/v3/users/me` |
| `params` | No | Query string parameters (object) |
| `body` | No | Request body (object, for POST/PUT/PATCH) |
| `profile` | No | Named profile to use (default: active profile) |
| `as` | No | Identity to use: `user` or `bot` (default depends on profile) |

## Identity Types

Two identity types are available. Specify via the `as` parameter on `lark_api` calls:

| Identity | `as` value | How to Obtain | Use Case |
|----------|------------|---------------|---------|
| User identity | `as: "user"` | OAuth login via `lark_auth_login` flow | Access the user's own resources (calendar, drive, etc.) |
| Bot identity | `as: "bot"` | Automatic, requires only App ID + App Secret | App-level operations, access bot-owned resources |

### Identity Selection Principles

Behavior differs significantly between bot and user identity. Confirm identity matches the target need:

- **Bots cannot see user resources**: cannot access user calendars, drive documents, email, and other personal resources. Querying schedules with `as: "bot"` returns the bot's own (often empty) calendar.
- **Bots cannot act on behalf of users**: messages are sent in app identity; created docs belong to the bot.
- **Bot permissions**: only require enabling scopes in the Feishu developer console. No user OAuth needed.
- **User permissions**: require both enabled scopes in console and user authorization via `lark_auth_login` flow.

## Authorization Flow (User Identity)

To authorize user identity, use the OAuth device flow:

1. Call `lark_auth_login` with required scopes
2. Present the returned authorization URL to the user
3. Call `lark_auth_poll` to wait for completion
4. Confirm with `lark_auth_status`

```
Call MCP tool `lark_auth_login`:
- scopes: ["calendar:calendar:readonly"]

→ Returns: { "auth_url": "https://..." }

Present auth_url to user. Then:

Call MCP tool `lark_auth_poll`:
- (wait for user to authorize)
```

**Rule**: Specify only the minimum required scopes. Multiple auth calls accumulate scopes incrementally.

## Handling Insufficient Permissions

When permission-related errors occur, apply different solutions based on current identity type.

Error responses include key fields:
- `permission_violations`: missing scopes list
- `console_url`: permission configuration link in the Lark developer console
- `hint`: suggested fix

### Bot Identity (`as: "bot"`)

Provide the `console_url` from the error to the user and guide them to enable scopes in the developer console. Do not attempt OAuth login for bot identity.

### User Identity (`as: "user"`)

Initiate the OAuth device flow with the missing scopes:

```
Call MCP tool `lark_auth_login`:
- scopes: ["<missing_scope>"]
```

Then poll with `lark_auth_poll` and present the auth URL to the user.

## Rate Limits

- Most APIs: 100 requests/minute per app
- Some high-volume APIs (drive, IM): may have lower limits
- When rate limited, wait and retry with exponential backoff
- Batch APIs are preferred over looping single-record calls

## Safety Rules

- **Never output secrets** (App Secret, access tokens) in plaintext.
- **Always confirm user intent before write/delete operations**.
- For risky requests, describe the intended operation to the user and ask for confirmation before calling `lark_api`.
- Identity (`as: "user"` vs `as: "bot"`) must match the resource access pattern.
