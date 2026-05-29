---
name: lark-slides
version: 2.0.0
description: "Use this skill when operating Lark Slides via LarkSkill MCP: create and edit presentations via the XML protocol; read content; manage pages (create, delete, read, partial replace). Also handles doubao.com /slides/ URLs/tokens directly — route by path+token, not domain; no WebFetch fallback."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api", "lark_api_search"]
---

# slides (v1)

## Quick Reference

| User need | Preferred action | Key docs / commands |
|----------|----------|-----------------|
| Create a new presentation | Plan `slide_plan.json` first, then choose one-step or two-step creation based on complexity | `planning-layer.md`, `visual-planning.md`, `asset-planning.md`, `lark_api({ tool: 'slides', op: 'create', ... })` |
| Major page rewrite | Read back existing XML first, write a new plan, then replace or rebuild the relevant pages | `lark_api({ tool: 'slides', op: 'xml_presentations.get', ... })`, `lark_api({ tool: 'slides', op: 'replace-slide', ... })`, `lark-slides-edit-workflows.md` |
| Edit a single title, text block, image, or partial element | Prefer block-level replace/insert; do not change page order | `lark_api({ tool: 'slides', op: 'replace-slide', ... })`, `lark-slides-replace-slide.md` |
| Read or analyze an existing presentation | Parse slides/wiki token, read back full or single-page XML, save `xml_presentation_id`, `slide_id`, `revision_id` | `lark_api({ tool: 'slides', op: 'xml_presentations.get', ... })`, `lark_api({ tool: 'slides', op: 'xml_presentation.slide.get', ... })` |
| Upload or use an image | Upload first to get a `file_token`; DO NOT write http(s) external links directly | `lark_api({ tool: 'slides', op: 'media-upload', ... })`, or the `@./path` placeholder of `op: 'create'` with `slides` |
| User mentions template, theme, or layout | Search templates first, then summarize, and extract a skeleton only when needed | `template_tool.py search → summarize → extract` |
| Create failure, blank page, 3350001, layout anomaly | Read back state first, then fix per the troubleshooting checklist; do not assume the original op succeeded atomically | `troubleshooting.md`, `validation-checklist.md` |

**CRITICAL — Before starting, MUST first use the Read tool to read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md), which covers authentication and permission handling.**

**CRITICAL — Before generating any XML, MUST first use the Read tool to read [xml-schema-quick-ref.md](references/xml-schema-quick-ref.md). DO NOT guess the XML structure from memory.**

**CRITICAL — When creating a new presentation or performing a major page rewrite, MUST first generate `.lark-slides/plan/<deck-or-task-id>/slide_plan.json` before generating XML. Create the corresponding directory first; planning-layer rules and the intermediate artifact lifecycle are in [planning-layer.md](references/planning-layer.md). Minor edits to existing pages — such as replacing a single title or inserting one block — are exempt.**

**CRITICAL — When creating a new presentation or performing a major page rewrite, MUST read [visual-planning.md](references/visual-planning.md) before generating XML, to ensure `layout_type`, `visual_focus`, and `text_density` actually change the page geometry, primary visual, and text density.**

**CRITICAL — When creating a new presentation or performing a major page rewrite, planning `asset_need` MUST follow [asset-planning.md](references/asset-planning.md): metadata planning only, MUST include `fallback_if_missing`, and MUST NOT require real searches, downloads, or uploads of assets.**

**CRITICAL — After creation or a major rewrite, MUST perform explicit validation per [validation-checklist.md](references/validation-checklist.md): read back the full XML, verify page count and key elements, check for blank/broken pages, obvious overflow, and layout risks. Prefer [`scripts/xml_text_overlap_lint.py`](scripts/xml_text_overlap_lint.py) for static XML syntax and text-overlap checks.**

**CRITICAL — During pre-creation self-check or failure troubleshooting, MUST check [troubleshooting.md](references/troubleshooting.md) for XML escaping, structure, shell truncation, image token, 3350001, and layout risks.**

**CRITICAL — If the user mentions "template", "apply a template", "reference a theme/style/layout", or the user's need clearly falls within an existing scenario template (e.g. work report, product intro, business plan, training, promotion report), MUST first use the `search` of [`scripts/template_tool.py`](scripts/template_tool.py) to search templates; by default, offer 2-3 best-matching template candidates for the user to choose from. Once a template is locked, use `summarize` to get the theme and layout summary; only use `extract` to cut the target page-type XML when a layout skeleton is needed. Do not read the complete template XML directly.**

> [!NOTE]
> `scripts/template_tool.py` requires Python 3. `references/template-index.json` is a script cache / lightweight routing index — not a document for the agent to read by default; `assets/templates/*.xml` are machine resources and should only be summarized or sliced via the script, not read in full.

**CRITICAL — When using a template to generate or rewrite pages, MUST `summarize` the target page type first; only `extract` when a specific layout skeleton is needed.**

**Editing existing slide pages**: prefer `lark_api({ tool: 'slides', op: 'replace-slide', ... })` (block-level replace/insert, without changing page order); for action selection and the full read-modify-write flow, see [`lark-slides-edit-workflows.md`](references/lark-slides-edit-workflows.md).

## Identity Selection

Lark Slides are usually the user's own content resources. **By default, prefer explicitly using user identity for slides operations, and always specify the identity explicitly.**

- **User identity (recommended)**: create, read, and manage presentations as the currently logged-in user. Complete user authorization first via the LarkSkill MCP auth flow:

```
lark_auth_login({ domain: 'slides' })
```

Then `lark_auth_poll` to wait for authorization, and confirm via `lark_whoami` / `lark_auth_status`.

- **Bot identity**: only when the user explicitly requests app identity, or the workflow requires the bot to hold/create resources. When using bot identity, additionally confirm whether the bot actually has access to the target presentation. Switch via `lark_profile_switch`.

**Execution rules**:

1. Create, read, add/remove slides, and continue editing an existing presentation from a user-supplied link — default to user identity first.
2. If a permission error occurs, first check whether bot identity was mistakenly used; do not default to falling back to bot.
3. Only switch to bot identity when the user explicitly requests "use app / bot identity", or when the current workflow is bot-creates-resource then grants collaborative authorization.

## Before Execution

> **Important**: `references/slides_xml_schema_definition.xml` is the sole authoritative XML protocol source for this skill; the other `.md` files are only summaries of it and of the MCP tool schema.

High-frequency read-only:

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

> **This is a presentation, not a document.** Each slide is an independent visual frame — keep information density low and leave whitespace in the layout.

### Design Ideas

Do not produce slides with no design sense. Pure white background + title + bullets is acceptable only as a minimal temporary draft, not as a final deliverable.

Before writing XML, determine the deck-level visual strategy in `slide_plan.json`:

- **Thematic color scheme**: colors must serve this theme, industry, and audience — do not default to corporate blue. If the same palette would still hold up when swapped onto a completely different theme, it is not specific enough.
- **Primary/secondary ratio**: choose 1 primary color carrying about 60-70% of the visual weight, 1-2 supporting colors for structure and zoning, and 1 accent color used only for key numbers, conclusions, or action points. Do not give all colors equal weight.
- **Background consistency**: determine the whole-deck background strategy first; by default keep the same light/dark tone and base color system. Only deliberately change the background for section breaks, transitions, or emphasis pages, and you MUST make the change look like part of the same design via the same primary color, texture, sidebar, or motif. Whether light or dark, ensure sufficient contrast for body text, icons, and lines.
- **Unified motif**: choose one reusable visual motif that runs throughout, e.g. a thick sidebar, circular icon bases, half-bleed image areas, numbered nodes, card-corner color blocks, or large numbers. Do not switch the decorative language on every page.

Every page must have at least one visual element: an image, icon, chart, table, process flow, comparison structure, large number, diagram, or an abstract visual composed of shapes. A text box itself does not count as a primary visual.

Preferred page forms to consider:

- **Two-column structure**: text-left/image-right or image-left/text-right, with the visual area at 35-45% width.
- **Icon row**: icon in a color block or circle, with a short heading and a one-sentence explanation to the right.
- **2x2 / 2x3 grid**: suited to capabilities, modules, risks, action items, with each cell at the same level.
- **Half-bleed visual**: an image or abstract shape occupying the left/right half of the screen, with text overlaid or aligned to the edge.
- **Large-number card**: key metrics in 60-72pt numbers, with a 10-14pt label below.
- **Comparison columns**: before/after, plan A/B, problem/solution laid out side by side, with titles and baselines strictly aligned.
- **Timeline/flowchart**: steps expressed via nodes and arrows, with the flow direction immediately obvious.

Font and spacing suggestions:

- Titles 36-44pt, key conclusions may be larger; body 14-18pt; notes 10-12pt.
- Body left-aligned by default; use centering only on cover, closing, or large-number scenarios.
- Page margins at least 40px; keep 24-40px spacing between content blocks, and keep it consistent within the same deck.
- Card padding must leave real breathing room — do not let text touch the edge; account for text-box padding when aligning shapes and text.

Common mistakes you MUST avoid:

- Do not reuse the same title + three-bullets layout on every page.
- Do not use low-contrast text or low-contrast icons, e.g. light gray text on a light background.
- Do not let decorative lines pass through text, or let footers, sources, and numbering crowd the main content.
- Do not render missing assets as empty image frames; you MUST generate XML-native visuals per `fallback_if_missing`.
- Do not leave template placeholder copy, sample company names, sample dates, or original template content unrelated to the user's theme.

### Choosing the Creation Method

| Scenario | Recommended method |
|------|----------|
| Simple XML (1-3 pages, simple structure, almost no complex CJK or special characters) | `lark_api({ tool: 'slides', op: 'create', args: { slides: [...] } })` — one-step creation |
| Complex XML (multi-page, contains CJK, large text blocks, complex layout, nested quotes, many special characters) | **Two-step creation**: first `lark_api({ tool: 'slides', op: 'create', args: {} })` to create a blank presentation, then add pages one by one via `lark_api({ tool: 'slides', op: 'xml_presentation.slide.create', ... })` |
| Continue appending or inserting pages into an existing presentation | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.create', args: { xml_presentation_id: '...' } })`, with `before_slide_id` when needed |
| Read the content of a single page | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.get', args: { xml_presentation_id: '...', slide_id: '...' } })` |
| Delete a page | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.delete', args: { xml_presentation_id: '...', slide_id: '...' } })` |
| Replace a single page's content | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.replace', args: { xml_presentation_id: '...', slide_id: '...' } })` |

> [!WARNING]
> The risk of one-step creation with a `slides` array is mainly in argument size, not page count alone. Even with only 1 page, if the XML is complex enough, two-step creation is recommended.

> [!IMPORTANT]
> One-step `op: 'create'` with a `slides` array creates pages one by one under the hood — it is not atomic. On mid-way failure, first record the `xml_presentation_id`, read back via `lark_api({ tool: 'slides', op: 'xml_presentations.get', ... })` to confirm the current state, then continue to fix or append.

### Template-and-Script-First Flow

For template details see [template-catalog.md](references/template-catalog.md). For the main flow just remember: `search` first, `summarize` after locking, and `extract` only when a skeleton is needed; do not read the complete template XML directly or copy placeholder copy.

```bash
python3 skills/lark-slides/scripts/template_tool.py search --query "<user need verbatim>" --limit 3
python3 skills/lark-slides/scripts/template_tool.py summarize --template <template-id> --label <cover|toc|section|content|closing>
python3 skills/lark-slides/scripts/template_tool.py extract --template <template-id> --label <page-type> --out /tmp/template-slice.xml
```

```text
Step 1: Clarify requirements & read knowledge
  - Clarify theme, audience, page count, style; handle template needs per "Template-and-Script-First Flow"
  - Read xml-schema-quick-ref.md; for new creation / major rewrite, also read planning-layer.md, visual-planning.md, asset-planning.md

Step 2: Generate outline → user confirmation → write slide_plan.json
  - Generate a structured outline for the user to confirm; if using a template, note which template it is based on
  - New creation / major rewrite MUST first create the directory and write `.lark-slides/plan/<deck-or-task-id>/slide_plan.json`
  - Plan fields, path naming, template boundaries, and `asset_need` structure follow planning-layer.md / asset-planning.md

Step 3: Generate XML per slide_plan.json → create
  - Consume the plan page by page: key_message sets the main conclusion, layout_type sets geometry, visual_focus sets the primary visual, text_density sets the text amount
  - When real assets are missing, MUST use `fallback_if_missing` to generate XML-native fallback visuals; do not leave blank
  - Choose the creation method per "Choosing the Creation Method"; handle images, complex XML, escaping, and 3350001 per lark-slides-create.md, media-upload.md, troubleshooting.md

Step 4: Review & deliver
  - After creation, MUST use `lark_api({ tool: 'slides', op: 'xml_presentations.get', ... })` to read back the full XML and perform explicit validation per validation-checklist.md, including the XML text-overlap check
  - Handle failures or partial success per troubleshooting.md; for local issues, prefer `lark_api({ tool: 'slides', op: 'replace-slide', ... })` to fix
  - No issues → deliver: inform the user of the presentation ID and how to access it
```

### Appending Pages to an Existing Presentation

For new presentations, one-step `op: 'create'` with a `slides` array is recommended. When appending pages to an existing presentation, build the slide content as an XML string and pass it through `args`:

```
# Append to the end
lark_api({
  tool: 'slides',
  op: 'xml_presentation.slide.create',
  args: {
    xml_presentation_id: 'YOUR_ID',
    slide: {
      content: '<slide xmlns="http://www.larkoffice.com/sml/2.0"><style><fill><fillColor color="BACKGROUND_COLOR"/></fill></style><data>Place shape, line, table, chart, and other elements here</data></slide>'
    }
  }
})

# Insert before a specific page: before_slide_id MUST be at the same level as slide
# (not buried under the presentation id) so the server honors the position; otherwise the new page lands at the end
lark_api({
  tool: 'slides',
  op: 'xml_presentation.slide.create',
  args: {
    xml_presentation_id: 'YOUR_ID',
    slide: { content: '<slide ...>...</slide>' },
    before_slide_id: 'TARGET_SLIDE_ID'
  }
})
```

> Gradients MUST use the `rgba()` format with percentage stops, e.g. `linear-gradient(135deg,rgba(15,23,42,1) 0%,rgba(56,97,140,1) 100%)`. Using `rgb()` or omitting stops causes the server to fall back to white.

### Outline Template

When generating an outline, use the following format and hand it to the user for confirmation:

```text
[Presentation title] — [positioning description], for [target audience]

Template: [no template used / <category>/<template>.xml (reason for recommendation)]

Page structure (N pages):
1. Cover: [title copy]
2. [Page topic]: [point 1], [point 2], [point 3]
3. [Page topic]: [point description]
...
N. Closing: [closing copy]

Style: [color scheme], [layout style]
```

## Core Concepts

### URL Format and Token

| URL format | Example | Token type | Handling |
|----------|------|-----------|----------|
| `/slides/` | `https://example.larkoffice.com/slides/xxxxxxxxxxxxx` | `xml_presentation_id` | The token in the URL path is used directly as `xml_presentation_id` |
| `/wiki/` | `https://example.larkoffice.com/wiki/wikcnxxxxxxxxx` | `wiki_token` | ⚠️ **Cannot be used directly** — must query first to obtain the real `obj_token` |

> The `replace-slide` and `media-upload` operations auto-resolve both URL types above; when calling `xml_presentations.get` / `xml_presentation.slide.*` directly, you still need to resolve wiki links manually.

### Wiki Link Special Handling (Important!)

A wiki link (`/wiki/TOKEN`) cannot be used directly as `xml_presentation_id`. Before calling `xml_presentations.get` directly, query the wiki node, confirm `node.obj_type == "slides"`, then use `node.obj_token` as the real presentation ID.

```
lark_api({ tool: 'wiki', op: 'spaces.get_node', args: { token: 'wiki_token' } })
```

The `replace-slide` and `media-upload` operations auto-resolve `/wiki/` URLs; manual resolution is needed only when calling `xml_presentations.get` / `xml_presentation.slide.*` yourself.

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

Use the LarkSkill MCP `lark_api` tool for all slides operations. A shortcut op (e.g. `create`, `media-upload`, `replace-slide`) is a high-level wrapper over common operations — prefer the shortcut when one exists. The catalog provides these slides operations:

| Operation | MCP call | Description |
|----------|------|------|
| Create presentation | `lark_api({ tool: 'slides', op: 'create', args: { slides: [...] } })` | Create a presentation; optionally pass a `slides` array to add pages in one call; supports the `<img src="@./local.png">` placeholder for auto-upload |
| Upload image | `lark_api({ tool: 'slides', op: 'media-upload', args: { xml_presentation_id: '...', file: '...' } })` | Upload a local image to a specific presentation and return a `file_token` (used as `<img src="...">`); max 20 MB |
| Block-level edit | `lark_api({ tool: 'slides', op: 'replace-slide', args: { ... } })` | Block-level replace/insert (`block_replace` / `block_insert`) on an existing slide page; auto-injects id and `<content/>`; does not change page order |
| Read full presentation | `lark_api({ tool: 'slides', op: 'xml_presentations.get', args: { xml_presentation_id: '...' } })` | Read the full presentation XML |
| Create a page | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.create', args: { xml_presentation_id: '...' } })` | Add a single page; supports `before_slide_id` for position |
| Delete a page | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.delete', args: { xml_presentation_id: '...', slide_id: '...' } })` | Delete a single page; deletion is irreversible |
| Read a page | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.get', args: { xml_presentation_id: '...', slide_id: '...' } })` | Read a single page's XML |
| Replace a page | `lark_api({ tool: 'slides', op: 'xml_presentation.slide.replace', args: { xml_presentation_id: '...', slide_id: '...' } })` | Replace a single page's whole-page structure |

Use `lark_api_search` to discover the exact args shape for any operation before invoking it — do not guess field structures.

## Core Rules

1. **Plan before writing XML**: when creating a new presentation or performing a major page rewrite, you MUST first write `.lark-slides/plan/<deck-or-task-id>/slide_plan.json`; templates, styles, and outlines can only be planning inputs and cannot bypass the planning layer.
2. **Creation flow**: simple short XML (1-3 pages, simple structure, few special characters) can use `lark_api({ tool: 'slides', op: 'create', args: { slides: [...] } })` for one-step creation; for complex content, images, large CJK text blocks, nested quotes, many special characters, or more than 10 pages, default to `op: 'create'` (blank presentation) first, then add pages one by one via `op: 'xml_presentation.slide.create'`.
3. **The only direct children of `<slide>` are `<style>`, `<data>`, `<note>`**: text and graphics MUST be placed inside `<data>`.
4. **Text is expressed via `<content>`**: MUST use `<content><p>...</p></content>`; do not write text directly inside a shape.
5. **Save key IDs**: subsequent operations require `xml_presentation_id`, `slide_id`, `revision_id`.
6. **Be cautious with deletions**: deletion via `op: 'xml_presentation.slide.delete'` is irreversible, and at least one slide must remain.
7. **Prefer block-level replace when editing existing pages**: to modify a single shape/img, use `op: 'replace-slide'` (`block_replace` / `block_insert`); do not rebuild the whole page. Only use `op: 'xml_presentation.slide.delete'` + `op: 'xml_presentation.slide.create'` when you need to replace the whole-page structure.
8. **`<img src>` may only use a `file_token` uploaded to Lark Drive; http(s) external link URLs are FORBIDDEN**: the Lark slides renderer does not proxy external images, so an external src usually does not display or shows a broken image in the presentation. The flow MUST be: save the image locally first → upload via `op: 'media-upload'` or have the `@./path` placeholder of `op: 'create'` auto-upload it → take the `file_token` and write it into `<img src>`. If the user provides a web image link, download it into the CWD first, then go through the upload flow; do not paste the external URL directly into `src`. **Max image size 20 MB** (the slides upload op does not support chunked upload).

## Permissions Quick Reference

| Operation | Required scope |
|------|-----------|
| `slides create` | `slides:presentation:create`, `slides:presentation:write_only` (also `docs:document.media:upload` when `@` placeholders are used) |
| `slides media-upload` | `docs:document.media:upload` (wiki URL resolution also requires `wiki:node:read`) |
| `slides replace-slide` | `slides:presentation:update` (wiki URL resolution also requires `wiki:node:read`) |
| `slides xml_presentations.get` | `slides:presentation:read` |
| `slides xml_presentation.slide.create` | `slides:presentation:update` or `slides:presentation:write_only` |
| `slides xml_presentation.slide.delete` | `slides:presentation:update` or `slides:presentation:write_only` |
| `slides xml_presentation.slide.get` | `slides:presentation:read` |
| `slides xml_presentation.slide.replace` | `slides:presentation:update` |

> **Note**: if the `.md` content conflicts with `slides_xml_schema_definition.xml` or the `lark_api_search` output for a slides operation, the latter two take precedence.
