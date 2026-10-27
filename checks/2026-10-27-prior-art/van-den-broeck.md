# Prior art: Van Den Broeck 1999's quantum-inequality check was not redone for the published parameters
status: final
Checked: 2026-10-27. Finding dated 2026-09-29.

## The finding
Source: `runs/2026-09-29-alcubierre-negative-energy/verdicts/C3-0.md`, a falsifier's verdict from a quick run whose sources had not been independently checked before today. Its calculations are `runs/2026-09-29-alcubierre-negative-energy/calc/falsifier-C3-0_vdb_qi.py` and `lens-constraints_vdb_curvature.py`.

The paper is C. Van Den Broeck, "A `warp drive' with more reasonable total energy requirements", Class. Quantum Grav. 16, 3973 (1999), arXiv:gr-qc/9905084. The finding makes five points:

1. **Parameters changed between versions.** arXiv v1, v3 and v4 use Planck-scale pocket parameters in eq. (7): alpha = 1e34, Delta~ = R~ = 1e-32 m, R = 3e-32 m. v5, which carries the CQG journal reference, changes eq. (7) to femtometre values: alpha = 1e17, Delta~ = R~ = 1e-15 m, R = 3e-15 m. It adds "The value of R in (7) is roughly the largest that keeps |EIV| below a solar mass for vs ≃ 1."
2. **v5's QI section is stale.** It still prints the old numbers: the peak at w = 0.349, r_c,min = Delta~/72.5 = 1.4e-34 m, -6.6e93 against -9.2e94 kg/m^3, and "the QI is amply satisfied". With v5's own Delta~ = 1e-15 m, Delta~/72.5 is 1.4e-17 m.
3. **Recomputation at the published parameters.** The density peak is at w = 0.576 with rho = -2.37e59 kg/m^3, and r_c = 2.3e-17 m. The Ford-Roman bound with tau0 = 0.1 r_c is violated by about 2.0e33. With the v1-v4 parameters, the same code reproduces the paper's printed QI numbers exactly.
4. **Pass condition.** For this profile family, the QI passes only if r_c is below about 32 Planck lengths (Delta~ < 3.7e-32 m).
5. **Conclusion.** The published claim that the QI is "amply satisfied" does not hold for the published parameters.

## Verdict
**Already published, informally and only hours earlier. In the formal literature it is only partly anticipated.**

The public GitHub repository LoreMonti/Warp_Drive (Lorenzo Monti) states all five points, with the same numbers. Its commit history dates the result to 2026-09-29 16:01 UTC. Our run was framed at 18:25 UTC and our verdict was committed at 21:02 UTC the same day. Those git timestamps are author-set and could not be checked against any external record.

No paper, erratum or review makes the point. The only peer-reviewed precedent is a footnote by Krasnikov (arXiv v1 July 2002; PRD 67, 104013, 2003). It says, without a calculation, that Van Den Broeck's profile violates the QI. That claim is about a different region of the profile and does not mention the version or parameter mismatch.

## Is the finding itself right?
**Yes, on every point that could be checked against the primary source, with two qualifications.** One is a minor omission; the other is a reading on which the finding is too lenient.

**Confirmed directly from the arXiv text (all five versions were read by sibling agents; I re-printed the key passages today):**
- **The eq. (7) change.** v1-v4 print "α = 10 34, ˜∆ = 10 −32 m, ˜R = 10 −32 m R = 3 × 10−32 m. (7)". v5 prints "α = 10 17, ˜∆ = 10 −15 m, ˜R = 10 −15 m, R = 3 × 10−15 m. (7)".
  - Today's re-print of v5 p. 7 reads: "The value of R in (7) is roughly the largest that keeps |EIV | below a solar mass for vs ≃ 1."
  - Minor correction: v2 also uses the Planck-scale values. The finding lists only v1, v3 and v4.
- **The stale QI section.** v5 p. 8, re-printed today: "the left hand side is about −6.6 × 1093 kg/m3 at its smallest, while the right hand side is approximately −9.2 × 1094 kg/m3. We conclude that the QI is amply satisﬁed."
  - A word-level diff of v4 against v5 shows the QI section changed only in notation and citation numbers.
  - 72.5 × 1.4e-34 m = 1.0e-32 m, so the printed r_c,min belongs to the v1-v4 Delta~.
- **Why the parameters changed.** The arXiv comment on v5 reads "error in calculation corrected" (re-printed today). v4's E_II,- = -3.4e-3 kg became -1.4e30 kg in v5, because v1-v4 omitted the B^3 volume factor. The author then rescaled eq. (7) but did not redo the QI section.
- **The numbers.** Three sibling scripts reproduce the finding's numbers. Two of them derive eqs. (11) and (19) symbolically with sympy and match the paper exactly.
  - Femtometre parameters: peak at w = 0.5758, rho = -2.369e59 kg/m^3, r_c = 2.305e-17 m = Delta~/43.39, bound -1.184e26 kg/m^3, violated by 2.001e33.
  - Planck-scale parameters: w = 0.349, -6.626e93 kg/m^3, r_c = Delta~/72.46 = 1.38e-34 m, bound -9.21e94 kg/m^3, ratio 0.072.
  - The scripts are `checks/2026-10-27-prior-art/calc/vdb_versions_check.py`, `vdb_qi_recompute.py` and `vdb_local_qi_krasnikov.py`.
- **The pass condition.** It holds as stated for Van Den Broeck's own test: Delta~ < 3.74e-32 m, r_c < 31.8-31.9 L_P.

**Not directly checked:**
- **That v5 is the printed CQG text.** The IOP PDF returned a bot-check page again today, and the UFRJ copy failed TLS and then returned 503. The inference is strong:
  - the journal reference and DOI sit on v5 (last revised 21 Sep 1999);
  - Crossref's title (re-queried today) is "A `warp drive' with more reasonable total energy requirements", the v5 title (v1-v4 lack "more"); the article went online on 1999-11-10;
  - Bobrick and Martire (CQG 2021) read the published example as "R~ = Delta = 10^-15 m";
  - Finazzi et al. (2009) quote the v5 energies.
- **That no corrigendum exists.** Crossref has no `update-to` and an empty `relation`, and INSPIRE and web searches found none, but the IOP article page itself is unreadable.

**Qualification: the finding is too lenient on the Planck-scale case.** Its pass condition (r_c < ~32 L_P), and C3-0's "Planck variant formally passes by 14", hold only for Van Den Broeck's test: peak density with one global tau0 = 0.1 r_c,min. Two sibling scripts (`vdb_local_qi_scan.py`, `vdb_local_qi_krasnikov.py`) apply the bound pointwise with a local sampling time. The profile then fails at both parameter sets, worst near w = 0.97-0.98, by about 1e65, and essentially all of E_II,- sits in that region.
- That local prescription is the siblings' choice, not the paper's. It follows the Ford-Roman curved-space rule ("small compared to the minimum local characteristic radius of curvature").
- If it is accepted, "amply satisfied" was already wrong in v1-v4. The femtometre mismatch is then a second, independent error. This does not contradict the finding; it means the finding understates the problem.

## Point by point
| Our point | Status | Closest prior work (citation, link, date, status) | Verified quote |
|---|---|---|---|
| 1. v1-v4 use Planck-scale eq. (7); v5 switches to femtometre values to keep E_IV below a solar mass | Already published (informal) | L. Monti, LoreMonti/Warp_Drive README, https://github.com/LoreMonti/Warp_Drive. This passage was committed in ef73e40, 2026-09-29 19:39 UTC: after our run was framed (18:25) and before our verdict commit (21:02). Informal GitHub README, not peer reviewed. | "versions 1 to 4 of the paper (May and June 1999) use $\alpha = 10^{34}$ and $\tilde R = \tilde\Delta = 10^{-32}$ m throughout, with energies of a few milligrams; version 5, "error in calculation corrected", moves eq. (7) to the femtometre configuration and recomputes the energies" |
| 2. v5's QI section is stale; Delta~/72.5 = 1.4e-34 m needs Delta~ = 1e-32 m | Already published (informal) | Same README; the README table was first committed in c756800, 16:10 UTC. FusionVault/physica report.md errata row R6 (2026-10-25, later than ours, unreviewed) says the same. | "The giveaway is $\tilde\Delta/72.5 = 1.4 \times 10^{-34}$ m, which needs $\tilde\Delta \approx 10^{-32}$ m." and "keeps the curvature radius, "about ten Planck lengths", and the quantum-inequality numbers of the earlier one." |
| 3. At the published parameters: peak -2.37e59 kg/m^3, r_c = Delta~/43.4, QI violated by 2e33; v1-v4 parameters reproduce the printed values | Already published (informal) | Same README table. The result was first stated in commit 6987bbe, 2026-09-29 16:01 UTC (author-set timestamp). | README table: "peak density \| $-2.37 \times 10^{59}$ kg/m³ \| $-6.63 \times 10^{93}$ kg/m³ ... quantum inequality \| violated by a factor $2 \times 10^{33}$ \| holds, margin 0.072" |
| 4. The QI passes only for r_c < ~32 L_P (Delta~ < 3.7e-32 m) | Already published (informal) | Same README | "the inequality holds only below $\tilde\Delta = 3.7 \times 10^{-32}$ m, and $r_c$ reaches the Planck length at $1.2 \times 10^{-33}$ m, so the check passes in a window of a decade and a half, with curvature radii of a few to a few tens of Planck lengths" |
| 5. "QI amply satisfied" is false for the published parameters | Already published (informal); partly anticipated in peer-reviewed work | README as above ("the parameters printed in eq. (7) violate the inequality by 33 orders of magnitude"). S. Krasnikov, "The quantum inequalities do not forbid spacetime shortcuts", arXiv:gr-qc/0207057 v1 (15 Jul 2002), https://arxiv.org/abs/gr-qc/0207057; PRD 67, 104013 (2003), peer reviewed. A bare assertion, probably about a different region of the profile. | v3 fn. 8: "We take r different from that proposed in the original paper [23], because the latter, first, leads to a much (by ~ 10^36) greater amount of exotic matter and, second, violates the quantum inequality (e. g. in w = 0.98)." |

## Closest prior work
- **L. Monti, LoreMonti/Warp_Drive (public GitHub repository; README section on checking the 1999 paper).** https://github.com/LoreMonti/Warp_Drive. Informal, no DOI, not peer reviewed.
  - **What it says.** It makes our whole point with our numbers:
    - two parameter sets, v1-v4 against v5;
    - the stale curvature radius and QI numbers;
    - violation by 2e33 at eq. (7)'s values, and "holds, margin 0.072" at the Planck values;
    - the pass condition Delta~ < 3.7e-32 m.
  - **How it frames it.** It calls this "an inconsistency at the level of an erratum, not a refutation", because the energies barely depend on Delta~ at fixed pocket radius. It cites Krasnikov's footnote and says the size and origin of that violation are "not documented".
  - **Quotes.** All the quotes in the table above were re-printed today with fetch_text from raw.githubusercontent.com.
  - **Dating.** Sibling agents dated it from a bare clone of the repository history (62 commits, starting 2026-08-20):
    - 6987bbe, "Check the quantum inequality of the 1999 paper": 2026-09-29 16:01 UTC;
    - c756800 (the table): 16:10 UTC;
    - ef73e40 (the version-history explanation): 19:39 UTC.
    - An earlier roadmap commit (2026-09-21) lists redoing the QI check as an open item.
  - **What cannot be confirmed.** The GitHub API was blocked, the repository is not in GitHub code search and the Wayback Machine has no snapshot. So the first-public date and independence from our run cannot be confirmed. Our run directory never mentions the repository.
- **FusionVault/physica, `research/topics/frontier-gaps-and-metric-engineering/report.md`, errata row R6, and issue #14.** First committed 2026-10-25, author Dan Garden. Unreviewed.
  - Verified wording: "With the printed α = 10¹⁷ and Δ̃ = 10⁻¹⁵ m the QI is violated by 2×10³³ | The paper's QI numbers follow exactly from α = 10³⁴ and Δ̃ = 10⁻³² m; the energies are unaffected. The CQG version was not checked".
  - It is later than both our finding and Monti's, and cites neither, so it may derive from either. The issue page itself could not be opened (403), so its wording is unverified.
- **S. Krasnikov, arXiv:gr-qc/0207057.** v1, 15 Jul 2002, footnote 4; v3 and PRD 67, 104013 (2003), footnote 8. Peer reviewed.
  - **v1 wording (verified, PDF symbols garbled):** "violates the quantum inequality (e.g. on the interval w 2 [0: 97; 0: 98])", i.e. w in [0.97, 0.98].
  - **v3 wording** adds the "~10^36" exotic-matter factor. That factor fits v5's corrected 1.4e30 kg, so Krasnikov was reading the corrected energies.
  - **What it lacks.** No calculation and no parameters. It says nothing about the eq. (7) change or the printed 1.4e-34 m.
  - **Why it is probably a different violation.** The siblings' local-sampling scan puts the worst violation at w ≈ 0.974 at both parameter sets. That region depends only on alpha·Delta~ = 100 m, so it is unaffected by the parameter mismatch. This is an inference, since Krasnikov's criterion is not shown.
  - **Relation.** It partly anticipates point 5 only, and it is the earliest statement found that Van Den Broeck's profile violates the QI.
- **C. Van Den Broeck, "On the (im)possibility of warp bubbles", arXiv:gr-qc/9906050 v4 (18 May 2000).** Preprint.
  - The author restates the claim after v5: "Using this scheme, the required total energy can be reduced to stellar magnitude, in such a way that the QI is satisfied. On the other hand, the energy densities are still unreasonably large, and the spacetime has structure with sizes only a few orders of magnitude above the Planck scale."
  - "Planck scale" fits the v1-v4 parameters. There is no recheck or correction.
- **A. Bobrick and G. Martire, "Introducing Physical Warp Drives", CQG 38, 105009 (2021), arXiv:2102.06824.** Peer reviewed.
  - It reads the published example as femtometre-scale: "B(0) = B(R~) ~ 1017 ... where R~ = Delta = 10^-15 m".
  - It repeats that Van Den Broeck reached a solar mass "while satisfying the vacuum energy inequalities", without recomputing.
  - It supports "v5 = CQG", and shows the QI claim being passed on unchecked.
- **Uncritical citers.** These repeat the claim without checking it:
  - Lobo-Visser (CQG 2004), Lobo-Crawford (2003), Lobo's review (0710.4474) and Alcubierre-Lobo "Warp Drive Basics" (2017) give one sentence ("considerably ameliorates/improves the conditions").
  - Finazzi-Liberati-Barcelo (PRD 2009) quote v5's energies at face value.
  - Barzegar et al. 2026 exclude quantum inequalities by design.
  - Sajeendran et al. (PRD 2025) still quote "a few milligrams".
  - Wikipedia pairs v5's energy with a v1-v4 neck size of 10^-32 m.
  - All quotes are verified in the notes files; none makes the point.
- **Background.** Pfenning-Ford 1997 and Ford-Roman 1996 state the curved-space rule (sample "on timescales smaller than the minimum local radius of curvature") that both the paper's check and ours use. Both predate the paper.

## Coverage
**Searched:**
- **The paper.** All five arXiv versions of gr-qc/9905084, read and word-diffed, plus the abstract page and version history.
- **Indexes for an erratum.** Crossref (the record, and corrigendum searches on the CQG ISSN for 1999-2003), INSPIRE (record 500415 and related records) and web searches.
- **Citers.**
  - INSPIRE's 96 citers: titles and abstracts scanned; about 28 read in full.
  - Semantic Scholar: 101 citers, 38 with citation contexts.
  - A full-text grep for "Broeck" across 163 arXiv papers that cite Van Den Broeck 1999, Krasnikov 2003 or Pfenning-Ford 1997 found 83 with a real passage; the flagged passages were read.
- **Reviews.** Lobo, Alcubierre-Lobo, Kontou-Sanders 2020, Ford 2010, Fewster 2012, and Le 2026.
- **Other sources.**
  - DataCite (including Zenodo) and GitHub code search.
  - Web searches for errata, forum and blog discussion.
  - Wikipedia, Cramer's 1999 Analog column and 1999 mailing lists.
  - Krasnikov v1 and v3.

**Not reached:**
- **The published CQG text.** The IOP bot check was hit again today, and the UFRJ copy failed TLS and returned 503.
- **Van Den Broeck's AIP Conf. Proc. 504, 1105 (2000)**, doi:10.1063/1.1290913: no free copy.
- **Books.** Everett-Roman, "Time Travel and Warp Drives" (2012), doi:10.7208/chicago/9780226225005.001.0001, and Krasnikov's 2018 Springer book, doi:10.1007/978-3-319-72754-7: no free copy, and Google Books and archive.org were blocked.
- **Other papers.**
  - Davis 2004 (DTIC 403) and Davis 2009 (paywalled).
  - Gauthier-Gravel-Melanson, Grav. Cosmol. 9, 301 (2003), and Gravel-Plante (CQG 21, 2004): no text found. These are the best unread candidates.
- **Rate limits and blocks.**
  - OpenAlex was rate-limited (429) and Semantic Scholar only partly answered.
  - The GitHub API was blocked, so neither repository has an independent first-public date, and the physica issue page was not read.
- **Partial or no coverage.**
  - About 68 INSPIRE citers were checked only by name or abstract.
  - Google Scholar-only theses and reports, non-English sources, Reddit and Usenet were not covered.

Not finding a source in these places does not mean it does not exist.

## What this means
**Priority.** We cannot claim priority. A third party, Lorenzo Monti, publicly documented the same inconsistency with the same numbers, including the version-history explanation and the Delta~ < 3.7e-32 m pass condition. By his git timestamps that was a few hours before our run began, and apparently independently. Krasnikov had already asserted in 2002 that the profile violates the QI.

**What remains.**
- Nothing in the peer-reviewed literature, and no erratum from the author or IOP, records that the printed QI section belongs to the superseded Planck-scale parameters. A good part of the citing literature repeats "QI satisfied".
- The point is real and checkable, but it is erratum-sized: the energies are unaffected.
- The one new element is the sibling observation that a pointwise, local-sampling-time application of the bound fails at both parameter sets by about 1e65. If that holds up, it would make "amply satisfied" wrong even for v1-v4, and would give Krasnikov's bare footnote a calculation. It would need a defensible curved-space QI prescription before anyone relied on it.

**Recommendation.** It is not worth a standalone paper. If it is sent to the author or written up as a short comment, it should credit Monti's repository and Krasnikov's footnote. It should present the stale-parameter point as already noted, and lead with the local-QI result only after that analysis has been checked independently.
