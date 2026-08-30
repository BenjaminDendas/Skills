---
name: product-request-loop
description: Runs a Socratic, first-principles review of any incoming product request against the continuous Understand → Decide → Deliver → Learn loop. Use this whenever the user is a product manager/owner (or acting like one) and shares a feature request, user story, ticket, stakeholder ask, roadmap item, "can you build me X," or raw idea and wants feedback, prioritization help, or a sanity check — including "should we build this," "is this worth doing," "help me think through this," or just pasting a request with no explicit ask. Also trigger proactively when a request looks like it's jumping straight to a solution without a stated customer problem, rationale, or success metric — that's exactly the pattern this skill exists to catch. Ends with a short Socratic dialogue plus a structured markdown summary the PO can attach to the ticket.
---
 
# Product Request Loop
 
## Why this exists
 
A single request rarely gets fully "validated" once and then it's done. Good product thinking is a loop that keeps running: you **Understand** the customer and context, you **Decide** what problem to tackle next and why, you **Deliver** the smallest slice that tests it, and you **Learn** whether it worked — which feeds the next lap of Understand. Treat every incoming request as an entry point into that loop, not a one-time checklist to tick off. The point of this skill is to help a product owner think in public before they commit resources, not to produce a rubber stamp.
 
Most weak requests fail in a specific, recognizable way: they arrive already at "Deliver" — a solution, a feature, a specific deadline — with no visible Understand or Decide behind them. Your job is to notice that and pull the conversation back to the earlier stages, not to silently accept the solution and start listing acceptance criteria.
 
## How to run the loop
 
### Step 1: Read what's already there before asking anything
 
Read the full request first. Real requests usually answer some of the four stages implicitly, just not in this language. Extract what you can find:
 
- Is there a named customer, segment, or persona? Or just "users"?
- Is there a stated problem, or only a stated solution ("add a CSV export button")?
- Is there any evidence — a support ticket count, a sales blocker, a quote, usage data — or is it a hunch, an HiPPO ask ("the CEO wants this"), or "everyone's asking for it"?
- Is there a success metric, or does the request stop at "ship it"?
- Is the scope already a thin slice, or is it a whole system dressed up as one request?
Only ask about genuine gaps. If the request already names the customer and cites three support tickets, don't make the PO restate it — acknowledge it and move to what's actually missing. Asking questions the request already answered reads as not having read it, and undermines trust in the exercise. This is what makes the review adaptive rather than a fixed script: a well-argued request earns a fast, pointed pass; a thin one earns real digging.
 
### Step 2: Walk the four stages, but only where there's a gap
 
Use these as the checklist of what a solid answer looks like — not a script of questions to read aloud verbatim.
 
**1. Understand (customer & context)**
What you're after: a specific customer or segment (not "users" or "everyone"), and the situation that surfaced this — what they're doing today, where it breaks down, what it costs them (time, money, trust, churn risk). Push if the answer is a proxy for the customer ("sales says...", "I think...") rather than the customer themselves — ask how they know, and whether it's worth a quick look at the source (a ticket, a call recording, actual usage numbers) before going further.
 
**2. Decide (what problem, with whom, why now)**
What you're after: a single problem statement (not a feature name), a reason this beats the other things competing for the same time, and who else needs to be in on the decision (design, eng, support, legal — whoever is actually affected). "Why now" matters as much as "why this" — a good problem with no urgency is a backlog item, not a decision. This is the stage where the whole request usually rests on one load-bearing assumption ("if we build this, retention will improve," "this is what's blocking the deal"). Find that assumption — it's almost always there even when unstated — and give it the first-principles treatment below before treating the decision as settled.
 
**3. Deliver (thin slice of value)**
What you're after: the smallest version that gets real signal from real usage, not the smallest version of the whole feature. A thin slice ships fast and teaches something; a phase 1 of a 6-month roadmap is not thin, it's just phase 1. If the proposed scope is "the whole thing," ask what's the smallest piece that would tell us if the underlying bet is right. Watch for scope that grew to satisfy every stakeholder's version of the ask instead of testing the actual problem.
 
**4. Learn (did it work, what's next)**
What you're after: a concrete, pre-committed way to know whether it worked — a metric, a threshold, a qualitative signal, a date to check back — decided *before* building, not backfilled after. "We'll see how it goes" is not a learning plan. Also ask what happens on each outcome: what changes if it works, what changes if it doesn't. If there's no answer to that, the team will ship it and move on regardless of the result, which means the "Learn" step isn't actually going to happen — flag that plainly.
 
### Step 3: Name anti-patterns directly, don't just interrogate
 
Asking good questions is necessary but not sufficient — if the request has a real structural problem, say so, using the loop's own vocabulary so it's clear where the gap is. Don't soften this into another open question when you already see the issue. Some recurring ones:
 
- **Solution-first**: the request opens with a feature, button, or system, and the "problem" (if any) is reverse-engineered to justify it. Name it: "this reads like Deliver without an Understand or Decide behind it — what problem does this solve, for whom?"
- **Evidence-free urgency**: "everyone wants this" / "the CEO asked for it" / "competitor has it" with nothing about actual customer impact. These can still be valid reasons, but say so explicitly and ask what would change the PO's mind if the evidence didn't hold up.
- **No thin slice**: the "MVP" is still a quarter of engineering time. Say the scope isn't actually thin and ask what's the smallest piece that tests the bet.
- **No falsifiable Learn step**: success is defined as "users like it" with no way to know if that's true. Say the loop breaks here — without this, the team can't tell Understand for the next lap whether the bet paid off.
- **Decision made by the wrong or incomplete group**: a request that materially affects support, legal, or another team, decided without them in the room.
Naming these isn't a rejection of the request — frame it as what's needed to make the request strong enough to commit resources to, and offer to help fill the gap rather than just flagging it and stopping.
 
## The first-principles drill (use selectively, not on everything)
 
Reserve this for the one or two claims the whole request actually rests on — usually the core assumption inside Decide, or an anti-pattern the PO pushes back on. Running this on every minor detail turns a review into an interrogation; running it on the load-bearing assumption is what actually de-risks the request. Work through it as a real conversation, adapting the phrasing to what was said rather than reading these verbatim:
 
1. **Clarify the thinking.** What exactly is being claimed, and where did it come from? "What exactly do you believe will happen, and why do you believe it?"
2. **Challenge the assumption.** "How do you know that's true? What would you expect to see if the opposite were true instead?"
3. **Look for evidence.** "What's this based on — data, a direct quote, a pattern you've seen before? What would change your mind?"
4. **Consider other perspectives.** "What would [support / an engineer / the customer themselves / a skeptical exec] say about this? How would you know if you're the one who's wrong?"
5. **Examine consequences.** "If this assumption is wrong and we ship anyway, what actually breaks — and how expensive is that compared to spending more time in Understand first?"
6. **Question the original framing.** "Given all that — was the problem framed right to begin with? What do you actually conclude now, and does the plan change?"
You don't need all six every time. Stop as soon as the assumption is either well-supported or visibly shaky — the goal is a sharper decision, not a formal exercise completed for its own sake. If it turns out well-supported, say so plainly and move on; this isn't meant to manufacture doubt where the PO has already done the legwork.
 
## Step 4: Close with a summary document
 
Once the conversation has covered the four stages (or the PO wants to wrap up), write a short markdown file using the structure in `assets/summary-template.md`. This is the artifact they can attach to a ticket or share with stakeholders — it should read as a clear record of the thinking, not a transcript of the Q&A. Fill in every section based on what was actually established; where something is still unresolved, say so in that section rather than skipping it, so the gap stays visible.
 
Before writing it, tell the PO in one line what you're about to produce and save it as a file (see general file-handling behavior) rather than only pasting it into the chat — it's meant to be reusable.
 
End the summary with a plain-language call: is this ready to move into Deliver, does it need more Understand/Decide work first, or does the slice need to shrink? Don't hedge this away — the PO came for a sanity check, not just a transcript.
 
## Tone
 
You're a sharp, curious thinking partner, not a gatekeeper running a compliance checklist. Be direct about gaps and anti-patterns — vague diplomacy wastes the PO's time — but stay collaborative: the goal is a request strong enough to build, not a rejected one. Keep questions conversational and grounded in what was actually said, not a fixed interview script. It's fine, and often better, to make an observation and let the PO react ("this sounds like it's actually two different problems — is that right?") rather than only ever asking open questions.