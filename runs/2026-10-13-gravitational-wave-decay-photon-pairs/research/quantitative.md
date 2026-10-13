# Research: quantitative
status: final
Mandate: numbers and inputs: merger parameters, rho_GW bounds, CMB mu/y, EBL, BBN photodisintegration, ULDM, plasma frequencies.
Access: lit_search INSPIRE ok (arXiv source timed out repeatedly); fetch_text on arxiv.org PDFs/abs worked; WebSearch worked; WebFetch not used

## Claims
- [RQ-01] CLAIM: B&O's own inputs (v2, 31 Jul 2026, p. 3): for the merger phase they scale from GW150914 as nu ~ 150 Hz x (65 Msun/M), E_rel ~ 2 Msun c^2 x (M/65 Msun), t_m ~ 5 ms x (M/65 Msun); for the inspiral they use equal-mass binaries (M = 2^(6/5) M_c) with fractional bandwidth epsilon = 0.1, and they require tau << min(1/(eps omega_s), t_eps). Their E_rel = 2 Msun c^2 is below the LVK central value 3.0 Msun c^2 (see RQ-02), their only stated source for the number being refs [39,40].
  SOURCE: Blas & Oller, arXiv:2607.24930v2 [hep-ph], 31 Jul 2026, p. 3, https://arxiv.org/pdf/2607.24930
  QUOTE: "For the merger phase, at fixed mass ratio and spins, the characteristic frequency ωs, the released energy, and the duration tm of the phase, of around one period, scale as [39, 40]: ν≈150 Hz×(65M ⊙/M), E rel ≈ 2M⊙c2×(M/65M⊙) and tm≈5 ms×(M/65M ⊙), where we anchor the total mass to GW150914"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RQ-02] CLAIM: GW150914 measured values (LVK, 90% credible intervals, source frame): total energy radiated in GWs 3.0 (+0.5 -0.5) Msun c^2; peak GW luminosity 3.6 (+0.5 -0.4) x 10^56 erg/s (= 3.6e49 W SI) equivalent to 200 (+30 -20) Msun c^2/s; luminosity distance 410 (+160 -180) Mpc, z = 0.09 (+0.03 -0.04); source-frame initial masses 36 (+5 -4) and 29 (+4 -4) Msun, final 62 (+4 -4) Msun; signal sweeps 35 to 250 Hz, peak strain 1.0e-21. (Original 2016 values; the GWTC-1 re-analysis shifted them slightly, not yet re-checked here.)
  SOURCE: Abbott et al. (LVK), 2016, Observation of Gravitational Waves from a Binary Black Hole Merger, Phys. Rev. Lett. 116, 061102, arXiv:1602.03837
  QUOTE: "The estimated total energy radiated in gravitational waves is 3.0þ0.5 −0.5 M⊙c2. The system reached a peak gravitational-wave luminosity of 3.6þ0.5 −0.4 × 1056 erg=s, equivalent to 200þ30 −20 M⊙c2=s." and "The signal sweeps upwards in frequency from 35 to 250 Hz with a peak gravitational-wave strain of 1.0 × 10−21."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RQ-03] CLAIM: Cosmological inputs (Planck 2018, base LCDM, TT,TE,EE+lowE+lensing): H0 = 67.4 +- 0.5 km/s/Mpc, Omega_m = 0.315 +- 0.007, Omega_c h^2 = 0.1200 +- 0.0012 (68%); with BAO, N_eff = 2.99 +- 0.17 (abstract), i.e. 2.99 +0.34 -0.33 at 95% (TT,TE,EE+lowE+lensing+BAO), against the SM value 3.046. Planck 2018 is the final Planck release; no later re-analysis is used here.
  SOURCE: Planck Collaboration, 2020, Planck 2018 results. VI. Cosmological parameters, A&A 641, A6, arXiv:1807.06209
  QUOTE: "Neﬀ = 2.99±0.17, in agreement with the Standard Model prediction Neﬀ = 3.046" and "Neﬀ = 2.99+0.34 −0.33 (95 %, TT,TE,EE+lowE+lensing +BAO)." and "Ωch2 = 0.1200± 0.0012 (68 %, Planck TT,TE,EE +lowE+lensing)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RQ-04] CLAIM: The BBN/CMB bound on total GW energy density (integrated over all frequencies, valid for GWs present at nucleosynthesis, i.e. of cosmological origin and f above the horizon scale) is, in Maggiore's review, integral d(log f) h0^2 Omega_gw(f) <= 5.6e-6 (N_nu - 3), with h0^2 Omega_gamma = 2.481e-5. With a permitted Delta N_eff of 0.3 (my reading of the Planck+BAO 95% interval) this gives h^2 Omega_GW,tot = 1.7e-6 (derived here, not quoted); converting with rho_crit gives rho_GW c^2 = 2.8e-15 J/m^3 = 1.8e4 eV/m^3 (printed by the RQ-11 script). This bound does NOT apply to a background made by astrophysical mergers after BBN, which is the relevant one for B&O's SGWB depletion; for that class the direct limit is LVK (RQ-05).
  SOURCE: Maggiore, 2000, Gravitational wave experiments and early universe cosmology, Phys. Rept. 331, 283, arXiv:gr-qc/9909001, p. 44
  QUOTE: "∫ f =∞ f =0 d(logf ) h2 0Ω gw(f ) ≤ 5.6 × 10−6(Nν − 3). (118)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RQ-05] CLAIM: Direct GW background limits. LVK O1-O4a isotropic search (95% credible): for a CBC-like Omega_GW ~ f^(2/3) spectrum Omega_GW(25 Hz) <= 2.0e-9; for a scale-invariant spectrum Omega_GW(25 Hz) <= 2.8e-9. NANOGrav 15 yr (nHz band, Hellings-Downs evidence): strain amplitude 2.4 (+0.7 -0.6) x 10^-15 (median, 90% credible interval) at f = 1/yr for a fiducial f^(-2/3) characteristic strain spectrum.
  SOURCE: LVK 2025, Upper Limits on the Isotropic GWB from the first part of the fourth observing run, arXiv:2508.20721 (PRD 114, 042001 per INSPIRE); Agazie et al. (NANOGrav) 2023, ApJL 951, L8, arXiv:2306.16213
  QUOTE: "we constrain the fractional energy density to $\Omega_{\rm GW}(25{\rm Hz})\leq 2.0\times 10^{-9}$ (95% cred.), a factor of 1.7 improvement over previous results. Scale-invariant backgrounds are constrained to $\Omega_{\rm GW}(25{\rm Hz})\leq 2.8\times 10^{-9}$" and "the strain amplitude is $2.4^{+0.7}_{-0.6} \times 10^{-15}$ (median + 90% credible interval) at a reference frequency of 1/(1 yr)."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RQ-06] CLAIM: COBE/FIRAS spectral-distortion limits (the ones B&O use): |y| < 15e-6 and |mu| < 9e-5 at 95% CL; FIRAS CMB temperature 2.728 +- 0.004 K (95% CL). B&O quote |y| < 1.5e-5, which is the same number. These have not been improved by any later spectrometer to date (PIXIE/other forecasts: see engineering facet).
  SOURCE: Fixsen et al. 1996, The Cosmic Microwave Background Spectrum from the Full COBE FIRAS Data Set, ApJ 473, 576, arXiv:astro-ph/9605054
  QUOTE: "For t he Comptonization and chemical potential we ﬁnd |y| <15 × 10−6 and |µ| <9 × 10−5 (95% CL). There are also reﬁnements in the absolute temperature, 2.728 ± 0.004 K (95% CL)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RQ-07] CLAIM: B&O's stated constraint inputs (v2, pp. 5-6): FIRAS |mu| < 9e-5 and |y| < 1.5e-5; mu-regime 1e5 <~ z <~ z_a ~ 3e6 and y-regime 1e3 <~ z <~ 1e5; photons injected before z ~ 3e6 'simply thermalize'; UV/X-ray background from a synthesis model (their ref. [55]); Fermi-LAT IGRB 100 MeV to 820 GeV (ref. [56]); D and 4He photofission from cascade analyses (refs. [57,58]); the plotted quantity is sqrt(Gamma eps E_rel/Msun) in Gpc^(-3/2) yr^(-1/2). For the SGWB they quote an emissivity 2 dP/dt dV ~ 1e-110 m^-3 s^-1 and |Phi| ~ 1e-25 Hz^-1 up to z ~ 1e28 at the largest rho_GW allowed by Delta N_eff.
  SOURCE: Blas & Oller, arXiv:2607.24930v2, pp. 3-6
  QUOTE: "The number emissiv- ity is absolutely negligible, 2dP/dtdV≈10 −110 m−3s−1, assuming theN eff bounds on the energy density of GWs [7, 42]." and "From the COBE/FIRAS mea- surement [60] one finds|µ|<9×10 −5,which implies the bound shown by the black line in Fig. 3." and "which COBE/FIRAS constrained to|y|< 1.5×10 −5 [60]"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RQ-08] CLAIM: Taking B&O eqs. 8-12 at face value (SI, ħ-free form tau = 25 pi c^2/(6 L^2 omega_s sigma_omega^2), L = G E_rel/c^4) with B&O's own GW150914 inputs (E_rel = 2 Msun c^2 = 3.57e47 J, nu = 150 Hz, sigma = 1/t_m = 200 s^-1): tau = 3.6e3 s in vacuum, i.e. 7e5 times longer than t_m = 5 ms; N0 = E/(hbar omega) = 3.6e78 gravitons; W_gamma = 2.8e-35 W (eq. 11 and eq. 12 agree); photons emitted during one t_m = t_m/tau ~ 1.4e-6 in vacuum. With the LVK central E_rad = 3.0 Msun c^2: tau = 1.6e3 s, W_gamma = 6.3e-35 W. The depletion time tau_h = tau N0 = 1.3e82 s (4e74 yr). Fraction of GW energy converted over t_m is ~1e-76 even with CMB stimulation. So B&O's own tau << t_m condition fails at the nominal GW150914 point; the nominal point is outside their 'allowed' region (consistent with their Fig. 2b).
  SOURCE: this run's calculation, [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py]; formulas from B&O eqs. 8-12; inputs RQ-01, RQ-02
  QUOTE: "tau (vacuum) = 3.578e+03 s  (>> t_m = 5 ms: B&O's tau<<t_m condition is violated at nominal point)" / "W_gamma (eq.11) = 2.778e-35 W ; via eq.12 = 2.778e-35 W (should agree)" / "depletion time tau_h = tau*E/(hbar omega) (vacuum) = 1.287e+82 s = 4.077e+74 yr"  (script log output)
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: medium
- [RQ-09] CLAIM: CMB stimulation factor (1 + 2 f_gamma) for the GW150914 150 Hz point: hbar omega = 6.2e-13 eV against kT_CMB = 2.35e-4 eV (T0 = 2.7255 K), so f_gamma = 3.8e8 and 1+2f = 7.6e8; with it tau = 4.7e-6 s, L_gamma = 1/tau = 2.1e5 photons/s (3.6e5 to 4.8e5 for E = 3 Msun c^2), the same order as B&O Fig. 2b's '~1e6 s^-1'. Without stimulation W_H(65 Msun)/W_gamma = 340 to 770, matching B&O eq. 13 ('1e2-1e3'); eq. 13 therefore refers to the unstimulated power. The stimulated W_gamma is 2e-26 W (E = 2 Msun c^2) to 5e-26 W, against a GW peak luminosity of 3.6e49 W. Whether f_gamma applies at all is the question for hidden premise 8: the 'average sense' factor assumes an isotropic bath at the photon's own frequency, while the pair emerges back to back with each photon at ~omega_s in the wave frame.
  SOURCE: this run's calculation, [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py]
  QUOTE: "f_gamma(150 Hz) = 3.786e+08; stimulation factor 1+2f = 7.572e+08" / "tau with CMB stim = 4.725e-06 s ; L_gamma = 1/tau = 2.116e+05 photons/s (B&O Fig 2b: ~1e6 s^-1)" / "Hawking W_H(65 Msun) = 2.132e-32 W ; W_H/W_gamma(vacuum) = 7.676e+02 (B&O eq.13: 1e2-1e3)"  (script log output)
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: medium
- [RQ-10] CLAIM: Plasma frequency omega_p = hbar sqrt(n_e e^2/(eps0 m_e)); nu_p = 8.98 kHz sqrt(n_e/cm^-3). Mean fully ionised IGM today, n_e = 2.2e-7 cm^-3 (Planck Omega_b h^2 = 0.0224, Y_p = 0.245): nu_p = 4.2 Hz, omega_p = 1.7e-14 eV. Mean IGM is NOT where most space sits: an older estimate says uniform fully ionised baryons give n_e = 1.8e-7 cm^-3 and that the real average is lower by at least a factor of 15 at z <~ 1. Fully ionised plasma at z = 1e5: n_e = 2.2e8 cm^-3, omega_p = 5.5e-7 eV; at z = 3e6: 9e-5 eV. Warm ISM (0.03 cm^-3): nu_p = 1.6 kHz (6.4e-12 eV); solar wind at 1 AU (5 cm^-3): 20 kHz; ionospheric F-layer (1e6 cm^-3): 9 MHz. A 150 Hz photon (6.2e-13 eV) is above the mean-IGM cutoff today by a factor ~35 but below the ISM cutoff by a factor ~10, so it cannot propagate in the Galactic ISM; B&O footnote 4 already says 'below kHz ... immediately absorbed by the interstellar medium'. In the early universe omega_p(z) grows as (1+z)^(3/2) while a redshifting photon grows as (1+z), so omega_s/omega_p = 36 (1+z)^(-1/2) for a 150 Hz photon (observed today) in a fully ionised mean medium, which falls below 1 at 1+z ~ 1300 (a number derived here from the two scalings). Fully ionised conditions hold only before recombination (z > ~1700), so such a photon would be evanescent in the pre-recombination plasma, while after recombination the neutral IGM has a much smaller n_e (re-ionised to ~z 6 only).
  SOURCE: this run's calculation [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py]; n_e estimate: Mirizzi, Raffelt, Serpico 2002, Effects of the Intergalactic Plasma on Supernova Dimming via Photon-Axion Oscillations, arXiv:hep-ph/0112212 (cited as the source of the factor-15 statement)
  QUOTE: "if all of the baryons in our Univer se had been uniformly distributed and fully ionized, the electron density would have been ∗ ne = 1. 8·10− 7cm− 3." and "This estimate is very likely too high, by at least a factor of 15, in the region z <∼ 1 which is the relevant regime for our" (hep-ph/0112212 p. 3); script: "IGM mean, fully ionised, z=0   n_e= 2.207e-07 cm^-3 : nu_p =   4.2184e+00 Hz ; omega_p =  1.745e-14 eV"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RQ-11] CLAIM: B&O eq. 14 at face value, natural units converted to SI with G = 1/M_Pl^2 (M_Pl = 1.22089e28 eV): dP/dtdV = 8 pi G^2 rho_GW^2/15 gives, for Omega_GW h^2 = 5.6e-6 x DeltaN_eff with DeltaN_eff = 0.3, 0.1, 0.05: pair rates 2.8e-109, 3.1e-110, 7.7e-111 m^-3 s^-1 (photon rates x2: 5.5e-109, 6.1e-110, 1.5e-110). B&O's '2 dP/dtdV ~ 1e-110 m^-3 s^-1' therefore corresponds to DeltaN_eff of about 0.05 to 0.1, tighter than the Planck+BAO 95% interval (N_eff 2.99 +0.34 -0.33) allows, i.e. it is a modest underestimate (factor up to ~50 in rate, since rate ~ rho^2) of the maximum for a primordial background; for the astrophysical-merger background the relevant bounds are LVK Omega_GW(25 Hz) <= 2.8e-9 (scale-invariant) or ~1e-9 (PTA band), which give photon rates 3e-115 and 2e-115 m^-3 s^-1. Either way, the rate is negligible by >100 orders of magnitude, which B&O themselves state.
  SOURCE: this run's calculation [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py]; B&O eq. 14 (arXiv:2607.24930v2 p. 3); bounds RQ-04, RQ-05
  QUOTE: "BBN/CMB integral bound 5.6e-6*DeltaN, DeltaN=0.3 (Planck+BAO 95% ~ N_eff<3.3) ... eq.14 pair rate = 2.758e-109 m^-3 s^-1 ; photon rate (x2) = 5.517e-109 m^-3 s^-1 (B&O: ~1e-110)" and "LVK O4a Omega(25Hz)<=2.8e-9 flat, h^2 included ... photon rate (x2) = 3.163e-115 m^-3 s^-1"  (script log output)
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: medium
- [RQ-12] CLAIM: ULDM inputs and B&O eqs. 16-18. (i) Eq. 16 is reproduced by N_phi = (2 pi)^3 n/((4 pi/3)(m v)^3) with n = Omega_DM rho_c/m: for m = 1e-22 eV, v = 1e-3 c, Omega_DM = 0.26 gives 5.7e87 (B&O: 6e87). (ii) Cosmic mean DM density 1.26e-6 GeV/cm^3 (Planck 2018 Omega_c h^2 = 0.120, Omega_DM = 0.264); local DM density 0.3-0.5 GeV/cm^3 (global studies) or 0.4-0.6 GeV/cm^3 (local analyses) is 2.4e5 to 4.7e5 times the cosmic mean, vs B&O x_MW ~ 1e5; v_rms ~ 220 km/s = 7.3e-4 c vs B&O v = 1e-3. (iii) A reconstruction of eq. 18, W_phi = (9 pi/256) G m^2 v^3 N0^2 H0^2 Omega_DM x_MW (formula garbled in the PDF extraction; this form follows from eqs. 16-17 and reproduces the stated magnitude), with N0 = E_rel/(hbar omega_s), omega_s = m, ISCO mass from omega_ISCO = 8800 pi (Msun/M) rad/s and an ASSUMED E_rel = 3/65 M c^2: for m = 1e-21 eV the binary has M = 1.8e10 Msun and W_phi = 8.6e13 W x (x_MW/1) = 8.6e18 W at x_MW = 1e5, i.e. B&O's '1e14 W' matches only with x_MW as a multiplicative boost left unevaluated. The relevant sources (1.8e10 Msun SMBH binaries at ISCO, GW period 2 pi/omega = 4.2e6 s for omega = 1.5e-6 rad/s) are in the nHz band, where the observed signal is the PTA background (RQ-05), not individually resolved sources; the E_rel and N0 here rest on my assumption E_rel = 3/65 M c^2.
  SOURCE: this run's calculation [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py]; de Salas & Widmark 2021, Dark matter local density determination, Rep. Prog. Phys. 84, 104901, arXiv:2012.11477; Planck 2018 (RQ-03); B&O eqs. 16-18 pp. 4-5
  QUOTE: "The result of most local analyses coincide within a range of ρDM,⊙≃ 0.4–0.6GeV/cm3 = 0.011–0.016M⊙/pc3, while a slightly lower range of ρDM,⊙≃ 0.3–0.5GeV/cm3 = 0.008–0.013M⊙/pc3 is preferred by most global studies." (arXiv:2012.11477 abstract); script: "N_phi(m=1e-22 eV, v=1e-3, Omega=0.26 version) = 5.663e+87" and "m=1e-21 eV: binary mass at ISCO 1.820e+10 Msun ; N0 = 9.368e+95 (E_rel=3/65 M c^2) ; W_phi (x_MW=1e5) = 8.643e+18 W"
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: low
- [RQ-13] CLAIM: BBN photodisintegration thresholds (Cyburt, Ellis, Fields, Olive 2003): d(gamma,n)p 2.2246 MeV; 3He(gamma,p)d 5.4935 MeV; 4He(gamma,p)t 19.8139 MeV; 4He(gamma,n)3He 20.5776 MeV. B&O's photofission bounds (their Fig. 3) need cascade photons above ~2.2 MeV (D) or ~20 MeV (4He) hitting nuclei after BBN, i.e. injected photon energies >~ 1e6 eV, which for a GW of frequency nu (photon energy h nu) requires nu >~ 5e20 Hz for D (2.2 MeV / h) and >~ 5e21 Hz for 4He (20 MeV / h) (my conversion, 1 eV = 2.418e14 Hz); this is far above any binary frequency (kHz), so cascade bounds in B&O's Fig. 3 concern hypothetical high-frequency sources only. Also the cascade is non-universal below the pair-production threshold E_gamma <~ 10/T_keV MeV (Poulin & Serpico).
  SOURCE: Cyburt, Ellis, Fields, Olive, arXiv:astro-ph/0211258 (Table 1; title and journal reference not verified in this run); Poulin & Serpico, arXiv:1503.04852 (preprint)
  QUOTE: "Reaction Threshold (E γ, th) d(γ,n)p 2.2246 MeV t(γ,n)d 6.2572 MeV t(γ,np)n 8.4818 MeV 3He(γ,p)d 5.4935 MeV 3He(γ,np)p 7.7181 MeV 4He(γ,p)t 19.8139 MeV 4He(γ,n)3He 20.5776 MeV" ; "the universality of the nonthermal photon spectrum ... Eγ <∼ 10T−1 keV MeV" (1503.04852 p. 1)
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RQ-14] CLAIM: The Fermi-LAT isotropic gamma-ray background (IGRB) that B&O compare against covers 100 MeV to 820 GeV (50 months of data); the IGRB is what remains after subtracting resolved extragalactic sources, and so includes a residual Galactic foreground.
  SOURCE: Ackermann et al. (Fermi-LAT) 2015, Limits on dark matter annihilation signals from the Fermi LAT 4-year measurement of the isotropic gamma-ray background, JCAP 09 (2015) 008, arXiv:1501.05464 (describing the IGRB measurement of Ackermann et al. ApJ 799, 86)
  QUOTE: "The Fermi LAT collaboration has recently published a new measurement of the IGRB [8] based on 50 months of data and extending the analysis described in [5] down to 100 MeV and up to 820 GeV."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RQ-15] CLAIM: Long-lived inspiral reference: GW170817 chirp mass 1.188 (+0.004 -0.002) Msun, total mass 2.74 (+0.04 -0.01) Msun (low-spin prior), luminosity distance 40 (+8 -14) Mpc, E_rad > 0.025 Msun c^2. Pushed through B&O's recipe (eps = 0.1, E_rel = t_eps L_GW, sigma = 1/t_eps, quadrupole chirp): at f_GW = 100 Hz, t_eps = 0.60 s, L_GW = 1.8e44 W, tau(vacuum) = 8.8e14 s, tau(CMB-stimulated, 1+2f = 1.1e9) = 7.7e5 s, L_gamma = 1.3e-6 photons/s, W_gamma = 8.6e-38 W; at 30 Hz tau(stim) = 2.4e9 s. For a GW150914-like inspiral (Mc = 28 Msun) at 50 Hz: tau(stim) = 5.6e-2 s, L_gamma = 18 photons/s, W_gamma = 6e-31 W. For an assumed galactic WD binary (Mc = 0.3 Msun, 6.2 mHz; ASSUMED parameters) tau = 1.5e51 s. In every case tau >> 1/(eps omega) except possibly the BBH inspiral, so B&O's validity condition tau << min(1/(eps omega_s), t_eps) fails at astrophysical frequencies except in a narrow high-mass corner. Power ratio W_gamma/L_GW is 1e-79 to 1e-102.
  SOURCE: LVK 2017, GW170817: Observation of Gravitational Waves from a Binary Neutron Star Inspiral, PRL 119, 161101, arXiv:1710.05832; calculation [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py]
  QUOTE: "Chirp mass M 1.188þ0.004 −0.002 M⊙ ... Total mass mtot 2.74þ0.04 −0.01 M⊙ ... Radiated energy Erad > 0.025M⊙c2 ... Luminosity distance DL 40þ8 −14 Mpc" ; script: "-- GW150914-like BBH inspiral (Mc~28 Msun) at 50 Hz ... tau(vacuum) = 1.266e+08 s ; ... tau(stim) = 5.575e-02 s ; L_gamma(stim) = 1.794e+01 photons/s"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RQ-16] CLAIM: Check of B&O's ISCO number: f_GW,ISCO = c^3/(6^(3/2) pi G M) = 4397 Hz (Msun/M), i.e. 67.6 Hz for 65 Msun; B&O's omega_s ~ 8800 pi (Msun/M) rad/s = 2 pi x 4400 Hz is therefore the GW (not orbital) angular frequency at ISCO, consistent. The 150 Hz nominal merger/ringdown frequency of GW150914 is 2.2x f_GW,ISCO of 65 Msun. Peak GW energy flux at Earth from 3.6e49 W at 410 Mpc is 1.8e-2 W/m^2 (an order-of-magnitude cross-check from h = 1e-21 at 150 Hz gives 3.6e-3 W/m^2).
  SOURCE: this run's calculation [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/quantitative_inputs.py]
  QUOTE: "f_GW,ISCO for 1 Msun = 4397.2 Hz (B&O: 8800 pi rad/s /2pi = 4400 Hz) ; for 65 Msun = 67.6 Hz" ; "peak GW energy flux at Earth, L/(4 pi d^2), d=410 Mpc: 1.790e-02 W/m^2"  (script log output)
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: medium

## Gaps
- Not searched or not opened this run: CMB spectral-distortion mission sensitivities (PIXIE etc.) and ARCADE-2/radio background numbers (engineering facet owns them); GWTC-1/GWTC-4 re-analysed GW150914 values (the 2016 numbers above are cited; later catalog values may differ slightly); Haardt-Madau/UV-X-ray background intensity J_nu used by B&O (their ref. [55]); BBN photofission abundance limits themselves (B&O refs. [57,58]).
- B&O supplemental sections SA-SF were not opened (frontier/theory own them); eq. 18 and eq. 20 were garbled in the PDF extraction, so RQ-12's reconstruction of eq. 18 is an assumption.
- PDF-extraction tool gave "N eff" no matches in Planck; the N_eff quote is from the abstract and Sec. 7 of 1807.06209.
- The factor DeltaN_eff used by B&O for the 1e-110 figure is not stated in the main text; RQ-11's inference (0.05 to 0.1) is mine.
