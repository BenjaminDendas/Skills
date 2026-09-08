---
name: svg-flowchart
description: Generate a standalone HTML file containing an SVG flowchart / decision tree diagram. Trigger when the user asks to "make a flowchart", "draw a decision tree", "visualise a process", "create a diagram", or provides a branching logic / process description and wants a visual output.
---

# Skill: svg-flowchart

This skill produces a **single self-contained HTML file** with an inline SVG flowchart. No external libraries, no images — just one file the user can open in any browser.

## Before you start

Ask (or infer from context) the following if not already clear:
1. **What is the process / logic?** Steps, branches, conditions, outcomes.
2. **What language** should labels be in? (default: same language as user's request)
3. **What filename** should the output have? (default: `flowchart.html`)
4. **Colour theme** — default is generic brand (primary blue `#6B8CAE`, black `#000000`, white `#fff`, light blue tint `#8A96A3`). Ask only if user explicitly wants a different palette.

Do **not** guess business logic. If the branching rules are unclear, ask before drawing.

---

## Design rules (non-negotiable)

### Layout
- Flow runs **top-to-bottom**. Left/right branches for binary splits, additional branches spread horizontally.
- **Minimum vertical gap between rows: 80px.** More for rows with many siblings or long edge labels.
- **Minimum horizontal gap between sibling nodes: 40px** (measure from box edge to box edge, not centre-to-centre).
- Nodes must **never overlap** each other or their edge labels.
- **Cross-branch collision rule:** boxes from different branches (e.g. a left-side training note and a right-side cross-cutting block) can share the same vertical space on screen even if they belong to separate subtrees. Before finalising any y-coordinate, check the full horizontal extent (`x` to `x + width`) of every box at that y-range across ALL branches — not just the current branch. If any two boxes share overlapping x- and y-ranges, push the lower one down until there is at least 20px of vertical clearance.
- SVG `width` and `height` must be large enough to fit all content with ≥ 30px padding on every side. When in doubt, go bigger.
- Use `viewBox="0 0 W H"` matching `width` and `height`.

### Node types and visual style

| Type | Shape | Fill | Stroke | Text colour |
|---|---|---|---|---|
| **Root / Start** | `<circle r="30">` | `#000000` | none | `#fff` bold |
| **Decision node** | `<polygon>` (diamond) | `#fff` | `#6B8CAE` 1.2px | `#6B8CAE` |
| **Outcome / Action** | `<rect rx="6">` | `#6B8CAE` | none | `#fff` bold |
| **Info / Note box** | `<rect rx="6">` | `#8A96A3` | `#6B8CAE` 1px | `#6B8CAE` |

- **Every flowchart MUST begin with a START node** — a black filled circle (`<circle>`) with the label "START" in white bold text. Never omit this node, even for simple diagrams.
- The START node is always a `<circle r="30">` with `fill="#000000"` and white text. Never use a rect for the start node.
- Standard node size: **160–220px wide × 40–60px tall** depending on text length.
- Decision nodes use a `<polygon>` diamond shape, not a rect. Size it so the widest label fits with ≥ 10px padding.
- Multi-line text: use multiple `<text>` elements with `dy="1.2em"` increments; centre-align with `text-anchor="middle"` at the node's centre x.
- Font: `Arial, sans-serif`. Sizes: root/skill labels 11–12px bold; decision labels 11px; edge labels 10px bold `#6B8CAE`.

### Edges
- Use `<line>` or `<path>` with `stroke="#999" stroke-width="1.5" fill="none"`.
- Edge labels: place midway along the edge, offset 6px to the right of the line. Class `edge-label`: `font-size:10px; fill:#6B8CAE; font-weight:bold`.
- Lines connect from the **bottom-centre** of a parent node to the **top-centre** of a child node (or side-centre for horizontal splits).

### CSS classes (include in `<style>`)
```css
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
h1 { color: #6B8CAE; font-size: 20px; margin-bottom: 20px;
     border-left: 4px solid #6B8CAE; padding-left: 10px; }
svg { display: block; margin: 0 auto; }
.edge { stroke: #999; stroke-width: 1.5; fill: none; }
.edge-label { font-size: 10px; fill: #6B8CAE; font-weight: bold; }
.skill-text { fill: #fff; font-weight: bold; font-size: 11px; }
.root-text  { fill: #fff; font-weight: bold; font-size: 12px; }
```

### Legend (always include at bottom of SVG)
```svg
<rect x="20" y="{bottom-30}" width="16" height="16" fill="#6B8CAE" rx="3"/>
<text x="42" y="{bottom-17}" font-size="11" fill="#6B8CAE">Outcome</text>
<polygon points="...diamond..." fill="#fff" stroke="#6B8CAE" stroke-width="1.2"/>
<text x="152" y="{bottom-17}" font-size="11" fill="#6B8CAE">Decision</text>
<rect x="250" y="{bottom-30}" width="16" height="16" fill="#000000" rx="3"/>
<text x="272" y="{bottom-17}" font-size="11" fill="#6B8CAE">Start</text>
```

---

## Coordinate planning (do this mentally before writing SVG)

1. **Count the levels** (rows) in the tree. Assign each a y-baseline. Start at y=20, add at least 100px per level (more if a level has many nodes or long labels).
2. **Count the nodes per level**. Space them evenly across the available width. For a tree with max N nodes on one row, width ≥ N × 200px.
3. **Sketch branch connections** — make sure edge label text won't collide with node boxes.
4. Only then write the SVG coordinates.

---

## Output format

Deliver a single `.html` file with this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{Diagram title}</title>
  <style>
    /* CSS classes listed above */
  </style>
</head>
<body>
  <h1>{Diagram title}</h1>
  <svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">
    <!-- nodes and edges -->
    <!-- legend -->
  </svg>
</body>
</html>
```

---

## Workflow

1. **Parse** the user's process/logic into a tree or graph structure (levels, nodes, edges, labels).
2. **Plan coordinates** per the planning rules above — write them out as a quick mental table before coding.
3. **Write the HTML/SVG** following all design rules.
4. **Self-check before delivering:**
   - [ ] No nodes overlap — check every sibling pair on the same row **and** every pair of boxes from different branches that occupy the same y-range.
   - [ ] No edge label collides with a node box.
   - [ ] SVG width/height fits all content + 30px padding.
   - [ ] All node types use the correct colour/style.
   - [ ] Legend is present.
   - [ ] File is self-contained (no external URLs).

---

## Finishing

Always end with:
1. A 3–5 line self-evaluation: which layout choices were made, what might need tweaking if the user has more nodes.
2. The path to the generated `.html` file so the user can open it directly.
