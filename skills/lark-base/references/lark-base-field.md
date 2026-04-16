# base field operations

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

Index of field-related MCP `lark_api` calls.

## Operation navigation

| Reference doc | Operation | Description |
|---------------|-----------|-------------|
| [lark-base-field-list.md](lark-base-field-list.md) | `field-list` | Paginated field listing |
| [lark-base-field-get.md](lark-base-field-get.md) | `field-get` | Get single field configuration |
| [lark-base-field-create.md](lark-base-field-create.md) | `field-create` | Create a field |
| [lark-base-field-update.md](lark-base-field-update.md) | `field-update` | Update a field |
| [lark-base-field-search-options.md](lark-base-field-search-options.md) | `field-search-options` | Search option field candidate values |
| [lark-base-field-delete.md](lark-base-field-delete.md) | `field-delete` | Delete a field |

## Notes

- This index page is directory-only. For detailed call signatures, read the corresponding single-operation doc.
- All list calls must run sequentially. If you need multiple list requests, run them one by one.
- Read [lark-base-shortcut-field-properties.md](lark-base-shortcut-field-properties.md) before constructing any field create/update JSON body. Field type properties vary significantly by `type`.
- For formula fields (`type=formula`): read [formula-field-guide.md](formula-field-guide.md) before writing the `expression`.
- For lookup fields (`type=lookup`): read [lookup-field-guide.md](lookup-field-guide.md) before writing the lookup config. Formula is the default preference; use lookup only when explicitly requested or structurally appropriate.
