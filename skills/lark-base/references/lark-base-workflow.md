# workflow

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Workflow (automation) operation index.

## Operation navigation

| Document | Operation | Description |
|----------|-----------|-------------|
| [lark-base-workflow-list.md](lark-base-workflow-list.md) | `workflow-list` | List all automated workflows in Base |
| [lark-base-workflow-get.md](lark-base-workflow-get.md) | `workflow-get` | Get the details and complete structure of a single workflow |
| [lark-base-workflow-create.md](lark-base-workflow-create.md) | `workflow-create` | Create a new automated workflow |
| [lark-base-workflow-update.md](lark-base-workflow-update.md) | `workflow-update` | Full replacement of existing workflow definition |
| [lark-base-workflow-enable.md](lark-base-workflow-enable.md) | `workflow-enable` | Enable an automated workflow |
| [lark-base-workflow-disable.md](lark-base-workflow-disable.md) | `workflow-disable` | Disable an automated workflow |
| [lark-base-workflow-schema.md](lark-base-workflow-schema.md) | (reference) | Workflow creation and update structure specifications |

## Notes

- This index page holds only directory responsibilities; see individual operation documents for details.
- **Config pre-dependency:** Before creating or updating a workflow, you likely need real table / field IDs as node parameters. Check [lark-base-table.md](lark-base-table.md) or [lark-base-field.md](lark-base-field.md) as needed.
- **Schema must-read:** Before creating or updating a workflow, read [lark-base-workflow-schema.md](lark-base-workflow-schema.md) carefully for trigger and node component structures.
