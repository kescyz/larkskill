# Layout system

## Layout decisions

> Don’t guess the layout based on keywords. Analyze the information structure first, and then decide on the layout strategy.

| Judgment conditions | Layout strategy |
|----------|----------|
| Elements have clear upper and lower levels (user layer → service layer → data layer) | **Flex layering** |
| Spatial location carries information (geographical orientation, topological coordinates, angle) | **Pure absolute positioning** (script calculated coordinates) |
| Multiple independent modules are interconnected horizontally, without superior or subordinate | **Hybrid layout (island style)** |
| Unsure | **Default Flex Layering** (most secure) |

| Layout Strategy | Applicable Charts |
|----------|----------|
| Pure absolute positioning | Fishbone diagram, bar chart, line chart, topology map, map route |
| Flex skeleton | Architecture hierarchy diagram, card wall, organization chart, comparison table |
| Hybrid (island type) | System integration diagram, flywheel diagram, flow chart |

**Read the code and draw the architecture diagram**: Scan the directory structure (by layer → Flex; by functional module → look at the dependency direction) → grep import (one-way → Flex; mesh → hybrid) → not sure → default to Flex.

> `x/y` inside **flex container will be completely ignored! **

❌ Fatal error:
```json
{ "type": "frame", "layout": "vertical", "children": [
  { "type": "rect", "x": 100, "y": 0, "text": "Chengdu" },
  { "type": "rect", "x": 540, "y": 0, "text": "Kangding" }
]}
```
✅ Correct: use `layout: "none"` or put it on top nodes and use x/y.

**Build method**:

| Layout type | How to do |
|----------|------|
| Pure Flex | Write JSON directly |
| Mixed layout | Write JSON directly + estimation assistance |
| Pure absolute positioning | Write a script to generate JSON (node ​​xxx.js) |
| Need precise avoidance | Script + `--layout` two phases |

---

## Grid Methodology

Core concept: **Draw the grid first, then fill in the content**.

Answer three questions first:
1. **How ​​many rows and columns is the information divided into? ** One row or column per group
2. **How ​​big is each grid? ** Equal width or primary and secondary?
3. **How ​​big is the distance between rows and columns? ** 24-32px between partitions, 12-16px within the same area

---

## Layout mode selection

| Mode | Applicable Scenario | DSL Mapping |
|------|---------|---------|
| grid | architecture diagram, comparison table, card wall, billboard | vertical frame nested horizontal frame |
| flow | flow chart, approval flow | vertical frame, the main process is centered |
| tree | Organizational structure, module dependencies | The root node is centered and the child nodes are expanded horizontally |
| free | system integration, topology diagram, fishbone diagram | `layout: "none"` + x/y |

Most charts use grid mode. Use free only when the node position itself has meaning.

> The above are layout strategy names, not the `layout` attribute value of DSL. DSL layout only supports three types: `'horizontal'`, `'vertical'`, and `'none'`.

---

## DSL and CSS Flexbox property mapping

| DSL properties | Corresponding CSS mental model | Limitations |
|-----------------------|-----------------------------------|--------|
| `layout: 'horizontal'` | `flex-direction: row` | Do not write layout = absolute positioning |
| `layout: 'vertical'` | `flex-direction: column` | Same as above |
| `layout: 'none'` | `position: absolute` (use x/y for child nodes) | `fill-container` cannot be used for child nodes |
| `width/height: 'fill-container'` | `flex: 1` (main axis) / `align-self: stretch` (cross axis) | Ancestor must have definite size |
| `width/height: 'fit-content'` | `width/height: auto` | — |
| `alignItems` | Same as CSS `align-items` | Only `'start'`/`'center'`/`'end'`/`'stretch'` (without flex- prefix) |
| `justifyContent` | Same as CSS `justify-content` | Only `'start'`/`'center'`/`'end'`/`'space-between'`/`'space-around'` |
| `gap` | Same as CSS `gap` | Must be written explicitly (nodes will be sticky if not written) |
| `padding` | Same as CSS `padding` | Must be written explicitly. Support `number` / `[v,h]` / `[t,r,b,l]` |

The default value of `alignItems` is `'start'` (CSS Flexbox default `stretch`). When cards of equal height are required, `alignItems: 'stretch'` must be written explicitly.

The syntax of the DSL is a strict whitelist, and native CSS properties cannot be written (`alignSelf`, `flexWrap`, `margin`, etc. are not supported).

---

## DSL Notes

1. **Frame must write layout attribute**. If not written, all child nodes will be piled in the upper left corner.
2. **fill-container deadlock trap**: When using `fill-container`, there must be a fixed width (or height) in the ancestor chain, otherwise it will form a deadlock with `fit-content` and the size will degenerate to 0.
   ```json
   // Deadlock: horizontal parent width fit-content + child width fill-container
   { "type": "frame", "layout": "horizontal", "width": "fit-content", "children": [
     { "type": "rect", "width": "fill-container" }
   ]}
   // Correct: the ancestor has a fixed size on the corresponding axis
   { "type": "frame", "layout": "horizontal", "width": 1200, "children": [
     { "type": "rect", "width": "fill-container" }
   ]}
   ```
3. **Use fit-content** to specify the height of text nodes. The engine does not support overflow. If the height is hard-coded, the text will be truncated.
4. **Shape nodes have padding**: rect/ellipse/diamond/triangle 12px on each side; cylinder vertical +42px.
5. **Does not support flex-wrap**, use nested frames to simulate line breaks.
6. **Layer Order**: The nodes further back in the array have higher levels. When overlapping labels are required, place them at the end of the array.

---

## Layout Selection Guide

| The relationship you want to express | How to arrange | DSL writing method |
|-------------|-------|---------|
| Sequence, level from top to bottom | Vertical stacking | `layout: 'vertical'` |
| Parallel, equally important, comparable | Horizontal equal division | `layout: 'horizontal'` + `alignItems: 'stretch'` + `width: 'fill-container'` |
| The area has a name, and the name is on the side | Side label + content side by side | Horizontal frame: [text(label), frame(content)] |
| Multiple large partitions, each independent | Partitions arranged vertically | Vertical frame includes multiple color frames |
| Can’t fit in one line and needs to be wrapped | Nested horizontal frames simulate line breaks | Vertical frames include multiple horizontal frames |
| The node position itself has meaning (topology, map) | Absolute positioning | `layout: 'none'` + x/y |

These can be freely nested and combined. For example: vertical stacking (title) + vertical arrangement of partitions (multiple layers) + horizontal divisions (nodes) within each layer.

---

## Layout example

### Vertical stacking (title + content)

```json
{
  "type": "frame", "layout": "vertical", "gap": 28, "padding": 32,
  "width": 1200, "height": "fit-content",
  "children": [
    { "type": "text", "width": "fill-container", "height": "fit-content",
      "text": "Chart title", "fontSize": 24, "textAlign": "center" },
    ...content...
  ]
}
```

### Horizontal equal division (parallel elements)

```json
{
  "type": "frame", "layout": "horizontal", "gap": 16, "padding": 0,
  "width": "fill-container", "height": "fit-content",
  "alignItems": "stretch",
  "children": [
    { "type": "rect", "width": "fill-container", "height": "fit-content",
      "textAlign": "center", "verticalAlign": "middle", "text": "A" },
    { "type": "rect", "width": "fill-container", "height": "fit-content",
      "textAlign": "center", "verticalAlign": "middle", "text": "B" }
  ]
}
```

`alignItems: 'stretch'` + `width: 'fill-container'` = equal width and equal height.

### Side tag + content

```json
{
  "type": "frame", "layout": "horizontal", "gap": 24, "padding": 0,
  "width": "fill-container", "height": "fit-content",
  "alignItems": "center",
  "children": [
    { "type": "text", "width": 160, "height": "fit-content",
      "text": "Area Name", "fontSize": 20, "textColor": "#1F2329", "textAlign": "right" },
    { "type": "frame", "width": "fill-container", "height": "fit-content",
      ...area content...
    }
  ]
}
```

Do not use the `title` attribute of the frame as a label - it will be rendered as a very small title bar and unreadable.

### Partitions arranged vertically

Divide the content into several large areas, and distinguish each area with a different color (the color is selected from the color palette of the style file):

```json
{
  "type": "frame", "layout": "vertical", "gap": 28, "padding": 0,
  "width": "fill-container", "height": "fit-content",
  "children": [
    { "type": "frame", "borderRadius": 8,
      "layout": "horizontal", "gap": 16, "padding": 20, ...area 1... },
    { "type": "frame", "borderRadius": 8,
      "layout": "horizontal", "gap": 16, "padding": 20, ...area 2... }
  ]
}
```

### Simulate newline

When one line cannot fit, split it into multiple horizontal frames:

```json
{
  "type": "frame", "layout": "vertical", "gap": 8, "padding": 0,
  "children": [
    { "type": "frame", "layout": "horizontal", "gap": 8, "padding": 0,
      "children": [item1, item2, item3, item4] },
    { "type": "frame", "layout": "horizontal", "gap": 8, "padding": 0,
      "children": [item5, item6] }
  ]
}
```

---

## Absolute positioning

Use absolute positioning when the node position itself has meaning (topology diagram, map, timeline axis). Flex is preferred for most charts.

### Mixed layout

Flex is used for automatic typesetting inside the module, and absolute positioning is used between modules to freely place them. Each module is a flex frame with x/y:

```json
{
  "type": "frame", "id": "module-a", "x": 100, "y": 100,
  "width": 300, "height": "fit-content",
  "layout": "vertical", "gap": 8, "padding": 16,
  "children": [
    { "type": "rect", "width": "fill-container", "height": "fit-content", "text": "content1" },
    { "type": "rect", "width": "fill-container", "height": "fit-content", "text": "content2" }
  ]
}
```

### Two-stage drawing

First, export the coordinates from the skeleton diagram, and then add connections and annotations based on the coordinates:

```bash
npx -y @larksuite/whiteboard-cli@^0.1.0 -i skeleton.json -o step1.png -l coords.json
```

`coords.json` contains the exact coordinates (absX, absY, width, height) of each node with id.

---

## Common spacing and dimensions

| Parameters | Common ranges | Description |
|------|---------|------|
| Whole image width | 1000-1400px | — |
| Spacing between partitions | 24-32px | — |
| Spacing between nodes in the same partition | 12-16px | — |
| Spacing between connected nodes | >= 40px | Leave space for arrows |
| Section padding | 16-24px | — |
| side label width | 120-180px | — |

---

## and other large cards

When a row of cards needs to be of equal width and height, do not write fixed pixels:

```json
{
  "type": "frame", "layout": "horizontal", "gap": 16, "padding": 0,
  "alignItems": "stretch",
  "children": [
    { "type": "rect", "width": "fill-container", "height": "fit-content", "text": "A" },
    { "type": "rect", "width": "fill-container", "height": "fit-content", "text": "B" }
  ]
}
```

`alignItems: 'stretch'` + `width: 'fill-container'` = equal width and equal height.
