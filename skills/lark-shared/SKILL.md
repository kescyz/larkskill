---
name: lark-shared
version: 2.0.0
description: "Use when first setting up LarkSkill MCP, running auth login, switching user/bot identity, handling permission denied or scope errors, needing to update lark-cli, or seeing _notice in JSON output."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_auth_login", "lark_auth_poll", "lark_auth_status", "lark_auth_logout", "lark_whoami", "lark_profile_list", "lark_profile_switch", "lark_enable_domain"]
---

# LarkSkill MCP Shared Rules

This skill guides you on how to operate Lark resources via the LarkSkill MCP tool, and what to watch out for.

## Configuration Initialization

On first use, run `lark_auth_login` to complete the app authorization flow.

When you help the user initialize configuration, use `lark_auth_login` to start the authorization flow; once started, read the output, extract the authorization URL from it, and send it to the user.

**URL forwarding rule**: When the tool outputs `verification_url`, `verification_uri_complete`, `console_url`, or similar URL fields, you MUST forward the URL exactly as returned to the user and treat it as an immutable opaque string — do NOT URL-encode/decode it, do NOT append `%20`, spaces, or punctuation, do NOT re-assemble the query string, do NOT rewrite it as a Markdown link text. Recommended: output the raw URL in its own code block.

```javascript
// Start authorization flow
lark_auth_login({ domain: '<domain>' })
// or with specific scope
lark_auth_login({ scope: 'calendar:calendar:readonly' })
```

## Authentication

### Identity Types

Two identity types, toggled via the active profile:

| Identity | Identifier | How to obtain | Applicable scenarios |
|------|------|---------|---------|
| User identity | `as: "user"` | `lark_auth_login` + `lark_auth_poll` | Access user's own resources (calendar, Drive, etc.) |
| Bot identity | `as: "bot"` | Automatic — only needs appId + appSecret | App-level operations, accessing bot's own resources |

### Identity Selection Principles

The `[identity: bot/user]` in the output represents the current identity. Bot and user behave very differently; confirm that the identity matches the target requirement:

- **Bot cannot see user resources**: Cannot access the user's calendar, Drive documents, mailbox, or other personal resources. For example, bot identity querying events returns the bot's own (empty) calendar.
- **Bot cannot act on behalf of the user**: Messages are sent under the app name; documents created are owned by the bot.
- **Bot permissions**: Only requires enabling scopes in the Lark Developer Console — no `lark_auth_login` needed.
- **User permissions**: Both enabling scopes in the console AND user authorization via `lark_auth_login` + `lark_auth_poll` are required.

### Handling Insufficient Permissions

When you encounter permission-related errors, **take different remediation steps based on the current identity type**.

The error response contains key information:
- `permission_violations`: lists missing scopes (pick N)
- `console_url`: link to the Lark Developer Console permission configuration
- `hint`: suggested fix command

#### Bot identity

Provide the `console_url` from the error verbatim to the user, guiding them to enable the scope in the console. **DO NOT** run `lark_auth_login` for bot identity.

#### User identity

```javascript
lark_auth_login({ domain: '<domain>' })           // Authorize by business domain
lark_auth_login({ scope: '<missing_scope>' })     // Authorize by specific scope (recommended — follows least-privilege principle)
```

**Rule**: `lark_auth_login` MUST specify a scope (`domain` or `scope`). Multiple logins accumulate scopes (incremental authorization). After calling `lark_auth_login`, call `lark_auth_poll` to complete the device flow.

#### Agent-initiated authentication (recommended)

When you as an AI agent need to help the user complete authentication, prefer the split-flow to avoid blocking and waiting for user authorization within the same conversation turn:

```javascript
// Step 1: Initiate authorization (returns device_code and verification_url immediately)
lark_auth_login({ scope: 'calendar:calendar:readonly', no_wait: true })
```

After obtaining the `verification_url`, forward it verbatim as the final message for this turn and return control to the user. Do NOT display the URL and then immediately poll in the same turn; in agent harnesses that do not surface intermediate output, the user will never see the URL.

After the user replies that they have completed authorization, execute in a subsequent step:

```javascript
// Step 2: Complete the device flow
lark_auth_poll({ device_code: '<device_code>' })
```

### Profile Management

Use `lark_profile_list` to see all configured profiles (app identities), and `lark_profile_switch` to switch the active profile:

```javascript
lark_profile_list({})
lark_profile_switch({ profile: '<profile_name>' })
```

Use `lark_whoami` to confirm the current identity and authorization status:

```javascript
lark_whoami({})
```

Use `lark_enable_domain` to enable a business domain for the current user profile:

```javascript
lark_enable_domain({ domain: '<domain>' })
```

## Update Check

After a LarkSkill MCP tool call, if a new version is detected, the JSON output will contain a `_notice.update` field (with `message`, `command`, etc.).

**When you see `_notice.update` in the output, after completing the user's current request, proactively offer to help the user update**:

1. Inform the user of the current version and the latest version number.
2. Offer to run the update (updates both CLI and Skills):
   ```bash
   lark-cli update
   ```
3. After the update completes, remind the user: **exit and reopen the AI Agent** to load the latest Skills.

**Important**: Always use `lark-cli update` to update — it updates both the CLI and AI Skills simultaneously.

**Rule**: Do not silently ignore update notices. Even if the current task is unrelated to updating, notify the user after completing their request.

## Security Rules

- **DO NOT output secrets** (appSecret, accessToken) as plaintext to the terminal.
- **Confirm user intent before write/delete operations**.
- Use dry-run mode where available to preview dangerous requests.

## High-Risk Operation Approval Protocol

The LarkSkill MCP enforces a mandatory confirmation gate for high-risk write operations. When you call such tools without explicit confirmation, the tool will return an error of type `confirmation_required` with a structured envelope:

```json
{
  "ok": false,
  "error": {
    "type": "confirmation_required",
    "message": "drive delete requires confirmation",
    "hint": "add yes: true to confirm",
    "risk": {
      "level": "high-risk-write",
      "action": "drive delete"
    }
  }
}
```

**Do NOT treat this as an ordinary error and give up.** Handle it with the following flow:

1. **Identify**: error type is `confirmation_required`
2. **Confirm with the user**: display `error.risk.action` and key parameters to the user, clearly stating "this is a high-risk operation", and wait for explicit user consent
3. **User consents** → add `yes: true` to the args and retry
4. **User refuses** → terminate the flow; do not arbitrarily rewrite parameters or bypass the gate

**Strictly prohibited**:
- Silently adding `yes: true` and retrying on seeing `confirmation_required` (this disables the gate)
- Treating `confirmation_required` as a network error or permission error
- Adding `yes: true` and retrying without explicit user consent

Plan ahead: to let the user review the details of a dangerous request before it runs, use dry-run mode where available — it does not trigger the gate and prints the complete request details; you can show this preview to the user before executing for real.

### How to identify a high-risk operation

Use `lark_api_search` to look up the tool's schema — if the schema includes `"risk": "high-risk-write"`, the operation requires confirmation.
