---
name: lark-slides
version: 1.0.0
description: "Use this skill when creating or editing Lark Slides presentations via LarkSkill MCP. Handles presentation creation, reading slide content, and managing individual slides (create, delete, read, partial replace). Communication uses XML protocol."
metadata:
  requires:
    mcp: "larkskill"
  mcpTools: ["lark_api"]
---

# slides (v1)

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) first — it covers authentication and permission handling.

**CRITICAL — Before generating any XML, MUST read [`xml-schema-quick-ref.md`](references/xml-schema-quick-ref.md). DO NOT guess XML structure from memory.**

**CRITICAL — If the user mentions "template", "apply a template", or "reference a theme/style/layout", or the request clearly fits an existing template scenario (e.g. work report, product intro, business plan, training, promotion review), MUST first use [`scripts/template_tool.py`](scripts/template_tool.py) `search` to retrieve template candidates. Default to 2–3 best-match candidates for the user to choose from. After locking in a template, use `summarize` to get theme and layout summary; use `extract` to crop target page-type XML only when a layout skeleton is needed. Do NOT read full template XML directly.**

> [!NOTE]
> `scripts/template_tool.py` requires Python 3. `references/template-index.json` is a script cache / lightweight routing index, not a document for the agent to read by default. `assets/templates/*.xml` are machine resources — access only via script summary or extract, never full-read.

**CRITICAL — When generating or rewriting pages from a template, MUST first `summarize` the target page type; use `extract` only when a concrete layout skeleton is needed. After generating local XML, if Python is available, MUST run [`scripts/layout_lint.py`](scripts/layout_lint.py) to check XML well-formedness, overlap/out-of-bounds/text-height risks before creating or appending slides. This is not a full XSD schema validation.**

**Editing existing slides:** prefer [`+replace-slide`](references/lark-slides-replace-slide.md) (block-level replace/insert, does not alter page order). For action selection and the full read-modify-write workflow, see [`lark-slides-edit-workflows.md`](references/lark-slides-edit-workflows.md).

## Identity selection

Lark Slides are typically the user's own content resources. **Default to explicit `user` identity for all slides operations.**

- **`user` identity (recommended):** Create, read, and manage presentations as the currently logged-in user. Complete user authorization first:

```
lark_auth_login({ domain: 'slides' })
```

- **`bot` identity:** Only when the user explicitly requires bot/app-identity operations, or when the bot needs to own/create the resource. When using bot identity, confirm separately that the bot actually has access to the target presentation.

**Execution rules:**

1. Create, read, add/delete slides, and continue editing an existing PPT from a user-supplied link — default to `user` identity.
2. If a permission error occurs, first check whether bot identity was mistakenly used; do NOT default-fallback to bot.
3. Switch to bot identity only when the user explicitly requests "app identity / bot identity", or the workflow is bot-creates-resource-then-collaborates.

## Quick start

Create a PPT with slide content in one call (recommended):

```
lark_api({ tool: 'slides', op: 'create', args: {
  title: 'Presentation Title',
  slides: [
    '<slide xmlns="http://www.larkoffice.com/sml/2.0"><style><fill><fillColor color="rgb(245,245,245)"/></fill></style><data><shape type="text" topLeftX="80" topLeftY="80" width="800" height="100"><content textType="title"><p>Page Title</p></content></shape><shape type="text" topLeftX="80" topLeftY="200" width="800" height="200"><content textType="body"><p>Body content</p><ul><li><p>Point one</p></li><li><p>Point two</p></li></ul></content></shape></data></slide>'
  ]
} })
```

Two-step approach also available (create empty PPT first, then add slides one by one) — see [`+create` reference](references/lark-slides-create.md).

> [!WARNING]
> `slides` array is suitable for simple batch page creation, but is NOT "safe for anything under 10 pages". If slide XML contains significant non-ASCII text, long passages, complex layouts, nested quotes, or many special characters, shell parameter passing may cause escaping or truncation issues — leading to lost content, blank pages, or layout errors. For complex pages, prefer the two-step approach.

> [!IMPORTANT]
> `slides +create --slides` is internally "create blank PPT first, then call `xml_presentation.slide.create` per page". This is not atomic: if one page fails mid-way, previously created pages are retained. The skill MUST inform the user of this "partial success" risk upfront, and after failure first record `xml_presentation_id`, read back the current state, then decide whether to continue fixing or appending to the existing PPT.

## Before you begin

> **Important:** `references/slides_xml_schema_definition.xml` is the single authoritative XML protocol source for this skill; other `.md` files are only summaries of it and the CLI schema.

### Required reading (before every create)

| Document | Description |
|----------|-------------|
| [xml-schema-quick-ref.md](references/xml-schema-quick-ref.md) | **XML elements and attributes quick reference — required reading** |

### Optional reading (consult as needed)

| Scenario | Document |
|----------|----------|
| Need detailed XML structure | [xml-format-guide.md](references/xml-format-guide.md) |
| Need to quickly screen templates / lightweight routing | [`scripts/template_tool.py search`](scripts/template_tool.py) |
| Need to match PPT template / theme / style | [template-catalog.md](references/template-catalog.md) |
| Need to summarize a page type or crop XML fragments | [`scripts/template_tool.py`](scripts/template_tool.py) |
| Need local layout risk check | [`scripts/layout_lint.py`](scripts/layout_lint.py) |
| Need CLI call examples | [examples.md](references/examples.md) |
| Need real PPT XML as reference | [slides_demo.xml](references/slides_demo.xml) |
| Need table / chart and other complex elements | [slides_xml_schema_definition.xml](references/slides_xml_schema_definition.xml) (full schema) |
| Need to edit an existing PPT page | [lark-slides-edit-workflows.md](references/lark-slides-edit-workflows.md) |
| Need detailed parameters for a specific command | Corresponding reference doc (see References section below) |

## Workflow

> **This is a presentation, not a document.** Each slide is an independent visual frame — keep information density low and leave whitespace.

### Creation method selection

| Scenario | Recommended approach |
|----------|----------------------|
| Simple XML (1–3 pages, simple structure, minimal non-ASCII / special characters) | `lark_api({ tool: 'slides', op: 'create', args: { slides: [...] } })` one-step create |
| Complex XML (multiple pages, non-ASCII text, long passages, complex layouts, nested quotes, many special characters) | **Two-step:** first `slides +create` to create blank PPT, then `xml_presentation.slide create` to add pages one by one |
| Appending or inserting pages to an existing PPT | Use `lark_api({ tool: 'slides', op: 'xml_presentation.slide create', ... })`, with `before_slide_id` if needed |

> [!WARNING]
> The risk in `--slides '[...]'` lies primarily in shell parameter passing, not page count alone. Even a single page can be problematic if the XML is sufficiently complex — prefer the two-step approach.

### Template and script priority flow

```bash
# 1. Search candidates: pass the user's original request verbatim in --query
python3 skills/lark-slides/scripts/template_tool.py search --query "<user request verbatim>" --limit 3

# 2. After locking in a template, get page-type summary first
python3 skills/lark-slides/scripts/template_tool.py summarize --template <template-id> --label <cover|toc|section|content|closing>

# 3. Crop XML only when reusing a layout skeleton
python3 skills/lark-slides/scripts/template_tool.py extract --template <template-id> --label <page-type> --out /tmp/template-slice.xml

# 4. Run layout risk check after generating the XML to create
python3 skills/lark-slides/scripts/layout_lint.py --input /tmp/presentation.xml
```

Execution rules:

1. Use the user's original description for `search --query`; add `--tone light|dark|colorful` or `--formality formal|casual|creative` only when the user specifies a style.
2. Show only 2–3 candidates, including template name, applicable scenario, style/tone, and recommendation reason — do not paste the full catalog.
3. After locking in a template, reuse `<theme>`, colors, page flow, and layout skeleton; rewrite ALL placeholder text with the user's real content.
4. If `layout_lint.py` reports errors, fix the XML first — do not submit for creation. Warnings are acceptable only when they are verifiable decoration/background false positives.

```text
Step 1: Requirements clarification & knowledge loading
  - Clarify user requirements: topic, audience, page count, style preferences
  - If the request clearly falls into an existing template scenario, proactively suggest "can generate directly from a ready-made template" and show 2–3 best-match candidates (template name + scenario + style/tone + brief recommendation reason)
  - Default: do not paste the full template catalog to the user; show only 2–3 candidates unless the user explicitly asks for more
  - Prioritize scenario-specific templates; fall back to general templates (e.g. light_general.xml / dark_general.xml) only when no obvious scenario template matches
  - If the user has not specified a style, recommend based on topic (see style judgment table below)
  - If the user requests "template / theme / style reference", or the topic belongs to a common template scenario:
    · First run `python3 skills/lark-slides/scripts/template_tool.py search --query "<user request verbatim>" --limit 3` for low-cost template matching
    · Read template-catalog.md to compose candidate descriptions only when human-readable explanation is needed
    · After locking in a template, prefer running `template_tool.py summarize` to inspect `<theme>` / page-type summary; use `template_tool.py extract` only when concrete layout is needed
    · Reuse template theme, colors, page flow, and layout skeleton; rewrite ALL placeholder text with real content
    · `references/template-index.json` is a script cache/routing index; `assets/templates/*.xml` are machine resources — do not read directly unless user explicitly requests raw template audit
  - Load XML Schema references:
    · xml-schema-quick-ref.md — elements and attributes quick reference
    · xml-format-guide.md — detailed structure and examples
    · slides_demo.xml — real XML examples

Step 2: Generate outline → user confirmation → create
  - Before generating outline, confirm whether user adopts the recommended template; for lightweight tasks with one clear best match, you may state "defaulting to <template-id>" in the outline and proceed — but MUST give user a chance to change before actual creation
  - Generate a structured outline (page title + key points + layout description) and present to user for confirmation
  - If a template is selected, outline and page layout MUST clearly note "based on which template / which pages"
  - If user explicitly declines templates, proceed with custom style — do not keep pushing template selection
  - Determine creation approach first:
    · Simple XML: can use `lark_api({ tool: 'slides', op: 'create', args: { slides: [...] } })` one-step
    · Complex XML: prefer `slides +create` to create blank PPT first, then add pages via `xml_presentation.slide.create`
    · More than 10 pages: default to two-step to avoid overly long single input
  - For local images:
    · New PPT with images — write `<img src="@./pic.png" .../>` in slide XML; `+create` auto-uploads and replaces with file_token (see lark-slides-create.md)
    · Add image pages to existing PPT — first `lark_api({ tool: 'slides', op: 'media-upload', args: { file: './pic.png', presentation_id: '$PID' } })` to get file_token, then use it in slide XML for `xml_presentation.slide.create`
    · Add image to existing page — two steps: (1) `slides +media-upload` for file_token; (2) `slides +replace-slide` with `block_insert` to insert `<img src="<file_token>" .../>`; do NOT rebuild the whole page
    · Path MUST be a relative path within CWD (e.g. ./pic.png or ./assets/x.png); absolute paths are rejected by the CLI — `cd` to the asset directory first
  - Each slide needs complete XML: background, text, shapes, colors
  - Complex elements (table, chart) require consulting the full XSD
  - MUST self-check XML before creating:
    · Verify special characters are escaped per XML rules: bare `& → &amp;` in text nodes and attribute values; `< → &lt;` and `> → &gt;` in text. E.g. `Q&A → Q&amp;A`, URL attribute `a=1&b=2 → a=1&amp;b=2`
    · Double quotes in attribute values MUST be escaped or use safe outer wrapping to avoid shell and JSON double-truncation
    · Confirm all tags are closed, and `<slide>` direct children include only `<style>`, `<data>`, `<note>`
    · If content contains significant non-ASCII text, long passages, complex layouts, or many special characters — default to two-step approach, not `--slides '[...]'`
    · If XML is already in a local file and Python is available, run `layout_lint.py --input <file>` first; it checks XML well-formedness then layout risks, but is not equivalent to full XSD schema validation; fix errors before creating
  - When generating pages from a template, reuse the template skeleton then fill in content — do NOT copy long placeholder text from the template

Step 3: Review & delivery
  - After creation, MUST read the full XML with xml_presentations.get to verify, confirming:
    · Is the page count correct?
    · Does each page's `<data>` contain the expected `<shape>` / `<img>` / other elements?
    · Is text content complete with no truncation, loss, or blank areas?
    · Are key layout coordinates and dimensions reasonable with no obvious overlap?
    · Are colors consistent? Is the font-size hierarchy reasonable?
  - If Python 3 is available locally, run `python3 skills/lark-slides/scripts/layout_lint.py --input presentation.xml` to check overlap, out-of-bounds, footer collision, and text-height risks; fix errors before delivery
  - If creation fails:
    · First retain and record `xml_presentation_id` — do not assume failure means nothing was created
    · Determine whether partial pages were written, then decide whether to fix and continue appending to the existing PPT
    · Prioritize diagnosing the failing page: inspect its XML, check for unescaped `&`, wrong quotes, unclosed tags, shell parameter truncation
  - Localized issues → use `+replace-slide` for block-level correction; full page structure change → `slide.delete` old page + `slide.create` new page
  - No issues → deliver: inform user of presentation ID and access method
```

### Post-creation verification

Successful creation does not mean correct content. After creating the PPT, **MUST** read the full XML to verify:

```
lark_api({ tool: 'slides', op: 'xml_presentations.get', args: { xml_presentation_id: 'YOUR_ID' } })
```

Key checks:

- [ ] Is the page count as expected?
- [ ] Does each page's `<data>` contain all expected elements?
- [ ] Is text content complete — not truncated or damaged by shell escaping?
- [ ] Were key layout areas (white content area, card area, image+text area) actually created?
- [ ] Are coordinates and dimensions reasonable — no stacking or out-of-bounds?

When issues are found:

1. Do NOT assume "creation succeeded means rendering is correct"
2. Read the problematic page's XML first — confirm whether it is a generation issue or parameter damage
3. Delete the problematic page and re-add; for complex pages, prefer the two-step approach

### Minimum acceptance checklist

After creation, run through this sequence by default — do not skip:

1. Record `xml_presentation_id`
2. Confirm whether the returned `slides_added` or actual page count matches expectations
3. Immediately call `xml_presentations.get`
4. Check title, key pages, key text content
5. Check for obvious blank pages, missing content, or wrong page order
6. Then decide whether to deliver the URL and follow-up editing suggestions to the user

Recommended minimum closed loop:

```
// Create
lark_api({ tool: 'slides', op: 'create', args: { title: 'Demo', slides: ['...'] } })

// Immediately read back
lark_api({ tool: 'slides', op: 'xml_presentations.get', args: { xml_presentation_id: 'YOUR_ID' } })
```

## XML self-check and troubleshooting

Before actually creating, perform at least these 4 checks:

- [ ] Special characters escaped: `&`, `<`, `>` in body and titles MUST NOT appear bare; bare `&` in attribute values also MUST be written as `&amp;`
- [ ] Attribute quote safety: XML attributes, shell quotes, and JSON string wrapping do not break each other
- [ ] Valid structure: `<slide>` children are only `<style>`, `<data>`, `<note>`; all text is inside `<content>`
- [ ] Correct paths: `<img src="@...">` is only valid in the `+create --slides` pipeline

Common failure signals and resolution order:

1. `invalid param` / a page create fails
2. First check if the failing page contains unescaped `&` / `<` / `>`: `Q&A → Q&amp;A`, attribute URL `a=1&b=2 → a=1&amp;b=2`
3. Then check tag closure, attribute quotes, `<content>` structure
4. If using `--slides '[...]'`, switch directly to the two-step approach when shell truncation is suspected
5. After creation — success or failure — always record `xml_presentation_id` first and read back to confirm whether partial pages were written

### jq command templates (when appending to an existing PPT)

For new PPTs, use `+create --slides`. The following jq templates apply when appending to an existing presentation — they avoid manual double-quote escaping:

```bash
# Append to end
lark-cli slides xml_presentation.slide create \
  --as user \
  --params '{"xml_presentation_id":"YOUR_ID"}' \
  --data "$(jq -n --arg content '<slide xmlns="http://www.larkoffice.com/sml/2.0">
  <style><fill><fillColor color="BACKGROUND_COLOR"/></fill></style>
  <data>
    Place shape, line, table, chart, and other elements here
  </data>
</slide>' '{slide:{content:$content}}')"

# Insert before a specific page: before_slide_id MUST be in the --data body, at the same level as slide
# WARNING: do NOT put before_slide_id in --params — the CLI passes it as an unknown query param and the server ignores it, moving the new page to the end
lark-cli slides xml_presentation.slide create \
  --as user \
  --params '{"xml_presentation_id":"YOUR_ID"}' \
  --data "$(jq -n --arg content '<slide ...>...</slide>' --arg before 'TARGET_SLIDE_ID' \
    '{slide:{content:$content}, before_slide_id:$before}')"
```

### Style quick-reference table

> **Note:** Gradient colors MUST use `rgba()` format with percentage stop points, e.g. `linear-gradient(135deg,rgba(15,23,42,1) 0%,rgba(56,97,140,1) 100%)`. Using `rgb()` or omitting stop points causes the server to fall back to white.

| Scenario / topic | Recommended style | Background | Primary color | Text color |
|------------------|-------------------|------------|---------------|------------|
| Tech / AI / product | Dark tech | Deep blue gradient `linear-gradient(135deg,rgba(15,23,42,1) 0%,rgba(56,97,140,1) 100%)` | Blue `rgb(59,130,246)` | White |
| Business report / quarterly summary | Light business | Light gray `rgb(248,250,252)` | Deep blue `rgb(30,60,114)` | Dark gray `rgb(30,41,59)` |
| Education / training | Fresh bright | White `rgb(255,255,255)` | Green `rgb(34,197,94)` | Dark gray `rgb(51,65,85)` |
| Creative / design | Gradient vibrant | Purple-pink gradient `linear-gradient(135deg,rgba(88,28,135,1) 0%,rgba(190,24,93,1) 100%)` | Pink-purple | White |
| Weekly / daily report | Minimal professional | Light gray `rgb(248,250,252)` + top color gradient bar | Blue `rgb(59,130,246)` | Dark `rgb(15,23,42)` |
| Not specified by user | Default minimal professional | Same as above | Same as above | Same as above |

### Page layout guidance

| Page type | Layout key points |
|-----------|-------------------|
| Cover | Centered large title + subtitle + bottom info; gradient or dark background |
| Data overview | Metric cards in a row (rect background + large number + small label), chart or list below |
| Content | Left vertical line decoration + title, split columns or list below |
| Comparison / table | `table` element or side-by-side cards; header with dark background and white text |
| Chart | `chart` element (column / line / pie), with text callouts |
| Closing | Centered thank-you text + decorative line; style echoes the cover |

### Outline template

Use this format when generating an outline for user confirmation:

```text
[PPT Title] — [Positioning description], for [target audience]

Template: [no template / <category>/<template>.xml (recommendation reason)]

Page structure (N pages):
1. Cover: [title copy]
2. [Page topic]: [Point 1], [Point 2], [Point 3]
3. [Page topic]: [description]
...
N. Closing: [closing copy]

Style: [color scheme], [layout style]
```

### Common slide XML templates

Ready-to-copy templates (cover, content, data card, closing pages): [slide-templates.md](references/slide-templates.md)

---

## Core concepts

### URL formats and tokens

| URL format | Example | Token type | Handling |
|------------|---------|------------|----------|
| `/slides/` | `https://example.larkoffice.com/slides/xxxxxxxxxxxxx` | `xml_presentation_id` | Token from the URL path is used directly as `xml_presentation_id` |
| `/wiki/` | `https://example.larkoffice.com/wiki/wikcnxxxxxxxxx` | `wiki_token` | **Cannot be used directly** — must query to get the real `obj_token` first |

> `+replace-slide` and `+media-upload` shortcuts auto-resolve both URL types; when calling raw APIs directly, wiki links must still be parsed manually.

### Wiki link special handling (critical)

Wiki links (`/wiki/TOKEN`) may resolve to cloud documents, spreadsheets, slides, or other document types. **Do NOT assume the URL token is the `xml_presentation_id`** — always query the actual type and real token first.

#### Handling flow

1. **Query node info via `wiki.spaces.get_node`**
   ```
   lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: 'wiki_token' } })
   ```

2. **Extract key fields from the result**
   - `node.obj_type`: document type; slides corresponds to `slides`
   - `node.obj_token`: **the real presentation token** (used for subsequent operations)
   - `node.title`: document title

3. **After confirming `obj_type` is `slides`, use `obj_token` as `xml_presentation_id`**

#### Query example

```
// Query wiki node
lark_api({ method: 'GET', path: '/open-apis/wiki/v2/spaces/get_node', params: { token: 'wikcnxxxxxxxxx' } })
```

Example response:
```json
{
   "node": {
      "obj_type": "slides",
      "obj_token": "xxxxxxxxxxxx",
      "title": "2026 Annual Product Summary",
      "node_type": "origin",
      "space_id": "1234567890"
   }
}
```

```
// Use obj_token to read slide content
lark_api({ tool: 'slides', op: 'xml_presentations.get', args: { xml_presentation_id: 'xxxxxxxxxxxx' } })
```

### Resource relationships

```text
Wiki Space
└── Wiki Node (obj_type: slides)
    └── obj_token → xml_presentation_id

Slides (Presentation)
├── xml_presentation_id (unique presentation identifier)
├── revision_id (version number)
└── Slide (individual page)
    └── slide_id (unique page identifier)
```

## Shortcuts (use these first)

Shortcuts are high-level wrappers (`lark_api({ tool: 'slides', op: '<verb>', args: {...} })`). Prefer shortcuts when available.

| Shortcut | Description |
|----------|-------------|
| [`+create`](references/lark-slides-create.md) | Create a PPT (optional `--slides` to add pages in one step, supports `<img src="@./local.png">` placeholder auto-upload); bot mode auto-grants permissions |
| [`+media-upload`](references/lark-slides-media-upload.md) | Upload a local image to a presentation and return `file_token` (use as `<img src="...">`); max 20 MB |
| [`+replace-slide`](references/lark-slides-replace-slide.md) | Block-level replace/insert on an existing slide page (`block_replace` / `block_insert`); auto-injects id and `<content/>`; does not alter page order |

### Shortcut examples

```
// Create a new presentation with slides
lark_api({ tool: 'slides', op: 'create', args: { title: 'My Presentation', slides: ['<slide ...>...</slide>'] } })

// Upload a local image and get file_token
lark_api({ tool: 'slides', op: 'media-upload', args: { file: './image.png', presentation_id: 'YOUR_PPT_ID' } })

// Block-level replace on an existing slide
lark_api({ tool: 'slides', op: 'replace-slide', args: { xml_presentation_id: 'YOUR_PPT_ID', slide_id: 'SLIDE_ID', parts: [{ action: 'block_replace', block_id: 'BLOCK_ID', content: '<shape ...>...</shape>' }] } })

// Read full presentation XML
lark_api({ tool: 'slides', op: 'xml_presentations.get', args: { xml_presentation_id: 'YOUR_PPT_ID' } })
```

## API Resources

> **Important:** Before using any raw API, inspect the request schema to understand `data` / `params` field structure — do not guess field formats.

### xml_presentations

- `get` — Read full presentation content, returned in XML format

### xml_presentation.slide

- `create` — Create a slide in the specified XML presentation (no shortcut op; use raw HTTP form)

- `delete` — Delete a slide from the specified XML presentation (no shortcut op; use raw HTTP form)

- `get` — Get a single slide's XML content from the specified XML presentation (no shortcut op; use raw HTTP form)

- `replace` — Perform element-level partial replacement on a slide in the specified XML presentation (no shortcut op; use raw HTTP form)

## Core rules

1. **Lock in template/style and produce outline before starting work:** If the request can match a template, give the user 2–3 template candidates first. Once template or custom style is confirmed, generate the outline for user confirmation — avoid rework.
2. **Creation flow:** Simple short XML (1–3 pages, simple structure, few special characters) can use `lark_api({ tool: 'slides', op: 'create', args: { slides: [...] } })` one-step; complex content, images / non-ASCII long text / nested quotes / many special characters, or more than 10 pages — default to `slides +create` to create blank PPT first, then add pages one by one via `xml_presentation.slide.create`.
3. **`<slide>` direct children are only `<style>`, `<data>`, `<note>`:** Text and shapes MUST be placed inside `<data>`.
4. **Text is expressed through `<content>`:** MUST use `<content><p>...</p></content>`; do NOT write text directly inside a shape element.
5. **Save key IDs:** Subsequent operations require `xml_presentation_id`, `slide_id`, `revision_id`.
6. **Deletion is irreversible:** Delete operations cannot be undone; at least one slide MUST remain in the presentation.
7. **Prefer block-level replacement when editing existing pages:** For modifying a single shape/img, use `+replace-slide` (`block_replace` / `block_insert`) — do NOT rebuild the whole page. Only use `slide.delete` + `slide.create` when the entire page structure needs replacing.
8. **`<img src>` MUST use a `file_token` uploaded to Lark Drive — external HTTP(S) URLs are forbidden:** The Lark Slides renderer does not proxy external images; external `src` values typically show as broken or missing. The flow MUST be: "save image locally → upload via `slides +media-upload` or use `+create --slides` `@./path` placeholder auto-upload → use the returned `file_token` in `<img src>`". If the user provides a web image URL, first `curl`/download it to CWD, then follow the upload flow — do NOT paste the external URL directly into `src`. **Max image size: 20 MB** (the slides upload API does not support chunked upload).

## Permission table

| Method | Required scope |
|--------|----------------|
| `slides +create` | `slides:presentation:create`, `slides:presentation:write_only` (also `docs:document.media:upload` when `@` placeholder is used) |
| `slides +media-upload` | `docs:document.media:upload` (wiki URL resolution also requires `wiki:node:read`) |
| `slides +replace-slide` | `slides:presentation:update` (wiki URL resolution also requires `wiki:node:read`) |
| `xml_presentations.get` | `slides:presentation:read` |
| `xml_presentation.slide.create` | `slides:presentation:update` or `slides:presentation:write_only` |
| `xml_presentation.slide.delete` | `slides:presentation:update` or `slides:presentation:write_only` |
| `xml_presentation.slide.get` | `slides:presentation:read` |
| `xml_presentation.slide.replace` | `slides:presentation:update` |

## Common error quick reference

| Error code | Meaning | Resolution |
|------------|---------|------------|
| 400 | XML format error | Check XML syntax; ensure all tags are closed |
| 400 | Request wrapping error | Check that `--data` passes `xml_presentation.content` or `slide.content` per schema |
| Creation succeeds but page is blank / content missing / layout broken | Common with `--slides '[...]'` shell escaping or long parameter issues | Switch to two-step: first `slides +create`, then use `jq -n` to wrap `xml_presentation.slide.create` per page; immediately read back XML after creation to verify |
| 404 | Presentation not found | Check that `xml_presentation_id` is correct |
| 404 | Slide not found | Check that `slide_id` is correct |
| 403 | Insufficient permission | Check that you have the required scope |
| 400 | Cannot delete the only slide | The presentation must retain at least one slide |
| 1061002 | params error (during media upload) | Use `slides +media-upload`; do not hand-craft raw `medias/upload_all`; the only valid `parent_type` for slides is `slide_file` |
| 1061004 | forbidden: current identity has no edit access to the presentation | Confirm user/bot has edit access to the target PPT; bot commonly lacks access when PPT was not created by that bot — grant access first or use `+create --as bot` to create new |
| 3350001 | XML not well-formed, XML structure does not meet server requirements, or `xml_presentation.slide.replace` failed (catch-all) | First check for unescaped `&` / `<` / `>`: `Q&A → Q&amp;A`, attribute URL `a=1&b=2 → a=1&amp;b=2`; run `layout_lint.py --input <file>` to locate line/column and context; also check `block_id` / `<content/>` / coordinates in replace scenarios |
| 3350002 | `revision_id` greater than current version | Use `-1` for the current version, or re-read `xml_presentations.get` for the latest `revision_id` |
| validation: unsafe file path | `--file` given an absolute path or parent path | `--file` MUST be a relative path within CWD; `cd` to the asset directory first |

## Pre-creation checklist

Quick checks before generating XML per page:

- [ ] Is each page's background color / gradient set? Is the style consistent with the overall theme?
- [ ] Title uses large font (28–48), body uses small font (13–16), clear hierarchy?
- [ ] Consistent colors within element groups? (e.g. all metric cards same color scheme, all body text same color)
- [ ] Decoration elements (divider lines, color blocks, vertical lines) in harmony with the primary color?
- [ ] Are text box dimensions sufficient to contain the content? (width × height)
- [ ] Is the shape `type` correct? (text boxes use `text`, decorations use `rect`)
- [ ] Are all XML tags correctly closed? Are special characters (`&`, `<`, `>`) escaped?

## Symptom → fix table

| Observed issue | What to fix |
|----------------|-------------|
| Text is cut off / not fully visible | Increase the shape's `width` or `height` |
| Elements overlap | Adjust `topLeftX` / `topLeftY`, increase spacing |
| Large blank area on page | Reduce element spacing, or add content to fill |
| Text and background color too similar | Dark background → light text; light background → dark text |
| Table column widths are unreasonable | Adjust `width` of `col` in `colgroup` |
| Chart not displaying | Check that both `chartPlotArea` and `chartData` are present; verify `dim1` / `dim2` data counts match |
| Image appears cropped | `<img>` `width` / `height` is the cropped size; if ratio mismatches the original, auto-cropping occurs — match `width:height` to the original image ratio for full display |
| Want to change only one element (text / image / shape) on a page | Use `+replace-slide` block-level replace — do NOT rebuild the whole page |
| Want to add an image to an existing page without touching other elements | (1) `+media-upload` to get `file_token`; (2) `+replace-slide` with `block_insert` to insert `<img src="<file_token>" .../>`; do NOT use the old "full page create + delete" flow |
| Newly inserted `<img>` overlaps or covers existing elements | Use `slide.get` to read the page; compare existing block `topLeftX/Y/width/height` to find a clear position; if space is tight, include both a `block_replace` to shrink/move the existing block and a `block_insert` for the image in the same `--parts` batch |
| Gradient background becomes white | Gradient MUST use `rgba()` format + percentage stop points, e.g. `linear-gradient(135deg,rgba(30,60,114,1) 0%,rgba(59,130,246,1) 100%)`; using `rgb()` or omitting stop points causes fallback to white |
| Gradient direction is wrong | Adjust the `linear-gradient` angle (`90deg` horizontal, `180deg` vertical, `135deg` diagonal) |
| Overall style is inconsistent | Cover and closing pages use the same background; content pages maintain a consistent color scheme and font-size hierarchy |
| API returns 400 | Check XML syntax: tag closure, attribute quotes, special character escaping |
| API returns 3350001 | `block_replace` root element missing `id=<block_id>` or `<shape>` missing `<content/>`; see replace-slide docs |
| Image not displaying / `<img src>` still shows `@path` | `@` placeholder **is only replaced in `+create --slides`**; when calling `xml_presentation.slide.create` directly, you MUST use `+media-upload` first to get `file_token` and write it into src |
| Image upload reports 1061002 params error | `parent_type` MUST be `slide_file` (the only accepted value for slides); do not hand-craft — use `slides +media-upload` |

## References

| Document | Description |
|----------|-------------|
| [lark-slides-create.md](references/lark-slides-create.md) | **+create shortcut: create PPT (supports `--slides` one-step page addition, `@` placeholder auto-image-upload)** |
| [lark-slides-media-upload.md](references/lark-slides-media-upload.md) | **+media-upload shortcut: upload local image, return `file_token`** |
| [lark-slides-replace-slide.md](references/lark-slides-replace-slide.md) | **+replace-slide shortcut: block-level replace/insert, including valid root element quick reference and 3350001 troubleshooting** |
| [lark-slides-edit-workflows.md](references/lark-slides-edit-workflows.md) | Read-modify-write workflow and action decision tree for editing existing pages |
| [template-index.json](references/template-index.json) | **Script cache / lightweight routing index: used by `template_tool.py search` — not a default reading entry** |
| [template-catalog.md](references/template-catalog.md) | **Match ready-made PPT templates by scenario / tone, locate page-type ranges** |
| [`scripts/template_tool.py`](scripts/template_tool.py) | **Optional Python helper: `search` / `summarize` / `extract`, supports `--layout-tag` and `extract --with-summary`** |
| [`scripts/layout_lint.py`](scripts/layout_lint.py) | **Local pre-check script: checks XML well-formedness, then detects overlap, out-of-bounds, footer collision, and text-height risk; not a full XSD schema validation** |
| [xml-schema-quick-ref.md](references/xml-schema-quick-ref.md) | **XML Schema condensed quick reference (required reading)** |
| [slide-templates.md](references/slide-templates.md) | Ready-to-copy slide XML templates |
| [xml-format-guide.md](references/xml-format-guide.md) | Detailed XML structure and examples |
| [examples.md](references/examples.md) | CLI call examples |
| [slides_demo.xml](references/slides_demo.xml) | Complete XML of a real PPT |
| [slides_xml_schema_definition.xml](references/slides_xml_schema_definition.xml) | **Complete schema definition** (the sole authoritative protocol source) |
| [lark-slides-xml-presentations-get.md](references/lark-slides-xml-presentations-get.md) | Read PPT command details |
| [lark-slides-xml-presentation-slide-create.md](references/lark-slides-xml-presentation-slide-create.md) | Add slide command details |
| [lark-slides-xml-presentation-slide-delete.md](references/lark-slides-xml-presentation-slide-delete.md) | Delete slide command details |
| [lark-slides-xml-presentation-slide-get.md](references/lark-slides-xml-presentation-slide-get.md) | Read single slide command details |
| [lark-slides-xml-presentation-slide-replace.md](references/lark-slides-xml-presentation-slide-replace.md) | Raw slide.replace API command details |

> **Note:** If a `.md` file conflicts with `slides_xml_schema_definition.xml` or `lark-cli schema slides.<resource>.<method>` output, the latter two take precedence.
