# Dashboard Module Guide

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Dashboard is a data visualization board in Base that turns table data into **blocks** (charts, KPI cards, etc.) for display.

## Core concepts

- **Dashboard**: container that holds multiple blocks
- **Block**: a single visualization element in a dashboard (column chart, line chart, pie chart, KPI card, etc.)
- **data_config**: data source configuration of a block (table name, fields, grouping, etc.)

## Capability overview

| What you want to do | Operations | Key docs |
|---------------------|------------|----------|
| Create/delete/rename | `dashboard-create` / `dashboard-delete` / `dashboard-update` | See sections below |
| Add a block to a dashboard | `dashboard-block-create` | Read [lark-base-dashboard-block-create.md](lark-base-dashboard-block-create.md) first, then [dashboard-block-data-config.md](dashboard-block-data-config.md) |
| Modify a block | `dashboard-block-update` | Read [lark-base-dashboard-block-update.md](lark-base-dashboard-block-update.md) first, then [dashboard-block-data-config.md](dashboard-block-data-config.md) |
| View blocks in a dashboard | `dashboard-get` or `dashboard-block-list` | See sections below |

## Typical scenario workflows

### Scenario 1: Create a dashboard from scratch

1. Call `dashboard-create` with `name` (and optionally `theme_style`). Record the returned `dashboard_id`.
2. Call `table-list` and `field-list` to get data source info.
3. Plan which blocks to create based on user needs.
4. Create each block sequentially using `dashboard-block-create` — **blocks must be created serially**.
   - Read [lark-base-dashboard-block-create.md](lark-base-dashboard-block-create.md) for parameters.
   - Read [dashboard-block-data-config.md](dashboard-block-data-config.md) for `data_config` structure.

### Scenario 2: Add new blocks to an existing dashboard

1. Call `dashboard-list` to locate the target; get `dashboard_id`.
2. Call `dashboard-get` to review existing blocks (avoid duplicates).
3. Call `table-list` and `field-list` to get data source info.
4. Create each new block sequentially using `dashboard-block-create`.

### Scenario 3: Edit an existing block

> `dashboard-block-update` **cannot modify `type`** (chart type) — only `name` and `data_config`.
> To change the chart type, delete and recreate the block.

1. Call `dashboard-list` to locate the target.
2. Call `dashboard-block-list` to get the target `block_id`.
3. Call `dashboard-block-get` to get current block details.
4. If data source changes are needed, call `table-list` / `field-list` first.
5. Call `dashboard-block-update` with updated `data_config`.

### Scenario 4: View dashboard or block status

- See overall dashboard structure → use `dashboard-get`
- Quick block list → use `dashboard-block-list`
- Detailed `data_config` of a specific block → use `dashboard-block-get`

## Block type selection

| What the user wants to see | Type | Description |
|----------------------------|------|-------------|
| Data trend (over time) | `line` | Line chart |
| Category comparison | `column` | Column chart |
| Proportion distribution | `pie` | Pie chart |
| Single key metric | `statistics` | KPI card |

Full block types and complete `data_config` rules: [dashboard-block-data-config.md](dashboard-block-data-config.md)

## FAQ

**Q: Why did block creation fail?**
- `table_name` used a table ID instead of the table name (must use the display name, e.g. "Orders")
- `series` and `count_all` both present (mutually exclusive — choose one)
- Field name misspelled (use real names from `field-list`, guessing is prohibited)
- Blocks created concurrently (must be serial)

**Q: Can I create multiple blocks at once?**
No. Blocks must be created serially; wait for each `dashboard-block-create` to complete before starting the next.

**Q: Can the block `type` be changed after creation?**
No. `dashboard-block-update` can only modify `name` and `data_config`.

**data_config update strategy (top-level key merge):**
- Pass only the top-level fields to modify (e.g. `series`, `filter`)
- Omitted top-level fields retain their original values
- Each passed field is **fully replaced** (e.g. a new `filter` completely overwrites the old one)

## Operation reference

| Operation | Description | Detailed doc |
|-----------|-------------|--------------|
| `dashboard-list` | List all dashboards | [lark-base-dashboard-list.md](lark-base-dashboard-list.md) |
| `dashboard-get` | Get dashboard details (incl. all blocks) | [lark-base-dashboard-get.md](lark-base-dashboard-get.md) |
| `dashboard-create` | Create dashboard | [lark-base-dashboard-create.md](lark-base-dashboard-create.md) |
| `dashboard-update` | Update dashboard | [lark-base-dashboard-update.md](lark-base-dashboard-update.md) |
| `dashboard-delete` | Delete dashboard | [lark-base-dashboard-delete.md](lark-base-dashboard-delete.md) |
| `dashboard-block-list` | List blocks | [lark-base-dashboard-block-list.md](lark-base-dashboard-block-list.md) |
| `dashboard-block-get` | Get single block details | [lark-base-dashboard-block-get.md](lark-base-dashboard-block-get.md) |
| `dashboard-block-create` | Create block | [lark-base-dashboard-block-create.md](lark-base-dashboard-block-create.md) |
| `dashboard-block-update` | Update block | [lark-base-dashboard-block-update.md](lark-base-dashboard-block-update.md) |
| `dashboard-block-delete` | Delete block | [lark-base-dashboard-block-delete.md](lark-base-dashboard-block-delete.md) |
