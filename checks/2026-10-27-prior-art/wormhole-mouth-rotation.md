# Prior art: One-sided wormhole shortcuts: rotating or misaligning the mouths does not escape the achronal-null-line argument
status: final
Checked: 2026-10-27. Finding dated 2026-10-08.

## The finding
Source: `runs/2026-10-03-traversable-wormhole-shortcuts/report.md` (C6 paragraph under "Why, candidate by candidate", and the "Finite-mouth line threshold" row of Key numbers). Calculations: `runs/2026-10-03-traversable-wormhole-shortcuts/calc/falsifier-C6-0_finite_mouth_lines.py.log` (Ellis lensing), `falsifier-C6-1_thinshell_realign.py.log` and `falsifier-C6-1_tube_realign.py.log` (thin shell and tube), `falsifier-C6-2_finite_mouth_line.py.log` (flat-exterior minimiser). Verdicts: `verdicts/C6-0.md`, `C6-1.md`, `C6-2.md`.

The finding has five points:
- **P1 (premise).** Graham and Olum 2007 (GO07; Phys. Rev. D 76, 064001, arXiv:0705.3193) tie the ban on shortcuts to a complete achronal null geodesic through the throat. Their topological-censorship theorem assumes simple connectedness. We found no published theorem that derives the complete achronal through-line for curved, back-reacted one-sided geometries.
- **P2 (the proposed escape).** If the two mouths of a one-sided wormhole are misaligned or rotated, perhaps no through-throat null line is achronal, so the ban would not apply.
- **P3 (the result).** We tested this with three finite-mouth models. Each finds a complete achronal through-throat null line for every gluing whenever the through-length L is shorter than the outside distance d. The line thresholds are L* ≈ 1.16–1.20 d at mouth radius a = 0.1 d.
- **P4.** The escape seen with point mouths is an artefact of conical mouths.
- **P5.** What survives is a band at the scale of the mouth, at most 1.5a/c wide (0.075 s for the MM 2020 mouths).

## Verdict
**Partly anticipated.** The question was raised before but not answered. Dias, Frassino, Paccoia and Rocha (PRD 107, 124056, 2023) named a "twist along the wormhole" and the orientation of the mouths as a possible way for a one-sided wormhole to avoid the achronal ANEC. They called it "unlikely" and left it as "an open possibility that requires a dedicated analysis". No paper we reached answers that question. Our answer (P3–P5) is not in the literature searched. The premise P1 was already published, by GO07 v2 itself and by later papers, so P1 is background and not part of our claim to novelty.

## Is the finding itself right?
Mostly yes, within its stated scope (flat exterior, static mouths). Two wording fixes and one qualifier are needed.

**Confirmed**
- **GO07 assumes simple connectedness, but only from v2 onwards.** Checked in GO07 v2 (27 Aug 2007, the version that matches the published PRD text) at p. 5: "We must also restrict ourselves to simply-connected spacetimes, which means that the wormholes we rule out are only those which connect one asymptotically flat region to another, not those which connect a region to itself."
- **v1 said something different.** I fetched v1 (22 May 2007). Its Theorem 1 has no simple-connectedness hypothesis, and the text says topological censorship theorems "rule out such things as traversable wormholes". The "simply" grep finds only "simply solves".
- **The numbers match the log.** `falsifier-C6-2_finite_mouth_line.py.log` gives:
  - L* = 1.2000 d (aligned), 1.1999 d (rot10), 1.1643 d (rot180 and mirror), 1.1882 d and 1.1892 d (random O(3) gluings).
  - Section 1: the worst margin over 9 gluings equals L − d for a = 0.3, 0.1, 0.01 and 0.001 d, and for L from 0 to 0.99 d.
  - Section 4: as a → 0 the minimisers become kinked at the conical mouth (10°, 180° and 180° kinks), which supports P4.
  - The Ellis-lensing log (C6-0) independently finds achronal lines for the 10°, 180° and mirror gluings at L = 0.5 d and 0.9 d. Its worst residual window is 1.40 b0.
- **Independent check of P3 and P5:** `checks/2026-10-27-prior-art/calc/wmr_band_bound.py` and its `.log`. The script uses the line criterion stated in the C6-2 log but not the run's code.
  - **Reduction.** Write m' = Gᵀm and v = Gᵀu. The minimum over the entry and exit points then depends only on Θ = ang(−u, Gᵀu), through g(Θ; L/a).
  - **Monotonic.** g is non-decreasing in Θ (checked on a grid from 0° to 180°).
  - **Worst gluing.** So G = +I (the run's "mirror", which has Θ = π for every u) bounds L*(G) from below for all G in O(3).
  - **Thresholds.** This gives L* = 1.2000 d (aligned) and 1.1643 d (worst) at a = 0.1 d, both matching the log.
  - **Every gluing has a line when L < d.** Equator-grazing entry and exit give g ≤ L/a for every gluing, so a line exists whenever L < d.
  - **Direct brute force.** 25 random O(3) gluings, minimised directly, all have a line at L = 1.16 d (margins −0.011 to −0.040 d).

**Needs correcting or qualifying**
1. **"Graham and Olum argue that a wormhole shortcut implies a complete achronal null geodesic through the throat" over-reads GO07.**
   - In GO07 v2, the word "shortcut" never occurs, and the through-line argument covers only simply connected spacetimes (wormholes joining two asymptotic regions).
   - For a one-sided wormhole, GO07 give Ford's long-throat counterexample and name the gap: "the timelike connections between points on such a path are not in the same homotopy class as the path itself."
   - The idea that a short one-sided wormhole is banned is how later papers read GO07 (Urban 2013, MMP 2018, Dias et al. 2023, Kontou 2024, Freivogel et al. 2026, Kanai et al. 2026).
   - Suggested wording: "the literature attributes to GO07 a ban on short wormholes; their theorem (v2/PRD) covers only simply connected spacetimes."
2. **"No published theorem" should be softened.**
   - Gao and Wald (2000), footnote 1, report a construction due to Galloway: when the time-delay conclusion fails, a null line (an inextendible achronal null geodesic) exists. Morales and Santillan (2022) give an independent proof.
   - That result has an uncontrolled compact region K', holds at the level of the NEC, and does not say the line crosses a throat.
   - Classical arguments that pass to the covering space also exist: FSW 1993 (full ANEC), Witten 2020 (classical NEC) and MMP footnote 2.
   - Suggested wording: no published theorem with controlled constants, for the self-consistent achronal ANEC, or for finite mouths.
3. **"At most 1.5a/c" holds only for a ≤ 0.1 d.**
   - The independent script gives a worst-gluing band of 1.15a at a = 0.001 d, 1.35a at 0.05 d, 1.50a at 0.1 d, 1.52a at 0.11 d and 1.86a at 0.3 d.
   - For MM-scale mouths (a/d ~ 10⁻⁹) the band is about (π − 2)a = 1.14a. So 0.075 s is a safe upper bound, and the actual value is about 0.057 s.
   - In the C6-2 log, the band line is a hard-coded print statement. Its inputs (the L* values) are computed.
4. **Scope.**
   - All three models have a flat exterior, a static geometry and test (not back-reacted) mouths. The report says this.
   - The claim "for every gluing" rests on continuity arguments (C6-0 winding, C6-1 choice of hit point), on samples, and on the reduction above for the tube model. It is not a theorem.
   - The upper edge of the band (an exterior wrap of at most d + πa) is a modelling choice.

**Could not check:** the curved-exterior or back-reacted case (the report's own decisive test, a near-extremal Reissner–Nordström exterior); whether Visser's polyhedral or Krasnikov's book constructions include rotated face identifications.

## Point by point
| Our point | Status | Closest prior work (citation, link, date, status) | Verified quote |
|---|---|---|---|
| P1a. GO07's theorem assumes simple connectedness | Already published (by GO07 itself; we cite it as a premise) | Graham & Olum, PRD 76, 064001, arXiv:0705.3193v2, https://arxiv.org/pdf/0705.3193v2, 27 Aug 2007 (v1 22 May 2007 lacks it), peer-reviewed. Also Freivogel, Fumagalli & Tomasevic, arXiv:2606.12528, Jun/Sep 2026, preprint, fn 3 | "We must also restrict ourselves to simply-connected spacetimes, which means that the wormholes we rule out are only those which connect one asymptotically flat region to another, not those which connect a region to itself." (GO07 v2 p.5). "Technically, the authors of [5] proved their theorem under the assumption of simply connected spacetimes, and they too acknowledge that the long-path loophole exists in non-simply connected spacetimes." (Freivogel et al. fn 3) |
| P1b. No published theorem derives the complete achronal through-line for curved, back-reacted one-sided geometries | Partly anticipated (gap stated by others; partial general results exist; no theorem found) | GO07 v2 p.5-6 (names the homotopy-class gap); Urban, PhD thesis, Tufts 2013, https://dl.tufts.edu/downloads/dn39xd33z (asserts without proof that only long one-sided wormholes escape); Gao & Wald, CQG 17, 4999 (2000), gr-qc/0007021, fn 1 (Galloway null line); Morales & Santillan, EPJC 82, 353 (2022), arXiv:2004.12523; MMP, CQG 40, 155016, arXiv:1807.04726, fn 2; Witten, RMP 92, 045004, arXiv:1901.03928 | "This can happen because the timelike connections between points on such a path are not in the same homotopy class as the path itself." (GO07 v2). "However, this version, as given in [26], only fails to censor wormholes which do not threaten causality." (Urban). "Galloway's proof of his version of Theorem 1 provides a direct construction of a null line when the conclusion of Theorem 1 fails, thereby bypassing Lemma 1" (Gao-Wald). "In classical physics the equations are local, so we can go the covering space, where it joins two different universes. In this case, the wormhole becomes short, since the two different universes are infinitely far, so it should be forbidden by causality." (MMP fn 2) |
| P2. Rotating, misaligning or twisting the mouths as a possible escape from the achronal ANEC | Partly anticipated (question raised, explicitly left open, no analysis) | Dias, Frassino, Paccoia & Rocha, "Black hole-wormhole collisions and the emergence of islands", PRD 107, 124056, arXiv:2304.06098, https://arxiv.org/pdf/2304.06098v2, Apr/Jul 2023, peer-reviewed. Weaker: Frolov, Krtous & Zelnikov, PRD 108, 024034, arXiv:2305.03887 (2023); Feng, Lemos & Matzner, PRD 103, 124037, arXiv:2105.03433 (2021) | "Other parameters of the model that might play a role are the twist along the wormhole, and the orientation of the axis connecting the two mouths compared to the planar horizon. For example, there could be a chance to create a short-lived island without any violation of the AANEC if the wormhole twists. Although this seems unlikely, it is still an open possibility that requires a dedicated analysis." (Dias et al. Sec. VI). "Obviously, there is an ambiguity in the choice of positions and orientations of the discs." (FKZ). "we shall only consider cases where the identifications are performed without twisting" (FLM) |
| P3. Finite mouths: a complete achronal through-throat null line for every gluing whenever L < d; L* ≈ 1.16-1.20 d at a = 0.1 d | Not found in the literature searched | None. Dias et al. 2023 guess the escape is "unlikely" but do no calculation | none |
| P4. The point-mouth escape is an artefact of conical mouths | Not found in the literature searched | Nearest: Feng-Lemos-Matzner 2021 (flat-exterior portals with conical or dihedral mouths, untwisted identifications only) | "we shall only consider cases where the identifications are performed without twisting, meaning that a frame transported along a straight line traveling through the wormhole does not experience any change in orientation." (FLM p.2; context only) |
| P5. A residual band at the mouth scale, at most 1.5a/c (0.075 s for MM) | Not found in the literature searched (and true only for a ≤ 0.1 d) | None | none |

## Closest prior work
- **Dias, Frassino, Paccoia, Rocha 2023**, PRD 107, 124056, arXiv:2304.06098 (v1 12 Apr 2023; v2 3 Jul 2023 matches the published version), peer-reviewed. This is the nearest prior work.
  - **Setup.** They build an "intra-universe" (one-sided) Ellis–Bronnikov wormhole with both mouths in the same universe, a distance d = 10a apart, and give it zero length. Their own gluing already fixes one orientation: "we now rotate the green 'cone' around the vertical axis by 180°".
  - **What they assume about the ANEC.** They state that the achronal ANEC forces the path through the wormhole to be longer than the path outside: "Imposing the physically-relevant achronal averaged null energy condi[tion] amounts to making the length through the wormhole longer than the direct path without crossing the wormhole [13, 34, 37]."
  - **The twist caveat.** They add: "This statement might need to be revised if a twist along the wormhole is included, as discussed in section VI."
  - **The open question.** Section VI is the passage quoted in the table. The twist remark is verified by my own fetch of v2 (pp. 9 and 12).
  - **Follow-ups.** INSPIRE lists 9 citers. Judging by title and abstract, none of them takes up the twist question.
  - **Relation to us.** They name our P2 question in their own setting and leave it open. Our P3–P5 answer it for flat-exterior finite mouths. Twisting gives no escape beyond the band at the mouth scale, and that band exists for aligned mouths too: (π − 2)a ≈ 1.14a aligned against ≤ 1.50a for the worst gluing at a = 0.1 d.
  - **What we do not answer.** Their specific island question, whether a band that narrow can still produce a short-lived island, is not addressed by our finding.
- **Graham & Olum 2007**, arXiv:0705.3193, peer-reviewed. This is the source of P1. v2 adds the simple-connectedness hypothesis, the sentence about wormholes "which connect a region to itself", and Ford's long-throat counterexample. v1 has none of these: its Theorem 1 is stated for any "asymptotically flat, globally hyperbolic space-time", and the paper says such theorems "rule out such things as traversable wormholes" (verified on v1, p. 5). GO07 do not use "shortcut" and do not mention mouth orientation.
- **Freivogel, Fumagalli, Tomasevic 2026**, arXiv:2606.12528, preprint. Footnote 3 restates GO07's simple-connectedness assumption and the long-path loophole, using the quote in the table. Elsewhere they write that short wormholes "are now ruled out by [5]" without that caveat. They explain that the step to the covering space is harmless classically but fails semiclassically (Casimir energy). Nothing on mouth orientation.
- **Maldacena, Milekhin, Popov 2018/2023**, arXiv:1807.04726, CQG 40, 155016. Footnote 2 (credited to A. Wall) gives the classical covering-space argument and notes that it fails for topology-dependent Casimir energy. Their mentions of "rotation" are about orbital motion of the mouths, not the gluing.
- **Urban 2013**, PhD thesis, Tufts, supervised by Olum. It asserts without derivation that GO07's gap "only fails to censor wormholes which do not threaten causality", meaning only long one-sided wormholes get through. It says nothing on mouth orientation.
- **Gao & Wald 2000**, footnote 1, and **Morales & Santillan 2022**. Galloway's general construction of a null line, with an uncontrolled compact region, at NEC level, and without saying the line crosses a throat. Morales and Santillan say Galloway's own proof "has never been released". This is a reason to soften "no published theorem".
- **Witten 2020** and **Friedman–Schleich–Witt 1993**. Witten says a one-sided "shortcut between two distant regions of a single asymptotically flat world" reduces to the two-world case by taking a cover "without affecting the classical null energy condition", and that the self-consistent achronal ANEC "has not been proved". FSW's proof passes to the universal cover under the full ANEC. Neither covers the case of the achronal ANEC alone.
- **Frolov, Krtous, Zelnikov 2023**, PRD 108, 024034. They build ring wormholes with both disc mouths in one flat space, note that "there is an ambiguity in the choice of positions and orientations of the discs", and then pick the coaxial case. There is no causal or ANEC test.
- **Feng, Lemos, Matzner 2021**, PRD 103, 124037. They study flat-exterior portal wormholes, the class of conical or polyhedral mouths, and set twisted identifications aside for a collision problem. There is no energy-condition test.
- **Schein, Aichelburg, Israel 1996** (PRD 54, 3800) and **Konstantinov 1997/98** (Grav. Cosmol. 3, 299). Each uses a single fixed gluing, one with a curved exterior and one with a flat exterior. Neither varies the gluing.
- **Background on the consensus that "short means banned"**, with no orientation content: Marolf & McBride 2019 (JHEP 11, 037; arXiv:1908.03998), Kontou–Sanders 2020, Kontou 2024, Kanai et al. 2026, and Emparan & Tomasevic 2022. Emparan & Tomasevic describe the identification between mouths only as a boost.

## Coverage
**Searched by the earlier agents**
- INSPIRE: all 130 INSPIRE citers of GO07, enumerated by date slices. Most were judged on title and abstract, and about 20 were grepped in full text.
- INSPIRE full-text word filters over those citers ("simply connected", "region to itself", mouths, rotated, twisted, orientation, holonomy, gluing).
- Citers of Gao–Wald, FSW, Morales–Santillan and Freivogel et al.
- Crossref, and WebSearch (standard and extended, plus queries in Scholar, arXiv-only, StackExchange, thesis and blog styles).
- Direct full-text greps of about 35 papers, plus the Urban thesis.

**Searched by me**
- Re-fetched Dias et al. v2 (pp. 8–9 and the twist passage) and GO07 v1.
- INSPIRE citers of Dias et al. (9).
- INSPIRE full-text phrase searches:
  - "twist along the wormhole" and "wormhole twists": the only hit for each is Dias et al.
  - "orientation of the mouths", "relative orientation of the mouths", "orientation of the wormhole mouths", "misaligned mouths", "twisted identification" with wormhole in the title, "identified with a rotation", "rotated relative to each other", and "twisted wormhole" together with achronal: 0 hits each.
  - "null line" together with "wormhole mouths": 3 hits (MMP, Shoshany–Hauser 1911.11590, and a 2110.14958 review), none of them relevant.
- An independent calculation (above).

**Not reached**
- Books: Visser, *Lorentzian Wormholes* (1995); Krasnikov (Springer 2018); Everett & Roman (2012).
- Pre-arXiv papers: Morris–Thorne–Yurtsever 1988, Kim–Thorne 1991, Frolov–Novikov 1990, Frolov PRD 43, 3878 (1991), and Visser PRD 41, 1116 (1990). A remark on mouth rotation there cannot be ruled out.
- Tomasevic, Universe 9, 159 (2023): MDPI returned HTTP 403, so only the abstract was read. PAPER TO REQUEST: doi:10.3390/universe9040159, to check whether it treats mouth orientation.
- Emparan & Tomasevic, "Time in traversable wormholes": cited as "in preparation" in 2021, never located.
- Olum, JBIS 68, 214 (2015): abstract only.
- Galloway's unpublished proof of the null-line proposition.

**Limits of the search tools**
- The arXiv and Semantic Scholar APIs were rate-limited (HTTP 429), and OpenAlex and Google Scholar were not queried directly.
- INSPIRE's full-text filter matches whole words and rejected some operator syntax.
- Recent 2026 preprints may lag in the index.
- Absence here means absence in what was reachable, not proof that nothing exists.

## What this means
**What is new.** The answer looks new. With finite, smooth mouths in a flat exterior, every gluing (rotated, mirrored or a random O(3)) has a complete achronal through-throat null line whenever L < d. The escape seen with point mouths comes from the conical mouth, and twisting buys at most a band at the mouth scale (≤ 1.5a for a ≤ 0.1 d, and about 1.14a for realistic a ≪ d). It answers a question that Dias, Frassino, Paccoia and Rocha (2023) posed in print and left open. Their guess that a twist escape "seems unlikely" is borne out in our models.

**What is not new.** The premise is not ours: GO07's simple-connectedness gap and the long-path loophole are in GO07 v2 and in Freivogel et al. 2026. Before any write-up, three things need fixing:
- Reword the GO07 sentence to attribute the one-sided ban to the later literature, and note the v1/v2 change.
- Soften "no published theorem" to acknowledge Galloway's null-line construction and the classical covering-space argument.
- Restrict the 1.5a/c bound to a ≤ 0.1 d.

**Is it worth writing up?** Yes, as a short note or comment, because it closes an explicitly open question. The result is negative and limited to idealised flat-exterior models, so it is not a full paper on its own. Dias et al. are the natural people to send it to, since they asked for "a dedicated analysis". It would be stronger with the curved-exterior check the run already names as its decisive test (a near-extremal Reissner–Nordström exterior with photon spheres).
