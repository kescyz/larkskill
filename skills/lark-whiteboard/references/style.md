# color matching system

## How to color (the most important thing)

Coloring steps:

1. **Find out how many groups there are in the diagram** (level, branch, category, stage...)
2. **Choose a different color for each group** (choose 2-4 colors from the color palette)
3. Fill the **Group Container** with a light color — tell the reader "this area is a whole"
4. **Nodes within the group** are filled with white + the dark borderColor of the group — telling readers "these belong to this group"

Specific mapping (classic color palette):

| Grouping | Layer container fillColor | Layer container borderColor | Internal node borderColor |
|------|----------------|-------------------|---------------------|
| Group 1 | #F0F4FC (Light Blue) | #5178C6 | #5178C6 |
| Group 2 | #EAE2FE (Light Purple) | #8569CB | #8569CB |
| Group 3 | #DFF5E5 (Light Green) | #509863 | #509863 |
| Group 4 | #FEF1CE (light yellow) | #D4B45B | #D4B45B |
| Group 5 | #FEE3E2 (light red) | #D25D5A | #D25D5A |
| Internal node | #FFFFFF | Follow the group it belongs to | — |

**How ​​to color various charts**:
- The architecture diagram has 3 layers → each layer has one color, the layer background is filled with light color, and the nodes within the layer are white + dark border
- The comparison table has 3 columns → each column header has a color, and the data cells in this column have the same color border
- The organizational structure has 4 departments → each department has a color, and the sub-departments are white + the same color border
- Flowchart → One color for start and end nodes, one color for judgment nodes, and white for step nodes

> [!IMPORTANT]
> **User color matching is given priority. ** When the user specifies the color value/style, the user shall prevail. When the user only gives 1-2 color values, the complete color palette is derived: main color → light base → dark border → gray tone connecting color.
> When the user **does not specify** the color matching, he must select the color from the color palette table above, and do not use self-created color values ​​that are not in the table (such as `#E8F3FF`, `#1664FF`, `#14C9C9`, etc. are not in the color palette).

---

## Structure rules

### Grouping — Different layers/groups must use different colors

Choose 2-4 colors, each representing a group. Nodes in the same group are visually identical (the fillColor and borderColor are the same).

### Layered - heavy on the outside and light on the inside

- Outer layer (large partition): light filled background
- Inner layer (specific node): white fill + group color border

### Clear

- All nodes have borders (borderWidth=2)
- The gap is not sticky (gap >= 8, when there is a connection >= 40)
- Text is clearly readable on the background (fontSize >= 14). The contrast between text and background color should be sufficient (refer to WCAG 2.1: at least 4.5:1 for main text and at least 3:1 for titles)
- Don’t rely on color alone to differentiate information—use borders, shapes, or text labels to help make sure users with color vision impairments can understand it as well.
- Use gray (#BBBFC4) for connections to avoid grabbing the attention of nodes.

### Unified parameters

| Parameter | Value | Why |
|------|---|--------|
| borderWidth | 2 | Make the border clearly visible |
| borderRadius | 8 | Uniform rounded corners, neat |
| gap (minimum value) | 8 | elements are not sticky |
| padding (minimum value) | 8 | content will not fit |
| gap (when connected) | 40 | Leave space for arrows |
| fontSize(text) | >= 14 | Readable |
| fontSize(title) | >= 24 | Eye-catching |
| fontSize (auxiliary) | >= 13 | Easy on the eyes |

---

## Color Swatch Selection Guide

Choose the appropriate color palette based on the keywords or scenes that the user needs. Defaults to the "Classic" color palette when not specified.

| Color palette | Applicable scenarios | Keywords |
|------|---------|-------|
| Classic | General charts, documentation | Default, general |
| Business | Reporting, corporate structure, formal documents | Professional, formal, showing to the boss |
| Technology | Technical architecture, DevOps, monitoring | Technology, cool, dark colors |
| Fresh | Flowcharts, user journeys, tutorials | Fresh, natural, and easy |
| Minimalist | Paper illustrations, academic reports | Academic, minimalist, black and white |

---

## Default color palette

Each set of swatches defines the colors of 7 characters. **The connecting color is part of the color palette**, and different color palettes have different connecting colors.

### Classic

| role | fillColor | borderColor | textColor |
|------|-----------|-------------|-----------|
| Partition Background | #F0F4FC | #5178C6 | #1F2329 |
| Group title | #EAE2FE | #8569CB | #1F2329 |
| Content Node | #FFFFFF | #5178C6 | #1F2329 |
| Second Group | #DFF5E5 | #509863 | #1F2329 |
| Third Group | #FEF1CE | #D4B45B | #1F2329 |
| Group 4 | #FEE3E2 | #D25D5A | #1F2329 |
| Emphasis/Header | #1F2329 | #1F2329 | #FFFFFF |
| Wired | -- | -- | #BBBFC4 |

### Business

| role | fillColor | borderColor | textColor |
|------|-----------|-------------|-----------|
| Partition Background | #EDF2F7 | #4A6FA5 | #1A202C |
| Group title | #D4E0ED | #4A6FA5 | #1A202C |
| Content Node | #FFFFFF | #718BAE | #1A202C |
| Second Group | #E8EDF3 | #5A7B9A | #1A202C |
| The third group | #F0F0F0 | #8895A7 | #1A202C |
| Emphasis/Header | #2D4A7A | #2D4A7A | #FFFFFF |
| Wired | -- | -- | #718BAE |

### science and technology

| role | fillColor | borderColor | textColor |
|------|-----------|-------------|-----------|
| Canvas/Partition Background | #0F172A | #1E293B | #E2E8F0 |
| Group title | #1E293B | #3B82F6 | #E2E8F0 |
| Content Node | #1E293B | #334155 | #E2E8F0 |
| Second Group | #1E293B | #8B5CF6 | #E2E8F0 |
| The third group | #1E293B | #10B981 | #E2E8F0 |
| Highlight | #2563EB | #3B82F6 | #FFFFFF |
| Wired | -- | -- | #475569 |

### Fresh

| role | fillColor | borderColor | textColor |
|------|-----------|-------------|-----------|
| Partition Background | #F0FDF4 | #86EFAC | #14532D |
| Group title | #DCFCE7 | #4ADE80 | #14532D |
| Content Node | #FFFFFF | #86EFAC | #14532D |
| Second Group | #ECFDF5 | #6EE7B7 | #14532D |
| Third Group | #F0FDFA | #5EEAD4 | #134E4A |
| Highlight | #16A34A | #16A34A | #FFFFFF |
| Wired | -- | -- | #86EFAC |

### Minimalist

| role | fillColor | borderColor | textColor |
|------|-----------|-------------|-----------|
| Partition Background | #F8F9FA | #DEE2E6 | #212529 |
| Group title | #E9ECEF | #ADB5BD | #212529 |
| Content Node | #FFFFFF | #CED4DA | #212529 |
| Second Group | #F1F3F5 | #868E96 | #212529 |
| Third Group | #F8F9FA | #ADB5BD | #212529 |
| Emphasis/Header | #495057 | #495057 | #FFFFFF |
| Wired | -- | -- | #ADB5BD |

---

## How to draw each element

> The following examples use classic color palettes. If you select another color palette, just replace the corresponding color and the structure remains unchanged.

### Chart title

Tell the reader "What is this picture about?" Large dark text, centered.

```json
{ "type": "text", "fontSize": 24, "textColor": "#1F2329", "textAlign": "center" }
```

### Partition background

Circle related content together to tell readers "these belong to the same category." Use fillColor for light colors, and borderColor for dark colors. Place white nodes inside.

```json
{ "fillColor": "#F0F4FC", "borderColor": "#5178C6", "borderWidth": 2, "borderRadius": 8, "padding": 20 }
```

### Partition label

Give the partition a name. Use independent text nodes and do not use the `title` attribute of the frame (it will be rendered as a very small title bar).

**All partition labels use dark text `#1F2329`**. Do not use different colors for each label - the color distinction is reflected through the background and border of the layer container, and the color of the label text remains consistent.

```json
{ "type": "text", "width": 180, "height": "fit-content", "text": "Access layer", "fontSize": 20, "textColor": "#1F2329", "textAlign": "right" }
```

### Group title

Tell the reader "What is this subgroup called?" Swatch color fill + same color dark border.

```json
{ "fillColor": "#EAE2FE", "borderColor": "#8569CB", "borderWidth": 2, "borderRadius": 8, "fontSize": 14, "textColor": "#1F2329" }
```

### Content node

specific information items. White filling, border color follows the group it belongs to.

```json
{ "fillColor": "#FFFFFF", "borderColor": "#5178C6", "borderWidth": 2, "borderRadius": 8, "fontSize": 14, "textColor": "#1F2329" }
```

The borderColor of a white node depends on the group it belongs to:
```
Belongs to the blue group: fillColor="#FFFFFF" borderColor="#5178C6" borderWidth=2
Belongs to the purple group: fillColor="#FFFFFF" borderColor="#8569CB" borderWidth=2
Independent node: fillColor="#FFFFFF" borderColor="#DEE0E3" borderWidth=2
```
(Note: The above are the values ​​​​of the classic color palette, other color palettes replace the corresponding borderColor)

### Header

Tell the reader "what dimension is this column/row". Dark fill + white text.

```json
{ "fillColor": "#1F2329", "borderColor": "#1F2329", "borderWidth": 2, "borderRadius": 0, "fontSize": 15, "textColor": "#FFFFFF", "textAlign": "center" }
```

### textColor rules

```
- Text: #1F2329 (dark, clear on white/light background)
- Auxiliary explanation: #646A73 (weakened, not grabbing attention)
- On dark background: #FFFFFF (reverse color, clear and readable)
(The above are the values ​​​​of the classic color palette, other color palette references correspond to the textColor column)
```

### Auxiliary instructions

Supplementary information without stealing the protagonist’s attention. Small gray text.

```json
{ "fontSize": 13, "textColor": "#646A73" }
```

### Connect

Express the relationship or flow between elements. Use the connecting color from the color palette.

```json
{ "lineColor": "#BBBFC4", "lineWidth": 2 }
```

### Layout container

The frame is purely used for typesetting and is invisible to readers. There is no fillColor or borderColor.

```json
{ "type": "frame", "layout": "vertical", "gap": 28, "padding": 32 }
```

### Grouping container

Use a dotted box to enclose a group of nodes, which is more lightweight than a partition background.

```json
{ "borderColor": "#DEE0E3", "borderWidth": 2, "borderDash": "dashed", "borderRadius": 8 }
```

---

## Common mistakes

Error: One color for each node -> Readers can’t tell who is in a group with whom
```json
{ "fillColor": "#8569CB" }, { "fillColor": "#5178C6" }, { "fillColor": "#509863" }
```
Correct: Nodes in the same group are visually consistent -> readers can see the relationship at a glance
```json
{ "fillColor": "#FFFFFF", "borderColor": "#8569CB" }, { "fillColor": "#FFFFFF", "borderColor": "#8569CB" }
```

Error: Use heavy colors for both inner and outer layers -> Readers don’t know where to look first
```json
{ "type": "frame", "fillColor": "#5178C6", "children": [{ "fillColor": "#8569CB" }] }
```
Correct: light color on the outside and white on the inside -> readers look at the structure first and then look at the details
```json
{ "type": "frame", "fillColor": "#F0F4FC", "children": [{ "fillColor": "#FFFFFF", "borderColor": "#5178C6" }] }
```

Error: use the same color as the node for the connection -> grab attention with the node color
```json
{ "connector": { "lineColor": "#5178C6" } }
```
Correct: Use the connection color in the color palette for the connection -> set off the node
```json
{ "connector": { "lineColor": "#BBBFC4" } }
```

Error: Node has no border -> blends into the background and cannot see the border clearly
```json
{ "fillColor": "#FFFFFF" }
```
Correct: The node has a border -> the border is clear
```json
{ "fillColor": "#FFFFFF", "borderColor": "#DEE0E3", "borderWidth": 2 }
```

Error: The whole picture is black and white and gray, with no color distinction -> readers cannot quickly identify the groups
```json
{ "fillColor": "#FFFFFF", "borderColor": "#DEE0E3" }
```
Correct: use different colors for different groups -> see the structure at a glance (blue group + purple group)
```json
{ "fillColor": "#F0F4FC", "borderColor": "#5178C6" }
{ "fillColor": "#EAE2FE", "borderColor": "#8569CB" }
```
