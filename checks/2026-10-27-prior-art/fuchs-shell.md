# Prior art: limits of the Fuchs et al. 2024 positive-energy warp shell
status: final
Checked: 2026-10-27. Finding dated 2026-10-02.

## The finding
Source: `runs/2026-10-01-warp-drive-without-negative-energy/report.md` (Bottom line; C1, C2 and C7 sections; Key numbers). It comes from an independent rebuild of the shell in Fuchs, Helmerich, Bobrick, Sellers, Melcher and Martire, "Constant velocity physical warp drive solution", Class. Quantum Grav. 41, 095013 (2024), arXiv:2405.02709. The rebuild used the project toolkit (`warp_shell.py`, `numeric_stress_energy.py`). The paper does not print its smoothing spans (its footnote 11 says they were "found by trial and error"), so the rebuild chose its own, with Rb = 0. The paper's energy-condition claim is at beta_warp = 0.02. The speed 0.04 c appears only in the caption of its Table 1 (light-timing comparison).

- **(a)** An all-observer scan of the rebuild at shift beta = 0.02 passes NEC, WEC, SEC and DEC at all 850 sampled points, all Hawking-Ellis type I. At beta = 0.04 the NEC fails at 100 of 850 points.
- **(b)** The NEC fails above beta_crit = 0.0239. That is about 0.0716 C, where C = 0.335 (M_ADM = 2.38 Jupiter masses, R1 = 10 m, R2 = 20 m). At fixed C the cap falls to 0.00242 as the wall thins to 1.5 m. With zero shift, the DEC fails from C of about 0.45.
- **(c)** Interior forward light exceeds c only above beta of about 0.21. Even interior superluminality therefore needs at least 3.4 times the NEC cap (design scan over cavity 0.5-16 m and C = 0.01-0.85). A net arrival advance at D = 1 km needs 21-80 times the shift the NEC allows.
- **(d)** The cavity shift is pure gauge. The only invariant signature is a Sagnac-type co-minus-counter light-timing asymmetry, 6.86 ns at beta = 0.02: a gravitomagnetic holonomy that threads the wall. P_ADM = 0, so the "warp effect" is a wall circulation with no propulsion gain.
- **(e)** The required tangential-minus-radial stress-to-energy ratio peaks at 0.539, whatever the shell's size. That is 7.5-8.9 orders of magnitude beyond graphene.

## Verdict
**Partly anticipated.**

Every qualitative frame of the finding is already in print. Most of it is in the Fuchs paper itself:
- an upper limit on the shift exists;
- light is still delayed, not advanced;
- a forward-minus-backward light-timing difference (7.6 ns) is the invariant test, which the paper calls "linear frame dragging";
- the shell needs hoop stress.

Bobrick and Martire 2021 already said any warp drive needs propulsion. Le reproduced the beta = 0.02 pass independently, before our date.

None of the following appears in any source we searched:
- the quantitative cap and how it scales;
- the NEC failure at 0.04;
- the superluminality and advance margins;
- the cavity-gauge plus wall-holonomy reading with P_ADM = 0;
- the 0.539 stress ratio and the graphene gap.

## Is the finding itself right?
No direct check contradicts it. The parts that can be checked against the primary source hold up. The headline numbers rest on one rebuild, and nobody recomputed them independently.

**Confirmed against the paper's text (arXiv v1, the only version; the CQG typeset page was not read):**
- The energy-condition claim is at 0.02. Sec. 4.1, re-printed today, reads "...possible for betawarp = 0.02 without any energy condition violation", and footnote 13 adds "This is likely not an upper limit as optimizations could be considered."
  - Our beta_crit = 0.0239 is above 0.02, so it agrees with that footnote.
  - 0.04 c appears only in the Table 1 caption ("Comparison of time delay between different warp models and the matter shell for vwarp = 0.04 c", re-printed today).
  - The paper prints no failing beta and no smoothing spans.
- Before our date, two Le preprints independently found the shell passing at 0.02:
  - arXiv:2602.18023 v4-v6 (Fuchs panel first in v4, 12 Jun 2026): a regularised variant, 100% type I, NEC slack +0.021/+0.022.
  - arXiv:2605.25417 v1 (25 May 2026): 0 of 13 interior probes violate.
- The arithmetic holds (`calc/fuchs_topical_arith.py`):
  - C = 0.3350 with the rebuild mass (0.3334 with the paper's 4.49e27 kg);
  - beta_crit/C = 0.0713-0.0715, against the quoted 0.0716, a rounding difference;
  - M = 2.377 Jupiter masses;
  - the upper end of the graphene gap (8.91 orders) is reproduced.

**Conflicts and unreconciled items:**
- **The tail.** Le 2605.25417 v1/v2 reports type IV violations at 22 of 25 probes in the smoothing tail beyond R2. Our rebuild has an exact zero-shift Schwarzschild tail with no such failures.
  - Le attributes them to his iterative Gaussian smoothing ("residual matter halo") and to the transition geometry, not to the shift. The later Le versions (2605.25417 v3; 2602.18023 v6) no longer report them.
  - This is a difference in regularisation, not a refutation, but it is still unresolved.
- **The light-timing number.**
  - I re-ran `calc/fuchs_table1_check.py` today. The same convention reproduces the paper's Alcubierre row (8.02 ns against 8.0 ns at v = 0.04, R = 15 m).
  - The rebuild gives 6.80-6.87 ns at 0.02 and 13.60-13.74 ns at 0.04, whatever span is chosen.
  - The paper's Warp Shell row (7.6 ns, under the 0.04 c caption) is 1.11 times our 0.02 value and 0.55 times our 0.04 value.
  - So either the shell row was computed at about beta = 0.022 and the caption covers only the other rows, or the paper's shell profile differs from the rebuild by about 1.8 times. The paper does not say which.
  - The report already lists the Table 1 convention [D-33] as unresolved. What this shows is that our 6.86 ns is our rebuild's value of the paper's own observable, not a new observable.
- **Interpretation of (d).**
  - The authors say the shift "cannot be reduced to a coordinate transformation". That fits our reading at the global level: the wall holonomy is invariant.
  - It conflicts with our reading inside the cavity, and with their claim of a "similar effect on passenger transport to that in the Alcubierre drive".
  - The report itself concedes that "frame dragging" is a misnomer for the cavity and that the 0.07 C cap is specific to this profile.

**Could not check here (needs the rebuild):**
- the 850-point and 100-of-850 counts (the report marks point counts as unverified, M-CONSTRAINTS-14);
- beta_crit itself;
- the 0.00242 thin-wall cap;
- the zero-shift DEC failure at C of about 0.45;
- the 0.21 threshold and the 3.4 times and 21-80 times margins;
- the 0.539 ratio;
- the 7.55-order lower end of the graphene gap. It depends on strength and density inputs that the report flags as search-summary values.

## Point by point
| Our point | Status | Closest prior work (citation, link, date, status) | Verified quote |
|---|---|---|---|
| (a) all-observer pass at beta = 0.02 (850 points, type I); NEC fails at 100/850 at 0.04 | Partly anticipated. The 0.02 pass is the paper's own claim and was independently reproduced before our date. No source scans 0.04 or any other speed. | Fuchs et al. 2024, CQG 41 095013, https://arxiv.org/abs/2405.02709, 2024-05-04, peer-reviewed. Le, arXiv:2602.18023 v4-v6, https://arxiv.org/abs/2602.18023, 2026-06-12 (first Fuchs panel) to 2026-09-24, preprint. | Fuchs: "Varying the values of betawarp, we find that the addition of shift inside the shell is possible for betawarp = 0.02 without any energy condition violation". Le v5: "The Fuchs constant-velocity shell is Type I with a non-negative NEC margin throughout its sampled shell wall and interior". |
| (b) beta_crit = 0.0239, about 0.0716 C; 0.00242 at a 1.5 m wall; zero-shift DEC fails from C of about 0.45 | Partly anticipated. That a cap exists is stated qualitatively by the authors and left as future work. No value, compactness scaling or wall-thickness dependence was found. Zero-shift DEC compactness limits exist only for other matter models (background). | Fuchs et al. 2024 (as above), Sec. 2 and conclusions. Background: Bolivar, Abellan, Vasilev, arXiv:2608.15000, https://arxiv.org/abs/2608.15000, 2026-08-15, preprint. | Fuchs: "Increasing the shift vector will continue to add more momentum flux to the stress-energy tensor, so there is an upper limit to the magnitude of the shift vector that keeps the warp drive physical before the momentum flux exceeds energy density. This upper limit is a future direction of work." Also: "The added shift vector is kept below a threshold that causes energy condition violation from the added momentum flux that accompanies its addition." |
| (c) interior light exceeds c only above beta of about 0.21 (at least 3.4 times the cap); net advance at 1 km needs 21-80 times the cap | Partly anticipated, qualitatively only. The paper says the shell still delays light; the theorems say an advance needs NEC or WEC violation. No threshold or margin was found. | Fuchs et al. 2024 (as above), conclusions. Visser, Bassett, Liberati, gr-qc/9810026, https://arxiv.org/abs/gr-qc/9810026, 1998, peer-reviewed. Olum, PRL 81 3567, https://arxiv.org/abs/gr-qc/9805003, 1998, peer-reviewed. | Fuchs: "from B to A is still a delay compared to the propagation time in the corresponding flat region. This is in contrast to the Alcubierre metric, in which an advance is perceived." VBL: "Given the NEC, the Shapiro time delay in any weak gravitational field is always a delay relative to the Minkowski background, and never an advance." |
| (d) cavity shift pure gauge; only invariant is a Sagnac-type co-minus-counter asymmetry (6.86 ns at 0.02), a wall holonomy; P_ADM = 0; no propulsion gain | Partly anticipated. The light-timing invariant, its size (7.6 ns) and the frame-dragging and circulation wording are the paper's own. "Any warp drive requires propulsion" is Bobrick and Martire's. "Shift is a choice of coordinate system" appears as a one-line general remark. No source gives the cavity-gauge plus wall-holonomy reading or P_ADM = 0 for this shell. | Fuchs et al. 2024 (as above), Sec. 5.1. Bobrick and Martire, CQG 38 105009, https://arxiv.org/abs/2102.06824, 2021-02, peer-reviewed. Barzegar, Buchert, Vigneron, arXiv:2602.16495, https://arxiv.org/abs/2602.16495, 2026-02-18, preprint. | Fuchs: "Running this test we find that the Warp Shell (from Section 4) has dt ~ 7.6 ns and the Matter Shell (from Section 3) has dt = 0 ns." and "This experiment demonstrates a Lense-Thirring effect exists for warp drives with shift vectors, creating a linear frame dragging." Bobrick and Martire: "Therefore, any warp drive requires propulsion." Barzegar: "which lacks clear meaning, especially since the shift vector is a choice of coordinate system." |
| (e) tangential-minus-radial stress/energy peaks at 0.539, size-invariant, 7.5-8.9 orders beyond graphene | Partly anticipated, as a qualitative premise only. The paper says hoop stress is needed with pressures below the energy density. Le shows isotropic pressure cannot hold a vacuum-faced shell. No ratio, size invariance or materials comparison was found. | Fuchs et al. 2024 (as above), Sec. 3.2. Background: Le, arXiv:2605.25417 v3, https://arxiv.org/abs/2605.25417, 2026-09-17, preprint. Barzegar et al. App. B (as above). | Fuchs: "This manifests as a kind of hoop stress around the inner radius of the shell. It is also important that these pressures are all lower in magnitude than the value of the energy density at that point to ensure that the shell is physical." Le v3: "Nonnegative isotropic pressure cannot support a static spherical shell of positive-density matter with two free vacuum faces, whereas tangential elastic stress admits equilibria near relaxation." |

## Closest prior work
- **Fuchs et al. 2024, the source paper itself** (CQG 41 095013; arXiv:2405.02709 v1, 2024-05-04; peer-reviewed; partly anticipates). This is the strongest prior statement of every qualitative frame in the finding.
  - It checks the shell at beta_warp = 0.02 only. Footnote 13 says that value is "likely not an upper limit". It states that an upper limit exists ("This upper limit is a future direction of work") and that the mass was chosen "to allow the most amount of the shift vector ... while balancing physicality".
  - It reports the forward-minus-backward light-timing test as the invariant: 7.6 ns for the warp shell, 0 for the matter shell. It calls this "a Lense-Thirring effect ... a linear frame dragging" (footnote 15 cites Costa and Natario 2021). It notes "a circulation pattern forming in the momentum flow of the shell".
  - It says the Shapiro effect is still a delay and that the shell needs hoop stress. It also says this "can always be satisfied by making the shell large", and calls for a better "mass-to-velocity ratio".
  - What it lacks: any cap value, compactness or wall-thickness dependence, the 0.04 failure, superluminality or advance thresholds, any gauge, holonomy or P_ADM statement, and any materials comparison.
  - Our results partly answer its stated future work. They also qualify two of its claims:
    - Making the shell large (lowering C) lowers the shift cap in proportion.
    - The cavity shift gives no passenger-transport effect beyond the wall holonomy.
- **Le, "Observer-robust energy condition verification for warp drive spacetimes"** (arXiv:2602.18023; Fuchs panel from v4, 12 Jun 2026, through v6, 24 Sep 2026; preprint; checks the same paper differently).
  - It independently reproduces the pass at vs = 0.02 for a regularised variant: 100% type I, slack +0.021/+0.022. It says "The Fuchs shell's energy-condition compliance is designed at vs = 0.02".
  - It gives a general mechanism (momentum from the curl of the curl of the shift, and an irrotational shift being pure gauge) but only for flat unit-lapse slices. It does not apply this to the Fuchs shell.
  - No beta scan. Its v1 (Feb 2026) has no Fuchs test.
- **Le, "On the boundary cost of source-consistent warp shells"** (arXiv:2605.25417 v1, 2026-05-25, and v2, 2026-06-20; preprint; checks the same paper differently).
  - Quote: "An independent frame-independent verification of the Fuchs constant-velocity shell confirms interior energy-condition compliance (0 of 13 interior probes violate) but reveals Hawking-Ellis Type IV violations in the smoothing tail beyond the nominal shell."
  - This agrees with our interior result and conflicts with our clean tail, through a different regularisation.
  - Its compactness-thickness scan and its v2 type IV onset, which "grows linearly with the matter tilt", concern Le's own shells, not the Fuchs metric.
- **Barzegar, Buchert, Vigneron 2026** (arXiv:2602.16495; preprint; partly anticipates the gauge half of (d) in one line, and otherwise checks the same paper differently).
  - Error 18 and App. B: "The construction proposed by Fuchs et al. [28] is not a solution to Einstein's equations". The constant-density first step gives P(R1)/rho = sqrt(1 - 2GM/R2) - 1 < 0.
  - The coordinate-choice remark quoted above is a general one. It would also deny the invariant the paper reports.
  - Nothing on (a)-(c) or on a stress ratio.
- **Bobrick and Martire 2021** (CQG 38 105009; peer-reviewed; partly anticipates the "no propulsion gain" half of (d); otherwise background).
  - Quote: "Conceptually, we demonstrate that any warp drive, including the Alcubierre drive, is a shell of regular or exotic material moving inertially with a certain velocity. Therefore, any warp drive requires propulsion."
  - Its statement that the Alcubierre interior is Minkowski after x -> x - v_s t, and its "always subluminal" Class I, are background. They concern the Alcubierre interior and the causal character of the Killing field, not this shell.
- **Le, "Relativistic elastic shells"** (arXiv:2605.25417 v3, 2026-09-17; preprint; background for (e)).
  - A free-faced static shell needs tangential stress. Theorem A.1 gives p_r = 0, p_t = rho m/(2(r - 2m)), with the DEC holding if and only if 5m <= 2r.
  - That is a different matter profile from ours, with no Fuchs shift and no materials comparison. Its Sagnac content is for rotating shells.
- **Bolivar, Abellan, Vasilev** (arXiv:2608.15000, 2026-08-15; preprint; background for the zero-shift DEC clause of (b)).
  - Quote: "the DEC endpoint 2m/r <= 4/5 is the exact pointwise DEC boundary of the p_r = 0 sector". This is zero shift and a different matter model, so it cannot be compared with our C of about 0.45.
- **Theorems behind (c)** (all peer-reviewed; background):
  - Visser, Bassett, Liberati (gr-qc/9810026). The Fuchs paper cites the sibling AIP version, gr-qc/9908023.
  - Olum 1998: "I prove that superluminal travel requires weak-energy-condition violation".
  - Gao and Wald 2000 (gr-qc/0007021).
  - None gives a threshold for a shell.
- **Background for (d)'s holonomy language:**
  - Costa and Natario 2021 (arXiv:2109.14641; the paper's own ref. [7]): the Sagnac delay "Delta t_S = 2 oint A_i dx^i"; "Unlike translational motion, which is inherently relative, rotation is not".
  - Lobo and Harko 2026 (arXiv:2604.11456): "Delta t_Sagnac = -2 oint beta_i dx^i".
  - Ashtekar and Magnon 1975; Tartaglia 1998; Maraner and Zendri 2012.
  - Ralph and Chang 2020 relate an Alcubierre shift term to the Sagnac effect on a circular path.
  - None applies this to a shell wall.
- **Schuster, Santiago, Visser 2022** (arXiv:2205.15950; peer-reviewed; background for (b)'s mechanism).
  - A shift on a massive vacuum background breaks the NEC at first order in velocity: "there is consequently an entire hemisphere where rho + p < 0".
  - There is no threshold, because rho = 0 there.
- **Not prior art:**
  - Idrissov, arXiv:2610.17629, posted 2026-10-13, after our date: independent corroboration only.
  - Lentz et al. 2405.19381, which reads the shell as a light-speed design without checking it.
  - The authors' TMF2024 talk, which restates the paper.
  - The NextBigFuture blog.
  - Meyler, "The Meyler-Fuchs Hybrid Warp Drive" (PhilArchive): could not be opened (HTTP 403), so it is unverified and cannot be ruled out.

## Coverage
**Citation trail:**
- INSPIRE `refersto:arxiv:2405.02709`: 14 citing records, re-run today and unchanged. Semantic Scholar lists 11 citers; OpenAlex gives a count of 11 but refused the list.
- Citers of Warp Factory (2404.03095), Bobrick-Martire (25 records since 2024), Lentz, Fell-Heisenberg, and the Santiago-Schuster-Visser papers.
- Le 2602.18023 and Buchert-Frackowiak 2605.03653 were checked by reading, because INSPIRE does not list them as citers.

**Topical and author searches:**
- INSPIRE sweeps of every "warp" title since 2024 (28 records). Re-run today for titles since 2026-07: the only new item was Sanches et al. arXiv:2608.08213, which does not mention Fuchs.
- INSPIRE author queries for the whole Fuchs team (no later warp papers).
- Sagnac and holonomy queries.
- About 20 WebSearch queries, including exact-number searches for 0.0239, 6.86 ns and 0.539. Forums, blogs, press and the authors' talk.

**Full-text reads and greps** of more than 25 papers, including:
- every version of Le 2602.18023 except v4 (read only for its Fuchs panel);
- every version of Le 2605.25417, and v1-v4 of Le 2606.22531;
- Barzegar et al. in full.

Version histories were re-checked today; there are no versions after those listed.

**Could not reach:**
- The arXiv API, which was rate-limited or timed out throughout, again today. Topical arXiv coverage therefore rests on INSPIRE and WebSearch summaries.
- NASA ADS and Google Scholar (no access).
- The OpenAlex citer list.
- The CQG typeset version of the paper (only arXiv v1 text was read).
- The Warp Factory MATLAB source, which holds the actual spans and the beta behind Table 1.
- The EPJ Plus Casimir-plasma paper (presumably a passing citation).
- Meyler on PhilArchive (HTTP 403).
- Conference slides, video, and non-English literature.

A "not found" here means not found in these sources. It is not proof of absence.

## What this means
**What is new:**
- the threshold structure: beta_crit = 0.0239, about 0.07 C for this profile;
- the collapse of the cap to 0.00242 as the wall thins;
- the NEC failure at the 0.04 c that appears in the paper's own Table 1;
- the 3.4 times (interior) and 21-80 times (advance) margins below any superluminal effect;
- the reading of the invariant as a wall holonomy, with a gauge cavity and P_ADM = 0;
- the size-invariant 0.539 stress ratio and its materials gap.

**What is not new:**
- that a cap exists;
- that light is delayed rather than advanced;
- that a light-timing asymmetry of a few ns is the invariant trace of the shift;
- that the wall needs hoop stress;
- that a warp shell needs propulsion like any massive body.

The write-up must credit Fuchs et al. for these, along with Bobrick and Martire, Visser-Bassett-Liberati and Olum, and Le's independent reproduction at 0.02.

**Writing it up and contacting people:** the results are worth a short note, and worth sending to the Fuchs/Helmerich group, because they answer the paper's own "future direction of work". They are also worth sending to Le, whose certifier could certify beta_crit. Three things should come first:
1. Ask the authors which beta_warp and spans produced the 7.6 ns row, to reconcile it with our 6.86 ns (0.02) and 13.72 ns (0.04).
2. Settle Le's tail type IV against our clean tail, with an interval-certified scan.
3. Frame the cap as a property of the published profile as rebuilt. The authors' footnote 13 expects optimisation to raise it.
