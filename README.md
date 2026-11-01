# Skills

A collection of custom [Claude Skills](https://www.anthropic.com/news/skills): packaged instruction sets that teach Claude Code specific workflows. This is not a software project. There is no build system or test suite, and "development" means writing and refining each skill's Markdown instructions.

## Skills

| Skill | What it does | Group |
| --- | --- | --- |
| [`product-request-loop`](#product-request-loop) | Socratic review of a product request | Product |
| [`functional-requirements-analyst`](#functional-requirements-analyst) | Turns a raw idea into a requirements spec | Product |
| [`idea-market-research`](#idea-market-research) | Market research and a success score for an idea | Product |
| [`svg-flowchart`](#svg-flowchart) | Standalone HTML/SVG flowchart | Diagrams |
| [`generate-image`](#generate-image) | Text-to-image with a local Flux Klein service | Media (local) |
| [`generate-audio`](#generate-audio) | Text-to-speech WAV with a local Kokoro service | Media (local) |

### Product skills

#### `product-request-loop`

Runs a Socratic, first-principles review of an incoming product request (feature request, user story, ticket, stakeholder ask) against a continuous **Understand → Decide → Deliver → Learn** loop. It triggers when someone acting as a product manager or owner wants feedback, prioritization help, or a sanity check, especially when a request jumps straight to a solution without a stated customer problem, rationale, or success metric.

It walks through the stages the request hasn't answered, names common anti-patterns (solution-first requests, evidence-free urgency, scope that isn't a thin slice, no falsifiable learning step), and drills into the one assumption the request depends on most. It ends with a structured markdown summary, based on `assets/summary-template.md`, that can be attached to the ticket.

#### `functional-requirements-analyst`

Turns a raw idea, ticket, or Slack message into an unambiguous requirements specification a dev team can build from: functional requirements, business rules, edge cases, non-functional requirements, and testable acceptance criteria. It deliberately excludes implementation, architecture, tech stack, and API/database design. It states what the system must do, never how to build it. It can also clean up an existing draft that has technical solutioning mixed in.

It asks only the clarifying questions that would change the document, picks a fitting format (user stories, numbered requirements, or use cases, with templates in `references/formats.md`), drafts the full document, and finishes with a self-check for leaked technical detail.

#### `idea-market-research`

Runs a structured market-research pass on a product or app idea and delivers a living doc covering user segments, pain points, the competitive landscape, and a calibrated success-rate score out of 10 with reasoning. It first asks 2-3 short clarifying questions (market scope, depth, any known angle). In unattended runs it uses defaults and states its assumptions at the top of the doc.

### Diagrams

#### `svg-flowchart`

Generates a single self-contained HTML file with an inline SVG flowchart or decision tree: no external libraries and no images, so it opens in any browser. It triggers on requests like "make a flowchart", "draw a decision tree", or "visualise this process". It confirms the process logic, label language (defaults to the user's language), and file name (defaults to `flowchart.html`).

### Media generation (local services)

These two skills call MCP tools backed by **local models**, not a hosted API. The models must be running and reachable through the `flux-klein` MCP server for the skills to work. Both use a short clickable wizard to collect input and then call the tools directly, never an HTTP endpoint.

#### `generate-image`

Generates an image from a text-only prompt with [FLUX.2-klein-4B](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B). The wizard collects the user's choices and builds one English prompt. Generation is asynchronous: the skill starts a job and then polls for the result before showing the image inline. Width and height are capped at 1024, and there is no negative prompt, so exclusions go in the prompt text. It also responds to `/flux-klein`, and triggers on English and Dutch phrasing ("generate an image", "maak een afbeelding").

MCP tools used: `start_image_generation`, `get_image_result`, `service_health`.

#### `generate-audio`

Generates a spoken WAV file from text with a local Kokoro text-to-speech service. The wizard collects the text, voice, speed, and an optional file name. It speaks the text exactly as given (no rewriting or translating), calls the tool as soon as the wizard is complete, saves the WAV, and returns the file to the conversation. It is for speech only.

MCP tool used: `generate_speech`.

## Repository layout

Each skill lives in its own top-level folder:

```
<skill-name>/
├── SKILL.md          # instructions + YAML frontmatter (name, description)
├── references/       # optional docs the skill loads on demand
└── assets/           # optional templates the skill references
```

- `SKILL.md`'s frontmatter `description` is what Claude Code uses to decide when to invoke the skill. `name` must match the folder name.
- `functional-requirements-analyst/` keeps supporting docs in `references/`. `product-request-loop/` keeps its template in `assets/`.
- `product-request-loop/` also ships a packaged `product-request-loop.skill`, a zip archive of the skill folder for distribution. It is the only skill packaged this way so far.
- `idea-market-research/SKILL.md` currently has no YAML frontmatter, so it won't auto-trigger until `name` and `description` are added.
- Templates use `{{placeholder}}` syntax. Keep placeholder names consistent between a skill's instructions and its template.

See `CLAUDE.md` for guidance on editing skills in this repo.

## Installing a skill

For a plain source folder (such as `functional-requirements-analyst/`), point Claude Code at the folder or copy it into your skills directory (for example `~/.claude/skills/`).

For a packaged `.skill` file, install it in Claude Code or unzip it yourself:

```
unzip "product-request-loop/product-request-loop.skill" -d <destination>
```

To inspect a package without extracting it, run `unzip -l "<path>.skill"`. To rebuild one after editing, zip the skill folder (with `SKILL.md` at its root and any `assets/`) into `<skill-name>.skill`.
