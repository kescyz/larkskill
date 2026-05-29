---
name: lark-base
version: 2.0.0
description: "Use this skill when operating Lark Base via LarkSkill MCP: search Base, create tables, manage fields, record read/write, share links, view config, history, role/form/dashboard/workflow. Mandatory for formula fields, lookup references, cross-table computation, row-level derived metrics, and data analysis."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# base

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first.
> **Mandatory before execution:** Before invoking any `base` operation, read the corresponding command reference doc first, then call the operation via `lark_api`.
> **Mandatory for query tasks:** When the task involves filtering, sorting, Top/Bottom N, aggregation, multi-table joins, post-query writes, or drawing a global conclusion, MUST read [`references/lark-base-data-analysis-sop.md`](references/lark-base-data-analysis-sop.md) first, then choose the `record / view / data-query` path.
> **Naming convention:** Base business operations call `lark_api({ tool: 'base', op: '<op>', args: {...} })`; to resolve a Wiki link first, call `lark_api` with the HTTP form `{ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_token>' } }`.
> **Routing rule:** If the user wants to "import a local file as Base / Bitable", the first step is NOT a `base` op — it is `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`. After import completes, return to `lark_api({ tool: 'base', op: '...' })` for in-table operations.

## 1. When to use this Skill

### 1.1 Trigger conditions

This skill should be used for the following scenarios:

- The user explicitly wants to operate Lark Base / Bitable.
- The user wants to create / modify / query / delete tables, or manage fields, records, views.
- The user wants formula fields, lookup fields, derived metrics, or cross-table computation.
- The user wants ad-hoc statistics, aggregation analysis, comparison / sorting, or extreme-value retrieval.
- The user wants to manage workflow, dashboard, form, or role permissions.
- The user gives a `/base/{token}` link.
- The user gives a `/wiki/{token}` link that ultimately resolves to `bitable`.
- The user wants to rewrite legacy aggregated Base forms into the current atomic operation form, e.g. translating legacy `+table / +field / +record / +view / +history / +workspace` into current ops.

This skill should NOT be used for the following:

- The user is only doing auth, init configuration, switching identity, or handling scope. Read `../lark-shared/SKILL.md` first.
- The user is only generally discussing "data analysis / field design" but is NOT actually in a Base scenario. Do NOT trigger merely because the words "statistics / formula / lookup" appear.

### 1.2 Prerequisites

1. Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first.
2. Base business operations call `lark_api({ tool: 'base', op: '<op>', args: {...} })`. If the input is a Wiki link or Wiki token and the user wants to read/operate the Base inside it, first call `lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_url_or_token>' } })`; when it returns `node.obj_type=bitable`, use `node.obj_token` as the `base_token` arg. Do NOT treat the `/wiki/{token}` in the URL as a Base token.
3. After locating the operation, read its corresponding reference first, then execute it.
4. If the user wants to import a local Excel / CSV / `.base` snapshot as Base / Bitable, the first step is NOT a `base` op — it is `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`; after import, return to `lark_api({ tool: 'base', op: '...' })` for in-table operations.
5. Do NOT bypass the catalog and call raw `/open-apis/bitable/v1/...` paths in Base scenarios.
6. If the user only gives a Base name or keyword, or says "find me a Base", first search Base / Bitable resources via `lark_api({ tool: 'docs', op: 'search', args: { query: '<keyword>', filter: { doc_types: ['BITABLE'] } } })`; after getting the Base URL, use this skill's `base` ops. For complex searches, read [`../lark-drive/references/lark-drive-search.md`](../lark-drive/references/lark-drive-search.md): exact title match, scoping by owner (`mine` / `creator_ids`, where owner does NOT mean "original creator") / chat / folder / time range, title-only / comment-only search, paginated / full search.

## 2. Module and operation navigation

This chapter is organized "pick the module first, then pick the operation". Decide which large module the user's goal belongs to, enter the corresponding sub-module, read the reference per requirements, then execute the operation.

### 2.1 Module map

| Large module | What problem it handles | Sub-modules / capabilities |
|------|-------------|-------------------|
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
|------|------------------|----------------|----------|
| `lark_api({ tool: 'docs', op: 'search', args: { query: '<keyword>', filter: { doc_types: ['BITABLE'] } } })` | Search for a Base / Bitable by name or keyword | For complex searches, also read [`../lark-drive/references/lark-drive-search.md`](../lark-drive/references/lark-drive-search.md) | Locate the resource first, then return to `base` ops to operate in-table |
| `lark_api({tool:'base', op:'base-create'})` | Create a new Base | [`lark-base-base-create.md`](references/lark-base-base-create.md), [`lark-base-workspace.md`](references/lark-base-workspace.md) | Write op; read reference first; `folder_token`, `time_zone` are optional |
| `lark_api({tool:'base', op:'base-get'})` | Get Base info | [`lark-base-base-get.md`](references/lark-base-base-get.md), [`lark-base-workspace.md`](references/lark-base-workspace.md) | Suitable for confirming Base identity; not a substitute for table/field structure reads |
| `lark_api({tool:'base', op:'base-copy'})` | Copy an existing Base | [`lark-base-base-copy.md`](references/lark-base-base-copy.md), [`lark-base-workspace.md`](references/lark-base-workspace.md) | Write op; read reference first; on success, proactively return new Base identifiers |

### 2.3 Table & data module

This is the most-used module, including four sub-modules: `table / field / record / view`.
Supplemental examples: [`references/examples.md`](references/examples.md) — read when chaining table / record / view operations end-to-end.

#### 2.3.1 Table sub-module

Sub-module index: [`references/lark-base-table.md`](references/lark-base-table.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|------|------------------|----------------|----------|
| `lark_api({tool:'base', op:'table-list'})` / `lark_api({tool:'base', op:'table-get'})` | List data tables, or get details of a single table | [`lark-base-table-list.md`](references/lark-base-table-list.md), [`lark-base-table-get.md`](references/lark-base-table-get.md) | `table-list` must run serial; `table-get` is for confirming a target before delete/update |
| `lark_api({tool:'base', op:'table-create'})` / `lark_api({tool:'base', op:'table-update'})` / `lark_api({tool:'base', op:'table-delete'})` | Create, update, or delete a table | [`lark-base-table-create.md`](references/lark-base-table-create.md), [`lark-base-table-update.md`](references/lark-base-table-update.md), [`lark-base-table-delete.md`](references/lark-base-table-delete.md) | Create suits one-off table builds; update requires confirming the target first; if user has stated the target, delete may run directly with `yes: true` |

#### 2.3.2 Field sub-module

Regular field management goes here; if the field type is `formula` or `lookup`, switch to the "Formula / Lookup module" below.
Sub-module index: [`references/lark-base-field.md`](references/lark-base-field.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|------|------------------|----------------|----------|
| `lark_api({tool:'base', op:'field-list'})` / `lark_api({tool:'base', op:'field-get'})` | List field schema, or get details of a single field | [`lark-base-field-list.md`](references/lark-base-field-list.md), [`lark-base-field-get.md`](references/lark-base-field-get.md) | Before writing records / fields / running analysis, usually call `field-list` first; `field-list` must run serial; `field-get` is for confirming a target before delete/update |
| `lark_api({tool:'base', op:'field-create'})` / `lark_api({tool:'base', op:'field-update'})` / `lark_api({tool:'base', op:'field-delete'})` | Create, update, or delete a regular field | [`lark-base-field-create.md`](references/lark-base-field-create.md), [`lark-base-field-update.md`](references/lark-base-field-update.md), [`lark-base-field-delete.md`](references/lark-base-field-delete.md), [`lark-base-shortcut-field-properties.md`](references/lark-base-shortcut-field-properties.md) | Read the field-property spec before writing fields; for type conversions, follow the type-change rules in `field-update` — only consider in-place conversion for safe-whitelist types; if type is `formula / lookup`, read the corresponding guide first; if user has stated the target, update or delete may run directly with `yes: true` |
| `lark_api({tool:'base', op:'field-search-options'})` | Query selectable options of a field | [`lark-base-field-search-options.md`](references/lark-base-field-search-options.md) | Suitable for single/multi-select option fields |

#### 2.3.3 Record sub-module

Sub-module index: [`references/lark-base-record.md`](references/lark-base-record.md), [`references/lark-base-history.md`](references/lark-base-history.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|------|------------------|----------------|----------|
| `lark_api({tool:'base', op:'record-search'})` / `lark_api({tool:'base', op:'record-list'})` / `lark_api({tool:'base', op:'record-get'})` | Search records by keyword, list / paginate / export record details, or get one or more records by ID | [`lark-base-data-analysis-sop.md`](references/lark-base-data-analysis-sop.md) | For all record reads, first read the data analysis SOP: use `record-get` when `record_id` is known; `record-search` when an explicit keyword is given; `record-list` for general details; project into a temporary view then `record-list` with `view_id` for explicit filtering / sorting / Top N; route to `data-query` only for aggregation; `record-get` supports multiple `record_id` values |
| `lark_api({tool:'base', op:'record-upsert'})` / `lark_api({tool:'base', op:'record-batch-create'})` / `lark_api({tool:'base', op:'record-batch-update'})` | Create, update, or batch-write records | [`lark-base-record-upsert.md`](references/lark-base-record-upsert.md), [`lark-base-record-batch-create.md`](references/lark-base-record-batch-create.md), [`lark-base-record-batch-update.md`](references/lark-base-record-batch-update.md), [`lark-base-cell-value.md`](references/lark-base-cell-value.md) | Call `field-list` before writing; only write storage fields; `record-batch-update` is same-value update (one patch applied to many records); single-batch limit is `200` records; do not route attachments through here |
| `lark_api({tool:'base', op:'record-upload-attachment'})` | Upload one or more attachments to an existing record | See `lark_api_search({ query: 'base record-upload-attachment' })` for args | Dedicated attachment-upload flow; do not fake attachment values via `record-upsert` / `record-batch-*` |
| `lark_api({tool:'base', op:'record-download-attachment'})` | Download one or more Base attachments locally | See `lark_api_search({ query: 'base record-download-attachment' })` for args | Base attachments MUST be downloaded via this operation; other download paths may fail |
| `lark_api({tool:'base', op:'record-remove-attachment'})` | Remove one or more attachments from an attachment field | See `lark_api_search({ query: 'base record-remove-attachment' })` for args | Destructive op; confirm the target, then use `yes: true` |
| `lark_api({tool:'base', op:'record-delete'})` | Delete one or more records | [`lark-base-record-delete.md`](references/lark-base-record-delete.md) | For multiple records, supply an array of `record_id`; if user has stated the target, delete may run directly with `yes: true` |
| `lark_api({tool:'base', op:'record-history-list'})` | Query change history of a specified record | [`lark-base-record-history-list.md`](references/lark-base-record-history-list.md) | Queried by `table_id + record_id`, no full-table scan; `record-history-list` must run serial |
| `lark_api({tool:'base', op:'record-share-link-create'})` | Generate share links for one or more records | [`lark-base-record-share-link-create.md`](references/lark-base-record-share-link-create.md) | Max 100 records per call; duplicate `record_id` values are auto-deduplicated; suitable for sharing individual or multiple records |

#### 2.3.4 View sub-module

Sub-module index: [`references/lark-base-view.md`](references/lark-base-view.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|------|------------------|----------------|----------|
| `lark_api({tool:'base', op:'view-list'})` / `lark_api({tool:'base', op:'view-get'})` | List views, or get a single view | [`lark-base-view-list.md`](references/lark-base-view-list.md), [`lark-base-view-get.md`](references/lark-base-view-get.md) | `view-list` must run serial; `view-get` is for inspecting an existing view config |
| `lark_api({tool:'base', op:'view-create'})` / `lark_api({tool:'base', op:'view-delete'})` / `lark_api({tool:'base', op:'view-rename'})` | Create, delete, or rename a view | [`lark-base-view-create.md`](references/lark-base-view-create.md), [`lark-base-view-delete.md`](references/lark-base-view-delete.md), [`lark-base-view-rename.md`](references/lark-base-view-rename.md) | Confirm table and view type before create; confirm target before delete; if user has stated the new name, rename may run directly |
| `lark_api({tool:'base', op:'view-get-filter'})` / `lark_api({tool:'base', op:'view-set-filter'})` | Read or configure filter conditions | [`lark-base-view-get-filter.md`](references/lark-base-view-get-filter.md), [`lark-base-view-set-filter.md`](references/lark-base-view-set-filter.md), [`lark-base-data-analysis-sop.md`](references/lark-base-data-analysis-sop.md) | Often combined with `record-list` to read records under a view filter |
| `lark_api({tool:'base', op:'view-get-sort'})` / `lark_api({tool:'base', op:'view-set-sort'})` | Read or configure sort | [`lark-base-view-get-sort.md`](references/lark-base-view-get-sort.md), [`lark-base-view-set-sort.md`](references/lark-base-view-set-sort.md) | Field names must come from real schema |
| `lark_api({tool:'base', op:'view-get-group'})` / `lark_api({tool:'base', op:'view-set-group'})` | Read or configure grouping | [`lark-base-view-get-group.md`](references/lark-base-view-get-group.md), [`lark-base-view-set-group.md`](references/lark-base-view-set-group.md) | Field names must come from real schema |
| `lark_api({tool:'base', op:'view-get-visible-fields'})` / `lark_api({tool:'base', op:'view-set-visible-fields'})` | Read or configure visible fields of a view | [`lark-base-view-get-visible-fields.md`](references/lark-base-view-get-visible-fields.md), [`lark-base-view-set-visible-fields.md`](references/lark-base-view-set-visible-fields.md) | Controls field order and visibility in a view; field names must come from real schema |
| `lark_api({tool:'base', op:'view-get-card'})` / `lark_api({tool:'base', op:'view-set-card'})` | Read or configure card view | [`lark-base-view-get-card.md`](references/lark-base-view-get-card.md), [`lark-base-view-set-card.md`](references/lark-base-view-set-card.md) | Suitable for card-display scenarios |
| `lark_api({tool:'base', op:'view-get-timebar'})` / `lark_api({tool:'base', op:'view-set-timebar'})` | Read or configure timebar view | [`lark-base-view-get-timebar.md`](references/lark-base-view-get-timebar.md), [`lark-base-view-set-timebar.md`](references/lark-base-view-set-timebar.md) | Suitable for timeline scenarios |

### 2.4 Formula / Lookup module

If the user's intent involves derived metrics, conditional logic, text processing, date diff, cross-table computation, or cross-table filtered value retrieval, decide first whether to enter this module.

Default to `formula`: suits routine computation, conditional logic, text processing, date diff, cross-table aggregation, and any derived result that should be persisted in-table.
Use `lookup` only when the user explicitly requests it, or when the scenario naturally fits `from / select / where / aggregate` fixed-lookup modeling.

| Operation | Purpose / when to use | Required reference | Routing reminder |
|------|------------------|----------------|----------|
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
|------|------------------|----------------|----------|
| `lark_api({tool:'base', op:'data-query'})` | Grouped statistics, SUM / AVG / COUNT / MAX / MIN, conditional aggregation analysis | [`lark-base-data-query.md`](references/lark-base-data-query.md) | Field names must exactly match real ones; do not pull all rows via `record-list` / `record-search` and compute manually; `data-query` does not return raw records; verify permission and field-type support before use |

### 2.6 Workflow module

This is a high-constraint module. Before any workflow operation, read the corresponding command doc and schema.
Module index: [`references/lark-base-workflow.md`](references/lark-base-workflow.md)

| Operation | Purpose / when to use | Required reference | Routing reminder |
|------|------------------|----------------|----------|
| `lark_api({tool:'base', op:'workflow-list'})` / `lark_api({tool:'base', op:'workflow-get'})` | List workflows, or get a complete workflow structure | [`lark-base-workflow-list.md`](references/lark-base-workflow-list.md), [`lark-base-workflow-get.md`](references/lark-base-workflow-get.md), [`lark-base-workflow-schema.md`](references/lark-base-workflow-schema.md) | `workflow-list` returns summaries only and must run serial; use `workflow-get` for full structure |
| `lark_api({tool:'base', op:'workflow-create'})` / `lark_api({tool:'base', op:'workflow-update'})` | Create or update a workflow | [`lark-base-workflow-create.md`](references/lark-base-workflow-create.md), [`lark-base-workflow-update.md`](references/lark-base-workflow-update.md), [`lark-base-workflow-schema.md`](references/lark-base-workflow-schema.md) | Read schema first; DO NOT guess `type` from natural language; confirm real table and field names first |
| `lark_api({tool:'base', op:'workflow-enable'})` / `lark_api({tool:'base', op:'workflow-disable'})` | Enable or disable a workflow | [`lark-base-workflow-enable.md`](references/lark-base-workflow-enable.md), [`lark-base-workflow-disable.md`](references/lark-base-workflow-disable.md), [`lark-base-workflow-schema.md`](references/lark-base-workflow-schema.md) | Confirm the target workflow before enable/disable; `workflow_id` and `table_id` must be distinguished by prefix |

### 2.7 Dashboard module

When the user mentions keywords such as "dashboard, data board, chart, visualization, block, component, add component, create chart", enter this module and read [`lark-base-dashboard.md`](references/lark-base-dashboard.md) first.

| Operation | Purpose / when to use | Required reference | Routing reminder |
|------|------------------|----------------|----------|
| `lark_api({tool:'base', op:'dashboard-list'})` / `lark_api({tool:'base', op:'dashboard-get'})` | List dashboards, or get dashboard details | [`lark-base-dashboard-list.md`](references/lark-base-dashboard-list.md), [`lark-base-dashboard-get.md`](references/lark-base-dashboard-get.md), [`lark-base-dashboard.md`](references/lark-base-dashboard.md) | Read the guide once dashboard semantics are entered; `dashboard-list` must run serial |
| `lark_api({tool:'base', op:'dashboard-create'})` / `lark_api({tool:'base', op:'dashboard-update'})` / `lark_api({tool:'base', op:'dashboard-delete'})` | Create, update, or delete a dashboard | [`lark-base-dashboard-create.md`](references/lark-base-dashboard-create.md), [`lark-base-dashboard-update.md`](references/lark-base-dashboard-update.md), [`lark-base-dashboard-delete.md`](references/lark-base-dashboard-delete.md), [`lark-base-dashboard.md`](references/lark-base-dashboard.md) | Clarify dashboard goals and display scenario before create; read current config before update; confirm target before delete |
| `lark_api({tool:'base', op:'dashboard-block-list'})` / `lark_api({tool:'base', op:'dashboard-block-get'})` | List chart blocks, or get a single block | [`lark-base-dashboard-block-list.md`](references/lark-base-dashboard-block-list.md), [`lark-base-dashboard-block-get.md`](references/lark-base-dashboard-block-get.md), [`lark-base-dashboard.md`](references/lark-base-dashboard.md), [`dashboard-block-data-config.md`](references/dashboard-block-data-config.md) | `dashboard-block-list` must run serial; read the block-config doc when inspecting config details |
| `lark_api({tool:'base', op:'dashboard-block-create'})` / `lark_api({tool:'base', op:'dashboard-block-update'})` / `lark_api({tool:'base', op:'dashboard-block-delete'})` | Create, update, or delete a chart block | [`lark-base-dashboard-block-create.md`](references/lark-base-dashboard-block-create.md), [`lark-base-dashboard-block-update.md`](references/lark-base-dashboard-block-update.md), [`lark-base-dashboard-block-delete.md`](references/lark-base-dashboard-block-delete.md), [`lark-base-dashboard.md`](references/lark-base-dashboard.md), [`dashboard-block-data-config.md`](references/dashboard-block-data-config.md) | When `data_config`, chart type, or filter is involved, read the block-config doc; confirm target before delete |

### 2.8 Form module

Manages the form itself and form questions.
Module index: [`references/lark-base-form.md`](references/lark-base-form.md), [`references/lark-base-form-questions.md`](references/lark-base-form-questions.md)
Form-question operations depend on `form_id`; see the references for `form-list` and `form-create` for how to obtain it.

| Operation | Purpose / when to use | Required reference | Routing reminder |
|------|------------------|----------------|----------|
| `lark_api({tool:'base', op:'form-list'})` / `lark_api({tool:'base', op:'form-get'})` | List forms, or get a single form | [`lark-base-form-list.md`](references/lark-base-form-list.md), [`lark-base-form-get.md`](references/lark-base-form-get.md) | `form-list` can be used to obtain `form_id`; `form-get` is for inspecting an existing form config |
| `lark_api_search({ query: 'base form-detail' })` then call the resolved op | Get form details via a form share link (includes question list, field types, validation rules) | [`lark-base-form-detail.md`](references/lark-base-form-detail.md) | Read-only; needs only the `share_token` arg (extracted from the share link), not base_token/table_id/form_id; the returned `questions` can be used directly to build form-submit parameters |
| `lark_api_search({ query: 'base form-submit' })` then call the resolved op | Fill and submit a form via a form share link (supports regular fields + attachment upload) | [`lark-base-form-submit.md`](references/lark-base-form-submit.md) | Write op; supports share_token mode only; **when the submission includes attachments you MUST additionally provide the `base_token` arg** (attachment upload to Base Drive Media requires it); attachments are passed as local paths via the `attachments` arg, and the server uploads them in parallel automatically |
| `lark_api({tool:'base', op:'form-create'})` / `lark_api({tool:'base', op:'form-update'})` / `lark_api({tool:'base', op:'form-delete'})` | Create, update, or delete a form | [`lark-base-form-create.md`](references/lark-base-form-create.md), [`lark-base-form-update.md`](references/lark-base-form-update.md), [`lark-base-form-delete.md`](references/lark-base-form-delete.md) | After create, may continue into form-question operations; confirm the target form before update or delete |
| `lark_api({tool:'base', op:'form-questions-list'})` | List form questions | [`lark-base-form-questions-list.md`](references/lark-base-form-questions-list.md) | For inspecting an existing question structure |
| `lark_api({tool:'base', op:'form-questions-create'})` / `lark_api({tool:'base', op:'form-questions-update'})` / `lark_api({tool:'base', op:'form-questions-delete'})` | Create, update, or delete questions | [`lark-base-form-questions-create.md`](references/lark-base-form-questions-create.md), [`lark-base-form-questions-update.md`](references/lark-base-form-questions-update.md), [`lark-base-form-questions-delete.md`](references/lark-base-form-questions-delete.md) | Confirm `form_id` first; confirm question target before update or delete |

### 2.9 Permission & role module

For enabling advanced permissions and managing Base custom roles.
For `advperm-enable / advperm-disable / role-*`, the operating user MUST be a Base admin, otherwise a permission error is returned.

| Operation | Purpose / when to use | Required reference | Routing reminder |
|------|------------------|----------------|----------|
| `lark_api({tool:'base', op:'advperm-enable'})` / `lark_api({tool:'base', op:'advperm-disable'})` | Enable or disable advanced permissions | [`lark-base-advperm-enable.md`](references/lark-base-advperm-enable.md), [`lark-base-advperm-disable.md`](references/lark-base-advperm-disable.md) | Must be enabled before role management; disabling is high risk and invalidates existing custom roles |
| `lark_api({tool:'base', op:'role-list'})` / `lark_api({tool:'base', op:'role-get'})` | List roles, or get role details | [`lark-base-role-list.md`](references/lark-base-role-list.md), [`lark-base-role-get.md`](references/lark-base-role-get.md), [`role-config.md`](references/role-config.md) | `role-list` must run serial; `role-get` is for inspecting full permission config |
| `lark_api({tool:'base', op:'role-create'})` / `lark_api({tool:'base', op:'role-update'})` / `lark_api({tool:'base', op:'role-delete'})` | Create, update, or delete a role | [`lark-base-role-create.md`](references/lark-base-role-create.md), [`lark-base-role-update.md`](references/lark-base-role-update.md), [`lark-base-role-delete.md`](references/lark-base-role-delete.md), [`role-config.md`](references/role-config.md) | `role-create` only supports `custom_role`; `role-update` uses Delta Merge — `role_name` and `role_type` must always be supplied even if unchanged; `role-delete` is irreversible |

## 3. Lark Base common knowledge

Lark Base's English name is `Base`; its legacy name is `Bitable`. Therefore `bitable` appearing in old docs, return fields, params, or error messages is mostly historical compatibility — it does NOT mean another command set should be used.

### 3.1 Field categories and writability

| Field type | Meaning | Can be a direct write target for `record-upsert / record-batch-create / record-batch-update`? | Notes |
|----------|------|-----------------------------------------------------------|------|
| Storage field | Holds real user input | Yes | Common: text, number, date, single select, multi select, user, link |
| Attachment field | Holds file attachments | Should not be written like a normal field | Upload via `lark_api({tool:'base', op:'record-upload-attachment'})`; download via `lark_api({tool:'base', op:'record-download-attachment'})`; remove via `lark_api({tool:'base', op:'record-remove-attachment'})` |
| Location field | Stores coordinates and the platform resolves the address | Yes | Write must use `{lng,lat}`; for reading, filtering, and text conversion use the `full_address` string; only formulas can access the coordinates |
| System field | Maintained by the platform | No | Common: created time, updated time, created by, modified by, auto number |
| `formula` field | Computed from an expression | No | Read-only |
| `lookup` field | Cross-table lookup reference | No | Read-only |

### 3.2 Task-routing mental model

| User intent | Preferred path | Do not mistake for |
|---------|----------|----------|
| One-off analysis / ad-hoc statistics | `lark_api({tool:'base', op:'data-query'})` | Do not pull everything via `record-list` / `record-search` then compute manually |
| Result must persist in the table long term | formula field | Do not return only a one-shot manual analysis |
| User explicitly requests lookup, or it's naturally a fixed lookup configuration | lookup field | Do not default to lookup; first decide whether formula is more suitable |
| Read raw record details / keyword search / export | `lark_api({tool:'base', op:'record-search'})` / `record-list` / `record-get` | Do not use `data-query` as a record-fetching command |
| Upload an attachment to a record | `lark_api({tool:'base', op:'record-upload-attachment'})` | Do not fake attachment values via `record-upsert` / `record-batch-*` |
| Download an attachment file from a record | `lark_api({tool:'base', op:'record-download-attachment', args:{ record_id: '...', output: '...' }})` — add the `file_token` arg to download a specific attachment | Base attachments MUST be downloaded via this operation; other download paths may fail |
| Write a location | `lark_api({tool:'base', op:'record-upsert'})` / `record-batch-*` passing `{lng,lat}` | Do not treat plain address text as a CellValue |
| Read records via a view filter | `view-set-filter` + `record-list` | Do not skip the view filter and guess conditions |
| Import a local Excel / CSV / `.base` as Base | `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })` | Do not mistakenly call `base-create`, `table-create`, or `record-upsert` |

### 3.3 Query execution contract

When a task involves querying, statistics, or drawing a conclusion, first read [`references/lark-base-data-analysis-sop.md`](references/lark-base-data-analysis-sop.md) and comply with the following high-priority rules:

1. A `record-list` default page, a fixed `limit`, and local post-processing can only prove facts within the range already fetched — they cannot directly support global extreme values, total counts, Top/Bottom N, anomaly identification, or grouped conclusions.
2. Filtering, sorting, projection, aggregation, grouping, and limiting that Base can express should be executed in the Base cloud query service — do not pull details into local context and filter/sort manually.
3. `has_more=true` or an equivalent pagination signal means the current result is not complete. Unless the user only wants a sample / first N rows, do not answer global questions based on that page.
4. Multi-table queries must first confirm the relationship fields and join keys; the `record_id` inside a link cell is a join key, not a human-readable answer.
5. The final answer must be traceable to real tables, real fields, query scope, filter/sort/aggregation conditions, and any required join keys.

### 3.4 Table names, field names, and expression references

1. Table and field names must exactly match the real return; the source must be `table-list / table-get / field-list`.
2. Do not guess names from natural language; do not silently rewrite table/field names from the user's verbal description.
3. Names appearing in `formula / lookup / data-query / workflow` must also match exactly; expression references, where conditions, DSL field names, and workflow configs all obey the same rule.
4. Cross-table scenarios additionally require reading the target table schema — current-table-only is not enough.

### 3.5 Token and link

This is a high-priority section. Whenever input contains a link or token, or an error mentions `baseToken` / `wiki_token` / `obj_token`, return here first to check.

| Input type | Correct handling | Notes |
|---------|--------------|------|
| Direct Base link `/base/{token}` | Extract the token directly as the `base_token` arg | Do not pass the full URL as `base_token` |
| Wiki link `/wiki/{token}` | First resolve `node.obj_token` via the fast path below | Do not pass `wiki_token` directly as `base_token`; if this step fails, see [`lark-wiki-node-get.md`](../lark-wiki/references/lark-wiki-node-get.md) |
| `?table={id}` in URL | Decide object type by prefix first | `tbl` prefix = data table `table_id` arg; `blk` prefix = dashboard `dashboard_id`; `wkf` prefix = `workflow_id`; `ldx` prefix = embedded doc — do NOT treat all of these as `table_id` |
| `?view={id}` in URL | Extract as the `view_id` arg | Suitable for direct view targeting |

Wiki Base fast path — call `lark_api` with the wiki `get_node` HTTP form, then take `obj_token` when `obj_type` is `bitable`:

```
lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_url_or_token>' } })
```

| `obj_type` returned by the wiki `get_node` call above | Follow-up route | Notes |
|-----------------------------------------------|----------|------|
| `bitable` | Prefer `lark_api({tool:'base', op:'...'})` | If a typed op is missing, do NOT fall back to raw `/open-apis/bitable/v1/...`; check the catalog first |
| `docx` | Switch to docs / Drive related skill | Do not continue with this skill's Base ops |
| `sheet` | Switch to Sheets-related skill | Do not continue with this skill's Base ops |
| `slides` | Switch to Drive-related skill | Do not continue with this skill's Base ops |
| `mindnote` | Switch to Drive-related skill | Do not continue with this skill's Base ops |

### 3.6 Identity selection and permission-fallback strategy

Lark Base usually belongs to a user's personal or team resources. **Default to user identity for all Base operations**, and always specify the identity explicitly via the active profile.

- **User identity (recommended)**: operate as the logged-in user against Bases they have access to. Complete user authorization first via the LarkSkill MCP auth flow:

```
lark_auth_login({ domain: 'base' })
```

Then `lark_auth_poll` to wait for authorization, and confirm via `lark_whoami` / `lark_auth_status`.

- **Bot identity (fallback)**: only when user-identity permission is insufficient AND bot identity actually has access to the target Base. Bots cannot see user-private resources; behavior runs under the app identity. Switch via `lark_profile_switch`.

**Execution rules**:

1. All operations default to user identity.
2. If user identity returns a permission error, first check whether it is a **non-retryable error code** (e.g. `91403`). If so, **stop immediately** — do not retry or fall back. Follow the `lark-shared` insufficient-permission flow to guide the user.
3. For retryable codes, check the error response for hints like `permission_violations` / `hint` indicating scope-elevation:
   - **Has elevation hint**: follow the `lark-shared` flow to guide the user through user-identity scope elevation (re-run `lark_auth_login` with the requested scope, or `lark_enable_domain`); after confirmation, retry as user.
   - **No elevation hint** (e.g. resource-level access denied, not a scope issue): switch to bot identity via `lark_profile_switch` and retry **once**.
4. If bot identity also returns a permission error, **stop retrying immediately**, and per the error response follow the `lark-shared` flow to guide the user (developer-console scope or resource-access confirmation).
5. Only when the user explicitly says "use app identity / bot identity", skip user and go straight to bot via `lark_profile_switch`.

## 4. Execution rules

### 4.1 Standard execution order

1. Decide which module the task belongs to and pick the right operation family.
2. If the user gave a link, parse the token first — do not mistake a wiki token, full URL, or other object ID for `base_token`.
3. For query tasks, first assess the question scope, read the data analysis SOP, then decide between `record / view / data-query`.
4. Get schema before writing ops; avoid guessing table names, field names, expression references.
5. After locating the operation, read the corresponding reference, then execute.
6. Execute and decide the next step from the return value.
7. Reply with the key result and follow-up actions, so the agent can continue chaining the next step.

### 4.2 Inviolable rules

1. Get schema before writing ops; at minimum get current table schema, and target table for cross-table.
2. Do not guess table names, field names, or expression references — always honor the real return.
3. Use only atomic ops; do not regress to legacy aggregated forms `+table / +field / +record / +view / +history / +workspace`.
4. Read field schema before writing records; call `field-list` first, then build CellValues per [`lark-base-cell-value.md`](references/lark-base-cell-value.md).
5. Read the field-property spec before writing fields; read `lark-base-shortcut-field-properties.md` first, then build the JSON for `field-create / field-update`.
6. Only write writable fields; system fields, attachment fields, `formula`, `lookup` are NOT default write targets in record ops.
7. Aggregation analysis vs. retrieval are split: stats go to `data-query`, keyword search goes to `record-search`, details go to `record-list / record-get`.
8. Filtered queries go through view capability: configure with `view-set-filter` first, then read with `record-list`.
9. Global queries MUST NOT draw conclusions from a default page, small `limit`, or local results not proven to be complete.
10. In Base scenarios, do not bypass the catalog and call raw `/open-apis/bitable/v1/...` paths.
11. Use `base_token` uniformly in args; do not use the legacy `app_token` style.
12. In workflow scenarios, read schema first; do not guess `type` from natural language.
13. In dashboard scenarios, read the guide first; once chart / board / block is mentioned, enter the dashboard module.
14. In formula / lookup scenarios, read the guide first; do not create or update before reading the guide.

### 4.3 Concurrency, pagination, and batching limits

- `table-list / field-list / record-list / view-list / record-history-list / role-list / dashboard-list / dashboard-block-list / workflow-list` MUST NOT be called concurrently — serial only.
- For `record-list` pagination, `limit` max is `200`; first fetch the initial batch and inspect `has_more`, only continue paging when the user explicitly requires more data.
- Batch writes are capped at `200` records per call.
- Continuous writes against the same table MUST be serial, with `0.5–1` second delay between batches.

### 4.4 Confirmation and reply rules

- For view rename, when the user has clearly stated "which view, what new name", call `view-rename` directly.
- For updating fields or deleting records / fields / tables, when the user has clearly stated the target, `field-update / record-delete / field-delete / table-delete` may run directly with `yes: true`.
- When the delete target is still ambiguous, call `record-get / field-get / table-get` or the corresponding list to confirm first.
- After `base-create / base-copy` succeeds, the reply MUST proactively return identifiers for the new Base; if the result includes an accessible link, return it as well.
- If a Base was created or copied under bot identity, the op auto-attempts to grant the current user `full_access`, returning `permission_grant` in the output; the agent does NOT need to orchestrate a separate grant. Owner transfer must be confirmed separately and never executed implicitly.

## 5. Common errors and recovery

| Error / symptom | Meaning | Recovery |
|-------------|------|----------|
| `1254064` | Date format error | Pass a `YYYY-MM-DD HH:mm:ss` string, not a relative time |
| `1254068` | Hyperlink format error | `"https://example.com"` or `"[text](https://example.com)"` |
| `1254066` | User-field error | `[{ "id": "ou_xxx" }]` |
| `1254045` | Field name not found | Check the field name (spaces, case included) |
| `1254015` | Field value type mismatch | Call `field-list` first, then build by type |
| `param baseToken is invalid` / `base_token invalid` | A wiki token, workspace token, or other token was used as `base_token` | If input came from `/wiki/...`, first call `lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_url_or_token>' } })` to get the real `obj_token`; when `obj_type=bitable`, retry with `obj_token` as `base_token`; do not switch to raw `bitable/v1` |
| `not found` when user gave a wiki link | Common when a wiki token is mistaken for a base token | Roll back and re-check wiki resolution rather than switching to raw `bitable/v1` |
| formula / lookup creation fails | Guide not read or invalid structure | Read `formula-field-guide.md` / `lookup-field-guide.md` first, then rebuild the request per guide |
| `ignored_fields` / `READONLY` | A read-only field treated as writable (common: system field, formula, lookup) | Remove read-only fields, write only storage fields; let formula / lookup / system fields produce computed outputs automatically |
| `1254104` | Batch over 200 records | Split into batches |
| `1254291` | Concurrent write conflict | Serial writes + delay between batches |
| `91403` | No permission to access the Base | **Do NOT retry**. Follow the `lark-shared` insufficient-permission flow to guide the user |
