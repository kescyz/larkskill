# Pyramid

## Content constraints

- 3-6 levels, decreasing width from bottom to top
- One short tag (such as a keyword or phrase) per layer
- The long copy is placed outside the pyramid, and only the core short copy is retained in the graphic.

## Layout selection

vertical frame + width decreases with each layer. gap 4px to keep it tight.

## Layout rules

- The outer frame uses `layout: "vertical"` + `alignItems: "center"`
- All layers must use a script to calculate the width to guarantee **absolutely perfect equal slopes (straight edges)**. Never write by hand the width of your head!
- The first element in the children array is the top level (narrowest), and the last element is the bottom level (widest).
- Usually use `triangle` (`topWidth: 0`) for the top layer, and `trapezoid` for the middle and bottom layers.
- The gap is usually set to 4px to maintain a tight pyramid feel.

> **strict slope algorithm (must be implemented in script)**:
> For the sides of the pyramid to form a perfect straight line, the increment in width must be strictly tied to the height and gap**.
> 1. Set the overall width expansion coefficient `angleK` (recommended value 1.5 to 2.5, indicating the number of pixels the total width increases for every 1px increase in height).
> 2. The formula for the bottom width of the current layer: `width = topWidth + (height * angleK)`
> 3. The top width formula of the next layer (the additional expansion caused by gap must be considered): `nextTopWidth = width + (gap * angleK)`

## Script build template

You must use `node` to run the script to generate JSON.

```javascript
import fs from 'fs';

// 1. Configure basic parameters
const GAP = 4;
const ANGLE_K = 2; // Slope coefficient: for every 1px increase in height, the width increases by 2px
const LAYER_HEIGHT = 80;

const data = [
  { text: "Top Core", fillColor: "#1F2329", textColor: "#FFFFFF" },
  { text: "Middle layer B", fillColor: "#DFF5E5", textColor: "#1F2329" },
  { text: "Middle layer A", fillColor: "#EAE2FE", textColor: "#1F2329" },
  { text: "The lowest foundation", fillColor: "#F0F4FC", textColor: "#1F2329" }
];

let currentTopWidth = 0; // If the top layer is a sharp corner, it is initially 0
const children = data.map((layer, index) => {
  // 2. Calculate the bottom width of the current layer according to the formula
  const currentBottomWidth = currentTopWidth + (LAYER_HEIGHT * ANGLE_K);
  
  const node = {
    type: currentTopWidth === 0 ? "triangle" : "trapezoid",
    width: currentBottomWidth,
    topWidth: currentTopWidth,
    height: LAYER_HEIGHT,
    text: layer.text,
    textAlign: "center",
    fillColor: layer.fillColor,
    borderColor: layer.fillColor,
    borderWidth: 2,
    fontSize: 16,
    textColor: layer.textColor
  };

  // 3. Key: Calculate the top width of the next layer. The extension of the gap must be taken into account!
  currentTopWidth = currentBottomWidth + (GAP * ANGLE_K);
  
  return node;
});

const output = {
  version: 2,
  nodes: [
    {
      type: "frame",
      layout: "vertical",
      alignItems: "center",
      gap: GAP,
      padding: 40,
      children: children
    }
  ]
};

fs.writeFileSync('pyramid.json', JSON.stringify(output, null, 2));
```

## trap

- **Don't handwrite randomly increasing widths**: This will cause the sides of the pyramid to become folded lines, not straight. The above `angleK` formula calculation must be strictly used.
- **Forgot to calculate the expansion caused by the gap**: If the `topWidth` of the next layer is simply equal to the `width` of the previous layer, if there is a gap, jagged corners will occur at the connection. `gap * angleK` must be added.
- **Arrangement error from top to bottom**: The first one in the children array is the top layer (narrowest), the last one is the bottom layer (widest), and the width increases in sequence.
- **Text overflows top-level triangle**: There is very little space available inside the top-level triangle. Use `\n` for short copy to manually wrap; long copy is externally placed next to the pyramid (the outer layer is covered with a horizontal frame, on the left side of the pyramid, on the right side of the description text)
- **Inverted pyramid misuse**: If the user requests "inverted pyramid", "funnel chart" or "top-down decreasing structure", **do not** use this file, switch to `scenes/funnel.md`

## Extension

- **Auxiliary explanation**: When you need to add a text explanation next to it, put a `layout: "horizontal"` frame on the outermost layer, put the pyramid on the left, and put the explanatory text (vertical arranged text node) on the right
- **Color matching**: The color of each layer should be selected from the color palette to show distinction (such as blue → purple → green → yellow in progress)
