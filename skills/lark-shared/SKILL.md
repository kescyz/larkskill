---
name: lark-shared
version: 2.0.0
description: "LarkSkill MCP shared foundation: user/bot identity model, `lark_auth_login` flow, profile switching, scope management, Permission denied handling, safety rules. Use when the user first logs in, hits a permission error, switches identity, or any sibling lark-* skill needs auth context."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_auth_login", "lark_auth_poll", "lark_auth_status", "lark_auth_logout", "lark_profile_list", "lark_profile_switch", "lark_whoami", "lark_enable_domain"]
---

# lark-shared

Shared foundation for every LarkSkill MCP domain skill. Read this first before invoking any `lark_api` / `lark_api_search` call from a sibling skill (lark-base, lark-calendar, lark-mail, etc.).

## Prerequisites

- LarkSkill MCP server connected (install via `/plugin marketplace add kescyz/larkskill` -> `/plugin install larkskill`, or see https://portal.larkskill.app/setup)
- Core MCP tools available: `lark_auth_login`, `lark_auth_poll`, `lark_auth_status`, `lark_auth_logout`, `lark_profile_list`, `lark_profile_switch`, `lark_whoami`, `lark_enable_domain`

## First-time setup

App configuration is handled by the marketplace install flow — there is no MCP equivalent of `lark-cli config init`. Once `/plugin install larkskill` completes (or the user follows the setup prompt at https://portal.larkskill.app/setup), the MCP server is ready and bot identity is available immediately. User identity still requires an explicit `lark_auth_login` (see below).

## Authentication

### Identity types

Two identity types are exposed by the LarkSkill MCP server:

| Identity | How to obtain | Use case |
|------|---------|---------|
| user identity | `lark_auth_login` (OAuth flow, then `lark_auth_poll`) | Access the user's own resources (calendar, drive, mail, etc.) |
| bot (app) identity | Automatic — provided by the connected app's `appId` + `appSecret` | App-level operations, accessing the bot's own resources |

Use `lark_whoami` to inspect the current identity at any time. The tool response includes an `identity` field (`user` or `bot`).

### Identity selection principles

Bot and user behave very differently — confirm the identity matches the target need:

- **Bot cannot see user resources**: cannot access the user's calendar, drive docs, mailbox, or other personal resources. For example, querying schedules under bot identity returns the bot's own (empty) calendar.
- **Bot cannot act on behalf of the user**: messages are sent under the app name, created docs are owned by the bot.
- **Bot permissions**: only need scope enabled in the Lark Developer Console, no login required.
- **User permissions**: scope enabled in the console + user authorization via `lark_auth_login`; both layers must be satisfied.

Switch the active profile (when multiple identities are configured) via `lark_profile_switch`. List configured profiles via `lark_profile_list`.

### Permission denied handling

When encountering permission-related errors, **adopt different solutions based on the current identity type**.

The error response contains key fields:
- `permission_violations`: lists missing scopes (N-of-1)
- `console_url`: link to the Lark Developer Console for permission configuration
- `hint`: suggested fix tool call

#### Bot identity

Provide the `console_url` from the error to the user, guiding them to enable scopes in the console. **DO NOT** call `lark_auth_login` for a bot.

#### User identity

Call `lark_auth_login` with the missing scope (or the parent business domain). The tool returns an authorization URL plus a poll token; relay the URL to the user, then poll completion via `lark_auth_poll`.

```
Call MCP tool `lark_auth_login`:
- args: { "scope": "<missing_scope>" }       # Authorize by specific scope (recommended, follows least-privilege principle)

Call MCP tool `lark_auth_login`:
- args: { "domain": "<domain>" }             # Or authorize by business domain
```

**Rule**: `lark_auth_login` MUST specify a range (`domain` or `scope`). Multiple logins accumulate scopes (incremental authorization).

#### Agent-driven authentication (recommended)

When you, as an AI agent, need to help the user complete authentication:

1. Call `lark_auth_login` with the desired `scope` — the response includes an authorization URL and a poll token.
2. Send the authorization URL to the user.
3. Poll completion with `lark_auth_poll` (using the token from step 1) until status is `completed` or `expired`.

```
Call MCP tool `lark_auth_login`:
- args: { "scope": "calendar:calendar:readonly" }

Call MCP tool `lark_auth_poll`:
- args: { "token": "<token from auth_login response>" }
```

### Enabling a domain

Some domains are gated and must be explicitly enabled before their `lark_api` ops resolve. If a sibling skill returns a "domain not enabled" error, call `lark_enable_domain` with the domain name (for example `base`, `calendar`, `mail`).

```
Call MCP tool `lark_enable_domain`:
- args: { "domain": "calendar" }
```

### Logout / status

- `lark_auth_status` — inspect current login state and remaining scopes.
- `lark_auth_logout` — revoke the current user identity (bot identity is unaffected).

## Update check

After any `lark_api` / `lark_api_search` call, if a new MCP server or skill version is available, the response will include a `_notice.update` field (with `message`, `command`, etc.).

**When you see `_notice.update` in the output, after completing the user's current request, proactively offer to help update**:

1. Inform the user of the current version and the latest version number.
2. Offer the upgrade path (the marketplace plugin and the MCP server update together):
   ```
   /plugin update larkskill
   ```
3. After the update completes, remind the user: **quit and reopen the AI Agent** to load the latest skills.

**Rule**: Do not silently ignore update prompts. Even when the current task is unrelated to updates, you should still inform the user after completing the request.

## Safety rules

- **DO NOT output secrets** (`appSecret`, `accessToken`, `refresh_token`) to the chat or terminal in plaintext.
- **Write/delete operations MUST confirm user intent first** (record-delete, table-delete, file-delete, message-delete, advperm-disable, etc.).
- Prefer read-only operations for discovery; only escalate to write operations once the target is unambiguous.
- Treat any URL returned by `lark_auth_login` as a one-time authorization link — relay it to the user, do not store or share it elsewhere.
