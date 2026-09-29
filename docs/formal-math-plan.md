# Formal mathematics for `/conundrum`: review and plan

*Status: proposal, not built. Reviewed 2026-09-29. The cloud facts were checked the same day in this repository's cloud environment.*

## The proposal

A Gemini-drafted proposal asks for two tiers of mathematical checking, aimed at questions such as the Problem of Time or interpretations of quantum mechanics:

1. **A computer algebra scratchpad.** The analysts write SymPy scripts, using the `tensor` and `physics` modules, to derive field equations and test ideas instead of doing algebra in prose.
2. **Lean 4 as the verifier.** A new "Formalization Worker" translates the analysts' equations into Lean 4 files and recompiles them until the proof compiles or a contradiction appears. It writes the compiler output to a "Math Status" file that the analysts' next debate turn must build on.

It also asks that the skill install its tools itself (`python3`, `pip`, `sympy`, and Lean through `elan`) in local and cloud sessions alike. It asks for the Formalization Worker's instructions, and for how the `.py` and `.lean` files are run and their output fed back.

## Verdict

Keep the goal, but change the design.

- **The SymPy tier is right, and mostly already built.** What's missing is an independent check of each lens's math.
- **Lean is worth adding only as a narrow, optional check** for pure-math lemmas, installed once with the user's consent. It shouldn't be the "ultimate verifier" of physics claims.
- **For Problem-of-Time and interpretation questions, the bigger gap isn't algebra.** The judge's scoring rules were built for feasibility questions.

## Evaluation

### What it gets right

LLM algebra slips are real. Building this pipeline hit three:
- a toolkit bug that passed the weak energy condition where it fails;
- a statistics formula that lost precision;
- a wrong tidal measure for a warp-bubble ship.

An independent check caught each one; more careful prose would not have.

### Where it doesn't fit

1. **The SymPy tier mostly exists.** Every lens and refuter already writes SymPy scripts in `calc/` and cites them. `gr_tensors.py` is a tested SymPy toolkit for GR, and the judge already ranks "a computed result with visible code" highest.
   - What's missing is anyone re-deriving a lens's math independently. The pipeline checks sources, not derivations.
   - SymPy's abstract-index tensor module is weak. Computing tensors component by component, as `gr_tensors.py` does, is more reliable.
   - Canonical machinery such as Poisson or Dirac brackets is covered by the calculator-on-demand step at framing.
2. **Lean checks the Lean statement, not the physics.** Translating a claim into Lean is itself an LLM step, and that's where errors would hide:
   - a weakened statement;
   - an extra hypothesis;
   - a definition that makes the claim trivially true.

   A proof of a mis-stated theorem earns a "verified" stamp it doesn't deserve. That's worse than an honest "unverified".
3. **Most of this physics is out of Mathlib's reach.**
   - As far as we know, Mathlib has manifolds, Hilbert spaces and operators, but not the curvature machinery GR needs.
   - The Wheeler–DeWitt equation and path integrals aren't rigorously defined mathematics at all.
   - What can be formalized is mostly finite-dimensional algebra and inequalities, which SymPy checks in seconds.
4. **"Compile until it passes or a contradiction is found" has no useful stopping point.** A compile error means the proof attempt failed; it says nothing about whether the math is contradictory. Lean can't tell "false" from "I couldn't prove it". Only a proof of the negation disproves a claim.
5. **Wrong stage, and no turns to feed.** Derivations happen in the analysis stage (lenses and refuters), not in research. The lenses deliberately don't debate in turns: they work independently, and their results flow forward to the candidate slate, the refuters and the judge.
6. **Installing mid-run is the fragile part.**
   - Mathlib's prebuilt cache is blocked by this environment's default network access. It comes from `cache.mathlib.org` since September 2026, and from `lakecache.blob.core.windows.net` before that and as a fallback. Building Mathlib from source instead takes hours.
   - The cache costs several GB, and more time per fresh session.
   - Running a downloaded install script inside an unattended run is a supply-chain risk that auto mode may refuse. On the user's own computer, it would install software without asking.
7. **The bigger gap for these questions.** The report scores options "in principle / in practice / orders-of-magnitude gap". QM interpretations are mostly empirically equivalent, and Problem-of-Time positions differ in what they give up. They need scoring on internal consistency, what they give up, and testability.

### Where Lean does earn a place

- **A pure-math lemma the question hinges on:** an inequality, a linear-algebra fact, or a finite-dimensional version of the Page–Wootters construction.
- **Whether a set of premises is consistent,** as in Frauchiger–Renner-style no-go arguments. Formalizing forces hidden premises into the open, which is what the brief's "premises to test" is for.

## Implementation plan

Merge PR #2 (earlier runs) first; this work touches the same agent files.

### Phase 1a: independent math checks with SymPy (same local and cloud)

1. **`math_checks.py`** (toolkit): checks identities, limits, series expansions, signs, inequalities and units (through `unit_tools.py`).
   - Each check tries SymPy symbolically, then confirms at 50 random points at 30-digit precision with mpmath, because SymPy failing to simplify proves nothing.
   - It returns pass, fail with a counterexample, or undecided, and tests itself against known identities.
2. **`math_run.py`** (toolkit): runs one check script with a timeout, and saves its output, errors, exit code, run time and library versions to a log beside the script. The existing allow rule covers it, so there are no new permission prompts.
3. **A `math-checker` agent** (Opus):
   - It reads one lens's analysis and lists its load-bearing math: equations, derived results, signs, scaling laws and numbers.
   - It re-derives each claim in a fresh script, never the lens's own.
   - It writes `math/<lens>.md`, marking each claim verified, refuted (with the counterexample or corrected form) or unverified (with the reason). Each row cites its log.
   - It tags the claims a formalizer could take.
4. **`conundrum-analyze.js`:**
   - Each lens hands off to its math checker as soon as it finishes, in standard and deep runs. Quick runs skip it, as they skip source checks.
   - The candidate builder, refuters, crux advocates and judge all read the status files.
   - Refuted math can't support a candidate, and a refuter can cite it as a calculation.
5. **File formats and judge rules:**
   - Add the status format to `schemas.md`.
   - In `rubric.md`: refuted math eliminates a candidate, unverified math counts less, and a reviewed formal proof ranks with theorems.
   - The auditor traces the report's math claims to status rows.
6. **Preflight:** report the SymPy and mpmath versions.
7. **Tests:**
   - helper self-tests;
   - runner timeouts and output capture;
   - one checker per lens, with quick runs skipping it;
   - a failed checker never blocks the candidate slate;
   - wiring checks across the skill, schemas and agents.

Rough cost: one more Opus agent per lens, perhaps +$15–30 on a standard run. That's a guess until measured with `dev/run_costs.py`.

### Phase 1b: a `foundations` question type

- **Scope:** questions about consistency and interpretation.
- **Default lenses:** examiner, decomposer, dialectician, idealizer and constraints.
- **Candidate answers are positions:** resolve the problem, dissolve it, modify the theory, or call it ill-posed.
- **Report columns:**
  - internally consistent (taken from the math checks);
  - what the position gives up;
  - empirically distinguishable or equivalent;
  - open problems.
- **Ranking:** where positions are empirically equivalent, the judge ranks them by what they give up, and says so, rather than inventing probabilities.

### Phase 2: optional Lean checks (experimental)

1. **A pinned `lean/` project:** a fixed Lean toolchain, a fixed Mathlib version with its manifest committed, `.lake/` ignored by git, and a smoke-test file.
2. **`dev/setup_lean.sh`**, safe to re-run. It:
   - checks free disk space;
   - downloads a pinned elan release and verifies its checksum, rather than piping an install script into the shell;
   - fetches Mathlib's prebuilt cache;
   - compiles the smoke test;
   - names any host the network refused.
3. **Preflight and framing.**
   - The preflight reports whether Lean is ready.
   - At framing, Claude offers formal checks only for questions that hinge on formalizable math.
   - If Lean is missing, Claude asks before running the setup script.
   - If the user declines or the network blocks it, formal checks are skipped and the report says so.
4. **`lean_check.py`** (toolkit):
   - compiles one file in the pinned project, with a timeout;
   - rejects `sorry`, `admit`, `axiom`, `native_decide`, `unsafe` and `implemented_by`;
   - runs `#print axioms` and accepts only Lean's three standard axioms, which catches `sorry` and `native_decide` a second way;
   - saves a log and a status.

   A `--statement-only` flag allows `sorry` while the formalizer checks that its statement compiles.
5. **A formalizer (draft below) plus a statement reviewer** (Sonnet). The reviewer reads only the Lean theorem, writes what it says in plain math, then compares that with the original claim and lists every difference. Only a proof whose statement survives review counts as formally verified.
6. **In the workflow:** after the math checks, at most 3 tagged claims (6 in deep runs) go to formalizers, then to reviewers. Each ends as proved, disproved (its negation proved), not settled, or not formalizable. It is never reported as "contradiction found".
7. **Tests:** fixture files for the rejection rules; compile tests that skip unless Lean is installed; workflow tests with the mock runtime.

## The proposal's three constraints

### 1. Installing what's needed

| | Local terminal | Cloud session |
|---|---|---|
| python3, pip | Already required, since the hooks run on python3 | Already installed |
| SymPy, mpmath | Preflight checks and asks before `pip install` | Setup script (already in the README) |
| Lean + Mathlib | `dev/setup_lean.sh` once, after the user approves (several GB) | The same script in the environment's setup script, plus the Mathlib cache hosts on the network allowlist |
| Missing at run time | Formal checks skipped, and the report says so | Same |

### 2. Formalization worker instructions (draft)

Its budget, checkpoint and path rules would be generated by `dev/agent_rules.py` like the other agents'.

```markdown
---
name: formalizer
description: Conundrum pipeline formalizer. States one mathematical claim as a Lean 4 theorem and tries to prove or disprove it. No physics. Use only when the conundrum workflow asks for it.
tools: Read, Write, Edit, Bash
model: opus
effort: high
maxTurns: 45
---

You translate one mathematical claim into Lean 4 with Mathlib and try to settle it. You do not do
physics, judge the argument it came from, or propose better claims. Your prompt names the run
directory, the claim ID and the status file that holds it.

1. Read only the claim, its symbols and its stated assumptions, not the analysis it came from.
2. State it first. In `runs/<slug>/math/formal/<ID>.lean`, write
   `theorem claim_<ID> : <statement> := by sorry`.
   - Every assumption becomes an explicit hypothesis. Use Mathlib's definitions, and define
     nothing that could make the claim trivially true.
   - If it can't be stated with Mathlib (it needs path integrals, the curvature of a general
     spacetime, or anything else Mathlib lacks), stop and report `not formalizable`, saying what
     is missing.
3. Check that the statement compiles:
   `python3 .claude/skills/conundrum/scripts/lean_check.py <file> --statement-only`.
4. Prove it, compiling after each change, within about 25 compiles. If it stalls, try proving
   the negation as `theorem negation_<ID> : ¬ (<statement>)`.
5. Never use `sorry`, `admit`, `axiom`, `native_decide`, `unsafe` or `implemented_by`.
   `lean_check.py` rejects them and lists the axioms your proof depends on.
6. Write `runs/<slug>/math/formal/<ID>.md` with:
   - the Lean statement, and what it says in plain math;
   - every way it is narrower than the claim or differs from it: a fixed dimension, real
     instead of complex numbers, extra hypotheses;
   - the outcome;
   - the last compiler output.

A compile error is a fact about your Lean file, never evidence about the mathematics or the
physics. Report it as `not settled`, never as a contradiction. Only a proof of the negation
disproves a claim.

Finish by returning `ok`, `path`, `outcome` (proved | disproved | not settled | not formalizable)
and `summary`.
```

### 3. Files and execution

```
runs/<slug>/math/
  <lens>.md                      status table, one row per claim (math checker)
  <lens>/M-<LENS>-03.py          fresh re-derivation
  <lens>/M-<LENS>-03.py.log      output, errors, exit code, versions (math_run.py)
  formal/M-<LENS>-03.lean        statement and proof (formalizer)
  formal/M-<LENS>-03.log         compiler output and axioms (lean_check.py)
  formal/M-<LENS>-03.md          outcome, and how the statement differs from the claim
  formal/M-<LENS>-03.review.md   the reviewer's reading and comparison
```

- **Nothing runs bare.** Agents never run code or redirect output themselves: `math_run.py` and `lean_check.py` run it with timeouts and save the logs. Every status row cites a file anyone can re-run.
- **No shared files.** Each checker writes its own status file, so agents working in parallel never edit the same file.
- **Who reads what.** Later agents read the status files; the judge and auditor open the logs when a claim matters.

## Cloud environment facts (checked 2026-09-29)

- **The VM:** 16 GB of RAM, 30 GB of disk and 4 CPUs, so 2 agents run at once. Mathlib's cache fits.
- **Reachable at the default "Trusted" network level:**
  - PyPI;
  - `raw.githubusercontent.com`;
  - a Lean toolchain download from GitHub releases;
  - a `git ls-remote` of Mathlib.
- **Blocked at "Trusted":** `cache.mathlib.org`, where Mathlib's cache tool reads since September 2026, and `lakecache.blob.core.windows.net`, its legacy fallback and older versions' host.
- **GitHub release downloads may be limited.** The docs say GitHub release-asset requests can be limited to repositories attached to the session. The Lean toolchain download worked anyway. The download of `leantar` (from `digama0/leangz`), which Mathlib's cache tool also needs, is untested.
- **Setup scripts are cached only when they finish in about five minutes.** The Mathlib download may not fit. The docs suggest running a long download from a SessionStart hook in the background instead.
- **To allow the hosts:**
  1. Edit the environment at claude.ai/code or in the Desktop app; the mobile app can't edit environments.
  2. Set **Network access** to **Custom**.
  3. List the two hosts under **Allowed domains**.
  4. Check **Also include default list of common package managers** to keep the Trusted list.

## Sequencing

1. Merge PR #2.
2. Build Phases 1a and 1b, and measure their cost on a real run.
3. Hold Phase 2 until a theory-heavy run shows claims that SymPy can't settle but Lean could. Its cloud prerequisite is the network change above.
