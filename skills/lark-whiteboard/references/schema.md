# DSL Schema

> Frame's layout system is based on the Yoga engine, and its behavior is basically the same as CSS Flexbox. `layout: 'horizontal'` = `flex-direction: row`, `fill-container` = `flex: 1`, `fit-content` = `width: auto`, `gap` / `padding` / `alignItems` / `justifyContent` have the same semantics. Use `'start'`/`'end'` instead of `'flex-start'`/`'flex-end'` for enumeration values. **Note the difference**: The default value of `alignItems` is `'start'` (CSS default `stretch`). When you need equal height cards, you must explicitly write `alignItems: 'stretch'`.

## WBDocument

```typescript
interface WBDocument {
  version: 2;
  nodes: WBNode[]; // Top-level node. connector must be placed here and cannot be nested in children
}
```

## Node type

### Frame (container)

The only type that can contain child nodes. Used for grouping, layout, background.

```typescript
{
  type: 'frame';
  id?: string;
  x?: number; y?: number; // Flex child nodes do not need x/y
  width: WBSizeValue;
  height: WBSizeValue;

  layout: 'horizontal' | 'vertical' | 'none'; // Must be written, otherwise the default is absolute positioning
  gap: number; // Must be written explicitly (if not written, the node will be sticky and prone to bugs)
  padding: number | [number, number] | [number, number, number, number]; // Must be written explicitly (no content padding)
  justifyContent?: 'start' | 'center' | 'end' | 'space-between' | 'space-around';
  alignItems?: 'start' | 'center' | 'end' | 'stretch';
  fillColor?: string;
  borderColor?: string;
  borderWidth?: number;
  borderDash?: 'solid' | 'dashed' | 'dotted';
  borderRadius?: number;
  children?: WBNode[]; // Cannot contain connector
}
```

> **Virtual frame trap**: frames with no title, no fillColor, no borderColor, and no borderWidth will be skipped during compilation (child nodes are directly promoted to the parent). If you set an ID for this kind of virtual frame and use a connector to connect it, the frame will disappear after compilation and the connector reference will become invalid. Solution: Add `borderWidth: 0` or any visible attribute to frame to prevent it from being optimized away.

### Basic graphics

```typescript
{
  type: 'rect' | 'ellipse' | 'cylinder' | 'diamond' | 'triangle' | 'trapezoid';
  id?: string;
  x?: number; y?: number;
  opacity?: number; // 0-1, only affects the transparency of fillColor (invalid for frame/text/stickyNote)
  vFlip?: boolean;
  hFlip?: boolean;
  width: WBSizeValue;
  height: WBSizeValue;
  fillColor?: string;
  borderColor?: string;
  borderWidth?: number;
  borderDash?: 'solid' | 'dashed' | 'dotted';
  borderRadius?: number;
  topWidth?: number; // Only valid for triangle / trapezoid, trapezoid top width or triangle corner truncated width
  text?: string | WBTextRun[]; // Plain text or rich text
  fontSize?: number;
  textColor?: string;
  textAlign?: 'left' | 'center' | 'right'; // Shape defaults to 'center' (different from CSS)
  verticalAlign?: 'top' | 'middle' | 'bottom'; // Shape defaults to 'middle' (unlike CSS)
}
```

> **cylinder constraints**: The arc of the cylinder is fixed at 16px and does not scale with the width. If the width is too large, it will become an oblate ellipse. `width: "fill-container"` is prohibited, fixed width + `height: "fit-content"` must be used. The width is chosen based on the text length, usually 120-200px.

> **Shape padding (TEXT_INSET)**: The Shape node has forced padding, and fit-content will automatically compensate.
> - rect/ellipse/diamond/triangle: 12px each for top, bottom, left and right
> - cylinder: top arc 32px + bottom arc 10px (vertical +42px), horizontal 7px each
>
> When a fixed size needs to be calculated by hand: `actual text width/height + corresponding inset`.
> Example: 14px font size in rect, two lines of text height ~32px → `height >= 32 + 24 = 56px`

### Text (plain text node)

```typescript
{
  type: 'text';
  id?: string;
  x?: number; y?: number;
  width: WBSizeValue;
  height: WBSizeValue;
  text?: string | WBTextRun[];
  fontSize?: number;
  textColor?: string;
  textAlign?: 'left' | 'center' | 'right';
  verticalAlign?: 'top' | 'middle' | 'bottom';
}
```

### StickyNote (sticky notes)

```typescript
{
  type: 'stickyNote';
  id?: string;
  x?: number; y?: number;
  width: WBSizeValue;
  height: WBSizeValue;
  fillColor?: '#FEF1CE' | '#F5D1A7' | '#DFF5E5' | '#CDF7CC' | '#C9E8EF' | '#D6DCF3' | '#D3CCEE' | '#F1C5E7' | '#F6C8C8'; // Note background color (only these 9 types are supported)
  text?: string | WBTextRun[];
  fontSize?: number;
  textColor?: string;
  textAlign?: 'left' | 'center' | 'right';
  verticalAlign?: 'top' | 'middle' | 'bottom';
}
```

### Connector

Must be placed in the top-level `nodes` array and cannot be nested in the `children` of the frame.

```typescript
{
  type: 'connector';
  id?: string;
  connector: {
    from: string | { x: number; y: number }; // Node id or coordinates
    to:   string | { x: number; y: number };
    fromAnchor?: 'top' | 'right' | 'bottom' | 'left';
    toAnchor?:   'top' | 'right' | 'bottom' | 'left';
    lineShape?: 'straight' | 'polyline' | 'curve' | 'rightAngle'; // Straight line, rounded polyline, curve, right-angled polyline
    lineColor?: string;
    lineWidth?: number;
    lineStyle?: 'solid' | 'dashed' | 'dotted';
    startArrow?: 'none' | 'arrow' | 'triangle' | 'circle' | 'diamond';
    endArrow?:   'none' | 'arrow' | 'triangle' | 'circle' | 'diamond';
    label?: string; // Label text in the middle of the connection
    waypoints?: { x: number; y: number }[]; // polyline waypoints
    label?: string; // Label text in the middle of the connection
    labelPosition?: number; // Label position, 0-1, default 0.5 (midpoint)
  };
}
```

### SVG

```typescript
{
  type: 'svg';
  id?: string;
  x?: number; y?: number;
  opacity?: number;
  width: WBSizeValue;
  height: WBSizeValue;
  svg: { code: string }; // SVG code string
}
```

#### Rendering specification

SVG is loaded into the canvas via an `image/svg+xml` Blob, which is not in the HTML DOM, so there are strict limitations:

**must**:
- Contains the `viewBox` attribute (e.g. `viewBox="0 0 24 24"`), which the engine relies on to determine the coordinate system
- Contains `xmlns="http://www.w3.org/2000/svg"` (the XML specification requires a namespace declaration when SVG is parsed as a standalone `image/svg+xml`)

**Allowed elements** (Pure geometry drawing):
- Basic graphics: `<rect>` `<circle>` `<ellipse>` `<line>` `<polyline>` `<polygon>` `<path>`
- Gradient/Filter: `<defs>` `<linearGradient>` `<radialGradient>` `<filter>` `<feGaussianBlur>` `<feMerge>`
- Structure: `<g>` `<clipPath>` `<mask>` `<use>`

**Forbidden Elements** (Fonts and external resources cannot be loaded in the Blob sandbox):
- `<text>` `<tspan>` (replaced by the same layer DSL rect node + text attribute)
- `<image>` (replaced by DSL image node of the same layer)
- `<foreignObject>`
- Any attribute that refers to an external URL (`xlink:href` points to a remote resource, etc.)

#### Two typical usages

**1. Background decoration SVG** (large size, same size as frame)

Used to draw geometric backgrounds such as lines, curves, and glow effects. Text information is superimposed through rect nodes in the same frame:

```json
{
  "type": "frame", "width": 1400, "height": 680, "layout": "none",
  "children": [
    { "type": "svg", "x": 0, "y": 0, "width": 1400, "height": 680,
      "svg": { "code": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1400 680\" ...>...</svg>" } },
    { "type": "rect", "x": 100, "y": 50, "width": 200, "height": 40,
      "text": "Label", "fillColor": "transparent" }
  ]
}
```

**2. Inline icon SVG** (24-48px, Feather/Lucide style)

Used for small icons in cards/buttons, pure stroke lines:

```json
{ "type": "svg", "width": 32, "height": 32,
  "svg": { "code": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#3B82F6\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><polyline points=\"12 6 12 12 16 14\"/></svg>" } }
```

---

## Rich text WBTextRun

The `text` field can be a plain string or a `WBTextRun[]` array. Similar to HTML inline styles: bold corresponds to `<b>`, italic corresponds to `<i>`, and listType corresponds to `<ol>/<ul>`. Each run is a styled text:

```typescript
interface WBTextRun {
  content: string; // Text content, may contain \n newline
  bold?: boolean;
  italic?: boolean;
  underline?: boolean;
  strikeThrough?: boolean;
  fontSize?: number;
  color?: string; // text color
  backgroundColor?: string; // Text highlight background
  hyperlink?: string;
  listType?: 'none' | 'ordered' | 'unordered';
  indent?: number; // indentation level
  quote?: boolean; // quote block
}
```

Example:

```json
{
  "text": [
    { "content": "Title text\n", "bold": true, "fontSize": 16 },
    { "content": "Text content,", "fontSize": 14 },
    { "content": "highlighted part", "backgroundColor": "#FEF1CE", "fontSize": 14 }
  ]
}
```

Double quotes appearing in `text` and `content` must be written as `\"`, which is required by the JSON specification. Use `\n` for line breaks (written as `"first line\nsecond line"` in JSON, do not double escape as `\\n`).

---

## Size value WBSizeValue

| Value | Meaning | Notes |
|----|------|------|
| `number` | fixed pixels | any scene |
| `'fit-content'` | Size determined by content | Parent requires Flex layout |
| `'fit-content(N)'` | Same as above, fallback N when there is no content | Same as above |
| `'fill-container'` | Fill the remaining space of the parent | The parent requires Flex layout and the ancestor chain has a fixed width |
| `'fill-container(N)'` | Same as above, fallback N without Flex | — |

`fill-container` has no effect with `layout: 'none'` (absolute positioning). `fit-content` can still be used for nodes with text (the engine measures text size via Yoga measureFunc).
