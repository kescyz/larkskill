# lark-wiki +node-list

List wiki nodes in a space or under a specific parent node. **Default fetches a single page** (large knowledge bases can have thousands of nodes).

## Usage

```js
// Default: single page of root nodes
lark_api({ tool: 'wiki', op: 'node-list', args: { space_id: '<SPACE_ID>' } })

// Drill into a sub-directory (still single page by default)
lark_api({ tool: 'wiki', op: 'node-list', args: { space_id: '<SPACE_ID>', parent_node_token: '<NODE_TOKEN>' } })

// Personal document library (user identity only)
lark_api({ tool: 'wiki', op: 'node-list', args: { space_id: 'my_library', as: 'user' } })
```

## Flags

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `space_id` | string | **Yes** | — | Wiki space ID. Use `my_library` for personal document library (user only) |
| `parent_node_token` | string | No | — | Parent node token; omit to list the space root |
| `as` | enum | No | `auto` | Identity `user`/`bot`; wiki is user-centric → pass `as: 'user'` (`my_library` requires `as: 'user'`) |

## Output

```json
{
  "ok": true,
  "data": {
    "nodes": [
      {
        "space_id": "6946843325487912356",
        "node_token": "wikcn_EXAMPLE_TOKEN",
        "obj_token": "doccn_EXAMPLE_TOKEN",
        "obj_type": "docx",
        "parent_node_token": "",
        "node_type": "origin",
        "title": "Getting Started",
        "has_child": true
      }
    ],
    "has_more": false,
    "page_token": ""
  },
  "meta": { "count": 1 }
}
```

When the default single-page fetch does not exhaust the upstream cursor, `has_more=true` and `page_token=<cursor>` so the caller can resume.

## Traverse the wiki tree

To list all content recursively, call `+node-list` again with each node's `node_token` as `parent_node_token` when `has_child` is `true`.

```js
// Step 1: list root nodes
lark_api({ tool: 'wiki', op: 'node-list', args: { space_id: '6946843325487912356' } })

// Step 2: drill into a node that has children
lark_api({ tool: 'wiki', op: 'node-list', args: { space_id: '6946843325487912356', parent_node_token: 'wikcn_EXAMPLE_TOKEN' } })
```

## Notes

- `space_id: 'my_library'` is a per-user alias and only valid with `as: 'user'`. The shortcut will refuse `as: 'bot'` with `my_library` upfront.

## Required Scope

`wiki:node:retrieve`
