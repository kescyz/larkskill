# Mermaid chart path

This scenario is mutually exclusive with DSL paths.

| | DSL Path | Mermaid Path |
|---|---|---|
| Intermediate format | JSON (WBDocument) | Mermaid text (.mmd file) |
| Layout control | Precise control (x/y coordinates, Flex) | Automatic layout by parser-kit |
| Visual customization | Full control (color, font size, rounded corners, etc.) | Limited (Mermaid syntax) |
| Reference module | references/ + corresponding scene | This file only |

## Applicable conditions

Use when any of the following conditions are met:
- The user explicitly requested "Use Mermaid" or "Export Mermaid"
- User pasted Mermaid syntax text directly
- Diagram types are mind maps, sequence diagrams, class diagrams, pie charts, flow charts (automatic routing)

## CLI usage

```bash
npx -y @larksuite/whiteboard-cli@^0.1.0 -i diagram.mmd -o output.png
```

## Mindmap

```mermaid
mindmap
  root((topic))
    Branch A
      Sub-item A1
      Sub-item A2
    Branch B
      Sub-item B1
    Branch C
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant A as browser
    participant B as server
    participant C as database
    A->>B: Request data
    B->>C: Query
    C-->>B: Return results
    B-->>A: response data
```

Message type:
- `->>` solid arrow (synchronous request)
- `-->>` dashed arrow (responsive/asynchronous)
- `-x` with x arrow (fails)

## Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +fetch()
    }
    Animal <|-- Dog
```

## Pie Chart

```mermaid
pie title distribution
    "Category A" : 40
    "Category B" : 30
    "Category C" : 20
    "Category D" : 10
```

## Flowchart

Suitable for: business processes, approval flows, order processing processes and other scenarios with clear sequences and branch judgments.

```mermaid
flowchart TD
    A([Start]) --> B{Conditional judgment}
    B -->|Yes| C[Processing steps]
    B -->|No| D[Another step]
    C --> E([End])
    D --> E
```

### Constraints and specifications

- **Node text ≤ 8 words** (if more than necessary, add a legend if necessary)
- Judgment nodes (diamond-shaped) only write conditional keywords and do not write long descriptions
- Number of steps ≤ 12 (more steps need to be merged or split into sub-processes)
- Follow standard flowchart notation: stadium shape or circle `A([start])` for start/end, diamond `B{judgement}` for judgment, rectangle `C[step]` for steps

### Grammar reference

Direction: `TD` (top to bottom), `LR` (left to right), `BT` (bottom to top), `RL` (right to left)

Node shape: `A[rectangle]`, `A(rounded corners)`, `A{rhombus}`, `A((circle))`, `A([stadium])`, `A[[subroutine]]`

Connections: `-->` (solid line), `-.->` (dotted line), `==>` (thick line), `-->|label|` (with label)

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: Request received
    Processing --> Success : Processing is successful
    Processing --> Failed: Processing failed
    Success --> [*]
    Failed --> Idle : Try again
```

## Other supported chart types

- **Gantt Chart**: `gantt`
- **ER Diagram**: `erDiagram`
- **Git branch graph**: `gitGraph`

## Notes

- Output plain Mermaid text, not JSON, don't mix DSL
- When the node text contains special characters, wrap it in double quotes: `A["Text containing (brackets)"]`
- `subgraph` for logical grouping
- The flow chart defaults to `TD` (top to bottom). If the process is wider (many steps but shallow levels), use `LR` (left to right).
