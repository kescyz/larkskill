#Organization chart

Applicable to: tree-shaped hierarchical structure scenarios such as company organizational structure, module dependency tree, classification hierarchical tree, etc.

## Content constraints

- Level ≤ 4
- ≤ 5 child nodes under each parent node
- Leaf nodes are meaningful (don’t add empty nodes just to make up the numbers)
- Use `\n` to manually wrap long text (such as "R&D person in charge\n(CTO)")

## Layout selection

| Mode | Applicable Conditions | Characteristics |
|------|---------|------|
| **tree (centered expansion)** | A hierarchical structure with clear affiliation | The root node is in the center, and the child nodes are arranged horizontally and expanded layer by layer. Each "parent + child" is wrapped with a vertical frame (subtree module) |
| **grid (matrix)** | Multiple departments are leveled, each department has subdivisions | Horizontally divide the departments equally, and each department has a vertical list inside |

## Layout rules

Violation of the following rules will cause wiring confusion or typesetting collapse:

1. **Subtree wrapping mode (key)**: Each parent node and its child node group are wrapped with a frame of `layout: "vertical"` + `alignItems: "center"`. **Don't** put all parent nodes on one level and all child nodes on another level. *Consequences of violation: The centers of the parent node and child node groups are offset, the orthogonal connections cannot be merged, and split into two parallel lines. *
2. **Nodes on the same layer are recommended to have equal heights**: Nodes on the same layer should have the same `height` (such as 60-70) to ensure that the horizontal main axis of the connection is straight. If there is a big difference in text length, you can use `fit-content`, but make sure that the number of lines of text on the same layer is close. *Consequences of violation: Nodes on the same layer are uneven, and rightAngle connections are bent horizontally and disorderly. *
3. **Vertical spacing >= 60**: Vertical `gap: 60` between parent and child. *Consequences of violation: The wiring engine does not have enough space to bend and merge, resulting in the wiring passing through the mold or bifurcating in advance. *
4. **Leaf container even width**: For the horizontal frame containing leaf nodes, the width should be calculated manually (sum of child node widths + gap × (n-1)), such as 2 120px nodes + 20px gap = `width: 260`. Or use `fill-container` to automatically divide. *Consequences of violation: There is a pixel-level deviation between the center of the parent node and the center of the child node group. *
5. **Horizontal gap between brothers on the same level: 20-40**
6. Minimum font size 14px
7. Connection: All parent-child connections must be `lineShape: "rightAngle"` (bus style), `fromAnchor: "bottom"`, `toAnchor: "top"`. *Consequences of violation: loss of bus visual effects exclusive to the organization chart. *
8. The width of the root frame should be sufficient (such as 1200-1600) to prevent leaf nodes from being squeezed and overlapping.
9. Different levels are progressively distinguished in terms of fontSize, borderWidth, and color (such as Root dark gray → L1 light blue → L2 light green → L3 light purple)
10. Use `\n` to automatically wrap long text (such as "Infrastructure Department\n(including cloud native)") to ensure that the node height is enough to accommodate

## Skeleton example

### Tree expansion (subtree wrapping mode)

```json
{
  "version": 2,
  "nodes": [
    {
      "type": "frame",
      "width": 1200,
      "height": "fit-content",
      "layout": "vertical",
      "gap": 48,
      "padding": 40,
      "alignItems": "center",
      "children": [
        {
          "type": "text",
          "id": "title",
          "width": "fill-container",
          "height": "fit-content",
          "text": "[Chart title]",
          "fontSize": 24,
          "textAlign": "center",
          "verticalAlign": "middle"
        },
        {
          "type": "rect",
          "id": "root-node",
          "width": 240,
          "height": "fit-content",
          "borderWidth": 3,
          "borderRadius": 8,
          "text": "[root node name]",
          "fontSize": 18,
          "padding": 12
        },
        {
          "type": "frame",
          "width": "fill-container",
          "height": "fit-content",
          "layout": "horizontal",
          "gap": 40,
          "padding": 0,
          "alignItems": "stretch",
          "children": [
            {
              "type": "frame",
              "width": "fill-container",
              "height": "fit-content",
              "layout": "vertical",
              "gap": 48,
              "padding": 0,
              "alignItems": "center",
              "children": [
                {
                  "type": "rect",
                  "id": "child-a",
                  "width": 200,
                  "height": "fit-content",
                  "borderWidth": 2,
                  "borderRadius": 8,
                  "text": "[child node name]",
                  "fontSize": 16,
                  "padding": 10
                },
                {
                  "type": "frame",
                  "width": "fill-container",
                  "height": "fit-content",
                  "layout": "horizontal",
                  "gap": 40,
                  "padding": 0,
                  "alignItems": "stretch",
                  "children": [
                    { "type": "rect", "id": "leaf-a1", "width": "fill-container", "height": "fit-content", "borderWidth": 1, "borderRadius": 8, "text": "[leaf node name]", "fontSize": 14, "padding": 8 },
                    { "type": "rect", "id": "leaf-a2", "width": "fill-container", "height": "fit-content", "borderWidth": 1, "borderRadius": 8, "text": "[leaf node name]", "fontSize": 14, "padding": 8 }
                  ]
                }
              ]
            },
            {
              "type": "frame",
              "width": "fill-container",
              "height": "fit-content",
              "layout": "vertical",
              "gap": 48,
              "padding": 0,
              "alignItems": "center",
              "children": [
                {
                  "type": "rect",
                  "id": "child-b",
                  "width": 200,
                  "height": "fit-content",
                  "borderWidth": 2,
                  "borderRadius": 8,
                  "text": "[child node name]",
                  "fontSize": 16,
                  "padding": 10
                },
                {
                  "type": "frame",
                  "width": "fill-container",
                  "height": "fit-content",
                  "layout": "horizontal",
                  "gap": 40,
                  "padding": 0,
                  "alignItems": "stretch",
                  "children": [
                    { "type": "rect", "id": "leaf-b1", "width": "fill-container", "height": "fit-content", "borderWidth": 1, "borderRadius": 8, "text": "[leaf node name]", "fontSize": 14, "padding": 8 },
                    { "type": "rect", "id": "leaf-b2", "width": "fill-container", "height": "fit-content", "borderWidth": 1, "borderRadius": 8, "text": "[leaf node name]", "fontSize": 14, "padding": 8 }
                  ]
                }
              ]
            }
          ]
        }
      ]
    },
    { "type": "connector", "connector": { "from": "root-node", "to": "child-a", "fromAnchor": "bottom", "toAnchor": "top", "lineShape": "rightAngle", "lineWidth": 2 } },
    { "type": "connector", "connector": { "from": "root-node", "to": "child-b", "fromAnchor": "bottom", "toAnchor": "top", "lineShape": "rightAngle", "lineWidth": 2 } },
    { "type": "connector", "connector": { "from": "child-a", "to": "leaf-a1", "fromAnchor": "bottom", "toAnchor": "top", "lineShape": "rightAngle", "lineWidth": 2 } },
    { "type": "connector", "connector": { "from": "child-a", "to": "leaf-a2", "fromAnchor": "bottom", "toAnchor": "top", "lineShape": "rightAngle", "lineWidth": 2 } },
    { "type": "connector", "connector": { "from": "child-b", "to": "leaf-b1", "fromAnchor": "bottom", "toAnchor": "top", "lineShape": "rightAngle", "lineWidth": 2 } },
    { "type": "connector", "connector": { "from": "child-b", "to": "leaf-b2", "fromAnchor": "bottom", "toAnchor": "top", "lineShape": "rightAngle", "lineWidth": 2 } }
  ]
};

fs.writeFileSync('org_chart.json', JSON.stringify(doc, null, 2));
```

## trap

- **Separate parent-child hierarchy (fatal error)**: Do not put all sibling parent nodes in one horizontal frame and all child nodes in another. A vertical frame with alignItems: "center" must be used to wrap each parent node and its child nodes together.
- **Nodes on the same layer are uneven**: The heights of nodes on the same layer should be the same (or the number of lines of text should be close), otherwise the rightAngle connection will be bent horizontally and disorderly.
- **Insufficient vertical spacing**: The gap between parent and child must be >= 60. If there is not enough, the connection engine cannot bend and merge. Don’t use 80 either, 3-4 layers will stretch it too much lengthwise.
- **Make it a linear chain instead of a tree expansion**: The child nodes of each parent node must be expanded horizontally, not a single chain.
- **Mixed connections straight**: All parent-child connections must have `lineShape: "rightAngle"`, `fromAnchor: "bottom"`, `toAnchor: "top"`.
- **Leaf node font size 12px cannot be seen clearly**: Minimum font size 14px.
- **All nodes have the same size and style**: Different levels must be distinguished in fontSize, borderWidth, and color (root>child>leaf).
