---
name: lark-whiteboard
version: 2.0.0
description: "Use this skill when operating Lark Whiteboard via LarkSkill MCP: query and edit whiteboards in Lark Docs, export preview images or raw nodes, and update content via Mermaid, PlantUML, or DSL. Also use it for visualizing architecture, flow, org charts, timelines, causality, or comparisons."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

> [!IMPORTANT]
> **Environment check before execution**:
> - This skill renders diagrams locally via the standalone `@larksuite/whiteboard-cli` package, then writes the result to Lark via the LarkSkill MCP. Run `whiteboard-cli --version` and confirm version `0.2.x`; if not installed or version mismatched → `npm install -g @larksuite/whiteboard-cli@^0.2.0`.
> - Confirm the LarkSkill MCP server is connected (install via `/plugin marketplace add kescyz/larkskill` → `/plugin install larkskill`, or see https://portal.larkskill.app/setup).
> - Before running any `npm install`, **you MUST get user consent**.

**CRITICAL — Before starting, you MUST first use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which contains authentication and permission handling.**

---

## Quick decisions

| User need | Action |
|---|---|
| View whiteboard content / export image | [`whiteboard +query` with `output_as: image`](references/lark-whiteboard-query.md) |
| Get the Mermaid/PlantUML code of a whiteboard | [`whiteboard +query` with `output_as: code`](references/lark-whiteboard-query.md) |
| Check whether a whiteboard is drawn from code | [`whiteboard +query` with `output_as: code`](references/lark-whiteboard-query.md) |
| Modify node text/color (simple change) | `whiteboard +query` with `output_as: raw` → manually edit JSON → `whiteboard +update` with `input_format: raw` |
| User **already provided** Mermaid/PlantUML code, or explicitly specifies that format | Generate/use the code yourself → [`whiteboard +update` with `input_format: mermaid` / `plantuml`](references/lark-whiteboard-update.md) |
| Draw a complex diagram (architecture/flow/org chart, etc.) | → **[§ Authoring Workflow](#authoring-workflow)** |
| Modify/redraw an existing complex whiteboard | → **[§ Modification Workflow](#modification-workflow)** |

> **⚠️ Mandatory rule (updating via stdin)**:
> When data comes from a local file, you **MUST** stream it through `source: '-'` with the matching `input_format`. Pipe the file content into the MCP call.
> Example: read `chart.mmd` locally, then call:
>
> ```
> lark_api({
>   tool: 'whiteboard',
>   op: 'update',
>   args: {
>     whiteboard_token: '<token>',
>     source: '-',
>     input_format: 'mermaid',
>     stdin: '<contents of chart.mmd>',
>     as: 'user'
>   }
> })
> ```

## Shortcuts

| Shortcut | Description |
|---|---|
| [`whiteboard +query`](references/lark-whiteboard-query.md) | Query a whiteboard, export as preview image, code, or raw node structure |
| [`whiteboard +update`](references/lark-whiteboard-update.md) | Update a whiteboard, supports PlantUML, Mermaid, or OpenAPI native format |

Example query call:

```
lark_api({
  tool: 'whiteboard',
  op: 'query',
  args: {
    whiteboard_token: '<token>',
    output_as: 'image',  // or 'code' / 'raw'
    as: 'user'
  }
})
```

---

## Authoring Workflow

> This workflow is for **independently authoring a single whiteboard**.
> When you need to bulk-create multiple whiteboards inside a document, lark-doc orchestrates the flow — see `references/lark-doc-whiteboard.md` in the lark-doc skill.

**Step 1: Obtain board_token**

| What the user gave you | How to obtain it |
|---|---|
| Whiteboard token directly (`wbcnXXX`) | Use it directly |
| Document URL or doc_id, document already contains a whiteboard | `lark_api({ tool: 'docs', op: 'fetch', args: { doc: '<URL>', as: 'user' } })`, extract from the returned `<whiteboard token="xxx"/>` |
| Document URL or doc_id, need to create a new whiteboard | `lark_api({ tool: 'docs', op: 'update', args: { doc: '<doc_id>', mode: 'append', markdown: '<whiteboard type="blank"></whiteboard>', as: 'user' } })`, take from response `data.board_tokens[0]` (see lark-doc SKILL.md for parameter details) |

**Step 2: Render & write**

→ Enter the **[§ Render & write to whiteboard](#render--write-to-whiteboard)** section, follow the flow, and return the result to the user when done.

---

## Modification Workflow

**Step 1: Obtain board_token** (same as Authoring Workflow Step 1)

**Step 2: Decide modification strategy**

```
whiteboard +query (output_as: code)
  ├─ Returns Mermaid/PlantUML code
  │   → Edit on top of the original code → whiteboard +update (input_format: mermaid/plantuml)
  ├─ No code returned (whiteboard drawn via DSL or other means)
  │   ├─ Only changing text/color → whiteboard +query (output_as: raw) → manually edit JSON → whiteboard +update (input_format: raw)
  │   └─ Redraw / structural change → whiteboard +query (output_as: image) → review the image, then enter [§ Render & write to whiteboard]
  └─ User has explicit requirements → user requirements take precedence
```

---

## Render & write to whiteboard

### Render routing

**First, self-identify**: by your training origin, which family do you belong to? `Claude` / `Gemini` / `GPT` / `GLM` / `Doubao or Seed` / `Other`. Identity decides the SVG / DSL split (different families have uneven capability between these two expression languages). Do not skip this step.

**Then pick the path by diagram type × identity**, read the corresponding file, and execute its full workflow (including reading the scene guide, generating content, render review, and delivery):

| Diagram type | Identity | Path |
|---|---|---|
| Mind map, sequence diagram, class diagram, pie chart, Gantt chart | Any identity | [`routes/mermaid.md`](routes/mermaid.md) |
| Other diagrams | `Claude` / `Gemini` / `GPT` / `GLM` | [`routes/svg.md`](routes/svg.md) |
| Other diagrams | `Doubao` / `Seed` / `Other` | [`routes/dsl.md`](routes/dsl.md) |

> **⚠️ SVG path failure fallback**: when on `routes/svg.md`, if any of the following occur → **discard the current SVG and switch to `routes/dsl.md` to redraw from scratch — do NOT patch line-by-line**:
> - Render command errors out directly (syntax-level crash, not a `--check` warn/error)
> - After two rewrite rounds the `text-overflow` error from `--check` still cannot be eliminated
> - Visual inspection of the PNG shows severe layout corruption (large-scale text overflow, elements overlapping and covering critical info, overall layout collapsed)
>
> Patching SVG source often introduces new bugs; switching to DSL and redrawing from scratch is usually more stable. This is the hard fallback for the SVG free-form path — do NOT intrude into the `routes/svg.md` authoring flow.

### Output artifact spec

Output directory: `./diagrams/YYYY-MM-DDTHHMMSS/` (local time, no colons, no timezone suffix). If the user specifies a path, follow the user.

Fixed file names inside the directory:

```
diagram.svg           ← SVG source (SVG path)
diagram.mmd           ← Mermaid source (Mermaid path)
diagram.json          ← DSL source file (DSL path) / OpenAPI JSON (SVG path exports from diagram.svg)
diagram.gen.cjs       ← Coordinate-calculation script (DSL script-build mode only)
diagram.png           ← Render result
```

### Write to whiteboard

> [!CAUTION]
> **Mandatory dry-run before write**: when writing to a whiteboard that already has content, you MUST first probe with `overwrite: true` and `dry_run: true`.
> If output contains `XX whiteboard nodes will be deleted` → you MUST confirm with the user before executing.

```
# Step 1: render the artifact to OpenAPI JSON locally
npx -y @larksuite/whiteboard-cli@^0.2.0 -i <artifact-file> --to openapi --format json
# (capture the resulting JSON; pass it as the stdin payload below)

# Step 2: dry-run probe via LarkSkill MCP
lark_api({
  tool: 'whiteboard',
  op: 'update',
  args: {
    whiteboard_token: '<Token>',
    source: '-',
    input_format: 'raw',
    idempotent_token: '<10+-char unique string>',
    overwrite: true,
    dry_run: true,
    as: 'user',
    stdin: '<OpenAPI JSON from Step 1>'
  }
})

# Step 3: execute after confirmation (drop dry_run)
lark_api({
  tool: 'whiteboard',
  op: 'update',
  args: {
    whiteboard_token: '<Token>',
    source: '-',
    input_format: 'raw',
    idempotent_token: '<10+-char unique string>',
    overwrite: true,
    as: 'user',
    stdin: '<OpenAPI JSON from Step 1>'
  }
})
```

> `idempotent_token` requires at least 10 characters; recommend concatenating timestamp + identifier (e.g. `1744800000-board-1`) to avoid duplicate writes on retry.
> If you need to upload as the application identity, replace `as: 'user'` with `as: 'bot'`.
