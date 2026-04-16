# Comparison chart / matrix chart

Applicable to scenarios where multiple options are compared in multiple dimensions such as solution comparison, function matrix, technology selection, etc.

## Content constraints

- **Each box should be enriched**: Don't just write one keyword, give specific instructions (such as "MVCC multi-version concurrency control, supports row-level locks" instead of just "support")
- Different cells of single cell content are allowed different lengths, but each cell should not exceed 5 lines.
- For long text (more than 15 words) use `textAlign: "left"` (do not center)
- The first row is the header row (object name) and the first column is the dimension label column
- The number of dimensions must be at least 4 to fully expand the comparison dimensions

## Layout selection

| Mode | Applicable Conditions | Characteristics |
|------|---------|------|
| **Strict grid (default)** | All comparison scenarios | Header row + data row, horizontal frame for each row, rect within the row equally divided |
| **Card-style comparison (alternative)** | Fewer dimensions (2-3) | Make an independent card for each object, and list each dimension vertically in the card. Cards are equally divided horizontally: outer layer `layout: "horizontal"`, each card `width: "fill-container"` |

## Layout rules

- Outermost frame: `layout: "vertical"`, fixed `width` (such as 1000), `height: "fit-content"`
- Each row: horizontal frame, `width: "fill-container"`, `alignItems: "stretch"`
- All cells in the row `width: "fill-container"` equal the column width
- `gap >= 12` between lines (not 8, too tight)
- `gap: 8-12` between rows and columns
- Title row: white text on dark background (specific color controlled by style)
- Same color borders for each column to maintain visual consistency
- Cell `height: "fit-content"`, do not write fixed height

## Skeleton example

### 3 columns 4 rows table

```json
{
  "version": 2,
  "nodes": [
    {
      "type": "frame",
      "width": 1000,
      "height": "fit-content",
      "layout": "vertical",
      "gap": 12,
      "padding": 0,
      "children": [
        {
          "type": "text",
          "id": "title",
          "width": "fill-container",
          "height": "fit-content",
          "text": "[Comparison chart title]",
          "fontSize": 24,
          "textAlign": "center",
          "verticalAlign": "middle"
        },
        {
          "type": "frame",
          "id": "header-row",
          "width": "fill-container",
          "height": "fit-content",
          "layout": "horizontal",
          "gap": 8,
          "padding": 0,
          "alignItems": "stretch",
          "children": [
            { "type": "rect", "id": "h-dim", "width": "fill-container", "height": "fit-content", "text": "[dimension]", "fontSize": 15, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 0, "borderWidth": 2 },
            { "type": "rect", "id": "h-col-1", "width": "fill-container", "height": "fit-content", "text": "[Object A]", "fontSize": 15, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "h-col-2", "width": "fill-container", "height": "fit-content", "text": "[Object B]", "fontSize": 15, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "h-col-3", "width": "fill-container", "height": "fit-content", "text": "[Object C]", "fontSize": 15, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 }
          ]
        },
        {
          "type": "frame",
          "id": "data-row-1",
          "width": "fill-container",
          "height": "fit-content",
          "layout": "horizontal",
          "gap": 8,
          "padding": 0,
          "alignItems": "stretch",
          "children": [
            { "type": "rect", "id": "d1-dim", "width": "fill-container", "height": "fit-content", "text": "[dimension 1]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "d1-c1", "width": "fill-container", "height": "fit-content", "text": "[...]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "d1-c2", "width": "fill-container", "height": "fit-content", "text": "[...]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "d1-c3", "width": "fill-container", "height": "fit-content", "text": "[...]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 }
          ]
        },
        {
          "type": "frame",
          "id": "data-row-2",
          "width": "fill-container",
          "height": "fit-content",
          "layout": "horizontal",
          "gap": 8,
          "padding": 0,
          "alignItems": "stretch",
          "children": [
            { "type": "rect", "id": "d2-dim", "width": "fill-container", "height": "fit-content", "text": "[Dimension 2]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "d2-c1", "width": "fill-container", "height": "fit-content", "text": "[...]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "d2-c2", "width": "fill-container", "height": "fit-content", "text": "[...]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "d2-c3", "width": "fill-container", "height": "fit-content", "text": "[...]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 }
          ]
        },
        {
          "type": "frame",
          "id": "data-row-3",
          "width": "fill-container",
          "height": "fit-content",
          "layout": "horizontal",
          "gap": 8,
          "padding": 0,
          "alignItems": "stretch",
          "children": [
            { "type": "rect", "id": "d3-dim", "width": "fill-container", "height": "fit-content", "text": "[Dimension 3]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "d3-c1", "width": "fill-container", "height": "fit-content", "text": "[...]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "d3-c2", "width": "fill-container", "height": "fit-content", "text": "[...]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 },
            { "type": "rect", "id": "d3-c3", "width": "fill-container", "height": "fit-content", "text": "[...]", "fontSize": 14, "textAlign": "center", "verticalAlign": "middle", "borderRadius": 8, "borderWidth": 2 }
          ]
        }
      ]
    }
  ]
}
```

## trap

- **Line spacing 8px is too tight**: The gap between lines is at least 12, 8 will make the lines visually sticky.
- **Center alignment of long text**: Text that exceeds one line should be changed to `textAlign: "left"`. Centered multi-line text is less readable.
- **Too many columns cause each column to be too narrow**: It is recommended that the comparison object should be ≤ 5 columns (including dimension columns). If it exceeds, the dimensions will be merged or split into multiple tables.
- **Unequal column widths**: All data columns must be equally divided with `width: "fill-container"`. Do not write a fixed width for a certain column.
- **Row heights vary**: The frame of each row must have `alignItems: "stretch"`, otherwise the cells in the same row will be uneven in height due to the different number of lines of text.
- **Forgot the dimension label column**: The first column holds the dimension name, and the header row (dimension column) has a different visual treatment than the data column.
- **Cells with fixed height**: Cells must have `height: "fit-content"`, fixed height will cause text to be truncated.
