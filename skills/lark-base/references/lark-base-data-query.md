# data-query

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Run aggregation queries on Base data (grouping, filtering, sorting, and aggregation calculations) with JSON DSL.

## Constraints

- **Permission requirement:** Caller must be an admin of the target Base and have FA (Full Access), otherwise permission errors are returned.
- **Supported field types** (whitelist for dimensions / measures / filters / sort):
  text, email, barcode, number, progress, currency, rating, single select, multi select, date, checkbox, user, hyperlink
- **Unsupported field types:**
  formula, lookup, attachment, duration, stage, created time, modified time, created by, modified by, group, phone number, auto number, location, relation, bidirectional relation

## Recommended call

Group count by field:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/data/query
- body:
  ```json
  {
    "datasource": {"type": "table", "table": {"tableId": "tblxxxxxxxx"}},
    "dimensions": [{"field_name": "city", "alias": "dim_city"}],
    "measures": [{"field_name": "city", "aggregation": "count", "alias": "count"}],
    "shaper": {"format": "flat"}
  }
  ```

With filter conditions + sorting + limit:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/data/query
- body:
  ```json
  {
    "datasource": {"type": "table", "table": {"tableId": "tblxxxxxxxx"}},
    "dimensions": [{"field_name": "city", "alias": "dim_city"}],
    "measures": [{"field_name": "amount", "aggregation": "sum", "alias": "total_amount"}],
    "filters": {
      "type": 1,
      "conjunction": "and",
      "conditions": [{"field_name": "city", "operator": "isNot", "value": [""]}]
    },
    "sort": [{"field_name": "total_amount", "order": "desc"}],
    "pagination": {"limit": 100},
    "shaper": {"format": "flat"}
  }
  ```

Use `tableName` instead of `tableId`:

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/data/query
- body:
  ```json
  {
    "datasource": {"type": "table", "table": {"tableName": "Sales Data"}},
    "measures": [{"field_name": "amount", "aggregation": "sum", "alias": "total"}],
    "shaper": {"format": "flat"}
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base App token (path param) |
| `datasource` | Yes | Data source: `{"type":"table","table":{"tableId":"..."}}` or `{"tableName":"..."}` |
| `dimensions` | No* | Grouping dimensions (GROUP BY) |
| `measures` | No* | Aggregation measures |
| `filters` | No | Filter conditions (WHERE) |
| `sort` | No | Sort rules |
| `pagination` | No | Row limit `{limit: N}`, max 5000 |
| `shaper` | No | Fixed `{"format": "flat"}` |

> *At least one of `dimensions` and `measures` is required.

## Extract params from URL

Users often provide a URL like:

```
https://example.feishu.cn/base/<app_token>?table=<table_id>
```

- `base_token`: value after `/base/`
- `tableId` in DSL: value after `table=`

## API request details

```
POST /open-apis/base/v3/bases/{base_token}/data/query
```

**Request body - DSL schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `datasource` | object | Yes | Data source object with `type` (fixed `"table"`) and `table` |
| `datasource.table.tableId` | string | one-of-two | Target table ID |
| `datasource.table.tableName` | string | one-of-two | Target table name |
| `dimensions` | Dimension[] | No* | Grouping dimensions (GROUP BY) |
| `measures` | Measure[] | No* | Aggregation measures |
| `filters` | FilterGroup | No | Filter conditions (WHERE) |
| `sort` | Sort[] | No | Sort rules |
| `pagination` | object | No | Row limit `{limit: N}`, max 5000 |
| `shaper` | object | No | Result shape, fixed `{format: "flat"}` |

**Dimension fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field_name` | string | Yes | Field name |
| `alias` | string | No | Output alias, globally unique |

**Measure fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field_name` | string | Yes | Field name |
| `aggregation` | string | Yes | `sum`, `avg`, `min`, `max`, `count`, `count_all`, `distinct_count` |
| `alias` | string | No | Output alias, globally unique |

**Aggregation support by field type:**

| Aggregation | Supported field types |
|-------------|----------------------|
| `sum` / `avg` | number, progress, currency, rating (not checkbox) |
| `min` / `max` | number, progress, currency, rating, date |
| `count` | all whitelist types, non-empty count |
| `count_all` | all whitelist types, row count |
| `distinct_count` | all whitelist types |

**FilterGroup example:**

```json
{
  "filters": {
    "type": 1,
    "conjunction": "and",
    "conditions": [
      {"field_name": "city", "operator": "is", "value": ["Beijing"]}
    ]
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | int | Yes | Fixed `1` |
| `conjunction` | string | No | `"and"` or `"or"`, default `"and"` |
| `conditions` | Condition[] | No | Condition list |

**Condition fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field_name` | string | Yes | Field name, exact match required |
| `operator` | string | Yes | Operator (see table below) |
| `value` | string[] | Yes | Value array. For `isEmpty` / `isNotEmpty`, must be `[]` |

**Operators:**

| Operator | Description |
|----------|-------------|
| `is` | equals |
| `isNot` | not equals |
| `contains` | contains |
| `doesNotContain` | does not contain |
| `isEmpty` | is empty |
| `isNotEmpty` | is not empty |
| `isGreater` | greater than |
| `isGreaterEqual` | greater or equal |
| `isLess` | less than |
| `isLessEqual` | less or equal |

### Value format by field type

**Text / Email / Barcode**

| Operator | value format | count | example |
|----------|--------------|-------|---------|
| `is` / `isNot` / `contains` / `doesNotContain` | `["text"]` | exactly 1 | `["Hello"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 | `[]` |

**Number / Currency**

| Operator | value format | count | example |
|----------|--------------|-------|---------|
| `is` / `isNot` / `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual` | `["numeric-string"]` | exactly 1 | `["23.4"]`, `["-100"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 | `[]` |

**Progress**

| Operator | value format | count | example |
|----------|--------------|-------|---------|
| `is` / `isNot` / `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual` | `["decimal-string"]` | exactly 1 | `["0.34"]` (=34%) |
| `isEmpty` / `isNotEmpty` | `[]` | 0 | `[]` |

**Rating**

| Operator | value format | count | example |
|----------|--------------|-------|---------|
| `is` / `isNot` / `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual` | `["numeric-string"]` | exactly 1 | `["4"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 | `[]` |

**Single select / Multi select**

| Operator | value format | count | example |
|----------|--------------|-------|---------|
| `is` / `isNot` | `["OptionA"]` | exactly 1 | `["OptionA"]` |
| `contains` / `doesNotContain` | `["OptionA","OptionB"]` | multiple | `["OptionA","OptionB"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 | `[]` |

**User**

| Operator | value format | count | example |
|----------|--------------|-------|---------|
| `is` / `isNot` | `["ou_aaa"]` | exactly 1 | `["ou_aaa"]` |
| `contains` / `doesNotContain` | `["ou_aaa","ou_bbb"]` | multiple | `["ou_aaa","ou_bbb"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 | `[]` |

Use `open_id` (`ou_` prefix). ID conversion is handled at API layer.

**Hyperlink**

| Operator | value format | count | example |
|----------|--------------|-------|---------|
| `is` / `isNot` / `contains` / `doesNotContain` | `["Click to view"]` | exactly 1 | `["Click to view"]` |
| `isEmpty` / `isNotEmpty` | `[]` | 0 | `[]` |

Filter by display name, not raw URL.

**Checkbox**

| Operator | value format | count | example |
|----------|--------------|-------|---------|
| `is` | `["true"]` or `["false"]` | exactly 1 | `["true"]` |

Only `is` is supported.

**Date**

Date supports only `is`, `isEmpty`, `isNotEmpty`, `isGreater`, `isLess`.

Value uses predefined keywords as first element:

| Keyword | Description | value format | Operators |
|---------|-------------|--------------|-----------|
| `ExactDate` | exact date | `["ExactDate","1773187200000"]` (ms timestamp) | `is`, `isGreater`, `isLess` |
| `Today` | today | `["Today"]` | `is`, `isGreater`, `isLess` |
| `Tomorrow` | tomorrow | `["Tomorrow"]` | `is`, `isGreater`, `isLess` |
| `Yesterday` | yesterday | `["Yesterday"]` | `is`, `isGreater`, `isLess` |
| `CurrentWeek` | current week | `["CurrentWeek"]` | `is` |
| `LastWeek` | last week | `["LastWeek"]` | `is` |
| `CurrentMonth` | current month | `["CurrentMonth"]` | `is` |
| `LastMonth` | last month | `["LastMonth"]` | `is` |
| `TheLastWeek` | last 7 days | `["TheLastWeek"]` | `is` |
| `TheNextWeek` | next 7 days | `["TheNextWeek"]` | `is` |
| `TheLastMonth` | last 30 days | `["TheLastMonth"]` | `is` |
| `TheNextMonth` | next 30 days | `["TheNextMonth"]` | `is` |

Notes:
- ExactDate timestamp is converted to 00:00 in document timezone during filtering.
- Range keywords support only `is`.
- Keywords are case-sensitive.

**Sort fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field_name` | string | Yes | Field name or alias |
| `order` | string | No | `"asc"` (default) or `"desc"` |

**Pagination fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | int | No | Positive integer, max 5000, no offset support |

**Shaper fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `format` | string | Yes | Fixed `"flat"` |

## API response details

**Success example:**

```json
{"code": 0, "data": {"main_data": [{"dim_city": {"value": "Beijing"}, "total_amount": {"value": 12345.00}}]}, "msg": ""}
```

**Failure example:**

```json
{"code": 800004006, "data": {"error": {"code": 800004006}}, "msg": "DSL validation failed"}
```

**Response fields:**

| Field | Type | Description |
|-------|------|-------------|
| `code` | int | Status code, `0` means success |
| `msg` | string | Error message |
| `data.main_data` | []object | Query result rows |
| `data.error` | object | Error details on failure |

Each row field value is wrapped in CellValue:

```json
{
  "dim_city": {"value": "Beijing"},
  "total_amount": {"value": 12345.00}
}
```

## Workflow

1. Confirm `base_token` and `table_id`
2. Inspect table schema first via `lark_api GET /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields`
3. From field list:
   - get exact `field_name`
   - keep only supported field types
4. Build DSL JSON body
5. Call `lark_api POST .../data/query`
6. Interpret response:
   - rows in `data.main_data`
   - keys are aliases (or auto-generated names)
   - actual values are in `value`
   - failures appear in `data.error`

## Pitfalls

- ⚠️ Always inspect table schema first. `field_name` must match exactly (case-sensitive).
- ⚠️ Caller must have FA (Full Access).
- ⚠️ Use English aliases only.
- ⚠️ Endpoint is `base/v3`, not `bitable/v1`.
- ⚠️ At least one of `dimensions` and `measures` is required.
- ⚠️ `shaper` should be explicitly set to `{"format":"flat"}`.
- ⚠️ Use either `tableId` or `tableName`, not both.
- ⚠️ `pagination.limit` max is 5000, no offset support.
- ⚠️ All aliases must be globally unique.

## References

- [lark-base](../SKILL.md) - all Base commands
- [lark-shared](../../lark-shared/SKILL.md) - auth and global flags
- [lark-base-shortcut-record-value.md](lark-base-shortcut-record-value.md) - shortcut field value spec
- [lark-base-shortcut-field-properties.md](lark-base-shortcut-field-properties.md) - shortcut field types and JSON schema
