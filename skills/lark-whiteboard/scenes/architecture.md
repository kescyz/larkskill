# System architecture diagram

Applicable to: hierarchical architecture diagrams, microservice architecture diagrams, front-end and back-end architecture diagrams, and other scenarios with clear module divisions.

## Content constraints

- **Full expansion**: The user said "IM architecture" should be expanded to the access layer (Web/iOS/Android/Desktop), gateway layer (access/routing/security), service layer (two sub-areas of core service + support service), and storage layer (MySQL/Redis/MongoDB + brackets indicate the purpose)
- 3-6 nodes per layer. More than 6 are divided into two rows or divided into sub-areas (such as one sub-frame each for "Core Services" and "Support Services")
- Layer labels should be short (2-4 words), such as "access layer" and "gateway layer"
- Each node has a title + a short description (such as "User Service\nRegistration Login and Permission Management")
- Add brackets to the technical components to indicate the technology stack (such as "Message Queue\n(Kafka)")
- Storage nodes must use `cylinder` type (radians are fixed at 16px, `fill-container` width is prohibited, and 120-200 is used to fix the width). Maximum of 4 cylinders per line (more than 4 line breaks or merging similar items, such as merging multiple MySQLs into "relational database\n(MySQL)")
- Sidebars (such as operation and maintenance monitoring, infrastructure) are only added when the user explicitly requests them, with a maximum of 2-3 items. Don’t add a sidebar on your own
- **Connection: Do not draw unless necessary. ** The hierarchical structure of the architecture diagram itself has expressed the calling direction (the upper layer calls the lower layer), and there is no need to connect every pair of nodes. Only draw when you need to emphasize a specific call relationship, and the total number should not exceed 3-5

## Layout selection

| Mode | Applicable Conditions | Characteristics |
|------|---------|------|
| **grid (hierarchical stripe)** | There is a clear upper and lower hierarchical relationship (access → gateway → service → storage) | row = hierarchy, each row horizontal frame divides the nodes into equal parts. Left text label + right layer frame (Label-Outside mode) |
| **grid (grid matrix)** | Multi-module leveling, no clear hierarchy | N×M grid equally divided, one module per grid |
| **Hybrid (island style)** | Mesh interconnection between modules, no clear layering | Macro `layout: "none"` + x/y to position each module island, micro each island uses flex layout inside |

## Layout rules

- **Root node**: fixed width (1200), `height: "fit-content"`, `layout: "vertical"`, `gap: 20`, `padding: 24`
- **Body double columns** (when there are sidebars): horizontal frame, `alignItems: "stretch"`, `gap: 16`
-Left layers-container: `width: "fill-container"`, vertical, `gap: 16`
- Right sidebar: fixed width 160-180, `height: "fill-container"`, `justifyContent: "space-between"`
- **Single layer (Label-Outside)**: horizontal frame, left text label (`width: 80`, `textAlign: "right"`), right layer frame (`fill-container`, with borderWidth/borderRadius, `padding: 24`, `gap: 16`). **Why use Label-Outside**: Placing labels outside the frame is more concise and avoids vertical text and alignment problems caused by nesting narrow rects inside the frame.
- **Sub-area**: A horizontal wrapper is nested within the layer frame (`alignItems: "stretch"` ensures that the same height is the same), containing multiple vertical frames (each sub-area), each sub-area has its own title text + content line. Inline components `width: "fill-container"` are automatically divided equally.
- **Sidebar**: Split into independent logical block frames (such as "operation and maintenance monitoring" and "infrastructure" are separated), each block `height: "fill-container"`. The outer layer `justifyContent: "space-between"` ensures alignment with the left side, and the inner layer `justifyContent: "center"` can be set to center the content.
- **Inline labels**: If there are special components (such as middleware) that run through multiple columns in the layer, a horizontal layout of "small label on the left + component group on the right" can be used

## Skeleton example

### Layered Strips (Label-Outside + Sidebar)

```json
{
  "version": 2,
  "nodes": [
    {
      "type": "frame",
      "id": "root",
      "x": 0, "y": 0,
      "width": 1200,
      "height": "fit-content",
      "layout": "vertical",
      "gap": 20,
      "padding": 24,
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
          "type": "frame",
          "id": "main-container",
          "width": "fill-container",
          "height": "fit-content",
          "layout": "horizontal",
          "alignItems": "stretch",
          "gap": 16,
          "padding": 0,
          "children": [
            {
              "type": "frame",
              "id": "layers-container",
              "width": "fill-container",
              "height": "fit-content",
              "layout": "vertical",
              "alignItems": "stretch",
              "gap": 16,
              "padding": 0,
              "children": [
                {
                  "type": "frame",
                  "id": "row-layer-1",
                  "width": "fill-container",
                  "height": "fit-content",
                  "layout": "horizontal",
                  "gap": 24,
                  "padding": 0,
                  "alignItems": "center",
                  "children": [
                    {
                      "type": "text",
                      "id": "label-1",
                      "width": 80,
                      "height": "fit-content",
                      "text": "[layer label]",
                      "fontSize": 20,
                      "textAlign": "right"
                    },
                    {
                      "type": "frame",
                      "id": "layer-1",
                      "width": "fill-container",
                      "height": "fit-content",
                      "borderWidth": 2,
                      "borderRadius": 8,
                      "layout": "horizontal",
                      "gap": 16,
                      "padding": 24,
                      "alignItems": "stretch",
                      "children": [
                        { "type": "rect", "id": "n-1-1", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                        { "type": "rect", "id": "n-1-2", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                        { "type": "rect", "id": "n-1-3", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" }
                      ]
                    }
                  ]
                },
                {
                  "type": "frame",
                  "id": "row-layer-2",
                  "width": "fill-container",
                  "height": "fit-content",
                  "layout": "horizontal",
                  "gap": 24,
                  "padding": 0,
                  "alignItems": "center",
                  "children": [
                    {
                      "type": "text",
                      "id": "label-2",
                      "width": 80,
                      "height": "fit-content",
                      "text": "[layer label]",
                      "fontSize": 20,
                      "textAlign": "right"
                    },
                    {
                      "type": "frame",
                      "id": "layer-2",
                      "width": "fill-container",
                      "height": "fit-content",
                      "borderWidth": 2,
                      "borderRadius": 8,
                      "layout": "vertical",
                      "gap": 16,
                      "padding": 24,
                      "alignItems": "stretch",
                      "children": [
                        {
                          "type": "frame",
                          "id": "subareas-wrapper",
                          "width": "fill-container",
                          "height": "fit-content",
                          "layout": "horizontal",
                          "alignItems": "stretch",
                          "gap": 16,
                          "padding": 0,
                          "children": [
                            {
                              "type": "frame",
                              "id": "subarea-a",
                              "width": "fill-container",
                              "height": "fit-content",
                              "layout": "vertical",
                              "gap": 8,
                              "padding": 12,
                              "borderRadius": 8,
                              "borderWidth": 2,
                              "children": [
                                { "type": "text", "id": "title-a", "width": "fill-container", "height": "fit-content", "text": "[subarea name]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                                {
                                  "type": "frame",
                                  "id": "row-a-1",
                                  "width": "fill-container",
                                  "height": "fit-content",
                                  "layout": "horizontal",
                                  "gap": 8,
                                  "padding": 0,
                                  "children": [
                                    { "type": "rect", "id": "sa-1", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                                    { "type": "rect", "id": "sa-2", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" }
                                  ]
                                }
                              ]
                            },
                            {
                              "type": "frame",
                              "id": "subarea-b",
                              "width": "fill-container",
                              "height": "fit-content",
                              "layout": "vertical",
                              "gap": 8,
                              "padding": 12,
                              "borderRadius": 8,
                              "borderWidth": 2,
                              "children": [
                                { "type": "text", "id": "title-b", "width": "fill-container", "height": "fit-content", "text": "[subarea name]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                                {
                                  "type": "frame",
                                  "id": "row-b-1",
                                  "width": "fill-container",
                                  "height": "fit-content",
                                  "layout": "horizontal",
                                  "gap": 8,
                                  "padding": 0,
                                  "children": [
                                    { "type": "rect", "id": "sb-1", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                                    { "type": "rect", "id": "sb-2", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" }
                                  ]
                                }
                              ]
                            }
                          ]
                        }
                      ]
                    }
                  ]
                },
                {
                  "type": "frame",
                  "id": "row-layer-3",
                  "width": "fill-container",
                  "height": "fit-content",
                  "layout": "horizontal",
                  "gap": 24,
                  "padding": 0,
                  "alignItems": "center",
                  "children": [
                    {
                      "type": "text",
                      "id": "label-3",
                      "width": 80,
                      "height": "fit-content",
                      "text": "[layer label]",
                      "fontSize": 20,
                      "textAlign": "right"
                    },
                    {
                      "type": "frame",
                      "id": "layer-3",
                      "width": "fill-container",
                      "height": "fit-content",
                      "borderWidth": 2,
                      "borderRadius": 8,
                      "layout": "horizontal",
                      "gap": 0,
                      "padding": 24,
                      "justifyContent": "space-around",
                      "children": [
                        { "type": "cylinder", "id": "db-1", "width": 140, "height": "fit-content", "text": "[storage name]", "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                        { "type": "cylinder", "id": "db-2", "width": 140, "height": "fit-content", "text": "[storage name]", "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" }
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "type": "frame",
              "id": "right-sidebar-wrapper",
              "width": 180,
              "height": "fill-container",
              "layout": "vertical",
              "alignItems": "stretch",
              "justifyContent": "space-between",
              "gap": 16,
              "padding": 0,
              "children": [
                {
                  "type": "frame",
                  "id": "side-block-1",
                  "width": "fill-container",
                  "height": "fill-container",
                  "layout": "vertical",
                  "alignItems": "stretch",
                  "justifyContent": "center",
                  "gap": 12,
                  "padding": 16,
                  "borderRadius": 8,
                  "borderWidth": 2,
                  "children": [
                    { "type": "text", "id": "side-title-1", "width": "fill-container", "height": "fit-content", "text": "[sidebar module name]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                    {
                      "type": "frame",
                      "id": "side-items-1",
                      "width": "fill-container",
                      "height": "fit-content",
                      "layout": "vertical",
                      "gap": 8,
                      "padding": 0,
                      "children": [
                        { "type": "rect", "id": "s-1", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                        { "type": "rect", "id": "s-2", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" }
                      ]
                    }
                  ]
                },
                {
                  "type": "frame",
                  "id": "side-block-2",
                  "width": "fill-container",
                  "height": "fill-container",
                  "layout": "vertical",
                  "alignItems": "stretch",
                  "justifyContent": "center",
                  "gap": 12,
                  "padding": 16,
                  "borderRadius": 8,
                  "borderWidth": 2,
                  "children": [
                    { "type": "text", "id": "side-title-2", "width": "fill-container", "height": "fit-content", "text": "[sidebar module name]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                    {
                      "type": "frame",
                      "id": "side-items-2",
                      "width": "fill-container",
                      "height": "fit-content",
                      "layout": "vertical",
                      "gap": 8,
                      "padding": 0,
                      "children": [
                        { "type": "rect", "id": "s-3", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
                        { "type": "rect", "id": "s-4", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### Island style (mesh interconnection)

```json
{
  "version": 2,
  "nodes": [
    {
      "type": "frame",
      "id": "root",
      "x": 0, "y": 0,
      "width": 1200,
      "height": 800,
      "layout": "none",
      "padding": 24,
      "children": [
        {
          "type": "text",
          "id": "title",
          "x": 0, "y": 0,
          "width": 1152,
          "height": "fit-content",
          "text": "[Chart title]",
          "fontSize": 24,
          "textAlign": "center",
          "verticalAlign": "middle"
        },
        {
          "type": "frame",
          "id": "island-a",
          "x": 40, "y": 60,
          "width": 320,
          "height": "fit-content",
          "layout": "vertical",
          "gap": 12,
          "padding": 20,
          "borderWidth": 2,
          "borderRadius": 8,
          "children": [
            { "type": "text", "id": "island-a-title", "width": "fill-container", "height": "fit-content", "text": "[module name]", "fontSize": 16, "textAlign": "center", "verticalAlign": "middle" },
            { "type": "rect", "id": "ia-1", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
            { "type": "rect", "id": "ia-2", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" }
          ]
        },
        {
          "type": "frame",
          "id": "island-b",
          "x": 440, "y": 60,
          "width": 320,
          "height": "fit-content",
          "layout": "vertical",
          "gap": 12,
          "padding": 20,
          "borderWidth": 2,
          "borderRadius": 8,
          "children": [
            { "type": "text", "id": "island-b-title", "width": "fill-container", "height": "fit-content", "text": "[module name]", "fontSize": 16, "textAlign": "center", "verticalAlign": "middle" },
            { "type": "rect", "id": "ib-1", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" },
            { "type": "rect", "id": "ib-2", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" }
          ]
        },
        {
          "type": "frame",
          "id": "island-c",
          "x": 240, "y": 340,
          "width": 320,
          "height": "fit-content",
          "layout": "vertical",
          "gap": 12,
          "padding": 20,
          "borderWidth": 2,
          "borderRadius": 8,
          "children": [
            { "type": "text", "id": "island-c-title", "width": "fill-container", "height": "fit-content", "text": "[module name]", "fontSize": 16, "textAlign": "center", "verticalAlign": "middle" },
            { "type": "rect", "id": "ic-1", "width": "fill-container", "height": "fit-content", "text": "[node name]", "borderRadius": 8, "borderWidth": 2, "fontSize": 14, "textAlign": "center", "verticalAlign": "middle" }
          ]
        }
      ]
    },
    { "type": "connector", "connector": { "from": "ia-1", "to": "ib-1", "fromAnchor": "right", "toAnchor": "left", "lineShape": "straight", "lineWidth": 2, "endArrow": "arrow" } },
    { "type": "connector", "connector": { "from": "island-a", "to": "ic-1", "fromAnchor": "bottom", "toAnchor": "top", "lineShape": "rightAngle", "lineWidth": 2, "endArrow": "arrow" } },
    { "type": "connector", "connector": { "from": "island-b", "to": "ic-1", "fromAnchor": "bottom", "toAnchor": "top", "lineShape": "rightAngle", "lineWidth": 2, "endArrow": "arrow" } }
  ]
}
```

## trap

- **All architecture diagrams use hierarchical strips**: When multiple modules are interconnected in a horizontal mesh, the island type should be selected; when there is no clear hierarchy, the grid matrix should be selected. Determine the information structure first and then choose the layout.
- **Excessive connections leading to crossovers**: Do not draw connections unless necessary in the architecture diagram. The hierarchical structure itself already expresses the calling direction, and there is no need to wire each pair of nodes. If you must draw, at most 3-5 critical paths.
- **Use frame title (unreadable) for layer labels**: Layer labels must be placed outside the frame using independent text nodes (Label-Outside mode), and should not be embedded inside the frame.
- **Cylinder uses fill-container width**: The cylinder curvature is fixed at 16px and does not scale with the width. It must use a fixed width (120-200).
- **Sidebar Logic Mix**: "Operation and Maintenance Monitoring" and "Infrastructure" must be independent frames and cannot be merged into one long bar.
- **Root node has no fixed width**: The root frame must have a clear width (such as 1200), otherwise the `fill-container` of the child nodes cannot be calculated.
