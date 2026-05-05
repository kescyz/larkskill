---
name: lark-okr
version: 2.0.0
description: "Use this skill when managing Lark OKR objectives and key results via LarkSkill MCP. Covers OKR cycles, objectives, key results, alignments, quantitative indicators, and progress records."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api"]
---

# okr (v2)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first — it covers authentication and permission handling.

## Shortcuts (use these first)

Shortcuts are high-level wrappers for common operations (`lark_api({ tool: 'okr', op: '<verb>', args: {...} })`). Prefer shortcuts when available.

| Shortcut | Description |
|----------|-------------|
| [`+cycle-list`](references/lark-okr-cycle-list.md) | List OKR cycles for a specific user, optionally filtered by time range |
| [`+cycle-detail`](references/lark-okr-cycle-detail.md) | Retrieve all objectives and key results within a specific OKR cycle |
| [`+progress-list`](references/lark-okr-progress-list.md) | List all progress records for an objective or key result |
| [`+progress-get`](references/lark-okr-progress-get.md) | Get a single OKR progress record by ID |
| [`+progress-create`](references/lark-okr-progress-create.md) | Create a progress record for an objective or key result |
| [`+progress-update`](references/lark-okr-progress-update.md) | Update the content of a progress record by ID |
| [`+progress-delete`](references/lark-okr-progress-delete.md) | Delete a progress record by ID (irreversible) |
| [`+upload-image`](references/lark-okr-image-upload.md) | Upload an image for use in OKR progress rich-text content |

### Shortcut examples

```
// List OKR cycles for a user
lark_api({ tool: 'okr', op: 'cycle-list', args: { user_id: '<user_id>' } })

// Get all objectives and key results in a cycle
lark_api({ tool: 'okr', op: 'cycle-detail', args: { cycle_id: '<cycle_id>' } })

// Create a progress record
lark_api({ tool: 'okr', op: 'progress-create', args: { entity_id: '<okr_id>', entity_type: 'objective', content: { ... } } })

// Update a progress record
lark_api({ tool: 'okr', op: 'progress-update', args: { progress_id: '<id>', content: { ... } } })

// Delete a progress record
lark_api({ tool: 'okr', op: 'progress-delete', args: { progress_id: '<id>' } })
```

## Format references

- [`OKR Business Entities`](references/lark-okr-entities.md) — OKR entity structures, definitions, and relationships; read this before operating on OKRs
- [`ContentBlock rich-text format`](references/lark-okr-contentblock.md) — rich-text format used by the `Content` / `Note` fields in Objectives, Key Results, and Progress records
- **Strongly recommended:** Read [`OKR Business Entities`](references/lark-okr-entities.md) before performing any OKR operation.

## API Resources

For raw API calls (use only when no shortcut covers the operation):

> **Important:** Before using any raw API, inspect the request schema to understand `data` / `params` field structure — do not guess field formats.

### alignments

- `delete` — Delete an alignment relationship
- `get` — Get an alignment relationship

### categories

- `list` — Batch-retrieve categories

### cycles

- `list` — Batch-retrieve user cycles

- `objectives_position` — Update the position of all objectives in a user cycle (no shortcut op; use raw HTTP form)
  - The request MUST include position updates for ALL objectives in the cycle simultaneously; overlapping positions are not allowed and will fail parameter validation.

- `objectives_weight` — Update the weight of all objectives in a user cycle (no shortcut op; use raw HTTP form)
  - The request MUST include weight updates for ALL objectives in the cycle simultaneously; all weight values MUST sum to 1, otherwise parameter validation fails.

### cycle.objectives

- `create` — Create an objective
- `list` — Batch-retrieve objectives in a user cycle

### indicators

- `patch` — Update a quantitative indicator

### key_results

- `delete` — Delete a key result
- `get` — Get a key result
- `patch` — Update a key result

### key_result.indicators

- `list` — Get quantitative indicators for a key result (no shortcut op; use raw HTTP form)

### objectives

- `delete` — Delete an objective
- `get` — Get an objective

- `key_results_position` — Update the position of all key results under an objective (no shortcut op; use raw HTTP form)
  - The request MUST include position updates for ALL key results under the objective simultaneously; overlapping positions are not allowed and will fail parameter validation.

- `key_results_weight` — Update the weight of all key results under an objective (no shortcut op; use raw HTTP form)
  - The request MUST include weight updates for ALL key results simultaneously; all weight values MUST sum to 1, otherwise parameter validation fails.

- `patch` — Update an objective

### objective.alignments

- `create` — Create an alignment relationship
  - Aligning an objective to itself is not allowed. The source and target objectives MUST belong to cycles whose time ranges overlap; otherwise parameter validation fails.
- `list` — Batch-retrieve alignment relationships under an objective

### objective.indicators

- `list` — Get quantitative indicators for an objective

### objective.key_results

- `create` — Create a key result under an objective (no shortcut op; use raw HTTP form)

- `list` — Batch-retrieve key results under an objective (no shortcut op; use raw HTTP form)

## Permission table

| Method | Required scope |
|--------|----------------|
| `alignments.delete` | `okr:okr.content:writeonly` |
| `alignments.get` | `okr:okr.content:readonly` |
| `categories.list` | `okr:okr.setting:read` |
| `cycles.list` | `okr:okr.period:readonly` |
| `cycles.objectives_position` | `okr:okr.content:writeonly` |
| `cycles.objectives_weight` | `okr:okr.content:writeonly` |
| `cycle.objectives.create` | `okr:okr.content:writeonly` |
| `cycle.objectives.list` | `okr:okr.content:readonly` |
| `indicators.patch` | `okr:okr.content:writeonly` |
| `key_results.delete` | `okr:okr.content:writeonly` |
| `key_results.get` | `okr:okr.content:readonly` |
| `key_results.patch` | `okr:okr.content:writeonly` |
| `key_result.indicators.list` | `okr:okr.content:readonly` |
| `objectives.delete` | `okr:okr.content:writeonly` |
| `objectives.get` | `okr:okr.content:readonly` |
| `objectives.key_results_position` | `okr:okr.content:writeonly` |
| `objectives.key_results_weight` | `okr:okr.content:writeonly` |
| `objectives.patch` | `okr:okr.content:writeonly` |
| `objective.alignments.create` | `okr:okr.content:writeonly` |
| `objective.alignments.list` | `okr:okr.content:readonly` |
| `objective.indicators.list` | `okr:okr.content:readonly` |
| `objective.key_results.create` | `okr:okr.content:writeonly` |
| `objective.key_results.list` | `okr:okr.content:readonly` |
