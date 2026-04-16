# view

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

View operation index.

## Operation navigation

| Document | Operation | Description |
|----------|-----------|-------------|
| [lark-base-view-list.md](lark-base-view-list.md) | `view-list` | Paginated list of views |
| [lark-base-view-get.md](lark-base-view-get.md) | `view-get` | Get basic view information |
| [lark-base-view-create.md](lark-base-view-create.md) | `view-create` | Create views |
| [lark-base-view-delete.md](lark-base-view-delete.md) | `view-delete` | Delete a view |
| [lark-base-view-rename.md](lark-base-view-rename.md) | `view-rename` | Rename a view |
| [lark-base-view-get-filter.md](lark-base-view-get-filter.md) | `view-get-filter` | Read filter configuration |
| [lark-base-view-set-filter.md](lark-base-view-set-filter.md) | `view-set-filter` | Update filter configuration |
| [lark-base-view-get-group.md](lark-base-view-get-group.md) | `view-get-group` | Read group configuration |
| [lark-base-view-set-group.md](lark-base-view-set-group.md) | `view-set-group` | Update group configuration |
| [lark-base-view-get-sort.md](lark-base-view-get-sort.md) | `view-get-sort` | Read sort configuration |
| [lark-base-view-set-sort.md](lark-base-view-set-sort.md) | `view-set-sort` | Update sort configuration |
| [lark-base-view-get-timebar.md](lark-base-view-get-timebar.md) | `view-get-timebar` | Read timeline configuration |
| [lark-base-view-set-timebar.md](lark-base-view-set-timebar.md) | `view-set-timebar` | Update timeline configuration |
| [lark-base-view-get-card.md](lark-base-view-get-card.md) | `view-get-card` | Read card configuration |
| [lark-base-view-set-card.md](lark-base-view-set-card.md) | `view-set-card` | Update card configuration |

## AI decision guide

Determine the view type first, then select the applicable operations; do not call unsupported capabilities.

| View type | Available operations |
|-----------|---------------------|
| `grid` | `group` `sort` `filter` |
| `kanban` | `group` `sort` `filter` `card` |
| `gallery` | `sort` `filter` `card` |
| `calendar` | `filter` `timebar` |
| `gantt` | `group` `sort` `filter` `timebar` |

## Notes

- This index page holds only directory responsibilities; see individual operation documents for details.
- All `*-list` calls must be executed serially; concurrent list requests are not supported.
