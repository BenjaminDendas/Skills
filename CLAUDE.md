# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is not a software codebase — it's a source repository for **Claude Skills**: packaged instruction sets that teach Claude Code a specific workflow. There is no build system, package manager, linter, or test suite. "Development" here means writing and refining the skill's Markdown instructions, then packaging them into the distributable `.skill` format.

## Repository structure

Each skill lives in its own top-level folder (currently `Product Owner/` and `flux-klein/`). Inside a skill folder:

- `<skill-name-in-source-form>.md` (e.g. `po-skill.md`) — the authored source of the skill. Its YAML frontmatter (`name`, `description`) is what Claude Code uses to decide when to invoke the skill, so the `description` field must be specific enough to trigger on the right user intents and phrasing.
- `summary-template.md` (or similarly named asset files) — supporting templates/assets the skill's instructions reference (e.g. via `assets/summary-template.md`).
- `<skill-name>.skill` — a **zip archive** (not readable as text) that packages the skill for distribution/installation. It contains:
  - `<skill-name>/SKILL.md` — the source `.md` file, renamed to `SKILL.md`
  - `<skill-name>/assets/<...>` — any asset/template files the skill references

The `.skill` file is a packaged artifact of the source `.md` + asset files, analogous to a build output. When editing a skill's behavior, edit the source `.md` and asset files, then repackage the `.skill` archive (zip the folder containing `SKILL.md` and its `assets/` subfolder) — don't try to hand-edit the zip contents in place.

## Working with skill files

- Skill `.md` files are prompts, not code: treat wording changes as behavior changes. Read the whole file before editing a section, since instructions cross-reference each other (e.g. step ordering, tone guidance, references to `assets/summary-template.md`).
- Preserve the YAML frontmatter contract: `name` must match the skill's folder/package name, and `description` is the sole signal Claude Code uses for auto-invocation — write it to cover the range of phrasings a user might actually type.
- Template files referenced by a skill (e.g. `summary-template.md`) use `{{placeholder}}` syntax; keep placeholder names consistent between the skill's instructions and the template itself.
- To inspect a `.skill` archive's contents without extracting: `unzip -l "path/to/name.skill"`. To rebuild one after editing source files, zip the skill's folder (containing `SKILL.md` at its root and any `assets/` subdirectory) into `<skill-name>.skill`.

## flux-klein

`flux-klein/` contains a single `SKILL.md` (no `.skill` package yet) for generating images from text prompts via the flux-klein MCP tools.

**Note:** this skill relies on a **local setup** of FLUX.2-klein-4B from Hugging Face (https://huggingface.co/black-forest-labs/FLUX.2-klein-4B), not a hosted API. The model must be running locally for the skill to work.
