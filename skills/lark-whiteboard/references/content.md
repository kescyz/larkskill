# Content planning

Core principle: **The amount of information matches the level of detail required by the user. ** If the user says "draw a simple architecture diagram", draw the simple one, and if the user says "draw a complete microservice architecture", draw the complex one. Don’t make your own decisions and **overextend**.

**When the user prompt is short/vague** (such as "Draw a funnel chart", "Draw an architecture diagram"), don't just output the literal content. Reasonable content in this field should be appropriately supplemented

## Information volume reference

| User needs | Reasonable amount of information |
|---------|------------|
| "Draw a simple XX architecture diagram" | 3 layers, 2-3 nodes per layer, no sidebar |
| "Draw a XX architecture diagram" (common request) | 3-4 layers, 3-4 nodes per layer |
| "Draw a complete/detailed XX architecture diagram" | 4-5 layers, 4-6 nodes per layer, sidebar can be added (sidebar can have up to 2-3 items) |
| Flow chart | 6-10 steps + 1-2 conditional branches |
| Comparison table | 4-6 dimensions, 1-2 lines of description per grid |
| Organizational structure | 3-4 layers, 2-4 child nodes under each parent node |

**Node text**: Title + short description (such as "User Service\nRegistration Login and Permission Management"), do not write long paragraphs. Description should be 12 words or less.

## Grouping

2-5 nodes per group. More than 5 split into subgroups.

## Connection prediction

| Number of connections | Strategy |
|--------|------|
| ≤8 | Draw one by one |
| 9-15 | Representative connections |
| >15 | Layer-to-layer, or rollback and streamlining |

## Simplified trigger conditions

Simplify only when the layout cannot fit:

| Question | Streamlined Way |
|------|---------|
| Node text cannot fit | Shorten description text |
| There are more than 5 nodes in a row | Split into two rows or merge similar ones |
| Crossover connections | Reduce the number of connections |
