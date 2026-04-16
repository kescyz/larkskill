# base table operations

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first to understand auth, global parameters and safety rules.

Index of table-related MCP `lark_api` calls.

## Operation navigation

| Reference doc | Operation | Description |
|---------------|-----------|-------------|
| [lark-base-table-list.md](lark-base-table-list.md) | `table-list` | List tables with pagination |
| [lark-base-table-get.md](lark-base-table-get.md) | `table-get` | Get table summary, fields, and views |
| [lark-base-table-create.md](lark-base-table-create.md) | `table-create` | Create a table with optional fields/views |
| [lark-base-table-update.md](lark-base-table-update.md) | `table-update` | Rename a table |
| [lark-base-table-delete.md](lark-base-table-delete.md) | `table-delete` | Delete a table |

## Notes

- This index page is directory-only. Before calling any table endpoint, read the corresponding single-operation doc first (this page does not include call details).
- All list calls (`table-list`, `field-list`, `record-list`, etc.) must run sequentially. If you need multiple list requests, run them one by one.
- Each operation maps to a `lark_api` call — method and path are documented in the individual reference files.
