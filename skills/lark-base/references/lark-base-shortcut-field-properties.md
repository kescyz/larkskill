# base shortcut field JSON specification (lark-base-shortcut-field-properties)

> Applicable operations: `field-create`, `field-update` (MCP tool `lark_api`)

This file defines the recommended JSON format for the `body` when writing fields via MCP tool calls, to avoid mixing with old `type=number + field_name + property` structures.

## 1. Top-level rules (must be followed)

- `--json` must be a JSON object.
- Top level uses uniformly: `type` + `name` + type-specific fields.
- To add a field description, pass `description` directly; supports plain text and Markdown links.
- Do not use old structures: `field_name`, `property`, `ui_type`, numeric enum `type`.
- `+field-update` has `PUT` semantics; it is recommended to `+field-get` first and then fully submit the target field configuration.
- When creating `type=formula` or `type=lookup`, you must first read the corresponding guide.

```json
{
  "type": "text",
  "name": "Requirements Background",
  "description": "Record requirements background and known constraints; see [Specification Template](https://example.com/spec) for filling guidelines"
}
```

## 2. Each type format and example

### 2.1 text

**Requirements**: `name` required; optionally pass `description`; `style.type` optional, default `plain`.

```json
{
  "type": "text",
  "name": "title",
  "style": { "type": "plain" }
}
```

`style.type` Common values: `plain`, `phone`, `url`, `email`, `barcode`.

**Schema**

```json
{
  "type": "object",
  "properties": {
    "type": { "type": "string", "const": "text", "description": "Text field type" },
    "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" },
    "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" },
    "style": {
      "type": "object",
      "properties": { "type": { "type": "string", "enum": ["plain", "phone", "url", "email", "barcode"], "description": "Text style type" } },
      "required": ["type"],
      "additionalProperties": false,
      "description": "Text style",
      "default": { "type": "plain" }
    }
  },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Text field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

### 2.2 number

**Requirements**: `name` required; `style.type` commonly used `plain/currency/progress/rating`.

```json
{
  "type": "number",
  "name": "working hours",
  "style": {
    "type": "plain",
    "precision": 2,
    "percentage": false,
    "thousands_separator": true
  }
}
```

```json
{
  "type": "number",
  "name": "budget",
  "style": { "type": "currency", "precision": 2, "currency_code": "CNY" }
}
```

```json
{
  "type": "number",
  "name": "Completion",
  "style": { "type": "progress", "percentage": true, "color": "Blue" }
}
```

```json
{
  "type": "number",
  "name": "rating",
  "style": { "type": "rating", "icon": "star", "min": 1, "max": 5 }
}
```

**Schema**

```json
{
  "type": "object",
  "properties": {
    "type": { "type": "string", "const": "number", "description": "Number field type" },
    "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" },
    "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" },
    "style": {
      "anyOf": [
        {
          "type": "object",
          "properties": {
            "type": { "type": "string", "const": "plain", "description": "Plain style type" },
            "precision": { "type": "number", "minimum": 0, "maximum": 4, "default": 2, "description": "Decimal precision" },
            "percentage": { "type": "boolean", "default": false, "description": "Use percentage" },
            "thousands_separator": { "$ref": "#/properties/style/anyOf/0/properties/percentage", "default": false, "description": "Use thousand separator" }
          },
          "required": ["type"],
          "additionalProperties": false,
          "description": "Plain number style"
        },
        {
          "type": "object",
          "properties": {
            "type": { "type": "string", "const": "currency", "description": "Currency style type" },
            "precision": { "type": "number", "minimum": 0, "maximum": 4, "default": 2, "description": "Decimal precision" },
            "currency_code": {
              "type": "string",
              "enum": ["CNY", "USD", "EUR", "GBP", "AED", "AUD", "BRL", "CAD", "CHF", "HKD", "INR", "IDR", "JPY", "KRW", "MOP", "MXN", "MYR", "PHP", "PLN", "RUB", "SGD", "THB", "TRY", "TWD", "VND"],
              "default": "CNY",
              "description": "Currency code"
            }
          },
          "required": ["type"],
          "additionalProperties": false,
          "description": "Currency style"
        },
        {
          "type": "object",
          "properties": {
            "type": { "type": "string", "const": "progress", "description": "Progress style type" },
            "percentage": { "$ref": "#/properties/style/anyOf/0/properties/percentage", "default": true, "description": "Use percentage" },
            "color": {
              "type": "string",
              "enum": ["Blue", "Purple", "DarkGreen", "Green", "Cyan", "Orange", "Red", "Gray", "WhiteToBlueGradient", "WhiteToPurpleGradient", "WhiteToOrangeGradient", "GreedToRedGradient", "RedToGreenGradient", "BlueToPinkGradient", "PinkToBlueGradient", "SpectralGradient"],
              "description": "Progress color"
            }
          },
          "required": ["type", "color"],
          "additionalProperties": false,
          "description": "Progress style"
        },
        {
          "type": "object",
          "properties": {
            "type": { "type": "string", "const": "rating", "description": "Rating style type" },
            "icon": { "type": "string", "enum": ["star", "heart", "thumbsup", "fire", "smile", "lightning", "flower", "number"], "default": "star", "description": "Rating icon" },
            "min": { "type": "integer", "minimum": 0, "maximum": 1, "default": 1, "description": "Minimum rating" },
            "max": { "type": "integer", "minimum": 1, "maximum": 10, "default": 5, "description": "Maximum rating" }
          },
          "required": ["type"],
          "additionalProperties": false,
          "description": "Rating style"
        }
      ],
      "default": { "type": "plain" },
      "description": "Number style"
    }
  },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Number field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

### 2.3 select (single selection/multiple selection)

**Requirements**: `name` required; `multiple` controls single/multiple selections; `options` is an object array.

```json
{
  "type": "select",
  "name": "status",
  "multiple": false,
  "options": [
    { "name": "Todo", "hue": "Blue", "lightness": "Lighter" },
    { "name": "Done", "hue": "Green", "lightness": "Light" }
  ]
}
```

- `options[].name` Required。
- `options` Do not pass `id` (the creation scene is generated by the backend).

**Schema**

```json
{
  "type": "object",
  "properties": {
    "type": { "type": "string", "const": "select", "description": "Select field type" },
    "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" },
    "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" },
    "multiple": { "type": "boolean", "default": false, "description": "Allow multiple" },
    "options": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string", "description": "Option name" },
          "hue": { "type": "string", "enum": ["Red", "Orange", "Yellow", "Lime", "Green", "Turquoise", "Wathet", "Blue", "Carmine", "Purple", "Gray"], "description": "Option hue", "default": "Blue" },
          "lightness": { "type": "string", "enum": ["Lighter", "Light", "Standard", "Dark", "Darker"], "description": "Option lightness", "default": "Lighter" }
        },
        "required": ["name"],
        "additionalProperties": false,
        "description": "Select option"
      },
      "maxItems": 10000,
      "description": "Static options"
    }
  },
  "required": ["type", "name", "options"],
  "additionalProperties": false,
  "description": "Select field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

### 2.4 datetime / created_at / updated_at

**Requirements**: `name` required; `style.format` Optional.

```json
{
  "type": "datetime",
  "name": "deadline",
  "style": { "format": "yyyy-MM-dd HH:mm" }
}
```

```json
{ "type": "created_at", "name": "Creation time", "style": { "format": "yyyy/MM/dd" } }
```

```json
{ "type": "updated_at", "name": "update time", "style": { "format": "yyyy/MM/dd HH:mm" } }
```

**Schema - datetime**

```json
{
  "type": "object",
  "properties": {
    "type": { "type": "string", "const": "datetime", "description": "Date time type" },
    "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" },
    "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" },
    "style": {
      "type": "object",
      "properties": { "format": { "type": "string", "enum": ["yyyy/MM/dd", "yyyy/MM/dd HH:mm", "yyyy/MM/dd HH:mm Z", "yyyy-MM-dd", "yyyy-MM-dd HH:mm", "yyyy-MM-dd HH:mm Z", "MM-dd", "MM/dd/yyyy", "dd/MM/yyyy"], "default": "yyyy/MM/dd", "description": "Date format" } },
      "additionalProperties": false,
      "default": { "format": "yyyy/MM/dd" },
      "description": "Date time style"
    }
  },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Date time field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

**Schema - created_at**

```json
{
  "type": "object",
  "properties": {
    "type": { "type": "string", "const": "created_at", "description": "Created time type" },
    "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" },
    "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" },
    "style": {
      "type": "object",
      "properties": { "format": { "type": "string", "enum": ["yyyy/MM/dd", "yyyy/MM/dd HH:mm", "yyyy/MM/dd HH:mm Z", "yyyy-MM-dd", "yyyy-MM-dd HH:mm", "yyyy-MM-dd HH:mm Z", "MM-dd", "MM/dd/yyyy", "dd/MM/yyyy"], "default": "yyyy/MM/dd", "description": "Date format" } },
      "additionalProperties": false,
      "default": { "format": "yyyy/MM/dd" },
      "description": "Created time style"
    }
  },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Created time field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

**Schema - updated_at**

```json
{
  "type": "object",
  "properties": {
    "type": { "type": "string", "const": "updated_at", "description": "Modified time type" },
    "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" },
    "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" },
    "style": {
      "type": "object",
      "properties": { "format": { "type": "string", "enum": ["yyyy/MM/dd", "yyyy/MM/dd HH:mm", "yyyy/MM/dd HH:mm Z", "yyyy-MM-dd", "yyyy-MM-dd HH:mm", "yyyy-MM-dd HH:mm Z", "MM-dd", "MM/dd/yyyy", "dd/MM/yyyy"], "default": "yyyy/MM/dd", "description": "Date format" } },
      "additionalProperties": false,
      "default": { "format": "yyyy/MM/dd" },
      "description": "Modified time style"
    }
  },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Modified time field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

### 2.5 user / created_by / updated_by

```json
{ "type": "user", "name": "person in charge", "multiple": true }
```

```json
{ "type": "created_by", "name": "created by" }
```

```json
{ "type": "updated_by", "name": "Updated by" }
```

**Schema - user**

```json
{
  "type": "object",
  "properties": { "type": { "type": "string", "const": "user", "description": "User field type" }, "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" }, "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" }, "multiple": { "type": "boolean", "default": true, "description": "Allow multiple" } },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "User field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

**Schema - created_by**

```json
{
  "type": "object",
  "properties": { "type": { "type": "string", "const": "created_by", "description": "Created by type" }, "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" }, "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" } },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Created by field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

**Schema - updated_by**

```json
{
  "type": "object",
  "properties": { "type": { "type": "string", "const": "updated_by", "description": "Modified by type" }, "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" }, "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" } },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Modified by field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

### 2.6 link

**Requirements**: `link_table` required; `bidirectional` defaults to `false`.

```json
{
  "type": "link",
  "name": "Associated tasks",
  "link_table": "Task table",
  "bidirectional": true,
  "bidirectional_link_field_name": "reverse association"
}
```

**Schema**

```json
{
  "type": "object",
  "properties": {
    "type": { "type": "string", "const": "link", "description": "Link field type" },
    "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" },
    "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" },
    "link_table": { "type": "string", "minLength": 1, "maxLength": 100, "description": "Linked table" },
    "bidirectional": { "type": "boolean", "default": false, "description": "Bidirectional link" },
    "bidirectional_link_field_name": { "$ref": "#/properties/name", "description": "Bidirectional link field name" }
  },
  "required": ["type", "name", "link_table"],
  "additionalProperties": false,
  "description": "Link field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

### 2.7 formula

**Requirements**: `expression` required.

```json
{
  "type": "formula",
  "name": "Total",
  "expression": "1+1"
}
```

**Schema**

```json
{
  "type": "object",
  "properties": { "type": { "type": "string", "const": "formula", "description": "Formula field type" }, "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" }, "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" }, "expression": { "type": "string", "description": "Formula expression" } },
  "required": ["type", "name", "expression"],
  "additionalProperties": false,
  "description": "Formula field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

### 2.8 lookup

**Requirements**: `from`, `select`, `where` required; `aggregate` optional. `where.logic` only supports `and/or`, `conditions` Each item must be a Yes triplet `[field, op, value]`.

```json
{
  "type": "lookup",
  "name": "Status summary",
  "from": "task list",
  "select": "status",
  "where": {
    "logic": "and",
    "conditions": [
      ["Responsible person", "==", { "type": "field_ref", "field": "Current person in charge" }],
      ["status", "non_empty", null]
    ]
  },
  "aggregate": "raw_value"
}
```

**Schema**

```json
{
  "type": "object",
  "properties": {
    "type": { "type": "string", "const": "lookup", "description": "Lookup field type" },
    "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" },
    "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" },
    "from": { "type": "string", "minLength": 1, "maxLength": 100, "description": "Source data table" },
    "select": { "type": "string", "minLength": 1, "maxLength": 100, "description": "Field to aggregate from source table" },
    "where": {
      "type": "object",
      "properties": {
        "logic": { "type": "string", "enum": ["and", "or"], "default": "and", "description": "Filter Condition Logic" },
        "conditions": {
          "type": "array",
          "items": {
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": [
              { "type": "string", "minLength": 1, "maxLength": 100, "description": "Field from source table to filter on" },
              { "type": "string", "enum": ["==", "!=", ">", ">=", "<", "<=", "intersects", "disjoint", "empty", "non_empty"], "description": "Condition operator" },
              {
                "anyOf": [
                  {
                    "anyOf": [
                      {
                        "type": "object",
                        "properties": {
                          "type": { "type": "string", "const": "constant" },
                          "value": {
                            "anyOf": [
                              { "type": "string", "description": "text & formula & location field support string as filter value" },
                              { "type": "number", "description": "number & auto_number(the underfly incremental_number) field support number as filter value" },
                              { "type": "array", "items": { "type": "string", "description": "option name" }, "description": "select field support one option: [\"option1\"] or multiple options: `[\"option1\", \"option2\"]` as filter value." },
                              { "type": "array", "items": { "type": "object", "properties": { "id": { "type": "string", "description": "record id" } }, "required": ["id"], "additionalProperties": false }, "description": "link field support record id list as filter value" },
                              { "type": "string", "description": "\ndatetime & create_at & updated_at field support relative and absolute filter value.\nabsolute:\n- \"ExactDate(yyyy-MM-dd)\"\nrelative:\n- Today\n- Tomorrow\n- Yesterday\n" },
                              { "type": "array", "items": { "type": "object", "properties": { "id": { "type": "string", "description": "user id" } }, "required": ["id"], "additionalProperties": false }, "description": "user field support user id list as filter value" },
                              { "type": "boolean", "description": "checkbox field support boolean as filter value" }
                            ]
                          }
                        },
                        "required": ["type", "value"],
                        "additionalProperties": false,
                        "description": "Constant filter value"
                      },
                      {
                        "type": "object",
                        "properties": { "type": { "type": "string", "const": "field_ref" }, "field": { "type": "string", "minLength": 1, "maxLength": 100, "description": "Field id or name" } },
                        "required": ["type", "field"],
                        "additionalProperties": false,
                        "description": "Dynamic field reference from current table"
                      }
                    ]
                  },
                  { "type": "null" }
                ],
                "description": "Condition value (null for isEmpty/isNotEmpty)"
              }
            ],
            "description": "Lookup condition tuple: [fieldRef, operator, value?]"
          },
          "minItems": 1,
          "description": "Filter conditions"
        }
      },
      "required": ["conditions"],
      "additionalProperties": false
    },
    "aggregate": { "type": "string", "enum": ["raw_value", "sum", "average", "counta", "unique_counta", "max", "min", "unique"], "default": "raw_value", "description": "Aggregation function" }
  },
  "required": ["type", "name", "from", "select", "where"],
  "additionalProperties": false,
  "description": "Lookup field. You MUST Read xxx document first!",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

### 2.9 auto_number

```json
{
  "type": "auto_number",
  "name": "number",
  "style": {
    "rules": [
      { "type": "text", "text": "TASK-" },
      { "type": "incremental_number", "length": 4 }
    ]
  }
}
```

**Schema**

```json
{
  "type": "object",
  "properties": {
    "type": { "type": "string", "const": "auto_number", "description": "Auto number type" },
    "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" },
    "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" },
    "style": {
      "type": "object",
      "properties": {
        "rules": {
          "type": "array",
          "items": {
            "anyOf": [
              {
                "type": "object",
                "properties": { "type": { "type": "string", "const": "text", "description": "Text rule type" }, "text": { "type": "string", "description": "Prefix text" } },
                "required": ["type", "text"],
                "additionalProperties": false,
                "description": "Auto number text rule"
              },
              {
                "type": "object",
                "properties": { "type": { "type": "string", "const": "incremental_number", "description": "Increment rule type" }, "length": { "type": "integer", "minimum": 1, "maximum": 9, "description": "Serial length" } },
                "required": ["type", "length"],
                "additionalProperties": false,
                "description": "Auto number increment rule"
              },
              {
                "type": "object",
                "properties": {
                  "type": { "type": "string", "const": "created_time", "description": "Date rule type(auto fill record created date)" },
                  "date_format": { "type": "string", "enum": ["yyyyMMdd", "yyyyMM", "yyMM", "MMdd", "yyyy", "MM", "dd"], "description": "Date format" }
                },
                "required": ["type", "date_format"],
                "additionalProperties": false,
                "description": "Auto number date rule"
              }
            ]
          },
          "minItems": 1,
          "maxItems": 9,
          "description": "Numbering rules"
        }
      },
      "required": ["rules"],
      "additionalProperties": false,
      "default": {
        "rules": [
          { "type": "text", "text": "NO." },
          { "type": "incremental_number", "length": 3 }
        ]
      },
      "description": "Auto number style"
    }
  },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Auto number field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

### 2.10 attachment / location / checkbox

```json
{ "type": "attachment", "name": "attachment" }
```

```json
{ "type": "location", "name": "location" }
```

```json
{ "type": "checkbox", "name": "Complete" }
```

**Schema - attachment**

```json
{
  "type": "object",
  "properties": { "type": { "type": "string", "const": "attachment", "description": "Attachment field type" }, "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" }, "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" } },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Attachment field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

**Schema - location**

```json
{
  "type": "object",
  "properties": { "type": { "type": "string", "const": "location", "description": "Location field type" }, "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" }, "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" } },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Location field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

**Schema - checkbox**

```json
{
  "type": "object",
  "properties": { "type": { "type": "string", "const": "checkbox", "description": "Checkbox field type" }, "name": { "type": "string", "minLength": 1, "maxLength": 1000, "description": "Field name" }, "description": { "type": "string", "description": "Field description; supports plain text or Markdown links" } },
  "required": ["type", "name"],
  "additionalProperties": false,
  "description": "Checkbox field",
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

## 3. Recommended workflow

1. `+field-list` / `+field-get` First get the current field structure.
2. Construct `--json` according to this specification.
3. When `type=formula/lookup` is used, read the corresponding guide first and then create it.
