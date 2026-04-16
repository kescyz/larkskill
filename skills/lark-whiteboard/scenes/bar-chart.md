# Histogram

## Content constraints

- Data points ≤ 12
- Use the same color for the same data series (do not use different colors for each column)
- The Y-axis must be labeled with units (such as "10,000 yuan", "person-time")

## Layout selection

- **Script generated coordinates** (recommended): Use a .js script to calculate the position and height of the cylinder. After the script outputs the JSON file, call `npx -y @larksuite/whiteboard-cli@^0.1.0` for rendering.
- **Absolute positioning handwriting**: Simple histogram (≤ 5 bars) can be handwritten with coordinates

## Layout rules

- The Y axis of the whiteboard coordinate system is positive downward, the "bottom origin" of the chart has the maximum Y value, and Y decreases as the cylinder grows upward.
- The columns are of equal width and equal spacing, and the bottom is aligned with the X-axis
- Cylinder height: `height = (value / maxValue) * chartHeight`
- Cylinder Y coordinate: `y = originY - height`
- The coordinate axis uses a connector straight line with an arrow at the end (endArrow: "arrow")
- Grid lines use dashed connectors (lineStyle: "dashed", endArrow: "none")
- tick mark dash connector (endArrow: "none")
- The numerical label is placed above the top of the column
- Category labels are placed below the X-axis, aligned to the center of the cylinder

## Coordinates and Dimensions Calculation Guide

In the whiteboard coordinate system, the X axis is positive to the right and the Y axis is positive downward. So the "bottom origin" of the graph actually has the largest Y coordinate, which decreases as the graph grows upward.

1. **Determine the chart area**:
- Set the chart area height `chartHeight` and width `chartWidth`
- Set the coordinate origin of the lower left corner `(originX, originY)`
- Example: originX=80, originY=480, chartWidth=1000, chartHeight=400
2. **Y-axis mapping (calculate height)**:
- Find the maximum value of the data `maxValue`
- Round maxValue up to "integer scale" (for example, the maximum data value is 190 → maxValue is 200)
- Column height: `height = (value / maxValue) * chartHeight`
- Column Y coordinate: `y = originY - height`
3. **X-axis mapping (calculate width and X coordinate)**:
- Divide the chartWidth equally according to the number of data: `slotWidth = chartWidth / barCount`
- Set the column spacing `barGap` (recommended 25%-30% of slotWidth)
- Column width: `barWidth = slotWidth - barGap`
- X coordinate of the i-th column: `x = originX + i * slotWidth + barGap / 2`
4. **Y-axis scale calculation**:
- Divide 0 to maxValue into 4-6 ticks
- Y coordinate of each tick: `gridY = originY - (tickValue / maxValue) * chartHeight`
- Tick marks: dash from (originX-10, gridY) to (originX, gridY)
- Grid lines: dashed lines from (originX, gridY) to (originX+chartWidth, gridY)

## Complete JSON example

The following example: 3 columns, data [120, 200, 150], maxValue=200, originX=80, originY=480, chartWidth=900, chartHeight=400.

- slotWidth = 900 / 3 = 300
- barGap = 80, barWidth = 220
- Scale: 0, 50, 100, 150, 200 (every 50, gridInterval = 80px)

```json
{
  "version": 2,
  "nodes": [
    { "type": "rect", "x": 0, "y": 0, "width": 1100, "height": 580 },

    { "type": "text", "x": 80, "y": 10, "width": 900, "height": "fit-content",
      "text": "Quarterly sales comparison", "fontSize": 24, "textAlign": "center" },

    { "type": "text", "x": 10, "y": 40, "width": 60, "height": "fit-content",
      "text": "ten thousand yuan", "fontSize": 12, "textAlign": "center" },

    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 480 }, "to": { "x": 80, "y": 55 },
      "lineShape": "straight", "lineWidth": 2, "endArrow": "arrow"
    }},
    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 480 }, "to": { "x": 1000, "y": 480 },
      "lineShape": "straight", "lineWidth": 2, "endArrow": "arrow"
    }},

    { "type": "connector", "connector": {
      "from": { "x": 70, "y": 480 }, "to": { "x": 80, "y": 480 },
      "lineShape": "straight", "lineWidth": 1,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "text", "x": 20, "y": 470, "width": 50, "height": 20,
      "text": "0", "fontSize": 12, "textAlign": "right" },

    { "type": "connector", "connector": {
      "from": { "x": 70, "y": 400 }, "to": { "x": 80, "y": 400 },
      "lineShape": "straight", "lineWidth": 1,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "text", "x": 20, "y": 390, "width": 50, "height": 20,
      "text": "50", "fontSize": 12, "textAlign": "right" },
    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 400 }, "to": { "x": 980, "y": 400 },
      "lineShape": "straight", "lineWidth": 1, "lineStyle": "dashed",
      "startArrow": "none", "endArrow": "none"
    }},

    { "type": "connector", "connector": {
      "from": { "x": 70, "y": 320 }, "to": { "x": 80, "y": 320 },
      "lineShape": "straight", "lineWidth": 1,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "text", "x": 20, "y": 310, "width": 50, "height": 20,
      "text": "100", "fontSize": 12, "textAlign": "right" },
    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 320 }, "to": { "x": 980, "y": 320 },
      "lineShape": "straight", "lineWidth": 1, "lineStyle": "dashed",
      "startArrow": "none", "endArrow": "none"
    }},

    { "type": "connector", "connector": {
      "from": { "x": 70, "y": 240 }, "to": { "x": 80, "y": 240 },
      "lineShape": "straight", "lineWidth": 1,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "text", "x": 20, "y": 230, "width": 50, "height": 20,
      "text": "150", "fontSize": 12, "textAlign": "right" },
    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 240 }, "to": { "x": 980, "y": 240 },
      "lineShape": "straight", "lineWidth": 1, "lineStyle": "dashed",
      "startArrow": "none", "endArrow": "none"
    }},

    { "type": "connector", "connector": {
      "from": { "x": 70, "y": 160 }, "to": { "x": 80, "y": 160 },
      "lineShape": "straight", "lineWidth": 1,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "text", "x": 20, "y": 150, "width": 50, "height": 20,
      "text": "200", "fontSize": 12, "textAlign": "right" },
    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 160 }, "to": { "x": 980, "y": 160 },
      "lineShape": "straight", "lineWidth": 1, "lineStyle": "dashed",
      "startArrow": "none", "endArrow": "none"
    }},

    { "type": "rect", "id": "bar-0", "x": 120, "y": 240,
      "width": 220, "height": 240, "borderRadius": 4 },
    { "type": "text", "x": 120, "y": 215,
      "width": 220, "height": 20,
      "text": "120", "fontSize": 14, "textAlign": "center" },
    { "type": "text", "x": 120, "y": 490,
      "width": 220, "height": 30,
      "text": "Q1", "fontSize": 14, "textAlign": "center" },

    { "type": "rect", "id": "bar-1", "x": 420, "y": 80,
      "width": 220, "height": 400, "borderRadius": 4 },
    { "type": "text", "x": 420, "y": 55,
      "width": 220, "height": 20,
      "text": "200", "fontSize": 14, "textAlign": "center" },
    { "type": "text", "x": 420, "y": 490,
      "width": 220, "height": 30,
      "text": "Q2", "fontSize": 14, "textAlign": "center" },

    { "type": "rect", "id": "bar-2", "x": 720, "y": 180,
      "width": 220, "height": 300, "borderRadius": 4 },
    { "type": "text", "x": 720, "y": 155,
      "width": 220, "height": 20,
      "text": "150", "fontSize": 14, "textAlign": "center" },
    { "type": "text", "x": 720, "y": 490,
      "width": 220, "height": 30,
      "text": "Q3", "fontSize": 14, "textAlign": "center" }
  ]
}
```

Coordinate derivation verification:
- bar-0 (120): height = (120/200)*400 = 240, y = 480-240 = 240
- bar-1 (200): height = (200/200)*400 = 400, y = 480-400 = 80
- bar-2 (150): height = (150/200)*400 = 300, y = 480-300 = 180
- bar-0 x = 80 + 0*300 + 80/2 = 120, bar-1 x = 80 + 1*300 + 40 = 420, bar-2 x = 80 + 2*300 + 40 = 720

**How ​​to run the script**:

```bash
node generate-bar-chart.js
npx -y @larksuite/whiteboard-cli@^0.1.0 -i bar-chart.json -o ./bar-chart.png
```

## trap

- Use multiple colors for a single series (unprofessional): all bars in the same data series should use the same color
- Missing Y-axis unit label, readers cannot understand the meaning of the value
- Uneven spacing between columns (the script needs to calculate barGap uniformly)
- Y-axis tick marks and grid lines have wrong arrows
- Forgot to add arrows to the coordinate axis
