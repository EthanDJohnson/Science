# Prior-art check: finding "fuchs-shell", angle "citations"

- Finding: Fuchs et al. 2024, "Constant velocity physical warp drive solution" (CQG 41, 095013; arXiv:2405.02709): limits of the positive-energy shell. Reached 2026-10-02 (run runs/2026-10-01-warp-drive-without-negative-energy/report.md).
- Our results (a)-(e): (a) rebuild passes NEC/WEC/SEC/DEC at 850 pts at beta=0.02; NEC fails at 100/850 at beta=0.04. (b) beta_crit=0.0239 ~ 0.0716 C (C=0.335); falls to 0.00242 at 1.5 m wall; zero-shift DEC fails from C~0.45. (c) interior superluminality only above beta~0.21 (>=3.4x NEC cap; net advance at D=1 km needs 21-80x). (d) cavity shift pure gauge; invariant = Sagnac co-minus-counter 6.86 ns at beta=0.02 (gravitomagnetic holonomy), P_ADM=0. (e) tangential-minus-radial stress/energy peaks 0.539, size-independent, 7.5-8.9 orders beyond graphene.
- Angle: citation trail (INSPIRE refersto:arxiv:2405.02709 plus named papers).
- Date of check: 2026-10-27
- Rules: a quote is "verified" only when fetch_text.py / find_fulltext.py / lit_search.py abstract printed those words.

## Searches run (log)

(appended below)


### S1. lit_search.py "refersto:arxiv:2405.02709" --source inspire --max 150 --sort mostrecent
INSPIRE returned 14 citing records (raw output saved in scratchpad citing.txt). List (arXiv id, author, year):
- 2610.17629 Idrissov (Minkowski-Schwarzschild thin shell stability, 2026)
- 2609.36211 Bolivar, Nelson et al. (Natario negative Eulerian energy minimum)
- 2608.15000 Bolivar, Nelson et al. (Boundary obstructions, lapse freedom, static spherical hollow cores)
- 2608.10800 Fell et al. (Radiative signatures, warp drives through atmosphere)
- 2606.22531 Le (Radiative steering of warp shells)
- 2605.25417 Le (Relativistic elastic shells: material support and cavity geometry)
- 2602.16495 Barzegar, Buchert, Vigneron (General formalism, classification, demystification)
- 2512.18008 Rodal (warp drive w/ predominantly positive invariant energy density, GRG 58)
- 2511.18251 Celmaster et al. (WEC violations for Lentz drives)
- 2510.11836 Santos-Pereira et al. (Alcubierre shift sign reversal, Burgers)
- 2505.09692 Chawla et al. (Scale without conformal invariance; likely unrelated, citing-match noise)
- 2512.19837 Rodal (Closer look at Natario zero-expansion, IJTP 63)
- 2405.19381 Lentz et al. (Motivating emissions from positive energy warp bubbles)
- heidok.00035613 Fell thesis (Celestial beacons; unrelated)
NOT in INSPIRE list although named in task: Le 2602.18023; Helmerich 2404.03095 (Warp Factory). Need to check separately.

### S2. lit_search.py "Constant velocity physical warp drive solution" --source all --max 10
INSPIRE: Fuchs record = inspirehep.net/literature/2782713, 14 citations (Crossref says 9). Also surfaced Buchert et al. "Novel Realizations of Warp Drive Spacetimes as Solutions of GR", Universe 12 132, arXiv:2605.03653 (NOT in the refersto list; must check). arXiv API returned HTTP 429.
### S3. lit_search.py "refersto:arxiv:2405.02709" --source s2 : SKIPPED (S2 cannot read INSPIRE syntax).
### S4. lit_search.py "a Le, An T. and t warp" --source inspire --since 2025
Le's warp preprints: 2606.22531, 2602.18023 (Observer-robust energy condition verification, 1 cite), 2605.25417. Not 2606... 2602.18023 missing from S1 (refersto Fuchs) list; so INSPIRE's reference match for Fuchs is incomplete OR Le does not cite Fuchs in 2602.18023 (to check by reading).
### S5. lit_search.py "t Warp Factory" --since 2024: Helmerich et al. 2404.03095 (CQG 41 095009, 13 cites); Warp Factory toolkit conference paper 2404.10855 (4 cites).
### S6. lit_search.py "refersto:arxiv:2404.03095" --source inspire: 13 citers = nearly the same set as S1 plus Lobo 2610.09143 (Intrinsic spatial-strain shortcuts) and Le 2602.18023; no later Helmerich-group paper beyond Fuchs/Fell/Lentz.

### S7. INSPIRE API cross-check: curl inspirehep.net/api/literature?q=refersto:recid:2782713 -> total 14, identical to S1 list. (INSPIRE complete as far as INSPIRE goes; Le 2602.18023, Buchert 2605.03653, Lobo 2610.09143 are NOT in INSPIRE's Fuchs citers; check by reading their text for "Fuchs".)

### W1. Barzegar, Buchert, Vigneron, arXiv:2602.16495v1 (preprint, 18 Feb 2026), full text fetched (fetch_text.py https://arxiv.org/pdf/2602.16495v1 --grep "Fuchs"). Status: preprint.
Treats Fuchs et al. [28] as part of the "R-Warp / physical warp drive" series (Bobrick-Martire, Helmerich, Fuchs) and critiques it on CONCEPTUAL grounds. Verified quotes (fetch_text PDF text):
- p.22 Error 18: "The construction proposed by Fuchset al. [28] is not a solution to Einstein's equations; indeed, as we showed in Appendix B, the authors do not solve the Tolman-Oppenheimer-Volkoff (TOV) equations resulting from the Einstein equation in the given context. Hence, the algorithm in Fuchset al.[28, Figure 3] for "metric creation" is flawed."
- p.30 App. B: "Fuchset al. [28, Section 3.1] propose a process to construct a stable shell matter. We show that their process fails already in the first step as it is not a solution to the Einstein equations"
- p.19 Error 8: "Fuchset al. [28] speculate that the violation of the energy conditions for the Alcubierre metric (or R-Warp models in general) is due to the vanishing of the ADM energy. However, this is not a consequence as there are direct counter examples"
- p.19: Fuchs et al. "suffers further from a vague formulation so that one cannot decide if the speculated metric is asymptotically flat or not (see also Error 9)".
- p.21 Error 13: "the whole conceptualization of a "constant velocity warp drive" by Fuchset al.[28] has no meaning as long as no distinction is made betweenui andui." (geodesic-equation u^i vs u_i confusion)
- p.21: Helmerich and "Fuchset al.[28] make the same mistake around which they build their central concept" (Galilean transformation to constant-velocity comoving frame drops time derivatives).
- p.27 Error 31: the "rule of thumb" that Eulerian momentum flux and pressures should be less than the energy density: "this is a well-known fact".
- p.27 Error 33: Fuchs metric Eq. (16) "is not spherically symmetric"; mixing orthonormal and coordinate bases (Eq. 10).
- p.28 Error 37: Fuchs "call a solution to the 3+1-form of the geodesic equation warp drive, without exactly saying in what way it differs from the motion of a particle ... it is not clear what a warp bubble, hence a warp drive, is supposed to be"
- p.29: they point to Santiago-Schuster-Visser Theorem IV.34 "showing that R-Warp models are fundamentally unphysical by violating the NEC".
Preliminary relation: checks-the-same-paper-differently (TOV/ADM/conceptual critique; none of (a)-(e) numbers). Still to grep for: 0.04, Sagnac, holonomy, frame dragging, stress/anisotropic, superluminal interior.
Barzegar greps (barzegar.txt full text): zero hits for sagnac, holonom, frame drag, gravitomagnet, 0.04, 0.02, graphene, tangential, compactness; "thick" 1 (Alcubierre tanh wall, unrelated). So Barzegar reports NONE of (a)-(d) numbers. "superluminal" hits concern general R-Warp theorems (Def III.8 |Vs|>1 relative to exterior; Thm IV.7 no globally hyperbolic superluminal R-Warp), not a beta threshold for the shell interior.
Barzegar App. B verified quote (p.30): "...Evaluating the above atr =R1 we find P(R 1) ρ = r 1−2 GM R2 −1<0, which not only violates the SEC (and possibly other energy conditions), but also contradicts their assumption of positive pressure in the first step" -- i.e. constant-density shell with positive isotropic pressure vanishing at R2 gives P(R1)<0 (TOV). Bears qualitatively on (e) (isotropic pressure cannot carry the shell; matter content), no magnitude, no 0.539, no graphene.
Barzegar also says (Error 20) Fuchs "do not perform a proper 3+1-numerics ... unclear IVF" and Remark IV.27 that Fuchs et al. "rushed to plot some figures without an in-depth analysis". Nowhere reports the energy-condition scan of Fuchs's own shell as failing at some beta.

### W2. Le, An T., arXiv:2602.18023 "Observer-robust energy condition verification for warp drive spacetimes" (preprint; v1 20 Feb 2026, v6 24 Sep 2026). Full text v6 fetched (fetch_text.py https://arxiv.org/pdf/2602.18023v6). Note: INSPIRE does NOT list it as citing Fuchs, but text cites Fuchs [7] (15 mentions).
Greps v6: sagnac 0, holonom 0, frame drag 0, gravitomagnet 0, graphene 0, tangential 0, compactness 1; "0.04" only as unrelated numbers; no beta scan for the Fuchs shell.
What it does for Fuchs (verified text, p.~20/33-34):
- Lit review: "Fuchset al.[7] introduce a constant-velocity shell-based positive-energy drive in the Bobrick-Martire family" and "Barzegar, Buchert and Vigneron [18] ... They also question the consistency of the Fuchs shell's assumed matter source with its metric. Our pointwise tests of Gab/8piddo not resolve that source-consistency question."
- Sec 3.6: "Table 9 applies the same pointwise energy-condition diagnostics to the regularized Fuchs shell [7] and the Garattini-Zatrimaylov de Sitter bubble [10], beside Alcubierre and Rodal." Standardized block uses "vs = 0.02 ... 10-90% profile width W = 4.419943 m, chosen from the Fuchs sigmoid."
- Table 9(a)/(b) Fuchs row: wall cells Type I 100.0%, Type IV 0.0%; min(rho+p_i) (Type I) = 0.021 (a) and 0.022 at vs=0.02 (b) (positive slack); i.e. it reproduces the PASS at vs=0.02 (Type I) with the author's own regularization. Fuchs row has "-" in the WEC/NEC "miss" columns.
- Appendix (verified): "The published parameters are R1 = 10 m, R2 = 20 m, M = 4.49x10^27 kg (2M = 6.668692 m), and vs = 0.02. We use four smoothing passes with fixed physical density smoothing width sigma_rho = 0.06(R2-R1) and pressure width sigma_P = sigma_rho/1.72." Also "We replace the published buffered clamps by the natural-endpoint extension Swarp(r) ... This C^inf extension is the manuscript's regularization of the published prescription." So Le, like us, had to choose smoothing spans (paper does not print them); consistent with our Rb=0 choice note.
- Table 10: Composite slice diagnostic, Fuchs vs=0.02, "Fuchs 0.02 7.5 15.4 100.0 0.0 0.022".
Relation: checks-the-same-paper-differently. It independently reproduces the paper's own claim (Type I, positive NEC slack at vs=0.02) with a different regularization; it does NOT scan beta upward (no beta_crit, no 0.04 failure, no compactness/wall-thickness dependence), no superluminality threshold, no holonomy, no stress ratio. It explicitly leaves the TOV/matter-source question unresolved.

### W3. Le, An T., arXiv:2605.25417 "Relativistic elastic shells: material support and cavity geometry" (preprint; v1 25 May 2026, v3 17 Sep 2026). Full text v3 fetched. Fuchs cited once, as [9], in the introduction.
Verified quotes (fetch_text):
- Intro: "The connection to subluminal warp shells is the geometry of a moving body with a vacuum interior [9]. Recent analyses emphasize the distinction between coordinate motion and material motion, and between a prescribed stress tensor and a matter model with its own equations of motion [10, 11]." ([10]=Barzegar et al., [11]=Buchert & Frackowiak 2605.03653)
- Abstract: "Nonnegative isotropic pressure cannot support a static spherical shell of positive-density matter with two free vacuum faces, whereas tangential elastic stress admits equilibria near relaxation."
- Intro: "A static spherical shell cannot meet these conditions with nonnegative isotropic pressure alone. We use a finite-thickness elastic annulus, whose tangential compression supplies the missing support."
- Intro: "Their nonconstant lapse and curved spatial slices lie outside the unit-lapse, spatially flat ansatz of many warp-metric restrictions [12, 13]; Olum's superluminal-travel criterion [14] has different hypotheses. Neither propulsion nor a travel-time advantage follows from the cavity."
- Appendix A, Theorem A.1 (Tangentially supported shell): p_r = 0, p_t = rho m / (2(r-2m)); "Where rho>0, DEC holds if and only if 5m<=2r. NEC and WEC hold everywhere." Example (a,b,M)=(10,20,1) in G=c=1 units. "This exact construction establishes that a vacuum interface need not violate DEC."
- App. A.1 (verified): "The obstruction in Proposition 2.1 cannot be removed by truncating a positive-pressure fluid solution. Integrating Eq. (2.5) inward from p(b) = 0 generally produces p(a)>0. ... a nonzero positive inner pressure produces a massless surface layer that violates surface DEC. Smoothing the jump instead produces a transition stress that must be included explicitly; it does not retain the original isotropic equilibrium." (This is the same TOV inner-pressure point as Barzegar App. B, in the Fuchs shell setting: constant-density shell, p(R2)=0.)
- Sec 4.1 / eq 4.12: Sagnac-type circular clock comparison, Delta tau = 4 pi r^2 e^{-Phi}(Omega_g - omega): "A guide corotating with the material has Omega_g = varpi and includes the kinematic Sagnac delay. A guide fixed relative to infinity ... measures the term proportional to -omega." This is a rotating-shell frame-dragging Sagnac, NOT the translating-shell shift holonomy. Frame dragging is for rotation (omega); abstract: "At leading weak-gravity order, static redshift and linear frame dragging probe the same inverse-radius mass moment."
- Sec 6.3 + Prop G.1 (asymptotic translation, boosted coasting shell): "This gives a coasting shell with V^i = P^i/P^0 ... The boost constructs uniform motion, not an acceleration process. Changing the shell's momentum requires exchange with another system or with outgoing radiation; the total ADM momentum of the complete isolated system remains conserved."
Not found: Fuchs beta (shift) scan; beta_crit; 0.04; superluminal interior threshold; graphene/material-strength comparison; the numbers 0.539. 
Relation: partly-anticipates (e) QUALITATIVELY (a vacuum-faced static shell needs tangential stress; p_t/rho set by compactness m/r only; DEC iff 5m<=2r), and (d)'s "no propulsion" in general; but not about the Fuchs shell's shift, no beta, no magnitude vs materials.

### W4. Le, An T., arXiv:2606.22531 "Radiative steering of warp shells" (preprint; v1 21 Jun 2026, v4 13 Sep 2026). Full text v4 fetched. Fuchs cited once [5], in passing.
Verified quote (intro): "Work on subluminal shells includes the classification proposed in [4], the constant-velocity shell of [5], and a member of Huey's noncompact planar membrane family satisfying the surface dominant energy condition (DEC) [6]. Energy conditions do not by themselves establish material viability or invariant motion [7, 8]." ([7]=Barzegar et al., [8]=Buchert-Frackowiak.)
Greps: sagnac 0, holonom 0, frame drag 0, gravitomagnet 0, superlumin 0, graphene 0, "0.02" 0; "0.04" only a figure axis. Abstract (lit_search): "Self-similar shells require anisotropic stress and have growing normal modes".
Relation: unrelated to (a)-(e) (cites Fuchs only as an example of a subluminal shell; its own topic is radiative steering). Part of the Le series.

### Searching next: Buchert-Frackowiak 2605.03653; Lobo 2610.09143; Idrissov 2610.17629; Bolivar 2608.15000/2609.36211; Rodal 2512.18008; Celmaster; Fell 2608.10800; Lentz 2405.19381; Santiago-Schuster-Visser follow-ups; Helmerich/Bobrick group later papers.

### S8. lit_search.py (inspire) author queries: "a Helmerich, Christopher", "a Bobrick, Alexey", "a Martire, Gianni" -> the Applied-Physics/Bobrick-Martire group has only: Bobrick-Martire 2102.06824 (2021), Warp Factory 2404.03095 and 2404.10855, Fuchs 2405.02709. NO later paper by the same group in INSPIRE as of 2026-10-27. ("a Visser and t warp and date > 2023" returned nothing: bad syntax.)

### S9. lit_search.py "refersto:arxiv:2105.03079" (Santiago-Schuster-Visser citers) --source inspire --since 2024 : 40 records. Besides the ones already in the Fuchs list, relevant-looking: Barzegar-Buchert 2407.00720 (Universe 11 293, "On Restrictions of Current Warp Drive Spacetimes"), Clough et al. 2406.02466 (warp drive collapse GWs), Abellan et al CQG 41 105011 (2024, nontrivial lapse bubble matter content), Bolivar et al Annals Phys 481 170147 (anisotropic fluids), Buchert-Frackowiak 2605.03653, Lobo 2610.09143, Garattini-Zatrimaylov 2408.04495/2502.13153, Chowdhury 2404.15948, Sanches 2608.08213. None of these appear in INSPIRE's Fuchs citers except those listed in S1, so they do not cite Fuchs per INSPIRE (to be confirmed by text for 2605.03653, 2407.00720).

### Text checks of other INSPIRE citers (full text fetched, grep "Fuchs"):
- Buchert & Frackowiak 2605.03653 (Universe 12 132): 0 mentions of "Fuchs" in full text -> does NOT cite Fuchs (consistent with INSPIRE).
- Idrissov 2610.17629 (preprint, 13 Oct 2026; 6 pp): thin-shell Minkowski-Schwarzschild; cites Fuchs [6] 4x. Verified quotes: "Fuchset al.[6] constructed numerically, with the tools of Ref. [7], a subluminal warp solution that satisfies all the energy conditions"; "Fuchset al.[6] check that the shift vector of their solution cannot be removed by a coordinate transformation; by this criterion the present shell is the degenerate member of the class."; "The null, weak and strong energy conditions hold for all a0 > 2M. The dominant energy condition, sigma0 >= p0, holds if and only if s>=1/5, that is a0 >= 25/12 M"; "No causal wall can stabilise a shell inside a_crit, i.e. for compactness 2M/a0 >~ 0.844."; stable shells need isotropic perfect-fluid wall with sound speed; "Pitre, Schneider and Poisson [21] ... finding a growing mode for all sampled parameters and all multipoles l>=2" (thin shell instability). No shift/beta scan, no Sagnac/holonomy, no stress ratio. Relation: checks-the-same-paper-differently / background (thin-shell zero-shift energy conditions vs compactness; not the thick Fuchs profile; its DEC bound C<=0.96 is for a thin shell, ours C~0.45 is for the thick smoothed Fuchs profile - different object, not a contradiction but NOT a reproduction).
- Bolivar & Abellan 2608.15000, Bolivar 2609.36211, Fell & Loeb 2608.10800, Lobo 2610.09143, Rodal 2512.18008, Celmaster-Rubin 2511.18251: "Fuchs" appears only in reference lists (1-3 hits) in the greps; no discussion of the Fuchs shell found in the text of these -> cite-in-passing, unrelated to (a)-(e).
- Helmerich et al. 2404.03095 (CQG 41 095009; Warp Factory; full text fetched, 54,815 chars): predates Fuchs; grep for 0.02, 0.04, beta, ADM, sagnac, frame drag, holonom, compactness = 0 hits. Only generic note: "Warp shells with a bubble consisting of regular matter, such as a matter shell, may require a change in lapse to the passenger volume [7]." Reports none of (a)-(e). Relation: unrelated (toolkit; the shell results are in Fuchs).
