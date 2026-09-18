# Idea Market Research

Runs a structured market-research pass on a product or app idea the user gives you, and delivers a living doc covering user segments, pain points, competitive landscape, and a calibrated success-rate score.

## 1. Clarify briefly, then go

Before starting research, ask 2-3 short clarifying questions with AskUserQuestion — don't skip this just because the goal (evaluate this idea) is already clear:

- Geographic/market scope (default: global, note this as the default option)
- Depth: solid overview vs. deep dive (default: deep dive — this skill exists for thorough passes)
- Anything already known or assumed: a specific angle, target user, or differentiation idea the research should test against, if the user has one in mind

If the session is clearly unattended (e.g. a scheduled run) or the user isn't there to answer, skip the questions, use the defaults above, and state the assumptions plainly at the top of the doc instead of blocking.

## 2. Research checklist (non-negotiable)

The research must cover all of the following before writing anything up:

1. **Key users** — who they are (demographics, life stage), their motivations, and the distinct segments among them (don't treat the audience as one blob)
2. **Pain points** — the underlying need or frustration driving demand, not just surface complaints
3. **Struggles with current options** — concrete, sourced complaints about existing products in this space: what users say is broken, tedious, expensive, or missing (app/product reviews, forums, newsletters, comparison articles)
4. **Market** — size and growth (with an honest read on source quality — see below), and the trends/drivers behind it
5. **Competitive environment** — the key players, their positioning/pricing, funding and traction signals, and market history (notable failures, acquisitions, consolidation); explicitly assess how crowded and differentiated the space is
6. **Success-rate score** — an X/10 with explicit reasoning (see methodology below)

## 3. Research approach

- Search broadly: comparison/review articles, app store or product reviews, forums and newsletters for qualitative complaints, startup/funding news, and academic or industry studies where they exist — academic/peer-reviewed sources are worth extra effort to find, they're rare in this kind of research and carry more weight.
- Prefer primary quotes and concrete numbers over generic marketing claims.
- Flag generic SEO "market report" mills (no named methodology, produced by content farms) and treat their sizing numbers as directional only, not precise.
- Call out when comparison/ranking content is published by a competing product itself — that's marketing, not a neutral source, even when it reads like one.
- If the idea doesn't map cleanly onto an existing, well-documented market, say so explicitly and research the closest adjacent category instead, explaining the gap rather than forcing a fit.

## 4. Success-rate score methodology

Score 1-10: the odds of this idea, built by a generic new entrant, reaching real and sustained success (profitability or a strong acquisition) — not just shipping or getting downloads.

- Start from a low base rate: most consumer/software products do not reach sustained success.
- Adjust **up** for: validated and growing demand, a clearly underserved segment or niche, a genuinely unsolved pain point the idea could credibly address, low switching costs for users, a differentiation angle that isn't already crowded.
- Adjust **down** for: a crowded competitive field, a history of failed or acquired-then-discontinued entrants in the category, no proven monetization model among existing players, or a structural problem (e.g. onboarding friction, trust, retention) that well-funded competitors have already tried and failed to solve.
- Give **one** score with the reasoning spelled out — don't hedge with a range as the primary answer, though it's fine to note what would move the score ("rises to X/10 if it specifically solves Y").
- Be honest and calibrated, not encouraging. This is a feasibility check, not a pitch deck — don't inflate the score to soften bad news, and don't undersell a genuinely good signal either.

## 5. Output

Deliver the research as a living doc (Claude Docs), not a chat summary or a file, using the standard create-outline-then-fill flow. Structure the doc as:

1. TL;DR — the headline read, including the success-rate score up front
2. Market size & growth
3. Landscape: key players (table — positioning, pricing, standout feature, known weakness)
4. Who the users are (segments, motivations, any hard data on behavior)
5. Pain points & struggles with current options
6. Business models & monetization patterns, if the category has established ones
7. Competitive dynamics & history (funding, consolidation, how crowded/differentiated it is)
8. Success-rate score & reasoning (can restate/expand on the TL;DR version)
9. Opportunities/gaps for this specific idea, if the research surfaced a clear one
10. Sources

Cite sources inline throughout, not just in the sources list. End the chat reply with one short line pointing to the doc — never a text summary of its contents.