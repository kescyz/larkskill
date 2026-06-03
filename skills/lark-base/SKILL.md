---
name: lark-base
version: 1.2.2
description: "Lark Base (Bitable) operations: create tables, fields, records, views, statistics, formula/lookup, forms, dashboards, workflows, role permissions; use when Base/Bitable or /base/ links are mentioned. File import → lark-drive; auth/authorization → lark-shared."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# base

## When to Use

Use this skill when:

- The user explicitly mentions Base / Bitable, or provides a `/base/` link.
- The user wants to create, modify, or manage tables, fields, write records, query records, or configure views inside Base.
- The user wants to work with formula fields, lookup fields, cross-table calculations, derived metrics, filter aggregations, TopN, or statistical analysis inside Base.
- The user wants to manage Base forms, dashboards, workflows, advanced permissions, or roles.
- The user wants to migrate old Base aggregate-style commands or old syntax to the current `lark_api({ tool: 'base', op: '...' })` form.

DO NOT use this skill when:

- The task is only about authentication, initial configuration, identity switching, scope handling, or permission authorization recovery — use `lark-shared` instead.
- Importing local Excel / CSV / `.base` files into Base — use `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })` instead.
- General data analysis, field design, or formula discussion without a Base/Bitable context.

## Usage Boundaries

- Base business operations MUST use the `lark_api({ tool: 'base', op: '...' })` form only; do NOT use the old aggregate-style `+table / +field / +record / +view / +history / +workspace`.
- Base does not depend on any schema CLI in this cycle. The SKILL retains only routing, risk, and complex JSON/DSL; simple commands are handled by their own parameters, tips, and error recovery.
- Upstream additionally exposes resource-directory shortcuts (`base-block-list` / `base-block-create` / `base-block-move` / `base-block-rename` / `base-block-delete`) that list and manage the `folder/table/docx/dashboard/workflow` directory a Base directly owns. These are NOT yet surfaced in the current MCP tool catalog, so they are unavailable here. Until they are: enumerate a Base's resources via `lark_api({ tool: 'base', op: 'table-list' })` / `dashboard-list` / `workflow-list` / `form-list` (or locate the Base via `lark_api({ tool: 'drive', op: 'search', args: { doc_types: 'bitable' } })`), and manage individual resources with their own table/dashboard/workflow commands.
- When the user wants to import Excel / CSV / `.base` into Base, first delegate to `lark_api({ tool: 'drive', op: 'import', args: { type: 'bitable', ... } })`, then return to Base commands after the import completes.
- When the user provides only a Base name or keyword, first use `lark_api({ tool: 'drive', op: 'search', args: { query: '<keyword>', doc_types: 'bitable' } })` to locate the resource.
- Base commands require a `base_token` or a resolvable Base URL. When no token is available: if the user wants to create a new one, use `lark_api({ tool: 'base', op: 'base-create' })`; if the user provides a title/keyword, search with `lark_api({ tool: 'drive', op: 'search', args: { query: '<base title>', doc_types: 'bitable', only_title: true, as: 'user' } })`; if the resource still cannot be located, ask the user which Base they mean.
- Authentication, initialization, scope, identity switching, and permission recovery belong to `lark-shared`; the Base document only retains permission rules that affect Base path selection.

## Quick Routing

| User Goal | Primary Command | When to Read Reference |
|---|---|---|
| Inspect Base itself | `lark_api({ tool: 'base', op: 'base-get' })` | Use the return to confirm Base name, owner, permissions, and a token for further operations |
| Create / copy Base | `lark_api({ tool: 'base', op: 'base-create' })` / `lark_api({ tool: 'base', op: 'base-copy' })` | Report the new Base identifier after write; note `permission_grant` in the return |
| Manage tables | `lark_api({ tool: 'base', op: 'table-list' })` / `lark_api({ tool: 'base', op: 'table-get' })` / `lark_api({ tool: 'base', op: 'table-create' })` / `lark_api({ tool: 'base', op: 'table-update' })` / `lark_api({ tool: 'base', op: 'table-delete' })` | Handle listing, details, creation, renaming, and deletion of tables |
| List / get / delete fields | `lark_api({ tool: 'base', op: 'field-list' })` / `lark_api({ tool: 'base', op: 'field-get' })` / `lark_api({ tool: 'base', op: 'field-delete' })` / `lark_api({ tool: 'base', op: 'field-search-options' })` | Use list/get to confirm field types, options, and IDs before writing; confirm the target field before deleting |
| Create / update fields | `lark_api({ tool: 'base', op: 'field-create' })` / `lark_api({ tool: 'base', op: 'field-update' })` | MUST read [lark-base-field-json.md](references/lark-base-field-json.md); for formula read [formula-field-guide.md](references/formula-field-guide.md); for lookup read [lookup-field-guide.md](references/lookup-field-guide.md); for command details read [lark-base-field-create.md](references/lark-base-field-create.md) / [lark-base-field-update.md](references/lark-base-field-update.md) |
| Read record details | `lark_api({ tool: 'base', op: 'record-get' })` / `lark_api({ tool: 'base', op: 'record-list' })` / `lark_api({ tool: 'base', op: 'record-search' })` | When filtering, sorting, Top/Bottom N, aggregation, multi-table joins, or global conclusions are involved, read [lark-base-data-analysis-sop.md](references/lark-base-data-analysis-sop.md) |
| Write records | `lark_api({ tool: 'base', op: 'record-upsert' })` / `lark_api({ tool: 'base', op: 'record-batch-create' })` / `lark_api({ tool: 'base', op: 'record-batch-update' })` | MUST read [lark-base-record-upsert.md](references/lark-base-record-upsert.md) / [lark-base-record-batch-create.md](references/lark-base-record-batch-create.md) / [lark-base-record-batch-update.md](references/lark-base-record-batch-update.md) and [lark-base-cell-value.md](references/lark-base-cell-value.md) |
| Attachment fields | `lark_api({ tool: 'base', op: 'record-upload-attachment' })` / `lark_api({ tool: 'base', op: 'record-download-attachment' })` / `lark_api({ tool: 'base', op: 'record-remove-attachment' })` | Do NOT fake attachments as ordinary CellValues; upload from local file; download/delete by file token or field |
| Delete records / share record links / history | `lark_api({ tool: 'base', op: 'record-delete' })` / `lark_api({ tool: 'base', op: 'record-share-link-create' })` / `lark_api({ tool: 'base', op: 'record-history-list' })` | Confirm the record before deleting; share links max 100; for history read [lark-base-record-history-list.md](references/lark-base-record-history-list.md) — query single records only, do not audit the entire table |
| Manage views | `lark_api({ tool: 'base', op: 'view-*' })` | For `view-set-filter` read [lark-base-view-set-filter.md](references/lark-base-view-set-filter.md); for other config, get current state first, then update following the returned structure |
| One-off aggregation statistics | `lark_api({ tool: 'base', op: 'data-query' })` | MUST read [lark-base-data-analysis-sop.md](references/lark-base-data-analysis-sop.md) and entry [lark-base-data-query-guide.md](references/lark-base-data-query-guide.md); for full DSL read [lark-base-data-query.md](references/lark-base-data-query.md) |
| Formula fields | `lark_api({ tool: 'base', op: 'field-create', args: { json: '{"type":"formula",...}' } })` / `lark_api({ tool: 'base', op: 'field-update', args: { json: '{"type":"formula",...}' } })` | MUST read [formula-field-guide.md](references/formula-field-guide.md), then add the hidden confirmation flag `i_have_read_guide: true` |
| Lookup fields | `lark_api({ tool: 'base', op: 'field-create', args: { json: '{"type":"lookup",...}' } })` / `lark_api({ tool: 'base', op: 'field-update', args: { json: '{"type":"lookup",...}' } })` | MUST read [lookup-field-guide.md](references/lookup-field-guide.md), then add the hidden confirmation flag `i_have_read_guide: true` |
| Form submission | `lark_api({ tool: 'base', op: 'form-submit' })` | First use `lark_api({ tool: 'base', op: 'form-detail' })` to read [lark-base-form-detail.md](references/lark-base-form-detail.md) to get `questions[].type`, `required`, `filter`, and `base_token` needed for attachments; for submission JSON read [lark-base-form-submit.md](references/lark-base-form-submit.md) |
| Create / update form questions | `lark_api({ tool: 'base', op: 'form-questions-create' })` / `lark_api({ tool: 'base', op: 'form-questions-update' })` | Read [lark-base-form-questions-create.md](references/lark-base-form-questions-create.md) / [lark-base-form-questions-update.md](references/lark-base-form-questions-update.md) |
| Other form management | `lark_api({ tool: 'base', op: 'form-list' })` / `lark_api({ tool: 'base', op: 'form-get' })` / `lark_api({ tool: 'base', op: 'form-detail' })` / `lark_api({ tool: 'base', op: 'form-create' })` / `lark_api({ tool: 'base', op: 'form-update' })` / `lark_api({ tool: 'base', op: 'form-delete' })` / `lark_api({ tool: 'base', op: 'form-questions-list' })` / `lark_api({ tool: 'base', op: 'form-questions-delete' })` | For `form-detail` read [lark-base-form-detail.md](references/lark-base-form-detail.md); confirm the target form before deleting |
| Dashboards and blocks | `lark_api({ tool: 'base', op: 'dashboard-*' })` / `lark_api({ tool: 'base', op: 'dashboard-block-*' })` | When charts/kanban/blocks are mentioned, first read [lark-base-dashboard.md](references/lark-base-dashboard.md); for block `data_config` read [dashboard-block-data-config.md](references/dashboard-block-data-config.md); use `lark_api({ tool: 'base', op: 'dashboard-block-get-data' })` to retrieve chart computed results |
| Workflow | `lark_api({ tool: 'base', op: 'workflow-*' })` | When creating/updating or interpreting steps, read entry [lark-base-workflow-guide.md](references/lark-base-workflow-guide.md) and steps JSON SSOT [lark-base-workflow-schema.md](references/lark-base-workflow-schema.md); list/get/enable/disable only need workflow ID and current enable/disable state |
| Advanced permissions and roles | `lark_api({ tool: 'base', op: 'advperm-*' })` / `lark_api({ tool: 'base', op: 'role-*' })` | First read entry [lark-base-role-guide.md](references/lark-base-role-guide.md) for role operations; for role create/update or interpreting full config, read the permission JSON SSOT [role-config.md](references/role-config.md); system roles cannot be deleted; disabling advanced permissions affects custom roles |

## Base Mental Model

- Base was formerly called Bitable; `bitable` appearing in returned fields, errors, or older docs is mostly for historical compatibility and does not indicate using the raw API or a different command set.
- To understand what is inside a Base before acting, enumerate its resources with `lark_api({ tool: 'base', op: 'table-list' })` / `dashboard-list` / `workflow-list` / `form-list`, or locate the Base itself via `lark_api({ tool: 'drive', op: 'search', args: { query: '<keyword>', doc_types: 'bitable' } })`; then decide whether to proceed with table, dashboard, workflow, or form commands.
- Table, field, view, workflow, and dashboard block names and IDs MUST come from real return values — do NOT guess from user descriptions.
- Storage fields are writable; system fields, `formula`, and `lookup` are read-only; attachment fields use the dedicated attachment commands.
- For one-off raw record queries, prefer `lark_api({ tool: 'base', op: 'record-list' })` / `lark_api({ tool: 'base', op: 'record-search' })` filter/sort; for aggregation analysis, prefer `lark_api({ tool: 'base', op: 'data-query' })`; only add `formula` / `lookup` fields when results need to persist long-term in the table.
- `formula` is suited for regular calculations, conditional logic, text/date processing, and long-term derived metrics; `lookup` is suited for explicit cross-table lookups, filtered value retrieval, or aggregate references.
- Before writing, analyzing, creating formula/lookup fields, workflows, or dashboards, first read the real structure: table, field, view, linked table, and dashboard block names must be taken from command returns.
- Cross-table scenarios MUST read the target table's structure; `record_id` inside a link cell is a relationship key, not a user-readable answer — always query back to display readable fields.

## Identity and Permission Downgrade

- Default: explicitly use `as: 'user'` for user resources; only use `as: 'bot'` directly when the user explicitly requests bot identity.
- If the user identity reports scope/authorization insufficient errors, or the error contains `permission_violations` / `hint`, first delegate to `lark-shared` for user authorization recovery — do NOT downgrade to bot directly.
- Only retry with `as: 'bot'` once when the user identity reports resource-level no-access with no authorization recovery hint; if bot also fails, stop retrying and handle as a permission error.
- Do NOT loop through identity switching for `91403` or clearly inaccessible errors.
- For `lark_api({ tool: 'base', op: 'base-create' })` / `lark_api({ tool: 'base', op: 'base-copy' })` executed with bot identity, check the `permission_grant` in the return and inform the user whether they can open the new Base.

## Query and Statistics Rules

When queries, statistics, or drawing conclusions are involved, first read [lark-base-data-analysis-sop.md](references/lark-base-data-analysis-sop.md) and comply with:

1. The default page of `lark_api({ tool: 'base', op: 'record-list' })`, a fixed `limit`, and local `jq` can only prove facts within the read range — they cannot directly support global max/min values, full counts, Top/Bottom N, anomaly identification, or grouping conclusions.
2. Filtering, sorting, projection, aggregation, grouping, and limiting that can be expressed in Base should be executed in Base cloud query capabilities; do NOT pull raw records to local context and then manually filter/sort.
3. `has_more=true` or equivalent pagination signals mean the current result is not the full dataset; unless the user only wants a sample/first N rows, do not answer global questions based on a single page.
4. Multi-table queries MUST first confirm relationship fields and join keys; `record_id` inside a link cell is a relationship key, not a user-readable answer.
5. Final answers MUST be traceable to the real table, real fields, query scope, filter/sort/aggregation conditions, and necessary join keys.
6. For one-off raw record queries, prefer `lark_api({ tool: 'base', op: 'record-list' })` / `lark_api({ tool: 'base', op: 'record-search' })` filter/sort; for aggregation analysis, prefer `lark_api({ tool: 'base', op: 'data-query' })`; only consider adding `formula` / `lookup` fields when results need to be displayed long-term in the table.
7. `lark_api({ tool: 'base', op: 'data-query' })` can return aggregated results or dimension field rows, but dimension rows are deduplicated by field combination and do not return `record_id`; when per-record detail, record location, or complete row-level fields are needed, fall back to `lark_api({ tool: 'base', op: 'record-list' })` / `lark_api({ tool: 'base', op: 'record-search' })` / `lark_api({ tool: 'base', op: 'record-get' })`.

## Pre-Write Rules

- Read field structure before writing records; only write to storage fields. System fields, attachment fields, `formula`, and `lookup` MUST NOT be used as ordinary record write targets.
- Attachment upload, download, and deletion use the dedicated `lark_api({ tool: 'base', op: 'record-upload-attachment' })` / `record-download-attachment` / `record-remove-attachment` commands.
- Read [lark-base-field-json.md](references/lark-base-field-json.md) before writing fields; when `formula` / `lookup` is involved, MUST read [formula-field-guide.md](references/formula-field-guide.md) / [lookup-field-guide.md](references/lookup-field-guide.md).
- Table names, field names, view names, and names in workflow configurations MUST come from real returns; cross-table scenarios also require reading the target table structure.
- High-risk operations such as deletion, role update, and field update follow the MCP confirmation gate; when the target is unclear, use get/list to disambiguate first.
- Batch writes: at most 200 records per batch; execute serially when writing to the same table consecutively; treat `1254291` as a brief-wait-then-retry scenario.
- `lark_api({ tool: 'base', op: 'record-batch-update' })` is a "same-value batch update": the same patch is applied to all `record_id_list` — do NOT use it for per-row different-value mapping.
- Writing unknown options to select/multiselect may trigger platform option creation; when not intending to add new options, first confirm available values with `lark_api({ tool: 'base', op: 'field-list' })` or `lark_api({ tool: 'base', op: 'field-search-options' })`.

## Form and View Details

- MUST run `lark_api({ tool: 'base', op: 'form-detail' })` before `lark_api({ tool: 'base', op: 'form-submit' })` to read `questions[].type`, `required`, `filter`, and `base_token` required for attachment scenarios; do NOT fill in questions hidden by a filter.
- Form attachments MUST NOT go into `fields`; place them in `attachments` arg; when submitting attachments, also pass the `base_token` of the Base the form belongs to.
- `lark_api({ tool: 'base', op: 'view-set-filter' })` is the only retained view reference; for sort/group/card/timebar/visible-fields configurations, first read the current state with the corresponding get command, preserve unmodified fields, and only replace the configuration the user wants changed.
- Views are suited for persistence, sharing, and UI reuse; one-off filter/sort can first be validated with `lark_api({ tool: 'base', op: 'record-list' })` / `lark_api({ tool: 'base', op: 'record-search' })` filter/sort, then persisted as a permanent view if needed.

## Token and Links

| Input Type | Meaning / Correct Handling |
|---|---|
| `/base/{token}` | Regular Base link; extract the token after `/base/` as `base_token` arg |
| `/wiki/{token}` | Wiki node link; first run `lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: '<wiki_token>' } })`; when `node.obj_type=bitable`, use `node.obj_token` as `base_token` |
| `/base/{token}?table={id}` | `table` parameter locates an object inside Base: prefix `tbl` → table `table_id` arg; prefix `blk` → dashboard ID; prefix `wkf` → workflow ID |
| `/base/{token}?view={id}` | `view` parameter locates a table view, extract as `view_id` arg; usually also need to confirm the `table` parameter or query the table structure first |
| `/share/base/form/{shareToken}` | Form share link; this is the form share token — use `lark_api({ tool: 'base', op: 'form-detail', args: { share_token: '<shareToken>' } })` / `lark_api({ tool: 'base', op: 'form-submit', args: { share_token: '<shareToken>' } })` |
| `/share/base/view/{shareToken}` | View share link; has share-permission semantics, not yet supported for direct MCP access — guide the user to open in browser or Lark client |
| `/share/base/dashboard/{shareToken}` | Dashboard share link; has share-permission semantics, not yet supported for direct MCP access — guide the user to open in browser or Lark client |
| `/record/{shareToken}` | Record share link; not yet supported for direct MCP access — guide the user to open in browser or Lark client. If the user wants to generate a share link for an existing record, use `lark_api({ tool: 'base', op: 'record-share-link-create', args: { base_token: '<base_token>', table_id: '<table_id>', record_ids: ['<record_id>'] } })` |
| `/base/workspace/{token}` | BaseApp / workspace link; not yet supported for direct MCP access |

When `lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node' })` returns a non-`bitable` type, do NOT continue using Base commands: `docx` → Docs skill, `sheet` → Sheets skill, other Drive objects → corresponding skill or drive.

## Dashboard / Workflow / Role

- The complexity of Dashboard lies in block `data_config`, not in the list/get/create/delete command parameters. Read [dashboard-block-data-config.md](references/dashboard-block-data-config.md) before creating or updating a block; blocks MUST be created serially. `lark_api({ tool: 'base', op: 'dashboard-arrange' })` is a server-side smart layout — only execute it when the user explicitly requests rearranging/beautifying. `lark_api({ tool: 'base', op: 'dashboard-block-get-data' })` reads the chart's final computed results; it does NOT return block name, type, layout, or `data_config` — use `lark_api({ tool: 'base', op: 'dashboard-block-get' })` first when metadata is needed.
- The complexity of Workflow lies in the `steps` structure. When creating, updating, or interpreting a complete workflow, read entry [lark-base-workflow-guide.md](references/lark-base-workflow-guide.md) and steps JSON SSOT [lark-base-workflow-schema.md](references/lark-base-workflow-schema.md); enable/disable/list only need the workflow ID, current enable/disable state, and user intent.
- The complexity of Role lies in the permission JSON. First read entry [lark-base-role-guide.md](references/lark-base-role-guide.md) for role operations; `lark_api({ tool: 'base', op: 'role-create' })` supports custom roles only; `lark_api({ tool: 'base', op: 'role-update' })` is a delta merge; read the permission JSON SSOT [role-config.md](references/role-config.md) when creating/updating a role or interpreting the full configuration. `lark_api({ tool: 'base', op: 'role-delete' })` applies to custom roles only — system roles cannot be deleted; MUST confirm the target and impact before deleting a role or disabling advanced permissions.

## Common Recovery

| Error / Symptom | Recovery Action |
|---|---|
| `param baseToken is invalid` / `base_token invalid` | Check whether a wiki token, workspace token, or full URL was mistakenly passed as `base_token`; re-locate the real Base token per the Token and Links section |
| `not found` and input came from a Wiki link | First check whether the wiki token was mistakenly used as base token — do NOT immediately switch to the raw API |
| `1254045` field name does not exist | Re-run `lark_api({ tool: 'base', op: 'field-list' })`; use the real field name or field ID; watch for spaces, case differences, and cross-table fields |
| `1254015` field value type mismatch | First run `lark_api({ tool: 'base', op: 'field-list' })`, then construct CellValue per [lark-base-cell-value.md](references/lark-base-cell-value.md) |
| Date / person / hyperlink field format error | Date: use `YYYY-MM-DD HH:mm:ss`; person: use `[{ "id": "ou_xxx" }]`; hyperlink: use a URL or markdown link string |
| formula / lookup creation failed | First read [formula-field-guide.md](references/formula-field-guide.md) / [lookup-field-guide.md](references/lookup-field-guide.md), then rebuild the request per the guide |
| `ignored_fields` / `READONLY` | Remove read-only fields; write to storage fields only |
| `1254104` | Batch exceeds 200; split into multiple calls |
| `1254291` | Concurrent write conflict; write serially with a brief wait between batches |
| `91403` | No permission to access this Base; follow the `lark-shared` permission flow — do NOT retry blindly |

## Retained References

- [lark-base-data-analysis-sop.md](references/lark-base-data-analysis-sop.md): Query/statistics/global conclusions routing SOP
- [lark-base-data-query-guide.md](references/lark-base-data-query-guide.md) / [lark-base-data-query.md](references/lark-base-data-query.md): Aggregation query entry fewshot and DSL SSOT
- [lark-base-cell-value.md](references/lark-base-cell-value.md): Record CellValue construction
- [lark-base-field-json.md](references/lark-base-field-json.md): Field JSON construction
- [formula-field-guide.md](references/formula-field-guide.md) / [lookup-field-guide.md](references/lookup-field-guide.md): Formula and lookup fields
- [lark-base-field-create.md](references/lark-base-field-create.md) / [lark-base-field-update.md](references/lark-base-field-update.md): Field create/update command-level supplements
- [lark-base-record-upsert.md](references/lark-base-record-upsert.md) / [lark-base-record-batch-create.md](references/lark-base-record-batch-create.md) / [lark-base-record-batch-update.md](references/lark-base-record-batch-update.md) / [lark-base-record-history-list.md](references/lark-base-record-history-list.md): Record write JSON and history return interpretation
- [lark-base-view-set-filter.md](references/lark-base-view-set-filter.md): View filter JSON
- [lark-base-form-detail.md](references/lark-base-form-detail.md) / [lark-base-form-submit.md](references/lark-base-form-submit.md) / [lark-base-form-questions-create.md](references/lark-base-form-questions-create.md) / [lark-base-form-questions-update.md](references/lark-base-form-questions-update.md): Form details, submission, and complex JSON
- [lark-base-dashboard.md](references/lark-base-dashboard.md) / [dashboard-block-data-config.md](references/dashboard-block-data-config.md) / [lark-base-dashboard-block-get-data.md](references/lark-base-dashboard-block-get-data.md): Dashboard, block configuration, and chart result protocol
- [lark-base-workflow-guide.md](references/lark-base-workflow-guide.md) / [lark-base-workflow-schema.md](references/lark-base-workflow-schema.md): Workflow entry and steps JSON SSOT
- [lark-base-role-guide.md](references/lark-base-role-guide.md) / [role-config.md](references/role-config.md): Role entry and permission JSON SSOT
