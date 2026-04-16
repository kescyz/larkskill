# Rectangular treemap (Treemap)

## Content constraints

- 3-5 categories, 2-4 sub-items under each category
- The total area ratio needs to be calculated in advance: area of ​​each rectangle = area of ​​parent rectangle * (value of this item / total value of the same level)
- Each leaf node label must contain a numerical value (such as "{{LABEL}} ({{VALUE}})")

## Layout selection

- **Script generated coordinates** (recommended): Treemap requires accurate area ratio calculation, use .js script to recursively divide the rectangle, and call `npx -y @larksuite/whiteboard-cli@^0.1.0` after the script outputs the JSON file for rendering.
- Not suitable for manual mental calculation of coordinates

## Layout rules

- Use alternating slice method (Slice-and-Dice): odd-numbered layers are sliced ​​horizontally by width, even-numbered layers are sliced ​​vertically by height
- 30-40px top space must be reserved for the title within the parent rectangle, and the child rectangle is placed starting from y + 35
- Child nodes must fall completely within the scope of the parent rectangle
- When splitting horizontally: child width = parent width * (child value / parent total value), child x is accumulated sequentially
- When split vertically: child height = (parent height - 35) * (child value / parent total value), child y is accumulated in sequence (note that the 35px reserved by the parent tag is deducted)

### Area ratio calculation rules

1. **The area is strictly proportional to the numerical value**: The rectangular area `width * height` of a node at any level must be proportional to the numerical value
2. **Odd-numbered horizontal segmentation** (such as the first level classification):
- The `height` and `y` coordinates of the parent rectangle are passed to all child nodes (after deducting the label reserved space)
- Split the `width` of the parent rectangle according to the ratio of the child node value to the parent node: `child width = parent width * (child value / total parent value)`
- The `x` coordinates of child nodes are accumulated to the right in sequence.
3. **Vertical splitting of even-numbered layers** (such as second-layer sub-items):
- The `width` and `x` coordinates of the parent rectangle are passed to all child nodes
- Split the `height` of the parent rectangle according to the ratio of the child node value to the parent node: `child height = parent height * (child value / total parent value)`
- The `y` coordinates of child nodes are accumulated downwards in sequence.
4. **Layer-by-layer recursion**: Continuously alternate horizontal and vertical splitting directions until all leaf nodes are assigned precise coordinates, width and height

### Reserve space for parent tag

30-40px must be reserved at the top of the rectangle of each non-leaf node to place the category label. The child rectangle is placed starting from `y + 35` of the parent rectangle, and the available height is `parent height - 35`.

Example: parent rectangle `{ x: 40, y: 40, height: 700 }`, then:
- The parent tag is placed at `y: 46` (leave 6px top margin)
- Subrectangles are placed starting from `y: 75` (40 + 35)
- The available height of the sub-rectangle is `700 - 35 = 665`

## Skeleton example

2-layer treemap: 3 categories (Hardware 40, Software 35, Services 25), each containing 2 sub-items.

The root rectangle is 1100x700, the first layer is divided horizontally by width, and the second layer is divided vertically by height.

```json
{
  "version": 2,
  "nodes": [
    {
      "type": "rect",
      "id": "root",
      "x": 40, "y": 40,
      "width": 1100, "height": 700,
      "borderWidth": 2, "borderRadius": 6
    },
    {
      "type": "text",
      "x": 48, "y": 46,
      "width": 1084, "height": 24,
      "text": "{{ROOT_TITLE}}",
      "fontSize": 14
    },

    {
      "type": "rect",
      "id": "cat-A",
      "x": 40, "y": 75,
      "width": 440, "height": 665,
      "borderWidth": 2, "borderRadius": 6
    },
    {
      "type": "text",
      "x": 48, "y": 81,
      "width": 424, "height": 24,
      "text": "{{CAT_A}}",
      "fontSize": 14
    },
    {
      "type": "rect",
      "id": "cat-A-item-1",
      "x": 40, "y": 110,
      "width": 440, "height": 380,
      "borderRadius": 4
    },
    {
      "type": "text",
      "x": 48, "y": 116,
      "width": 424, "height": 24,
      "text": "{{ITEM_A1}} (24)",
      "fontSize": 14
    },
    {
      "type": "rect",
      "id": "cat-A-item-2",
      "x": 40, "y": 490,
      "width": 440, "height": 250,
      "borderRadius": 4
    },
    {
      "type": "text",
      "x": 48, "y": 496,
      "width": 424, "height": 24,
      "text": "{{ITEM_A2}} (16)",
      "fontSize": 14
    },

    {
      "type": "rect",
      "id": "cat-B",
      "x": 480, "y": 75,
      "width": 385, "height": 665,
      "borderWidth": 2, "borderRadius": 6
    },
    {
      "type": "text",
      "x": 488, "y": 81,
      "width": 369, "height": 24,
      "text": "{{CAT_B}}",
      "fontSize": 14
    },
    {
      "type": "rect",
      "id": "cat-B-item-1",
      "x": 480, "y": 110,
      "width": 385, "height": 380,
      "borderRadius": 4
    },
    {
      "type": "text",
      "x": 488, "y": 116,
      "width": 369, "height": 24,
      "text": "{{ITEM_B1}} (20)",
      "fontSize": 14
    },
    {
      "type": "rect",
      "id": "cat-B-item-2",
      "x": 480, "y": 490,
      "width": 385, "height": 285,
      "borderRadius": 4
    },
    {
      "type": "text",
      "x": 488, "y": 496,
      "width": 369, "height": 24,
      "text": "{{ITEM_B2}} (15)",
      "fontSize": 14
    },

    {
      "type": "rect",
      "id": "cat-C",
      "x": 865, "y": 75,
      "width": 275, "height": 665,
      "borderWidth": 2, "borderRadius": 6
    },
    {
      "type": "text",
      "x": 873, "y": 81,
      "width": 259, "height": 24,
      "text": "{{CAT_C}}",
      "fontSize": 14
    },
    {
      "type": "rect",
      "id": "cat-C-item-1",
      "x": 865, "y": 110,
      "width": 275, "height": 399,
      "borderRadius": 4
    },
    {
      "type": "text",
      "x": 873, "y": 116,
      "width": 259, "height": 24,
      "text": "{{ITEM_C1}} (15)",
      "fontSize": 14
    },
    {
      "type": "rect",
      "id": "cat-C-item-2",
      "x": 865, "y": 509,
      "width": 275, "height": 231,
      "borderRadius": 4
    },
    {
      "type": "text",
      "x": 873, "y": 515,
      "width": 259, "height": 24,
      "text": "{{ITEM_C2}} (10)",
      "fontSize": 14
    }
  ]
}
```

Area proportion verification (first layer horizontal split width):
- Hardware 40/100 * 1100 = 440, software 35/100 * 1100 = 385, service 25/100 * 1100 = 275
- Subrectangle starts at y=75, available height 665

**How ​​to run the script**:

```bash
node generate-treemap.js
npx -y @larksuite/whiteboard-cli@^0.1.0 -i treemap.json -o ./treemap.png
```

## trap

- **Parent label is obscured by child rectangle** (most severe): child rectangle must be placed starting from y + 35 (relative to the top of parent rectangle) to leave space for parent category label
- **Category label is not visible**: The classification label text node must be added before its sub-rectangular rect node (nodes with lower z-index are in the upper layer)
- **Incorrect area proportions**: Proportions must be pre-calculated using a script, no mental arithmetic
- **Lack of color distinction**: Different top-level categories must use different background colors (selected from the color palette), and all child nodes inherit the corresponding color system
