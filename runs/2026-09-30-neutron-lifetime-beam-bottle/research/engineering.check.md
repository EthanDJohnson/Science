# Check: engineering
status: final

Checked against arXiv full text (fetch_text), PSI book of abstracts, lit_search. Journal versions of J-PARC 2024 and Ezhov 2018 not opened.

| Claim | Verdict | Note |
|---|---|---|
| RE-01 J-PARC 2024 877.2 +/-1.7 +4.0/-3.6; 2020 898; fivefold; 2.3 sigma | verified | Abstract and p.2 quotes match. Preprint, no journal ref found by lit_search. "Supersedes 2020" and "lower gas pressure" are the facet's inference, not checked. Omitted: the four sub-conditions in Table II disagree (870.9, 868.3, 868.2, 884.8) with chi2/DOF = 15.8/3, "cause undetermined" (p.4). Also the paper says 10.8 s below the proton-counting average, distinct from the 9.5 s beam-bottle gap in RE-10. |
| RE-02 J-PARC systematic table; 5333 +/-7 barn | verified | Table III matches line for line. The text names gas-scattering neutron background as the largest contributor, so the facet's "largest items" ranking (12C, pile-up, 3He amount) is its own reading and partly at odds with the paper. |
| RE-03 UCNtau 877.94+/-0.37; 877.82 +/-0.22 +0.20/-0.17; per-year values | verified | Abstract quote exact. Table p.23 gives 877.95 (not 877.94) for "Current"; trivial. Per-year averages match. PRC 111, 045501 confirmed by the PSI abstract reference list. Gonzalez 877.75 and Pattie 877.7 not re-opened. |
| RE-04 Largest UCNtau systematic is event definition, then uncleaned/heated UCN | verified | Quote matches p.23. |
| RE-05 Yue 2013 887.7 +/-1.2 +/-1.9; re-analysis of the 2005 data | verified | Abstract matches. Text calls the update an application of the new monitor efficiency to the 2005 result; the 2005 value is 886.3 in Yue (886.6 in the arXiv preprint). |
| RE-06 Yue Table II; 14 deposits at 20/30/40 ug/cm2; 0.1% bound | verified | Table II and text match ("Fourteen 6Li deposits", 0.1% on delta-rho). The facet's "costing 0.9 s" matches the table row. |
| RE-07 Gravitrap 881.5 +/-0.7 +/-0.6; Serebrov's history table | verified (table) / unverifiable (rest) | Table values match exactly (Yue chi2 7.0, Serebrov 2017 chi2 2.4, av_beam 887.7+/-3.1). Not confirmed: the "20-40 s falls to ~2 s" extrapolation-error figure (grep found no match), the PRC reference, and the "2004 vs 2017 re-interpretation". Note the same table lists Serebrov 2004 at 878.5, so the group's own older value is 3 s lower than its 2017 value; the facet's caution to drop the 2005 clause stands. |
| RE-08 Ezhov 2018 878.3 +/-1.6 +/-1.0 | unverifiable | Springer blocked; only a search summary. The 2014 arXiv quote ("purely statistical", 878.3 +/-1.9) is exact. The facet's reading that the 2018 paper is the same data is explicitly flagged as its own. |
| RE-09 UCNtau blinding factor 0.99986-1.00171; seven runs; 659 runs; 1.0 s shift | verified | Quote matches p.9, including the 659-run subset and 1.0 s shift. Minor: 2020 minus 2022 is 879.39 - 876.93 = 2.46 s, not "about 2.3 s" (the combined 1-sigma is about 1.06 s, so the difference is about 2.3 sigma). Possible unit confusion. |
| RE-10 Bottle average 878.4 +/-0.5; 9.5 s (4.6 sigma) | verified | Quote found in J-PARC p.1 in the earlier grep context via the PDG statement; PDG edition itself not opened. Beam average 887.9 is derived by addition, and 887.7+/-3.1 is Serebrov's own average. |
| RE-11 BL3 goal 0.3 s; BL2 charge exchange focus; BL2 "1 s" goal | verified (BL3/BL2 focus) / unverifiable (BL2 1 s) | PSI abstracts match. The 1 s BL2 goal is search-summary only, as the facet says. |
| RE-12 No BL2/BL3 result; J-PARC paper calls charge exchange negligible | verified (first half of quote by facet's read) | Charge-exchange statement is from the J-PARC p.1 text as the facet quotes; the absence of a BL2 result is an absence claim, not checkable here. |
| RE-13 tauSPECT target <0.3 s, 2024 blinded run, 1 s statistical precision | verified | PSI abstract matches. "Physics data taking in 2025" is search-summary, not confirmed. |
| RE-14 PENeLOPE 550 L, built TUM 2020, moved to TRIUMF 2024 | verified | Abstract matches. The field, coil count and 2025 cryostat test details were not checked. |
| RE-15 UCNProBe design | verified (design) / unverifiable (1-2 s goal) | Abstract quote exact (YAP:Ce, deuterated polystyrene). 1-2 s goal is search-summary only. |
| RE-16 UCNtau+ 5-10x loading, systematics well below 0.2 s | verified | Quote matches p.5. |
| RE-17 Partition synthesis | verified (inputs) | Derived from checked numbers. The inference that proton-counting-vs-rest fits better than beam-vs-bottle is the facet's interpretation. It omits that J-PARC's own sub-conditions scatter (chi2/DOF 15.8/3) and that J-PARC is systematics-limited. |
| RE-18 Nico 2005 Table IV, 886.6 | verified | Table IV lines (trap nonlinearity -5.3/0.8, total -0.1/3.4, etc.) match. The 886.6 vs 886.3 difference is unexplained; the facet correctly flags it. |
| RE-19 Caylor 2025 conclusion; cryopump remark | verified | Quotes match. The paper itself estimates about 0.3% proton loss probability for H2 and notes large uncertainty because H2 is not in thermal equilibrium; the facet's "own rebuttal" framing is fair but it should state that caveat. The "4He two orders below H2" and PRC 112, 065501 not checked. |
| RE-20 Design differences | verified (inputs) | Follows from checked budgets. The 4.6 T figure is correctly marked "do not use". |
