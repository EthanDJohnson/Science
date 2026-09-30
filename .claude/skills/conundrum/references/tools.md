# Tool catalog

Tested calculators and research tools in `.claude/skills/conundrum/scripts/`. Agents use these instead of re-deriving the same calculation. At framing, the main session checks a question's needs against this list (SKILL.md step 1).

Every calculator has a `selftest()` against independent reference values. The test suite runs all of them, including calculators promoted from runs.

## Calculators

| Tool | Covers | Checked against | Try it |
|---|---|---|---|
| `gr_tensors.py` | Stress-energy a metric requires; what every observer measures; energy conditions with Hawking–Ellis types; energy on a slice; curvature radius; Ford–Roman quantum-inequality bounds and Lorentzian averaging; horizons and Hawking temperatures; high-precision rechecks. Metrics: Minkowski, Schwarzschild, FRW, Morris–Thorne, Alcubierre, Van Den Broeck | Schwarzschild, FRW, Morris–Thorne, Painlevé–Gullstrand and Alcubierre closed forms | `python3 .claude/skills/conundrum/scripts/gr_tensors.py selftest` |
| `stats_tools.py` | Is a signal real? Gaussian tails; Poisson and Asimov significance with background uncertainty; look-elsewhere corrections (Šidák, Gross–Vitells); combining results (Fisher, Stouffer, weighted means with the PDG scale factor); Bayes-factor bounds; data needed for 5 sigma | Standard reference values, and mpmath to about 1e-13 | `python3 .claude/skills/conundrum/scripts/stats_tools.py selftest` |
| `unit_tools.py` | Units and dimensions: parse `"0.5 * 1 t * (3 km/s)^2"`, convert (`.to("MJ")`), check (`.expect("energy")`). SI prefixes, astronomical units, TNT, CODATA constants, Planck units | Exact SI and IAU definitions, and known values (G M_sun / c^2 = 1476.6 m) | `python3 .claude/skills/conundrum/scripts/unit_tools.py "G*Msun/c^2" --to km` |
| `rocket_tools.py` | Tsiolkovsky and relativistic (Ackeret) rocket equations; photon rocket; constant-proper-acceleration trips, with or without a coast, giving ship time, Earth time, peak speed and mass ratio | Closed forms, and the 1 g table in Gibbs and Baez, "The Relativistic Rocket" | `python3 .claude/skills/conundrum/scripts/rocket_tools.py trip --distance "4.37 ly" --accel "1 g0" --ve c` |
| `page_wootters.py` | Finite-dimensional Page–Wootters clocks (hbar = 1, energies in rad/s, SI helpers): physical states by null space and group averaging; conditional states with norm, fidelity and Schrödinger residual; effective generator (non-unitary or time-nonlocal) for degenerate, unequally spaced, finite-resolution and interacting clocks; clock resolution, speed limits and POVM defect; Smith–Ahmadi gravitational clock coupling; two-time probabilities, Kuchař's naive form versus the Giovannetti–Lloyd–Maccone memory (built as a lattice history state, not a coupled-constraint null state). Note: with no coupling, the conditional state obeys Schrödinger's equation exactly for any clock spectrum; non-ideal clocks fail by coverage, readability and degeneracy instead. Built in run 2026-09-29-problem-of-time-quantum-gravity | Rabi formula; lattice orthogonality and history state; exact resonance counting; Margolus–Levitin saturation (Physica D 120, 188); Dirichlet kernel and its large-d limit pi/sqrt(3); Smith & Ahmadi 2019 Eq. 23 and its lam → 0 limit; Gaussian characteristic function; sequential-measurement (Lüders) rule | `python3 .claude/skills/conundrum/scripts/page_wootters.py qubit --d 8 --omega "1e9 1/s" --gap "3e9 1/s" --sigma "0.1 ns"` |

## Checking tools

The math checker uses these to re-derive each lens's mathematics independently (standard and deep runs).

| Tool | Covers | Try it |
|---|---|---|
| `math_checks.py` | Identities, limits, series, signs, inequalities, quantities with units, and dimensions. SymPy first, then 50 points at 30 digits, including the domain's ends. Each check prints PASS, FAIL (with a counterexample) or UNDECIDED | `python3 .claude/skills/conundrum/scripts/math_checks.py identity "(x+1)**2" "x**2 + 2*x + 1"` |
| `math_run.py` | Runs one check script under `runs/` with a time limit, and saves its output, exit code and library versions to a log beside it | `python3 .claude/skills/conundrum/scripts/math_run.py runs/<slug>/math/<lens>/<ID>.py` |

## Research tools

| Tool | Covers |
|---|---|
| `lit_search.py` | INSPIRE-HEP, arXiv, Crossref and Semantic Scholar search, printing abstracts that can be quoted |
| `fetch_text.py` | A source's own words from a PDF or web page, around a phrase, for verbatim quotes |
| `check_env.py` | Preflight: packages, reachable sources, and how many agents run at once |
| `prior_runs.py` | Earlier runs related to a question; importing their evidence (never their conclusions) into a new run; each run's record of status, trust and notes |

## Adding a calculator

A calculator earns a place here when several agents in a run would need the same non-trivial calculation, and when that calculation is easy to get subtly wrong. One-off arithmetic doesn't qualify; agents write that in their own `calc/` scripts.

1. **At framing,** the main session proposes it to the user with the brief.
2. **During research,** a `toolsmith` agent builds it in `runs/<slug>/tools/<name>.py`, in the tool format in `schemas.md`.
3. **At the dossier checkpoint,** the main session re-runs its self-test and reviews its reference values. It then promotes the calculator into the toolkit and adds a row above, with a line on the run that built it.
