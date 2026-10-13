# Check: engineering
status: final

| Claim | Verdict | Note |
|---|---|---|
| RE-01 PIXIE/Super-PIXIE sigma, FIRAS limits | verified | Quote matches arXiv:1909.01593 p.5 verbatim. 9e-5/3e-8=3e3 correct; for y headroom is ~1e4, so "at most ~3 orders" is slightly low. |
| RE-02 SPECTER / A17 | misattributed | A17 quote and "easily measure y" verified (arXiv:2409.12188 p.3). But the claim says mu is "roughly 100 times below FIRAS-class noise"; source says mu is ~100x smaller than y, and y is ~10x below FIRAS noise, so mu is ~1000x below. The "1-10 nK" figure is present. |
| RE-03 ARCADE-2 excess | verified | ">5 sigma" quote, 2.725+-0.001 K above 60 GHz, index -2.62 (LF+ARC fit) all in arXiv:0901.0555 pp.8-9. The 7-9 orders gap is correct arithmetic. Published ApJ 734, 5. |
| RE-04 Voyager 1 plasma | verified | 2.6 kHz, 0.08 cm^-3, 0.06-0.08 range, 19%/AU all in Gurnett 2013 text. f_pe=8980 sqrt(n) is standard. |
| RE-05 ionosphere / LuSEE-Night | verified | Both quotes, "4 monopole antennas", "CS-3 early 2025" confirmed in arXiv:2203.07864 pp.7, 29. Preprint status stated correctly. The "late 2026" launch is a search-summary item and was not checked. |
| RE-06 LVK IR1 plan | verified | Page text matches. The page now says O5 plans "are being refined", not "are in discussion", so the second quote is stale or from an earlier page version; the substance (no fixed date) holds. |
| RE-07 detectability at face value | verified | Re-ran the script. Outputs match: 1.052e-46, 1.046e-77, 3.345e-35, 3e34, CMB/flux ~2.3e43. Model-dependent (isotropic emission) but labelled as such. |
| RE-08 plasma cutoff | verified | B&O fn.4 quote confirmed (arXiv:2607.24930 p.3). Script output matches: 2.79e-4 cm^-3, 2.54 kHz at 0.08. |
| RE-09 stochastic channel vs distortion | verified | Script outputs match (2.825e-109, 9.76e-110, 4.4e-100, 4y=6.4e-9). The "1e91 to 1e100" range covers only the primordial case; it is about 1e91 to 1e111 across all cases. See RE-13. |
| RE-10 path depletion | verified | Script gives 3.28e-66 and 2.48e-57. The gap against 1e-2 is 55-64 orders, as stated. |
| RE-11 LIGO O3B calibration | verified | Quote verbatim (arXiv:2107.00129 p.2). Preprint status correct. The 11.29% is the maximum for one Hanford epoch, so "upper limit" is fair. The O1/O2 5%/3 deg is flagged by the author as unopened. |
| RE-12 LISA, COSI, IPTA dates | verified (LISA); unverifiable (COSI, IPTA) | LISA quote and the 25 Jan adoption are confirmed on the Physics World page. The page says the year is 2024 only implicitly. COSI Aug 2027 on Falcon 9 was found in a search summary only (no 2026 confirmation). IPTA DR3 pulsar count was not checked. |
| RE-13 overall verdict | misattributed | The range "1e91 to 1e116" does not match RE-09's own "1e91 to 1e100"; the script gives 1e91 to ~1e119 (PTA). The qualitative conclusion is supported. "33-43 orders" matches RE-07. This is a derived claim with no independent source. |
