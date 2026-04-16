# docs +create

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Create a Lark cloud document from Markdown content.

## Recommended call

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/docx/v1/documents
- body:
  {
    "title": "Project Plan",
    "folder_token": "<FOLDER_TOKEN>"
  }
```

After creating the document, insert content blocks via:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
- body:
  {
    "children": [ ... block objects ... ],
    "index": 0
  }
```

## API request details

```
POST /open-apis/docx/v1/documents
POST /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
```

## Parameters (document creation body)

| Parameter | Required | Description |
|------|------|------|
| `title` | No | Document title |
| `folder_token` | No | Target Drive folder token. If omitted, creates in root |

## Markdown content support

The following Markdown/HTML structures are supported when inserting blocks:

### Text paragraphs

```markdown
normal text paragraph

**Bold text** in paragraphs

Separate multiple paragraphs with blank lines.

Center text {align="center"}
Right align text {align="right"}
```

### Headings

```markdown
# Level 1 title
## Second level title
### Third level title
#### Level 4 heading
##### Level 5 headings
###### Sixth level title
<h7>Level 7 heading</h7>
<h8>Eight-level headings</h8>
<h9>Level 9 headings</h9>

# Colored title {color="blue"}
## Red title {color="red"}
# Center the title {align="center"}
## Blue centered title {color="blue" align="center"}
```

### Lists

```markdown
- Unordered item 1
  - Unordered item 1.a
  - Unordered item 1.b

1. Ordered item 1
2. Ordered item 2

- [ ] To-do
- [x] Completed
```

### Quotes

```markdown
> This is a quote
> Can span multiple lines

> Reference formats such as **bold** and *italics* are supported
```

### Code blocks

````markdown
```python
print("Hello")
```
````

Supported languages: python, javascript, go, java, sql, json, yaml, shell, and more.

### Horizontal Rule

```markdown
---
```

### Callout

```html
<callout emoji="✅" background-color="light-green" border-color="green">
Supports **formatted** content, which can contain multiple blocks
</callout>
```

### Grid layout

```html
<grid cols="2">
<column>

Left column content

</column>
<column>

Right column content

</column>
</grid>
```

```html
<grid cols="3">
<column width="20">Left column (20%)</column>
<column width="60">Middle column (60%)</column>
<column width="20">Right column (20%)</column>
</grid>
```

### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|------|------|------|
| cell 1 | cell 2 | cell 3 |
| Cell 4 | Cell 5 | Cell 6 |
```

```
<lark-table> <- table container
  <lark-tr> <- row (direct child elements can only be lark-tr)
    <lark-td>Content</lark-td> <- cell (direct child element can only be lark-td)
    <lark-td>Content</lark-td> <- The number of lark-td in each line must be the same!
  </lark-tr>
</lark-table>
```

```html
<lark-td>

Write content here

</lark-td>
```

```html
<lark-table column-widths="200,250,280" header-row="true">
<lark-tr>
<lark-td>

**Header 1**

</lark-td>
<lark-td>

**Header 2**

</lark-td>
<lark-td>

**Header 3**

</lark-td>
</lark-tr>
<lark-tr>
<lark-td>

normal text

</lark-td>
<lark-td>

- List item 1
- List item 2

</lark-td>
<lark-td>

Code content

</lark-td>
</lark-tr>
</lark-table>
```

### Images and files

```html
<image url="https://example.com/image.png" width="800" height="600" align="center" caption="Image description text"/>
```

```html
<file url="https://example.com/document.pdf" name="Document.pdf" view-type="1"/>
```

### Whiteboard

```html
<whiteboard type="blank"></whiteboard>
```

Create a document with a single blank artboard:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/docx/v1/documents
- body: { "title": "Blank artboard example" }
```

Then insert whiteboard block into the document.

Multiple blank whiteboards:
```html
<whiteboard type="blank"></whiteboard>
<whiteboard type="blank"></whiteboard>
```

Reference existing whiteboard:
```html
<whiteboard token="xxx" align="center" width="800" height="600"/>
```

### Base (multidimensional table)

```html
<bitable view="table"/>
<bitable view="kanban"/>
```

### Other embeds

```html
<chat-card id="oc_xxx" align="center"/>
```

```html
<iframe url="https://example.com/survey?id=123" type="12"/>
```

```html
<link-preview url="Message link" type="message"/>
```

```html
<quote-container>
Reference container content
</quote-container>
```

```html
<sheet rows="5" cols="5"/>
<sheet/>
```

```html
<task task-id="xxx" members="ou_123, ou_456" due="2025-01-01">Task title</task>
```

```html
<!-- Source sync block -->
<source-synced align="1">Sub-block content...</source-synced>

<!-- Reference synchronized block -->
<reference-synced source-block-id="xxx" source-document-id="yyy">Source content...</reference-synced>
```

```html
<add-ons component-type-id="blk_xxx" record='{"key":"value"}'/>
```

```html
<sub-page-list wiki="wiki_xxx"/>
```

```html
<agenda>
  <agenda-item>
    <agenda-title>Agenda title</agenda-title>
    <agenda-content>Agenda content</agenda-content>
  </agenda-item>
</agenda>
```

```html
<okr id="okr_xxx">
  <objective id="obj_1">
    <kr id="kr_1"/>
  </objective>
</okr>
```

### Inline elements

```html
<mention-user id="ou_xxx"/>
```

```html
<mention-doc token="doxcnXXX" type="docx">Document title</mention-doc>
```

```html
<reminder date="2025-12-31T18:00+08:00" notify="true" user-id="ou_xxx"/>
```

### Math formulas

````markdown
$$
\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
````

Inline formula:

```markdown
Einstein's equation: $E = mc^2$ (note that spaces are required before and after $, and there must be no spaces immediately adjacent to it)
```

## References

- [lark-doc](../SKILL.md) — All Docs operations
- [lark-doc-update](lark-doc-update.md) — Update document content
- [lark-shared](../../lark-shared/SKILL.md) — Authentication and global parameters
