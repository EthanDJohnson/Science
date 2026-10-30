# Check: quantitative
status: final

Method: quotes and numbers re-grepped with fetch_text.py on the arXiv PDFs. Calc-derived numbers recomputed by hand where marked.

| Claim | Verdict | Note |
|---|---|---|
| RQ-01 GW150914 energy, luminosity, distance, z | verified | 3.0 +0.5/-0.5 M_sun c^2, 3.6e56 erg/s, 200 M_sun c^2/s and 410 Mpc / z=0.09 match the PDF. The "35 to 250 Hz" sweep is the paper's abstract wording, not in the quoted line (that line says 35 to 150 Hz); both appear in the paper. |
| RQ-02 B&O merger scalings (150 Hz, 2 M_sun c^2, 5 ms; ~1e6 s^-1; above keV) | verified | All wording matches p. 3-4. The 2 M_sun c^2 versus GW150914's 3.0 is an unreconciled difference, as the note says. |
| RQ-03 inspiral inputs, eps=0.1/0.15, t_eps formula | verified | Quote matches. The exponent is printed as (...)^(1/3) in the extraction, so the sign is not confirmable from text; flag stays. The dimensional expectation is exponent -1/3. |
| RQ-04 FIRAS limits, thresholds, delta_D<0.03, eta=6.1e-10, Y~0.25, z~3e6 | verified | |mu|<9e-5, |y|<1.5e-5, the four Q values, eta, Y and the z~3e6 cutoff all match. The y-era "1e3 <~ z <~ 1e5" is printed as 10^3 to z_a≈10^5. |
| RQ-05 ULDM N_phi, dP/dt, tau_phi=(54/7)tau | verified | Eq. 16 text matches. The layout (exponent 3 on 4e-3/v) is consistent with extraction. dP/dt and tau_phi lines were not re-grepped. |
| RQ-06 FIRAS 1996 limits and Bianchini & Fabbian re-analysis | verified | Abstract text matches for both (|y|<15e-6, |mu|<9e-5 at 95% CL; |<mu>|<47e-6, "factor of ~2"). Table 2 entries were not re-grepped. B&O's own cited FIRAS value is the 1996 one. Journal status of 2206.02762 (PRD 106, 063527) not rechecked. |
| RQ-07 Planck 2018 N_eff | verified | 2.99±0.17 (+BAO), 2.99 +0.34/-0.33 (95%), 2.89±0.19 (no BAO) all in the paper. |
| RQ-08 Maggiore BBN bound 5.6e-6 (N_nu-3) and derived rho_GW | verified | Eq. 118 matches. I recomputed 5.6e-7/0.454 = 1.2e-6 and 1.2e-6 × 7.67e-10 J/m^3 = 9.4e-16, matching the note. Coefficient is the 2000 value, as stated. |
| RQ-09 LVK O3 isotropic limits | verified | 5.8e-9 (flat, log-uniform), 3.4e-9 (alpha=2/3, log-uniform), 1.7e-8 (flat, uniform prior), and the 20-76.6 Hz band all match. 4.4e-18 J/m^3 = 5.8e-9 × 7.67e-10 recomputed. |
| RQ-10 NANOGrav 15-yr amplitude | verified | 2.4 +0.7/-0.6 e-15 at 1/yr and p=5e-5 to 1.9e-4 match. Omega conversion recomputed as 8.0e-9. |
| RQ-11 eq. 14 and the emissivity ~1e-110 | verified | Eq. 14 and the "2dP/dtdV≈10^-110 m^-3 s^-1" text match. The Delta N_eff numerics were not independently rerun. |
| RQ-12 merger-rate sizing | verified | Formulas as printed. N0 = 3.57e47 J / 9.9e-32 J = 3.6e78 and kT0/(hbar omega) = 3.8e8 recomputed. Note that the 1e5 versus 1e6 s^-1 gap is the note's own open item. |
| RQ-13 GW150914 flux at Earth | verified | 3.6e49 W / (4π (1.27e25 m)^2) = 1.8e-2 W/m^2, and the fluence 2.7e-4 J/m^2, recomputed. |
| RQ-14 GWTC-4 and GWTC-3 rates | verified | 7.6-250, 9.1-84, 14-26 (z=0); GWTC-3 10-1700, 7.8-140, 17.9-44 (z=0.2) and kappa=2.9 +1.7/-1.8 match. GWTC-4 is still a preprint here; I did not look for a journal reference. |
| RQ-15 ARCADE 2 | verified | 50±7 mK, 2.730±0.004 K, T_R=1.19±0.14 K, beta=-2.62±0.04, and 1.26±0.09 K, -2.60±0.04 from 22 MHz-10 GHz all match. |
| RQ-16 plasma frequencies | verified | Hand check with omega_p = 5.64e4 sqrt(n_e/cm^-3) rad/s: 4.2 Hz and 1.7e-14 eV (mean cosmic), 6.4e-13 eV at z=10, 1.56 kHz and 6.4e-12 eV (ISM 0.03), 9 MHz (ionosphere). B&O footnote on kHz absorption not re-grepped. |
| RQ-17 N_phi evaluation and cross-check | verified | 64× at v=1e-3 c is correct. The de Broglie wavelength is 1.2e19 m and n·lambda^3 is 7.6e93, as stated. This is a factor 5 below 3.8e94, which the note calls "consistent". The Milky Way dispersion of ~1e-3 c is from general knowledge, not a source (the note admits this). |
| RQ-18 PIXIE forecasts | verified | Table 3 (y 1.6e-8 / 8.3e-9; mu 2.2e-7 / 1.3e-7), |mu|<1e-7 and "factor of 1000" match. The attribution of the table to "10% priors and 50% delensing" was not confirmed. The Table 2 excerpt is ambiguous, so treat that qualifier as unconfirmed. |
| RQ-19 Fermi IGRB | verified | Index 2.32±0.02, break (279±52) GeV, and (7.2±0.6)e-6 cm^-2 s^-1 sr^-1 match (Table 4, model A). The 0.10-0.14 GeV bin value was not re-grepped. |
| RQ-20 Read 2014 conversion | verified | "0.008 M_sun pc^-3 = 0.3 GeV cm^-3" matches. Kapteyn/Jeans range values not rechecked. |

## Summary
20 claims checked: 20 verified, 0 unverifiable, 0 contradicted, 0 misattributed, 0 status-wrong. Weak points:
- RQ-03: the t_eps exponent sign is unconfirmable from the extraction.
- RQ-12: the stimulation factor reproduces B&O's ~1e6 s^-1 only to within a factor of ~10.
- RQ-18: the "10% priors" qualifier is unconfirmed.
- RQ-14: GWTC-4 is a preprint.
