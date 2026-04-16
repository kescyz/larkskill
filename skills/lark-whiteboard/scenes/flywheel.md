# Growth flywheel chart (Flywheel)

> **Must write script to generate JSON. ** The flywheel diagram requires label position and SVG ring cutting in the polar coordinate calculation stage, and direct handwritten JSON cannot correctly implement the concentric ring structure. Please use the script template below.

## Content constraints

- 4-6 stages, short label for each stage (title + optional subtitle/desc)
- Center-placed Flywheel theme title

## Layout selection

- **Script generates coordinates** (required): Use .js script polar coordinates to calculate stage label position, SVG ring cutting, and call `npx -y @larksuite/whiteboard-cli@^0.1.0` after the script outputs the JSON file for rendering

## Layout rules

- Construct a ring using the concentric circle occlusion method: large circle (background color) + small circle (white mask) + center text
- The order of the nodes array determines the z-index: large circle first -> small circle -> center text -> SVG cutting -> peripheral card
- The stage labels are evenly distributed around the periphery of the ring, and each label is at the same distance from the center of the circle.
- SVG polyline cutting rings to form segments + arrow direction sense
- When there are many stages, it is necessary to dynamically enlarge the radius, reduce the arrow corners, and tighten the text container.

### Detailed explanation of concentric circle occlusion method

Draw a large circle (as the base color of the flywheel), and then draw a small circle (filled with white `#FFFFFF`) right in the center of it. Both the large circle and the small circle are set to `borderWidth: 0`, and a ring is formed by superimposing occlusion.

The order of the layers in the nodes array (must be strictly adhered to):

1. **Bottom big circle** (`type: 'ellipse'`, coloring, `borderWidth: 0`)
2. **Mask small circle** (`type: 'ellipse'`, white filling, `borderWidth: 0`)
3. **Center text** — must be added after the two circles, otherwise it will be covered by the white circle
4. **SVG cutting arrow** — overlaid on the ring, cut out segments with thick white polyline
5. **Peripheral stage card** — Polar coordinate calculation position

### SVG arrow line cutting segmentation

By inserting an `svg` node that fills the large circle area, use polar coordinates to calculate the coordinates of each segment junction, and use `<polyline>` to draw a thick line with the same color as the background (white, 20px+ width). The line passes from the edge of the inner circle through the edge of the large circle, and deflects at a certain angle (`da` parameter) when passing through, visually "cutting" the ring and forming a sense of arrow direction.

### Peripheral text wrapping layout

- Calculate the center angle of each segment using polar coordinates `x = cx + R * cos(θ)`
- Place the `frame` container at the calculated coordinate point (`layout: 'vertical'`)
- The `text` node inside the peripheral text container cannot use `width: 'fill-container'`, and must specify a fixed width with `height: 'fit-content'`

### Dynamic scaling optimization (required when the number of stages >= 8)

When the number of stages is large (more than 8, 12 or 16), it must be adjusted dynamically:

- **Enlarge canvas and circle radius**: The more nodes there are, the longer the circle is needed to accommodate the surrounding text. Increase `rOut` and `rIn` appropriately (for example, `rOut` can be set to 400+ in 16 stages), and simultaneously increase `cx`/`cy` to avoid exceeding the boundary.
- **Reduce arrow cutting angle**: As the number of segments increases, the angle between each segment becomes smaller. Keeping the default angle will cause the gap to be too large. `da` should be reduced (e.g. `da = 4`)
- **Tighten the surrounding text container**: narrow the `boxWidth`, reduce the text size, and ensure that adjacent text boxes do not cover each other

## Skeleton example

This scene must be generated with a .js script. When using Agent, you only need to modify the `stages` array and `centerTitle`/`centerSubtitle`, and the rest of the coordinates will be calculated automatically.

```json
const { writeFileSync } = require('fs');

// ══════════════════════════════════════════════════════════════
// Just modify here -- fill in the stage data and center title required by the user
// ══════════════════════════════════════════════════════════════

const centerTitle = '{{CENTER_TITLE}}';
const centerSubtitle = '{{CENTER_SUBTITLE}}'; // Optional, leave empty string if not needed

const stages = [
  { title: '{{STAGE_1}}', subtitle: '{{SUB_1}}', desc: '{{DESC_1}}' },
  { title: '{{STAGE_2}}', subtitle: '{{SUB_2}}', desc: '{{DESC_2}}' },
  { title: '{{STAGE_3}}', subtitle: '{{SUB_3}}', desc: '{{DESC_3}}' },
  { title: '{{STAGE_4}}', subtitle: '{{SUB_4}}', desc: '{{DESC_4}}' },
];

// ══════════════════════════════════════════════════════════════
//The following is the automatic calculation logic and does not need to be modified.
// ══════════════════════════════════════════════════════════════

// --- layout parameters ---
const numSegments = stages.length;
const cx = 600, cy = 450; // Canvas center
const rOut = 240, rIn = 160; // Radius of inner and outer circles
const textDist = rOut + 40; // distance of text from center of circle
const boxWidth = 220; // Width of peripheral text card
const boxHeight = 80; // Estimated height (used for offset calculation)
const da = 8; // arrow fold angle

const nodes = [];

// --- Layer 1: Bottom large circle (circle background color) ---
nodes.push({
  type: 'ellipse',
  x: cx - rOut, y: cy - rOut,
  width: rOut * 2, height: rOut * 2,
  borderWidth: 0,
});

// --- Layer 2: Mask small circle (white) ---
nodes.push({
  type: 'ellipse',
  x: cx - rIn, y: cy - rIn,
  width: rIn * 2, height: rIn * 2,
  borderWidth: 0,
});

// --- Layer 3: Center text (must be after the two circles) ---
nodes.push({
  type: 'text',
  x: cx - rIn, y: cy - (centerSubtitle ? 30 : 20),
  width: rIn * 2, height: 'fit-content',
  text: [{ content: centerTitle, bold: true, fontSize: 32 }],
  textAlign: 'center',
});
if (centerSubtitle) {
  nodes.push({
    type: 'text',
    x: cx - rIn, y: cy + 20,
    width: rIn * 2, height: 'fit-content',
    text: [{ content: centerSubtitle, fontSize: 18 }],
    textAlign: 'center',
  });
}

// --- Layer 4: SVG Cut Arrow ---
let svg = `<svg viewBox="0 0 ${rOut * 2} ${rOut * 2}" xmlns="http://www.w3.org/2000/svg">`;
for (let i = 0; i < numSegments; i++) {
  const a = -90 + i * (360 / numSegments);
  const rad = (a * Math.PI) / 180;
  const radMid = ((a + da) * Math.PI) / 180;
  const R1 = rIn - 5, R2 = rOut + 5, Rm = (rIn + rOut) / 2;
  const x1 = rOut + R1 * Math.cos(rad), y1 = rOut + R1 * Math.sin(rad);
  const x2 = rOut + Rm * Math.cos(radMid), y2 = rOut + Rm * Math.sin(radMid);
  const x3 = rOut + R2 * Math.cos(rad), y3 = rOut + R2 * Math.sin(rad);
  svg += `<polyline points="${x1},${y1} ${x2},${y2} ${x3},${y3}" stroke="#FFFFFF" stroke-width="20" fill="none" stroke-linejoin="round" stroke-linecap="round" />`;
}
svg += `</svg>`;
nodes.push({
  type: 'svg',
  x: cx - rOut, y: cy - rOut,
  width: rOut * 2, height: rOut * 2,
  svg: { code: svg },
});

// --- Layer 5: Peripheral stage card (polar coordinate calculation position) ---
for (let i = 0; i < numSegments; i++) {
  const stage = stages[i];
  const a = -90 + (360 / numSegments) / 2 + i * (360 / numSegments);
  const rad = (a * Math.PI) / 180;
  const tx = cx + textDist * Math.cos(rad);
  const ty = cy + textDist * Math.sin(rad);

  //Dynamic offset: push the text box outward according to the angle
  let offsetX = 0, offsetY = 0;
  if (Math.cos(rad) > 0.1) offsetX = 0;
  else if (Math.cos(rad) < -0.1) offsetX = -boxWidth;
  else offsetX = -boxWidth / 2;
  if (Math.sin(rad) > 0.1) offsetY = 0;
  else if (Math.sin(rad) < -0.1) offsetY = -boxHeight;
  else offsetY = -boxHeight / 2;

  const textW = boxWidth - 24; // card padding 12 * 2
  nodes.push({
    type: 'frame',
    x: tx + offsetX, y: ty + offsetY,
    width: boxWidth, height: 'fit-content',
    layout: 'vertical', gap: 8, padding: 12,
    alignItems: 'start',
    borderWidth: 2, borderRadius: 8,
    children: [
      { type: 'text', width: textW, height: 'fit-content',
        text: [{ content: stage.title, bold: true, fontSize: 18 }], textAlign: 'left' },
      { type: 'text', width: textW, height: 'fit-content',
        text: [{ content: stage.subtitle, fontSize: 14 }], textAlign: 'left' },
      { type: 'text', width: textW, height: 'fit-content',
        text: [{ content: stage.desc, fontSize: 12 }], textAlign: 'left' },
    ],
  });
}

// --- Chart title ---
nodes.push({
  type: 'text',
  x: cx - rOut - 100, y: 30,
  width: (rOut + 100) * 2, height: 'fit-content',
  text: [{ content: centerTitle, bold: true, fontSize: 24 }],
  textAlign: 'center',
});

writeFileSync('flywheel.json', JSON.stringify({ version: 2, nodes }, null, 2));
```

**How ​​to run the script**:

```bash
node generate-flywheel.js
npx -y @larksuite/whiteboard-cli@^0.1.0 -i flywheel.json -o ./flywheel.png
```

## trap

- **The center text is obscured by SVG**: The center text node must be added after the large circle and small circle and before the SVG to ensure that the z-index is correct
- **Missing direction indicator arrow**: SVG polyline cutting line must have an angle deflection (da parameter) to form a clockwise/counterclockwise arrow feel
- **Label position asymmetry**: Peripheral cards must be evenly distributed using the polar coordinate formula `x = cx + R * cos(θ)` and cannot be placed manually.
- **Peripheral text container deadlock**: `layout: 'vertical'` frame internal text node cannot use `width: 'fill-container'`, a fixed width must be specified
