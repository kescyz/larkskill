# Line chart

## Content constraints

- Data points ≤ 15
- The Y-axis must have unit labels (such as "10,000 yuan", "%")
- Polyline series ≤ 3 (too dense to see clearly)

## Layout selection

- **Script to generate coordinates** (recommended): Use .js script to calculate data point coordinates and polyline paths. After the script outputs the JSON file, call `npx -y @larksuite/whiteboard-cli@^0.1.0` for rendering.

## Layout rules

- The Y axis of the whiteboard coordinate system is positive downward, the "bottom origin" of the chart has the maximum Y value, and Y decreases when the data points are distributed upward.
- Data points are marked with small ellipse (width: 12, height: 12)
- Polyline uses connector straight to connect adjacent data points, endArrow: "none"
- The coordinate axis uses a connector straight line with an arrow at the end (endArrow: "arrow")
- Grid lines use dashed connectors (lineStyle: "dashed", endArrow: "none")
- tick mark dash connector (endArrow: "none")
- Numeric labels are placed above the data points
- Category labels are placed below the X-axis, center aligning the data points

## Coordinates and Dimensions Calculation Guide

In the whiteboard coordinate system, the X axis is positive to the right and the Y axis is positive downward. The "bottom origin" of the chart has the largest Y coordinate, which decreases as the data points move upward.

1. **Determine the chart area**:
- Set the chart area height `chartHeight` and width `chartWidth`
- Set the coordinate origin of the lower left corner `(originX, originY)`
- Example: originX=80, originY=480, chartWidth=900, chartHeight=400
2. **Y-axis range adaptation**:
- Find the minimum value of data `dataMin` and the maximum value of `dataMax`
- yMin is not necessarily 0: if the data is concentrated in 80-120, starting the Y-axis from 0 will squeeze the polyline into a small area at the top
- Recommended: yMin = round down to the appropriate scale (such as dataMin=82 → yMin=80), yMax = round up (such as dataMax=118 → yMax=120)
- When the data fluctuation is extremely small (such as 98-102), appropriately expand the range to avoid the polyline being too flat.
3. **Data point coordinate calculation**:
- X coordinate: evenly distributed within the available width. `pointX = originX + (i / (pointCount - 1)) * chartWidth`
- Y coordinate: proportionally mapped to height. `pointY = originY - ((value - yMin) / (yMax - yMin)) * chartHeight`
- ellipse positioning: `ellipseX = pointX - 6, ellipseY = pointY - 6` (center-aligned data point)
4. **Connection logic**:
- Use connector straight to connect adjacent data points
- `from` = (pointX, pointY) of point[i], `to` = (pointX, pointY) of point[i+1]
   - startArrow: "none", endArrow: "none"
5. **Y-axis scale calculation**:
- Divide yMin to yMax into 4-5 equal divisions
- Y coordinate of each tick: `gridY = originY - ((tickValue - yMin) / (yMax - yMin)) * chartHeight`

## Complete JSON example

Example below: 4 data points, data [120, 200, 150, 180], yMin=100, yMax=220, originX=80, originY=480, chartWidth=900, chartHeight=400.

- Scale: 100, 130, 160, 190, 220 (every 30)
- Point 0 (120): pointX=80, pointY=480-((120-100)/120)*400=480-66.7=413
- Point 1 (200): pointX=80+300=380, pointY=480-((200-100)/120)*400=480-333.3=147
- Point 2 (150): pointX=80+600=680, pointY=480-((150-100)/120)*400=480-166.7=313
- Point 3 (180): pointX=80+900=980, pointY=480-((180-100)/120)*400=480-266.7=213

```json
{
  "version": 2,
  "nodes": [
    { "type": "rect", "x": 0, "y": 0, "width": 1100, "height": 580 },

    { "type": "text", "x": 80, "y": 10, "width": 900, "height": "fit-content",
      "text": "Quarterly Sales Trend", "fontSize": 24, "textAlign": "center" },

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
      "text": "100", "fontSize": 12, "textAlign": "right" },

    { "type": "connector", "connector": {
      "from": { "x": 70, "y": 380 }, "to": { "x": 80, "y": 380 },
      "lineShape": "straight", "lineWidth": 1,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "text", "x": 20, "y": 370, "width": 50, "height": 20,
      "text": "130", "fontSize": 12, "textAlign": "right" },
    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 380 }, "to": { "x": 980, "y": 380 },
      "lineShape": "straight", "lineWidth": 1, "lineStyle": "dashed",
      "startArrow": "none", "endArrow": "none"
    }},

    { "type": "connector", "connector": {
      "from": { "x": 70, "y": 280 }, "to": { "x": 80, "y": 280 },
      "lineShape": "straight", "lineWidth": 1,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "text", "x": 20, "y": 270, "width": 50, "height": 20,
      "text": "160", "fontSize": 12, "textAlign": "right" },
    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 280 }, "to": { "x": 980, "y": 280 },
      "lineShape": "straight", "lineWidth": 1, "lineStyle": "dashed",
      "startArrow": "none", "endArrow": "none"
    }},

    { "type": "connector", "connector": {
      "from": { "x": 70, "y": 180 }, "to": { "x": 80, "y": 180 },
      "lineShape": "straight", "lineWidth": 1,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "text", "x": 20, "y": 170, "width": 50, "height": 20,
      "text": "190", "fontSize": 12, "textAlign": "right" },
    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 180 }, "to": { "x": 980, "y": 180 },
      "lineShape": "straight", "lineWidth": 1, "lineStyle": "dashed",
      "startArrow": "none", "endArrow": "none"
    }},

    { "type": "connector", "connector": {
      "from": { "x": 70, "y": 80 }, "to": { "x": 80, "y": 80 },
      "lineShape": "straight", "lineWidth": 1,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "text", "x": 20, "y": 70, "width": 50, "height": 20,
      "text": "220", "fontSize": 12, "textAlign": "right" },
    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 80 }, "to": { "x": 980, "y": 80 },
      "lineShape": "straight", "lineWidth": 1, "lineStyle": "dashed",
      "startArrow": "none", "endArrow": "none"
    }},

    { "type": "connector", "connector": {
      "from": { "x": 80, "y": 413 }, "to": { "x": 380, "y": 147 },
      "lineShape": "straight", "lineWidth": 3,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "connector", "connector": {
      "from": { "x": 380, "y": 147 }, "to": { "x": 680, "y": 313 },
      "lineShape": "straight", "lineWidth": 3,
      "startArrow": "none", "endArrow": "none"
    }},
    { "type": "connector", "connector": {
      "from": { "x": 680, "y": 313 }, "to": { "x": 980, "y": 213 },
      "lineShape": "straight", "lineWidth": 3,
      "startArrow": "none", "endArrow": "none"
    }},

    { "type": "ellipse", "id": "pt-0", "x": 74, "y": 407,
      "width": 12, "height": 12 },
    { "type": "text", "x": 55, "y": 383,
      "width": 50, "height": 20,
      "text": "120", "fontSize": 14, "textAlign": "center" },
    { "type": "text", "x": 50, "y": 490,
      "width": 60, "height": 30,
      "text": "Q1", "fontSize": 14, "textAlign": "center" },

    { "type": "ellipse", "id": "pt-1", "x": 374, "y": 141,
      "width": 12, "height": 12 },
    { "type": "text", "x": 355, "y": 117,
      "width": 50, "height": 20,
      "text": "200", "fontSize": 14, "textAlign": "center" },
    { "type": "text", "x": 350, "y": 490,
      "width": 60, "height": 30,
      "text": "Q2", "fontSize": 14, "textAlign": "center" },

    { "type": "ellipse", "id": "pt-2", "x": 674, "y": 307,
      "width": 12, "height": 12 },
    { "type": "text", "x": 655, "y": 283,
      "width": 50, "height": 20,
      "text": "150", "fontSize": 14, "textAlign": "center" },
    { "type": "text", "x": 650, "y": 490,
      "width": 60, "height": 30,
      "text": "Q3", "fontSize": 14, "textAlign": "center" },

    { "type": "ellipse", "id": "pt-3", "x": 974, "y": 207,
      "width": 12, "height": 12 },
    { "type": "text", "x": 955, "y": 183,
      "width": 50, "height": 20,
      "text": "180", "fontSize": 14, "textAlign": "center" },
    { "type": "text", "x": 950, "y": 490,
      "width": 60, "height": 30,
      "text": "Q4", "fontSize": 14, "textAlign": "center" }
  ]
}
```

Coordinate derivation verification:
- Point 0 (Q1, 120): pointX = 80 + (0/3)*900 = 80, pointY = 480 - ((120-100)/120)*400 = 413
- Point 1 (Q2, 200): pointX = 80 + (1/3)*900 = 380, pointY = 480 - ((200-100)/120)*400 = 147
- Point 2 (Q3, 150): pointX = 80 + (2/3)*900 = 680, pointY = 480 - ((150-100)/120)*400 = 313
- Point 3 (Q4, 180): pointX = 80 + (3/3)*900 = 980, pointY = 480 - ((180-100)/120)*400 = 213
- ellipse positioning: ellipseX = pointX - 6, ellipseY = pointY - 6

**How ​​to run the script**:

```bash
node generate-line-chart.js
npx -y @larksuite/whiteboard-cli@^0.1.0 -i line-chart.json -o ./line-chart.png
```

## trap

- The Y-axis range is unreasonable: If the data is concentrated in 80-120, the Y-axis from 0 to 120 will cause the polyline to be squeezed into a small area at the top. yMin should be set close to the minimum value of the data
- Missing Y-axis unit label, readers cannot understand the meaning of the value
- When the data points are too dense, the labels will block each other (for more than 10 points, consider labeling every other point)
- Forgot to set endArrow: "none" for the polyline segment, which defaults to arrow
- When there are multiple series, the polyline colors are similar and difficult to distinguish, so different colors with high contrast should be used.
