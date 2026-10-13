# Research: engineering
status: final
Mandate: observational/experimental side: which instruments could see the claimed photons (radio at GW frequency, ionospheric/plasma cutoffs), CMB spectral-distortion missions, EBL/radio background, what each could constrain, planned experiments, timelines.
Access: lit_search INSPIRE ok, arXiv API mostly timed out (rate-limited), Crossref ok, Semantic Scholar rate-limited; fetch_text worked on arxiv.org PDFs, space.physics.uiowa.edu, observing.docs.ligo.org, physicsworld.com; WebFetch not used; WebSearch used for LVK/LISA/COSI/IPTA schedules (search-summary)

## Claims

- [RE-01] CLAIM: Forecast sensitivity of proposed CMB spectral-distortion spectrometers (1 sigma, with foregrounds marginalised): PIXIE sigma(y) ~ 3.4e-9 and sigma(mu) ~ 3e-8; Super-PIXIE sigma(y) ~ 1.6e-9 and sigma(mu) ~ 7.7e-9. These are forecasts for concepts, not built instruments. They would improve the COBE/FIRAS limits (|y| < 1.5e-5, |mu| < 9e-5 at 95% c.l.), which remain the only measurement, "by several orders of magnitude" (a factor ~ 3e3 in mu at 1 sigma vs FIRAS 95%, my arithmetic: 9e-5/3e-8). B&O's mu and y bounds therefore have at most ~3 orders of magnitude of headroom in any planned mission, whereas the GW-photon injected energy they would test is dozens of orders of magnitude lower (see RE-09).
  SOURCE: Chluba et al. 2021, New horizons in cosmology with spectral distortions of the CMB (ESA Voyage 2050 white paper), Exper. Astron. 51, 1515, arXiv:1909.01593, p. 5
  QUOTE: "In the presence of foregrounds, PIXIE could reach one standard deviation errors of σ(y)≃ 3.4× 10−9 and σ(µ)≃ 3× 10−8, while Super-PIXIE could reach σ(y)≃ 1.6× 10−9 and σ(µ)≃ 7.7× 10−9 (see Sect. 3.2, Fig. 10). Both concepts would improve the long-standing distortion limits of COBE/FIRAS|y| < 1.5× 10−5 and |µ| < 9× 10−5 (95% c.l.) [2, 3] by several orders of magnitude."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RE-02] CLAIM: Realistic mu-distortion detection is not guaranteed even for PIXIE-class hardware once foregrounds are marginalised. The SPECTER paper (2025) states the LCDM mu signal is roughly 100 times below FIRAS-class noise, needs ~1-10 nK sensitivity, and that an earlier forecast (Abitbol et al. 2017, "A17") "showed that an extended PIXIE mission would not be able to detect the mu-distortion when marginalizing over all foreground components"; SPECTER is a multichroic concept proposed to fix that. The y-distortion "could easily" be measured by one FTS satellite.
  SOURCE: Sabyr et al. 2025, SPECTER: an instrument concept for CMB spectral distortion measurements with enhanced sensitivity, JCAP 10 (2025) 088, arXiv:2409.12188, p. 3
  QUOTE: "Since the y-distortion signal is predicted to be only about an order of magnitude below the COBE/FIRAS noise levels [16, 24], a single satellite of this design could easily measure the y-distortion." and "Ref. [26] (hereafter A17) showed that an extended PIXIE mission would not be able to detect the µ-distortion when marginalizing over all foreground components, despite having instrumental noise that is formally lower than the targeted µ signal."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-03] CLAIM: The ARCADE-2 balloon radiometer (3, 8, 10, 30, 90 GHz) found an extragalactic radio excess: the 3 GHz channels lie more than 5 standard deviations above the FIRAS CMB temperature (2.725 +- 0.001 K at the frequencies above 60 GHz). Its frequency range (3-90 GHz) and the excess's power-law antenna-temperature fit (index -2.62) are ~7-9 orders of magnitude above the Hz-kHz photon frequencies B&O's GW-fusion process emits (omega ~ omega_s), so the radio-background measurements cannot constrain a 150 Hz photon population directly; they could constrain it only if the photons were up-converted, which B&O do not claim.
  SOURCE: Fixsen et al. 2011, ARCADE 2 measurement of the absolute sky brightness at 3-90 GHz, ApJ 734, 5, arXiv:0901.0555, p. 8-9
  QUOTE: "the data at 8 and 3 GHz show a clear excess. The excess is statistically significant, with both 3 GHz channels lying more than 5 standard deviations above the FIRAS value."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RE-04] CLAIM: The lowest-frequency radiation measured in situ in any astrophysical plasma is bounded below by the local plasma frequency. Voyager 1 beyond the heliopause (very local interstellar medium) detected electron plasma oscillations at ~2.6 kHz = n_e ~ 0.08 cm^-3 (densities 0.06-0.08 cm^-3, rising ~19% per AU); the relation is f_pe = 8980 sqrt(n_e) Hz. Free-space electromagnetic waves below f_pe (2-3 kHz here; 150 Hz is a factor ~17 below) are evanescent. So a 150 Hz GW-sourced photon cannot propagate in the local interstellar plasma, never mind the 20 kHz solar wind at 1 AU or the MHz ionosphere (see RE-05).
  SOURCE: Gurnett et al. 2013, In situ observations of interstellar plasma with Voyager 1, Science 341, 1489, https://space.physics.uiowa.edu/~dag/publications/2013_InSituObservationsOfInterstellarPlasmaWaveVoyager_Science.pdf
  QUOTE: "On 9 April 2013, the Voyager 1 plasma wave instrument began detecting locally generated electron plasma oscillations at a frequency of about 2.6 kilohertz. This oscillation frequency corresponds to an electron density of about 0.08 cm −3, very close to the value expected in the interstellar medium."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RE-05] CLAIM: Ground-based radio astronomy is blocked below a few MHz by the ionosphere, and the lowest-frequency radio telescopes planned or built (LuSEE-Night on the lunar far side, a DOE/NASA test-bed radio receiver of 4 monopole antennas) cover 1-50 MHz, i.e. their lowest band is ~4 orders of magnitude (1 MHz/150 Hz = 6.7e3) above a GW150914-like 150 Hz photon and ~300 times above 3 kHz; it has "percent level absolute calibration". Its launch date is unsettled in the sources found (CS-3 'early 2025' in the 2022 Snowmass paper; a 2026 web summary says late 2026). No instrument, existing or planned, receives free radiation at Hz-kHz frequencies from outside the solar system.
  SOURCE: Snowmass2021 Cosmic Frontier White Paper: 21cm radiation as a probe of physics across cosmic ages, arXiv:2203.07864, pp. 7, 29
  QUOTE: "the ionosphere is opaque at frequencies lower than a few MHz, and can cause distortions even at higher frequencies forcing observations to be done from space, where the far side of the moon currently holds most promise" and "The aim of the experiment is to characterise the radio sky at frequencies 1-50MHz with percent level absolute calibration and a 10−3 relative calibration between frequency bands."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RE-06] CLAIM: Ground-based GW detector schedule as of the LVK plan page (accessed 13 Oct 2026): the network is in an upgrade and commissioning period; a six-month Intermediate Run 1 (IR1) with both LIGO detectors is planned from early- to mid-November 2026, with Virgo and KAGRA joining as available; the long fifth run O5 has no fixed date ("Plans and timeline for the fifth observing run (O5) are in discussion"). Engineering consequence for B&O: the next ~2 years of LVK data are new detections of ordinary strain signals; no GW detector measures a photon channel, so none of them tests GW to gamma-gamma.
  SOURCE: LIGO-Virgo-KAGRA, Observing run plans, https://observing.docs.ligo.org/plan/
  QUOTE: "We are currently planning a six-month observing run, designated as IR1 (Intermediate Run 1), beginning early- to mid-November of 2026 . Both LIGO detectors will be observing in IR1." and "Plans and timeline for the fifth observing run (O5) are in discussion."
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: high

- [RE-07] CLAIM: Detectability of the GW150914 photons at face value of B&O's model (SI, my calculation; B&O inputs E_rel = 2 Msun c^2, 150 Hz, t_m = 5 ms, CMB-stimulated L_gamma = 2.1e5 photons/s). Photon energy hbar omega = 6.2e-13 eV = 9.9e-32 J, wavelength 2.0e3 km. If emitted isotropically and spread over 4 pi D^2 = 2.0e51 m^2 at D = 410 Mpc, photon number flux is 1.1e-46 photons m^-2 s^-1 and energy flux 1.0e-77 W/m^2. An isotropic antenna of effective area lambda^2/4pi = 3.2e11 m^2 (a 2000-km-wavelength antenna) would absorb 3.3e-35 photons per second; one photon per second would need a flux 3e34 times larger. The CMB's own Rayleigh-Jeans background at 150 Hz (B_nu = 1.9e-35 W m^-2 Hz^-1 sr^-1; 2.4e-34 W/m^2 for 4 pi sr and 1 Hz) is 2e43 times brighter than this flux. Conclusion: not detectable by any conceivable receiver, even before plasma absorption (RE-04, RE-05).
  SOURCE: this run's calculation [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py]; formulas from B&O eqs. 8-12 (RQ-08/RQ-09)
  QUOTE: "photon number flux = 1.052e-46 photons m^-2 s^-1 ; energy flux = 1.046e-77 W m^-2" / "expected photons absorbed by one isotropic antenna in 1 s = 3.345e-35" / "B&O energy flux / this = 4.417e-44"  (script log output)
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: medium
- [RE-08] CLAIM: Plasma cutoff for a 150 Hz photon (nu_p = 8980 sqrt(n_e) Hz, n_e in cm^-3): the photon propagates only where n_e < 2.8e-4 cm^-3. This is satisfied by the mean fully-ionised intergalactic medium today (n_e = 2.2e-7 cm^-3, nu_p = 4.2 Hz) but NOT by the warm ISM (0.03 cm^-3, 1.6 kHz), the Voyager-measured very local interstellar medium (0.08 cm^-3, 2.5 kHz), the solar wind at 1 AU (5 cm^-3, 20 kHz) or the ionospheric F layer (1e6 cm^-3, 9 MHz). So even in B&O's own picture, no photon of the merger band can leave the host galaxy's ISM or reach Earth's surface; B&O's footnote 4 itself concedes this for 'frequencies below kHz'. The Galactic and solar-system cutoffs, not instrument sensitivity, are the first barrier.
  SOURCE: this run's calculation [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py]; Blas & Oller arXiv:2607.24930, footnote 4, p. 3; Gurnett et al. 2013 (RE-04)
  QUOTE: "Note that if the frequencies are below kHz, they are immediately absorbed by the interstellar medium [38]." (B&O fn. 4, p. 3) / script: "f = 150 Hz -> n_e = 2.790e-04 cm^-3" and "VLISM (Voyager 1) n_e = 0.08 cm^-3 -> nu_p = 2.540e+03 Hz ; 150 Hz photon propagates: False"
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: high
- [RE-09] CLAIM: Stochastic-background channel (B&O eq. 14, pair rate 8 pi G^2 rho_GW^2/15 per volume) against CMB spectral-distortion sensitivity (SI, my calculation, photons emitted at the GW frequency, no redshift, integrated over t_H = 13.8 Gyr). For the largest BBN-allowed primordial background (h^2 Omega_GW = 1.7e-6): pair rate 2.8e-109 m^-3 s^-1; at 25 Hz (hbar omega = 1.0e-13 eV) the energy injected is 2.5e-104 eV/m^3 = 1e-109 of rho_CMB (2.6e5 eV/m^3), or 4e-100 even with a full CMB stimulation factor 1+2f = 4.5e9. For the LVK limit Omega_GW(25 Hz) <= 2.8e-9: pair rate 1.6e-115 m^-3 s^-1 and fraction 5e-116 (2e-106 stimulated). Distortion thresholds: FIRAS |y| < 1.5e-5 means energy fraction 4y = 6e-5; Super-PIXIE 1 sigma y = 1.6e-9 means 6.4e-9. The planned instruments are therefore 1e91 to 1e100 times too insensitive; the gap is not closable by any engineering improvement.
  SOURCE: this run's calculation [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py]; thresholds from RE-01 and RQ-06
  QUOTE: "primordial bound, h2 Omega=1.7e-6 (Delta N=0.3): pair rate = 2.825e-109 m^-3 s^-1 ; photon E = 1.034e-13 eV ; stim x1.00e+00 ; injected energy over t_H = 2.544e-104 eV/m^3 ; fraction of rho_CMB = 9.762e-110" and "Super-PIXIE 1 sigma y 1.6e-9: dE/E = 4y = 6.40e-09"  (script log output)
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: medium
- [RE-10] CLAIM: Depletion of the GW signal along its path, at face value of B&O's model (tau_h = tau N0, GW150914, E_rel = 2 Msun c^2, D = 410 Mpc, light-travel time 4.2e16 s): tau_h = 1.3e82 s (vacuum) or 1.7e73 s (CMB-stimulated), so the fractional energy lost on the way to Earth is 3.3e-66 (vacuum) or 2.5e-57 (stimulated). Present-day detector systematics are of order 1e-2 to 1e-1 in amplitude (RE-11), so a path depletion could not be tested by 55 to 64 orders of magnitude.
  SOURCE: this run's calculation [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py]
  QUOTE: "fractional energy lost over path: vac 3.280e-66 ; stimulated 2.483e-57"  (script log output)
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: medium

- [RE-11] CLAIM: Calibration of the LIGO strain channel (the best-controlled amplitude measurement of a GW): for the second half of O3 (O3B) the upper limit on systematic error plus uncertainty is 11.29% in magnitude and 9.18 deg in phase (68% confidence interval, 20-2000 Hz), with the systematic error alone < 2% in magnitude and <~ 4 deg in phase; for O1/O2 combined error and uncertainty was about 5% in magnitude and 3 deg in phase (O1/O2 figure from a search summary, not opened). I found no published LIGO O4 error budget (gap). So any GW-amplitude depletion test is limited to the ~1e-2 to 1e-1 level, against B&O's 1e-57 to 1e-66 (RE-10).
  SOURCE: LIGO Scientific Collaboration authors (first author not verified) 2021, Characterization of systematic error in Advanced LIGO calibration in the second half of O3, arXiv:2107.00129, p. 2
  QUOTE: "For O3B, the upper limit on the systematic error and associated uncertainty is 11.29% in magnitude and 9.18 deg in phase (68% confidence interval) in the most sensitive frequency band 20–2000 Hz. The systematic error alone is estimated at levels of < 2% in magnitude and ≲ 4 deg in phase."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RE-12] CLAIM: Planned space/ground facilities relevant to the GW side, with dates (as of Oct 2026). LISA (mHz band): ESA adopted it in Jan 2024; launch expected in 2035, operation for at least 4 years, estimated cost EUR 1.5 bn. COSI (NASA SMEX, 0.2-5 MeV gamma rays, the nearest instrument to B&O's photofission-energy cascade photons): launch targeted August 2027 on Falcon 9 (a plan, not confirmed; originally 2025). IPTA DR3 (nHz GW background, the band of B&O's ULDM channel): still in preparation, 121 or 130 pulsars (sources disagree), expected to give a definitive low-frequency background detection. None of these instruments has a Hz-kHz photon channel.
  SOURCE: Physics World (news), ESA gives construction go-ahead for LISA, https://physicsworld.com/a/european-space-agency-gives-construction-go-ahead-for-lisa-gravitational-wave-mission/ ; COSI and IPTA DR3 from web search summaries
  QUOTE: "LISA, which is estimated to cost €1.5bn, is expected to launch in 2035 and operate for at least four years." (LISA only; full text via fetch_text)
  ACCESS: full-text (LISA); search-summary (COSI, IPTA)
  STATUS: secondary
  CONFIDENCE: medium
- [RE-13] CLAIM: Overall engineering verdict (synthesis of RE-04 to RE-10, mine): the photons B&O predict from GW fusion at merger and inspiral frequencies (Hz-kHz, wavelengths 300-3e6 km) (i) are evanescent in the interstellar plasma, solar wind and ionosphere, so cannot reach any detector; (ii) are 33-43 orders of magnitude below a one-photon-per-second flux or the CMB's own 150 Hz brightness even if they could; (iii) have no instrument sensitive to them (lowest radio bands ~1 MHz on the lunar far side; lowest in situ plasma-wave channels ~kHz, Voyager); (iv) enter CMB-distortion or EBL constraints only through bulk energy injection, which is 1e91 to 1e116 below anything PIXIE, Super-PIXIE or FIRAS can see. Only the indirect 'constraint' route (bulk energy injection) could in principle reach an instrument, and it needs injected energy fractions ~1e-8 of rho_CMB, which B&O's own rates fall short of by dozens of orders. Existing or planned observations in the next ~20 years cannot detect or constrain GW to gamma gamma at B&O's rates.
  SOURCE: derived from the claims above and [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py]
  QUOTE: "fraction of rho_CMB = 9.762e-110" and "flux needed for 1 photon/s in that antenna = 3.146e-12 photons m^-2 s^-1 ; this is 2.99e+34 x the B&O flux"  (script log output)
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: medium

## Gaps
- Not found: a primary source quoting the ionospheric critical frequency (foF2 up to ~10-15 MHz) or the Earth-ionosphere-waveguide ELF receivers (Schumann resonance, ~8 Hz, ELF transmitters ~76 Hz); I used RE-04/RE-05 and the script's n_e = 1e6 cm^-3 figure (from quantitative RQ-10) instead. ELF antennas detect near-field/waveguide modes in the Earth-ionosphere cavity, not free photons, so they do not change the conclusion, but I did not source that.
- Not opened: PIXIE's own design paper (Kogut et al. 2011, arXiv:1105.2044) and NASA's status for PIXIE; a search summary from memory (not sourced) suggests NASA did not select PIXIE for its probe line. ESA Voyage 2050's spectroscopy theme (Chluba et al. 2021 white paper, RE-01) is a long-term plan; no launch date. BISOU (balloon pathfinder, Maffei et al.) and SPECTER exist as concepts; schedules not verified.
- Not found: Einstein Telescope and Cosmic Explorer construction timelines (the search returned no usable page); no LIGO O4 calibration error budget; no primary source for the O1/O2 5%/3 deg figure (search summary only); EBL / Fermi-LAT IGRB sensitivity numbers beyond RQ-14 (quantitative owns them).
- Not found: any experiment, built or planned, aimed at graviton-graviton to photon-photon scattering or vacuum GW decay. Laboratory and instrument searches returned only Gertsenshtein-type (background-field) conversion work, which is a different process and out of this facet's scope.
- No PAPER TO REQUEST: nothing here turns on a paywalled full text.
