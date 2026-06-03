---
name: lark-whiteboard
version: 1.0.0
description: >
  Lark Whiteboard: query and edit whiteboards in Lark Docs via LarkSkill MCP. Supports exporting whiteboards as preview images, exporting raw node structure, updating whiteboard content using DSL (converted to OpenAPI format), PlantUML/Mermaid formats.
  Use this skill when the user needs to view whiteboard content, export whiteboard images, edit a whiteboard, or needs to visually express architecture, workflows, org charts, timelines, causal diagrams, comparisons, or other structured information — regardless of whether "whiteboard" is explicitly mentioned.
  ⚠️ The former `lark-whiteboard-cli` skill has been merged into this skill. If `lark-whiteboard-cli` appears in the skill list alongside this one, ignore it and use this skill (`lark-whiteboard`) exclusively. Prompt the user to run `npx skills remove lark-whiteboard-cli -g` to remove the old skill.
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

> [!IMPORTANT]
> - Call `lark_whoami` to confirm the LarkSkill MCP tool is available — do not ask the user.
> - Run `npx -y @larksuite/whiteboard-cli@^0.2.11 -v` to confirm it is available — do not ask the user.

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling.**

---

## Quick Decision

| User need | Action |
|---|---|
| View whiteboard content / export image | [`op: 'query', args: { output_as: 'image' }`](references/lark-whiteboard-query.md) |
| Get Mermaid/PlantUML code for a whiteboard | [`op: 'query', args: { output_as: 'code' }`](references/lark-whiteboard-query.md) |
| Check whether a whiteboard was drawn from code | [`op: 'query', args: { output_as: 'code' }`](references/lark-whiteboard-query.md) |
| Modify node text/color (minor edits) | `op: 'query', args: { output_as: 'raw' }` → edit JSON manually → `op: 'update', args: { input_format: 'raw' }` |
| User **has already provided** Mermaid/PlantUML code, or explicitly requests that format | Generate/use the code → [`op: 'update', args: { input_format: 'mermaid/plantuml' }`](references/lark-whiteboard-update.md) |
| Draw a complex diagram (architecture/workflow/org chart, etc.) | → **[§ Creation Workflow](#creation-workflow)** |
| Modify/redraw an existing complex whiteboard | → **[§ Edit Workflow](#edit-workflow)** |

## Shortcuts

| Shortcut | Description |
|---|---|
| [`+query`](references/lark-whiteboard-query.md) | Query a whiteboard; export as preview image, code, or raw node structure |
| [`+update`](references/lark-whiteboard-update.md) | Update a whiteboard; supports PlantUML, Mermaid, or native OpenAPI format |

---

## Creation Workflow

> This workflow is for **independently creating a whiteboard**.
> When batch-creating multiple whiteboards inside a document, lark-doc handles orchestration — see `lark-doc`'s `references/lark-doc-whiteboard.md`.

**Step 1: Obtain board_token**

| What the user provided | How to obtain it |
|---|---|
| A whiteboard token directly (`wbcnXXX`) | Use it directly |
| A document URL or doc_id where a whiteboard already exists | `lark_api({ tool: 'docs', op: 'fetch', args: { api_version: 'v2', doc: '<URL>', as: 'user' } })`, then extract from the returned `<whiteboard token="xxx"/>` |
| A document URL or doc_id where a new whiteboard must be created | `lark_api({ tool: 'docs', op: 'update', args: { api_version: 'v2', doc: '<doc_id>', command: 'append', content: '<whiteboard type="blank"></whiteboard>', as: 'user' } })`, then take the token from `data.new_blocks[0].block_token` (the entry where `block_type == "whiteboard"`; see lark-doc SKILL.md for parameter details) |

**Step 2: Render & write**

→ Proceed to **[§ Render & Write Whiteboard](#render--write-whiteboard)**, complete the steps there, then return the result directly to the user.

---

## Edit Workflow

**Step 1: Obtain board_token** (same as Creation Workflow Step 1)

**Step 2: Determine edit strategy**

```
lark_api({ tool: 'whiteboard', op: 'query', args: { output_as: 'code' } })
  ├─ Returns Mermaid/PlantUML code
  │   → Edit the existing code → lark_api({ tool: 'whiteboard', op: 'update', args: { input_format: 'mermaid/plantuml' } })
  ├─ No code (whiteboard drawn via DSL or another method)
  │   ├─ Only changing text/color → lark_api({ tool: 'whiteboard', op: 'query', args: { output_as: 'raw' } }) → edit JSON manually → lark_api({ tool: 'whiteboard', op: 'update', args: { input_format: 'raw' } })
  │   └─ Redraw/restructure → lark_api({ tool: 'whiteboard', op: 'query', args: { output_as: 'image' } }) → inspect image → proceed to [§ Render & Write Whiteboard]
  └─ User has explicit requirements → user requirements take priority
```

---

## Render & Write Whiteboard

### Render routing

**First, identify yourself**: Based on your training origin, which family do you belong to? `Claude` / `Gemini` / `GPT` / `GLM` / `Doubao or Seed` / `Other`. Your identity determines the SVG / DSL routing (different model families have uneven capability across these two representation languages). Do not skip this step.

**Then, select the path based on diagram type × identity**, read the corresponding file and follow its complete workflow (including reading the scene guide, generating content, render review, and delivery):

| Diagram type | Identity | Path |
|---|---|---|
| Mind map, flowchart, sequence diagram, class diagram, pie chart, Gantt chart | Any identity | [`routes/mermaid.md`](routes/mermaid.md) |
| Other diagram types | `Claude` / `Gemini` / `GPT` / `GLM` | [`routes/svg.md`](routes/svg.md) |
| Other diagram types | `Doubao` / `Seed` / `Other` | [`routes/dsl.md`](routes/dsl.md) |

> **⚠️ SVG path fallback**: When following `routes/svg.md`, if any of the following occur → **discard the current SVG and switch to `routes/dsl.md` to redraw from scratch — do not patch line by line**:
> - The render command errors out directly (syntax-level crash, not a `--check` warn/error)
> - Two rounds of rewriting still cannot eliminate `--check` `text-overflow` errors
> - The PNG is visually severely broken on inspection (text widely overflowing, elements overlapping and covering key content, overall layout collapse)
>
> Patching SVG source frequently introduces new bugs; redrawing from scratch with DSL is usually more stable. This is the hard fallback for the SVG path's free-form rendering — do not intrude on the creative flow in `routes/svg.md`.

### Output artifact specification

Artifact directory: `./diagrams/YYYY-MM-DDTHHMMSS/` (local time, no colons or timezone suffix). If the user specifies a path, use the user's path.

Fixed filenames inside the directory:

```
diagram.svg           ← SVG source (SVG path)
diagram.mmd           ← Mermaid source (Mermaid path)
diagram.json          ← DSL source file (DSL path) / OpenAPI JSON (SVG path, exported from diagram.svg)
diagram.gen.cjs       ← Coordinate calculation script (DSL script-build method only)
diagram.png           ← Render result
```

### Write to whiteboard

> Regarding overwrite
> The whiteboard update operation without `overwrite: true` performs an incremental update. If the whiteboard already has content, the new content may overlap with existing content and cause issues.
> Therefore, when performing a full replacement of whiteboard content, pass `overwrite: true` for an overwrite-style update.

**Step 1 — Convert the artifact to OpenAPI JSON (local converter, shell):**

```bash
npx -y @larksuite/whiteboard-cli@^0.2.11 -i <artifact-file> --to openapi --format json > diagram.openapi.json
```

**Step 2 — Write the converted JSON to the whiteboard (MCP):**

```
lark_api({ tool: 'whiteboard', op: 'update', args: { whiteboard_token: '<Token>', source: '<contents of diagram.openapi.json>', input_format: 'raw', idempotent_token: '<10+-char unique string>', as: 'user', overwrite: true } })
```

> Read `diagram.openapi.json` and pass its contents as the `source` arg value (do not use the stdin sentinel `-`).
> `idempotent_token` must be at minimum 10 characters; recommended to construct by concatenating a timestamp with an identifier (e.g. `1744800000-board-1`) to avoid duplicate writes on retry.
> To upload using bot identity, replace `as: 'user'` with `as: 'bot'`.
