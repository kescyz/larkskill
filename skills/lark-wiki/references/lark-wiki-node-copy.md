# lark-wiki +node-copy

Copy a wiki node (including its content) to a target space or under a target parent node. Used for cross-space migration.

> ⚠️ **High-risk write** — the upstream API is flagged `danger: true`, so this shortcut requires explicit confirmation before issuing the request. Without confirmation it returns a `confirmation_required` error and the copy is **not** performed.

## Usage

```js
lark_api({ tool: 'wiki', op: 'node-copy', args: {
  space_id: '<source_space_id>',
  node_token: '<source_node_token>',
  // one of: target_space_id: '<target_space_id>' | target_parent_node_token: '<token>'
  target_space_id: '<target_space_id>',
  // title: '<new_title>',
  as: 'user'
} })
```

## Flags

| Flag | Required | Description |
|------|----------|-------------|
| `space_id` | **Yes** | Source wiki space ID |
| `node_token` | **Yes** | Source node token to copy |
| `target_space_id` | Conditional | Target space ID. Required if `target_parent_node_token` is not set |
| `target_parent_node_token` | Conditional | Target parent node token. Required if `target_space_id` is not set |
| `title` | No | New title for the copied node. Omit to keep the original title |
| `as` | No | Identity `user`/`bot` (default `auto`); wiki is user-centric → pass `as: 'user'` |

> At least one of `target_space_id` or `target_parent_node_token` must be provided.

## Output

```json
{
  "space_id": "target_space_id",
  "node_token": "wikcn_EXAMPLE_TOKEN",
  "obj_token": "doccn_EXAMPLE_TOKEN",
  "obj_type": "docx",
  "node_type": "origin",
  "title": "Getting Started (Copy)",
  "parent_node_token": "",
  "has_child": false
}
```

## Migration workflow

To migrate a subtree from one space to another:

```js
// 1. List nodes in the source space
lark_api({ tool: 'wiki', op: 'node-list', args: { space_id: 'source_space_id' } })

// 2. Copy each node to the target space
lark_api({ tool: 'wiki', op: 'node-copy', args: {
  space_id: '<source_space_id>',
  node_token: 'wikcn_EXAMPLE_TOKEN',
  target_space_id: '<target_space_id>'
} })
```

## Notes

- Copying is recursive — the subtree under the node is also copied.
- There is no native move API; migration = copy to target + (manually delete source if needed).

## Required Scope

`wiki:node:copy`
