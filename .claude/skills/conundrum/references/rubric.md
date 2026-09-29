# Adjudication rubric and report format

The adjudicator reads `brief.md`, `dossier.md`, `candidates.md`, every `verdicts/*.md`, every `cruxes/*.md` if present, and any calculation files those cite. It writes `report.md`.

## How to weigh evidence

1. **Judge evidence, not eloquence.** A verdict counts for what its calculation, quote or inconsistency shows, not for its confidence, length or rhetoric. Read the calculations it cites; don't trust summaries of them.
2. **Evidence hierarchy**, strongest first:
   - a theorem or a computed result with visible code;
   - a peer-reviewed measurement;
   - a review or textbook;
   - a single preprint;
   - secondary press;
   - fringe sources.
   Evidence marked ACCESS=snippet, or flagged unverifiable, counts for less. Say where that changed a ranking.
3. **Refutation beats support.** A computed violation of an established bound outweighs any number of plausibility arguments. Check the calculation's assumptions before accepting it.
4. **Separate "in principle" from "in practice"** for feasibility and design questions.
   - *In principle*: consistent with admissible physics, and under which assumptions?
   - *In practice*: how many orders of magnitude separate what is required from what has been demonstrated, and what is the technology readiness level (TRL 1–9)?
5. **Stay calibrated.**
   - Avoid 0 and 1.
   - Go below 0.05 only for a candidate that violates a computed, established bound.
   - Go above 0.95 only with a theorem or several independent measurements behind it.
   - For each headline number, say what would move it by 2×.
6. **Mutually exclusive candidates** (explanations) get a probability distribution that sums to 1, including an explicit "none of these".
   **Non-exclusive candidates** (options) each get an independent credence of viability, and the null candidate gets its own.
7. **Don't break ties by length or position.** Order does not signal strength. When two candidates are close, compare them directly on their decisive tests.

## report.md format

```
# <Title>: report
*Run <slug> · <date> · depth <depth> · question: "<question as asked>"*

## Bottom line
3–5 plain-language sentences a smart non-specialist can act on. State the headline answer,
its confidence, and the single biggest reason.

## Ranked answers
| # | Candidate | In principle | In practice (horizon) | Key obstacle | Gap (orders of magnitude) | Credence |
|---|---|---|---|---|---|---|
(For explanation-type questions, replace the two feasibility columns with "Fits the evidence?")

## Why, candidate by candidate
For each surviving candidate: strongest evidence for, strongest against, decisive test.

## Eliminated, and what eliminated them
One line each, citing the verdict file and its basis.

## Assumptions every surviving answer shares
If one of these is wrong, the ranking changes.

## What would change this verdict
The 1–3 results, calculations or discoveries that would move the headline most.

## Key numbers
| Quantity | Value (units) | Source or calc |

## Caveats
Snippet-only evidence, blocked sources, unresolved contradictions, speculative physics used.

## Sources
The references actually relied on, with URLs.
```

Keep the report under about 1,500 words, excluding tables and sources. Put detail in the run's other files and point to them.
