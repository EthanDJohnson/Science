# Check: frontier
status: final

Checked against arXiv abstract pages via fetch_text.py (quoted numbers and wording). Journal refs and peer-review status labels (ApJL, JCAP, PRD, A&A) were not independently confirmed from journal pages; arXiv pages for RF-06 and RF-10 carry no journal field. RF-02 was checked only through its abstract, not the full text.

| Claim | Verdict | Note |
|---|---|---|
| RF-01 TDCOSMO 2026: H0 = 71.1 +2.4 -2.3 (3.3%), 3.0% with SLACS+SL2S | verified | Abstract quote matches exactly. Preprint status is consistent with the arXiv page. |
| RF-01 sigma offsets: "about 1.7 sigma below H0DN, about 1.5 sigma above Planck+SPT+ACT" | contradicted | Recomputed. H0DN: (73.50-71.1)/sqrt(2.4^2+0.81^2) = 0.95 sigma. Planck+SPT+ACT: (71.1-67.24)/sqrt(2.3^2+0.35^2) = 1.66 sigma. The file's 1.7 and 1.5 are wrong and look swapped or miscomputed. Lensing is about 1 sigma from H0DN and about 1.7 sigma from the CMB. |
| RF-02 H0DN 73.50 +- 0.81; 7.1 sigma vs Planck+SPT+ACT; 5.0 sigma vs BBN+BAO | verified | arXiv abstract matches. The 67.24 +- 0.35 and 68.51 +- 0.58 values are from the full text, not re-opened. The sub-results (V08 72.51, V09 73.53, 71.61) were not checked. |
| RF-03 Roy Choudhury: 73.264 +- 0.806, 6.85 sigma; 73.139 +- 0.791, 6.82 sigma; 114 of 1701 rows; 52 of 277 | verified | Quote matches. The DES-DOVEKIE 73.267 +- 0.828 figure was not checked. |
| RF-04 Turner and Huterer: up to 2.5 shift; 1.1 +- 0.38 and 0.5 +- 0.1 | verified | Abstract matches. The "well under 1 sigma" gloss is the file's own and is clumsy but harmless. |
| RF-05 Efstathiou: tension insensitive to late-time expansion; DESI hint does not alter this | verified | Wording matches the abstract. |
| RF-06 SH0ES Perfect Host: 73.49 +- 0.93; 73.18 +- 0.88; 19 hosts/24 SNe, 37/42, 35 TRGB, 55 SNe | verified | Abstract matches exactly. The arXiv comment reads "ApJ, submitted", so the "ApJL 992 L34, peer-reviewed" label is unconfirmed here. |
| RF-07 Zaborowski: 69.2 +1.3 -1.4, 70.3 +1.4 -1.2, 69.6 +1.3 -1.8 | verified | Abstract matches. The sigma offsets from H0DN and Planck are the file's own arithmetic. |
| RF-08 Lynch et al.: 71.1 +- 0.7 with Planck; 69.3 +- 0.5 with ACT+SPT-3G | verified | Abstract matches. The 0.21 variance bound was not checked. |
| RF-09 Strunk eROSITA: f_EDE = 0.10 +0.04 -0.03, 3.2 sigma, H0 = 71.4 +- 1.4 | misattributed | The numbers match. The status is out of date: the arXiv comment says "Accepted for publication by A&A", so "not refereed / preprint" is wrong. Treat it as accepted, not yet a published journal paper. |
| RF-10 Poulin et al.: f_EDE = 0.09 +- 0.03, H0 = 71.0 +- 1.1; 3.7 sigma before; Delta chi2 = -35.4 | verified | Abstract matches. The PRD 113 063519 reference was not confirmed. |
| RF-11 Khalife et al. SPT-3G D1 AEDE | verified | The quote matches the abstract. The claim is weak: it carries no number. |
| RF-12 Wang et al.: quintessence-like 1 sigma, Delta chi2 <~ -14 | verified | Abstract matches exactly. |
| RF-13 GWTC-5.0: 71.7 +9.4 -7.5; 22.0% smaller uncertainty | verified | Both match. The abstract says "reduction by 22.0%" versus GWTC-4.0. |
| RF-14 Xiong et al.: 83.78 +12.53 -10.23 (13.58%); 75.42 +3.74 -4.66 (5.57%) | verified | Abstract matches. The difference is 8.4 km/s/Mpc, consistent with "~8". |
| RF-15 Anand: Delta mu = 0.17 +- 0.04 +- 0.06 mag, HST TRGB further | verified | Abstract matches exactly. |
| RF-16 Li et al. JAGB 2.0: -0.03 +- 0.02 +- 0.05; 0.11 +- 0.02; 73.3 +- 1.4 +- 2.0 | verified | Abstract matches. The arXiv comment says "submitted to ApJ", so ApJ 988, 97 was not independently confirmed. |
| RF-17 Gaia DR4 on 2 Dec 2026 (archive down 25 Nov, reopens 2 Dec) | verified | ESA news page text matches. |
| RF-18 TDCOSMO companion: 3.7 sigma no-SN; 2.7 sigma without LDL | verified | Abstract matches. The arXiv comment says "Submitted to PRL". |
| RF-19 Percival: -1.4, -0.2, -1.0 km/s/Mpc; 1.3 to 2.3 sigma | verified | Abstract matches. |
| RF-20 Dong et al.: 74.30 to 71.37; 60.83 to 63.25; 6.8 to 3.9 sigma; 7.3 to 4.3 sigma | verified | Abstract matches. The paper says the results move "closer to the input CMB constraint". |
| RF-21 Stiskalek: 5.2 scatter; 68.4 +- 5.9; 72.3 +- 2.6; "cannot yet arbitrate" | verified | Abstract matches. |
| RF-22 Camilleri Unite: 3.3 and 3.1 sigma, weak Bayesian evidence | verified | Quote matches. The Omega_m values were not checked. |
| RF-23 DES Y6: S8 = 0.806, Omega_m = 0.302, h = 0.683, sum m_nu < 0.14; 2.3 sigma | verified | Abstract matches. The 3x2pt-alone numbers (S8 = 0.789, 1.8/2.6 sigma) were not checked. |
| RF-24 Chen et al.: 73.30 +- 0.92, 5.6 sigma above Planck | verified | Abstract matches. The review is "accepted" in RAA. |
| RF-25 absence claims (no CCHP 2026 update, no DESI DR3) | unverifiable | Absence-of-evidence claims resting on search summaries. The "70.39 +-1.22 ..." CCHP figures also come from a search summary and were not checked. |

Most serious problem: RF-01's sigma comparisons are wrong (about 1 sigma from H0DN, about 1.7 sigma from the CMB, not 1.7 and 1.5).
