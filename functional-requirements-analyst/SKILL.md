---
name: functional-requirements-analyst
description: Turns a product owner's raw idea, ticket, Slack message, or "wouldn't it be nice if..." into a clean, unambiguous requirements specification a development team can build from — functional requirements, business rules, edge cases, non-functional requirements, and testable acceptance criteria, deliberately leaving out any technical implementation, architecture, tech-stack, or API/database design. Use this whenever someone is acting as a functional analyst, business analyst, or product owner and wants to "write up requirements," "turn this idea into a spec," "break this feature down for dev," "document what the system should do," draft user stories with acceptance criteria, or hand off a vague ask to engineering — even if they never say "functional analyst" or "requirements document." Also use it to review or clean up an existing requirements draft that has technical solutioning mixed into it.
---

# Functional Requirements Analyst

## What this skill is for

A product owner's idea usually arrives messy: a Slack message, a half-formed user story, a "can we also make it so..." tacked onto a meeting. Someone has to turn that into something a development team can actually estimate and build without guessing. That's the job here — act as the functional analyst standing between the idea and the backlog.

The one rule that shapes everything else: **write down what the system must do, never how it should be built.** A requirement says "the system must prevent a customer from submitting an order with a quantity of zero." It does not say "add a client-side validation check using a regex on the quantity field." The first survives a rewrite in a different framework, a different database, a different team. The second is an implementation detail masquerading as a requirement, and it quietly removes the development team's ability to make their own technical calls — which is usually exactly the judgment they're best placed to make. Every step below exists to keep that line intact.

## Step 1 — Understand the idea before writing anything

Read (or ask for) the raw idea and pull out, in your own head, four things: the problem or opportunity being addressed, who is acting (which user, role, or system), what triggers the behavior, and what outcome counts as success. If the idea already contains a technical suggestion — "let's cache the results" or "we should add a webhook" — don't transcribe it. Ask yourself what underlying need that suggestion was trying to solve (faster response time? real-time notification to another system?) and write the requirement in those terms instead. The person who had the technical idea is often right that something needs to happen; they're just not always the one who should decide how.

## Step 2 — Ask the essential clarifying questions, then draft

Real requirements docs fall apart most often on things nobody thought to ask about. Before drafting, ask about whatever the idea leaves genuinely open — but ask like an analyst triaging for what actually changes the document, not like a form. A handful of questions people forget to volunteer:

- **Actors and permissions** — is this for every user, or only some role/tier/state? What happens for a logged-out or unauthorized user?
- **Data involved** — what has to be captured, shown, or changed, and does any of it already exist elsewhere in the product?
- **Boundaries and error states** — what's the correct behavior when things go wrong (empty input, duplicate, network failure, permission denied)?
- **Volume and frequency** — does this need to work for 10 records or 10 million? Once a day or continuously? (This shapes non-functional requirements, not the functional ones.)
- **Interaction with existing features** — does this replace, extend, or run alongside something that already exists?
- **Definition of done** — how will the product owner know, when it ships, that it does what they wanted?

Don't ask all six every time — a small, obviously-scoped idea might only need one or two answered. Ask the ones whose answer would actually change what you write. Whatever remains unresolved after asking — because the product owner doesn't know yet, or it's a reasonable call either way — gets carried forward explicitly as an assumption or open question in the final document (Step 4) rather than silently guessed at or used to block the whole draft.

If there's no one to ask — the idea arrives as a one-shot request, comes through an unattended or asynchronous channel, or the person has said something like "just draft it" — don't stall waiting for answers that aren't coming. Make the most reasonable call on each open point, state it plainly as an assumption, and deliver the complete document anyway. A finished draft with clearly flagged assumptions is far more useful to a product owner than no draft at all; they can correct an assumption in seconds, but they can't act on a list of unanswered questions sitting in place of the document they needed.

## Step 3 — Choose the shape of the document

Not every idea deserves the same template. Pick based on what the idea actually is, and say which you picked and why isn't usually necessary — just use it:

- **A small, self-contained feature or change** with a clear user-facing behavior → user stories ("As a [role], I want [capability], so that [benefit]") each followed by their own acceptance criteria. Fits a single backlog item or two.
- **A larger feature or initiative** touching several screens, roles, or areas of the system → a numbered functional requirements list (FR-01, FR-02, ...) grouped by area, which reads more like a spec than a backlog and is easier to review, reference in tickets, and sign off on as a whole.
- **A multi-step or branching interaction** — checkout, an approval workflow, onboarding with different paths — → use cases: actor, precondition, main flow, alternate/exception flows, postcondition. This is the only structure that makes branching logic readable; forcing it into flat user stories tends to lose the branches.

These aren't exclusive — a numbered FR document can include a use case for its one complex flow, and either structure always carries acceptance criteria per item (see Step 4). Full templates with worked examples for all three are in `references/formats.md`; open it when drafting, don't try to hold the exact layout from memory.

## Step 4 — Draft the document

Regardless of which structure you picked in Step 3, the document as a whole always includes these parts. `references/formats.md` has the full templates; this is the checklist of what must be present:

1. **Title and one-paragraph summary** — what's being requested and the business goal behind it, in plain language a non-technical stakeholder can confirm at a glance.
2. **Actors / user roles** — who or what interacts with this capability.
3. **Functional requirements** — the core of the document, in whichever shape Step 3 chose. Every individual requirement or story gets a stable ID (`FR-01`, `FR-02`, ...) so it can be referenced later from a ticket, a test case, or a future revision, and every one carries its own **acceptance criteria** — the specific, testable conditions someone would check to confirm it's done (Given/When/Then works well; a plain checklist works too). A requirement that can't be turned into a pass/fail test is usually still a vague idea, not a requirement yet — that's the signal to sharpen it rather than write it down as-is.
4. **Business rules & edge cases** — validation rules, boundary conditions, and error/exception scenarios that don't fit neatly as their own requirement but that the dev team needs to handle (what happens at zero, at the maximum, on a duplicate, on a conflict).
5. **Non-functional requirements** — performance, security, accessibility, scalability constraints, numbered `NFR-01` and so on. Keep these at requirement level too: "the search must return results within 2 seconds for a catalog of up to 100,000 items" is a requirement; "use an Elasticsearch index" is the solution to it, and belongs to engineering, not this document.
6. **Out of scope** — what this explicitly does not cover. This is one of the most valuable sections and the easiest to skip; it's what stops a developer, a QA engineer, and the product owner from three different assumptions about the boundary later.
7. **Assumptions & open questions** — anything you drafted around rather than confirmed, and anything still genuinely unresolved, listed so the product owner can close them out before or during development rather than after.

## Step 5 — Check your own draft for leaks before handing it over

Technical solutioning creeps in quietly, usually because it's the natural way people already talk about the idea. Before delivering, reread every requirement and business rule looking specifically for:

- Named technologies, frameworks, libraries, or products ("use Redis," "a React modal," "call the Stripe API")
- Architecture or design decisions ("add a new microservice," "store this in a separate table," "queue it asynchronously")
- API, schema, or data-model specifics (endpoint names, field types, table structures)
- Any sentence that reads like a solution rather than a need — if you can imagine two completely different technical implementations that would both satisfy the sentence as written, it's a requirement; if only one implementation fits, it's probably solutioning that needs rewriting back to the need underneath it.

Also check that each requirement is atomic (one requirement, one behavior — split anything joined by "and" if the two halves could be built or tested independently) and that the language is unambiguous enough for someone who wasn't in the room when the idea came up ("must," "must not," "shall" read more precisely than "should" or "can").

## Step 6 — Save and deliver

Write the finished document as a markdown file. Name it after the feature, not generically (`checkout-guest-flow-requirements.md`, not `requirements.md`), so it's identifiable once it's sitting in a folder with others.