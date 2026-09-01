# Skills

A collection of custom [Claude Skills](https://www.anthropic.com/news/skills) — packaged instruction sets that teach Claude Code specific workflows.

## Skills

### Product Owner / `product-request-loop`

Runs a Socratic, first-principles review of an incoming product request (feature request, user story, ticket, stakeholder ask) against a continuous **Understand → Decide → Deliver → Learn** loop. Use it when acting as a product manager/owner who wants feedback, prioritization help, or a sanity check on a request — especially one that jumps straight to a solution without a stated customer problem, rationale, or success metric.

The skill walks through whichever of the four stages the request hasn't already answered, names common anti-patterns directly (solution-first requests, evidence-free urgency, scope that isn't actually a thin slice, no falsifiable learning step), and applies a first-principles drill to the one assumption the request most depends on. It closes by writing a structured markdown summary (see `Product Owner/summary-template.md`) that can be attached to the ticket.

### `functional-requirements-analyst`

Turns a product owner's raw idea, ticket, or Slack message into a clean, unambiguous requirements specification a development team can build from — functional requirements, business rules, edge cases, non-functional requirements, and testable acceptance criteria. Deliberately excludes technical implementation, architecture, tech-stack, or API/database design, so the document states what the system must do, never how to build it. Use it to write up requirements from scratch, or to review an existing draft that has technical solutioning mixed into it and needs it separated back out.

The skill asks only the clarifying questions that would actually change the document (actors/permissions, data involved, error states, volume, interaction with existing features, definition of done), then picks the right shape for the idea — user stories, a numbered functional-requirements list, or use cases for branching flows (templates and worked examples in `functional-requirements-analyst/references/formats.md`) — and drafts a full document: summary, actors, numbered requirements with acceptance criteria, business rules & edge cases, non-functional requirements, out of scope, and assumptions/open questions. It finishes with a self-check pass to catch any technical solutioning that crept into the wording before handing the document over.

## Repository layout

Each skill lives in its own top-level folder. The two skills here currently follow slightly different conventions:

- `Product Owner/` keeps its authored source as a plainly-named `.md` file (`po-skill.md`) plus a separate asset (`summary-template.md`), and also ships a packaged `<skill-name>.skill` — a zip archive for distribution/installation, containing that source renamed to `SKILL.md` alongside an `assets/` folder.
- `functional-requirements-analyst/` follows the more standard skill layout directly: `SKILL.md` at the folder root (with the YAML frontmatter — `name`, `description` — Claude Code uses to decide when to invoke it) plus a `references/` folder for supporting docs it loads on demand (`formats.md`). It has no packaged `.skill` archive yet.

See `CLAUDE.md` for more detail on how source files and any packaged `.skill` archive relate, and guidance for editing skills in this repo.

## Installing a skill

For a skill packaged as a `.skill` file, download it and install it in Claude Code, or unzip it yourself with:

```
unzip "Product Owner/product-request-loop.skill" -d <destination>
```

For a skill that ships as a plain source folder (containing `SKILL.md` at its root, like `functional-requirements-analyst/`), point Claude Code at that folder directly.
