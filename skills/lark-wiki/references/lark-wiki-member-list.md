# lark-wiki +member-list

List the members of a wiki space. OpenAPI: `GET /open-apis/wiki/v2/spaces/:space_id/members`. **Default fetches a single page** (matches `+space-list` / `+node-list`).

## Usage

```js
// Default: single page
lark_api({ tool: 'wiki', op: 'member-list', args: { space_id: '<space_id>' } })

// Personal library
lark_api({ tool: 'wiki', op: 'member-list', args: { space_id: 'my_library', as: 'user' } })
```

## Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `space_id` | string | **Yes** | — | Wiki space ID; use `my_library` for the personal document library (user only) |
| `as` | enum | No | `auto` | Identity `user`/`bot`; wiki is user-centric → pass `as: 'user'` |

## Output

```json
{
  "ok": true,
  "data": {
    "space_id": "7160145948494381236",
    "members": [
      {
        "member_id": "ou_449b53ad6aee526f7ed311b216aabcef",
        "member_type": "openid",
        "member_role": "admin"
      },
      {
        "member_id": "ou_67e5ecb64ce1c0bd94612c17999db411",
        "member_type": "openid",
        "member_role": "member"
      }
    ],
    "has_more": false,
    "page_token": ""
  },
  "meta": { "count": 2 }
}
```

`type` (`user` / `chat` / `department`) is included when the server returns it. When the default single-page fetch does not exhaust the upstream cursor, `has_more=true` and `page_token=<cursor>` so the caller can resume.

## Notes

- **Bot + `my_library` is rejected upfront** — pass an explicit `space_id` when `as: 'bot'`.
- Use `member_id` from the output as `member_id` for [`+member-remove`](lark-wiki-member-remove.md); `member_type` and `member_role` must be passed exactly as listed to remove a grant.

## Required Scope

`wiki:member:retrieve`
