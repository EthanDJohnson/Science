# Check: engineering
status: final

| Claim | Verdict | Note |
|---|---|---|
| RE-01 FIRAS limits, band | verified | Abstract quote matches (|y|<15e-6, |mu|<9e-5, 95% CL, 50 ppm). 2-21 cm^-1 and 0.4 cm^-1 phrases not re-grepped; unit conversions to GHz correct. |
| RE-02 B&O uses FIRAS only | verified | Both B&O quotes match p. 5 (mu<9e-5, y<1.5e-5, ref [60]). "Uses no low-frequency radio data" is an absence claim, only partly checked (Fig. 3 bounds also include D/H, UV/X-ray, gamma-ray, as RE-14 says). |
| RE-03 mu = 1.4 dE/E and derived energy limits | verified | Kogut eq. 4.1 quote matches (10^4<z<10^7). Arithmetic matches the calc log (2.684e-18, 2.505e-18 J/m^3). The "5-sigma" qualifier on PIXIE mu<1e-8 is not in the quoted text; the 4y relation is unsourced, as flagged. |
| RE-04 eq. 14 emissivity and injected fraction | verified | Log reproduces 6.166e-110 photons, 1.029e-110/-91/-87. Conditional on B&O eq. 14, which I did not test. Arithmetic only. |
| RE-05 PIXIE 400 channels 30 GHz-6 THz, mu<1e-8 | verified | "400 spectral channels ... 30 GHz to 6 THz" matches. mu<1e-8 and the 15 GHz resolution were not re-grepped. Forecast, not hardware. |
| RE-06 BISOU / PIXIE / PRISTINE status | verified | "have not been successful", Voyage 2050 theme, and |y|<1.5e-5 vs y~2e-6 all match the UCL copy. EPJ Web Conf. 293 (2024) 00012 citation was not checked in the PDF. Absence of a 2026 update is the researcher's own admitted gap, so the timeline claim is weakly supported. |
| RE-07 ARCADE 2 excess | verified | 1.06+/-0.11 K at 1 GHz, beta=-2.56+/-0.04 match. Channels 3, 8, 10, 30, 90 GHz match. The "2006 flight" and "still debated" are not checked. |
| RE-08 ionosphere cutoff, LuSEE-Night | verified | ~10 MHz F-layer plasma frequency quote matches. Abstract confirms "reach the lunar far side in 2027". The 0.1-50 MHz band comes from a different paper (arXiv:2407.07173), not opened. The Astron. J. 172, 123 reference was not verified. Mission date is a plan and could have slipped. |
| RE-09 Voyager densities, 150 Hz evanescence | verified | Gurnett author copy has 0.002 cm^-3, ~0.1 cm^-3 and 2.6 kHz. Calc log gives n_crit 2.79e2 m^-3, f_p 401 Hz and 2.54 kHz. The "0.08 cm^-3" sentence was not seen in my excerpt but is consistent with the 2.6 kHz figure. Solar-wind density is unsourced, as the file admits. |
| RE-10 B&O on propagation and detection | verified | All three quotes match pp. 4 and 6 ("still modest ~10^6 s^-1", "leftmost corner ... above keV", "new avenue"). The claim that they do not discuss a plasma cutoff is an absence claim I did not exhaustively check. |
| RE-11 flux of merger photons | verified | Log gives 4.942e-77 W/m^2, E_rms 1.364e-37 V/m, B_rms 4.551e-46 T, ratio 1.39e-75. Arithmetic is self-consistent. It rests on L~1e6 s^-1 read from the text and an assumed 5 ms duration. |
| RE-12 CMB occupation at 150 Hz | verified | Log gives x=2.641e-9, n=3.786e8, 1+2f=7.572e8, I=1.884e-35. |
| RE-13 DEMETER search coil 1 Hz-20 kHz | unverifiable | Seran 2005 abstract not fetched here (the file says no free full text). The wording is plausible but I could not confirm it. |
| RE-14 Cooke 2018 D/H and B&O delta_D<0.03 | verified | Cooke quote matches exactly (2.527+/-0.030, "one percent determination", six earlier plus one new). The B&O "delta_D<0.03" quote was not re-grepped. The "factor of a few from ELT" is acknowledged as unsourced judgement. |
| RE-15 COSI 0.2-5 MeV, launch 2027 | verified | Abstract quote matches. The launch date is as of the 2023 proceedings, so it may be stale, as the file says. The "preliminary" status label is a loose description of a proceedings paper. |
| RE-16 no GW-damping constraint, nearest test differs | verified | Mastrogiovanni abstract confirms the quoted sentence and that the focus is beyond-GR parameterisation. The negative result is the researcher's own, and a search can't fully prove an absence. |

Most serious issue: none of the checked numbers are wrong. The weakest points are RE-13 (unverifiable), the unsourced solar-wind density in RE-09, and RE-06's timeline statement, which rests on a 2024 paper only.
