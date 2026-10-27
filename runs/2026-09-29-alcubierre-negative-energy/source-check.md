# Source check of the quick Alcubierre run (added 2026-10-27)

This quick run (2026-09-29) originally had no source checks and no audit. On 2026-10-27 its sources were checked after the fact, its report was audited, and its one finding about a published paper was checked against the literature.

## What was checked

| Check | Files | Result |
|---|---|---|
| Every research claim (RC, RQ, RT: 57 claims), by 9 Sonnet source checkers | `research/critiques.check.md`, `quantitative.check.md`, `theory.check.md` | 53 verified, 4 misattributed, 0 contradicted |
| Every claim in the earlier hand-run notes the dossier imported as U-items (RS: 26 claims), by 4 checkers | `runs/2026-09-29-warp-bubble-shapes/research/shapes.check.md` | 1 contradicted (RS-12), 1 misattributed (RS-08), 3 unverifiable (RS-03, RS-06, RS-13); the rest verified, some with caveats |
| Every quote and source attribution in the eight falsifier verdicts (97 rows), by 8 checkers | `verdicts/C*-0.check.md` | 2 misattributed, 13 unverifiable, 0 contradicted; the rest verified |
| Every factual claim in `report.md` (47 claims), by the report auditor, with the checks above applied | `audit.md` | 24 flagged, all *weak*, none contradicted |

## What the checks change

- **The Van Den Broeck finding stands on its sources.** All of the verdict's quotes are verbatim in arXiv v1, v3, v4 and v5 of gr-qc/9905084, and v5 does print femtometre parameters in eq. (7) beside the Planck-scale quantum-inequality numbers (`verdicts/C3-0.check.md`). The one unverifiable row is that v5's text matches the published CQG version, which was not opened. Someone had: a public GitHub README by L. Monti (LoreMonti/Warp_Drive) states the same points with the same numbers, timestamped a few hours before this run (author-set git timestamps). A Krasnikov footnote (2002/2003) asserts a QI violation without a calculation. Two corrections: v2 is also Planck-scale, and the r_c < 32 L_P pass condition holds only under the paper's peak-only test (`checks/2026-10-27-prior-art/van-den-broeck.md`).
- **Loup lapse (C7).** The report's numbers reproduce, but the dossier's "no published critique" is wrong: Bobrick and Martire 2021 (CQG 38, 105009, App. A.1) show that the Loup lapse metric is the Alcubierre metric in a rescaled time, so it buys no real energy reduction (RS-12, contradicted). That supports C7's own point that the Eulerian total is the wrong figure of merit.
- **Thick-wall floor, v²R/12 = 1.12e30 kg.** The auditor marked it weak because no source states it (RQ-11). It is not from a source: the constraints and engineer lenses derived it, and both confirmed it numerically to 5-6 digits. The derivation is short and was rechecked by hand on 2026-10-27. The Eulerian energy is E = −(v²/12)∫ f′² r² dr (G = c = 1). For f falling from 1 at r = R to 0 at r = R + D, Cauchy–Schwarz gives 1 = (∫ f′ dr)² ≤ ∫ f′² r² dr · ∫ r⁻² dr, so ∫ f′² r² dr ≥ R(R + D)/D. That makes E ≤ −(v²/12) R(R + D)/D, which tends to −v²R/12 as D → ∞; at R = 100 m, v = 10 it is 833 m × c²/G = 1.12e30 kg. The headline stands; its support is a calculation, not a citation.
- **Lentz (C4).** The core quotes verify, but the reading of Fell–Heisenberg's positive total as an ADM-mass boundary flux in SSV's eqs. 7.16/7.17 is the verdict's own inference (C4-0.check Q15). The later deep run (`runs/2026-10-01-warp-drive-without-negative-energy`) also replaced this run's kink-sheet mechanism: kinks add no surface term, and the bulk alone is at most −2.2 M_sun at 10c.
- **Lab sources (C5).** Sopova and Ford 2002 is paraphrased too strongly (C5-0.check Q9): their abstract allows the gap region between two dielectric half-spaces to stay net negative. Maclay and Davis 2019 is peer-reviewed (Found. Phys. 49, 797), not a preprint (RQ-14). Neither changes C5's elimination, which rests on the plate-mass bound and the proven electromagnetic QI.
- **Smaller corrections:** Olum's theorem also assumes the generic condition (RC-08); Fell–Heisenberg's example energy is about 1.0e27 kg, about 0.5 Jupiter masses, not 2e26 kg (RC-18), and their "four orders of magnitude" below the Sun is about 3.3; the Van Den Broeck neck of 3e-15 m is 1.9e19 Planck lengths, not 2e20 (RQ-15); the "~8e3×" Natário penalty and the tabulated quintic-wall ratio (3.0e4) refer to different profiles (audit row 21).
- **Still resting on search summaries:** the 16 ng antimatter total (the source page returns 403), and White's JBIS publication record (RS-03).

None of these changes a ranking. The report's caveat "Quick run, no source check" is now out of date; see the note at the end of `report.md`.
