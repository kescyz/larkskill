# base shortcut record JSON specification (lark-base-shortcut-record-value)

> Applicable operations: `record-upsert` (MCP tool `lark_api`)

This file defines the recommended JSON format for the `body` when writing records via MCP tool calls. The goal is to allow the AI to write correctly on the first attempt.

## 1. Top-level rules (must be followed)

- `--json` Must Yes JSON object.
- Directly pass the field mapping from the top level: `{"fieldname orfieldID": value}`.
- Only use one key (field name or field ID) for the same field in a payload, do not repeat it.
- `+field-list` getfield `type/style/multiple` before writing, and then construct the value.

## 2. Each type value format and example

### 2.1 text / phone / url

**Recommended value**: String.

```json
{
    "Title": "Hello",
    "Contact number": "1380000000000",
    "Official website": "https://example.com"
}
```

**Schema**

```json
{ "type": "string", "description": "text field cell, example: \"one string and [one url](https://foo.bar)\"" }
```

### 2.2 number

**Recommended Value**: Number.

```json
{
    "Working Hours": 12.5,
    "Budget": 3000
}
```

**Schema**

```json
{ "type": "number", "description": "number field cell, can be any float64 value" }
```

### 2.3 select (single selection/multiple selection/stage)

**Recommended value**:
- Radio selection: string
-Multiple selection: string array

```json
{
    "Status": "Todo",
    "Tag": ["Backend", "High Quality"]
}
```

**Schema**

```json
{ "type": "array", "items": { "type": "string", "description": "option name" }, "description": "select field cell, example: [\"option_1\", \"option_2\"]" }
```

### 2.4 datetime

**Recommended value**: `YYYY-MM-DD HH:mm:ss` string (safe writing).

```json
{
    "Deadline": "2026-03-24 10:00:00"
}
```

**Schema**

```json
{ "type": "string", "description": "datetime field cell. accepts common datetime strings and timestamp-like values. Prefer \"YYYY-MM-DD HH:mm:ss\" in requests because it is the most stable format and matches the API output. Example: \"2026-01-01 19:30:00\"" }
```

### 2.5 checkbox

**Recommended Value**: Boolean value.

```json
{
    "Completed": true
}
```

**Schema**

```json
{ "type": "boolean", "description": "checkbox field cell" }
```

### 2.6 user

**Recommended value**: Array of objects with at least `id` elements.

```json
{
    "Responsible Person": [
      { "id": "ou_xxx" }
    ]
}
```

**Schema**

```json
{ "type": "array", "items": { "type": "object", "properties": { "id": { "type": "string", "description": "user id" } }, "required": ["id"], "additionalProperties": false }, "description": "user field cell, example: [{\"id\": \"ou_123\"}]" }
```

### 2.7 link

**Recommended value**: Array of objects with at least `id` elements.

```json
{
    "Associated tasks": [
      { "id": "rec_xxx" }
    ]
}
```

**Schema**

```json
{ "type": "array", "items": { "type": "object", "properties": { "id": { "type": "string", "description": "record id" } }, "required": ["id"], "additionalProperties": false }, "description": "link field cell, example: [{\"id\": \"rec_123\"}]" }
```

### 2.8 location

**Recommended value**: Object `{lng, lat}`.

```json
{
    "Coordinates": {
      "lng": 116.397428,
      "lat": 39.90923
    }
}
```

**Schema**

```json
{
  "type": "object",
  "properties": { "lng": { "type": "number", "description": "Longitude" }, "lat": { "type": "number", "description": "Latitude" } },
  "required": ["lng", "lat"],
  "additionalProperties": false,
  "description": "location field cell, example: {\"lng\": 113.94765, \"lat\": 22.528533}"
}
```

### 2.9 attachment

For the agent, attachment upload is a **special case**: if the user wants to add local files to a record, use `record-upload-attachment` (POST `.../records/{record_id}/attachment`) to upload to the existing record.

**Schema - attachment**

```json
{
  "type": "array",
  "items": { "type": "object", "properties": { "file_token": { "type": "string", "minLength": 0, "maxLength": 50 }, "name": { "type": "string", "minLength": 1, "maxLength": 255 } }, "required": ["file_token", "name"], "additionalProperties": false },
  "description": "attachment field cell. For agent, do not synthesize this payload via +record-upsert; must use +record-upload-attachment to upload files."
}
```

## 3. Read-only field (do not write)

The following fields should be treated as read-only when writing records:
- `auto_number`
- `lookup`
- `formula`
- `created_time` / `modified_time`
- `created_by` / `modified_by`

## 4. Complete example available quickly

```json
{
    "Title": "Created from shortcut",
    "Status": "Todo",
    "Tag": ["High Quality", "External Dependency"],
    "working hours": 8,
    "Deadline": "2026-03-24 10:00:00",
    "Completed": false,
    "Responsible person": [{ "id": "ou_123" }],
    "Associated tasks": [{ "id": "rec_456" }],
    "Coordinates": { "lng": 116.397428, "lat": 39.90923 }
}
```
