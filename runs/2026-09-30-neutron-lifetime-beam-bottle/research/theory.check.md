# Check: theory
status: final

Checked with fetch_text.py on arxiv.org/pdf (full-text). 14 claims checked.

| Claim | Verdict | Note |
|---|---|---|
| RT-01 master formula, RC=0.03886(38), 4908.6(1.9) s | verified | Exact quote found in CMS 2018 (PRL 120, 202002). The 5172.0(1.1) constant was not re-grepped here, but it appears in RT-07's source. |
| RT-02 BR<0.27%, 2.4 of 8.6 s, gA=1.268 gives BR=0.99; beam 888.0(2.0), trap 879.4(6) | verified | Text matches. gA=1.2755(11) is the post-2002 value. The "also applies to mirror/dark neutrons" sentence was not re-grepped. |
| RT-03 Gorchtein-Seng: 5024.7 s, Delta_R^V=0.02479(21), Delta_R=0.03985(21), Vud 0.97433(28)(82)(10) and 0.97404(20)(35)(10), PDG tau 878.4(5) | verified | Eqs. 8, 45 and 46 match. The paper compares with superallowed 0.97367(31). Universe 9, 422 journal status not re-checked. |
| RT-04 bottle compatible with superallowed and unitarity, beam not | unverifiable | The quote was not re-grepped. Fig. 1 context is consistent with the claim. Low risk. |
| RT-05 and RT-06 Fornal-Grinstein windows and branching | verified | Sampled the "3.5e-10" and "~1%" passages, which match. The mass windows were not re-grepped. |
| RT-07 Berezhiani: 879.5(1.3) s, gA=1.2681(17), >3.5 sigma | verified | Quote matches (EPJC 79, 484). Inputs are 2018-era, as the file notes. |
| RT-08/09 n-n' formulas and worked example | unverifiable | Not checked beyond the B_res and gA passages. Low priority. |
| RT-10 Cirigliano 2022: 2.7 sigma vs CalLat, ~1 sigma vs FLAG21, "does not impact Vud" | verified | The 2.7 sigma and 1 sigma passage matches. The "does not impact" quote was already in the file and is consistent with the passage. |
| RT-11 RDK II branching 0.00335(5)(15) and 0.00582(23)(62) | verified | Matches abstract and text of Bales 2016. The "factor ~250 and ~3 below" arithmetic is correct: 1.1%/0.335% is about 3.3, and 1.1%/4e-6 is about 2750. The "~250" is unclear (perhaps 1.1%/4e-5?), so treat that figure as sloppy. It does not change the conclusion. |
| RT-12 Dubbers 2019: BR_X<0.28% (from <0.92%), 1.0(0.2)% needed | verified | Quote matches (PLB 791, 6). The text also says the bound drops to 0.14% if the pre-2000 lambda values are discarded. This is not mentioned in the claim, but it is relevant. |
| RT-13 Tan constants 5024.46(30), dR'=0.014902, Delta_R^V=0.02454(18), Vud0+=0.97373(31) | verified | Matches Tan 2023 Eqs. 8-9. The superallowed Vud is 0.97373 in Tan but 0.97367(31) in Gorchtein-Seng, so the two reviews give slightly different values. |
| RT-14 Gialidi 2026 preprint exists (arXiv:2608.14794, Delta(1232) ChPT) | verified | Title, authors and abstract start found. It is a preprint, as labelled. Seng 2024 not re-checked. |
| RT-16 McKeen: heavier than 1.2 GeV or repulsive self-interactions | verified | Abstract matches. |
| RT-17 Broussard 2022: excluded above 10 neV; p<2.5e-8; UCN limits theta0 >~1e-3 below ~60 neV | verified | Matches PRL 128, 212503. The 6.6 T peak field was not checked. The abstract says the Berezhiani model is for NIST's 4.6 T field. |
| RT-18 Tan reversed partition | unverifiable | Not opened. Labelled speculative in the file. |
| RT-19 Veselsky 2025 | unverifiable | Not opened. The file labels it a preprint. |
| RT-20 J-PARC: 877.2 +-1.7 +4.0/-3.6, 2.3 sigma, chi2/DOF 15.8/3, runs 868.2 to 884.8 | verified | All of this matches the arXiv text and Table II. The paper says "10.8 s shorter" than the beam average, which fits 888.0. Journal status was not found (search found only the preprint and talks), so the file's "preprint (not verified)" label is appropriate. |
| RT-15 NS bound, Baym/McKeen | verified (McKeen part) | McKeen's 0.7 Msun and 1.2 GeV statements match. Fornal 2023 and Baym were not opened. |
| RT-21 scale calculations | unverifiable | Own calculation, not reproduced. The arithmetic is plausible: 60.3 neV/T x 4.6 T is 277 neV, and 1-878/888 is 0.01126. |

## Most serious issue
Nothing contradicted. One minor flaw is the unexplained "factor ~250" in RT-11. The 2018 inputs in RT-02, RT-07 and RT-12 (gA, tau) are dated, which the file says itself. The "bound" arguments depend on lambda and on the bottle value being the true tau_n.
