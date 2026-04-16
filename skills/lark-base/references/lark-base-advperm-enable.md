# advperm-enable

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Enable advanced permissions for a Base. After enabling, custom roles and related advanced permission features are available.

## Recommended call

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/advperm/enable
- params:
  ```json
  { "enable": true }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token, a 27-character alphanumeric string (path param) |
| `enable` | Yes | Query param, fixed to `true` to enable advanced permissions |

## API request details

```
PUT /open-apis/base/v3/bases/{base_token}/advperm/enable?enable=true
```

**Path params:**

| Param | Required | Description |
|-------|----------|-------------|
| `base_token` | Yes | Unique Base identifier, a 27-character alphanumeric string |

**Query params:**

| Param | Required | Type | Description |
|-------|----------|------|-------------|
| `enable` | Yes | bool | Fixed to `true`, meaning enable advanced permissions |

## API response details

**Response:**

| Field | Type | Description |
|-------|------|-------------|
| `code` | int32 | Error code, `0` means success |
| `message` | string | Error message |
| `data` | string | Empty on success |

## Return value

On success, API returns:

```json
{
  "code": 0,
  "data": "",
  "message": "success"
}
```

## Workflow

1. Confirm `base_token` with user
2. Call the API
3. Verify `code: 0`

## Pitfalls

- ⚠️ Acting user must be a Base admin, otherwise permission errors are returned.
- ⚠️ Endpoint version is `base/v3`; use the canonical path above.
- ⚠️ `data` is a JSON string, not an object, so parse twice when needed.
- ⚠️ `role-create / role-update / role-delete` require advanced permissions to be enabled first.

## References

- [lark-base](../SKILL.md) - all Base commands
- [lark-shared](../../lark-shared/SKILL.md) - auth and global flags
