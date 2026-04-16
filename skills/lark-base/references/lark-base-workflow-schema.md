# workflow data structure reference

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Defines the complete JSON body structure for the `workflow-create` / `workflow-update` MCP calls (V2 protocol).

When creating or updating a workflow, pass this structure as the `body` of:

```
Call MCP tool `lark_api`:
- method: POST  (create) or PUT  (update)
- path: /open-apis/base/v1/apps/{app_token}/workflows[/{workflow_id}]
- body: { "title": "...", "steps": [ ...workflowStep[] ] }
```

---

## workflowStep base structure

Every step (Trigger / Action / Branch / System) shares these fields:

```json
{
  "id": "step_xxx",
  "type": "AddRecordTrigger",
  "title": "Monitor new orders",
  "children": {
    "links": []
  },
  "next": "step_yyy",
  "data": {}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique step ID (user-defined; referenced by `next` and `children.links[].to`) |
| `type` | string | Yes | Step type — see StepType enums below |
| `title` | string | No | Step title |
| `children` | StepChildren | No | Child relationships — branches and loops |
| `next` | string \| null | No | Linear successor node ID; `null` means end of flow |
| `data` | object | Yes | Step-specific configuration — varies by `type` |

> **General rule:** topology goes in `children`; extended identifiers go in `meta`; input parameters go in `data`.

---

## StepChildren and ChildLink

### StepChildren

```json
{
  "links": [ /* ChildLink[] */ ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `links` | ChildLink[] | Child relationship list; empty array `[]` when no children |

### ChildLink

Each edge describes a directed connection from the current node to a target node:

```json
{ "kind": "if_true", "to": "step_4", "label": "branch_1", "desc": "Amount greater than 1000" }
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `kind` | string | Yes | Relationship type: `if_true` / `if_false` / `case` / `loop_start` / `slot` |
| `to` | string | Yes | Target node ID |
| `label` | string | No | Optional tag (e.g. `branch_1`, `tool`, `llm`, `memory`) |
| `desc` | string | No | Optional semantic description (e.g. "Sales dept", "Positive sentiment") |

`kind` usage scenarios:

| kind | Used by node | Description |
|------|-------------|-------------|
| `if_true` | IfElseBranch | Jump when condition is true |
| `if_false` | IfElseBranch | Jump when condition is false |
| `case` | SwitchBranch / AIClassificationBranch | Multi-way branch; use `branch_1`-style neutral `label`, put semantics in `desc` |
| `loop_start` | Loop | Loop body entry point |
| `slot` | AIAgentAction | Mount LLM / tool / Memory child node; `label` is `llm` / `tool` / `memory` |

---

## StepType enums

### Trigger types

| type | Description |
|------|-------------|
| `AddRecordTrigger` | Triggered when a new record is added |
| `SetRecordTrigger` | Triggered when a record is modified |
| `ChangeRecordTrigger` | Triggered when a record is added or modified |
| `TimerTrigger` | Scheduled trigger |
| `ReminderTrigger` | Date reminder trigger |
| `LarkMessageTrigger` | Triggered by receiving a Lark message |

> All Trigger nodes have empty `children.links: []`; use `next` for serial successor.

### Trigger selection guide

| Requirement | Trigger |
|-------------|---------|
| Only when a new record is added | `AddRecordTrigger` |
| Only when a field changes to a specific value (modify only) | `SetRecordTrigger` |
| Both add and modify trigger | `ChangeRecordTrigger` |
| Unsure which to use | `ChangeRecordTrigger` |

> `SetRecordTrigger` listens for changes only. `ChangeRecordTrigger` monitors both new additions and modifications.

### Action types

| type | Description |
|------|-------------|
| `AddRecordAction` | Add a new record |
| `SetRecordAction` | Update a record |
| `FindRecordAction` | Find records |
| `Delay` | Delay |
| `LarkMessageAction` | Send a Lark message |
| `GenerateAiTextAction` | AI-generated text |

> All Action nodes have empty `children.links: []`; use `next` for serial successor.

### Branch types

| type | Description |
|------|-------------|
| `IfElseBranch` | Conditional branch; `children.links` contains `if_true` and `if_false` |
| `SwitchBranch` | Multi-way branch; `children.links` contains multiple `case` edges |

### System types

| type | Description |
|------|-------------|
| `Loop` | Loop; `children.links` contains a `loop_start` edge pointing to the loop body entry |

---

## Trigger data structures

### AddRecordTrigger

```json
{
  "table_name": "Order table",
  "watched_field_name": "status",
  "trigger_control_list": ["pasteUpdate", "automationBatchUpdate"],
  "condition_list": []
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `table_name` | Yes | Monitored table name |
| `watched_field_name` | Yes | Monitored field name |
| `trigger_control_list` | No | Trigger control; options: `pasteUpdate` / `automationBatchUpdate` / `syncUpdate` / `appendImport` / `openAPIBatchUpdate` |
| `condition_list` | No | Filter condition array; each element is an AndCondition; multiple AndConditions are OR-related |

### ChangeRecordTrigger

```json
{
  "table_name": "Task table",
  "trigger_control_list": [],
  "condition_list": null
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `table_name` | Yes | Monitored table name |
| `trigger_control_list` | No | Trigger control; options: `pasteUpdate` / `automationBatchUpdate` / `syncUpdate` / `appendImport` |
| `condition_list` | No | Filter condition array; each element is an AndCondition; multiple AndConditions are OR-related |

### SetRecordTrigger

```json
{
  "table_name": "Order table",
  "record_watch_conjunction": "and",
  "record_watch_info": [ /* FieldCondition[] */ ],
  "field_watch_info": [
    { "field_name": "status", "operator": "is", "value": [{ "value_type": "text", "value": "shipped" }] }
  ],
  "trigger_control_list": [],
  "condition_list": null
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `table_name` | Yes | Monitored table name |
| `record_watch_conjunction` | No | Record filter combination: `and` / `or`; default `and` |
| `record_watch_info` | No | Record-level filters (match pre-modification values); if empty, listens to all |
| `field_watch_info` | No | Field-level monitoring conditions list; at least one required |
| `trigger_control_list` | No | Trigger control; options: `pasteUpdate` / `automationBatchUpdate` / `syncUpdate` / `appendImport` |
| `condition_list` | No | Filter condition array |

`fieldWatchItem`:

| Field | Type | Description |
|-------|------|-------------|
| `field_name` | string | Monitored field name |
| `operator` | string | Operator (fill in only when field condition is explicitly required) |
| `value` | ValueInfo[] | Trigger value |

### TimerTrigger

```json
{
  "rule": "WEEKLY",
  "start_time": "2025-01-01 09:00",
  "sub_unit": [1, 3, 5],
  "is_never_end": true
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `rule` | Yes | `NO_REPEAT` / `DAILY` / `WEEKLY` / `MONTHLY` / `YEARLY` / `WORKDAY` / `CUSTOM` |
| `start_time` | No | Start time; format `yyyy-MM-dd HH:mm` |
| `interval` | No | Custom interval [1,30] (only for `CUSTOM`) |
| `unit` | No | Custom unit: `SECOND` / `MINUTE` / `HOUR` / `DAY` / `WEEK` / `MONTH` / `YEAR` |
| `sub_unit` | No | Sub-unit: for `WEEKLY` an array of weekday indices 0-6; for `MONTHLY` an array 1-31 |
| `end_time` | No | End time |
| `is_never_end` | No | Whether the trigger never ends |

### ReminderTrigger

```json
{
  "table_name": "Project table",
  "field_name": "Deadline",
  "offset": 1,
  "unit": "DAY",
  "hour": 9,
  "minute": 0,
  "condition_list": null
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `table_name` | Yes | Table name |
| `field_name` | Yes | Date field name (must be DateTime / CreatedTime / Formula / Lookup type) |
| `unit` | Yes | Offset unit: `MINUTE` / `HOUR` / `DAY` / `WEEK` / `MONTH` |
| `offset` | Yes | Advance/delay offset (positive = advance, negative = delay). Valid ranges: `MINUTE` ∈ {0,5,15,30,-5,-15,-30}; `HOUR` ∈ [-6,-1]∪[1,6]; `DAY` ∈ [-7,7]; `WEEK` ∈ [-7,-1]∪[1,7]; `MONTH` ∈ [-7,-1]∪[1,7] |
| `hour` | Yes | Trigger hour (0-23); default 9 |
| `minute` | Yes | Trigger minute (0-59); default 0 |
| `condition_list` | No | Filter condition array |

### LarkMessageTrigger

```json
{
  "receive_scene": "group",
  "receiver": [{ "value_type": "group", "value": "test group" }],
  "scope": "all",
  "filter": {
    "conjunction": "and",
    "content_contains": ["keywords"],
    "sender_contains": [{ "value_type": "user", "value": {"id": "ou_xxxx", "name": ""} }],
    "is_new_message": true,
    "is_message_contain_attachment": false
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `receive_scene` | Yes | Receive scene: `group` (group chat) / `chat` (private chat) |
| `receiver` | Yes | Trigger source; supports `user` / `group` / `ref` |
| `scope` | Yes | Trigger range: `at` (@mention) / `all` (all messages) |
| `filter` | Yes | MessageFilter conditions |

`MessageFilter`:

| Field | Type | Description |
|-------|------|-------------|
| `conjunction` | string | `and` (all conditions) / `or` (any condition) |
| `content_contains` | string[] | Keyword list |
| `sender_contains` | ValueInfo[] | Filter senders (effective in group chat + group source) |
| `is_new_message` | boolean | New topic messages only (group chat only) |
| `is_message_contain_attachment` | boolean | Trigger only for messages with attachments |

---

## Action data structures

### AddRecordAction

```json
{
  "table_name": "Order table",
  "field_values": [
    { "field_name": "Customer name", "value": [{ "value_type": "text", "value": "Zhang San" }] },
    { "field_name": "amount", "value": [{ "value_type": "number", "value": 100 }] },
    { "field_name": "Creator", "value": [{ "value_type": "ref", "value": "$.trigger_1.fieldIdxxx" }] }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `table_name` | Yes | Target table name |
| `field_values` | Yes | RecordFieldValue[] |

### SetRecordAction

```json
{
  "table_name": "Order table",
  "max_set_record_num": 10,
  "field_values": [
    { "field_name": "status", "value": [{ "value_type": "option", "value": { "id": "opt1", "name": "Completed" } }] }
  ],
  "filter_info": { /* RecordFilterInfo */ },
  "ref_info": { "step_id": "step_trigger" }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `table_name` | Yes | Target table name |
| `max_set_record_num` | No | Max records to update; default 100; range 1-15000 |
| `field_values` | Yes | RecordFieldValue[] |
| `filter_info` | No* | RecordFilterInfo filter conditions (mutually exclusive with `ref_info`) |
| `ref_info` | No* | RefInfo — reference records from a previous step (mutually exclusive with `filter_info`) |

### FindRecordAction

```json
{
  "table_name": "Customer table",
  "field_names": ["Customer Name", "Contact", "Level"],
  "should_proceed_when_no_results": true,
  "filter_info": { /* RecordFilterInfo */ }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `table_name` | Yes | Target table name |
| `field_names` | Yes | Field names to retrieve; at least one |
| `should_proceed_when_no_results` | No | Whether to continue to next step when no results found; default `true` |
| `filter_info` | No* | RecordFilterInfo (mutually exclusive with `ref_info`) |
| `ref_info` | No* | RefInfo (mutually exclusive with `filter_info`) |

### Delay

```json
{ "duration": 30 }
```

| Field | Required | Description |
|-------|----------|-------------|
| `duration` | Yes | Delay duration in minutes; range [1, 120] |

### LarkMessageAction

```json
{
  "receiver": [{ "value_type": "user", "value": "ou_xxxx" }],
  "send_to_everyone": false,
  "title": [{ "value_type": "text", "value": "New Order Notification" }],
  "content": [
    { "value_type": "text", "value": "Customer" },
    { "value_type": "ref", "value": "$.trigger_1.fieldIdxxx" },
    { "value_type": "text", "value": "New order created" }
  ],
  "btn_list": [
    { "text": "View details", "btn_action": "openLink", "link": [{ "value_type": "text", "value": "https://example.com" }] }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `receiver` | Yes | ValueInfo[] |
| `send_to_everyone` | Yes | Whether to send to everyone |
| `title` | No | TextRefItem[] message title |
| `content` | Yes | TextRefItem[] message content |
| `btn_list` | Yes | Button list; empty array when not needed |

`ButtonConfig`:

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Button label |
| `btn_action` | string | `addRecord` / `setRecord` / `openLink` |
| `link` | ValueInfo[] | Jump link (used with `openLink`) |
| `table_name` | string | Target table name (used with `addRecord`) |
| `record_values` | RecordFieldValue[] | Record assignment (used with `addRecord` / `setRecord`) |

### GenerateAiTextAction

```json
{
  "prompt": [
    { "value_type": "text", "value": "Please summarize the following:" },
    { "value_type": "ref", "value": "$.step_1.fieldxxx" }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `prompt` | Yes | TextRefItem[] prompt; supports `text` / `ref` |

---

## Branch data structures

### IfElseBranch

`children.links` contains `if_true` and `if_false` edges. `next` points to the successor node after both branches merge.

> For complex multi-branch scenarios (3 or more branches), use `SwitchBranch` instead of nested `IfElseBranch`.

```json
{
  "condition": {
    "conjunction": "or",
    "conditions": [
      {
        "conjunction": "and",
        "conditions": [
          {
            "left_value": { "value_type": "ref", "value": "$.step_1.fieldxxx" },
            "operator": "isGreater",
            "right_value": [{ "value_type": "number", "value": 1000 }]
          }
        ]
      }
    ]
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `condition` | Yes | OrGroup judgment condition; structure is `(A and B) or (C and D)` |

### SwitchBranch

`children.links` contains multiple `case` edges (use `branch_1`, `branch_2` for `label`; put semantics in `desc`).

```json
{
  "child_branch_list": [
    {
      "name": "High priority",
      "condition": {
        "conjunction": "or",
        "conditions": [
          {
            "conjunction": "and",
            "conditions": [
              {
                "left_value": { "value_type": "ref", "value": "$.step_1.fieldxxx" },
                "operator": "is",
                "right_value": [{ "value_type": "text", "value": "P0" }]
              }
            ]
          }
        ]
      }
    }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `child_branch_list` | Yes | BranchItem[]; 1-10 conditional branches |

`BranchItem`:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Branch name |
| `condition` | OrGroup | Branch condition |

---

## System data structures

### Loop

`children.links` contains a `loop_start` edge pointing to the loop body entry. `next` points to the successor node after the loop ends.

```json
{
  "loop_mode": "continue",
  "max_loop_times": 100,
  "data": [{ "value_type": "ref", "value": "$.find_record_stepIdxxx.records" }]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `data` | Yes | ValueInfo[] (only `ref` type); loop data source; only one entry allowed |
| `loop_mode` | No | On single-item error: `end` (stop) / `continue` (skip and continue) |
| `max_loop_times` | No | Maximum loop iterations |

---

## Common types

### ValueInfo

Base value type — distinguished by `value_type`:

| value_type | value type | Description | Example |
|------------|-----------|-------------|---------|
| `text` | string | Plain text | `"Zhang San"` |
| `number` | number | Number | `100` |
| `boolean` | boolean | Boolean | `true` |
| `date` | string | Date string or relative value | `"2025/01/01"`, `"now"`, `"today"`, `"yesterday"`, `"lastWeek"`, `"currentMonth"`, `"lastMonth"`, `"theLastWeek"`, `"theNextWeek"`, `"theLastMonth"`, `"theNextMonth"` |
| `option` | `{ id, name }` | Select option | `{ "id": "opt1", "name": "Completed" }` |
| `link` | `{ text, link }` | Hyperlink (text and URL each can be ValueInfo of text/ref type) | `{ "text": [{ "value_type": "text", "value": "View" }], "link": [{ "value_type": "text", "value": "https://example.com" }] }` |
| `user` | `{ id, name }` | User OpenID and name | `{ "id": "ou_xxxx", "name": "Zhang San" }` |
| `group` | `{ id, name }` | Group chat ID and name | `{ "id": "oc_xxx", "name": "Test group" }` |
| `ref` | string | Reference path to a preceding node's output | See ref variable reference section below |

> All user-related `value.id` must use OpenID (`ou_xxxx` format).
> All group-related `value.id` must use ChatID (`oc_xxxx` format).

### ref variable reference

`ref` type is the core data-passing mechanism between workflow nodes. When `value_type` is `ref`, `value` points to an output variable of a preceding node.

#### Reference path format

```
$.{stepId}
$.{stepId}.{pathId}
$.{stepId}.{pathId}.{childPathId}
$.{stepId}.{pathId}.{childPathId}.{grandChildPathId}
```

- `{stepId}`: the preceding node's `id` field
- `{pathId}`: the output path identifier from that node
- Multi-level drill-down is supported, e.g. referencing a field property: `$.step_1.fldXXX.name`

---

#### Trigger node output

##### Record triggers (AddRecordTrigger / ChangeRecordTrigger / SetRecordTrigger / ReminderTrigger)

All four triggers share the same output structure:

| pathId | Description | Reference example |
|--------|-------------|-------------------|
| `{fieldId}` | Field ID from the configured table; can drill down into field properties | `$.{stepId}.{fieldId}` |
| `{fieldId}.fieldId` | Field ID property | `$.{stepId}.{fieldId}.fieldId` |
| `{fieldId}.fieldName` | Field name attribute | `$.{stepId}.{fieldId}.fieldName` |
| `startTime` | Trigger timestamp | `$.{stepId}.startTime` |
| `recordId` | Record ID | `$.{stepId}.recordId` |
| `recordLink` | Record link | `$.{stepId}.recordLink` |
| `recordCreatedUser` | Record creator | `$.{stepId}.recordCreatedUser` |
| `recordCreatedTime` | Record creation time | `$.{stepId}.recordCreatedTime` |
| `recordModifiedUser` | Last modified by | `$.{stepId}.recordModifiedUser` |
| `recordModifiedTime` | Last modified time | `$.{stepId}.recordModifiedTime` |

**Dynamic field output rules:**
- Reads all fields from the table configured in the trigger
- Each field generates an output where `pathId` = fieldId
- For link fields, children of the related table are available (single level only, no recursion)
- Each field can drill down into specific field properties (see "Field attribute drill-down" below)

**`recordLink` children:** If the table is configured, all views of that table are listed as children: `{ pathId: viewId, pathName: viewName, pathtype: 'string' }`. Reference example: `$.{stepId}.recordLink.{viewId}`.

##### TimerTrigger (scheduled trigger)

| pathId | Description | Reference example |
|--------|-------------|-------------------|
| `scheduleTime` | Scheduled trigger time | `$.{stepId}.scheduleTime` |

##### LarkMessageTrigger (Lark message trigger)

| pathId | Description | Reference example |
|--------|-------------|-------------------|
| `Sender` | Message sender | `$.{stepId}.Sender` |
| `AtUser` | Users @mentioned in message | `$.{stepId}.AtUser` |
| `SenderGroup` | Group where message was sent (group chat only) | `$.{stepId}.SenderGroup` |
| `MessageSendTime` | Message send time | `$.{stepId}.MessageSendTime` |
| `MessageContent` | Message text | `$.{stepId}.MessageContent` |
| `Messagetype` | Message type identifier | `$.{stepId}.Messagetype` |
| `MessageID` | Message unique identifier | `$.{stepId}.MessageID` |
| `MessageLink` | Message link (group chat only) | `$.{stepId}.MessageLink` |
| `ParentID` | Reply message ID | `$.{stepId}.ParentID` |
| `ThreadID` | Thread message ID | `$.{stepId}.ThreadID` |
| `Attachments` | Attachments in message | `$.{stepId}.Attachments` |

Constraint: If scene is private chat (`receive_scene = "chat"`), then `SenderGroup` and `MessageLink` are not available.

---

#### Action node output

##### FindRecordAction (find records)

| pathId | Description | Reference example |
|--------|-------------|-------------------|
| `fieldRecords` | References to all found records (for Loop iteration) | Not directly quotable |
| `firstfieldsRecord` | First matching record | `$.{stepId}.firstfieldsRecord` |
| `firstfieldsRecord.{fieldId}` | First record's field value; can drill down | `$.{stepId}.firstfieldsRecord.{fieldId}` |
| `firstfieldsRecord.recordId` | First record's ID | `$.{stepId}.firstfieldsRecord.recordId` |
| `fields` | All found records' column values | Not directly quotable |
| `fields.{fieldId}` | User-selected field values (all records) | `$.{stepId}.fields.{fieldId}` |
| `fields.{fieldId}.fieldId` | User-selected field ID array | `$.{stepId}.fields.{fieldId}.fieldId` |
| `fields.{fieldId}.fieldName` | User-selected field name array | `$.{stepId}.fields.{fieldId}.fieldName` |
| `fields.recordId` | Record ID array | `$.{stepId}.fields.recordId` |
| `recordNum` | Total number of records found | `$.{stepId}.recordNum` |

##### AddRecordAction (add new record)

| pathId | Description | Reference example |
|--------|-------------|-------------------|
| `{fieldId}` | User-configured field value; can drill down | `$.{stepId}.{fieldId}` |
| `{fieldId}.fieldId` | User-configured field ID | `$.{stepId}.{fieldId}.fieldId` |
| `{fieldId}.fieldName` | User-configured field name | `$.{stepId}.{fieldId}.fieldName` |
| `recordId` | New record ID | `$.{stepId}.recordId` |
| `recordLink` | New record URL | `$.{stepId}.recordLink` |

##### SetRecordAction (update record)

| pathId | Description | Reference example |
|--------|-------------|-------------------|
| `{fieldId}` | User-configured field value; can drill down | `$.{stepId}.{fieldId}` |
| `{fieldId}.fieldId` | User-configured field ID | `$.{stepId}.{fieldId}.fieldId` |
| `{fieldId}.fieldName` | User-configured field name | `$.{stepId}.{fieldId}.fieldName` |
| `recordId` | Record ID array (multiple records may be updated) | `$.{stepId}.recordId` |

##### GenerateAiTextAction (AI-generated text)

| pathId | Description | Reference example |
|--------|-------------|-------------------|
| (whole output) | AI-generated text content (no drill-down; reference as `$.{stepId}`) | `$.{stepId}` |

##### Action nodes with no output

The following nodes produce no referenceable output:

- **Delay** (delay waiting)
- **LarkMessageAction** (send Lark message)

---

#### Branch node output

None of the branch nodes produce referenceable output:

- **IfElseBranch** (conditional branch)
- **SwitchBranch** (multi-way conditional branch)

---

#### System node output

##### Loop (loop)

| pathId | Description | Reference example |
|--------|-------------|-------------------|
| `item` | Current loop element | `$.{stepId}.item` |
| `index` | Loop index starting from 0 | `$.{stepId}.index` |

**`item` type inference rules** (determined by loop data source):

**Scenario 1: Traverse combined records** — data source is `record` type (e.g. `FindRecordAction.fieldRecords`); `item` type is `record`; can select specific fields:

| Description | Reference example |
|-------------|-------------------|
| Currently traversed record | `$.{loopStepId}.item` |
| Specific field on the record | `$.{loopStepId}.item.{fieldId}` |
| Index starting from 0 (number) | `$.{loopStepId}.index` |

**Scenario 2: Traverse a multi-value field** — data source is a multi-value field (e.g. attachment field, person field); `item` inherits the field's type and can drill down into field properties:

| Description | Reference example |
|-------------|-------------------|
| Currently traversed element (type inherits data source field type) | `$.{loopStepId}.item` |
| Person name | `$.{loopStepId}.item.name` |
| Index starting from 0 (number) | `$.{loopStepId}.index` |

---

#### Field attribute drill-down

All field variables can drill down further to select field properties. All fields support at least `fieldId` and `fieldName`; some support additional attributes:

| Field type | Property name | Property pathId | Property type | Description |
|-----------|--------------|----------------|---------------|-------------|
| **All fields (base)** | Field ID | `fieldId` | `string` | Field unique identifier |
| | Field name | `fieldName` | `string` | Field display name |
| **Person fields** (User / CreatedUser / ModifiedUser) | Name | `name` | `string` | User name |
| **Date fields** (DateTime / CreatedTime / ModifiedTime) | Timestamp | `timestamp` | `number` | Timestamp value |
| **Attachment fields** (Attachment) | File name | `fileName` | `string` | Attachment file name |
| | File type | `filetype` | `string` | MIME type |
| | File size | `size` | `number` | File bytes |
| | File token | `fileToken` | `string` | Attachment token |
| **Hyperlink fields** (URL) | Text | `text` | `string` | Link text portion |
| | Link | `link` | `string` | Link URL portion |
| **Auto-number fields** (AutoNumber) | Sequence | `sequence` | `number` | Numeric sequence number |
| **Link fields** (SingleLink / DuplexLink) | Field drill-down | `{fieldId}` | - | Can drill down into related table's fields |

> Other field types (text, number, checkbox, single/multi select, phone, location, date, formula, lookup, etc.) only support `fieldId` and `fieldName`.

Drill-down reference examples:

```
$.{stepId}.{fieldId}              → field value itself
$.{stepId}.{fieldId}.fieldId      → field ID (string)
$.{stepId}.{fieldId}.fieldName    → field name (string)
$.{stepId}.{fieldId}.name         → person name list (array<string>, person fields only)
$.{stepId}.{fieldId}.unionId      → person unionId list (array<string>, person fields only)
$.{stepId}.{fieldId}.timestamp    → timestamp (array<number>, date fields only)
$.{stepId}.{fieldId}.fileName     → list of file names (array<string>, attachment fields only)
$.{stepId}.{fieldId}.fileToken    → file token list (array<string>, attachment fields only)
```

---

#### Node output capability overview

| Node | Type | Has output | Output characteristics |
|------|------|-----------|----------------------|
| AddRecordTrigger | trigger | Yes | Dynamic (table fields + record properties) |
| ChangeRecordTrigger | trigger | Yes | Dynamic (table fields + record properties) |
| SetRecordTrigger | trigger | Yes | Dynamic (table fields + record properties) |
| ReminderTrigger | trigger | Yes | Dynamic (table fields + record properties) |
| TimerTrigger | trigger | Yes | Static (scheduleTime only) |
| LarkMessageTrigger | trigger | Yes | Static (message property list) |
| FindRecordAction | action | Yes | Dynamic (user-selected fields) |
| AddRecordAction | action | Yes | Dynamic (user-configured fields) |
| SetRecordAction | action | Yes | Dynamic (user-configured fields) |
| GenerateAiTextAction | action | Yes | Static (one string) |
| Delay | action | No | No output |
| LarkMessageAction | action | No | No output |
| IfElseBranch | branch | No | No output |
| SwitchBranch | branch | No | No output |
| Loop | system | Yes | Dynamic (depends on data source) |

---

### TextRefItem

Mixed text and references — used for dynamic content splicing (e.g. message content):

```json
[
  { "value_type": "text", "value": "Customer" },
  { "value_type": "ref", "value": "$.step_1.fieldxxx" },
  { "value_type": "text", "value": "New order created" }
]
```

### RecordFieldValue

```json
{ "field_name": "Customer name", "value": [{ "value_type": "text", "value": "Zhang San" }] }
```

### AndCondition (trigger filter conditions)

```json
{
  "conjunction": "and",
  "conditions": [
    { "field_name": "status", "operator": "is", "value": [{ "value_type": "text", "value": "in progress" }] }
  ]
}
```

### OrGroup (branch condition)

```json
{
  "conjunction": "or",
  "conditions": [
    {
      "conjunction": "and",
      "conditions": [
        {
          "left_value": { "value_type": "ref", "value": "$.step_1.fieldxxx" },
          "operator": "isGreater",
          "right_value": [{ "value_type": "number", "value": 1000 }]
        }
      ]
    }
  ]
}
```

**operator values:** `is` / `isNot` / `containsAny` / `doesNotContainAny` / `containsAll` / `isEmpty` / `isNotEmpty` / `isGreater` / `isGreaterEqual` / `isLess` / `isLessEqual`

### RecordFilterInfo

> `conjunction` only supports `and`. To match field X equal to A or B, use `containsAny`.

```json
{
  "conjunction": "and",
  "conditions": [
    { "field_name": "status", "operator": "is", "value": [{ "value_type": "text", "value": "in progress" }] }
  ]
}
```

### Select / MultiSelect field multi-value matching

| Operation | operator | Correct form |
|-----------|----------|--------------|
| Equal to single value | `is` | `[{"value_type": "option", "value": {"name": "L2"}}]` |
| Match multiple values (L2 or L3) | `containsAny` | `[{"value_type": "option", "value": {"name": "L2"}}, {"value_type": "option", "value": {"name": "L3"}}]` |

> Do not use multiple `is` conditions (they are treated as OR, cannot achieve AND). Use `containsAny` to match multiple values.

> For Select field conditions: `value_type` must be `option`; `value` object only needs `name` (e.g. `{"name": "L2"}`); option ID is not required.

### RefInfo

```json
{ "step_id": "step_trigger" }
```

---

## Full example: conditional branch + send message

```json
{
  "title": "Automatic notification of new orders",
  "steps": [
    {
      "id": "step_1",
      "type": "AddRecordTrigger",
      "title": "Triggered when a new record is added to the Order Table",
      "children": { "links": [] },
      "next": "step_2",
      "data": {
        "table_name": "Order table",
        "watched_field_name": "Order number"
      }
    },
    {
      "id": "step_2",
      "type": "IfElseBranch",
      "title": "Determine whether order amount is greater than 1000",
      "children": {
        "links": [
          { "kind": "if_true", "to": "step_3" },
          { "kind": "if_false", "to": "step_4" }
        ]
      },
      "next": "step_5",
      "data": {
        "condition": {
          "conjunction": "or",
          "conditions": [{
            "conjunction": "and",
            "conditions": [{
              "left_value": { "value_type": "ref", "value": "$.step_1.fieldxxx" },
              "operator": "isGreater",
              "right_value": [{ "value_type": "number", "value": 1000 }]
            }]
          }]
        }
      }
    },
    {
      "id": "step_3",
      "type": "LarkMessageAction",
      "title": "Notify supervisor to approve large orders",
      "children": { "links": [] },
      "next": null,
      "data": {
        "receiver": [{ "value_type": "ref", "value": "$.step_1.fieldxxx" }],
        "send_to_everyone": false,
        "title": [{ "value_type": "text", "value": "Large Order Reminder" }],
        "content": [
          { "value_type": "text", "value": "The new order amount is:" },
          { "value_type": "ref", "value": "$.step_1.fieldxxx" },
          { "value_type": "text", "value": "Yuan, please approve in time." }
        ],
        "btn_list": []
      }
    },
    {
      "id": "step_4",
      "type": "SetRecordAction",
      "title": "Automatically mark small orders as passed",
      "children": { "links": [] },
      "next": null,
      "data": {
        "table_name": "Order table",
        "ref_info": { "step_id": "step_1" },
        "field_values": [
          { "field_name": "Approval status", "value": [{ "value_type": "text", "value": "Passed" }] }
        ]
      }
    },
    {
      "id": "step_5",
      "type": "GenerateAiTextAction",
      "title": "AI generates order processing daily report",
      "children": { "links": [] },
      "next": null,
      "data": {
        "prompt": [
          { "value_type": "text", "value": "Please generate a brief processing daily report based on the following order information:" },
          { "value_type": "ref", "value": "$.step_1.fieldxxx" }
        ]
      }
    }
  ]
}
```

---

## References

- [lark-base-workflow-create.md](lark-base-workflow-create.md) — workflow-create operation
- [lark-base-workflow-update.md](lark-base-workflow-update.md) — workflow-update operation
- [lark-base-workflow-list.md](lark-base-workflow-list.md) — workflow-list operation
