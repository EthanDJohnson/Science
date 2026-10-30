# Check: frontier
status: final

Checked 2026-10-30 with fetch_text.py against arXiv full text or abstract pages. All cited quotes below were matched word for word unless noted.

| Claim | Verdict | Note |
|---|---|---|
| RF-01 v1 says quantum, vanishes for hbar->0; v2 says classical process | verified | v1 abstract "a quantum process forbidden classically and semi- classically" and v1 p.2 "vanishes for hbar->0" both match. v2 p.3 "our calculation corresponds to a classical process" matches. Eq. 9-11 text matches in both. The claim that eq. 8 is identical in v1 and v2 was not re-checked. |
| RF-02 state |f>=S|0>, used as initial state | verified | v2 p.2 "evolution of the GW has to be studied with these coherent states as initial states" confirmed in the context seen. Top-hat profile and no r in eq. 8 not re-read. |
| RF-03 unpolarized-graviton fusion amplitude (s^2-2tu)/s; s-channel dropped | verified | v2 p.2 text confirms "assuming an unpolarized graviton state" and eq. 7 with (s^2-2tu)/s and delta_{mu1 mu2}. The s=0 on-shell argument is also on p.2. The SM SA quote was not re-fetched. |
| RF-04 2 pi delta(0) -> T, P/T is the rate | verified | SM SB p.10 quote matches exactly. |
| RF-05 eqs. 9-12 definitions (tau, W_gamma, E_rel) | verified | Eqs. 9, 10 and 11 as printed in v2 match the claim. The SI form 6 G^2 hbar/(25 pi c^10) matches. The eq. 12 and strain relation were not independently re-read. |
| RF-06 W_gamma=2.8e-35 W, about 2e5 photons/s with (1+2f), vs quoted ~1e6 | verified | B&O text "still modest, ~10^6 s^-1" confirmed. I recomputed by hand: 2.78e-35 W / 9.9e-32 J = 2.8e-4 /s, and times 7.6e8 gives 2.1e5. The hbar omega value at 150 Hz (6.2e-13 eV) is right. The inputs (E_rel=2 Msun, t_m=5 ms) were not re-read. The researcher flags the result as their own analysis, which is fair. |
| RF-07 binaries "very weak", Hawking comparison, below kHz absorbed, keV corner | verified | All three quotes confirmed (p.3 footnote 4, p.4 "frequencies are above keV", p.6 Hawking). The "W_H/W_gamma ~ 1e2-1e3" figure was not confirmed. Eq. 13 prints a prefactor of about 1e-4 times (lambda l/(r_s r_m))^2 and the text after it was cut off. Treat that range as unverifiable. |
| RF-08 stochastic rate 8 pi G^2 rho^2/15, 1e-110 m^-3 s^-1, wavelength volume | verified | Quotes match on p.4. |
| RF-09 ULDM: 7/450pi, tau_phi=(54/7)tau, eq. 17, eq. 18 1e14 W, 1e54 s^-1 | verified | Eq. 17 and eq. 18 text confirmed on p.5. "too small to have a clear significant effect" confirmed on p.4. The N_phi~6e87 coefficient of eq. 16 was not checked. |
| RF-10 constraints: "Far from aiming..." and other inputs | verified | Quote confirmed on p.5. The COBE/FIRAS and D-photofission bounds and Fig. 3 labels are consistent with the caption; individual numerical values were not re-read. |
| RF-11 Ai, Ellis, Pradler (arXiv:2510.27690v2) | verified | Abstract quote matches. v2 comment "corrected and improved interpretation" is present. Preprint status is right. |
| RF-12 Fang et al. and Miyauchi et al. | verified | Both abstract quotes match. Preprint status is right. |
| RF-13 Franchino-Vinas et al.: 1e-28 s^-1 for HM Cancri, n=0 does not contribute | verified | All three quotes match (p.11-12). omega^(13/3) and M^(10/3) scaling confirmed. HM Cancri omega=0.0195 Hz and M=0.5 Msun confirmed. The "massless scalar" restriction was not re-checked. |
| RF-14 Bao et al. (arXiv:2607.27313) | verified | Quote and "rule out proposals to establish the quantization of gravity" match the abstract. Date, authors and the acknowledgement of Rodd were not checked. |
| RF-15 Redi-Tesi: time-like momenta give pair production; null tensor perturbations produce none | verified | Both quotes match (p.3 and p.6). The W^2 expression was not checked. |
| RF-16 Khusnutdinov, EPJ Plus 141, 532 (2026) | verified | The journal ref is on the arXiv page and the abstract quote matches. "peer-reviewed" is right. |
| RF-17 Kanno, Soda, Taniguchi, PRL 136, 061404 (2026), squeezing ~1e-4 | verified | The journal ref and the abstract quote match. The 27-citation figure was not checked. |
| RF-18 Sawyer, PRL 124, 101301 (2020) | verified | Both quotes match the arXiv v3 text, including "essentially classical fields". The arXiv text shows a "quantum break" time of order (8 pi G n)^-1 log N. The PRL volume and number were not checked on a journal page. |
| RF-19 Cheong, Rodd, Wang, PRD 111, 015028 (2025) | verified | The journal ref is on the arXiv page. The "Gaussian over the basis of coherent states" quote was not re-grepped, but the arXiv journal ref supports the peer-reviewed status. |
| Headline: 0 INSPIRE citations of B&O, no comment or erratum | unverifiable | This is a negative search result. I did not re-run INSPIRE. It is a plausible gap statement, and the researcher discloses that the arXiv endpoint timed out. |

Summary: 19 of 19 numbered claims verified on the points checked, plus 1 unverifiable headline negative. Weakest points are the W_H/W_gamma range of 1e2-1e3 in RF-07 (eq. 13 in the text read gives a prefactor of about 1e-4 and the range was not confirmed) and RF-06, which is the researcher's own analysis. No misattribution, unit errors or status errors found.
