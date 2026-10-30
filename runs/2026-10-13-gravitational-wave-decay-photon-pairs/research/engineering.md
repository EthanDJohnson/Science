# Research: engineering
status: final
Mandate: observational side: which instruments could see GW -> gamma gamma photons (radio below the plasma cutoff, CMB spectral-distortion missions, EBL / radio-background measurements, MeV gamma rays) and what each could actually constrain, with status and timeline of planned missions.
Access: lit_search INSPIRE ok (arXiv intermittently timed out / HTTP 429; INSPIRE used instead); fetch_text ok for arXiv, ucl.ac.uk repository and a University of Iowa copy of Gurnett 2013; WebSearch ok (summaries only); find_fulltext found no free copy of Gurnett 2013 (Science) or Seran 2005 (RSI).
Units: SI unless stated. B&O = Blas & Oller, arXiv:2607.24930 (version as fetched 2026-10-30, 13 pages, "v" not stated in the PDF text I read). Numbers marked [calc] come from runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py (log beside it).

Bottom line for this facet: B&O's photons for real mergers (frequency = GW frequency, ~1e-13 eV, ~150 Hz) lie 7 to 8 orders of magnitude below the lowest frequency any cosmological-background instrument has measured, are evanescent in the solar wind and local interstellar plasma, and arrive at ~5e-77 W/m^2 if B&O's own Fig. 2 luminosity is taken at face value. The only instrument-based constraints B&O use (FIRAS mu/y, the UV/X-ray and gamma-ray backgrounds, D/H) constrain integrated energy injection, not the 150 Hz photons. No planned mission within ~20 years changes this.

## Claims

- [RE-01] CLAIM: COBE/FIRAS, the only instrument behind B&O's mu and y bounds, measured the CMB spectrum in the 2 to 21 cm^-1 band (about 60 GHz to 630 GHz), with some information down to 0.4 cm^-1 (about 12 GHz); the limits are |y| < 15e-6 and |mu| < 9e-5 (95% CL, dimensionless) and the RMS deviation from a blackbody is < 50 ppm of the CMB peak. Its lowest frequency is ~8e7 times the 150 Hz of a GW150914-like merger [calc].
  SOURCE: Fixsen, Cheng, Gales, Mather, Shafer, Wright 1996, "The Cosmic Microwave Background Spectrum from the Full COBE FIRAS Data Set", ApJ 473, 576, arXiv:astro-ph/9605054, https://arxiv.org/pdf/astro-ph/9605054
  QUOTE: "For t he Comptonization and chemical potential we ﬁnd |y| <15 × 10−6 and |µ| <9 × 10−5 (95% CL)." and "All of the previous work in this frequency range (2 to 21 cm −1) was based on part of the data from a single detector." and "Thus there is information down to 0.4 cm −1 rather than only to 0.56 cm −1."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware (satellite, 10-month mission; trial count not applicable)
  CONFIDENCE: high

- [RE-02] CLAIM: B&O's "microwave and radio background" constraint is built on COBE/FIRAS mu and y only (|mu| < 9e-5, |y| < 1.5e-5, citing Fixsen 1996); it uses no low-frequency radio data. Their photon injection is treated as energy deposition after z ~ 3e6 and the bound is on the energy released, not on a spectral feature at the injected photon's frequency. Note B&O print |y| < 1.5e-5 where Fixsen's abstract says |y| < 15e-6 (same number).
  SOURCE: Blas & Oller 2026, "Gravitational waves decay in vacuum", arXiv:2607.24930, p. 5, https://arxiv.org/pdf/2607.24930
  QUOTE: "From the COBE/FIRAS mea- surement [60] one finds|µ|<9×10 −5,which implies the bound shown by the black line in Fig. 3." and "giving rise to a y-distortion, which COBE/FIRAS constrained to|y|< 1.5×10 −5 [60]."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RE-03] CLAIM: A spectral-distortion measurement constrains only the fractional energy released into the CMB: mu = 1.4 dE/E (Kogut et al. 2011, for release at 1e4 < z < 1e7). Using that conversion, FIRAS mu < 9e-5 allows dE/E < 6.4e-5, i.e. an injected energy density < 2.7e-18 J/m^3 (rho_CMB = 4.17e-14 J/m^3 at T0 = 2.7255 K); the FIRAS y limit (dE/E = 4y) gives 2.5e-18 J/m^3; PIXIE's 5-sigma mu < 1e-8 would correspond to 3.0e-22 J/m^3. These are my conversions [calc], not values quoted by the sources.
  SOURCE: Kogut et al. 2011, "The Primordial Inflation Explorer (PIXIE)", JCAP 07 (2011) 025, arXiv:1105.2044, https://arxiv.org/pdf/1105.2044 ; conversion arithmetic in [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py]
  QUOTE: "For energy injected at redshift 10 4 < z <107, the distorted spectrum is characterized by a chemical potential µ = 1.4∆E E (4.1) proportional to the fractional energy release ∆ E/E to the CMB"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: medium (the 1.4 factor holds for the mu-era only; y conversion 4y is the standard Compton-y relation, not quoted from a source here)

- [RE-04] CLAIM: Taking B&O's eq. 14 at face value (pair emissivity 8 pi G^2 rho_GW^2/15, in SI 8 pi G^2 rho^2/(15 c^7), hbar-free) with rho_GW at the N_eff-type bound Delta N_eff = 0.1 (rho_GW = 9.5e-16 J/m^3), the photon emissivity is 6.2e-110 m^-3 s^-1 and the energy injected over a Hubble time (4.35e17 s) is 1e-110 of rho_CMB at hbar*omega = 1e-13 eV, 1e-91 at 1 MeV, and 1e-87 at 10 GeV (top of B&O's Fig. 3 axis), without any stimulated (1+2f) boost. That is 80 or more orders of magnitude below the FIRAS-allowed 6e-5, so no spectral-distortion mission, existing or proposed, is within reach of the stochastic-background channel even if eq. 14 were right. (The quantitative facet gives the same emissivity; this is an independent recompute of the arithmetic, not a check of eq. 14 itself.)
  SOURCE: [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py]; eq. 14 from B&O arXiv:2607.24930
  SUMMARY: "Script prints rho_gamma = 4.175e-14 J/m^3, rho_GW = 9.481e-16 J/m^3, pair emissivity 3.083e-110 m^-3 s^-1, photons 6.166e-110; injected fraction of rho_CMB 1.029e-110 (1e-13 eV), 1.029e-91 (1 MeV), 1.029e-87 (10 GeV)."
  ACCESS: full-text (B&O equation) / analysis
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium (conditional on eq. 14, which other facets test; the 1.029e-110 figure at 1e-13 eV is read from the log line for 1e-13 eV after rho_gamma fix)

- [RE-05] CLAIM: PIXIE (proposed NASA Explorer-class mission) is a Fourier-transform spectrometer covering 400 channels from 30 GHz to 6 THz at 15 GHz resolution, forecast to reach mu < 1e-8 (compare FIRAS 9e-5, ~4 orders of magnitude). Its lowest frequency is ~2e8 times 150 Hz [calc-style ratio 30e9/150]. Forecast, not hardware.
  SOURCE: Kogut et al. 2011, JCAP 07 (2011) 025, arXiv:1105.2044, https://arxiv.org/pdf/1105.2044
  QUOTE: "PIXIE will map the absolute intensity and linear polarization (Stokes I,Q, and U parameters) over the full sky in 400 spectral channels spanning 2.5 decades in frequency from 30 GHz to 6 THz (1 cm to 50µm wavelength)." and "to a chemical potential µ <10−8 (Fig. 12)."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: simulation (design forecast; no hardware flown)
  CONFIDENCE: high

- [RE-06] CLAIM: Status of the next spectral-distortion mission: as of the BISOU paper (EPJ Web of Conferences, 2024) the space proposals PIXIE and PRISTINE "have not been successful"; the ESA Voyage 2050 programme selected spectral distortions as one of its themes (no mission or launch date is fixed); the active hardware step is BISOU, a CNES Phase-0 study of a balloon-borne Fourier-transform spectrometer that aims to measure "at least the Compton y-distortion" (expected y ~ 2e-6 against FIRAS |y| < 1.5e-5, a factor ~7 gap). No funded flight measurement of mu at the 1e-8 level exists, and none is scheduled inside ~20 years from what I could find. I found no 2026 status update.
  SOURCE: BISOU collaboration, "BISOU: a balloon project to measure the CMB spectral distortions", EPJ Web Conf. 293 (2024) 00012 (UCL repository copy), https://discovery.ucl.ac.uk/10193106/1/BISOU%20-%20A%20balloon%20project%20to%20measure%20the%20CMB%20spectral%20distortions.pdf
  QUOTE: "while the space mission proposals PIXIE 3 and PRISTINE (to ESA F-mission call) have not been successful, following two white papers, 4, 5 the ESA Voyage 2050 programme has selected this topic amongst its three themes." and "this CNES Phase 0 study will evaluate if such a spectrometer is sensitive enough to measure at least the Compton y-distortion" and "The COBE-FIRAS limit, |y| < 1.5× 10−5 (95% C.L.), is roughly one order of magnitude larger than the expected signal, 7 y≈ 2× 10−6."
  ACCESS: full-text
  STATUS: peer-reviewed (conference proceedings, EPJ Web of Conferences; journal number/page from a search summary, not verified in the PDF text)
  SETTING: n/a (planning status)
  CONFIDENCE: medium

- [RE-07] CLAIM: The radio-background measurement that B&O could have used (ARCADE 2, balloon, absolute radiometers at 3, 8, 10, 30 and 90 GHz) finds unexplained excess emission at 3 GHz, a power law of amplitude 1.06 +/- 0.11 K at 1 GHz with spectral index beta = -2.56 +/- 0.04 (brightness temperature; a Galactic-foreground-model dependent result, still debated). Its lowest channel, 3 GHz, is 2e7 times the 150 Hz of a merger [calc]. B&O do not use it (RE-02). Any photon injected at ~1e-13 eV is not a signal that ARCADE 2 could see.
  SOURCE: ARCADE 2 collaboration (Fixsen, Kogut et al.), "Interpretation of the ARCADE 2 Absolute Sky Brightness Measurement", ApJ 734, 6 (2011), arXiv:0901.0559, https://arxiv.org/pdf/0901.0559 ; frequencies from Fixsen et al. 2011, ApJ 734, 5, arXiv:0901.0555
  QUOTE: "The unexplained resid- ual emission is consistent with a power law with amplitude 1 .06 ± 0.11 K at 1 GHz, with a spectral index of β = − 2.56 ± 0.04." and (Fixsen 2011 abstract) "The ARCADE 2 instrument has measured the absolute temperature of the sky at frequencies 3, 8, 10, 30, and 90 GHz"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware (one 2006 balloon flight; trial count 1 flight)
  CONFIDENCE: high

- [RE-08] CLAIM: Ground-based radio astronomy is blocked below ~10 MHz by the terrestrial ionosphere (F-layer plasma frequency ~10 MHz), so a 150 Hz photon cannot be received by any radio telescope on Earth in the normal sense; the lowest-frequency cosmological radio instrument now being built is LuSEE-Night (NASA-DOE-ESA, lunar far side, 0.1 to 50 MHz, arrival planned 2027), whose lowest frequency is ~670 times the 150 Hz merger frequency and ~1e5 times the lowest frequency usable from the ground [calc].
  SOURCE: Yousuf et al. 2026, "Joint Estimation of Properties of the Lunar Subsurface and Galactic Foregrounds with LuSEE-night", Astron. J. 172, 123, arXiv:2604.21170, https://arxiv.org/pdf/2604.21170 ; band from Saliwanchik et al. 2024, Proc. SPIE 13102, arXiv:2407.07173
  QUOTE: "This is due to the∼10 MHz plasma frequency of the F-layer peak of the terrestrial ionosphere, below which the ionosphere becomes opaque" and (abstract, lit_search) "LuSEE-Night will measure the redshifted 21 cm transition of neutral hydrogen over a frequency range of 0.1-50 MHz" and "will reach the lunar far side in 2027."
  ACCESS: full-text (first quote); abstract (band and date)
  STATUS: peer-reviewed (Astron. J.) / preprint (SPIE proc. abstract)
  SETTING: n/a (planned hardware; not yet flown)
  CONFIDENCE: high

- [RE-09] CLAIM: A 150 Hz electromagnetic wave is evanescent wherever the electron density exceeds n_crit = eps0 m_e (2 pi f)^2 / e^2 = 2.8e2 m^-3 = 2.8e-4 cm^-3 [calc, checked: f_p(1 cm^-3) = 8979 Hz vs textbook 8980 Hz]. Voyager 1 measured n_e ~ 0.002 cm^-3 in the outer heliosphere (f_p ~ 400 Hz [calc], 2.7x above 150 Hz) and ~0.08 cm^-3 (plasma oscillations at 2.6 kHz) in the local interstellar medium (f_p ~ 2.5 kHz [calc], 17x above 150 Hz). So a 150 Hz photon from a merger cannot propagate into the solar system, nor through the interstellar plasma of the Galaxy, at those densities. Only the mean intergalactic medium is transparent: n_e0 = 2.2e-7 cm^-3, f_p0 = 4.2 Hz today [calc], and a photon observed at 150 Hz was blocked in the mean IGM only at z > ~1.3e3.
  SOURCE: Gurnett, Kurth, Burlaga, Ness 2013, "In Situ Observations of Interstellar Plasma with Voyager 1", Science 341, 1489, University of Iowa author copy https://space.physics.uiowa.edu/~dag/publications/2013_InSituObservationsOfInterstellarPlasmaWaveVoyager_Science.pdf ; arithmetic [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py]
  QUOTE: "by a large increase in plasma density, from about 0.002 per cubic centimeter (cm −3) in the outer heliosphere, to about 0.1 cm −3 in the interstellar medium. On 9 April 2013, the Voyager 1 plasma wave instrument began detecting locally generated electron plasma oscillations at a frequency of about 2.6 kilohertz. This oscillation frequency corresponds to an electron density of about 0.08 cm −3"
  ACCESS: full-text (author copy of the published paper; Science page itself had no free copy)
  STATUS: peer-reviewed
  SETTING: hardware (in-situ spacecraft measurement; one spacecraft, single crossing)
  CONFIDENCE: high for the densities and f_p arithmetic; medium for the statement about propagation in the full Galactic ISM and solar wind at Earth (I did not source a solar-wind density at 1 AU; typical 5 to 10 cm^-3 would give f_p ~ 20 to 28 kHz, my standard-knowledge estimate, unsourced)

- [RE-10] CLAIM: B&O themselves note that their Fig. 2b photons propagate to detectors only in a corner of parameter space far from physical mergers: "In the leftmost corner of the allowed region in Fig. 2b), frequencies are above keV and may propagate towards our detectors", while along the physical-merger (nominal frequency) line the number luminosity is "still modest, ~1e6 s^-1". They do not discuss a plasma cutoff or a receiver. They close: "even if our first esti- mates are not particularly optimistic, detecting them could open a new avenue". So within the paper, the merger-photon channel is not offered as detectable.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, pp. 4 and 6, https://arxiv.org/pdf/2607.24930
  QUOTE: "Along the nominal frequencyL γ is larger than in panel a), though still modest,∼10 6 s−1. In the leftmost corner of the allowed region in Fig. 2b), frequencies are above keV and may propagate towards our detectors."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RE-11] CLAIM: Taking B&O's number luminosity L_gamma ~ 1e6 photons/s at the nominal GW150914-like frequency (150 Hz, h*nu = 9.94e-32 J = 6.2e-13 eV, wavelength 2.0e6 m) and distance 410 Mpc, the photon power is 9.9e-26 W, the flux at Earth 4.9e-77 W/m^2 (5.0e-46 photons m^-2 s^-1), equivalent E_rms = 1.4e-37 V/m and B_rms = 4.6e-46 T. Per event (L_gamma x 5 ms) ~5e3 photons carrying 5e-28 J, a fraction 1.4e-75 of the 3.6e47 J (2 Msun c^2) GW energy; an Earth-sized disk (1.3e14 m^2) would intercept 3e-34 photons during the 5 ms. Isotropic emission and no absorption are assumed, both generous. Detection by any receiver is therefore not a question of incremental sensitivity: the field is ~4.6e-46 T, and I could not source a receiver noise floor to compare (see Gaps).
  SOURCE: [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py] using L_gamma from B&O arXiv:2607.24930 p. 4 and GW150914 parameters (150 Hz, 410 Mpc) as in the brief
  SUMMARY: "Script output: photon power at source = 9.939e-26 W ; flux at Earth = 4.942e-77 W/m^2 ; E_rms = 1.364e-37 V/m ; B_rms = 4.551e-46 T ; photons emitted per event 5.000e+03 ; ratio to GW energy 1.390e-75 ; photons crossing Earth disk during t_m 3.170e-34."
  ACCESS: full-text (inputs) / analysis
  STATUS: preprint (inputs); the arithmetic is mine
  SETTING: analysis
  CONFIDENCE: medium (rests on B&O's "~1e6 s^-1" read from the text, not from their figure; the 5 ms duration is the B&O/quantitative-facet scaling, not re-derived here)

- [RE-12] CLAIM: A CMB-referenced detection of 150 Hz photons is also hopeless on occupation grounds: the thermal CMB occupation at 150 Hz is kT/(h nu) = 3.8e8 photons per mode (x = h nu/kT = 2.6e-9, Rayleigh-Jeans), so B&O's stimulation factor (1+2f) = 7.6e8 [calc]; the RJ specific intensity there is 1.9e-35 W m^-2 sr^-1 Hz^-1, compared with ~3e-77 W m^-2 Hz^-1 for the merger photons spread over a 1% band. That CMB, however, cannot be observed at 150 Hz either, since the Galaxy is opaque (RE-09), so this comparison is the principle, not an observable.
  SOURCE: [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/engineering_detectability.py]
  SUMMARY: "x = 2.641e-09; occupation n = 3.786e+08; 1+2f = 7.572e+08; CMB specific intensity at 150 Hz (RJ) = 1.884e-35 W m^-2 sr^-1 Hz^-1; signal spectral flux density over 1.5 Hz = 3.294e-77 W m^-2 Hz^-1."
  ACCESS: analysis
  STATUS: n/a (own calculation)
  SETTING: analysis
  CONFIDENCE: high for the arithmetic

- [RE-13] CLAIM: The extreme-low-frequency magnetometers that exist (space search-coil magnetometers; e.g. the three-axis search coil on DEMETER) work in the 1 Hz to 20 kHz band in the Earth's magnetosphere, so the 150 Hz band is instrument-accessible only locally (Earth's ionosphere/magnetosphere, where natural ELF noise and Schumann-type resonances dominate), not as a propagating cosmic signal: the cosmic wave is evanescent before it gets there (RE-09). I did not retrieve a noise-floor number (see Gaps), so I do not state the instrument sensitivity.
  SOURCE: Seran et al. 2005, "An optimized low-frequency three-axis search coil magnetometer for space research", Rev. Sci. Instrum. 76, doi:10.1063/1.1884026
  QUOTE: "The design of a three-axis search coil magnetometer in the 1 Hz–20 kHz range developed for the scientific satellite DEMETER is described."
  ACCESS: abstract
  STATUS: peer-reviewed
  SETTING: hardware (one satellite instrument)
  CONFIDENCE: medium

- [RE-14] CLAIM: The upper end of B&O's constraints (photofission, gamma-ray background) rests on abundance and background-flux data, not on detecting the injected photons. The deuterium abundance constraint (B&O require a shift delta_D < 0.03, i.e. 3%) is tested against the current precision measurement 1e5 (D/H)_P = 2.527 +/- 0.030 (a 1.2% determination, from seven high-precision damped-Lyman-alpha systems, six earlier plus one new, Cooke et al. 2018). That precision is already better than B&O's 3% criterion; a further factor of a few from ELT-class spectrographs is plausible but I found no dated programme. B&O's own conclusion is only that cosmological sources would need to be extremely strong (their Fig. 3 y-axis: bounds on sqrt(Gamma eps E_rel/Msun) in Gpc^-3/2 yr^-1/2, with the plotted lines spanning many orders of magnitude).
  SOURCE: Cooke, Pettini, Steidel 2018, "One Percent Determination of the Primordial Deuterium Abundance", ApJ 855, 102, arXiv:1710.11129, https://arxiv.org/pdf/1710.11129 ; B&O arXiv:2607.24930 SM SF
  QUOTE: "we deduce that the primordial deuterium abundance is log 10 (D/H)P =−4.5974± 0.0052 or, expressed as a linear quantity, 10 5(D/H)P = 2.527± 0.030; this value corresponds to a one percent determination of the primordial deuterium abundance." and (B&O) "requiringδ D <0.03 yields the bound shown by the green line in Fig. 3"
  ACCESS: full-text
  STATUS: peer-reviewed (Cooke); preprint (B&O)
  SETTING: n/a (astrophysical observation; one new system plus six earlier ones)
  CONFIDENCE: high for the numbers; low for the "plausible factor of a few" remark (my judgement, unsourced)

- [RE-15] CLAIM: The next gamma-ray instrument that would improve the MeV background (the band relevant to B&O's D photofission threshold, 2.23 MeV, and 4He thresholds near 20 MeV) is COSI, a NASA Small Explorer wide-field Compton telescope, survey band 0.2 to 5 MeV, planned launch 2027. This is a source-detection/line mission; it does not search for GW-induced photons and, for the B&O photofission bound, the effect is on BBN abundances, not the present-day background. Planned launch date as of the 2023 ICRC proceedings; I did not find a later slip.
  SOURCE: Tomsick et al. 2023, "The Compton Spectrometer and Imager", PoS ICRC2023 745, arXiv:2308.12362, https://arxiv.org/pdf/2308.12362
  QUOTE: "The Compton Spectrometer and Imager (COSI) is a NASA Small Explorer (SMEX) satellite mission in development with a planned launch in 2027. COSI is a wide-field gamma-ray telescopedesignedtosurveytheentireskyat0.2-5MeV."
  ACCESS: full-text
  STATUS: preliminary (conference proceedings from the cosmic-ray conference; reviewed proceedings but not a journal)
  SETTING: n/a (planned hardware)
  CONFIDENCE: medium

- [RE-16] CLAIM: The other detection side, the GW detectors themselves, cannot test the depletion claim without a model: B&O's "depletion" of a signal over its path (time tau_h) would be a loss of GW strain with distance, which is degenerate with luminosity distance. I found no published constraint on GW damping by photon-pair emission; the nearest existing tests (standard-siren distance comparison, GW170817 and GW190521, for modified GW propagation) constrain a different, beyond-GR parameterisation. (Negative result; the item is here to scope what is not testable with LVK, LISA, ET or CE data, not as a claim of a limit.)
  SOURCE: Mastrogiovanni et al. 2021, "Gravitational wave friction in light of GW170817 and GW190521", JCAP 02 (2021) 043, arXiv:2010.04047, https://arxiv.org/pdf/2010.04047
  QUOTE: "We use the gravitational wave (GW) events GW170817 and GW190521, together with their proposed electromagnetic counterparts, to constrain cosmological parameters and theories of gravity beyond General Relativity (GR)."
  ACCESS: abstract
  STATUS: peer-reviewed
  SETTING: analysis (2 events with counterparts)
  CONFIDENCE: low (shows that the nearest test is a different quantity; no direct limit exists as far as I found)

## Gaps
- Noise floor of ELF/VLF magnetometers (search coil, SQUID, atomic) at 100 to 200 Hz, and Schumann/ionospheric noise levels there: not retrieved. The conclusion rests on the 40-order gap between 5e-46 T and any plausible floor and on plasma evanescence (RE-09), not on a sourced noise number. PAPER TO REQUEST: 10.1063/1.1884026 | An optimized low-frequency three-axis search coil magnetometer for space research | the DEMETER search-coil noise level at 100-200 Hz.
- Solar-wind electron density at 1 AU (for the f_p ~ 20 kHz cutoff at Earth) and the lower frequency limit of Wind/WAVES and Parker FIELDS: only a search summary (FIELDS LFR roughly 10.5 kHz to 1.7 MHz) was obtained, not quoted. The outer-heliosphere/ISM Voyager densities (RE-09) are enough to show the cutoff.
- No source found for a mission with sensitivity below 0.1 MHz in the planned period; sub-MHz space radio (Wind, Parker, Voyager plasma-wave) sees plasma emissions above ~kHz only.
- Status of COSMO, TMS and other ground/balloon spectrometers, and any 2025-2026 PIXIE/Voyage 2050 mission step: not found (the BISOU proceedings are from 2024).
- Fermi-LAT IGRB, UV/X-ray background data (B&O's Fig. 3) are covered by the quantitative facet (RQ-19); not repeated here.
- A GW-detector test of GW depletion by pair emission: no literature found (RE-16).
- This facet did not check whether photofission and CMB bounds use the right photon spectrum or the right propagation (plasma, cascade); that is for the constraints lens.
