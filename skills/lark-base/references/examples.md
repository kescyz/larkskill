# Base Usage Scenarios

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Complete examples covering common Base operations via MCP tool `lark_api`.

---

## Scenario 1: Create a table with fields

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables
- body:
  ```json
  {
    "name": "Customer Management Table",
    "fields": [
      {"name": "Customer name", "type": "text"},
      {"name": "Person in charge", "type": "user", "property": {"multiple": false}},
      {"name": "Signature date", "type": "datetime"},
      {"name": "Status", "type": "single_select", "property": {"options": ["In progress", "Completed"]}}
    ]
  }
  ```

---

## Scenario 2: List fields in a table

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/fields
- params:
  ```json
  { "page_size": 100 }
  ```

---

## Scenario 3: Create, read, and update a single record

### Create record

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records
- body:
  ```json
  {
    "fields": {
      "Customer Name": "ByteDance",
      "Responsible person": [{"id": "ou_xxx"}],
      "Status": "In progress"
    }
  }
  ```

### List records

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records
- params:
  ```json
  { "page_size": 100 }
  ```

### Update record

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}
- body:
  ```json
  {
    "fields": {
      "Status": "Completed"
    }
  }
  ```

### Delete record

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records/{record_id}

---

## Scenario 4: Configure a view filter, then read records by view

The API does not provide standalone search. For filtered querying, set a view filter first, then read records via `view_id`.

### Set view filter conditions

Call MCP tool `lark_api`:
- method: PUT
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/views/{view_id}/filter
- body:
  ```json
  {
    "logic": "and",
    "conditions": [
      {
        "field_name": "Status",
        "operator": "is",
        "value": ["In progress"]
      }
    ]
  }
  ```

### Read records filtered by view

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}/tables/{table_id}/records
- params:
  ```json
  { "view_id": "vewXXXXXXXX", "page_size": 100 }
  ```

---

## Scenario 5: When to use which operation

| Goal | Operation |
|------|-----------|
| One-shot table creation with fields | POST `/tables` with `fields` array |
| Upsert by business field | PATCH `/records/{record_id}` or POST `/records` |
| Filtered view | PUT `/views/{view_id}/filter` then GET records with `view_id` |
| Record history | GET `/tables/{table_id}/records/{record_id}/record_history` |

## References

- [lark-base-table-create.md](lark-base-table-create.md) — Create a table
- [lark-base-record-upsert.md](lark-base-record-upsert.md) — Create or update records
- [lark-base-view-set-filter.md](lark-base-view-set-filter.md) — Set view filter
- [lark-base-record-history-list.md](lark-base-record-history-list.md) — Record history
