---
name: lark-shared
version: 1.0.0
description: "Use when first setting up LarkSkill MCP, running auth login, switching user/bot identity, handling permission denied or scope errors, needing to update lark-cli, or seeing _notice in JSON output."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_auth_login", "lark_auth_poll", "lark_auth_status", "lark_auth_logout", "lark_whoami", "lark_profile_list", "lark_profile_switch", "lark_enable_domain", "lark_api_search"]
---

# LarkSkill MCP Shared Rules

This skill guides you on how to operate Lark resources via the LarkSkill MCP tool, and what to watch out for.

## Configuration Initialization

On first use, run `lark_auth_login` to complete the app authorization flow.

When you help the user initialize the configuration, use `lark_auth_login` to start the authorization flow; once started, read the output, extract the authorization URL from it, and send it to the user.

**URL Forwarding Rules**: When the tool outputs URL fields such as `verification_url`, `verification_uri_complete`, `console_url`, etc.: you MUST forward the URL exactly as returned to the user and treat it as an immutable opaque string — do NOT URL-encode/decode it, do NOT append `%20`, spaces, or punctuation, do NOT re-assemble the query string, and do NOT rewrite it as Markdown link text. Recommended: output the raw URL alone in its own code block. (Note: the upstream `lark-cli auth qrcode` QR-code generation step has no MCP-tool equivalent; forward the raw `verification_url` instead — the URL already carries the pre-filled `user_code`.)

```javascript
// Start the authorization flow
lark_auth_login({ domain: '<domain>' })
// or with a specific scope
lark_auth_login({ scope: 'calendar:calendar:readonly' })
```

## Authentication

### Identity Types

Two identity types, toggled via the active profile:

| Identity | Identifier | How to Obtain | Use Case |
|----------|-----------|---------------|----------|
| User identity | `as: "user"` | `lark_auth_login` + `lark_auth_poll` | Access the user's own resources (Calendar, Drive/cloud storage, etc.) |
| Bot application identity | `as: "bot"` | Automatic — only requires appId + appSecret | Application-level operations, accessing bot's own resources |

### Identity Selection Principles

The `[identity: bot/user]` in the output indicates the current identity. Bot and user behave very differently; confirm the identity matches the target requirement:

- **Bot cannot see user resources**: Cannot access the user's Calendar, Drive (cloud storage/documents), Mail, or other personal resources. For example, bot identity querying a schedule returns the bot's own (empty) calendar.
- **Bot cannot act on behalf of the user**: Messages are sent under the application name; created documents are owned by the bot.
- **Bot permissions**: Only requires enabling the scope in the Lark Developer Console — no `lark_auth_login` needed.
- **User permissions**: Both enabling the scope in the console AND the user granting authorization via `lark_auth_login` + `lark_auth_poll` are required — both layers must be satisfied.


### Handling Insufficient Permissions

When encountering permission-related errors, **adopt different solutions depending on the current identity type**.

The error response contains key information:
- `permission_violations`: lists the missing scopes (select any that apply)
- `console_url`: link to the permission configuration page in the Lark Developer Console
- `hint`: suggested fix command

#### Bot Identity (`as: "bot"`)

Provide the `console_url` from the error as-is to the user, guiding them to enable the scope in the console. **DO NOT** run `lark_auth_login` for a bot identity.

#### User Identity (`as: "user"`)

```javascript
lark_auth_login({ domain: '<domain>' })           // authorize by business domain
lark_auth_login({ scope: '<missing_scope>' })     // authorize by specific scope (recommended — follows least-privilege principle)
```

**Rule**: `lark_auth_login` MUST specify a scope (`domain` or `scope`). Multiple login calls accumulate scopes (incremental authorization). After calling `lark_auth_login`, call `lark_auth_poll` to complete the device flow.

#### Agent-Initiated Authentication (Recommended)

When you as an AI agent need to help a user complete authentication, prefer the split-flow to avoid blocking and waiting for user authorization within the same conversation turn:

```javascript
// Step 1: Initiate authorization (returns device_code and verification_url immediately)
lark_auth_login({ scope: 'calendar:calendar:readonly', no_wait: true })
```

Once you have the `verification_url`, forward it verbatim as the final message of the current turn and return control. Do not display the URL and then immediately poll in the same turn; in agent harnesses that do not pass through intermediate output, this causes the user to never see the URL.

After the user replies that authorization is complete, execute in a subsequent step:

```javascript
// Step 2: Complete the device flow
lark_auth_poll({ device_code: '<device_code>' })
```

**Split-Flow Complete Steps**:

**Step 1: Initiate Authorization (current turn)**

1. Execute `lark_auth_login({ scope: 'xxx', no_wait: true })` (MUST include `no_wait: true`)
2. Extract `verification_url` and `device_code` from the output
3. Display the URL to the user (output the raw URL alone in its own code block)
4. **Before ending the current turn, MUST explicitly inform the user**: "Please complete the authorization and then come back to tell me — I will help you complete the next steps."

**Step 2: Complete Authorization (subsequent turn)**

1. Wait for the user to reply "authorization complete"
2. **You (the AI agent) MUST personally execute**: `lark_auth_poll({ device_code: '<device_code>' })`
3. This call will poll the authorization status and complete the login
4. If authorization success is returned, the flow ends

**Key Rules**:

- **You MUST personally execute the `lark_auth_poll` call** — do not instruct the user to execute it themselves
- **DO NOT display the URL and then immediately poll in the same turn** — this causes the user to never see the URL
- **DO NOT cache `verification_url` or `device_code`**: Every time authorization is needed, you MUST re-execute `lark_auth_login({ no_wait: true })` to generate a new link. Do not store the authorization link and device code in context for later reuse.

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

Use `lark_auth_status` to check the current authorization state, and `lark_auth_logout` to clear stored credentials:

```javascript
lark_auth_status({})
lark_auth_logout({})
```

Use `lark_enable_domain` to enable a business domain for the current user profile:

```javascript
lark_enable_domain({ domain: '<domain>' })
```

## Update Check

After a LarkSkill MCP tool call, if a new version is detected, the JSON output will contain a `_notice.update` field (with `message`, `command`, etc.).

**When you see `_notice.update` in the output, after completing the user's current request, proactively offer to help the user update**:

1. Inform the user of the current version and the latest version number
2. Propose executing the update (updates both CLI and Skills simultaneously):
   ```bash
   lark-cli update
   ```
3. After the update completes, remind the user: **exit and reopen the AI Agent** to load the latest Skills

**Important**: Always use `lark-cli update` to update — it updates both the CLI and AI Skills simultaneously.

**Rule**: Do not silently ignore update notices. Even if the current task is unrelated to an update, you should additionally inform the user after completing their request.

## Security Rules

- **DO NOT output secrets** (appSecret, accessToken) as plaintext to the terminal.
- **MUST confirm user intent before write/delete operations**.
- Use dry-run mode where available to preview dangerous requests.

## High-Risk Operation Approval Protocol

The LarkSkill MCP enforces a mandatory confirmation gate for high-risk write operations (`risk: "high-risk-write"`). When you call such a tool without explicit confirmation, the tool returns an error of type `confirmation_required` with the following structured envelope:

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

**When this occurs, do not treat it as an ordinary error and give up.** Follow this flow:

1. **Identify**: the error type is `confirmation_required`
2. **Confirm with the user**: display `error.risk.action` and key parameters to the user, explicitly state "this is a high-risk operation," and wait for the user's explicit consent
3. **User consents** → add `yes: true` to the args and retry
4. **User declines** → terminate the flow; do not alter parameters or bypass the gate on your own

**Absolutely prohibited**:
- Seeing `confirmation_required` and silently adding `yes: true` and retrying (this disables the gate)
- Treating `confirmation_required` as a network error or permission error
- Adding `yes: true` and retrying without the user's explicit consent
- Reconstructing the call as a shell string to retry — pass `yes: true` as a structured tool argument so user-supplied values are never shell-interpreted (the MCP transport carries no shell; the upstream `sh -c` / `exec.Command(argv...)` rule does not apply, but the same intent holds: never splice user input into a command string)

Plan ahead: to let the user review the details of a dangerous request first, use dry-run mode where available — it does not trigger the gate and prints the full request details (URL / body / params); you can show this preview to the user before actually executing.

### How to Identify Whether an Operation Is High-Risk

Use `lark_api_search` to look up the tool's schema — if the schema includes `"risk": "high-risk-write"`, the operation requires confirmation.
