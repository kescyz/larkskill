---
name: lark-whiteboard
version: 2.0.0
description: "Use this skill when users are asked to draw diagrams in Feishu Cloud documents, or use Feishu Sketchpad to draw architecture diagrams, flow charts, mind maps, sequence diagrams or other visual diagrams via LarkSkill MCP."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# Whiteboard Skill

> [!NOTE]
> **Environment dependencies**: Drawing the artboard requires `@larksuite/whiteboard-cli` (the artboard Node.js CLI tool).
> If the execution fails, try again after manual installation: `npm install -g @larksuite/whiteboard-cli@^0.1.0`

> [!IMPORTANT]
> Before executing `npm install` to install new dependencies, be sure to obtain user consent!

> **Prerequisite:** Read [../lark-shared/SKILL.md](../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

## Workflow

> **This is an artboard, not a web page. ** The artboard is an infinite canvas for freely placing elements, and flex layout is an optional enhancement.

```
Step 1: Routing & reading knowledge
  - Determine rendering path (see routing table): Mermaid or DSL?
  - Read corresponding scene guides — understand structural features and layout strategies
  - Determine layout strategy (see quick judgment below) and construction method
  - Read references/ core modules - syntax, layout, color matching, typesetting, wiring

Step 2: Generate complete DSL (including color)
  - Plan information volume and grouping by content.md
  - Press layout.md to select layout mode and spacing
  - Color according to style.md (the default classic color palette is used when the user does not specify it)
  - Output complete JSON according to schema.md syntax
  - Refer to connectors.md for wiring and typography.md for layout.

  Note: For some graphics (fishbone/flywheel/column/polyline, etc.), you need to write a .js script according to the script template of the scene guide to generate JSON:
    - node xxx.js → Output JSON file
    - Use the output JSON file to enter Step 3

Step 3: Render & Review → Deliver
  - Self-check before rendering (see checklist below)
  - Render PNG, check:
    · Is the information complete? Is the layout reasonable? Color coordination?
    · No text truncation? No cross-connections?
  - Problematic → Fix by symptom table → Re-render (max 2 rounds)
  - Still having serious problems after 2 rounds → Consider taking the Mermaid route to find out.
  - No problem → Delivery:
    · The user requests to upload Feishu → See the instructions in the "Uploading Feishu Drawing Board" section below
    · Not specified by user → Show PNG image to user
```

**Quick judgment of layout strategy** (see layout.md for details):

| Judgment conditions | Layout strategy | Construction method |
|----------|----------|----------|
| There are clear upper and lower levels (user layer → service layer → data layer) | Flex layering | Write JSON directly |
| Spatial location carries information (geography, topology, angle) | Pure absolute positioning | Write script to calculate coordinates (node ​​xxx.js) |
| Multiple independent modules are interconnected horizontally | Hybrid (island style) | Directly write JSON + estimation assistance |
| Unsure | Default Flex (safest) | Write JSON directly |

> **The construction method is a strong constraint**: When the scene guide requires "script generation", you must first write a script (.js) and execute it with `node` to produce a JSON file. The coordinates of absolute positioning scenes (fishbone diagrams, flywheel diagrams, histograms, line diagrams, etc.) require mathematical calculations, and directly handwriting JSON can easily lead to overlapping nodes or cross-moulding.

---

## Rendering path selection (DSL or Mermaid)

| Chart Type | Path | Reason |
|----------|------|------|
| Mind map | **Mermaid** | Radial structure automatic layout |
| Sequence diagram | **Mermaid** | Automatic arrangement of participants + messages |
| Class diagram | **Mermaid** | Class relationship automatic layout |
| Pie chart | **Mermaid** | Mermaid native support |
| Flowchart | **Mermaid** | Stable structure generation through Mermaid syntax |
| All other types | **DSL** | Precise control over style and layout |

**Routing Rules**:
1. **Automatic Mermaid**: mind map, sequence diagram, class diagram, pie chart, flow chart → default to Mermaid
2. **Explicit Mermaid**: User input contains Mermaid syntax → Go Mermaid
3. **DSL path**: all other types → Read the core module first, then read the corresponding scenario guide

**Mermaid path**: Refer to `scenes/mermaid.md` to write the `.mmd` file and skip the DSL module.
**DSL Path**: Follow Workflow 3 steps.

---

## Module index

### Core Reference (required reading for DSL paths)

| Module | File | Description |
|------|------|------|
| DSL syntax | `references/schema.md` | Node types, attributes, size values ​​|
| Content planning | `references/content.md` | Information extraction, density decision-making, connection prediction |
| Layout system | `references/layout.md` | Grid methodology, Flex mapping, spacing rules |
| Typesetting rules | `references/typography.md` | Font size level, alignment, line spacing |
| Connection system | `references/connectors.md` | Topology planning, anchor point selection |
| Color matching system | `references/style.md` | Multi-color palette, visual hierarchy |


### Scenario guide (select one by type)

| Chart type | File | Applicable scenarios |
|----------|------|----------|
| Architecture diagram | `scenes/architecture.md` | Layered architecture, microservice architecture |
| Organization chart | `scenes/organization.md` | Company organization, tree hierarchy |
| Comparison chart | `scenes/comparison.md` | Scheme comparison, function matrix |
| Fishbone diagram | `scenes/fishbone.md` | Cause and effect analysis, root cause analysis |
| Histogram | `scenes/bar-chart.md` | Histogram, bar chart |
| Line chart | `scenes/line-chart.md` | Line chart, trend chart |
| Treemap | `scenes/treemap.md` | Rectangular treemap, level proportions |
| Funnel chart | `scenes/funnel.md` | Conversion funnel, sales funnel |
| Pyramid diagram | `scenes/pyramid.md` | Hierarchical structure, hierarchy of needs |
| Loop/flywheel diagram | `scenes/flywheel.md` | Growing flywheel, closed-loop link |
| Milestone | `scenes/milestone.md` | Timeline, version evolution |
| Mermaid | `scenes/mermaid.md` | Mind maps, sequence diagrams, class diagrams, pie charts, flow charts |

---

## Rendering commands

**Rendering** (uses local `@larksuite/whiteboard-cli` npm tool — not MCP):
```bash
npx -y @larksuite/whiteboard-cli@^0.1.0 -i my-diagram.json -o ./images/my-diagram.png # DSL path
npx -y @larksuite/whiteboard-cli@^0.1.0 -i diagram.mmd -o ./images/diagram.png # Mermaid path
npx -y @larksuite/whiteboard-cli@^0.1.0 -i skeleton.json -o ./images/step1.png -l coords.json # Two stages (extracting coordinates)
```

---

## Uploading to Feishu Drawing Board

> Feishu authentication is required for uploading. When encountering authentication or permission errors, read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) to learn about login and permission handling.

**Step one: Obtain the drawing board token**

| What the user gave | How to obtain Token |
|------------|--------------|
| Sketchboard Token (`XXX`) | Use directly |
| Document URL or doc_id, there is an artboard in the document | Call `lark_api GET /open-apis/docx/v1/documents/{document_id}/blocks` to find the whiteboard block and extract `token` |
| Document URL or doc_id, you need to create a new artboard | Call `lark_api PATCH /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}` to append a whiteboard block, then extract `board_token` from the response |

For more information on creating, reading, and reading Feishu documents, please refer to lark-doc skill [`../lark-doc/SKILL.md`](../lark-doc/SKILL.md).

**Step 2: Convert DSL to Whiteboard API format**

Convert the local DSL JSON to the whiteboard node format using the CLI tool, then upload via MCP:

```bash
# Convert DSL to API format (outputs JSON to stdout)
npx -y @larksuite/whiteboard-cli@^0.1.0 --to openapi -i <input file> --format json
```

**Step 3: Check existing nodes (pre-flight)**

> [!CAUTION]
> **MANDATORY PRE-FLIGHT CHECK (mandatory interception check before uploading)**
> When you want to write content to an **existing artboard Token**, you **must** first check if the artboard is empty.

Check if the whiteboard has existing nodes:

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/board/v1/whiteboards/{whiteboard_id}/nodes
- as: user
```

**Parse the results and intercept**:
- If the response contains existing nodes: the artboard is **not empty** — the current operation will overwrite and destroy the user's original chart!
- **You must stop the operation immediately** and confirm to the user: "The target artboard is currently not empty. Continuing the update will clear the original nodes. Are you sure to overwrite?"
- Only proceed with the upload if the user explicitly authorizes "agree to override".

**Step 4: Upload whiteboard nodes via MCP**

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/board/v1/whiteboards/{whiteboard_id}/nodes
- body: <converted node JSON from CLI output>
- as: user
```

> Once uploaded, the artboard cannot be modified. To apply bot identity, use `as: bot` instead.

**Symptom → Fix Table** (refer to when visual inspection reveals problems):

| Problems seen | What to change |
|-----------|--------|
| Text is truncated | height changed to fit-content |
| The text overflows the right side of the container | Increase the width, or shorten the text |
| Nodes overlap and stick together | Increase gap |
| Nodes are crowded together | Increase padding and gap |
| Connect lines through nodes | Adjust fromAnchor/toAnchor or increase the spacing |
| Large blank area | Reduce outer frame width |
| The text and background colors are too close | Adjust fillColor or textColor |
| The overall layout is left/right | Adjust the x coordinate of absolute positioning to center the content |

---

## Self-check before rendering

After generating the DSL and before rendering, a quick check:

- [ ] Different colors are used for different groups? Are the styles of nodes in the same group exactly the same?
- [ ] Light colored background on the outer layer and white nodes on the inner layer? (Heavy on the outside and light on the inside)
- [ ] All nodes have borders (borderWidth=2)? Is the text legible against the background?
- [ ] Use gray (#BBBFC4) for connections, not color?
- [ ] frame has layout attribute written? Are both gap and padding explicitly set?
- [ ] contains text node height. Use fit-content? connector in the top level nodes array?

---

## Quick check on key constraints

> The most frequently errored rules must be followed even if submodule files are not read.

1. **The height of nodes containing text must use `'fit-content'`** - hard-coding the value will truncate the text
2. **`fill-container` only takes effect in the flex parent container** — the width degenerates to 0 under `layout: 'none'`
3. **connector must be placed in the top-level nodes array** — cannot be nested in frame children
4. **Layer Order** — Array Order = Draw Order. The higher the level of elements defined later, they will overwrite those defined earlier. Overlapping/floating/label elements must be placed at the end of the array.
5. **x/y in the flex container will be completely ignored** — use `layout: 'none'` or place it on top-level nodes when free positioning is required

❌ Fatal error: The flex container is set to x/y, the coordinates do not take effect, and the nodes are arranged in order
```json
{ "type": "frame", "layout": "vertical", "children": [
  { "type": "rect", "x": 100, "y": 0, "text": "Chengdu" },
  { "type": "rect", "x": 540, "y": 0, "text": "Kangding" }
]}
```
✅ Correct: Use `layout: "none"` or put it on top nodes and use x/y positioning.
