# Smoke test: the constraints lens on the Alcubierre question

This is the output of one pipeline agent, `lens-constraints`, run once by hand on this question:

> Considering Alcubierre drives, what are viable engineering option(s) for the negative energy required to travel at superluminal effective speeds?

It tested one agent's instructions and the GR toolkit. It is not a full `/conundrum` run, so it has no candidate slate, refuters, judge or audit.

## Provenance: read before trusting anything here

- **The dossier is a hand-written fixture** of well-known results. The research stage didn't produce it, and no source checker verified it.
- **The agent was a stand-in:** a general-purpose Opus subagent, running at the session's `max` effort. It was given the lens-constraints instructions as they stood before the fixes below.
- **WebFetch to journals was blocked,** because the session started before network access was widened.
- **Every `[new: ...]` quote in the analysis is WebSearch summary text,** not verbatim source text. The agent disclosed this under "Assumptions I relied on". The current prompts require such claims to be labelled `search-summary`, never quoted.
- **The files are unchanged agent output.** Paths inside them still say `runs/smoke-constraints/`.
- **The analysis predates the analysis format's "Lens-specific outputs" section.**
- **It cost** 409k tokens, 75 tool calls and 73 minutes, for one agent.

## Files

| File | What it is |
|---|---|
| `brief.md` | The question made precise (written for the test) |
| `dossier.md` | The hand-written fixture the agent treated as its evidence base |
| `analyses/constraints.md` | The agent's analysis: findings, calculations, candidate answers, assumptions |
| `calc/*.py` | The six calculation scripts it wrote and ran |

To rerun a script, run it from the project root:

```
python3 examples/smoke-test-constraints-lens/calc/lens-constraints_qi_wall.py
```

## Headline results

| Result | Value | Script |
|---|---|---|
| Energy of a 100 m Alcubierre bubble with a 1 m wall at v = c | −6.7e46 J, i.e. −7.5e29 kg (SI) | `alcubierre_ec` |
| Thickest wall the Ford–Roman quantum inequality allows for free fields (v = c, τ0 = 0.1 × curvature radius, one field) | 51 Planck lengths = 8.3e-34 m | `qi_wall` |
| Energy of a 100 m bubble with that wall | −9.0e62 kg, about 4.5e32 solar masses | `qi_wall` |
| Casimir plates: plate rest mass over Casimir energy deficit (1 nm gap) | ≥ 7.7e9, so net positive | `sources` |
| Required energy density over ideal Casimir density (v = c, 1 m wall, 1 nm gap) | 10^33.4 | `sources` |
| Natário-class drives | Eulerian energy = −(1/32π)∫\|∇×β\|² ≤ 0, confirmed numerically to 7 digits | `natario_class` |
| Share of the wall's stress-energy the ship can't reach (v = 2c, R = 100 m, 1 m wall) | 3.0e-6 | `horizon_ctc` |
| Van Den Broeck toy model | +0.43 m total (geometric units), but with a −1.66 m negative part | `vdb` |

The agent's candidate answers:

| ID | Type | Claim | Confidence |
|---|---|---|---|
| A | null | No admissible negative-energy source can support a controllable superluminal Alcubierre, Natário or Van Den Broeck bubble at ship scale | high |
| B | reframe | Negative energy is unavoidable for every Natário-class drive and for superluminal travel generally; the positive-energy warp shells on record are subluminal | medium-high |
| C | option, strained | A microscopic Van Den Broeck bubble with Planck-thin walls. Its outer wall costs about 1e29–1e30 kg, but a tanh-shaped pocket region costs ≳ 1e60 kg, so it survives only if that region can be reshaped to satisfy the quantum inequality | low |
| D | option, speculative | Classical non-minimally coupled scalar fields evade the free-field bounds. But a v = c wall needs a field of about 3e18 GeV, near the Planck scale, and at v ≥ 2c the effective gravitational constant diverges | low |

## What this smoke test changed

| Problem found | Fix now in the pipeline |
|---|---|
| The toolkit reported the weak energy condition as satisfied at wall points where it fails, because the stress-energy there has no timelike eigenvector (Hawking–Ellis type IV) | `classify_stress_energy` and `scan_energy_conditions` classify the type and test every observer |
| Symbolic matrix inversion was slow, and every call recompiled | a closed-form 3+1 inverse (`Spacetime.from_adm`) and a compile cache |
| float64 flipped signs at large dynamic range | `precision_check` re-evaluates with mpmath |
| A NaN at r = 0 poisoned integrals | `integrate_parts` drops NaN points with a warning |
| The agent had to write its own Riemann tensor, curvature radius, quantum-inequality averaging, horizon finder and SI conversions | all are now in `gr_tensors.py` |
| WebSearch summaries were quoted as if they were source text | an `ACCESS: search-summary` level with `SUMMARY:` lines; `lit_search.py` abstracts are the quotable alternative |
| The agent killed its own shell with `pkill -f`, and a Bash call stops at 10 minutes | calculation rules for long runs: background runs, marker files, stopping processes by PID only |
| 75 tool calls against a 50-turn limit, with the analysis written near the end | call budgets, a first version written early, higher turn limits, and a `{ok, path, summary}` return so a cut-off agent counts as failed |

On 2026-09-29, rerunning all six scripts against the rewritten toolkit reproduced every headline number above. They took about 2 minutes in total, down from about 7 during the smoke test.
