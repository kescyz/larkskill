---
name: lark-slides
version: 2.0.0
description: "Use this skill when operating Lark Slides via LarkSkill MCP: create and edit presentations via the XML protocol. Create presentations, read slide content, manage slide pages (create, delete, read, partial replace). Use when the user needs to create or edit slides, read or modify individual pages."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# slides (v1)

## Quick Reference

| User intent | Recommended action | Key docs / commands |
|---|---|---|
| Create a new presentation | Plan `slide_plan.json` first, then choose one-step or two-step creation based on complexity | `planning-layer.md`, `visual-planning.md`, `asset-planning.md`, `lark_api({ tool: 'slides', op: 'create', ... })` |
| Major rewrite of pages | Read existing XML first, write a new plan, then replace or rebuild relevant pages | `lark_api({ tool: 'slides', op: 'xml_presentations.get', ... })`, `lark_api({ tool: 'slides', op: 'replace-slide', ... })`, `lark-slides-edit-workflows.md` |
| Edit a single title, text block, image, or partial element | Prefer block-level replace/insert; do not change page order | `lark_api({ tool: 'slides', op: 'replace-slide', ... })`, `lark-slides-replace-slide.md` |
| Read or analyze an existing presentation | Parse slides/wiki token, read full or single-page XML, save `xml_presentation_id`, `slide_id`, `revision_id` | `lark_api({ tool: 'slides', op: 'xml_presentations.get', ... })` |
| Upload or use an image | Upload first to get `file_token`; MUST NOT write http(s) external links directly | `lark_api({ tool: 'slides', op: 'media-upload', ... })` |
| User mentions template, theme, or layout | Search for a template first, then summarize; extract skeleton only if needed | `template_tool.py search → summarize → extract` |
| Create failure, blank page, 3350001, layout issue | Read current state first, then fix per troubleshooting checklist; do not assume the original op succeeded atomically | `troubleshooting.md`, `validation-checklist.md` |

**CRITICAL — Before starting, MUST use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling.**

**CRITICAL — Before generating any XML, MUST use the Read tool to read [xml-schema-quick-ref.md](references/xml-schema-quick-ref.md). DO NOT guess XML structure from memory.**

**CRITICAL — When creating a new presentation or performing a major rewrite, MUST first generate `.lark-slides/plan/<deck-or-task-id>/slide_plan.json` before generating any XML. Create the corresponding directory first; planning-layer rules and intermediate artifact lifecycle are in [planning-layer.md](references/planning-layer.md). Minor edits to existing pages (e.g. replacing a single title or inserting one block) are exempt.**

**CRITICAL — When creating a new presentation or performing a major rewrite, MUST read [visual-planning.md](references/visual-planning.md) before generating XML. Ensure `layout_type`, `visual_focus`, and `text_density` actually change the page geometry, primary visual, and text density.**

**CRITICAL — When creating a new presentation or performing a major rewrite, planning `asset_need` MUST follow [asset-planning.md](references/asset-planning.md): metadata planning only; MUST include `fallback_if_missing`; MUST NOT require real searches, downloads, or uploads of assets.**

**CRITICAL — After creating or performing a major rewrite, MUST perform explicit validation per [validation-checklist.md](references/validation-checklist.md): read full XML, verify page count and key elements, check for blank/broken pages, obvious overflow, and layout risks. Prioritize static XML syntax and text-overlap checks using [`scripts/xml_text_overlap_lint.py`](scripts/xml_text_overlap_lint.py).**

**CRITICAL — Before creation or during failure troubleshooting, MUST check [troubleshooting.md](references/troubleshooting.md) for XML escaping, structure, shell truncation, image token, 3350001, and layout risks.**

**CRITICAL — If the user mentions "template", "apply a template", "reference a theme/style/layout", or the user's request clearly maps to an existing scenario template (e.g. work report, product intro, business plan, training, promotion report), MUST first use [`scripts/template_tool.py`](scripts/template_tool.py) `search` to find templates; by default, provide 2-3 best-matching template candidates for the user to choose from. Once a template is selected, use `summarize` to get theme and layout summary; only use `extract` to cut the target page-type XML skeleton when needed. DO NOT read the complete template XML directly.**

> [!NOTE]
> `scripts/template_tool.py` requires Python 3. `references/template-index.json` is the script cache/lightweight routing index — not a document for the agent to read by default. `assets/templates/*.xml` are machine resources; access only via script summary or extraction, never read full content.

**CRITICAL — When using a template to generate or rewrite pages, MUST `summarize` the target page type first; only `extract` when a specific layout skeleton is needed.**

**Editing existing slide pages**: prefer `lark_api({ tool: 'slides', op: 'replace-slide', ... })` (block-level replace/insert, without changing page order). For action selection and the full read-modify-write workflow, see [`lark-slides-edit-workflows.md`](references/lark-slides-edit-workflows.md).

## Identity Selection

Lark Slides content typically belongs to the user's own resources. **Default to explicitly using user identity for all slides operations.**

- **User identity (recommended)**: create, read, and manage presentations as the logged-in user. Complete user authorization first via the LarkSkill MCP auth flow:

```
lark_auth_login({ domain: 'slides' })
```

Then `lark_auth_poll` to wait for authorization, and confirm via `lark_whoami` / `lark_auth_status`.

- **Bot identity**: only when the user explicitly requests app identity, or when the workflow requires bot-owned resources. When using bot identity, additionally confirm that the bot actually has access to the target presentation. Switch via `lark_profile_switch`.

**Execution rules**:

1. Create, read, add/remove slides, and continue editing an existing presentation from a user-supplied link — default to user identity first.
2. If a permission error occurs, first check whether bot identity was mistakenly used; do not default to falling back to bot.
3. Only switch to bot identity when the user explicitly requests "use app/bot identity", or when the current workflow is bot-creating resources followed by collaborative authorization.

## Before Execution

> **Important**: `references/slides_xml_schema_definition.xml` is the sole authoritative XML protocol source for this skill; other `.md` files are summaries of it and the MCP tool schema.

High-frequency read-only references:

- [xml-schema-quick-ref.md](references/xml-schema-quick-ref.md)
- [planning-layer.md](references/planning-layer.md) (new creation / major rewrite)
- [visual-planning.md](references/visual-planning.md) (new creation / major rewrite)
- [asset-planning.md](references/asset-planning.md) (new creation / major rewrite)
- [validation-checklist.md](references/validation-checklist.md) (after creation / major rewrite)

Read on demand:

- Create: [`lark-slides-create.md`](references/lark-slides-create.md)
- Edit: [`lark-slides-edit-workflows.md`](references/lark-slides-edit-workflows.md), [`lark-slides-replace-slide.md`](references/lark-slides-replace-slide.md)
- Images: [`lark-slides-media-upload.md`](references/lark-slides-media-upload.md)
- Templates: [`template-catalog.md`](references/template-catalog.md), [`scripts/template_tool.py`](scripts/template_tool.py)
- Troubleshooting: [`troubleshooting.md`](references/troubleshooting.md)
- Full protocol: [`slides_xml_schema_definition.xml`](references/slides_xml_schema_definition.xml)

## Workflow

> **This is a presentation, not a document.** Each slide is an independent visual frame — keep information density low and leave visual breathing room.

### Design Ideas

Do not produce slides with no design sensibility. Pure white background + title + bullets is only acceptable as a minimal draft — not a final deliverable.

Before writing XML, determine the deck-level visual strategy in `slide_plan.json`:

- **Thematic color scheme**: colors must serve the theme, industry, and audience — do not default to corporate blue. If the same color palette still works when applied to a completely different theme, it is not specific enough.
- **Hierarchy**: choose 1 primary color carrying approximately 60-70% visual weight, 1-2 supporting colors for structure and sections, and 1 accent color used only for key numbers, conclusions, or action points. Do not give every color equal weight.
- **Background consistency**: determine the full-deck background strategy first; maintain the same light/dark tone and base color system by default. Only change the background intentionally for section breaks, transitions, or emphasis pages — and unify the change visually via shared primary color, texture, sidebar, or motif. Regardless of light or dark, ensure sufficient contrast for body text, icons, and lines.
- **Unified motif**: choose one reusable visual motif that runs throughout the deck — e.g. thick side bars, circular icon bases, half-bleed image areas, numbered nodes, card-corner color blocks, or large numbers. Do not switch visual language on every page.

Every page must have at least one visual element: an image, icon, chart, table, process flow, comparison structure, large number, diagram, or abstract shape. Text boxes alone do not count as primary visuals.

Preferred page layouts:

- **Two-column**: text on one side, image on the other; visual area occupies 35-45% of the width.
- **Icon row**: icon in a color block or circle, with short heading and one-sentence description to the right.
- **2×2 / 2×3 grid**: suited for capabilities, modules, risks, or action items; maintain equal hierarchy within each cell.
- **Half-bleed visual**: image or abstract shape occupies left/right half of the screen; text overlays or aligns to the edge.
- **Large number card**: key metrics with 60-72pt numbers; 10-14pt label below.
- **Comparison column**: before/after, Plan A/B, problem/solution in left-right columns; align headings and baselines strictly.
- **Timeline/flowchart**: steps expressed via nodes and arrows; flow direction must be immediately clear.

Typography and spacing guidelines:

- Headings 36-44pt; key conclusions may be larger. Body 14-18pt; notes 10-12pt.
- Body text left-aligned by default; center-align only for cover pages, closing pages, or large-number scenarios.
- Page margin at least 40px; 24-40px between content blocks, consistent throughout the deck.
- Card padding must leave real breathing room — do not let text touch the edge. Account for text box padding when aligning shapes and text.

Common mistakes to avoid:

- Do not reuse the same heading + three bullets layout on every page.
- Do not use low-contrast text or icons (e.g. light gray text on a light background).
- Do not let decorative lines pass through text, or let footers, sources, and numbering crowd the main content.
- Do not represent missing assets as empty image placeholders — use `fallback_if_missing` to generate XML-native visuals.
- Do not leave template placeholder text, sample company names, sample dates, or template content unrelated to the user's topic.

### Creation Method Selection

| Scenario | Recommended approach |
|---|---|
| Simple XML (1-3 pages, simple structure, few special characters) | `lark_api({ tool: 'slides', op: 'create', args: { slides: [...] } })` — create in one step |
| Complex XML (multiple pages, large text blocks, complex layout, nested quotes, many special characters) | **Two-step creation**: first `lark_api({ tool: 'slides', op: 'create', args: {} })` to create a blank presentation, then add pages one by one via `xml_presentation.slide.create` (see below) |
| Appending or inserting pages into an existing presentation | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.create', args: { xml_presentation_id: '...', slides: [...] } })` |
| Reading the content of a specific page | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.get', args: { xml_presentation_id: '...', slide_id: '...' } })` |
| Deleting a page | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.delete', args: { xml_presentation_id: '...', slide_id: '...' } })` |
| Replacing a single page's content | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.replace', args: { xml_presentation_id: '...', slide_id: '...', xml: '...' } })` |

> [!WARNING]
> The risk of one-step creation primarily lies in argument size, not just page count. Even with only 1 page, if the XML is complex enough, consider breaking the content into fewer, denser slides.

> [!IMPORTANT]
> One-step `slides create` with a slides array creates pages sequentially — it is NOT an atomic operation. If it fails mid-way, record the `xml_presentation_id`, read back via `lark_api({ tool: 'slides', op: 'xml_presentations.get', ... })` to confirm current state, then use `lark_api({ tool: 'slides', op: 'replace-slide', ... })` to fix or extend.

### Template and Script Priority Flow

Template details are in [template-catalog.md](references/template-catalog.md). For the main flow: `search` first, then `summarize` after selecting a template; only `extract` when a layout skeleton is needed. Do not read complete template XML or copy placeholder text verbatim.

```bash
python3 skills/lark-slides/scripts/template_tool.py search --query "<user request verbatim>" --limit 3
python3 skills/lark-slides/scripts/template_tool.py summarize --template <template-id> --label <cover|toc|section|content|closing>
python3 skills/lark-slides/scripts/template_tool.py extract --template <template-id> --label <page-type> --out /tmp/template-slice.xml
```

```text
Step 1: Clarify requirements & read knowledge
  - Clarify theme, audience, page count, style; handle template needs via "Template and Script Priority Flow"
  - Read xml-schema-quick-ref.md; for new creation / major rewrite, also read planning-layer.md, visual-planning.md, asset-planning.md

Step 2: Generate outline → user confirmation → write slide_plan.json
  - Generate structured outline for user confirmation; if using a template, note which template it is based on
  - New creation / major rewrite: MUST create the directory and write `.lark-slides/plan/<deck-or-task-id>/slide_plan.json` first
  - Plan fields, path naming, template boundaries, and `asset_need` structure follow planning-layer.md / asset-planning.md

Step 3: Generate XML per slide_plan.json → create
  - Consume plan page by page: key_message drives the main conclusion, layout_type drives geometry, visual_focus drives primary visual, text_density drives text amount
  - For missing real assets, MUST generate XML-native fallback visuals using `fallback_if_missing`; do not leave blank
  - Creation method follows "Creation Method Selection"; images, complex XML, escaping, and 3350001 troubleshooting follow lark-slides-create.md, media-upload.md, troubleshooting.md

Step 4: Review & deliver
  - After creation, MUST use lark_api({ tool: 'slides', op: 'xml_presentations.get', args: { xml_presentation_id: '...' } }) to read full XML and perform explicit validation per validation-checklist.md, including XML text-overlap check
  - Handle failures or partial successes per troubleshooting.md; for partial issues, use lark_api({ tool: 'slides', op: 'replace-slide', ... })
  - No issues → deliver: inform the user of the presentation ID and access method
```

### Outline Template

Use the following format when generating an outline for user confirmation:

```text
[Presentation title] — [positioning description], for [target audience]

Template: [no template used / <category>/<template>.xml (reason for recommendation)]

Page structure (N pages):
1. Cover: [title text]
2. [Page topic]: [point 1], [point 2], [point 3]
3. [Page topic]: [description]
...
N. Closing: [closing text]

Style: [color scheme], [layout style]
```

## Core Concepts

### URL Format and Token

| URL format | Example | Token type | Handling |
|---|---|---|---|
| `/slides/` | `https://example.larkoffice.com/slides/xxxxxxxxxxxxx` | `xml_presentation_id` | Token in URL path is used directly as `xml_presentation_id` |
| `/wiki/` | `https://example.larkoffice.com/wiki/wikcnxxxxxxxxx` | `wiki_token` | ⚠️ **Cannot be used directly** — must query first to get the real `obj_token` |

> `replace-slide` and `media-upload` MCP operations auto-parse both URL types above. When reading full XML via `xml_presentations.get` directly, wiki links must still be resolved manually.

### Wiki Link Special Handling (Important!)

Wiki links (`/wiki/TOKEN`) cannot be used directly as `xml_presentation_id`. Before calling `xml_presentations.get` directly, query the wiki node, confirm `node.obj_type == "slides"`, then use `node.obj_token` as the real presentation ID.

```
lark_api({ tool: 'wiki', op: 'spaces.get_node', args: { token: 'wiki_token' } })
```

The `replace-slide` and `media-upload` operations auto-resolve `/wiki/` URLs. Manual resolution is only needed when calling `xml_presentations.get` directly.

### Resource Relationships

```text
Wiki Space
└── Wiki Node (obj_type: slides)
    └── obj_token → xml_presentation_id

Slides (presentation)
├── xml_presentation_id (unique presentation identifier)
├── revision_id (version number)
└── Slide (page)
    └── slide_id (unique page identifier)
```

## MCP Operations

Use the LarkSkill MCP tool for all slides operations. The catalog provides exactly these 4 slides operations:

| Operation | MCP call | Description |
|---|---|---|
| Create presentation | `lark_api({ tool: 'slides', op: 'create', args: { slides: [...] } })` | Create a presentation; optionally pass a slides array to add all pages in one call; supports `<img src="@./local.png">` placeholder for auto-upload |
| Upload image | `lark_api({ tool: 'slides', op: 'media-upload', args: { xml_presentation_id: '...', file: '...' } })` | Upload a local image; returns `file_token` (used as `<img src="...">`); max 20 MB |
| Block-level edit | `lark_api({ tool: 'slides', op: 'replace-slide', args: { ... } })` | Block-level replace/insert on existing slide pages (`block_replace` / `block_insert`); auto-injects id and `<content/>`; does not change page order |
| Read full presentation | `lark_api({ tool: 'slides', op: 'xml_presentations.get', args: { xml_presentation_id: '...' } })` | Read full presentation XML |

Use `lark_api_search` to discover the exact args shape for any operation before invoking it — do not guess field structures.

## Core Rules

1. **Plan before writing XML**: when creating a new presentation or performing a major rewrite, MUST write `.lark-slides/plan/<deck-or-task-id>/slide_plan.json` first. Templates, styles, and outlines may only serve as planning inputs — they cannot bypass the planning layer.
2. **Creation flow**: use `lark_api({ tool: 'slides', op: 'create', args: { slides: [...] } })` with the full slides array for both simple and complex presentations. For page-level edits to existing presentations, use `replace-slide`.
3. **`<slide>` direct children are only `<style>`, `<data>`, `<note>`**: text and graphics MUST be placed inside `<data>`.
4. **Text expressed via `<content>`**: MUST use `<content><p>...</p></content>`; do not write text directly inside a shape.
5. **Save key IDs**: subsequent operations require `xml_presentation_id`, `slide_id`, `revision_id`.
6. **Be cautious with deletions**: the MCP catalog does not include a slide-delete op; do not attempt to delete individual slides via MCP.
7. **Prefer block-level replace for editing existing pages**: to modify a single shape or image, use `replace-slide` (`block_replace` / `block_insert`); do not attempt full page rebuild via native slide ops — they are not in the MCP catalog.
8. **`<img src>` may only use `file_token` uploaded to Lark Drive; http(s) external link URLs are FORBIDDEN**: the Lark Slides renderer does not proxy external images — external links typically display as broken or invisible. The flow MUST be: save the image locally → upload via `slides media-upload` or the `@./path` placeholder in one-step create → use the returned `file_token` in `<img src>`. If the user provides a web image link, download it to the CWD first, then follow the upload flow. Do NOT paste external URLs directly into `src`. **Maximum image size: 20 MB**.

## Permissions Quick Reference

| Operation | Required scope |
|---|---|
| `slides create` | `slides:presentation:create`, `slides:presentation:write_only` (also `docs:document.media:upload` when `@` placeholders are used) |
| `slides media-upload` | `docs:document.media:upload` (wiki URL resolution also requires `wiki:node:read`) |
| `slides replace-slide` | `slides:presentation:update` (wiki URL resolution also requires `wiki:node:read`) |
| `slides xml_presentations.get` | `slides:presentation:read` |

> **Note**: if content in the `.md` files conflicts with `slides_xml_schema_definition.xml` or `lark_api_search` output for a slides operation, the latter two take precedence.
