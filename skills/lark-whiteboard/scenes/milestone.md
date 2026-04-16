# Milestone Timeline (Milestone)

## Content constraints

- Nodes 4-8
- Per node: title + date + optional description
- Time increases from left to right

## Layout selection

Two options to choose from:

1. **Horizontal Timeline**: horizontal frame, nodes are equally divided
2. **Alternate up and down**: Absolute positioning, nodes alternate up and down the timeline (more compact when there are many nodes)

## Structural features

- **Title Center**: Place the chart title at the top
- **Year/Timeline Bar**: The arrow-shaped color block carries the year, increasing from left to right according to time.
- **Milestone Card**: The dotted rounded card below carries the title and description
- **Strict alignment**: The year bar is the same width as the corresponding card, aligned left and right
- **Text level**: Title bold at the top, description text smaller and lighter at the bottom, aligned in the center

## Layout rules

- Absolute positioning is the main one (`layout: "none"`), and the node position carries the time series meaning.
- First determine the number of milestones and calculate the equidistant x-coordinate sequence
- The timeline uses connectors to run through all nodes
-Nodes are connected to the timeline with short vertical lines
- Consistent horizontal spacing between nodes
- Year bar width = card width, vertical spacing is uniform
- Leave enough space in the title and year areas

## Skeleton example

```json
{
  "version": 2,
  "nodes": [
    {
      "type": "frame",
      "x": 0, "y": 0,
      "width": 1200, "height": 360,
      "layout": "none",
      "children": [
        {
          "type": "text",
          "x": 300, "y": 12,
          "width": 600, "height": "fit-content",
          "text": [{ "content": "{{CHART_TITLE}}", "bold": true, "fontSize": 24 }],
          "textAlign": "center"
        },

        {
          "type": "svg",
          "x": 50, "y": 56,
          "width": 190, "height": 36,
          "svg": {
            "code": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 190 36\"><polygon points=\"0,0 170,0 190,18 170,36 0,36\"/></svg>"
          }
        },
        {
          "type": "text",
          "x": 50, "y": 64,
          "width": 190, "height": "fit-content",
          "text": "{{DATE_1}}",
          "textAlign": "center"
        },
        {
          "type": "rect",
          "x": 50, "y": 132,
          "width": 190, "height": 120,
          "borderDash": "dashed",
          "borderRadius": 8
        },
        {
          "type": "text",
          "x": 50, "y": 150,
          "width": 190, "height": "fit-content",
          "text": [{ "content": "{{MILESTONE_1_TITLE}}", "bold": true, "fontSize": 16 }],
          "textAlign": "center"
        },
        {
          "type": "text",
          "x": 50, "y": 180,
          "width": 190, "height": "fit-content",
          "text": "{{MILESTONE_1_DESC}}",
          "fontSize": 13,
          "textAlign": "center"
        },

        {
          "type": "svg",
          "x": 290, "y": 56,
          "width": 190, "height": 36,
          "svg": {
            "code": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 190 36\"><polygon points=\"0,0 170,0 190,18 170,36 0,36\"/></svg>"
          }
        },
        {
          "type": "text",
          "x": 290, "y": 64,
          "width": 190, "height": "fit-content",
          "text": "{{DATE_2}}",
          "textAlign": "center"
        },
        {
          "type": "rect",
          "x": 290, "y": 132,
          "width": 190, "height": 120,
          "borderDash": "dashed",
          "borderRadius": 8
        },
        {
          "type": "text",
          "x": 290, "y": 150,
          "width": 190, "height": "fit-content",
          "text": [{ "content": "{{MILESTONE_2_TITLE}}", "bold": true, "fontSize": 16 }],
          "textAlign": "center"
        },
        {
          "type": "text",
          "x": 290, "y": 180,
          "width": 190, "height": "fit-content",
          "text": "{{MILESTONE_2_DESC}}",
          "fontSize": 13,
          "textAlign": "center"
        }
      ]
    }
  ]
}
```

## trap

- **Too crowded when there are too many nodes**: When there are more than 6 nodes, consider alternating top and bottom layout or increasing the canvas width
- **The right node overlaps the end of the timeline**: the x + width of the last node should not exceed the canvas boundary
- **The year bar is not aligned with the card**: The x and width of the year bar and the card must be exactly the same
