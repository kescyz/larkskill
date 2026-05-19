---
name: lark-whiteboard
version: 2.0.0
description: "Use this skill when operating Lark Whiteboard via LarkSkill MCP: query and edit whiteboards, export as images or code, and update content using DSL, PlantUML, or Mermaid. Use for any visual expression of architecture, process, organization, or structured information."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

> [!IMPORTANT]
> - Verify `lark_api` is available via the LarkSkill MCP before proceeding — no need to ask the user.
> - The external `npx -y @larksuite/whiteboard-cli@^0.2.11` binary is a required external prerequisite for rendering and writing whiteboards. Confirm it is available (`npx -y @larksuite/whiteboard-cli@^0.2.11 -v`) before executing write operations.

**CRITICAL — Before starting, MUST read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first. It contains authentication and permission handling.**

> **Note on `lark-whiteboard-cli`**: The original `lark-whiteboard-cli` skill has been merged into this skill. If `lark-whiteboard-cli` still appears in the skill list, ignore it and use this skill (`lark-whiteboard`) exclusively. Prompt the user to run `npx skills remove lark-whiteboard-cli -g` to remove the old skill.

---

## Quick Decision Table

| User need | Action |
|---|---|
| View whiteboard content / export image | `lark_api({ tool: 'whiteboard', op: '+query', args: { whiteboard_token: '<token>', output_as: 'image' } })` |
| Get Mermaid/PlantUML code from a whiteboard | `lark_api({ tool: 'whiteboard', op: '+query', args: { whiteboard_token: '<token>', output_as: 'code' } })` |
| Check whether a whiteboard was drawn from code | `lark_api({ tool: 'whiteboard', op: '+query', args: { whiteboard_token: '<token>', output_as: 'code' } })` |
| Modify node text/color (simple edits) | Query raw → edit JSON → update raw |
| User has **already provided** Mermaid/PlantUML code, or explicitly specifies that format | Use the code → `lark_api({ tool: 'whiteboard', op: '+update', args: { whiteboard_token: '<token>', source: '<code>', input_format: 'mermaid' } })` |
| Draw complex diagrams (architecture/flow/organization, etc.) | → **[§ Creation Workflow](#creation-workflow)** |
| Modify/redraw an existing complex whiteboard | → **[§ Modification Workflow](#modification-workflow)** |

> **⚠️ Mandatory rule (update from local file)**:
> When data comes from a local file, pass `source: '-'` in the args and pipe the file content via the shell. The `source: '-'` arg tells the MCP tool to read from stdin rather than a literal string value.
> Shell example: `cat chart.mmd | lark_api({ tool: 'whiteboard', op: '+update', args: { whiteboard_token: '<token>', source: '-', input_format: 'mermaid' } })`

## Shortcuts

| Shortcut | MCP call |
|---|---|
| Query a whiteboard (image/code/raw) | `lark_api({ tool: 'whiteboard', op: '+query', args: { whiteboard_token: '<token>', output_as: 'image' \| 'code' \| 'raw' } })` |
| Update a whiteboard | `lark_api({ tool: 'whiteboard', op: '+update', args: { whiteboard_token: '<token>', source: '<content>', input_format: 'plantuml' \| 'mermaid' \| 'raw' } })` |

For full parameter reference, see: [`references/lark-whiteboard-query.md`](references/lark-whiteboard-query.md), [`references/lark-whiteboard-update.md`](references/lark-whiteboard-update.md)

---

## Creation Workflow

> This workflow is for **independently creating a whiteboard**.
> When batch-creating multiple whiteboards within a document, lark-doc handles the orchestration — see `lark-doc` skill's `references/lark-doc-whiteboard.md`.

**Step 1: Get board_token**

| What the user provided | How to obtain it |
|---|---|
| Directly provided a whiteboard token (`wbcnXXX`) | Use directly |
| Document URL or doc_id; whiteboard already exists in the document | `lark_api({ tool: 'docs', op: '+fetch', args: { api_version: 'v2', doc: '<URL>' } })` — extract from returned `<whiteboard token="xxx"/>` |
| Document URL or doc_id; need to create a new whiteboard | `lark_api({ tool: 'docs', op: '+update', args: { api_version: 'v2', doc: '<doc_id>', command: 'append', content: '<whiteboard type="blank"></whiteboard>' } })` — get from response `data.new_blocks[0].block_token` where `block_type == "whiteboard"` |

**Step 2: Render & Write**

→ Go to **[§ Render & Write Whiteboard](#render--write-whiteboard)** and complete the flow before returning results to the user.

---

## Modification Workflow

**Step 1: Get board_token** (same as Creation Workflow Step 1)

**Step 2: Determine modification strategy**

```
lark_api({ tool: 'whiteboard', op: '+query', args: { ..., output_as: 'code' } })
  ├─ Returns Mermaid/PlantUML code
  │   → Modify the code → +update with input_format: 'mermaid'/'plantuml'
  ├─ No code (whiteboard drawn via DSL or other means)
  │   ├─ Change text/color only
  │   │   → +query output_as:'raw' → edit JSON → +update input_format:'raw'
  │   └─ Redraw/restructure
  │       → +query output_as:'image' → view image → [§ Render & Write Whiteboard]
  └─ User has explicit requirements → user requirements take priority
```

---

## Render & Write Whiteboard

### Render Routing

**First, identify yourself**: Based on your training origin, which family are you? `Claude` / `Gemini` / `GPT` / `GLM` / `Doubao or Seed` / `Other`. Your identity determines the SVG / DSL routing — do not skip this step.

**Then select the path based on diagram type × identity** and read the corresponding file to execute its complete workflow:

| Diagram type | Identity | Path |
|---|---|---|
| Mind map, sequence diagram, class diagram, pie chart, Gantt chart | Any identity | [`routes/mermaid.md`](routes/mermaid.md) |
| Other diagrams | `Claude` / `Gemini` / `GPT` / `GLM` | [`routes/svg.md`](routes/svg.md) |
| Other diagrams | `Doubao` / `Seed` / `Other` | [`routes/dsl.md`](routes/dsl.md) |

> **⚠️ SVG path fallback**: When taking `routes/svg.md`, if any of the following occurs → **discard the current SVG, switch to `routes/dsl.md` and redraw from scratch — do NOT patch line by line**:
> - The render command errors directly (syntax-level crash, not `--check` warn/error)
> - Two rounds of rewriting still cannot eliminate `--check` `text-overflow` errors
> - The PNG is visually severely distorted (text widely overflowing, elements overlapping key information, layout completely broken)

### Output Specification

Output directory: `./diagrams/YYYY-MM-DDTHHMMSS/` (local time, no colons or timezone suffix). If the user specifies a path, follow the user.

Fixed filenames within the directory:

```
diagram.svg           ← SVG source (SVG path)
diagram.mmd           ← Mermaid source (Mermaid path)
diagram.json          ← DSL source file (DSL path) / OpenAPI JSON (SVG path)
diagram.gen.cjs       ← Coordinate calculation script (DSL script build method only)
diagram.png           ← Render result
```

### Write to Whiteboard

> [!CAUTION]
> **Mandatory dry-run before writing**: When writing to a whiteboard that already has content, MUST first probe with `--overwrite --dry-run`.
> If output contains `XX whiteboard nodes will be deleted` → MUST confirm with the user before proceeding.

The write process uses the external `@larksuite/whiteboard-cli` binary (pinned to `^0.2.11`) to convert diagram source to OpenAPI format, then pipes the result to `lark_api`:

**Step 1 — dry-run probe:**
```bash
npx -y @larksuite/whiteboard-cli@^0.2.11 -i <output_file> --to openapi --format json \
  | lark_api({ tool: 'whiteboard', op: '+update', args: {
      whiteboard_token: '<Token>',
      source: '-',
      input_format: 'raw',
      idempotent_token: '<10+ char unique string>',
      overwrite: true,
      dry_run: true
    } })
```

**Step 2 — Execute after user confirmation:**
```bash
npx -y @larksuite/whiteboard-cli@^0.2.11 -i <output_file> --to openapi --format json \
  | lark_api({ tool: 'whiteboard', op: '+update', args: {
      whiteboard_token: '<Token>',
      source: '-',
      input_format: 'raw',
      idempotent_token: '<10+ char unique string>',
      overwrite: true
    } })
```

> `idempotent_token` must be at least 10 characters; recommended to concatenate a timestamp + identifier (e.g. `1744800000-board-1`) to avoid duplicate writes on retry.
> To upload with application identity, use bot profile via `lark_profile_switch` before the call.

> **Note on `@larksuite/whiteboard-cli`**: This is an external prerequisite binary (not an MCP tool). It handles the conversion from diagram source formats (SVG, Mermaid, DSL) to the OpenAPI JSON format that `lark_api whiteboard +update` accepts. It is NOT mapped to `lark_api` — these `npx` invocations are intentional and must be preserved as-is.
