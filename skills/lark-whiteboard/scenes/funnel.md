# Funnel chart

## Content constraints

- Stages 3-6
- One row of label + value per stage (e.g. "{{STAGE_NAME}} ({{PERCENTAGE}})")
- Keep the copy as short as possible; place the long copy next to the funnel, and keep only the core short copy in the graphics

## Layout selection

Absolute positioning. Use `trapezoid` / `triangle` nodes to arrange them from wide to narrow, and use `fit-content` for height.

## Layout rules

- The outer frame is centered using `layout: "vertical"` + `alignItems: "center"`
- All layers must use a script to calculate the width to guarantee **absolutely perfect equal slopes (straight edges)**. Never write by hand the width of your head!
- The gap between each layer is 0-8px (close stacking has good visual effect), and the width decreases from top to bottom. Note that the first element of the children array is the topmost (widest)
- All graphics nodes must be set to `"vFlip": false` (the engine flips upward by default, and the funnel needs to face downward)
- Note: Because `vFlip: false` and it is an inverted pyramid structure, `topWidth` actually controls the **narrower edge** of the bottom of each layer of the funnel. The bottom layer can be narrowed to a sharp corner with `triangle` (`topWidth: 0`), or it can be kept flat with `trapezoid`.

> **strict slope algorithm (must be implemented in script)**:
> To make the sides of the funnel form a perfect straight line, the decreasing width must be strictly linked to the height and gap**.
> 1. Set the overall width shrinkage coefficient `angleK` (recommended value 1.5 to 2.5, indicating the number of pixels the total width decreases for every 1px increase in height).
> 2. Because it becomes narrower from top to bottom, the formula is subtraction: `bottomWidth (i.e. topWidth attribute) = currentWidth - (height * angleK)`
> 3. The top width formula of the next layer (the additional indentation caused by gap must be considered): `nextLayerWidth = bottomWidth - (gap * angleK)`

## Script build template

You must use `node` to run the script to generate JSON.

```javascript
import fs from 'fs';

// 1. Configure basic parameters
const GAP = 4;
const ANGLE_K = 2; // Slope coefficient: every time the height decreases by 1px, the width decreases by 2px
const LAYER_HEIGHT = 80;

const data = [
  { text: "Display (100%)", fillColor: "#F0F4FC", textColor: "#1F2329" },
  { text: "Click (50%)", fillColor: "#EAE2FE", textColor: "#1F2329" },
  { text: "Additional purchase (20%)", fillColor: "#DFF5E5", textColor: "#1F2329" },
  { text: "Deal (5%)", fillColor: "#1F2329", textColor: "#FFFFFF" }
];

// Calculate the initial width of the first layer (make sure the bottom layer shrinks to 0 or has a flat bottom)
// Backward formula: startWidth = bottom width of the last layer + all height consumption + all gap consumption
const totalHeightLoss = data.length * LAYER_HEIGHT * ANGLE_K;
const totalGapLoss = (data.length - 1) * GAP * ANGLE_K;
// Set the bottom layer to a sharp corner (bottom width is 0)
let currentWidth = 0 + totalHeightLoss + totalGapLoss;

const children = data.map((layer, index) => {
  // 2. Calculate the bottom width of the current layer according to the formula (corresponding to the topWidth attribute of the node)
  const currentBottomWidth = currentWidth - (LAYER_HEIGHT * ANGLE_K);
  
  const node = {
    type: currentBottomWidth <= 0 ? "triangle" : "trapezoid",
    width: currentWidth,
    // Note: topWidth in the funnel represents the narrow side below! If <=0 use triangle
    topWidth: Math.max(0, currentBottomWidth), 
    height: LAYER_HEIGHT,
    vFlip: false, // must be false
    text: layer.text,
    textAlign: "center",
    fillColor: layer.fillColor,
    borderColor: layer.fillColor,
    borderWidth: 2,
    fontSize: 16,
    textColor: layer.textColor
  };

  // 3. Key: Calculate the top width of the next layer. The inward shrinkage of the gap must be subtracted!
  currentWidth = currentBottomWidth - (GAP * ANGLE_K);
  
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

fs.writeFileSync('funnel.json', JSON.stringify(output, null, 2));
```

## trap

- **Don't write down the width randomly by hand**: This will cause the sides of the funnel to become folded lines, not straight. The above `angleK` formula calculation must be strictly used.
- **Forgot to calculate the shrinkage caused by the gap**: If the `width` of the next layer is simply equal to the `topWidth` of the previous layer, if there is a gap, jagged corners will occur at the connection. `gap * angleK` must be subtracted.
- **vFlip not set**: forgetting `"vFlip": false` will cause the trapezoid to flip upwards, giving the funnel the wrong shape
- **Text overflows the bottom layer**: The narrower the bottom layer, the smaller the space. Use `\n` to wrap short copy, and place long copy outside next to the funnel (the outer layer covers the frame of `layout: "horizontal"`, one side of the funnel, and the other side of the description text)
