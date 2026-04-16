# Fishbone diagram (cause and effect diagram)

> **You must write a script to generate JSON.** Fishbone branch angles and cause-branch coordinates require trigonometric calculations. Writing JSON manually can easily cause node overlap and connector crossing. Please use the script template below.

## Content constraints

- Categories 4-6
- Reasons for each category ≤ 4
- Total reasons ≤ 20 (exceeding must be combined into categories)

## Layout selection

- **Script generates coordinates** (required): Use a .js script to calculate the fishbone coordinates through trigonometric functions. After the script outputs the JSON file, call `npx -y @larksuite/whiteboard-cli@^0.1.0` for rendering.

## Layout rules

- The trunk is centered horizontally and extends from left to right
- Classification nodes are arranged from left to right by spineX, with odd numbers (1st, 3rd, 5th...) at the top and even numbers (2nd, 4th...) at the bottom
- The causes of each classification are arranged equidistantly along diagonal lines (branch bones)
- The fish head (center question) is on the right, with ellipse
- The main line is connected with an arrow pointing to the fish head, the branch bone and the small bone are connected endArrow: "none"
- The reason ossicle extends horizontally to the right side of the reason box, and the Y coordinate is accurately aligned

## Skeleton example

**Alternate up and down**: The classification labels are arranged from left to right according to spineX, with odd numbers (1st, 3rd, 5th...) at the top and even numbers (2nd, 4th...) at the bottom.

**Visual same color system**: The classification labels, connections and all reason nodes under the same branch must use the same color system (such as the same background color and border color combination) to maintain a unified graphic style and logical coherence. A set of color arrays can be predefined and used in branch polling.

### Coordinate calculation script template (must be generated strictly according to this algorithm)

The following Node.js script template contains a complete dynamic layout algorithm that can automatically adapt to any number of categories and reasons to generate a perfect non-overlapping fishbone diagram:

```javascript
const fs = require('fs');

const nodes = [];

// 1. Data definition (populated according to user needs)
const categories = [
  { id: "c0", text: "Front-end code", reasons: ["Uncompressed resources", "Redundant requests", "Oversized images are not lazy loaded"] },
  { id: "c1", text: "Backend service", reasons: ["Database slow query", "Cache failure", "Excessive concurrency"] },
  { id: "c2", text: "Network environment", reasons: ["CDN configuration error", "Slow DNS resolution", "Bandwidth limit", "Network jitter"] }
];

// 2. Dynamic layout calculation
const catWidth = 120;
const catHeight = 40;
const reasonWidth = 140; // Adjust reason box width to accommodate long text
const reasonHeight = 32;
const lineLength = 20; //The horizontal extension length of the line connecting the ossicles
const paddingX = 40; // Horizontal safety spacing between nodes on the same side

//Preset branch color coefficient group (branch bone classification and specific reasons keep the same color system)
const branchColors = [
  { fill: "#E8F3FF", stroke: "#1664FF" }, // Blue color
  { fill: "#E6FFED", stroke: "#00B42A" }, // Green color
  { fill: "#FFF7E8", stroke: "#FF7D00" }, // Orange color
  { fill: "#FFECE8", stroke: "#F5319D" }, // pink color
  { fill: "#F2E8FF", stroke: "#722ED1" }, // Purple color
  { fill: "#E8FFFF", stroke: "#14C9C9" } // Cyan color
];

let maxSpineY_up = 0;
let maxSpineY_down = 0;

// Step one: Calculate the internal size and relative bounding box of each category
categories.forEach((cat, index) => {
  const isTop = index % 2 === 0;
  const numReasons = cat.reasons.length;

  // Dynamically calculate branch heights to ensure that the cause ossicles do not overlap vertically
  //Each reason requires reasonHeight + upper and lower spacing (about 16)
  const requiredY = (numReasons + 1) * (reasonHeight + 16);
  const branchDY = Math.max(160, requiredY);
  const branchDX = -branchDY * 0.7; // Maintain a fixed tilt angle and extend to the left

  cat.isTop = isTop;
  cat.branchDX = branchDX;
  cat.branchDY = branchDY;

  //Record the maximum branch height, used to calculate the background height and main bone Y coordinate
  if (isTop) maxSpineY_up = Math.max(maxSpineY_up, branchDY + catHeight + 40);
  else maxSpineY_down = Math.max(maxSpineY_down, branchDY + catHeight + 40);

  // Calculate the extreme value of the relative bounding box of this category (relative to the spineX anchor point)
  //The far left may be determined by the classification box or the reason box
  cat.minX = Math.min(branchDX - catWidth / 2, branchDX - lineLength - reasonWidth);
  //The rightmost side is the main bone mounting point 0 or the right side of the classification box
  cat.maxX = Math.max(0, branchDX + catWidth / 2);
});

// Step 2: Calculate the absolute X coordinate (spineX) of each category on the main bone
let currentSpineX = 100; // initial offset
for (let i = 0; i < categories.length; i++) {
  const cat = categories[i];
  let startX = currentSpineX;

  // Need to keep distance from the previous category on the same side to prevent horizontal overlap
  if (i >= 2) {
    const prevSameSideCat = categories[i - 2];
    const requiredX = prevSameSideCat.spineX + prevSameSideCat.maxX - cat.minX + paddingX;
    startX = Math.max(startX, requiredX);
  }

  // Ensure that the longest branch on the left does not exceed the left boundary of the canvas
  if (startX + cat.minX < 50) {
    startX = 50 - cat.minX;
  }

  cat.spineX = startX;
  // Push forward slightly each time to ensure that the nodes on the opposite side can also be slightly staggered
  currentSpineX = startX + 80;
}

// Step 3: Calculate global canvas size
const lastCat = categories[categories.length - 1];
const spineY = maxSpineY_up + 50; // Dynamically derive the Y coordinate of the main bone
const totalWidth = lastCat.spineX + 350; // Leave space for the fish head on the right side
const totalHeight = spineY + maxSpineY_down + 50;

// 4. Generate node data
// background
nodes.push({ type: "rect", x: 0, y: 0, width: totalWidth, height: totalHeight, fillColor: "#FFFFFF", borderWidth: 0 });

// fish head
const headWidth = 180;
const headHeight = 80;
const headX = totalWidth - headWidth - 40;
const headY = spineY - headHeight / 2;
nodes.push({ type: "ellipse", id: "head", x: headX, y: headY, width: headWidth, height: headHeight, text: "Core Issue" });

// Main bone connection
const firstSpineX = categories[0].spineX + categories[0].minX;
nodes.push({
  type: "connector",
  connector: { from: { x: firstSpineX, y: spineY }, to: "head", toAnchor: "left", lineShape: "straight", endArrow: "arrow" }
});

// Traverse the generated classification and reason bones
categories.forEach((cat, index) => {
  const isTop = cat.isTop;
  const branchDY = cat.branchDY;
  const branchDX = cat.branchDX;
  const color = branchColors[index % branchColors.length];

  // Classification tags
  const catX = cat.spineX + branchDX - catWidth / 2;
  const catY = spineY + (isTop ? -branchDY - catHeight : branchDY);

  nodes.push({
    type: "rect", id: cat.id, x: catX, y: catY, width: catWidth, height: catHeight, text: cat.text,
    fillColor: color.fill, strokeColor: color.stroke
  });
  // Branch bone connection
  nodes.push({
    type: "connector",
    connector: { from: { x: cat.spineX, y: spineY }, to: cat.id, toAnchor: isTop ? "bottom" : "top", lineShape: "straight", endArrow: "none", lineColor: color.stroke }
  });

  // reason ossicles
  cat.reasons.forEach((reason, rIndex) => {
    //Linear interpolation, evenly distributed on the branch bones
    const t = (rIndex + 1) / (cat.reasons.length + 1);
    const attachX = cat.spineX + branchDX * t;
    const attachY = spineY + (isTop ? -branchDY : branchDY) * t;

    // Key alignment: Make sure the cause box is completely on the left side of the connection line, and the Y coordinate center is accurately aligned
    const boxX = attachX - lineLength - reasonWidth;
    const boxY = attachY - reasonHeight / 2;

    const rId = `${cat.id}-r${rIndex}`;
    nodes.push({
      type: "rect", id: rId, x: boxX, y: boxY, width: reasonWidth, height: reasonHeight, text: reason,
      fillColor: color.fill, strokeColor: color.stroke
    });
    // Reason ossicle connection
    nodes.push({
      type: "connector",
      connector: { from: { x: attachX, y: attachY }, to: rId, toAnchor: "right", lineShape: "straight", endArrow: "none", lineColor: color.stroke }
    });
  });
});

fs.writeFileSync('fishbone-diagram.json', JSON.stringify({ version: 2, nodes }, null, 2));
```

## Connection format and points to note

All connectors use the format `{ "type": "connector", "connector": { ... } }`.
**Note: Except for the main bone, all other connections (branch bones, small bones) must be set to `"endArrow": "none"`, otherwise arrows will be included by default, causing direction confusion. **

Branch bone: From the absolute coordinate point on the main bone → Classification label node:

```json
{
  "version": 2,
  "nodes": [
    { "type": "rect", "x": 0, "y": 0, "width": "__totalWidth__", "height": "__totalHeight__" },

    { "type": "ellipse", "id": "head", "x": "__headX__", "y": "__headY__",
      "width": 180, "height": 80, "text": "[central question]" },

    { "type": "connector", "connector": {
      "from": { "x": "__spineStartX__", "y": "__spineY__" },
      "to": "head", "toAnchor": "left",
      "lineShape": "straight", "endArrow": "arrow"
    }},

    { "type": "rect", "id": "c0", "x": "__catX__", "y": "__catY__",
      "width": 120, "height": 40, "text": "[Category A]" },
    { "type": "connector", "connector": {
      "from": { "x": "__spineX0__", "y": "__spineY__" },
      "to": "c0", "toAnchor": "bottom",
      "lineShape": "straight", "endArrow": "none"
    }},

    { "type": "rect", "id": "c0-r0", "x": "__reasonX__", "y": "__reasonY__",
      "width": 140, "height": 32, "text": "[Reason 1]" },
    { "type": "connector", "connector": {
      "from": { "x": "__attachX__", "y": "__attachY__" },
      "to": "c0-r0", "toAnchor": "right",
      "lineShape": "straight", "endArrow": "none"
    }}
  ]
}
```

The above skeleton shows the pattern of one category (above) + one reason. The full fishbone diagram repeats this pattern, alternating up and down. There can be multiple causes under each category, uniformly interpolated and distributed on the branch bones.

**How ​​to run the script**:

```bash
node generate-fishbone.js
npx -y @larksuite/whiteboard-cli@^0.1.0 -i fishbone.json -o ./fishbone.png
```

## trap

- **Code Generation**: A script with a dynamic anti-overlap algorithm must be used to calculate coordinates and output JSON.
- **Branch Bone Anti-Overlap**: Adjacent branch bones and reason boxes on the same side must not have any intersection.
- **Adaptive Height**: When the number of causes is large, the branch bones will automatically lengthen to accommodate all the small bones.
- **Cause Ossicle Level**: The attachment point on the right side of the reason box must be consistent with the Y coordinate of the starting point of the connection.
- **No arrows**: All classified branch connections and ossicle connections must have arrows turned off.
- **Same color system**: The same branch bone, classification label node, and reason bone node and connection line must use the same color system to maintain visual coherence.
