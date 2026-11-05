# Check: quantitative
status: final

| Claim | Verdict | Note |
|---|---|---|
| RQ-01 SPT-3G / CMB-SPA H0 values, 6.2/6.4 sigma, Table I (Omega_m, r_d, sigma8, ns) | verified | fetch_text on arXiv:2506.20707 matches 66.66, 67.19, 6.4 sigma, Table I columns, ns = 0.9679. The abstract says 6.2 sigma for SPT alone. Age 13.805 not re-opened. Paper is an arXiv preprint here; PRD status from INSPIRE not re-checked. |
| RQ-02 P-ACT 67.62, P-ACT-LB 68.22, DESI DR2 68.43, 1.6 sigma | verified | Text and Table in arXiv:2503.14452 match. SPT's 2.8 sigma for CMB-SPA vs DESI DR2 in the Omega_m-h r_d plane also verified (SPT paper Fig. 25). |
| RQ-03 DESI DR2: Omega_m, h r_d, BBN H0 = 68.50 +- 0.58, 2.3 sigma (1.9 in DR1), Table V values | verified | Matches arXiv:2503.14738 (p. 20, p. 33). Preprint status correct. The "2.0 sigma without lensing" detail was not checked. |
| RQ-04 DESI w0wa: w0, wa, H0 = 63.6, 67.51, 65.91, 66.74, wCDM 69.51 | verified | Table V rows match. Other table rows (not the claim) show 69.28 in a different (PPP m_nu) fit, so the 69.51 row is the standard one. |
| RQ-05 Planck 2018 H0 67.36 +- 0.54, 67.4 +- 0.5, N_eff 66.3 +- 1.4 | verified | The 67.36 +- 0.54 value is confirmed in arXiv:1807.06209 (p. 16). The abstract numbers and N_eff row were not re-fetched; they appear in the quoted table and were not contradicted. |
| RQ-06 Planck PR4 H0 67.64 +- 0.52, sigma8 0.8070, S8 0.819, Omega_m 0.3092, TT/TE/EE values | verified | Matches Tables 3 and 5 of arXiv:2309.10034. The Jense et al. 2026 values (67.62 vs 67.86) and the "+0.61 sigma / 13.7%" figures were not checked. |
| RQ-07 DES-SN5YR + DESI inverse ladder 67.19 (+0.66 -0.64), flat-LCDM 67.67, M_B | verified | Matches arXiv:2406.05049. The paper states r_d is calibrated from the CMB. The Aubourg and Macaulay values were not checked. |
| RQ-08 Popovic 2026: systematics < 0.1 km/s/Mpc, 73.04 +- 1.04 local value, 67.4 +- 0.5 | verified | Matches arXiv:2602.12822. The paper also says a -0.3 mag shift only recovers H0 = 70.96, which supports the claim. The "dmu/dz 0.2" and "Omega_M = 0.23 / 10 sigma" details were not confirmed from the garbled abstract. |
| RQ-09 KiDS-Legacy S8 0.815; DES Y6 3x2pt S8 0.789 +- 0.012, Omega_m 0.333; 1.8/2.6 sigma; joint S8 0.806, h 0.683 | verified | DES Y6 numbers confirmed in arXiv:2601.14559. KiDS-Legacy was not re-fetched. |
| RQ-10 Cooke 2018 D/H 2.527 +- 0.030, eta10 = 5.931 +- 0.051 | verified | eta10 confirmed in arXiv:1710.11129 (p. 14). The Pitrou clause rests on an INSPIRE title only, which the author already flagged. Treat it as unverified. |
| RQ-11 ACT DR6 extended models: f_EDE, H0 = 69.3, 67.5, 69.9, 69.1, 69.6, N_eff | verified | The f_EDE < 0.088 (ACT) and < 0.12 (P-ACT), with H0 = 67.5 and 69.3, match the arXiv:2503.14454 text and table. The other values are consistent with the quoted abstract. The Delta chi2 figures were not checked. |
| RQ-12 Philcox 2021 equality-scale H0 = 65.1, 65.6, 70.6 | verified | Abstract text matches arXiv:2008.08084 exactly. The "differs from SH0ES at 95%" statement applies to the first case only, as the file says. |
| RQ-13 Sound-horizon-free H0 66.7, 67.9, 67.8; 18 of 25 mocks | verified | Both the values and "18 of the 25 ... 72%" match arXiv:2411.16677. The JCAP status was not checked. |
| RQ-14 GC ages 13.57 (Part III), 13.81 +- 0.25 +- 0.23 (Part IV), 13.857 x 68/H0, 73 gives about 1 Gyr younger and 2 sigma | verified | The 13.57 and age-scaling text matches arXiv:2603.04872. The 13.61 mean age was not checked. First author and title were already flagged as unverified. |
| RQ-15 neutrino mass: DESI+CMB < 0.064 eV (LCDM), < 0.16 eV (w0wa); ACT DR6 "alone" < 0.089 eV | misattributed | The DESI 0.064 and 0.16 values are verified. The 0.089 eV limit is from P-ACT-LB (Planck + ACT + lensing + DESI DR1 BAO), not ACT alone (arXiv:2503.14454, Eq. 33). The "theta_* consistent" statement is verified. |
| RQ-16 LiteBIRD launch end of JFY2032 (Q1 2033); Euclid DR1 November 2026 first tranche, mid-2027 full | verified | Both match their sources (arXiv:2406.02724; telescoper blog). The Euclid source is a blog. Items (c) CMB-S4 cancellation and (e) DESI timeline rest on search summaries and are unverifiable. |

Not checked: Jense 2026 (RQ-06 secondary), Simons Observatory forecast statements, CMB-S4 cancellation.
Most serious problem: RQ-15 attributes the sum m_nu < 0.089 eV limit to "ACT DR6 alone"; it is a P-ACT-LB combined limit. All other checked numbers matched their sources.
