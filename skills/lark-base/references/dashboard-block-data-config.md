# Dashboard Block data_config Reference

The `data_config` schema of a block varies by `type`. This document describes all shared structures.

## Supported component types (`type` enum)

| type value | Description |
|---------|------|
| `column` | Column chart |
| `bar` | Bar chart |
| `line` | Line chart |
| `pie` | Pie chart |
| `ring` | Donut chart |
| `area` | Area chart |
| `combo` | Combo chart |
| `scatter` | Scatter chart |
| `funnel` | Funnel chart |
| `wordCloud` | Word cloud |
| `radar` | Radar chart |
| `statistics` | KPI card |

## Field type and operator quick reference (for AI decision-making)

> `+field-list` returned `type` field mapping: number, text, select (single select), multi_select, datetime, checkbox, user

```
Text/Phone/URL/Email:       is, isNot, contains, doesNotContain, isEmpty, isNotEmpty
Number/Currency/Progress:   is, isNot, isGreater, isGreaterEqual, isLess, isLessEqual, isEmpty, isNotEmpty
SingleSelect:               is, isNot, isEmpty, isNotEmpty
MultiSelect:                is, isNot, contains, doesNotContain, isEmpty, isNotEmpty
DateTime:                   is, isGreater, isGreaterEqual, isLess, isLessEqual, isEmpty, isNotEmpty
Checkbox:                   is (value: true/false)
User/CreatedBy/ModifiedBy:  is, isNot, isEmpty, isNotEmpty
```

## Common data_config structure

| Field | Type | Description |
|------|------|------|
| `table_name` | string | Associated table name |
| `series` | `[{ "field_name": "xxx", "rollup": "SUM" }]` | Metric / Y-axis (mutually exclusive with `count_all`). `rollup` supports `SUM` / `MAX` / `MIN` / `AVERAGE` |
| `count_all` | boolean | COUNTA aggregation, counts all records (mutually exclusive with `series`) |
| `group_by` | `[{ "field_name": "xxx", "mode": "integrated", "sort": {...} }]` | X-axis grouping dimensions. `mode` is required, `sort` is optional (see below) |
| `filter` | object | Filter conditions |
| `filter.conjunction` | `"and"` / `"or"` | Filter logic |
| `filter.conditions` | `[{ "field_name", "operator", "value" }]` | Filter condition array. `value` type depends on field type (see filter format rules below) |

## group_by details

### mode enum

| mode | Meaning | Use case |
|------|------|----------|
| `integrated` | Aggregated grouping (default) | Most scenarios, group and aggregate by field value |
| `enumerated` | Multi-value split counting | Multi-select, user, and other multi-value fields; splits each option/person for independent counting |

> Multi-select, user, and other multi-value fields default to `enumerated`; other fields default to `integrated`.

### sort ordering

| sort.type | Meaning | Typical scenario |
|-----------|------|----------|
| `group` | Sort by X-axis value | By month ascending, by category name alphabetically |
| `value` | Sort by Y-axis value | By sales amount descending |
| `view` | Sort by data source record order | Preserve original table row order (uncommon) |

`sort.order`: `asc` (ascending) / `desc` (descending)

Example - column chart sorted by sales descending:

```json
{
  "table_name": "Orders",
  "series": [{ "field_name": "Amount", "rollup": "SUM" }],
  "group_by": [{ "field_name": "Category", "mode": "integrated", "sort": {"type": "value", "order": "desc"} }]
}
```

## Filter format rules

**Basic structure:**

```json
{
  "filter": {
    "conjunction": "and",
    "conditions": [
      { "field_name": "field name", "operator": "operator", "value": "value" }
    ]
  }
}
```

**Multi-condition example (and/or):**

```json
{
  "filter": {
    "conjunction": "and",
    "conditions": [
      { "field_name": "Status", "operator": "is", "value": "Completed" },
      { "field_name": "Amount", "operator": "isGreater", "value": 1000 }
    ]
  }
}
```

**Operators:**

| Operator | Meaning | Requires `value` |
|--------|------|---------------|
| `is` | equals | Yes |
| `isNot` | not equals | Yes |
| `contains` | contains | Yes |
| `doesNotContain` | does not contain | Yes |
| `isEmpty` | is empty | No |
| `isNotEmpty` | is not empty | No |
| `isGreater` | greater than | Yes |
| `isGreaterEqual` | greater than or equal | Yes |
| `isLess` | less than | Yes |
| `isLessEqual` | less than or equal | Yes |

**`value` format by field type:**

| Field type | `value` type | Applicable operators | Example |
|----------|-----------|-----------|------|
| Text / Phone / URL / Email | string | is, isNot, contains, doesNotContain, isEmpty, isNotEmpty | `{"field_name":"Name","operator":"contains","value":"Zhang"}` |
| Number / Currency / Progress | number | is, isNot, isGreater, isGreaterEqual, isLess, isLessEqual, isEmpty, isNotEmpty | `{"field_name":"Amount","operator":"isGreater","value":0}` |
| SingleSelect | string (option name) | is, isNot, isEmpty, isNotEmpty | `{"field_name":"Status","operator":"is","value":"Completed"}` |
| MultiSelect | string[] (multiple) / string (single) | is, isNot, contains, doesNotContain, isEmpty, isNotEmpty | Multi-select passes array e.g. `["Tag1","Tag2"]`; single passes a string |
| DateTime / CreatedTime / ModifiedTime | number (Unix millisecond timestamp, 13 digits) | is, isGreater, isGreaterEqual, isLess, isLessEqual, isEmpty, isNotEmpty | `{"field_name":"Created Date","operator":"isGreater","value":1704038400000}` |
| Checkbox | boolean | is | `{"field_name":"Reviewed","operator":"is","value":true}` |
| User / CreatedBy / ModifiedBy | string or string[] (user ID, format `ou_xxx`) | is, isNot, isEmpty, isNotEmpty | `{"field_name":"Owner","operator":"is","value":"ou_xxxxxxxxxxxxxxxx"}` |
| All types (empty/non-empty) | no `value` needed | isEmpty, isNotEmpty | `{"field_name":"Notes","operator":"isEmpty"}` |

> `value` type can be `string | number | boolean | string[]`; must match the correct format for the field type

## Constraints and local validation

- Required and mutually exclusive
  - Required: `table_name`
  - Mutually exclusive: `series` and `count_all`; at least one must be provided
- Length / structure
  - `group_by` supports at most 2 items; each item requires `field_name`
  - `group_by[].sort.type` must be `group|value|view`; `order` must be `asc|desc`
- Normalization (auto-handled by CLI)
  - `series[].rollup` is normalized to uppercase (e.g. `sum` -> `SUM`)
  - `group_by[].sort.type/order` is normalized to lowercase
- Local validation (can be skipped with `--no-validate`)
  - `+dashboard-block-create/update` performs lightweight validation for `data_config` by default; failures are aggregated with repair hints
  - Only valid JSON is required; the CLI will not silently rewrite business semantics

## Copyable templates

**Choose template by intent:**
- Compare values across categories -> column chart / bar chart
- View trend changes -> line chart / area chart
- View proportion distribution -> pie chart / donut chart / word cloud
- Multi-metric comparison -> combo chart
- View relationship between two variables -> scatter chart
- View process conversion -> funnel chart
- View multi-dimension scores -> radar chart
- Display a single metric -> KPI card (numeric stat or record count)

Minimal column chart:

```json
{
  "table_name": "table name",
  "series": [{ "field_name": "numeric field", "rollup": "SUM" }],
  "group_by": [{ "field_name": "group field", "mode": "integrated" }]
}
```

Minimal pie/donut chart (count rows by category):

```json
{
  "table_name": "table name",
  "count_all": true,
  "group_by": [{ "field_name": "category field", "mode": "integrated" }]
}
```

Line chart (monthly trend):

```json
{
  "table_name": "table name",
  "series": [{ "field_name": "Amount", "rollup": "SUM" }],
  "group_by": [{ "field_name": "Month", "mode": "integrated", "sort": {"type":"group","order":"asc"} }]
}
```

Bar chart (horizontal column chart):

```json
{
  "table_name": "table name",
  "series": [{ "field_name": "numeric field", "rollup": "SUM" }],
  "group_by": [{ "field_name": "group field", "mode": "integrated" }]
}
```

Area chart (trend with fill):

```json
{
  "table_name": "table name",
  "series": [{ "field_name": "numeric field", "rollup": "SUM" }],
  "group_by": [{ "field_name": "time field", "mode": "integrated", "sort": {"type":"group","order":"asc"} }]
}
```

Combo chart (column + line multi-metric comparison):

```json
{
  "table_name": "table name",
  "series": [
    { "field_name": "metric1", "rollup": "SUM" },
    { "field_name": "metric2", "rollup": "SUM" }
  ],
  "group_by": [{ "field_name": "category field", "mode": "integrated" }]
}
```

Scatter chart (two-variable correlation):

```json
{
  "table_name": "table name",
  "series": [{ "field_name": "Y-axis field (numeric/metric)", "rollup": "SUM" }],
  "group_by": [{ "field_name": "X-axis field (category/dimension)", "mode": "integrated" }]
}
```

Funnel chart (process conversion):

```json
{
  "table_name": "table name",
  "series": [{ "field_name": "numeric field", "rollup": "SUM" }],
  "group_by": [{ "field_name": "stage field", "mode": "integrated" }]
}
```

Word cloud (text frequency):

```json
{
  "table_name": "table name",
  "count_all": true,
  "group_by": [{ "field_name": "text field", "mode": "integrated" }]
}
```

Radar chart (multi-dimension scores):

```json
{
  "table_name": "table name",
  "series": [
    { "field_name": "dimension1", "rollup": "SUM" },
    { "field_name": "dimension2", "rollup": "SUM" },
    { "field_name": "dimension3", "rollup": "SUM" }
  ],
  "group_by": [{ "field_name": "category field", "mode": "integrated" }]
}
```

KPI card (numeric stat):

```json
{
  "table_name": "data table",
  "series": [{ "field_name": "number", "rollup": "SUM" }]
}
```

KPI card (record count):

```json
{
  "table_name": "data table",
  "count_all": true
}
```

## Common errors and fixes

- `series` and `count_all` are both present
  - Symptom: backend/local validation reports mutual exclusion error
  - Fix: see the mutual exclusion rule in "Constraints" section
- Missing `table_name`
  - Symptom: local validation reports missing required field
  - Fix: set source table name (use table name, not table ID)
- Invalid `series[].rollup` case/value
  - Symptom: local validation reports unsupported enum
  - Fix: use one of `SUM|MAX|MIN|AVERAGE` (case-insensitive input, CLI normalizes to uppercase; for counting use `count_all:true`)
- `group_by` exceeds 2 items or has empty field name
  - Fix: keep first two items, or provide missing `field_name`
- Invalid sort enum
  - Fix: `group_by.sort.type` only supports `group|value|view`; `order` supports `asc|desc`
- Invalid filter schema
  - Fix: `conjunction` must be `and|or`; `conditions[].operator` must be in the operator table on this page; except `isEmpty/isNotEmpty`, `value` is required

## Pitfalls

- **`count_all` and `series` are mutually exclusive** - they cannot be used together
- **Filter `value` type depends on field type** - text/single-select use string, number uses number, date uses millisecond timestamp, multi-select/user can use string[], checkbox uses boolean; `isEmpty`/`isNotEmpty` needs no `value`
- **`data_config` varies by `type`** - fields differ by component type, so verify required fields before creation
- **Table name uses name, not ID** - `table_name` corresponds to the table name (e.g. "Orders"), not `table_id`
