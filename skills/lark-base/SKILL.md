---
name: lark-base
version: 2.0.0
description: "Use this skill when operating Lark Base via LarkSkill MCP: table creation, field management, record read/write, view configuration, history queries, and role/form/dashboard management. Also use it when designing formula fields, lookup references, cross-table computation, row-level derived metrics, and data analysis requests."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# base

## Prerequisites

- LarkSkill MCP server connected (install via `/plugin marketplace add kescyz/larkskill` → `/plugin install larkskill`, or see https://portal.larkskill.app/setup)
- MCP tools available: `lark_api`, `lark_api_search`
- Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first for auth, global flags, and safety rules

> **Mandatory before execution:** Before calling any `base` operation, read the corresponding reference doc first.

## Agent quick execution order

1. **Identify task type first**
   - Temporary statistics / aggregation analysis -> `data-query`
   - Result must be persisted and shown in-table long term -> formula field
   - User explicitly requests lookup, or the case clearly fits `from/select/where/aggregate` -> lookup field
   - Detail retrieval / export -> `record-list / record-get`
2. **Inspect schema before writing**
   - At minimum, get the current table schema first: `field-list` or `table-get`
   - For cross-table scenarios, also inspect the **target table** schema
3. **Formula / lookup has hard gating rules**
   - Read the corresponding guide first
   - Create/update the field only after reading the guide
4. **Check field writability before writing records**
   - Write only storage fields
   - System fields / formula / lookup are read-only by default

## Agent forbidden behavior

- Do not use `record-list` as an aggregation engine
- Do not create formula / lookup fields before reading the guide
- Do not guess table names, field names, or formula field references from natural language
- Do not use system fields, formula fields, or lookup fields as `record-upsert` write targets
- Do not switch to raw `lark_api GET /open-apis/bitable/v1/...` calls ad hoc in Base scenarios without reading the reference doc first

## Base mental model

1. **Base fields fall into three categories**
   - **Storage fields**: persist user-entered values and are typically writable via `record-upsert`, such as text, number, date, single select, multi select, user, and link fields. **Attachment field exception**: file upload must use the `record-upload-attachment` flow.
   - **System fields**: platform-maintained and read-only, including created time, updated time, created by, modified by, and auto number.
   - **Computed fields**: derived by expressions or cross-table rules and are read-only — mainly **formula** and **lookup** fields.
2. **Decide field category before writing records** — only storage fields are directly writable; formula / lookup / system fields must be treated as read-only output fields and cannot be write targets.
3. **Base supports built-in computation** — for user intents like statistics, comparison, ranking, text composition, date difference, cross-table aggregation, or state judgment, first decide whether to solve with `data-query` or formula fields inside Base.

## Analysis path decisions

1. **One-off analysis / temporary query** -> prefer `data-query`
   - Suitable for grouped stats, SUM / AVG / COUNT / MAX / MIN, and filtered aggregation.
   - Characteristic: user needs the result now, not as a persisted field.
2. **Reusable long-term derived metrics / row-level computed outputs** -> prefer formula field
   - Suitable for profit margin, overdue flag, remaining days, bucket tags, and derived cross-table results.
   - Characteristic: result should persist in Base and auto-update with records.
3. **Explicit lookup request, or strict `from/select/where/aggregate` modeling need** -> use lookup field
   - Formula is still the default preference. Use lookup only when explicitly requested or when fixed lookup config fits better.
4. **Raw record retrieval / detail export** -> `record-list / record-get`
   - Do not treat `record-list` as an analysis engine; it retrieves details, not aggregation.

## Formula / Lookup rules

1. **If formula / lookup is involved, read guide first, then call `lark_api`**
   - formula: [`formula-field-guide.md`](references/formula-field-guide.md)
   - lookup: [`lookup-field-guide.md`](references/lookup-field-guide.md)
2. **Guide before create/update**
   - Do not directly create formula / lookup fields before reading the corresponding guide
   - After reading the guide, complete JSON body, then call `lark_api`
   - `type=formula` must provide `expression`
   - `type=lookup` must provide `from / select / where`, and `aggregate` when needed
3. **Formula field takes precedence over lookup field**
   - If user intent is computation / conditional logic / text processing / date difference / cross-table aggregation / filtered cross-table value retrieval, try formula first by default.
   - Use lookup only when user explicitly asks for lookup, or when the configuration naturally fits the lookup four-tuple.
4. **Table names / field names must match exactly**
   - Any table/field names used in formula, lookup, or data-query must come from actual outputs of `table-list` / `table-get` / `field-list`; semantic guessing is prohibited.
5. **Inspect schema before writing expressions**
   - Always retrieve related table schemas before producing formula expressions or lookup configs.

## Workflow rules

1. **Before any workflow operation, read two docs: the command doc + [lark-base-workflow-schema.md](references/lark-base-workflow-schema.md)**
   - `workflow-create` -> read [lark-base-workflow-create.md](references/lark-base-workflow-create.md) + schema
   - `workflow-update` -> read [lark-base-workflow-update.md](references/lark-base-workflow-update.md) + schema
   - `workflow-list` -> read [lark-base-workflow-list.md](references/lark-base-workflow-list.md) + schema
   - `workflow-get` -> read [lark-base-workflow-get.md](references/lark-base-workflow-get.md) + schema
   - `workflow-enable` -> read [lark-base-workflow-enable.md](references/lark-base-workflow-enable.md) + schema
   - `workflow-disable` -> read [lark-base-workflow-disable.md](references/lark-base-workflow-disable.md) + schema
   - Schema defines StepType enums, step structure, Trigger/Action/Branch/Loop data formats, and value reference syntax
   - Do not guess `type` from natural language (for example mapping "add record" to `CreateTrigger`). Always copy exact type names from StepType enums in schema.

2. **Confirm dependency info before creation**
   - Get real table names and field names via `table-list` / `field-list` (`lark_api` GET calls)
   - Do not guess table/field names in workflow config

## Dashboard module

**When the user mentions keywords related to dashboards such as "dashboard, data board, chart, visualization, block, component, add component, create chart", you must read** [lark-base-dashboard.md](references/lark-base-dashboard.md) **to understand the dashboard module operations and capabilities before proceeding.**

## Core rules

1. **Use only atomic operations** — use single-action MCP calls such as `table-list / table-get / field-create / record-upsert / view-set-filter / record-history-list / base-get`; do not attempt to chain or aggregate multiple API calls into one
2. **Read field schema before writing records** — call `field-list` first, then read [lark-base-shortcut-record-value.md](references/lark-base-shortcut-record-value.md) to confirm value format by field type
3. **Read field property spec before writing fields** — read [lark-base-shortcut-field-properties.md](references/lark-base-shortcut-field-properties.md) for `field-create`/`field-update` JSON body structure
4. **Execute filtered queries through view capability** — read [lark-base-view-set-filter.md](references/lark-base-view-set-filter.md) and [lark-base-record-list.md](references/lark-base-record-list.md), and use `view-set-filter` + `record-list`
5. **For analytical intent on records (highest/lowest/total/average/rank/compare/count)** — read [lark-base-data-query.md](references/lark-base-data-query.md) first, then call `data-query` API for server-side filter + aggregation
6. **Aggregation analysis and detail retrieval are mutually exclusive** — for grouped stats / SUM / MAX / AVG / COUNT use the `data-query` endpoint (server-side computation); do not fetch full records via `record-list` then compute manually. Conversely, `data-query` does not return raw records, so retrieval use-cases still require `record-list / record-get`.
7. **All list operations must be serial** — `table-list / field-list / record-list / view-list / record-history-list / role-list` cannot be called concurrently
8. **Batch write limit is 500 per call** — recommend serial writes per table with 0.5-1 second delay between batches
9. **Unified parameter name** — always use `base_token` (snake_case in JSON body / query params), not `app_token`
10. **For intents involving formula / lookup / derived metric / cross-table computation, prioritize field-solution decision** — decide whether to build formula/lookup field or run one-off `data-query`
11. **Formula, lookup, and system fields are read-only by default** — except for maintaining definitions via `field-create / field-update`, do not write these fields in record operations
12. **Rename/delete by explicit intent** — if target view and new name are explicit, call `view-rename` directly. If user clearly requests delete and target is clear, call `record-delete / field-delete / table-delete` directly without extra confirmation. Ask follow-up only when target is ambiguous.

## Questionnaire / Form hints

- **Get questionnaire list**: `form-list` (obtain `form-id` first)
- **Get single questionnaire**: `form-get`
- **Get form/questionnaire questions**: `form-questions-list`
- **Delete questionnaire/form questions**: `form-questions-delete`
- **Create/update questions**: `form-questions-create / form-questions-update`

## Intent -> MCP call index

| Intent | V2 MCP call | Note |
|--------|-------------|------|
| List / get tables | `lark_api GET /open-apis/bitable/v1/apps/{app_token}/tables` | Atomic |
| Create table | `lark_api POST /open-apis/bitable/v1/apps/{app_token}/tables` | body: `{name, ...}` |
| Update / delete table | `lark_api PUT/DELETE /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}` | One call per action |
| List / get fields | `lark_api GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields` | Atomic |
| Create / update field | `lark_api POST/PUT /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields[/{field_id}]` | body: field JSON |
| Create / update formula field | same field endpoint | `type=formula`; read formula guide first |
| Create / update lookup field | same field endpoint | `type=lookup`; read lookup guide first; formula is default preference |
| List / get records | `lark_api GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records` | For aggregation use data-query |
| Create / update record | `lark_api POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create` or upsert endpoint | Read reference doc |
| Aggregation / comparison / ranking | `lark_api POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/data_query` | Do not manually compute from full record-list |
| Configure / query views | view endpoints — see [lark-base-view.md](references/lark-base-view.md) | list/get/create/delete/rename/set-filter |
| Query record history | `lark_api GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}/history` | Requires table + record ID |
| Create / get / copy Base | `lark_api POST/GET /open-apis/base/v3/bases[/{app_token}]` | Read workspace reference doc |
| List / get workflow | `lark_api GET /open-apis/base/v1/apps/{app_token}/workflows` | Atomic |
| Create / update workflow | `lark_api POST/PUT /open-apis/base/v1/apps/{app_token}/workflows[/{workflow_id}]` | body: full step JSON; schema required |
| Enable / disable workflow | `lark_api POST /open-apis/base/v1/apps/{app_token}/workflows/{workflow_id}/enable` or `/disable` | One call per action |
| Enable / disable advanced permissions | see [lark-base-advperm-enable.md](references/lark-base-advperm-enable.md) | Custom roles require advperm enabled |
| List / get roles | role endpoints — see [lark-base-role-list.md](references/lark-base-role-list.md) | Role summary/detail |
| Create / update / delete roles | role endpoints — see reference docs | Manage custom-role permissions |
| List / get forms | form endpoints — see [lark-base-form-create.md](references/lark-base-form-create.md) | Atomic |
| Create / update / delete forms | form endpoints | One call per action |
| List / create / update / delete form questions | form-questions endpoints | One call per action |
| Create/manage dashboards and charts | dashboard endpoints — **must read** [lark-base-dashboard.md](references/lark-base-dashboard.md) **first** | See reference |

## Operational notes

- **Base token**: always use `app_token` in API paths (the base identifier); in body/params use `base_token` or `app_token` as documented per endpoint
- **Serial list discipline**: `table-list / field-list / record-list / view-list / record-history-list / role-list / dashboard-list / dashboard-block-list / workflow-list` must be serial, never parallel
- **`record-list` limit**: max `page_size` is `200`. For more data, paginate with `page_token`; never request >200 in a single call
- **Check field writability first**: only storage fields are writable; formula / lookup / system fields are read-only
- **Actively consider formula capability**: for intents like "calculate", "generate labels", "detect anomalies", "cross-table aggregate", or "date-diff alert", first evaluate whether a formula field should be built instead of returning manual analysis
- **Lookup is not default**: use lookup only when explicitly requested or strictly better for fixed lookup patterns; prioritize formula for general computation, cross-table aggregation, and conditional logic
- **Attachment fields**: for "upload attachment / add file to record", only use `record-upload-attachment` flow (read field -> read record -> upload asset -> write back record) — see [lark-base-record-upload-attachment.md](references/lark-base-record-upload-attachment.md)
- **User/person fields**: pay attention to `user_id_type` and execution identity (user / bot)
- **History usage**: record-history endpoint supports `table_id + record_id`; no full-table history scan
- **Workspace status**: integrated with `base-create / base-get / base-copy`
- **`base-create / base-copy` return rule**: after success, always return identifier information of the new Base. If result includes accessible link (e.g. `base.url`), return it as well
- **`base-create / base-copy` optional params**: `folder_token`, `time_zone`, and copy `name` are optional. Do not interrupt for these unless user explicitly requests them
- **`base-create / base-copy` permission handling (bot-created base)**: if created by app identity (bot), after create/copy success, by default continue using bot identity to grant current available user `full_access` admin permission. In reply, explicitly report grant outcome (success / no available user / failed + reason). If grant not completed, provide next-step guidance. Owner transfer must be separately confirmed and must not be executed implicitly.
- **Dashboard usage**: `dashboard-create` returns `dashboard_id`; Block `data_config` is passed as JSON and supports file reference via the MCP client
- **Advperm usage**: custom role management (`role-*`) requires advperm enabled; advperm-disable is high-risk and invalidates existing custom roles. Operator must be Base admin. Read [lark-base-advperm-enable.md](references/lark-base-advperm-enable.md) / [lark-base-advperm-disable.md](references/lark-base-advperm-disable.md) first.
- **Role usage**: role-create only supports `custom_role`; role-update uses Delta Merge (`role_name` and `role_type` must always be provided); role-delete is irreversible and only supports custom roles. Role config supports `base_rule_map`, `table_rule_map`, `dashboard_rule_map`, and `docx_rule_map`. Read [role-config.md](references/role-config.md) before role writes.
- **Form form-id**: get via form-list; `id` returned by form-create is the `form-id` for form-questions-* operations
- **Workflow usage**: before creating/updating workflow, read [lark-base-workflow-schema.md](references/lark-base-workflow-schema.md) carefully for trigger/node structures. workflow-list does not return full tree structure; use workflow-get for full structure.
- **Data-query usage**: before calling the data-query endpoint, read [lark-base-data-query.md](references/lark-base-data-query.md) for DSL, supported field types, aggregation functions, and constraints. `field_name` in DSL must exactly match real table field names from field-list.
- **Formula / lookup usage**: before building expressions or where conditions, get current table schema first; for cross-table, inspect target table schema. Never guess field names from natural language.
- **View rename confirmation rule**: if user already clearly specified which view to rename and the new name, call the view-rename endpoint directly without extra confirmation.
- **Delete confirmation rule (record / field / table)**: if user explicitly requests delete and target is clear, call `record-delete / field-delete / table-delete` directly without re-confirmation. Only resolve ambiguity when target is unclear.

## Wiki link special handling (critical)

Knowledge-base links (`/wiki/TOKEN`) may point to different object types such as docs, sheets, or Base. **Do not assume the URL token is a file token**. You must resolve real type and token first.

### Processing flow

1. **Call `lark_api` to query node info**

   ```
   Call MCP tool `lark_api`:
   - method: GET
   - path: /open-apis/wiki/v2/spaces/get_node
   - params: { "token": "<wiki_token>" }
   ```

2. **Extract key fields from response**
   - `node.obj_type`: document type (`docx/doc/sheet/bitable/slides/file/mindnote`)
   - `node.obj_token`: **real object token** for follow-up operations
   - `node.title`: document title

3. **Choose follow-up operation by `obj_type`**

   | obj_type | Meaning | Follow-up |
   |----------|---------|-----------|
   | `docx` | New cloud doc | `drive file.comments.*`, `docx.*` |
   | `doc` | Legacy cloud doc | `drive file.comments.*` |
   | `sheet` | Spreadsheet | `sheets.*` |
   | `bitable` | Base | use base endpoints (this skill); do **not** call raw bitable API ad hoc |
   | `slides` | Slides | `drive.*` |
   | `file` | File | `drive.*` |
   | `mindnote` | Mind map | `drive.*` |

4. **Use wiki-resolved `obj_token` as Base token**
   - When `obj_type=bitable`, `node.obj_token` is the correct token for base operations.
   - If original input is `/wiki/...`, do not pass `wiki_token` directly as `app_token`.

5. **If token error already occurred, fallback and re-check wiki resolution**
   - If API returns `param baseToken is invalid`, `base_token invalid`, or `not found`, and original input is `/wiki/...` link or `wiki_token`, first suspect wiki token being used as base token.
   - Re-call `wiki/v2/spaces/get_node`, confirm `obj_type=bitable`, then retry with `node.obj_token` as the base `app_token`.

### Query example

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/wiki/v2/spaces/get_node
- params: { "token": "Pgrr***************UnRb" }
```

Response example:
```json
{
  "node": {
    "obj_type": "docx",
    "obj_token": "UAJ***************E9nic",
    "title": "ai friendly test - 1 copy",
    "node_type": "origin",
    "space_id": "6946843325487906839"
  }
}
```

## Base link parsing rules

| Link type | Format | Handling |
|-----------|--------|----------|
| Direct Base link | `/base/{token}` | Extract directly as `app_token` in API path |
| Wiki link | `/wiki/{token}` | Call `wiki/v2/spaces/get_node` first, then use `node.obj_token` |

### URL parameter extraction

```
https://{domain}/base/{base-token}?table={table-id}&view={view-id}
```

- `/base/{token}` -> `app_token`
- `?table={id}` -> `table_id`
- `?view={id}` -> `view_id`

### Prohibited behavior

- **Do not** pass full URL as `app_token`
- **Do not** pass `wiki_token` directly as `app_token`

## Common error quick reference

| Error code | Meaning | Resolution |
|------------|---------|------------|
| 1254064 | Date format error | Use millisecond timestamp, not string / second-level timestamp |
| 1254068 | Hyperlink format error | Use `{text, link}` object |
| 1254066 | User field format error | Use `[{id:"ou_xxx"}]` and verify `user_id_type` |
| 1254045 | Field name not found | Check exact field name (spaces and case included) |
| 1254015 | Field value type mismatch | Call `field-list` first, then build by field type |
| `param baseToken is invalid` / `base_token invalid` | Using wiki token/workspace token/other token as `app_token` | If input comes from `/wiki/...`, get real `obj_token` via `wiki/v2/spaces/get_node`; when `obj_type=bitable`, retry with `node.obj_token`; do not switch to raw bitable/v1 |
| formula / lookup creation failure | Guide not read or invalid structure | Read `formula-field-guide.md` / `lookup-field-guide.md` first, then rebuild request per guide |
| system/formula field write failure | Read-only field treated as writable | Write storage fields; let formula/lookup/system fields produce computed outputs |
| 1254104 | Batch exceeds 500 | Split into batches |
| 1254291 | Concurrent write conflict | Use serial writes + delay between batches |

## Reference docs

- [lark-base-shortcut-field-properties.md](references/lark-base-shortcut-field-properties.md) - `field-create`/`field-update` JSON spec (recommended)
- [role-config.md](references/role-config.md) - role permission config details
- [lark-base-shortcut-record-value.md](references/lark-base-shortcut-record-value.md) - `record-upsert` value format spec (recommended)
- [formula-field-guide.md](references/formula-field-guide.md) - formula syntax, function constraints, CurrentValue rules, cross-table computation patterns (strongly recommended)
- [lookup-field-guide.md](references/lookup-field-guide.md) - lookup config rules, where/aggregate constraints, and formula-vs-lookup decisions
- [lark-base-view-set-filter.md](references/lark-base-view-set-filter.md) - view filter config
- [lark-base-record-list.md](references/lark-base-record-list.md) - record list retrieval and pagination
- [lark-base-advperm-enable.md](references/lark-base-advperm-enable.md) - advperm-enable
- [lark-base-advperm-disable.md](references/lark-base-advperm-disable.md) - advperm-disable
- [lark-base-role-list.md](references/lark-base-role-list.md) - role-list
- [lark-base-role-get.md](references/lark-base-role-get.md) - role-get
- [lark-base-role-create.md](references/lark-base-role-create.md) - role-create
- [lark-base-role-update.md](references/lark-base-role-update.md) - role-update
- [lark-base-role-delete.md](references/lark-base-role-delete.md) - role-delete
- [lark-base-dashboard.md](references/lark-base-dashboard.md) - dashboard module workflow guide
- [dashboard-block-data-config.md](references/dashboard-block-data-config.md) - Block data_config structure, chart types, filter rules
- [lark-base-workflow.md](references/lark-base-workflow.md) - workflow operation index
- [lark-base-workflow-schema.md](references/lark-base-workflow-schema.md) - `workflow-create`/`workflow-update` JSON body schema details for triggers and nodes (strongly recommended)
- [lark-base-data-query.md](references/lark-base-data-query.md) - `data-query` aggregation analysis (DSL, supported field types, aggregation functions)
- [examples.md](references/examples.md) - full operation examples (table creation, import, filter, update)

## Operation groups

> **Mandatory before execution:** After locating an operation in this table, always read the corresponding reference doc before calling `lark_api`.

| Operation group | Description |
|-----------------|-------------|
| [`table operations`](references/lark-base-table.md) | `table-list / table-get / table-create / table-update / table-delete` |
| [`field operations`](references/lark-base-field.md) | `field-list / field-get / field-create / field-update / field-delete / field-search-options` |
| [`record operations`](references/lark-base-record.md) | `record-list / record-get / record-upsert / record-upload-attachment / record-delete` |
| [`view operations`](references/lark-base-view.md) | `view-list / view-get / view-create / view-delete / view-get-* / view-set-* / view-rename` |
| [`data-query operations`](references/lark-base-data-query.md) | `data-query` |
| [`history operations`](references/lark-base-history.md) | `record-history-list` |
| [`base / workspace operations`](references/lark-base-workspace.md) | `base-create / base-get / base-copy` |
| [`advperm operations`](references/lark-base-advperm-enable.md) | `advperm-enable / advperm-disable` |
| [`role operations`](references/lark-base-role-list.md) | `role-list / role-get / role-create / role-update / role-delete` |
| [`form operations`](references/lark-base-form-create.md) | `form-list / form-get / form-create / form-update / form-delete` |
| [`form questions operations`](references/lark-base-form-questions-create.md) | `form-questions-list / form-questions-create / form-questions-update / form-questions-delete` |
| [`workflow operations`](references/lark-base-workflow.md) | `workflow-list / workflow-get / workflow-create / workflow-update / workflow-enable / workflow-disable` |
| [`dashboard / dashboard-block operations`](references/lark-base-dashboard.md) | `dashboard-list / dashboard-get / dashboard-create / dashboard-update / dashboard-delete / dashboard-block-list / dashboard-block-get / dashboard-block-create / dashboard-block-update / dashboard-block-delete` |
