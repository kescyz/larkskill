# Typesetting rules

## Font size level table

| Level | Font Size | Purpose | Alignment |
|------|------|------|------|
| H1 | 24-28 | Chart title (one per chart) | center |
| H2 | 18-20 | Partition/layer labels | right (side label) or center (top label) |
| H3 | 15-16 | Group title, card title | center or left |
| Body | 14 | Text, node text | center (short label) or left (long text) |
| Caption | 13 | Auxiliary instructions and annotations | left |

rule:
- No more than 3 font size levels for the same picture
- The fontSize of nodes at the same level must be exactly the same
- Font size difference between adjacent levels >= 4px

---

## Alignment rules

Shape nodes default to `textAlign: 'center'` + `verticalAlign: 'middle'` (opposite of CSS). If left alignment is required, it must be explicitly declared.

| Content type | Alignment |
|---------|---------|
| Short text (<=15 words) | center |
| Long text (>15 words) | left |
| Side label (layer name, partition name) | right |
| chart title | center |
| Multi-line description/paragraph | left |

---

## Chart title

Use independent text nodes and do not use the `title` attribute of the frame.

- Flex layout: placed in the first child of the outermost frame, `width: "fill-container"`
- Absolute positioning: width is set to the overall width of the chart, `textAlign: "center"`

---

## Split the title and description into two nodes

When displaying the name and description in a card, use frame to wrap the two text nodes and do not stuff them into the same shape:

```json
{
  "type": "frame", "layout": "vertical", "gap": 4, "padding": 12,
  "width": "fill-container", "height": "fit-content",
  "borderWidth": 2, "borderRadius": 8,
  "children": [
    { "type": "text", "width": "fill-container", "height": "fit-content",
      "text": "User Service", "fontSize": 16 },
    { "type": "text", "width": "fill-container", "height": "fit-content",
      "text": "Processing registration, login and personal information management", "fontSize": 13 }
  ]
}
```

---

## Size rules

Nodes containing text `height` must use `'fit-content'`. Setting the height to a dead height will truncate the text.

All nodes must explicitly declare `width` and `height`.
