# Prior-art check: van-den-broeck / angle: recompute

- Finding: "van-den-broeck" - Van Den Broeck 1999 (CQG 16, 3973; arXiv:gr-qc/9905084): the quantum-inequality check was not redone for the published (v5, femtometre) parameters; at those parameters the QI fails by ~2e33.
- Angle: recompute (independent script, not reusing the falsifier's or lens's scripts)
- Date: 2026-10-27
- Source of finding: runs/2026-09-29-alcubierre-negative-energy/verdicts/C3-0.md

## Log

### Step 1: source text (fetch_text.py)
- v5 PDF (arxiv.org/pdf/gr-qc/9905084v5) read in full (15,450 chars). Confirmed verbatim: eq. 7 "α = 10 17, ˜∆ = 10 −15 m, ˜R = 10 −15 m, R = 3 × 10−15 m. (7)"; eq. 11 rho = (1/8π)(B'^2/B^4 - 2B''/B^3 - 4B'/(rB^3)); eq. 12 B = α(−(n − 1)w^n + n w^(n−1)) + 1; eq. 13 w = (R~+D~-r)/D~; n = 80; peak "at w = 0.349 ... T00 = −4.9 × 10^2 /D~^2 (14)"; eq. 19 R_1212 = B'^2/B^4 - B''/B^3 - B'/(rB^3); "rc,min = 1/sqrt|R1212| = ˜∆/72.5 = 1.4 × 10−34 m, (20) which is about ten Planck lengths"; tau0 = beta rc,min, beta = 0.1; QI (22) T00 >= -3/(32 pi^2 tau0^4); "the left hand side is about −6.6 × 10^93 kg/m3 at its smallest, while the right hand side is approximately −9.2 × 10^94 kg/m3. We conclude that the QI is amply satisfied."
- v5 also: "The value of R in (7) is roughly the largest that keeps |EIV | below a solar mass for vs ≃ 1." and eq. 7 text "the inner diameter of the ‘pocket’ is 200 m. For the moment, these numbers will seem arbitrary".
- v1, v2, v3, v4 eq. 7 (all four): "α = 10 34, ˜∆ = 10 −32 m, ˜R = 10 −32 m R = 3 × 10−32 m. (7) The most outer surface of the warp bubble will have an area corres ponding to a radius of approximately 2000 LP". NOTE: v2 also has the Planck parameters (finding listed only v1, v3, v4; v2 was not cited but agrees).
- abs page: v1 21 May 1999 ... v5 21 Sep 1999; "Comments: 9 pages, 1 figure; error in calculation corrected"; "Journal reference: Class.Quant.Grav. 16 (1999) 3973-3979"; DOI 10.1088/0264-9381/16/12/314. The abs page does not itself say which version matches CQG; v5 is the latest and post-dates submission period (Sep 1999; CQG vol 16 issue 12 = Dec 1999).
- v1 and v4 QI section (fetch_text --grep "amply", "rc,min"): identical wording and numbers to v5 ("= ˜∆ 72.5 = 1 .4 × 10−34 m, (20) which is about ten Planck lengths"; "−6.6 × 1093 kg/m3 ... −9.2 × 1094 kg/m3. We conclude that the QI is amply satisﬁed."). So the QI section is unchanged from v1 to v5.
- What v5 changed ("error in calculation corrected"): v4 p. 6 eq. 16: "EII, − = ... = ˜∆ ∫ 0.981 0 dw(−w + 2)2 ∫ π 0 dθ sinθ ∫ 2π 0 dφ ˜T 00(w) = −2.5 × 102 ˜∆ = −3.4 × 10−3 kg. (16)" (no sqrt(g)=B^3 volume factor) and p. 7 "The amount of positive energy in the region w > 0.981 is negligible compared to EII, −." v4 p. 5: "EIV ≃ −5.6 × 10−8v3 s kg (9) for vs ≫ 1, and EIV ≃ −6.7 × 10−5vs kg (10) for vs ≪ 1." v5 inserts B^3 (gS = B^6), gets −1.4e30 kg and +4.9e30 kg, and enlarges R/R~/Delta~ to femtometres, E_IV ≃ −6.3e29 vs kg. Interpretation (mine): once E_II became ~solar masses, VdB enlarged the outer bubble to fm scale (allowing E_IV up to a solar mass) and rescaled alpha to keep alpha R~ = 100 m, but did not redo the QI section, which depends on alpha and Delta~.

### Step 2: independent calculation
- Script: checks/2026-10-27-prior-art/calc/vdb_qi_recompute.py (own sympy derivation of G_00 and orthonormal Riemann for ds^2 = -dt^2 + B(r)^2 (dr^2 + r^2 dOmega^2); mpmath 60-digit evaluation; cross-check of one point with toolkit gr_tensors curvature_at).
