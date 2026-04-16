# view-set-filter

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Update the filter configuration of a view.

## Recommended call

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}/filter
- body:
  ```json
  {
    "logic": "and",
    "conditions": [
      ["fld_status", "intersects", ["Doing"]],
      ["fld_owner", "intersects", [{"id": "ou_xxx"}]],
      ["fld_end", "empty"]
    ]
  }
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `table_id` | Yes | Table ID or table name (path param) |
| `view_id` | Yes | View ID or view name (path param) |
| body | Yes | Filter configuration JSON object (body) |

## API request details

```
PUT /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}/filter
```

## Key return fields

- Returns the updated filter configuration.

## Structure rules

- `logic`: optional, `and` / `or`, default `and`
- `conditions`: array, can be empty; each item must be `[field, operator, value?]`
- `field`: field ID or field name, length `1–100`
- `operator`: `== != > >= < <= intersects disjoint empty non_empty`
- `value`: fill in according to field type; `empty` / `non_empty` can omit `value`

### Typical `value` shapes

- `text` / `location` / `formula`: string
- `number` / `auto_number`: number
- `select`: `["Todo"]`
- `user` / `created_by` / `updated_by`: `[{"id": "ou_xxx"}]`
- `link`: `[{"id": "rec_xxx"}]`
- `checkbox`: `true` / `false`
- `datetime` / `created_at` / `updated_at`: `"ExactDate(YYYY-MM-DD)"`, `"Today"`, `"Tomorrow"`, `"Yesterday"`

## JSON Schema

```json
{"type":"object","properties":{"logic":{"type":"string","enum":["and","or"],"default":"and","description":"Filter Condition Logic"},"conditions":{"type":"array","items":{"type":"array","minItems":3,"maxItems":3,"items":[{"type":"string","minLength":1,"maxLength":100,"description":"Field id or name"},{"type":"string","enum":["==","!=",">",">=","<","<=","intersects","disjoint","empty","non_empty"],"description":"Condition operator"},{"anyOf":[{"not":{}},{"anyOf":[{"anyOf":[{"type":"string","description":"text & formula & location field support string as filter value"},{"type":"number","description":"number & auto_number(the underfly incremental_number) field support number as filter value"},{"type":"array","items":{"type":"string","description":"option name"},"description":"select field support one option: [\"option1\"] or multiple options: `[\"option1\", \"option2\"]` as filter value."},{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","description":"record id"}},"required":["id"],"additionalProperties":false},"description":"link field support record id list as filter value"},{"type":"string","description":"\ndatetime & create_at & updated_at field support relative and absolute filter value.\nabsolute:\n- \"ExactDate(yyyy-MM-dd)\"\nrelative:\n- Today\n- Tomorrow\n- Yesterday\n"},{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","description":"user id"}},"required":["id"],"additionalProperties":false},"description":"user field support user id list as filter value"},{"type":"boolean","description":"checkbox field support boolean as filter value"}]},{"type":"null"}]}]}],"description":"one condition expression. shape: [field_id, filter_operator, value]. when operator is \"empty\" or \"non_empty\", the value is not required."},"default":[]}},"additionalProperties":false,"$schema":"http://json-schema.org/draft-07/schema#"}
```

## Workflow

1. Pull the current config with `view-get-filter` first, then make minimal modifications.

## Pitfalls

- This is a write operation; confirm with the user before execution.
- Conditions must use tuple form `[field, operator, value]`; do not use the old object style `{"field_name":...,"operator":...}`.
- `empty` / `non_empty` must not include a value; `select` / `user` / `link` must use array, not a single value.
- Date values must use the `ExactDate(...)` wrapper; do not pass bare date strings.

## References

- [lark-base-view.md](lark-base-view.md) — view index page
- [lark-base-view-get-filter.md](lark-base-view-get-filter.md) — read filter
