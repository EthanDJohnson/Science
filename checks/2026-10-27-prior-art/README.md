# Prior-art check of five findings (2026-10-27)

Each finding below was something this repository's runs or checks found that looked new: a mistake in a published paper, or a result not in print. Before telling anyone, we searched for whether someone had already found it.

## How

For each finding, a workflow ran:
1. Sonnet searchers, one per angle. The angles were: who cites the paper; public discussion; the background physics; the paper's own versions; and, for Van Den Broeck, an independent recomputation.
2. An adversarial Sonnet agent that hunted for anything the searchers had missed.
3. A Sonnet citation checker that opened every source and verified each quote.
4. A judge that weighed it all, checked the finding itself against the primary source, and wrote the verdict file.

The searchers' notes are in `notes/`, and the scripts they and the judges wrote are in `calc/`.

## Verdicts

| Finding | Verdict | What is already out there | What is not | File |
|---|---|---|---|---|
| **Blas & Oller 2026**, "Gravitational waves decay in vacuum" (our check: `checks/2026-10-11-blas-oller-gw-decay/`) | Partly anticipated | The far-from-source, plane-wave limit is classic (Gibbons 1975; Liu 2007, which B&O don't cite), and B&O accept it. The identity behind our incoming-wave point (retarded − advanced = outgoing − incoming) is standard. | No paper, comment or reply makes any of our six points about B&O. The paper has no citations; it is an unpublished preprint at v2. | `blas-oller.md` |
| **Van Den Broeck 1999**: the QI section was not redone for the published parameters (quick Alcubierre run, verdict C3-0) | **Already published, informally** | L. Monti's public GitHub README (LoreMonti/Warp_Drive) states all five points with the same numbers. By its git timestamps (author-set) it is a few hours earlier than our run. A Krasnikov footnote (2002/2003) asserts a QI violation without a calculation. | Nothing peer-reviewed records the stale QI section. The judge's sibling scripts found a possibly new pointwise-QI failure (about 1e65 near w = 0.97 at both parameter sets), which needs an independent check. | `van-den-broeck.md` |
| **Gambini, Porto & Pullin 2004** (PRL): eqs. (4) and (5) disagree by (8π)²; the black-hole information claim needs the last ~10⁻¹⁹⁹ s (problem-of-time run, verdict C6-0) | Partly anticipated | The authors themselves softened the claim from 2005: the formula "is not a valid expansion for t = Tmax". Conceptual critiques exist (Okon and Sudarsky 2016; Unruh and Wald 2017). | The (8π)² inconsistency is not in print. Our numbers are not in print. | `gambini-porto-pullin.md` |
| **Fuchs et al. 2024**, the positive-energy warp shell: NEC cap ~0.024c, its wall-thickness dependence, superluminality margins, wall holonomy, stress ratio (deep warp run) | Partly anticipated | The paper itself says a shift limit exists ("a future direction of work"), that light is still delayed, and that the effect is "linear frame dragging". Le's preprints reproduced its 0.02 pass. | No value or scaling of the cap, no 0.04c failure, no superluminality margin, no stress ratio. | `fuchs-shell.md` |
| **One-sided wormhole shortcuts**: rotating the mouths doesn't escape the achronal-null-line argument (wormhole run, C6) | Partly anticipated | Dias, Frassino, Paccoia and Rocha (PRD 2023) raised the twist escape and explicitly left it open. | The finite-mouth result is not in print. The judge's independent script confirms it and finds the worst gluing analytically. | `wormhole-mouth-rotation.md` |

## Corrections to our own findings

The judges also checked each finding against its primary source. None was contradicted, but four need rewording:
- **Gambini–Porto–Pullin:** "the coefficient should be (8π)⁻⁴" over-asserts. The authors' earlier paper (hep-th/0405183) suggests eq. (4) carries the misprint, so the right claim is "eqs. (4) and (5) are inconsistent as printed". The failure of the black-hole claim holds for the printed constants only: the model's loose constants can close the 2.3–4.3× gap.
- **Van Den Broeck:** v2 is also Planck-scale. The "r_c < 32 L_P" pass condition holds only under the paper's own peak-only test.
- **Fuchs shell:** the paper's 7.6 ns light-timing value is not reconciled with our rebuild's 6.86 ns (0.02c) and 13.72 ns (0.04c); under one convention it matches β of about 0.022. Le's tail type IV against our clean tail is a regularisation difference that remains open.
- **Wormhole mouths:** Graham and Olum never use the word "shortcut" and prove the line only in the simply connected case. "No published theorem" should acknowledge Galloway's null-line construction. The band bound "at most 1.5a/c" holds only for a ≤ 0.1d.

## Is any of it worth sending?

- **Blas & Oller:** yes. A polite technical note to the authors is worthwhile, crediting Gibbons and Liu for the plane-wave limit. The reader summary for this is `checks/2026-10-11-blas-oller-gw-decay/summary/blas-oller-check-summary.pdf`.
- **Gambini–Porto–Pullin:** at most a courteous note about the eq. (4)/(5) inconsistency.
- **Van Den Broeck:** not a standalone write-up; any note should credit Monti and Krasnikov.
- **Fuchs shell and the wormhole mouths:** small results for a write-up only after an independent recomputation.

## Limits

These limits apply to every verdict:
- The arXiv search API and Semantic Scholar's citation listing were rate-limited throughout.
- Google Scholar, ResearchGate, ADS and several publisher pages were unreachable.
- Private channels such as referee reports and email can't be searched.

"Not found" means not found in what was searched. This repository is public, so our own findings have been readable since they were pushed.
