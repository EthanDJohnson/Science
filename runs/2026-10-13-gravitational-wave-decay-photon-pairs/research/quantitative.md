# Research: quantitative
status: final
Mandate: numbers and inputs: merger parameters, rho_GW bounds, CMB mu/y, EBL, BBN photodisintegration, ULDM, plasma frequencies.
Access: lit_search INSPIRE ok, arXiv ok (fetch_text on arxiv.org/pdf works); WebFetch domains that worked: see claims
Note: B&O = Blas & Oller arXiv:2607.24930 (version read: the PDF served by arxiv.org/pdf/2607.24930 at fetch time, 13 pages, i.e. the current version; v1/v2 not distinguished by the fetcher). Units: SI for astrophysical numbers unless stated.

## Claims
- [RQ-01] CLAIM: GW150914 radiated 3.0 (+0.5/-0.5) M_sun c^2 in GW (source frame), at peak GW luminosity 3.6 (+0.5/-0.4) x 10^56 erg/s = 3.6e49 W (SI conversion by this note: 1 erg/s = 1e-7 W), equivalent to 200 (+30/-20) M_sun c^2/s; signal swept 35 to 250 Hz, amplitude maximum at ~150 Hz, over 0.2 s in about 8 cycles; luminosity distance 410 (+160/-180) Mpc, z = 0.09 (+0.03/-0.04); source-frame masses 36 (+5/-4) and 29 (+4/-4) M_sun, final 62 (+4/-4) M_sun. All 90% credible intervals.
  SOURCE: Abbott et al. (LIGO/Virgo) 2016, "Observation of Gravitational Waves from a Binary Black Hole Merger", Phys. Rev. Lett. 116, 061102, arXiv:1602.03837 (PDF read)
  QUOTE: "The estimated total energy radiated in gravitational waves is 3.0+0.5-0.5 M⊙c2. The system reached a peak gravitational-wave luminosity of 3.6+0.5-0.4 × 1056 erg/s, equivalent to 200+30-20 M⊙c2/s." ; "Over 0.2 s, the signal increases in frequency and amplitude in about 8 cycles from 35 to 150 Hz, where the amplitude reaches a maximum." ; "The source lies at a luminosity distance of 410+160-180 Mpc corresponding to a redshift z = 0.09+0.03-0.04."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-02] CLAIM: B&O's merger-phase inputs (Fig. 2b) are scalings anchored to GW150914: nu ~ 150 Hz x (65 M_sun/M), E_rel ~ 2 M_sun c^2 x (M/65 M_sun), merger-phase duration t_m ~ 5 ms x (M/65 M_sun) (about one period). The GW150914 total radiated energy in RQ-01 is 3.0 M_sun c^2, so B&O's 2 M_sun c^2 is the energy of the merger phase only (their choice; not independently checked here). The stated photon luminosity at the nominal merger frequency is "~10^6 s^-1" (a number luminosity, photons per second). Frequencies in the allowed region are said to be below kHz for inspiral, and "above keV" only in the leftmost corner of the allowed merger region.
  SOURCE: Blas & Oller 2026, "Gravitational waves decay in vacuum", arXiv:2607.24930, p. 3-4 and footnote 4-5
  QUOTE: "ν≈150 Hz×(65M ⊙/M), E rel ≈ 2M⊙c2×(M/65M⊙) and tm≈5 ms×(M/65M ⊙), where we anchor the total mass to GW150914" ; "Along the nominal frequency L γ is larger than in panel a), though still modest, ∼10 6 s−1."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RQ-03] CLAIM: B&O's inspiral inputs: quasi-circular inspiral, chirp mass M_c, quadrupole formula; time to climb a fractional bandwidth eps in frequency t_eps = (5 eps/12)(2 (G M_c)^5 omega_s^8)^(-1/3) [as printed: 5ϵ/12 (2(GMc)^5 ω_s^8)^(1/3), exponent sign garbled in extraction; check against the PDF before use]; equal-mass binary M = 2^(6/5) M_c; eps = 0.1; hatched allowed region bounded above by f_ISCO and below by tau = 1/(eps omega_s) or tau = t_eps. For GW150914 ringdown they take eps ~ 0.15 (Carullo et al. 2019).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, p. 3, footnote 5, and SM S-B
  QUOTE: "For ϵ= 0.1 the period 1/ν and the coherence time 1/ϵω s roughly coincide. In the ringdown phase of GW150914 ϵ≈0.15 [41]." ; "the time during which the frequency grows from ω s to ω s(1 +ϵ) is t ϵ = 5ϵ 12(2(GMc)5ω8s)1/3"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RQ-04] CLAIM: B&O adopt COBE/FIRAS bounds |mu| < 9e-5 and |y| < 1.5e-5 (dimensionless) for their CMB-distortion constraints, and photofission thresholds Q(gamma D -> pn) = 2.23 MeV, Q(gamma 4He -> pT) = 19.8 MeV, Q(gamma 4He -> n 3He) = 20.6 MeV, Q(gamma 4He -> pnD) = 26.1 MeV; D photofission bound from requiring delta_D < 0.03; n_e = eta n_gamma0 (1 - Y/2) with eta = 6.1e-10, Y ~ 0.25. Photon injection is only considered after z ~ 3e6 ("before they simply thermalize"); mu-era 1e5 <~ z <~ z_a ~ 3e6, y-era 1e3 <~ z <~ 1e5.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, p. 5 and SM S-E, S-F
  QUOTE: "From the COBE/FIRAS measurement [60] one finds |µ|<9×10 −5" ; "COBE/FIRAS constrained to |y|< 1.5×10 −5 [60]" ; "QγD→pn = 2.23 MeV, Qγ 4He→pT = 19.8 MeV, Qγ 4He→n 3He = 20.6 MeV, Qγ 4He→pnD = 26.1 MeV" ; "requiring δD <0.03 yields the bound shown by the green line in Fig. 3"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RQ-05] CLAIM: B&O ULDM inputs: number of quanta N_phi ~ 6e87 (10^-22 eV/m_DM)(4e-3/v)^3 (Omega_DM/0.26) x_MW, with v the velocity dispersion (dimensionless, units of c), x_MW ~ 1e5 the halo boost for the Milky Way (from Read 2014). Photon-pair decay of GWs into the ULDM channel quoted as dP/dt = 7 G^2 N0^2 omega_s^3 sigma_omega^2/(450 pi) and tau_phi = (54/7) tau for omega_s >> m_DM.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, p. 5
  QUOTE: "at the cosmological mean DM energy density Nϕ≃6×10 87 10−22 eV mDM 410−3 v 3 ΩDM 0.26xMW,(16) where v represents the velocity dispersion, ΩDM its average relative energy density and xMW is the boost one gets in a DM halo; for the Milky Way halo xMW∼10 5 [47]." ; "dP/dt = 7G 2N2 0ω3 sσ2 ω/450π. The resulting reaction time is τ ϕ = (54/7)τ"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium (extraction of eq. 16 is garbled; verify the exponent layout against the PDF)

- [RQ-06] CLAIM: COBE/FIRAS (original 1996 analysis) 95% CL limits are |y| < 15e-6 and |mu| < 9e-5 (dimensionless), from the fits mu = -1 +/- 4 x 10^-5 and y = -1 x 10^-6 with uncertainty entries 6, 4, 7 (x 10^-6). Table 2 prints, for y, value -1 then three uncertainty entries 6, 4, 7 (x 10^-6), and for mu, value -1 then 4, 1, 4 (x 10^-5); the header prints all three columns as "uncertainty", and in the other rows the third equals the quadrature sum of the first two, so the columns are presumably statistical, systematic, total (inference by this note; not combined here). B&O use the 1996 limits. SUPERSEDED for mu: a re-analysis of the same FIRAS data (Bianchini & Fabbian 2022, Phys. Rev. D 106, 063527, arXiv:2206.02762) gives |<mu>| < 47 x 10^-6 at 95% CL, "a factor of ~2" tighter than the 1996 value, so B&O's mu bound (black line, Fig. 3) is conservative by about a factor 2 in mu if the re-analysis is adopted; the y limit was not updated in the abstract I read. A Crossref hit (Dhal et al. 2025, Exp. Astron. 60, doi:10.1007/s10686-025-10035-7) was seen by title only.
  SOURCE: Fixsen et al. 1996, "The Cosmic Microwave Background spectrum from the full COBE FIRAS data set", Astrophys. J. 473, 576, arXiv:astro-ph/9605054 (PDF read); Bianchini & Fabbian 2022, arXiv:2206.02762 (PDF read, abstract)
  SOURCE: Fixsen, Cheng, Gales, Mather, Shafer, Wright 1996, "The Cosmic Microwave Background spectrum from the full COBE FIRAS data set", Astrophys. J. 473, 576, arXiv:astro-ph/9605054 (PDF read)
  QUOTE: "For the Comptonization and chemical potential we find |y| <15 × 10−6 and |µ| <9 × 10−5 (95% CL)." ; "The current FIRAS result is µ =−1 ± 4 × 10−5, or a 95% confidence level upper limit of |µ| <9 × 10−5." ; Table 2 row: "y para -1 6 4 7 ×10−6 µ para -1 4 1 4 ×10−5" ; re-analysis: "We provide an updated constraint on the µ distortion monopole |⟨µ⟩| < 47× 10−6 at 95% confidence level that sharpens the previous FIRAS estimate by a factor of ∼ 2."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-07] CLAIM: Planck 2018 with BAO constrains N_eff = 2.99 +/- 0.17 (68%), i.e. 2.99 +0.34/-0.33 (95%, TT,TE,EE+lowE+lensing+BAO), against the Standard Model 3.046; without BAO N_eff = 2.89 +/- 0.19. This is the input behind the "N_eff bounds on the energy density of GWs" that B&O cite for rho_GW.
  SOURCE: Planck Collaboration 2020, "Planck 2018 results. VI. Cosmological parameters", A&A 641, A6, arXiv:1807.06209 (PDF read)
  QUOTE: "we constrain the effective extra relativistic degrees of freedom to be Neff = 2.99±0.17, in agreement with the Standard Model prediction Neff = 3.046" ; "Neff = 2.99+0.34 −0.33 (95 %, TT,TE,EE+lowE+lensing +BAO)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-08] CLAIM: A relic GW background present at BBN is bounded by integral over d(ln f) of h0^2 Omega_gw(f) <= 5.6e-6 (N_nu - 3), equivalently (rho_gw/rho_gamma)_0 <= 0.227 (N_nu - 3). It applies only to GWs already present at T ~ MeV, "not to any stochastic background produced later, like backgrounds of astrophysical origin". Using h = 0.674, rho_crit c^2 = 7.67e-10 J/m^3 (SI): for Delta N_eff = 0.1, 0.17, 0.3 the bound gives rho_GW <= 9.5e-16, 1.6e-15, 2.8e-15 J/m^3 (Omega_GW integrated <= 1.2e-6, 2.1e-6, 3.7e-6). [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py]
  SOURCE: Maggiore 2000, "Gravitational wave experiments and early universe cosmology", Phys. Rept. 331, 283, arXiv:gr-qc/9909001, eqs. 117-118 (PDF read); numbers: this note's calc
  QUOTE: "∫ f =∞ f =0 d(logf ) h2 0Ωgw(f ) ≤ 5.6 × 10−6(Nν − 3). (118)" ; "Of course this bound holds only for GWs that were already produced at time of nucleosynthesis (T ∼ MeV, t ∼ sec). It does not apply to any stochastic background produced later, like backgrounds of astrophysical origin."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high for the bound form; the 5.6e-6 coefficient is the 2000 value (h0^2 rho_gamma/rho_c = 2.481e-5); not re-derived against current T0.

- [RQ-09] CLAIM: LIGO-Virgo-KAGRA O1+O2+O3 isotropic stochastic limit: Omega_GW <= 5.8e-9 (95% credible, flat spectrum, log-uniform prior, 99% of sensitivity from 20-76.6 Hz); Omega_GW(25 Hz) <= 3.4e-9 for spectral index 2/3 (log-uniform) and 1.7e-8 (flat, uniform prior). With rho_crit c^2 = 7.67e-10 J/m^3 the flat limit is rho_GW per e-fold of frequency <= 4.4e-18 J/m^3. Applying B&O's eq. 14 as printed to that density gives dP/dtdV = 6.8e-115 pairs m^-3 s^-1 [calc]. (Ground-based limit is ~9 orders below the BBN-type integrated bound's density, so eq. 14 would be at most ~1e-115 for terrestrial-band backgrounds.)
  SOURCE: LIGO/Virgo/KAGRA 2021, "Upper limits on the isotropic gravitational-wave background from Advanced LIGO and Advanced Virgo's third observing run", Phys. Rev. D 104, 022004, arXiv:2101.12130 (PDF read)
  QUOTE: "We find that the dimensionless energy density ΩGW≤ 5.8× 10−9 at the 95% credible level for a flat (frequency- independent) GWB, using a prior which is uniform in the log of the strength of the GWB, with 99% of the sensitivity coming from the band 20-76.6 Hz"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high (the 2021 O3 value; no later LVK isotropic limit was searched for - see Gaps)

- [RQ-10] CLAIM: NANOGrav 15-yr: common-spectrum GW background strain amplitude A = 2.4 (+0.7/-0.6) x 10^-15 (median, 90% credible) at f_ref = 1/yr for h_c ~ f^-2/3. This note's conversion Omega_GW(1/yr) = 2 pi^2 f^2 A^2/(3 H0^2) = 8.0e-9 (H0 = 67.4 km/s/Mpc; ignoring the A uncertainty), i.e. rho_GW ~ 6.1e-18 J/m^3 per e-fold near f = 3.2e-8 Hz [calc]. Evidence level is 3.5-4 sigma for Hellings-Downs correlation (a frequentist statistic p = 5e-5 to 1.9e-4); the source origin (SMBH binaries vs exotic) is not settled.
  SOURCE: Agazie et al. (NANOGrav) 2023, "The NANOGrav 15 yr Data Set: Evidence for a Gravitational-Wave Background", ApJL 951, L8, arXiv:2306.16213 (PDF read)
  QUOTE: "the strain amplitude is 2.4+0.7 −0.6× 10−15 (median + 90% credible interval) at a reference frequency of 1 yr −1." ; "yields p = 5× 10−5–1.9× 10−4 (approx. 3.5–4σ)"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high for A; medium for the Omega conversion (my formula, not the paper's)

- [RQ-11] CLAIM: Reproducing B&O's stochastic-background emissivity: eq. 14 (dP/dtdV = 8 pi G^2 rho_GW^2/15, natural units) evaluated with the BBN-type bound of RQ-08 gives photon emissivity 2 dP/dtdV = 6.1e-110 (Delta N_eff = 0.1), 1.8e-109 (0.17) and 5.5e-109 (0.3) photons m^-3 s^-1 (SI), so B&O's quoted "~1e-110 m^-3 s^-1" is reproduced to within a factor of a few to ~50 by taking eq. 14 as printed (this checks the numerics of the number, not the formula). For LVK O3 or PTA densities the same formula gives 1e-114 to 3e-114 photons m^-3 s^-1. Conversion used: G_nat = G/(hbar c^5) [J^-2], rate density = (8 pi/15) G_nat^2 (rho (hbar c)^3)^2 / ((hbar c)^3 hbar); cross-check G_nat = 1/(M_P c^2)^2 with M_P c^2 = 1.221e19 GeV printed equal.
  SOURCE: B&O eq. 14 (arXiv:2607.24930 p. 4); computation: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py
  QUOTE: "The number emissiv- ity is absolutely negligible, 2dP/dtdV≈10 −110 m−3s−1, assuming the Neff bounds on the energy density of GWs [7, 42]."
  ACCESS: full-text (B&O); calculation by this note
  STATUS: preprint (B&O); calc is analysis
  SETTING: analysis
  CONFIDENCE: high for the arithmetic, given the printed formula

- [RQ-12] CLAIM: Sizing B&O's merger numbers with their printed formulas (eq. 8, 10), nu = 150 Hz (hbar omega_s = 6.20e-13 eV), E_rel = 2 M_sun c^2 = 3.57e47 J, N0 = E_rel/(hbar omega_s) = 3.6e78 gravitons, sigma_omega = eps omega_s: eq. 8 pair rate = 7.0e-5 s^-1 (eps = 0.15) or 3.1e-5 s^-1 (eps = 0.10); photon rate (2 x pair) 1.4e-4 s^-1 or 6.2e-5 s^-1; eq. 10 reaction time tau = 7.2e3 s (eps = 0.15), 1.6e4 s (eps = 0.10), against a merger duration t_m = 5 ms and coherence time 1/(eps omega_s) = 7.1 ms. So without stimulation tau/t_m ~ 1.4e6 and the expected photon yield in t_m is ~7e-7 photons per merger. With GW150914's full 3.0 M_sun c^2: pair rate 1.6e-4 s^-1, tau = 3.2e3 s. B&O's photon luminosity of "~1e6 s^-1" at the nominal merger frequency therefore relies on the CMB stimulation factor: at hbar omega_s = 6.2e-13 eV, kT0/(hbar omega_s) = 3.8e8, so (1 + 2 f_gamma) = 7.6e8 (T0 = 2.7255 K); 1.4e-4 s^-1 x 7.6e8 = 1.1e5 s^-1, within a factor ~10 of their ~1e6 s^-1 (their exact prescription for the stimulation factor, per photon or per pair, was not recomputed here). The tau << t_m requirement is met only after multiplying the rate by (1+2f) ~ 7.6e8 (tau -> ~1e-5 s).
  SOURCE: B&O arXiv:2607.24930 eqs. 8-10, p. 3-4; computation: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py
  QUOTE: "Equation (8) is a probability per unit time for τ≪δt∼1/σ ω, with Poissonian uncertainty √σωτ." ; "Nγ(t)≈G 2N2 0 6ω3 sσ2 ωt 25π" ; "τ= 25π 6G2E2 relωsσ2ω"
  ACCESS: full-text (B&O); computation by this note
  STATUS: preprint; analysis
  SETTING: analysis
  CONFIDENCE: medium (formulas as printed in the extraction; the sigma_omega = eps omega_s identification and the stimulation prescription are assumptions of this note)

- [RQ-13] CLAIM: Scale of the GW150914 signal at Earth (SI): peak flux = L_peak/(4 pi d_L^2) = 1.8e-2 W/m^2 for L_peak = 3.6e49 W and d_L = 410 Mpc (1.27e25 m), i.e. a peak GW energy density of 6.0e-11 J/m^3 (flux/c). Total energy fluence = 3.0 M_sun c^2/(4 pi d_L^2) = 5.36e47 J/(2.01e51 m^2) = 2.7e-4 J/m^2 (hand arithmetic from the calc's E_rad and d_L; the fluence itself is not printed by the script). This is the rho_GW a detector sees from the one burst; any hypothetical eq. 14-like rate at this density would be ~1e-100 m^-3 s^-1 [calc], which is why a vacuum-decay signal over the propagation path is unobservable at the GW amplitude actually measured, even if the formula held.
  SOURCE: computation from RQ-01 inputs: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py
  SUMMARY: "calc output: peak flux at Earth [W/m^2] = 0.0179, peak GW energy density at Earth [J/m^3] = 5.97e-11; eq.14 as printed at that density: 1.2e-100 pairs m^-3 s^-1"
  ACCESS: full-text (inputs from RQ-01)
  STATUS: analysis
  SETTING: analysis
  CONFIDENCE: medium (eq. 14 is for a stochastic background; used here only as a scale check)

- [RQ-14] CLAIM: GWTC-4 (O1-O4a) local merger rates at z = 0, central 90% credible intervals: BNS 7.6-250 Gpc^-3 yr^-1, NSBH 9.1-84 Gpc^-3 yr^-1, BBH 14-26 Gpc^-3 yr^-1. This updates GWTC-3 (arXiv:2111.03634): BNS 10-1700 Gpc^-3 yr^-1, NSBH 7.8-140 Gpc^-3 yr^-1, BBH 17.9-44 Gpc^-3 yr^-1 at z = 0.2 (a different reference redshift, with BBH rate rising as (1+z)^kappa, kappa = 2.9 +1.7/-1.8). These are the population rates Gamma that enter B&O's Fig. 3 variable sqrt(Gamma eps E_rel)/M_sun in Gpc^-3/2 yr^-1/2.
  SOURCE: LVK 2025, "GWTC-4.0: Population Properties of Merging Compact Binaries", arXiv:2508.18083 (PDF read); LVK 2023 GWTC-3 population, Phys. Rev. X 13, 011048, arXiv:2111.03634 (PDF read)
  QUOTE: "We infer the local merger rates (i.e., at redshift z = 0) to be 7.6–250 Gpc −3 yr−1 for binary neutron stars, 9.1–84 Gpc−3 yr−1 for neutron star–black hole binaries, and 14–26 Gpc −3 yr−1 for binary black holes; all values reflect central 90% credible intervals."
  ACCESS: full-text
  STATUS: preprint (GWTC-4; check journal status) ; peer-reviewed (GWTC-3)
  CONFIDENCE: high

- [RQ-15] CLAIM: Radio/microwave background (relevant to B&O's "microwave and radio backgrounds" bound and their UV/X-ray and gamma-ray backgrounds): ARCADE 2 finds an extragalactic excess of 50 +/- 7 mK at 3.3 GHz on top of CMB temperature 2.730 +/- 0.004 K; fit of excess antenna temperature T_R = 1.19 +/- 0.14 K (nu/1 GHz)^beta with beta = -2.62 +/- 0.04 (T0 = 2.729 +/- 0.004 K). Combined with literature data the excess is T = 1.26 +/- 0.09 K (nu/nu0)^(-2.60 +/- 0.04) from 22 MHz to 10 GHz. These bound a radio-frequency photon injection at GHz. GW-band photons (150 Hz = 6.2e-13 eV, RQ-12) lie about seven orders of magnitude below 22 MHz, the lowest frequency in the combined radio fit, so these data do not constrain them directly.
  SOURCE: Fixsen et al. 2011, "ARCADE 2 Measurement of the Extra-Galactic Sky Temperature at 3-90 GHz", ApJ 734, 5, arXiv:0901.0555 (PDF read)
  QUOTE: "The ARCADE 2 data alone show an extragalactic rise of 50 ± 7 mK at 3.3 GHz in addition to a CMB temperature of 2.730 ± .004 K." ; "We obtain best-fit values T0 = 2.729 ±0.004 K, TR = 1.19±0.14 K and β = −2.62±0.04 for reference frequency ν0 = 1 GHz"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-16] CLAIM: Plasma frequencies (this note's calc; fully ionised H+He, Omega_b h^2 = 0.0224, h = 0.674, Y = 0.245): mean cosmic n_e0 = 0.221 m^-3 = 2.2e-7 cm^-3, hbar omega_p0 = 1.7e-14 eV (f_p = 4.2 Hz) today; scales as (1+z)^(3/2): 4.9e-14 eV (z = 1), 6.4e-13 eV (z = 10), 6.4e-10 eV (z = 1100), 5.5e-7 eV (z = 1e5), 9.1e-5 eV (z = 3e6). Milky Way ISM n_e = 0.03 cm^-3 gives f_p = 1.56 kHz (hbar omega_p = 6.4e-12 eV). Ionosphere F-layer peak n_e ~ 1e12 m^-3 gives f_p = 9.0 MHz. Photon energies for comparison: 150 Hz -> 6.2e-13 eV, 1 kHz -> 4.1e-12 eV. Consequence: a photon of hbar omega ~ 6e-13 eV (150 Hz) is below the cold-plasma frequency of the mean fully ionised cosmic medium for z >~ 10 (omega_p = 6.4e-13 eV at z = 10), below that of the Galactic ISM at n_e = 0.03 cm^-3 (6.4e-12 eV), and far below the ionosphere cutoff, so it cannot propagate as a vacuum photon in those media. For z < 10 the mean-IGM omega_p (1.7e-14 to 6e-13 eV) is comparable to or below that photon energy, but the real IGM is not uniformly ionised, so this is a mean estimate. The ISM n_e = 0.03 cm^-3 is a representative round number chosen by this note, not a measured value; B&O cite the NE2025 Galactic electron-density model (Ocker & Cordes, arXiv:2602.11838) for absorption.
  SOURCE: computation: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py (standard cold-plasma formula omega_p^2 = e^2 n_e/(eps0 m_e)); B&O p. 3 footnote 4 for the claim about absorption
  QUOTE: "Note that if the frequencies are below kHz, they are immediately absorbed by the interstellar medium [38]."
  ACCESS: full-text (B&O footnote); calc for the numbers
  STATUS: analysis; preprint
  SETTING: analysis
  CONFIDENCE: medium-high (cold unmagnetised plasma; ionised fraction assumed 1)

- [RQ-17] CLAIM: B&O's eq. 16 as printed gives N_phi = 6e87 (10^-22 eV/m_DM)(4e-3/v)^3 (Omega_DM/0.26) x_MW occupation-quantum number with v the velocity dispersion; evaluating it (no extra factors) gives 6e87 at v = 4e-3 c and 3.8e89 at v = 1e-3 c, times x_MW ~ 1e5 in the Milky Way halo (3.8e94). Independent cross-check (this note): for m = 1e-22 eV and a local density of 0.4 GeV/cm^3 (n = 4.0e36 m^-3), the de Broglie wavelength at v = 1e-3 c is 1.2e19 m = 0.40 kpc and the occupation per mode n lambda^3 ~ 7.6e93, consistent with the x_MW-boosted B&O number. B&O's default v = 4e-3 c (= 1200 km/s) is a factor ~4 above a typical Milky-Way halo dispersion (~1e-3 c to 2e-3 c); at v = 1e-3 c N_phi rises by 64. Note the average cosmological DM density is 0.26 rho_crit = 1.25e-6 GeV/cm^3 [calc]; x_MW ~ 1e5 corresponds to a local halo density of ~0.1-0.4 GeV/cm^3.
  SOURCE: B&O arXiv:2607.24930 eq. 16 p. 5 (printed form); computation: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py
  QUOTE: "at the cosmological mean DM energy density Nϕ≃6×10 87 10−22 eV mDM 410−3 v 3 ΩDM 0.26xMW,(16) where v represents the velocity dispersion, ΩDM its average relative energy density and xMW is the boost one gets in a DM halo; for the Milky Way halo xMW∼10 5 [47]."
  ACCESS: full-text (B&O); calc
  STATUS: preprint; analysis
  SETTING: analysis
  CONFIDENCE: medium (garbled extraction of eq. 16; assumed layout above; the literature value of the Milky Way velocity dispersion is stated from general knowledge, not from a source I opened)

- [RQ-18] CLAIM: Forecast for the next CMB spectral-distortion measurement (PIXIE, a proposed mission, not funded flight hardware; STATUS: forecast): the baseline PIXIE mission (two years, 45% of observations on spectral distortions, after foreground marginalisation with 10% priors and 50% delensing) forecasts 68% CL uncertainties of 1.6e-8 on y, 2.2e-7 on mu (fiducial values y = 1.77e-6, mu = 2e-8); the extended mission 8.3e-9 on y and 1.3e-7 on mu. A longer distortion-dedicated mission "would lower the current 95% confidence upper limit on the chemical potential to |mu| < 10^-7", "a factor of 1000 improvement over the COBE/FIRAS limits". So any B&O mu bound could tighten by at most ~1e3 (from 9e-5) if such a mission flew.
  SOURCE: Kogut et al. 2025, "The Primordial Inflation Explorer (PIXIE): mission design and science goals", JCAP 04 (2025) 020, arXiv:2405.20403 (PDF read)
  QUOTE: "Conversely, a longer mission dedicated primarily to spectral distortions would lower the current 95% confidence upper limit on the chemical potential to |µ|< 10−7. The resulting factor of 1000 improvement over the COBE/FIRAS limits" ; Table 3 row: "Electron Pressure y 1.77× 10−6 1.6× 10−8 8.3× 10−9 ... Primordial Silk Damping µ 2× 10−8 2.2× 10−7 1.3× 10−7"
  ACCESS: full-text
  STATUS: peer-reviewed (mission-design forecast)
  SETTING: analysis
  CONFIDENCE: high for the quoted forecasts; no mission is approved (not checked here; engineering facet owns it)

- [RQ-19] CLAIM: Fermi-LAT isotropic gamma-ray background (the "gamma-ray background" bound in B&O Fig. 3): spectrum 100 MeV to 820 GeV described by a power law with exponential cutoff, index 2.32 +/- 0.02, break energy (279 +/- 52) GeV, and total IGRB intensity (7.2 +/- 0.6) x 10^-6 cm^-2 s^-1 sr^-1 above 100 MeV (baseline Galactic-foreground model; foreground-model systematic uncertainties are tabulated separately in Table 3 of the paper, e.g. +0.1/-0.9 x 10^-6 in the 0.10-0.14 GeV bin). The same table gives the 0.10-0.14 GeV IGRB intensity (2.8 +/- 0.6) x 10^-6 cm^-2 s^-1 sr^-1.
  SOURCE: Ackermann et al. (Fermi-LAT) 2015, "The spectrum of isotropic diffuse gamma-ray emission between 100 MeV and 820 GeV", ApJ 799, 86, arXiv:1410.3696 (PDF read)
  QUOTE: "The total intensity attributed to the IGRB is (7 .2± 0.6)× 10−6 cm−2 s−1 sr−1 above" [the text continues "100 MeV" in the published abstract; extraction breaks the sentence at an affiliation block] ; Table 3: "0.10 – 0.14 (2 .8± 0.6)× 10−6 +0.1 −0.9× 10−6"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high for the intensity; the "above 100 MeV" is from the abstract context (sentence cut by extraction)

- [RQ-20] CLAIM: Local dark-matter density input: the conversion 0.008 M_sun pc^-3 = 0.3 GeV cm^-3; the review compiles local-density measurements from Kapteyn (0.285 GeV cm^-3) to Jeans (1.935 GeV cm^-3), a wide historical spread. B&O's boost x_MW ~ 1e5 relative to the cosmic mean (1.25e-6 GeV/cm^3 for 0.26 rho_crit, this note's calc) corresponds to a local density ~0.1 GeV/cm^3, within the range of modern values (precise modern value in Read 2014 not extracted here; see Gaps).
  SOURCE: Read 2014, "The Local Dark Matter Density", J. Phys. G 41, 063101, arXiv:1404.1938 (PDF read)
  QUOTE: "a useful conversion is: 0 .008 M⊙ pc−3 = 0.3 GeV cm−3."
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high for the conversion; low for any modern density value (not extracted)

## Gaps
- Not found: EBL/CIB intensity data with uncertainties (optical-IR EBL) and the UV/X-ray background values B&O bound against; I opened only the Fermi IGRB (RQ-19) and radio (RQ-15) backgrounds.
- Not found: a primary-source quote for current BBN photodisintegration limits (Poulin & Serpico 2015, arXiv:1503.04852 and Kawasaki et al.), beyond the thresholds and the delta_D < 0.03 criterion B&O adopt (RQ-04). The threshold energies are standard nuclear data; B&O quote them, I did not independently check them against a nuclear data table.
- Not found: the modern Milky-Way dark-matter velocity dispersion and local density as quoted values (RQ-17/RQ-20 rely on a conversion only and on general knowledge for ~1e-3 c); the Hui, Ostriker, Tremaine, Witten 2017 paper (arXiv:1610.08297) was not opened.
- Not found: LISA galactic white-dwarf binary numbers (period, chirp mass, N of resolved sources) for B&O's Fig. 2a inspiral inputs; B&O's Fig. 2a axes are M and nu, not a specific source list, so this did not block anything here.
- Not found: any LVK isotropic stochastic limit newer than O3 (arXiv:2101.12130); the O4 result was not searched for. The arXiv API rate-limited several lit_search calls.
- Not checked: whether B&O has a v1/v2 difference in the numbers quoted here; the fetcher returned one 13-page PDF without a version tag. Equation extractions (8, 10, 16, S7) are partly garbled; numbers above use the layout that is dimensionally consistent, and the 1e-110 emissivity and 6/(25 pi) photon coefficient were reproduced from the printed text.
- Not computed: the full cosmological integration of eq. 19/S12 and the B&O Fig. 3 constraint curves (owner: constraints). My calc sizes only the inputs (RQ-11 to RQ-13).
- No PAPER TO REQUEST: all papers cited were open on arXiv.
