# lark-wiki +member-add

Add a member to a wiki space. OpenAPI: `POST /open-apis/wiki/v2/spaces/:space_id/members`. Shortcut over the raw `wiki members create` — adds enum hints, optional `--need-notification`, `my_library` resolution, and a flattened single-member output envelope.

> The underlying `members.create` API is flagged `danger: true` in the schema browser, but adding a member is **not** confirmation-gated (no `--yes`). To revert, call [`+member-remove`](lark-wiki-member-remove.md) with the same `(member_id, member_type, member_role)` tuple.

## Usage

```js
// Add a user as a regular member
lark_api({ tool: 'wiki', op: 'member-add', args: {
  space_id: '<space_id>',
  member_id: '<open_id|email|user_id|...>',
  member_type: '<openid|email|userid|unionid|openchat|opendepartmentid>',
  member_role: '<admin|member>',
  // need_notification: true,
  as: 'user'
} })

// Personal library (resolves my_library to the per-user real space first)
lark_api({ tool: 'wiki', op: 'member-add', args: {
  space_id: 'my_library',
  member_id: 'ou_xxx', member_type: 'openid', member_role: 'member',
  as: 'user'
} })
```

## Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `space_id` | string | **Yes** | — | Wiki space ID; use `my_library` for the personal document library (user only) |
| `member_id` | string | **Yes** | — | Member ID; interpretation is decided by `--member-type` |
| `member_type` | enum | **Yes** | — | `openchat` / `userid` / `email` / `opendepartmentid` / `openid` / `unionid` |
| `member_role` | enum | **Yes** | — | `admin` (full space administration) / `member` (collaborator) |
| `need_notification` | bool | No | unset | Send an in-app notification after the grant. **Omitting it sends no `need_notification` query at all** — passing `need_notification: false` is the explicit opt-out |
| `as` | enum | No | `auto` | Identity `user`/`bot`; wiki is user-centric → pass `as: 'user'` |

## Output

```json
{
  "space_id": "7160145948494381236",
  "member_id": "ou_449b53ad6aee526f7ed311b216aabcef",
  "member_type": "openid",
  "member_role": "admin",
  "type": "user"
}
```

`type` is a read-only enum (`user` / `chat` / `department`) the server attaches; absent when the API omits it.

## Notes

- **Bot + `my_library` is rejected upfront** — `my_library` is a per-user alias with no meaning for a tenant token. Pass an explicit `space_id` when `as: 'bot'`.
- **Bot + `opendepartmentid` is a known unsupported path on the backend.** The CLI does not pre-block it (the API may evolve), but the call will fail. Use `as: 'user'` for department adds.
- Resolve `member_id` **before** calling: `lark_api({ tool: 'contact', op: 'search-user' })` for users, `lark_api({ tool: 'im', op: 'chat-search' })` for groups, `lark_api({ tool: 'api', op: 'POST', args: { path: '/open-apis/contact/v3/departments/search' } })` for departments. Do not call `+member-add` first and reverse-engineer the type from the error.
- The role switch (`admin` ⇄ `member`) is not a single update — call [`+member-remove`](lark-wiki-member-remove.md) for the old role first, then `+member-add` with the new one.

## Required Scope

`wiki:member:create`
