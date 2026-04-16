#Connection system

## Connection strategy

| Number of connections | Strategy |
|--------|------|
| ≤8 | Draw one by one |
| 9-15 | Representative connections (select 1-2 nodes on each layer to connect to the next layer) |
| >15 | Layer-to-layer connection, or fallback to streamlined grouping |

When a node has 3+ connections: the incoming line is from the top, the outgoing line is from the bottom, and multiple lines on the same side are scattered in different directions.

---

## The connector must contain the root nodes array

```typescript
// Error: connector is placed in frame children
{ type: 'frame', children: [
  { type: 'connector', ... } // Will cause Schema to report an error or fail to connect!
]}

// Correct: connector is placed in the root nodes array
const doc: WBDocument = {
  version: 2,
  nodes: [
    { type: 'frame', id: 'box', ... },
    { type: 'connector', ... }, // must be at the same level as the top-level frame
  ],
};
```

---

## Arrow default value

- When `endArrow` is omitted, it defaults to `'arrow'` (that is, there is an arrow at the end of the connection by default).
- When `startArrow` is omitted, it defaults to `'none'` (that is, there is no arrow at the beginning of the connection by default).

---

## Connection skills

```typescript
// Automatic routing (recommended): Just specify the node id (the anchor point is also optional, the engine can automatically infer it), and use a polyline (or rightAngle) shape
// As long as waypoints are not passed, the engine will try to automatically avoid obstacles and generate polylines.
{ type: 'connector', connector: {
  from: 'a', to: 'b', // fromAnchor and toAnchor can also be omitted, allowing the engine to find the shortest path by itself
  lineShape: 'polyline', lineColor: '#000000', lineWidth: 2, endArrow: 'arrow' }}

// Precise coordinates (make annotation arrows)
{ type: 'connector', connector: {
  from: { x: 150, y: 200 }, to: 'b', toAnchor: 'left',
  lineShape: 'curve', lineColor: '#BBBFC4', lineWidth: 2,
  lineStyle: 'dashed', endArrow: 'triangle' }}

// Manually control waypoints (only used when a forced fixed route is required, or automatic routing does not meet expectations)
// Note: Once waypoints are provided, the engine will strictly respect these points and will no longer perform automatic obstacle avoidance.
{ type: 'connector', connector: {
  from: { x: 300, y: 140 }, to: { x: 300, y: 340 },
  waypoints: [{ x: 350, y: 140 }, { x: 350, y: 340 }],
  lineShape: 'polyline', lineColor: '#000000', lineWidth: 2, endArrow: 'arrow' }}
```

> [!IMPORTANT]
> **1. `lineShape` enforces constraints**:
> - **`'polyline'`**: **preferred by default**. Suitable for most scenarios such as flow charts and architecture diagrams.
> - **`'straight'` (straight line)**: Suitable for **coordinate axes, number axes, geometric figure borders** and other scenes that **must not be curved**.
> - **`'rightAngle'` (right-angled polyline)**: Suitable for scenes such as [organization.md](scenes/organization.md) that clearly require "bus/right-angle specification" and strict alignment of tree levels.
> - **`'curve'`**: Suitable for elegant cross-layer connections (S-shaped bends), freely diverging brain map branches, or when making annotation arrows.
> **2. Spacing requirements**: The gap between cards with connector lines must be ≥ 40, otherwise the arrows will be squeezed into the gap and cannot be seen clearly.
> **3. Top-level constraints**: `connector` must be placed directly in `WBDocument.nodes`, and it is **strictly prohibited** to be nested within `children`. It is recommended to declare the connection uniformly at the end of the data.

> [!TIP]
> **When to manually calculate waypoints**: The engine does not have automatic obstacle avoidance function. When you need to avoid specific obstacles or ensure a specific routing shape, you need to manually calculate `waypoints` to control the direction.
> **Connection label**: When text description is needed, `label` can be used.

---

## Anchor point direction rules

The anchor point (top/right/bottom/left) indicates which side of the node the connection starts from, and the direction meaning is the same as the four sides of the CSS border.

**Note: Since the current automatic winding function supports omitting anchor points and allowing the engine to automatically infer, the following rules are mainly applicable to scenarios where you want to forcefully control the direction of the line, or use straight lines/curves. **

When selecting the anchor point, use the relative position of the two nodes: the target is below using `fromAnchor: 'bottom'` + `toAnchor: 'top'`, and the target is on the right using `fromAnchor: 'right'` + `toAnchor: 'left'`. If the anchor point is manually specified, it must match the actual relative position of the node, otherwise it may cause the connection to detour in the opposite direction.

**Common paradigms for anchor binding**:
- **Same layer horizontal advancement** (target is on the right): `fromAnchor: "right"` -> `toAnchor: "left"`
- **Vertical sinking propulsion** (target is directly below): `fromAnchor: "bottom"` -> `toAnchor: "top"`
- **Cross-layer bevel advancement** (target at bottom left or bottom right): preferred **`fromAnchor: "bottom"` -> `toAnchor: "top"`**. Since the line segment itself has a gravitational tendency, it exits from the bottom and then bends into the top of the next layer. It perfectly fits the S-shaped bend of the assembly line and can draw the most elegant and smooth cross-layer curve. **Avoid** using left and right anchor points bridging each other.
- **Countercurrent retrieval** (the bottom diverges back to the top origin): preferred **`fromAnchor: "top"` -> `toAnchor: "bottom"`** with `lineStyle: "dashed"`.
