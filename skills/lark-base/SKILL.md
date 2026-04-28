---
name: lark-base
version: 2.0.0
description: "Use this skill when operating Lark Base via LarkSkill MCP: table creation, field management, record read/write, view configuration, history queries, and role/form/dashboard/workflow management. Mandatory for formula fields, lookup references, cross-table computation, and data analysis."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# base

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first.
> **Mandatory before execution:** Before invoking any `base` operation, read the corresponding command reference doc, then call the operation via `lark_api`.
> **Naming convention:** Base business operations call `lark_api({ tool: 'base', op: '<op>', args: {...} })`; if a Wiki link must be resolved first, call `lark_api` with the HTTP form `{ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_token>' } }` first.
> **Routing rule:** If the user wants to "import a local file as Base / Bitable", the first step is NOT a `base` op — it is `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`. After import completes, return to `lark_api({ tool: 'base', op: '...' })` for in-table operations.

## 1. When to use this Skill

### 1.1 Trigger conditions

This skill should be used for the following scenarios:

- The user explicitly wants to operate Lark Base / Bitable.
- The user wants to create / modify / query / delete tables, or manage fields / records / views.
- The user wants to build formula fields, lookup fields, derived metrics, or cross-table computation.
- The user wants ad-hoc statistics, aggregation analysis, comparison / sorting, or extreme-value retrieval.
- The user wants to manage workflow, dashboard, form, or role permissions.
- The user gives a `/base/{token}` link.
- The user gives a `/wiki/{token}` link that ultimately resolves to `bitable`.
- The user wants to rewrite legacy aggregated Base commands into atomic operation form, e.g. translating legacy `+table / +field / +record / +view / +history / +workspace` into current ops.

This skill should NOT be used for the following:

- The user is only doing auth, init configuration, switching `--as user/bot`, or handling scope. Read `../lark-shared/SKILL.md` first.
- The user is only generally discussing "data analysis / field design" but is NOT actually in a Base scenario. Do NOT trigger merely because the words "statistics / formula / lookup" appear.

### 1.2 Prerequisites

1. Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first.
2. Base business operations call `lark_api({ tool: 'base', op: '<op>', args: {...} })`; if input is a Wiki link, call `lark_api` with the HTTP form `{ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_token>' } }` first to resolve the real token.
3. After locating the operation, read the corresponding reference, then execute it.
4. If the user wants to import a local Excel / CSV as Base / Bitable, the first step is NOT a `base` op — it is `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`; after import, return to `lark_api({ tool: 'base', op: '...' })` for in-table operations.
5. Do NOT bypass the catalog and call raw `/open-apis/bitable/v1/...` paths in Base scenarios.

## 2. Module and operation navigation

This chapter is organized "pick the module first, then pick the operation". Decide which large module the user's goal belongs to, enter the corresponding sub-module, read the reference per requirements, then execute.

### 2.1 Module map

| Large module | What problem it handles | Sub-modules / capabilities |
|---|---|---|
| Base module | Manage the Base itself, or enter the Base scenario from a link | `base-create / base-get / base-copy`, Base / Wiki link parsing |
| Table & data module | Manage Base internal structure and routine data operations | `table / field / record / view` |
| Formula / Lookup module | Handle derived fields, conditional logic, cross-table computation, fixed lookup references | `formula / lookup` field create and update |
| Data analysis module | One-off filtering, grouping, aggregation analysis | `data-query` |
| Workflow module | Manage automation flows | `workflow-list / get / create / update / enable / disable` |
| Dashboard module | Manage dashboards and chart blocks | `dashboard-* / dashboard-block-*` |
| Form module | Manage forms and form questions | `form-* / form-questions-*` |
| Permission & role module | Manage advanced permissions and custom roles | `advperm-* / role-*` |

### 2.2 Base module

For managing the Base itself, or entering subsequent Base operations from a user-supplied link.
Module index: [`references/lark-base-workspace.md`](references/lark-base-workspace.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'base-create'})` | Create a new Base | [`lark-base-base-create.md`](references/lark-base-base-create.md), [`lark-base-workspace.md`](references/lark-base-workspace.md) | Write op; read reference first; `folder-token`, `time-zone` are optional |
| `lark_api({tool:'base', op:'base-get'})` | Get Base info | [`lark-base-base-get.md`](references/lark-base-base-get.md), [`lark-base-workspace.md`](references/lark-base-workspace.md) | Suitable for confirming Base identity; not a substitute for table/field structure reads |
| `lark_api({tool:'base', op:'base-copy'})` | Copy an existing Base | [`lark-base-base-copy.md`](references/lark-base-base-copy.md), [`lark-base-workspace.md`](references/lark-base-workspace.md) | Write op; read reference first; on success, proactively return new Base identifiers |

### 2.3 Table & data module

This is the most-used module, including four sub-modules: `table / field / record / view`.
Supplemental examples: [`references/examples.md`](references/examples.md) — read when chaining table / record / view operations end-to-end.

#### 2.3.1 Table sub-module

Sub-module index: [`references/lark-base-table.md`](references/lark-base-table.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'table-list'})` / `lark_api({tool:'base', op:'table-get'})` | List data tables, or get details of a single table | [`lark-base-table-list.md`](references/lark-base-table-list.md), [`lark-base-table-get.md`](references/lark-base-table-get.md) | `table-list` must run serial; `table-get` is for confirming a target before delete/update |
| `lark_api({tool:'base', op:'table-create'})` / `lark_api({tool:'base', op:'table-update'})` / `lark_api({tool:'base', op:'table-delete'})` | Create, update, or delete a table | [`lark-base-table-create.md`](references/lark-base-table-create.md), [`lark-base-table-update.md`](references/lark-base-table-update.md), [`lark-base-table-delete.md`](references/lark-base-table-delete.md) | Create suits one-off table builds; update requires confirming the target first; if user already states the target, delete may run directly with `yes: true` |

#### 2.3.2 Field sub-module

Regular field management goes here; if the field type is `formula` or `lookup`, switch to the "Formula / Lookup module" below.
Sub-module index: [`references/lark-base-field.md`](references/lark-base-field.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'field-list'})` / `lark_api({tool:'base', op:'field-get'})` | List field schema, or get details of a single field | [`lark-base-field-list.md`](references/lark-base-field-list.md), [`lark-base-field-get.md`](references/lark-base-field-get.md) | Before writing records / writing fields / running analysis, usually call `field-list` first; `field-list` must run serial; `field-get` is for confirming a target before delete/update |
| `lark_api({tool:'base', op:'field-create'})` / `lark_api({tool:'base', op:'field-update'})` / `lark_api({tool:'base', op:'field-delete'})` | Create, update, or delete a regular field | [`lark-base-field-create.md`](references/lark-base-field-create.md), [`lark-base-field-update.md`](references/lark-base-field-update.md), [`lark-base-field-delete.md`](references/lark-base-field-delete.md), [`lark-base-shortcut-field-properties.md`](references/lark-base-shortcut-field-properties.md) | Read field-property spec before writing fields; if type is `formula / lookup`, read the corresponding guide first; if user has already specified the target, delete may run directly with `yes: true` |
| `lark_api({tool:'base', op:'field-search-options'})` | Query selectable options of a field | [`lark-base-field-search-options.md`](references/lark-base-field-search-options.md) | Suitable for single/multi-select option fields |

#### 2.3.3 Record sub-module

Sub-module index: [`references/lark-base-record.md`](references/lark-base-record.md), [`references/lark-base-history.md`](references/lark-base-history.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'record-search'})` / `lark_api({tool:'base', op:'record-list'})` / `lark_api({tool:'base', op:'record-get'})` | Search records by keyword, list / paginate / export record details, or get a single record | [`lark-base-record-search.md`](references/lark-base-record-search.md), [`lark-base-record-list.md`](references/lark-base-record-list.md), [`lark-base-record-get.md`](references/lark-base-record-get.md) | Default to `record-list`; only use `record-search` when the user supplies an explicit search keyword; do not use record retrieval for aggregation analysis; `limit` max `200`; only continue paging when the user explicitly requires more data; `record-list` must run serial |
| `lark_api({tool:'base', op:'record-upsert'})` / `lark_api({tool:'base', op:'record-batch-create'})` / `lark_api({tool:'base', op:'record-batch-update'})` | Create, update, or batch-write records | [`lark-base-record-upsert.md`](references/lark-base-record-upsert.md), [`lark-base-record-batch-create.md`](references/lark-base-record-batch-create.md), [`lark-base-record-batch-update.md`](references/lark-base-record-batch-update.md), [`lark-base-shortcut-record-value.md`](references/lark-base-shortcut-record-value.md) | Call `field-list` before writing; only write storage fields; `record-batch-update` is same-value update (one patch applied to many records); single-batch limit is `200` records; do not route attachments through here |
| Two-step attachment upload: (1) `lark_api({tool:'drive', op:'upload'})` returns `file_token`; (2) `lark_api({tool:'base', op:'record-upsert'})` writes the attachment field referencing that `file_token` | Upload an attachment to an existing record | [`lark-base-record-upload-attachment.md`](references/lark-base-record-upload-attachment.md) | Dedicated attachment-upload flow; do not fake attachment values by skipping the upload step or hand-crafting raw values |
| `lark_api({tool:'docs', op:'media-download'})` | Download a Base attachment file locally | [`../lark-doc/references/lark-doc-media-download.md`](../lark-doc/references/lark-doc-media-download.md) | The `file_token` for a Base attachment comes from the attachment-field array returned by `record-get`; **do NOT use `lark_api({tool:'drive', op:'download'})`** — it returns 403 for Base attachments |
| `lark_api({tool:'base', op:'record-delete'})` / `lark_api({tool:'base', op:'record-history-list'})` | Delete a record, or query change history of a record | [`lark-base-record-delete.md`](references/lark-base-record-delete.md), [`lark-base-record-history-list.md`](references/lark-base-record-history-list.md) | If user has already specified the target, delete may run directly with `yes: true`; history is queried by `table-id + record-id`, no full-table scan; `record-history-list` must run serial |

#### 2.3.4 View sub-module

Sub-module index: [`references/lark-base-view.md`](references/lark-base-view.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'view-list'})` / `lark_api({tool:'base', op:'view-get'})` | List views, or get a single view | [`lark-base-view-list.md`](references/lark-base-view-list.md), [`lark-base-view-get.md`](references/lark-base-view-get.md) | `view-list` must run serial; `view-get` is for inspecting an existing view config |
| `lark_api({tool:'base', op:'view-create'})` / `lark_api({tool:'base', op:'view-delete'})` / `lark_api({tool:'base', op:'view-rename'})` | Create, delete, or rename a view | [`lark-base-view-create.md`](references/lark-base-view-create.md), [`lark-base-view-delete.md`](references/lark-base-view-delete.md), [`lark-base-view-rename.md`](references/lark-base-view-rename.md) | Confirm table and view type before create; confirm target before delete; if user has stated the new name, rename may run directly |
| `lark_api({tool:'base', op:'view-get-filter'})` / `lark_api({tool:'base', op:'view-set-filter'})` | Read or configure filter conditions | [`lark-base-view-get-filter.md`](references/lark-base-view-get-filter.md), [`lark-base-view-set-filter.md`](references/lark-base-view-set-filter.md), [`lark-base-record-list.md`](references/lark-base-record-list.md) | Often combined with `record-list` to read records under a view filter |
| `lark_api({tool:'base', op:'view-get-sort'})` / `lark_api({tool:'base', op:'view-set-sort'})` | Read or configure sort | [`lark-base-view-get-sort.md`](references/lark-base-view-get-sort.md), [`lark-base-view-set-sort.md`](references/lark-base-view-set-sort.md) | Field names must come from real schema |
| `lark_api({tool:'base', op:'view-get-group'})` / `lark_api({tool:'base', op:'view-set-group'})` | Read or configure grouping | [`lark-base-view-get-group.md`](references/lark-base-view-get-group.md), [`lark-base-view-set-group.md`](references/lark-base-view-set-group.md) | Field names must come from real schema |
| `lark_api({tool:'base', op:'view-get-visible-fields'})` / `lark_api({tool:'base', op:'view-set-visible-fields'})` | Read or configure visible fields of a view | [`lark-base-view-get-visible-fields.md`](references/lark-base-view-get-visible-fields.md), [`lark-base-view-set-visible-fields.md`](references/lark-base-view-set-visible-fields.md) | Used to control field order and visibility in a view; field names must come from real schema |
| `lark_api({tool:'base', op:'view-get-card'})` / `lark_api({tool:'base', op:'view-set-card'})` | Read or configure card view | [`lark-base-view-get-card.md`](references/lark-base-view-get-card.md), [`lark-base-view-set-card.md`](references/lark-base-view-set-card.md) | Suitable for card-display scenarios |
| `lark_api({tool:'base', op:'view-get-timebar'})` / `lark_api({tool:'base', op:'view-set-timebar'})` | Read or configure timebar view | [`lark-base-view-get-timebar.md`](references/lark-base-view-get-timebar.md), [`lark-base-view-set-timebar.md`](references/lark-base-view-set-timebar.md) | Suitable for timeline scenarios |

### 2.4 Formula / Lookup module

If the user's intent involves derived metrics, conditional logic, text processing, date diff, cross-table computation, or cross-table filtered value retrieval, decide first whether to enter this module.

Default to `formula`: suits routine computation, conditional logic, text processing, date diff, cross-table aggregation, and any derived result that should be persisted in-table.
Use `lookup` only when the user explicitly requests it, or when the scenario naturally fits `from / select / where / aggregate` fixed-lookup modeling.

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'field-create', args:{ type: 'formula', ... }})` | Create a formula field | [`formula-field-guide.md`](references/formula-field-guide.md), [`lark-base-field-create.md`](references/lark-base-field-create.md), [`lark-base-shortcut-field-properties.md`](references/lark-base-shortcut-field-properties.md) | Do not create before reading the guide |
| `lark_api({tool:'base', op:'field-update', args:{ type: 'formula', ... }})` | Update a formula field | [`formula-field-guide.md`](references/formula-field-guide.md), [`lark-base-field-update.md`](references/lark-base-field-update.md), [`lark-base-shortcut-field-properties.md`](references/lark-base-shortcut-field-properties.md) | Get current table schema first |
| `lark_api({tool:'base', op:'field-create', args:{ type: 'lookup', ... }})` | Create a lookup field | [`lookup-field-guide.md`](references/lookup-field-guide.md), [`lark-base-field-create.md`](references/lark-base-field-create.md), [`lark-base-shortcut-field-properties.md`](references/lark-base-shortcut-field-properties.md) | Do not create before reading the guide |
| `lark_api({tool:'base', op:'field-update', args:{ type: 'lookup', ... }})` | Update a lookup field | [`lookup-field-guide.md`](references/lookup-field-guide.md), [`lark-base-field-update.md`](references/lark-base-field-update.md), [`lark-base-shortcut-field-properties.md`](references/lark-base-shortcut-field-properties.md) | Cross-table also requires the target table schema |

### 2.5 Data analysis module

For one-off analysis and ad-hoc aggregation queries. When the user wants "the result computed this time" rather than persisting it as a field, prefer this module.

Confirm a few things before entering this module:

- `data-query` only does aggregation queries (group, filter, sort, aggregate compute) — not raw record listing or per-row detail.
- The caller MUST be an admin of the target Base with FA (Full Access), otherwise a permission error is returned.
- `data-query` only supports a whitelisted set of field types; `formula`, `lookup`, attachment, system fields, link fields cannot be used in `dimensions / measures / filters / sort`.

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'data-query'})` | Grouped statistics, SUM / AVG / COUNT / MAX / MIN, conditional aggregation analysis | [`lark-base-data-query.md`](references/lark-base-data-query.md) | Field names must exactly match real ones; do not pull all rows via `record-list` / `record-search` and compute manually; `data-query` does not return raw records; verify permission and field-type support before use |

### 2.6 Workflow module

This is a high-constraint module. Before any workflow operation, read the corresponding command doc and schema.
Module index: [`references/lark-base-workflow.md`](references/lark-base-workflow.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'workflow-list'})` / `lark_api({tool:'base', op:'workflow-get'})` | List workflows, or get a complete workflow structure | [`lark-base-workflow-list.md`](references/lark-base-workflow-list.md), [`lark-base-workflow-get.md`](references/lark-base-workflow-get.md), [`lark-base-workflow-schema.md`](references/lark-base-workflow-schema.md) | `workflow-list` returns summaries only and must run serial; use `workflow-get` for full structure |
| `lark_api({tool:'base', op:'workflow-create'})` / `lark_api({tool:'base', op:'workflow-update'})` | Create or update a workflow | [`lark-base-workflow-create.md`](references/lark-base-workflow-create.md), [`lark-base-workflow-update.md`](references/lark-base-workflow-update.md), [`lark-base-workflow-schema.md`](references/lark-base-workflow-schema.md) | Read schema first; do NOT guess `type` from natural language; confirm real table and field names first |
| `lark_api({tool:'base', op:'workflow-enable'})` / `lark_api({tool:'base', op:'workflow-disable'})` | Enable or disable a workflow | [`lark-base-workflow-enable.md`](references/lark-base-workflow-enable.md), [`lark-base-workflow-disable.md`](references/lark-base-workflow-disable.md), [`lark-base-workflow-schema.md`](references/lark-base-workflow-schema.md) | Confirm the target workflow before enable/disable; `workflow_id` and `table_id` must be distinguished by prefix |

### 2.7 Dashboard module

When the user mentions keywords such as "dashboard, data board, chart, visualization, block, component, add component, create chart", enter this module and read [`lark-base-dashboard.md`](references/lark-base-dashboard.md) first.

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'dashboard-list'})` / `lark_api({tool:'base', op:'dashboard-get'})` | List dashboards, or get dashboard details | [`lark-base-dashboard-list.md`](references/lark-base-dashboard-list.md), [`lark-base-dashboard-get.md`](references/lark-base-dashboard-get.md), [`lark-base-dashboard.md`](references/lark-base-dashboard.md) | Read the guide once dashboard semantics are entered; `dashboard-list` must run serial |
| `lark_api({tool:'base', op:'dashboard-create'})` / `lark_api({tool:'base', op:'dashboard-update'})` / `lark_api({tool:'base', op:'dashboard-delete'})` | Create, update, or delete a dashboard | [`lark-base-dashboard-create.md`](references/lark-base-dashboard-create.md), [`lark-base-dashboard-update.md`](references/lark-base-dashboard-update.md), [`lark-base-dashboard-delete.md`](references/lark-base-dashboard-delete.md), [`lark-base-dashboard.md`](references/lark-base-dashboard.md) | Clarify dashboard goals and display scenario before create; read current config before update; confirm target before delete |
| `lark_api({tool:'base', op:'dashboard-block-list'})` / `lark_api({tool:'base', op:'dashboard-block-get'})` | List chart blocks, or get a single block | [`lark-base-dashboard-block-list.md`](references/lark-base-dashboard-block-list.md), [`lark-base-dashboard-block-get.md`](references/lark-base-dashboard-block-get.md), [`lark-base-dashboard.md`](references/lark-base-dashboard.md), [`dashboard-block-data-config.md`](references/dashboard-block-data-config.md) | `dashboard-block-list` must run serial; read block-config doc when inspecting config details |
| `lark_api({tool:'base', op:'dashboard-block-create'})` / `lark_api({tool:'base', op:'dashboard-block-update'})` / `lark_api({tool:'base', op:'dashboard-block-delete'})` | Create, update, or delete a chart block | [`lark-base-dashboard-block-create.md`](references/lark-base-dashboard-block-create.md), [`lark-base-dashboard-block-update.md`](references/lark-base-dashboard-block-update.md), [`lark-base-dashboard-block-delete.md`](references/lark-base-dashboard-block-delete.md), [`lark-base-dashboard.md`](references/lark-base-dashboard.md), [`dashboard-block-data-config.md`](references/dashboard-block-data-config.md) | When `data_config`, chart type, or filter is involved, read the block-config doc; confirm target before delete |

### 2.8 Form module

Manages forms and form questions.
Module index: [`references/lark-base-form.md`](references/lark-base-form.md), [`references/lark-base-form-questions.md`](references/lark-base-form-questions.md)
Form-question operations require `form-id`; see the references for `form-list` and `form-create` for how to obtain it.

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'form-list'})` / `lark_api({tool:'base', op:'form-get'})` | List forms, or get a single form | [`lark-base-form-list.md`](references/lark-base-form-list.md), [`lark-base-form-get.md`](references/lark-base-form-get.md) | `form-list` is the source of `form-id`; `form-get` is for inspecting an existing form |
| `lark_api({tool:'base', op:'form-create'})` / `lark_api({tool:'base', op:'form-update'})` / `lark_api({tool:'base', op:'form-delete'})` | Create, update, or delete a form | [`lark-base-form-create.md`](references/lark-base-form-create.md), [`lark-base-form-update.md`](references/lark-base-form-update.md), [`lark-base-form-delete.md`](references/lark-base-form-delete.md) | After create, may continue into form-question ops; confirm the target form before update or delete |
| `lark_api({tool:'base', op:'form-questions-list'})` | List form questions | [`lark-base-form-questions-list.md`](references/lark-base-form-questions-list.md) | For inspecting an existing question structure |
| `lark_api({tool:'base', op:'form-questions-create'})` / `lark_api({tool:'base', op:'form-questions-update'})` / `lark_api({tool:'base', op:'form-questions-delete'})` | Create, update, or delete questions | [`lark-base-form-questions-create.md`](references/lark-base-form-questions-create.md), [`lark-base-form-questions-update.md`](references/lark-base-form-questions-update.md), [`lark-base-form-questions-delete.md`](references/lark-base-form-questions-delete.md) | Confirm `form-id` first; confirm question target before update or delete |

### 2.9 Permission & role module

For enabling advanced permissions and managing Base custom roles.
Calling `advperm-enable / advperm-disable / role-*` requires the operating user to be a Base admin, otherwise a permission error is returned.

| Operation | Purpose / when to use | Required reference | Routing reminder |
|---|---|---|---|
| `lark_api({tool:'base', op:'advperm-enable'})` / `lark_api({tool:'base', op:'advperm-disable'})` | Enable or disable advanced permissions | [`lark-base-advperm-enable.md`](references/lark-base-advperm-enable.md), [`lark-base-advperm-disable.md`](references/lark-base-advperm-disable.md) | Must be enabled before role management; disabling is high risk and invalidates existing custom roles |
| `lark_api({tool:'base', op:'role-list'})` / `lark_api({tool:'base', op:'role-get'})` | List roles, or get role details | [`lark-base-role-list.md`](references/lark-base-role-list.md), [`lark-base-role-get.md`](references/lark-base-role-get.md), [`role-config.md`](references/role-config.md) | `role-list` must run serial; `role-get` is for inspecting full permission config |
| `lark_api({tool:'base', op:'role-create'})` / `lark_api({tool:'base', op:'role-update'})` / `lark_api({tool:'base', op:'role-delete'})` | Create, update, or delete a role | [`lark-base-role-create.md`](references/lark-base-role-create.md), [`lark-base-role-update.md`](references/lark-base-role-update.md), [`lark-base-role-delete.md`](references/lark-base-role-delete.md), [`role-config.md`](references/role-config.md) | `role-create` only supports `custom_role`; `role-update` uses Delta Merge — `role_name` and `role_type` must always be supplied even if unchanged; `role-delete` is irreversible |

## 3. Bitable common knowledge

Lark Base's English name is `Base`; its legacy name is `Bitable`. Therefore `bitable` appearing in old docs, return fields, params, or error messages is mostly historical compatibility — it does NOT mean another command set should be used.

### 3.1 Field categories and writability

| Field type | Meaning | Can be a direct write target for `record-upsert / record-batch-create / record-batch-update`? | Notes |
|---|---|---|---|
| Storage field | Holds real user input | Yes | Common: text, number, date, single select, multi select, user, link |
| Attachment field | Holds file attachments | Should not be written like a normal field | Upload via two-step flow: `lark_api({tool:'drive', op:'upload'})` then `lark_api({tool:'base', op:'record-upsert'})` with the returned `file_token`; download via `lark_api({tool:'docs', op:'media-download'})` |
| System field | Maintained by the platform | No | Common: created time, updated time, created by, modified by, auto number |
| `formula` field | Computed from an expression | No | Read-only |
| `lookup` field | Cross-table lookup reference | No | Read-only |

### 3.2 Task-routing mental model

| User intent | Preferred path | Do not mistake for |
|---|---|---|
| One-off analysis / ad-hoc statistics | `lark_api({tool:'base', op:'data-query'})` | Do not pull everything via `record-list` / `record-search` then compute manually |
| Result must persist in the table long term | formula field | Do not return only a one-shot manual analysis |
| User explicitly requests lookup, or it's naturally a fixed lookup configuration | lookup field | Do not default to lookup; first decide whether formula is more suitable |
| Read raw record details / keyword search / export | `lark_api({tool:'base', op:'record-search'})` / `record-list` / `record-get` | Do not use `data-query` as a record-fetching command |
| Upload an attachment to a record | Two-step: `lark_api({tool:'drive', op:'upload'})` then `lark_api({tool:'base', op:'record-upsert'})` writing the returned `file_token` into the attachment field | Do not fake attachment values via raw `record-upsert` / `record-batch-*` payloads bypassing the upload step |
| Download an attachment file from a record | `lark_api({tool:'docs', op:'media-download', args:{ token: '<file_token>', output: '<path>' }})` | `file_token` comes from the attachment field returned by `record-get`; usage in [`../lark-doc/references/lark-doc-media-download.md`](../lark-doc/references/lark-doc-media-download.md) |
| Read records via a view filter | `view-set-filter` + `record-list` | Do not skip the view filter and guess conditions |
| Import a local Excel / CSV as Base | `lark_api({tool:'drive', op:'import', args:{ type: 'bitable', ... }})` | Do not mistakenly call `base-create`, `table-create`, or `record-upsert` |

### 3.3 Table names, field names, and expression references

1. Table and field names must exactly match the real return; the source must be `table-list / table-get / field-list`.
2. Do not guess names from natural language; do not silently rewrite table/field names from the user's verbal description.
3. Names appearing in `formula / lookup / data-query / workflow` must also match exactly; expression references, where conditions, DSL field names, workflow configs all obey the same rule.
4. Cross-table scenarios additionally require reading the target table schema — current-table-only is not enough.

### 3.4 Token and link

This is a high-priority section. Whenever input contains a link or token, or an error mentions `baseToken` / `wiki_token` / `obj_token`, return here first to check.

| Input type | Correct handling | Notes |
|---|---|---|
| Direct Base link `/base/{token}` | Extract token directly as `base_token` arg | Do not pass the full URL as `base_token` |
| Wiki link `/wiki/{token}` | First call `lark_api` with `{ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_token>' } }`, then take `node.obj_token` | Do not pass `wiki_token` directly as `base_token` |
| `?table={id}` in URL | Decide object type by prefix first | `tbl` prefix = data table `table_id` arg; `blk` prefix = dashboard `dashboard_id`; `wkf` prefix = `workflow_id`; `ldx` prefix = embedded doc — do NOT treat all of these as `table_id` |
| `?view={id}` in URL | Extract as `view_id` arg | Suitable for direct view targeting |

| `obj_type` returned by the wiki `get_node` HTTP call above | Follow-up route | Notes |
|---|---|---|
| `bitable` | Prefer `lark_api({tool:'base', op:'...'})` | If a typed op is missing, do NOT fall back to raw `/open-apis/bitable/v1/...`; check the catalog first |
| `docx` | Switch to docs / Drive related skill | Do not continue with this skill's Base ops |
| `sheet` | Switch to Sheets-related skill | Do not continue with this skill's Base ops |
| `slides` | Switch to Drive-related skill | Do not continue with this skill's Base ops |
| `mindnote` | Switch to Drive-related skill | Do not continue with this skill's Base ops |

### 3.5 Identity selection and permission-fallback strategy

Lark Base usually belongs to a user's personal or team resources. **Default to user identity for all Base operations**, and always specify identity explicitly via the active profile.

- **User identity (recommended)**: operate as the logged-in user against Bases they have access to. Complete user authorization first via the LarkSkill MCP auth flow:

```
Call MCP tool `lark_auth_login`:
- domain: "base"
```

Then `lark_auth_poll` to wait for authorization, and confirm via `lark_whoami` / `lark_auth_status`.

- **Bot identity (fallback)**: only when user-identity permission is insufficient AND bot identity actually has access to the target Base. Bots cannot see user-private resources; behavior runs under the app identity. Switch via `lark_profile_switch`.

**Execution rules**:

1. All ops default to user identity.
2. If user identity returns a permission error, first check whether it is a **non-retryable error code** (e.g. `91403`). If so, **stop immediately** — do not retry or fall back. Follow the `lark-shared` insufficient-permission flow to guide the user.
3. For retryable codes, check the error response for hints like `permission_violations` / `hint` indicating scope-elevation:
   - **Has elevation hint**: follow the `lark-shared` flow to guide the user through user-identity scope elevation (re-run `lark_auth_login` with the requested scope, or `lark_enable_domain`); after confirmation, retry as user.
   - **No elevation hint** (e.g. resource-level access denied, not a scope issue): switch to bot identity via `lark_profile_switch` and retry **once**.
4. If bot identity also returns a permission error, **stop retrying immediately**, and per the error response follow the `lark-shared` flow to guide the user (developer-console scope or resource-access).
5. Only when the user explicitly says "use app identity / bot identity", skip user and go straight to bot via `lark_profile_switch`.

**Additional notes**:

- User / person fields: pay attention to `user_id_type` differences vs. execution identity (user / bot).

## 4. Execution rules

### 4.1 Standard execution order

1. Decide which module the task belongs to and pick the right operation family.
2. If the user gave a link, parse the token first — do not mistake a wiki token, full URL, or other object ID for `base_token`.
3. Get schema before writing ops; avoid guessing table names, field names, expression references.
4. After locating the operation, read the corresponding reference, then execute.
5. Execute and decide next step from the return value.
6. Reply with the key result and follow-up actions, so the agent can continue chaining.

### 4.2 Inviolable rules

1. Get schema before writing ops; at minimum get current table schema, and target table for cross-table.
2. Do not guess table names, field names, or expression references — always honor the real return.
3. Use only atomic ops; do not regress to legacy aggregated forms `+table / +field / +record / +view / +history / +workspace`.
4. Read field schema before writing records; call `field-list` first, then build write values per field type.
5. Read field-property spec before writing fields; read `lark-base-shortcut-field-properties.md` first, then build the JSON for `field-create / field-update`.
6. Only write writable fields; system fields, attachment fields, `formula`, `lookup` are NOT default write targets in record ops.
7. Aggregation analysis vs. retrieval are split: stats go to `data-query`, keyword search goes to `record-search`, details go to `record-list / record-get`.
8. Filtered queries go through view capability: configure with `view-set-filter` first, then read with `record-list`.
9. In Base scenarios, do not bypass the catalog and call raw `/open-apis/bitable/v1/...` paths.
10. Use `base_token` uniformly in args; do not use the legacy `app_token` style.
11. In workflow scenarios, read schema first; do not guess `type` from natural language.
12. In dashboard scenarios, read the guide first; once chart / board / block is mentioned, enter the dashboard module.
13. In formula / lookup scenarios, read the guide first; do not create or update before reading the guide.

### 4.3 Concurrency, pagination, and batching limits

- `table-list / field-list / record-list / view-list / record-history-list / role-list / dashboard-list / dashboard-block-list / workflow-list` MUST NOT be called concurrently — serial only.
- For `record-list` pagination, `limit` max is `200`; first fetch the initial batch and inspect `has_more`, only continue paging when the user explicitly requires more data.
- Batch writes are capped at `200` records per call.
- Continuous writes against the same table MUST be serial, with `0.5–1` second delay between batches.

### 4.4 Confirmation and reply rules

- For view rename, when the user has clearly stated "which view, what new name", call `view-rename` directly.
- For deleting records / fields / tables, when the user has clearly requested deletion AND the target is unambiguous, call `record-delete / field-delete / table-delete` directly with `yes: true` arg.
- When the delete target is still ambiguous, call `record-get / field-get / table-get` or the corresponding list to confirm first.
- After `base-create / base-copy` succeeds, the reply MUST proactively return identifiers for the new Base; if the result includes an accessible link, return it as well.
- If a Base was created or copied under bot identity, the op auto-attempts to grant the current CLI user `full_access`, returning `permission_grant` in the output; the agent does NOT need to orchestrate a separate grant. Owner transfer must be confirmed separately and never executed implicitly.

## 5. Common errors and recovery

| Error / symptom | Meaning | Recovery |
|---|---|---|
| `1254064` | Date format error | Use millisecond timestamp, not string / second-level timestamp |
| `1254068` | Hyperlink format error | Use `{text, link}` object |
| `1254066` | User-field error | Use `[{id:"ou_xxx"}]` and confirm `user_id_type` |
| `1254045` | Field name not found | Check field name (spaces, case included) |
| `1254015` | Field value type mismatch | Call `field-list` first, then build by type |
| `param baseToken is invalid` / `base_token invalid` | A wiki token, workspace token, or other token was used as `base_token` | If input came from `/wiki/...`, call `lark_api` with `{ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_token>' } }` to get the real `obj_token`; when `obj_type=bitable`, retry with `node.obj_token` as `base_token`; do not switch to raw `bitable/v1` |
| `not found` when user gave a wiki link | Common when wiki token is mistaken for base token | Roll back and re-check wiki resolution; do not switch to raw `bitable/v1` |
| formula / lookup creation fails | Guide not read or invalid structure | Read `formula-field-guide.md` / `lookup-field-guide.md` first, rebuild request per guide |
| System field / formula field write fails | A read-only field treated as writable | Write storage fields; let formula / lookup / system fields produce computed outputs |
| `1254104` | Batch over 200 records | Split into batches |
| `1254291` | Concurrent write conflict | Serial writes + delay between batches |
| `91403` | No permission to access the Base | **Do NOT retry**. Follow the `lark-shared` insufficient-permission flow to guide the user |
