# Check: quantitative
status: final

| Claim | Verdict | Note |
|---|---|---|
| RQ-01 PERKEO III lambda, A0 | verified | fetch_text on arXiv 1812.04666 gives the exact values and wording. PRL reference not checked. |
| RQ-02 Vud = 0.97351(60) from 879.7 s | verified | Eq. 6 matches, including the 4908.6(1.9) constant and the superallowed 0.97417(21). |
| RQ-03 PDG 2024 lambda avg | verified | -1.2754(13), scale factor 2.7, chi2 35.1, CL<0.0001 and the listed inputs all match the PDG listing. The per-experiment chi2 values are unattributed, as the note says. |
| RQ-04 PDG A avg | verified | -0.11958(21), scale factor 1.2, CL 0.261. The "driven by a-coefficient inputs" reading is the researcher's inference. The A-only chi2 of 2.7 does support consistency. |
| RQ-05 PDG Vud 0.97367(32) | verified | Quote found in the CKM review. The pion beta decay 0.9739(27) was not checked. |
| RQ-06 PDG unitarity sums | verified | All four sums and the 2.3 sigma first-row tension match. |
| RQ-07 PDG Vus | verified | 0.22431(85), 0.2250(4) and fK/fpi 1.1932(21) confirmed. The 0.2233(5) and f+(0) = 0.9698 were not individually grepped. |
| RQ-09 Vub | unverifiable | The inclusive 4.13e-3 and exclusive 3.67e-3 values appear in the PDG quote. The "scaled by sqrt(chi2)=1.4" detail and the Gorchtein-Seng quote were not checked. Low stakes. |
| RQ-10 Hardy-Towner 2020 | unverifiable | Not re-fetched. The figure 0.97373(31) is consistent with other sources, but the 23 decays, 222 measurements and bF figures were not checked. |
| RQ-11 Gorchtein-Seng | verified | -0.00166(69), 2.4 sigma and -0.00037(174) match arXiv 2311.00044 eq. 42. The note on 0.97361 vs 0.97373 is correct. |
| RQ-12 CMS 4908.6(1.9) s, f = 1.6887(1) | verified | Exact match in arXiv 1802.01804. |
| RQ-13 Seng 2018 | verified | Delta_R^V = 0.02467(22) and Vud = 0.97366(15) match the abstract. |
| RQ-14 Cirigliano 2023 Vud values | verified | 0.97402 (best) and the UCNtau 877.75(36) s input match eq. 8. The 0.97402(42) total matches the conclusions. The 0.7 sigma figures are correct arithmetic. The researcher's flag that the bare formula gives 0.97459 is correct and still unresolved. Do not use the 5.7e-4 offset as a physics result. |
| RQ-15 pion-induced corrections | verified | Abstract wording matches arXiv 2202.10439. PRL 129, 121801 was not checked. |
| RQ-16 Ma et al. lattice box | verified | The abstract matches: 3.65(8)(1)e-3, Vud = 0.97386 and 2.1 to 1.8 sigma. |
| RQ-17 ETM gA = 1.250(24) | verified | The abstract matches. The "20x worse than experiment" remark is the researcher's arithmetic: 2% against 0.04% is about 50x, or about 20x only if the PDG lambda error of 0.1% is used. Minor. |
| RQ-18 Nab | verified | The abstract of arXiv 2508.16045 confirms the Dalitz plot and the excited-neutron constraint. The Delta a/a = 1e-3 goal is from proceedings and was not re-grepped. PRC 113, 035501 not checked. |
| RQ-19 derived arithmetic | misattributed | The tau predictions, sensitivities and inverted Vud values match the calc log and my hand checks. One error: the beam Vud of 0.96911 is 0.00456 below the superallowed 0.97367, not 0.0055, which is the shift for 10 s from the bottle value. That gives about 14 sigma (0.00456/0.00032), not 17. Use 0.0046 and about 14 sigma. The constant K = 4908.6 s is the CMS 2018 baseline. |
| RQ-20 aSPECT 2024 | verified | a = -0.10402(82), lambda = -1.2668(27) and b = -0.0098(193) match. The 3.5 sigma figure is correct arithmetic. The PDG 2024 listing does carry the 2020 value, as stated. |
| RQ-21 planned experiments | unverifiable | Only quotes from the ESS and PERC abstracts were offered. PERC timeline is from search summaries. The da/dlambda estimate is labelled as the researcher's own. |

Most serious problem: RQ-19 overstates the gap between a beam-lifetime Vud and superallowed Vud (0.0055 and about 17 sigma, where 0.0046 and about 14 sigma is correct). The rest of the file holds up. The unresolved offset between the bare-formula and Cirigliano 2023 Vud values is honestly flagged.
