# Feishu Base Role Permission Configuration Guide

> **Back**: [SKILL.md](../SKILL.md) | **Related**: [role-create](lark-base-role-create.md) · [role-update](lark-base-role-update.md) · [role-get](lark-base-role-get.md)

This document explains the complete JSON structure of role permissions (`AdvPermBaseRoleConfig`) for building `--json` payloads used by `+role-create` and `+role-update`.

## Table of contents

- [Top-level structure (AdvPermBaseRoleConfig)](#top-level-structure-advpermbaseroleconfig)
- [Role type (RoleType)](#role-type-roletype)
- [Base-level permissions (BaseRuleMap)](#base-level-permissions-baserulemap)
- [Dashboard permissions (DashboardRule)](#dashboard-permissions-dashboardrule)
- [Document permissions (DocxRule)](#document-permissions-docxrule)
- [Table permissions (TableRule)](#table-permissions-tablerule)
    - [Table-level permission (TablePerm)](#table-level-permission-tableperm)
    - [View permissions (ViewRule)](#view-permissions-viewrule)
    - [Field permissions (FieldRule)](#field-permissions-fieldrule)
    - [Record permissions (RecordRule)](#record-permissions-recordrule)
    - [Filter conditions (FilterRuleGroup)](#filter-conditions-filterrulegroup)
- [Default permission strategy and risk-control rules](#default-permission-strategy-and-risk-control-rules)
    - [Default-off items](#default-off-items)
    - [Permission object selection](#permission-object-selection)
    - [Default strategy for record operations](#default-strategy-for-record-operations)
    - [field_perms construction SOP](#field_perms-construction-sop)
    - [Default strategy for view permissions](#default-strategy-for-view-permissions)

---

## Top-level structure (AdvPermBaseRoleConfig)

```json
{
  "role_name": "Financial Auditor",
  "role_type": "custom_role",
  "base_rule_map": { "copy": false, "download": false },
  "table_rule_map": { "Order table": { "perm": "edit", "...": "..." } },
  "dashboard_rule_map": { "Sales Board": { "perm": "read_only" } },
  "docx_rule_map": { "Document A": { "perm": "edit", "allow_download": true } }
}
```

| Field | Type | Required | Description |
|------|------|----|------|
| `role_name` | string | Yes  | Role name, cannot be empty |
| `role_type` | string | Yes  | Role type, see [RoleType](#role-type-roletype) |
| `base_rule_map` | map\<string, bool\> | Yes  | Base-level permissions, see [BaseRuleMap](#base-level-permissions-baserulemap) |
| `table_rule_map` | map\<string, TableRule\> | No  | Table permissions, key is table name |
| `dashboard_rule_map` | map\<string, DashboardRule\> | No  | Dashboard permissions, key is dashboard name |
| `docx_rule_map` | map\<string, DocxRule\> | No  | Document permissions (solo-base mode only), key is document name |

---

## Role type (RoleType)

| Value | Description |
|------|------|
| `editor` | System role: editor |
| `reader` | System role: reader |
| `custom_role` | Custom role |

**Notes**:
- Create API (`+role-create`) only supports `custom_role`
- Update API (`+role-update`) supports `editor` / `reader` / `custom_role`

---

## Base-level permissions (BaseRuleMap)

1. Default value is `false`; set to `true` only when explicitly needed.
2. This field must be included by default when creating or updating roles. **Never** set it to `true` unless the user explicitly asks.

```json
{
  "base_rule_map": {
    "copy": true,
    "download": false
  }
}
```

| Key | Description |
|-----|------|
| `copy` | Allow copying Base content |
| `download` | Allow creating copies, downloading, and printing Base content |

---

## Dashboard permissions (DashboardRule)

```json
{
  "dashboard_rule_map": {
    "Sales Board": { "perm": "read_only" },
    "internal data": { "perm": "no_perm" }
  }
}
```

| Field | Type | Description |
|------|------|------|
| `perm` | string | Dashboard permission |

**Allowed `perm` values**:

| Value | Description |
|----|------|
| `read_only` | Read-only |
| `no_perm` | No permission |

---

## Document permissions (DocxRule)

> ⚠️ Available only in solo-base mode (`is_base_solo = true`).

```json
{
  "docx_rule_map": {
    "Document A": { "perm": "edit", "allow_download": true },
    "Document B": { "perm": "read_only" }
  }
}
```

| Field | Type | Required | Description |
|------|------|------|------|
| `perm` | string | Yes | Document permission |
| `allow_download` | bool | No | Whether download/export is allowed |

**Allowed `perm` values**:

| Value | Description |
|----|------|
| `edit` | Editable |
| `read_only` | Read-only |
| `no_perm` | No permission |

---

## Table permissions (TableRule)

```json
{
  "table_rule_map": {
    "Order form": {
      "perm": "edit",
      "view_rule": { "..." : "..." },
      "record_rule": { "..." : "..." },
      "field_rule": { "..." : "..." }
    },
    "User table": {
      "perm": "read_only"
    }
  }
}
```

| Field | Type | Description |
|------|------|------|
| `perm` | string | Table-level permission, see [TablePerm](#table-level-permission-tableperm) |
| `view_rule` | ViewRule | View permission config |
| `record_rule` | RecordRule | Record permission config |
| `field_rule` | FieldRule | Field permission config |

**Note**: When `perm` is `no_perm`, `view_rule`, `record_rule`, and `field_rule` should not be set.

---

### Table-level permission (TablePerm)

| Value | Description |
|----|------|
| `manage` | Manage |
| `edit` | Edit |
| `read_only` | Read-only |
| `no_perm` | No permission (in this case, view/record/field permissions cannot be configured) |

---

### View permissions (ViewRule)

```json
{
  "view_rule": {
    "allow_edit": true,
    "visibility": {
      "all_visible": false,
      "visible_views": ["Table view", "Kanban board view"]
    }
  }
}
```

| Field | Type | Description |
|------|------|----------------------------|
| `allow_edit` | bool | Allow create/delete/update views. Defaults to `false` if not specified |
| `visibility` | object | View visibility config |
| `visibility.all_visible` | bool | Whether all views are visible |
| `visibility.visible_views` | []string | List of visible view names |

**⚠️ Core rule: `view_rule` must include both `allow_edit` and `visibility`. Neither can be omitted.**

When outputting `view_rule`, **always** use the full structure below, based on scenario:

```json
// Situation A: The user requires the ability to edit/add/delete views → set allow_edit to true
{
  "view_rule": {
    "allow_edit": true,
    "visibility": {
      "all_visible": true
    }
  }
}

// Situation B: The user did not mention the specific view and did not ask to edit the view → all visible, not editable
{
  "view_rule": {
    "allow_edit": false,
    "visibility": {
      "all_visible": true
    }
  }
}

// Case C: The user mentioned a specific view → only the specified view is visible
{
  "view_rule": {
    "allow_edit": false,
    "visibility": {
      "all_visible": false,
      "visible_views": ["Table view", "Kanban board view"]
    }
  }
}
```

**Notes**:
- When `all_visible` is `false`, `visible_views` cannot be empty
- Views with `biz_type = query_form_view` cannot appear in `visible_views`

---

### Field permissions (FieldRule)

```json
{
  "field_rule": {
    "field_perm_mode": "specify",
    "field_perms": {
      "Amount": "edit",
      "Remarks": "read",
      "password": "no_perm"
    },
    "allow_edit_and_modify_option_fields": [],
    "allow_edit_and_download_file_fields": []
  }
}
```

| Field | Type | Description |
|------|------|------|
| `field_perm_mode` | string | Field permission mode |
| `field_perms` | map\<string, string\> | Field name -> permission, valid only when `field_perm_mode` is `specify` |
| `allow_edit_and_modify_option_fields` | []string | Field names that can modify options |
| `allow_edit_and_download_file_fields` | []string | Field names that can download attachments |

**Allowed `field_perm_mode` values**:

| Value | Description |
|----|------|
| `all_edit` | All fields editable, but options cannot be modified |
| `all_read` | All fields readable |
| `specify` | Per-field permissions (`field_perms` + option edit permissions) |
| `no_perm` | No permission |

**Permission values for a single field in `field_perms`**:

| Value | Description |
|----|------|
| `edit` | Editable (includes create/read) |
| `create` | Creatable (includes read) |
| `read` | Readable |
| `no_perm` | No permission |

**⚠️ Important `field_perms` rules**:
1. Check field `type` before writing
2. Formula / Lookup / AutoNumber fields **must** be downgraded to `read` or `no_perm`; **never** set `edit`
3. Output all fields except the 4 system fields
4. `allow_edit_and_modify_option_fields`: configure only when user explicitly asks to modify options; otherwise it must be `[]`. Only SingleSelect/MultiSelect are supported. **Never include Stage fields**
5. `allow_edit_and_download_file_fields`: do not set unless user requests it, and only when `field_perm_mode = specify`

---

### Record permissions (RecordRule)

```json
{
  "record_rule": {
    "record_operations": ["add"],
    "edit_filter_rule_group": {
      "conjunction": "and",
      "filter_rules": [
        {
          "conjunction": "and",
          "filters": [
            {
              "field_name": "Department",
              "operator": "is",
              "filter_values": ["Finance Department"]
            }
          ]
        }
      ]
    },
    "other_record_all_read": true
  }
}
```

| Field | Type | Description |
|------|------|------|
| `record_operations` | []string | Record operation permissions; valid only when `TablePerm = edit` |
| `edit_filter_rule_group` | FilterRuleGroup | Filter condition for editable records. Leave empty when all records are editable |
| `other_record_all_read` | bool | Whether all records are readable. Use `true` for all-readable; otherwise `false` |
| `read_filter_rule_group` | FilterRuleGroup | Extra filter for readable records. Set only when readable scope differs from editable scope (depends on `other_record_all_read = false`) |

**Allowed `record_operations` values**:

| Value | Description |
|----|------|
| `add` | Can add records |
| `delete` | Can delete records |

---

### Filter conditions (FilterRuleGroup)

```json
{
  "conjunction": "and",
  "filter_rules": [
    {
      "conjunction": "and",
      "filters": [
        {
          "field_name": "Department",
          "operator": "is",
          "field_type": "SingleSelect",
          "filter_values": ["Finance Department"]
        }
      ]
    }
  ]
}
```

**FilterRuleGroup structure**:

| Field | Type | Description |
|------|------|------|
| `conjunction` | string | Logical connector: `and` / `or` |
| `filter_rules` | []FilterRule | Array of filter-rule groups |

**FilterRule structure**:

| Field | Type | Description |
|------|------|------|
| `conjunction` | string | Logical connector, default `and` |
| `filters` | []Filter | Array of filter conditions |

**Filter structure**:

| Field | Type | Required | Description |
|------|------|------|------|
| `field_name` | string | Yes | Field name. Only fields with `can_filter = true` are allowed. Must be empty when `field_type = CreatedUser` |
| `operator` | string | Yes | Operator, see table below |
| `field_type` | string | Yes | Field type. Supported: SingleSelect / MultiSelect / User / CreatedUser / Stage / Number-family fields (including progress/rating/currency), and some Formula/LookUp fields (`can_filter = true`) |
| `reference_type` | string | Conditional | Reference type. Must be set for formula/lookup field types; must not be set for other types |
| `filter_values` | []string | Conditional | Filter values. Omit for `isEmpty` / `isNotEmpty`, and also unnecessary for `User`; required in other cases. For options, use option `name` |
| `field_ui_type` | string | Conditional | Must be provided when present |
| `is_invalid` | bool | No | Indicates whether condition is invalid |

**Allowed `operator` values**:

| Value | Description |
|----|------|
| `is` | Equals |
| `isNot` | Not equals |
| `contains` | Contains |
| `doesNotContain` | Does not contain |
| `isEmpty` | Is empty |
| `isNotEmpty` | Is not empty |
| `isGreater` | Greater than |
| `isGreaterEqual` | Greater than or equal |
| `isLess` | Less than |
| `isLessEqual` | Less than or equal |

**Note**:
- In create/update role APIs, `field_type`, `field_ui_type`, and `reference_type` are usually auto-filled by server-side `filterFiller`; clients usually only need `field_name`, `operator`, and `filter_values`

---

## Default permission strategy and risk-control rules

When building role-config JSON, apply **default deny + least privilege**. Any permission not explicitly requested by the user must stay closed. Do not proactively expand scope based on “reasonable guess” or “common practice”.

### Default-off items

The following capabilities are **off by default** unless explicitly requested:

| Capability | Default | Enable when |
|------|--------|----------|
| Access to any unmentioned table | `no_perm` | User explicitly mentions that table |
| Dashboard access | Not configured | User explicitly mentions that dashboard |
| `base_rule_map.copy` | `false` | User explicitly asks to allow copy |
| `base_rule_map.download` | `false` | User explicitly asks to allow download/print/copy |
| `delete` in `record_operations` | Excluded | User explicitly says delete is allowed, or uses strong intent like full management |

---

### Permission ceiling rules for Editor / Reader
1. Editor and Reader permission configs can be updated, but ceiling constraints apply.
2. Reader cannot exceed read-only for any permission item.
3. Reader cannot have editable/create/delete permissions. Editor can be modified, but still capped by advanced-permission capability boundaries.

### Permission object selection

**Notes**:
- Generate config only for explicitly targeted objects (explicit table names/dashboard names, or uniquely resolvable references like “current table”)
- **Never** infer/expand permission objects using business assumptions, role semantics, name similarity, or historical role configs
- Any unmentioned object gets no generated config and is treated as `no_perm`

---

### Default strategy for record operations

**Notes**:
- If user does not specify, include `add` by default and exclude `delete` by default
- Read scope defaults to edit scope: if user only describes editable scope and does not describe readable scope, keep readable scope aligned and do not expand it
- If readable scope equals editable scope, **do not** generate `read_filter_rule_group`; set `other_record_all_read = false` and `read_filter_rule_group = null`

**⚠️ Record operation constraints**:
1. When `perm = read_only`, `record_rule.record_operations` **must be empty**
2. For synced tables (`is_sync = true`), add and delete operations are **strictly prohibited**

---

### field_perms construction SOP

When generating `field_perms`, do **not** rely on vague “inheritance” assumptions. Follow these steps:

| Step | Action | Description |
|------|------|------|
| 1. Baseline | For `perm = edit`, prefill all fields as `"edit"`; for `perm = read_only`, prefill as `"read"` | Based on full field list from `base_table_info` |
| 2. Physical downgrade | Formula / Lookup / AutoNumber and system fields -> force downgrade to `"read"` | Immutable fields must not be `edit` |
| 3. User override | Apply `no_perm` / `read` / `create` only to fields explicitly specified by user | Unspecified fields keep baseline |
| 4. Anti-filter misjudgment | Fields used in `filter_rules` keep `"edit"` if baseline is `"edit"` and user did not request downgrade | Filter usage does not imply read-only |
| 5. Filter dependency safety | Fields appearing in `filter_rules` must not be omitted; permission must be at least `"read"` | Final validation step |

**⚠️ `field_perm_mode` selection rules**:
1. If user expresses overall scope (“all fields”, “full-field”) and does not request option modification, **must** use `all_edit` / `all_read`; **do not** switch to per-field `specify`
2. Use `specify` only when user explicitly requests per-field differences, targets clearly differ by field, or option-modification permissions are explicitly requested
3. Auto-downgrades caused by system hard constraints do **not** count as a difference and should not trigger `specify`
4. For restrictive qualifiers like “only”, “must only”, “partial”, set out-of-scope fields in the opposite direction of the qualifier

**⚠️ Synced table constraint**: for `is_sync = true`, fields must **never** be set to `edit` or `create`

---

### Default strategy for view permissions

**Decision flow (must follow order, stop at first match):**

1. **First, determine whether the user mentioned specific view names** (for example, “Kanban view visible”, “Gantt view not editable”)
  - **Yes** -> `all_visible = false`, and `visible_views` contains only the explicitly mentioned visible view names (not view IDs). Unmentioned views are treated as not visible.
  - **No** (user did not mention any view) -> `all_visible = true`
2. `allow_edit` defaults to `false`. Set to `true` only when user explicitly requests editable/create/delete/manage views. Even when `true`, `visibility` is still mandatory (see View Rule Case A).
3. When `all_visible = false`, `visible_views` **must not be empty**

**❌ Common error - missing `visibility`:**
```json
// mistake! missing visibility
{ "view_rule": { "allow_edit": false } }
```
**✅ Correct:**
```json
// Even if everything is visible, visibility must be written explicitly
{ "view_rule": { "allow_edit": false, "visibility": { "all_visible": true } } }
```

---

### Hard constraints between field types and filter operators

When a field is used in record filters, there is a fixed binding between field type (`FieldType`) and operator (`Operator`):

**User / CreatedUser fields:**
- Only `contains` is allowed
- `is`, `isNot`, and other exact-match operators are not allowed
- No explicit value is needed in filter condition (system auto-matches current member)

**SingleSelect / Stage fields:**
- `is` and `isNot` can only match a **single option**, not multiple values
- For user intents like “equals / not equals one specific option” (for example, “attendance status is not present”), use `is` / `isNot` with exactly one value in `filter_values`
- For intents like “equals / not equals a set of options” (for example, “education is not junior college or other”), use `contains` / `doesNotContain` and include multiple values in `filter_values`
- `filter_values` in `contains` / `doesNotContain` can include multiple values (OR semantics)

**MultiSelect fields:**
- `is` / `isNot`: `filter_values` may include multiple options
  - With `operator = is` and options A,B selected, semantics are “contains both A and B” (A&B), not “equals A or B”
  - For “contains any of these options”, besides using `contains`, you can also use `is` with `filter_rules.conjunction = or`
- `contains` / `doesNotContain`: used for “contains any / does not contain any”; multiple values are allowed in `filter_values` (handled as any-match). To represent “equals A or equals B”, split into multiple filter conditions and combine with OR.

**Percentage fields**
- For numeric filters involving percentages, preserve user numeric meaning exactly by converting percentages to decimals. For example, “greater than 20%” -> “greater than 0.2”; “rate less than 60” -> “less than 0.6”.

### Forced field_perms rules for fields used in filters

When a field (excluding system fields) is used in “records matching specific conditions” filters, the system automatically applies these **non-overridable constraints** based on current table and record permissions:

**Read/write consistency for filter fields:**
- If table permission is `edit` and field type is in the editable-field category, that filter field must remain `edit` unless user explicitly requests downgrade
- Do not downgrade a field to `read` just because it is used in filters. Filters require visibility, not read-only status.

**Minimum field permission when add-record is allowed:**
- If and only if record permissions include add-record, the field must be at least `create`, so filtered fields can be written correctly on record creation
- If record permissions are read-only, this constraint does not apply

**Whether a field must be `edit` is not an infra-enforced requirement** and depends on the concrete permission plan.

System-enforced permissions above cannot be manually removed or downgraded.
