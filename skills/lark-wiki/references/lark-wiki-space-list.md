# lark-wiki +space-list

List wiki spaces accessible to the caller. **Default fetches a single page** (matches the rest of the list shortcuts).

## Usage

```js
// Default: single page
lark_api({ tool: 'wiki', op: 'space-list', args: {} })

// As user identity
lark_api({ tool: 'wiki', op: 'space-list', args: { as: 'user' } })
```

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `as` | enum | `auto` | Identity `user`/`bot`; wiki is user-centric → pass `as: 'user'` |

## Output

```json
{
  "ok": true,
  "data": {
    "spaces": [
      {
        "space_id": "6946843325487912356",
        "name": "Engineering Wiki",
        "description": "...",
        "space_type": "team",
        "visibility": "private",
        "open_sharing": "closed"
      }
    ],
    "has_more": false,
    "page_token": ""
  },
  "meta": { "count": 1 }
}
```

When the default single-page fetch does not exhaust the upstream cursor, `has_more=true` and `page_token=<cursor>` so the caller can resume.

## Notes

- **The underlying API never returns the my_library personal library**; resolve it via `lark_api({ tool: 'wiki', op: 'spaces.get', args: { space_id: 'my_library' } })`.
- Use `space_id` from the output as `space_id` for `+node-list` or `+node-copy`.

## Required Scope

`wiki:space:retrieve`
