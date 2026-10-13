# Research: frontier
status: final
Mandate: B&O itself (versions, SM S1-S12), 2025-2026 literature citing it, related recent work on graviton coherent states, GW-induced particle production, dark-matter production by GWs. Newest first.
Access: lit_search INSPIRE ok, arXiv rate-limited (HTTP 429); fetch_text.py on arxiv.org abs/pdf pages worked (v1 and v2); WebFetch/WebSearch not used

## Claims
- [RF-01] CLAIM: B&O (Blas & Oller, arXiv:2607.24930, hep-ph; no journal reference on INSPIRE as of 2026-10-13) has two versions: v1 submitted 27 Jul 2026, v2 revised 31 Jul 2026. v2 is the current one; its arXiv comment says results are unchanged but the semiclassical interpretation, title and abstract were changed. INSPIRE lists 0 citations to it (checked 2026-10-13).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930 abs page (v2), https://arxiv.org/abs/2607.24930 ; INSPIRE https://inspirehep.net/literature/3183912
  QUOTE: "[Submitted on 27 Jul 2026 ( v1 ), last revised 31 Jul 2026 (this version, v2)] ... Comments: 6 pages; 3 figures; v2: semiclassical interpretation clarified; title and abstract changed accordingly; results unchanged"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-02] CLAIM: The v1 title/abstract claimed the effect is a purely quantum process "forbidden classically and semiclassically"; v2 reverses the interpretation: the effect "admits a semiclassical description once the metric is solved to second order". The numbers (eq. 8 etc.) are stated unchanged. This is a significant retreat on Hidden premise 10 (N^2 enhancement = quantum vs classical nonlinearity).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v1 and v2 (PDF), https://arxiv.org/pdf/2607.24930v1 , https://arxiv.org/pdf/2607.24930v2
  QUOTE: v1: "Classical gravitational waves (GWs) are stable in vacuum. We show that treated as coherent graviton states, they decay into photon pairs, a quantum process forbidden classically and semi- classically and enhanced by the graviton number squaredN 2." ; v1 body: "Restoring SI units (ω s =ℏω,σ ω =ℏδ ω) makes explicit thatW γ vanishes forℏ→0: the effect is of quantum na- ture, and neither classically nor semiclassically do GWs...radiate photons in vacuum." ; v2: "We perform the calculation describing both gravity and the photons as quantized fields, though we show that the effect admits a semiclassical description once the metric is solved to second order." ; v2 body: "Being linear inℏ means that the quantumness of this number comes from the energy of photons, confirming the semiclassical origin for the gravitational field."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-03] CLAIM: In v2, B&O say their calculation "is equivalent to that of considering the creation of photons in a background h_c, once considered at second order (including ... the induced metric sourced by the energy-momentum tensor of the GWs)". They also acknowledge that "no particle production occurs for an individual plane-wave GW [21-26]" and claim to go beyond that limit with a QFT treatment. They use the Feynman propagator in diagram 2 of Fig. 1 and note the difference from the retarded one (G_F = G_ret - 2*pi*i*theta(-k0)delta(k^2)), asserting the extra term "vanishes when convoluted with the external coherent states".
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2, p.1-2, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "the calculation we will perform is equivalent to that of considering the creation of photons in a back- groundh c, once considered at second order (including in particular the induced metric sourced by the energy- momentum tensor of the GWs, cf. Fig. 1). To the best of our knowledge, this also supersedes previous semiclas- sical calculations." ; "Regarding semiclas- sical calculations, no particle production occurs for an individual plane-wave GW [21–26]"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-04] CLAIM: B&O eq. (8) (v2, p.3): dP/dt = 3 G^2 N^2 w_s^3 sigma_w^2 /(25 pi) (natural units); eq. (9): N_gamma(t) ~ G^2 N0^2 6 w_s^3 sigma_w^2 t/(25 pi); eq. (10) tau = 25 pi/(6 G^2 E_rel^2 w_s sigma_w^2). They state eq. (8) "is a probability per unit time for tau << dt ~ 1/sigma_w, with Poissonian uncertainty sqrt(sigma_w tau)". Photon power W_gamma = 6 G^2 E_rel^2 w_s^2 sigma_w^2/(25 pi) (eq. 11), re-expressed as W_gamma = (3/(50 pi)) (r_m/l)^2 (hbar w)^2 (eq. 12) with r_m = 2 G E_rel/c^4 and wavefront width l = c dt.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2, p.3, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "= 3G2N2ω3 sσ2 ω 25π .(8) Each reaction removes two gravitons and generates two photons. ... Nγ(t)≈G 2N2 0 6ω3 sσ2 ωt 25π .(9) ... τ= 25π 6G2E2 relωsσ2ω ,(10) ... Equation (8) is a probability per unit time for τ≪δt∼1/σ ω, with Poissonian uncertainty√σωτ."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-05] CLAIM: The 2 pi delta(0) -> T step (SM eq. S6 text, v2 and v1 identical): the remaining energy-conserving delta is "treated as 2 pi delta(0) -> T, the interaction time", justified "for narrower bands since T ~ 1/sigma_w, provided 1/sigma_w >> tau". Thus the "rate" is the total probability divided by the packet duration ~1/sigma_w, not a rate of a sustained process; this is the hinge flagged by Hidden premise 3. (The text of this step is identical in v1 and v2.)
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2 SM, p.10, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "With σω/ωs≪1, the remaining energy-conserving delta function is treated as 2πδ(0)→T, the interaction time, so that P/Tis the transition probability per unit time. This approximation improves for narrower bands sinceT∼1/σ ω, provided 1/σω≫τ, the reaction time, c.f. Eq. (10)."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-06] CLAIM: B&O (v2) apply eq. (8) to a chirp by cutting it into fractional-bandwidth bins epsilon (epsilon = 0.1 for the equal-mass Fig. 2 inspiral), with t_eps = (5 eps/12)(2 (G Mc)^5 w_s^8)^(-1/3) [as extracted], E_rel = t_eps L_GW, requiring tau << min(1/(eps w_s), t_eps). They state binning "yields a lower bound on the emissivity, as any residual coherence between bins is neglected" (Hidden premise 6). Fig. 2 is a contour of photon-number luminosity L_gamma = W_gamma/w_s in the (total mass M, frequency nu) plane; the merger panel b) gives L_gamma ~ 1e6 s^-1 "along the nominal frequency" and photon energies above keV only in the leftmost corner of the allowed region. Footnote 4: flux estimated "by interpreting this luminosity as the number of photons produced per unit time at the sphere of radius tau"; frequencies below kHz "are immediately absorbed by the interstellar medium".
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2, p.3-4, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "Dividing the GW into fractional bandwidth binsϵyields a lower bound on the emissivity, as any residual coher- ence between bins is neglected." ; "Along the nominal frequencyL γ is larger than in panel a), though still modest,∼10 6 s−1." ; "The flux can be estimated by interpreting this luminosity as the number of photons produced per unit time at the sphere of ra- diusτ."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-07] CLAIM: B&O (v2) state the binary photon power is comparable to the Hawking luminosity of a black hole of the binary's total mass: W_H/W_gamma = (5/(4608 pi^2)) (lambda l/(r_s r_m))^2 ~ 1e-4 (lambda l/(r_s r_m))^2 (eq. 13), "~1e2-1e3" for GW150914, and the decay "happens in an extended region". Their conclusion: photon luminosities of compact binaries "are very weak"; the stated route to observability is only "a new (challenging) handle".
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2, p.4 and p.6, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "For GW150914 one findsW H/Wγ∼102– 103, scaling with the binary masses in the merger phase like M0. A key difference between both sorts of radiation is that the one from the decay of the wavefront happens in an extended region." ; "even if compact binaries provide a realistic astrophysical setting for this phenomenon, the resulting photon luminosities are very weak, e.g., com- parable to the Hawking luminosity of a black hole with the total mass that of the binary."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-08] CLAIM: B&O (v2) say that for the eq. (11)-(12) power, "all the hbar disappear, and our calculation corresponds to a classical process" (in the SM/eq. 12 context) while the main text also states hbar-linear quantumness resides only in the photon energy; and the Discussion says the effect "vanishes in the classical limit, but can be recovered semiclassically (a calculation that was missing in the literature)". The v2 text thus carries both statements (classical-limit vanishing and a classical/semiclassical origin).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2, p.3 and p.6, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "can see that all theℏdisappear, and our calculation cor- responds to a classical process." ; "This effect vanishes in the classi- cal limit, but can be recovered semiclassi- cally (a calculation that was missing in the literature)."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium (the first quote begins mid-sentence in the PDF extraction; its antecedent is not identified)
- [RF-09] CLAIM: B&O constraints (v2): they inject photons only after z ~ 3e6 (before that "they simply thermalize"), use CMB mu (1e5 <~ z <~ z_a ~ 3e6) and y distortions, UV/X-ray and gamma-ray backgrounds, and D and 4He photofission (thresholds Q = 2.23 MeV for D -> pn, ~20 MeV for 4He; requiring delta_D < 0.03), plotted in Fig. 3 as upper bounds on sqrt(Gamma eps E_rel / M_sun) [Gpc^-3/2 yr^-1/2] vs w_s. They use the photon energy as vacuum photons ("the energy of photons in the laboratory frame ... considered in the average sense"); no plasma-frequency correction is mentioned in the passages found.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2, p.5-6 and SM SF p.13, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "We consider injection of photons happening af- terz∼3×10 6, as before they simply thermalize. In the µ-regime, 105 ≲z≲z a≈3×10 6, the injected photons generate a chemical potentialµ" ; "Integrating Eq. (S25) to first order inδ D and requiringδ D <0.03 yields the bound shown by the green line in Fig. 3"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-10] CLAIM: B&O ULDM channel (v2): for w_s >> m_DM decay is into states basically unoccupied with dP/dt = 7 G^2 N0^2 w_s^3 sigma_w^2/(450 pi) and tau_phi = (54/7) tau; in the high-occupation regime m_DM <= w_s <~ m_DM(1+v^2/2), dP/dt ~ G^2 m_DM^5 N0^2 v^6 N_phi/128 (eq. 17) with sigma_w ~ m_DM v^2/2; they model ULDM "as a stochastic background".
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2, p.5, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "forω s≫m DM the decay happens into states basically unoccupied anddP/dt= 7G 2N2 0ω3 sσ2 ω/450π. The result- ing reaction time isτ ϕ = (54/7)τ[τfrom Eq. (10)]. In the regime where the decay happens into states of high occupation number,m DM≤ω s ≲m DM(1 +v 2/2),N ϕ can enhance the rate enormously, dP dt ≃ G2m5 DMN2 0v6 128 Nϕ,(17)"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-11] CLAIM: B&O eq. (14) for an incoherent stochastic background: dP/(dt dV) = 8 pi G^2 rho_GW^2/15, number emissivity 2 dP/dt dV ~ 1e-110 m^-3 s^-1 for N_eff-allowed rho_GW; the difference from eq. (8) is the replacement V w_s sigma_w^2 -> 40 pi^2/9, "for a coherent state the effective volume is reduced to 5 lambda_s^3/(9 pi eps^2), roughly a wavelength volume".
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2, p.4, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "yield the decay rate per volume dP dtdV = 8πG2 15 ρ2 GW,(14) withρ GW the GW energy density. The number emissiv- ity is absolutely negligible, 2dP/dtdV≈10 −110 m−3s−1, assuming theN eff bounds on the energy density of GWs [7, 42]."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-12] CLAIM: Closest prior work on the same amplitude: Sawyer (2020, PRL 124, 101301) argued that g g -> gamma gamma has O(G^2) cross sections "too small to be of any interest" but that in dense clouds of pure gravitons collective effects "can lead to copious production of photons". B&O cite it as [16] (infrared-enhanced collective effects in graviton systems) but present their own result as a coherent-state calculation. Sawyer's arXiv comment notes the helicity amplitudes were redefined with no effect on later equations (relevant to the eq. 6 phase question).
  SOURCE: R. F. Sawyer 2020, "Quantum break in high intensity gravitational wave interactions", Phys. Rev. Lett. 124, 101301, arXiv:1910.08835, https://arxiv.org/abs/1910.08835
  QUOTE: "The lowest order amplitudes for [graviton+graviton -> photon +photon] lead to cross-sections of order G^2, where G is the gravitational constant. These are too small to be of any interest. However in dense clouds of pure gravitons there are collective effects utilizing these same amplitudes that under the right circumstances can lead to copious production of photons."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-13] CLAIM: Redi & Tesi (June 2026) give a general result for particle production by a metric perturbation: yield is controlled by the stress-tensor two-point function on the time-like support (q^2 > 0), whereas GW emission needs the light-like support; they state that "null-like tensor and vector perturbations do not produce particles". This is a linear-response (quadratic in h) statement for conformal fields, consistent with the plane-wave no-go and with the need in B&O for a second-order (h^4, N^2 G^2) process; it also says production requires time dependence "on a time-like support".
  SOURCE: M. Redi, A. Tesi 2026, "Particle Production from Inhomogeneities: the off-shell side of gravitational waves", arXiv:2606.28297 (preprint, 3 citations on INSPIRE as of 2026-10-13), https://arxiv.org/pdf/2606.28297
  QUOTE: "Notice that null-like tensor and vector perturbations do not produce particles." ; "GWs are produced provided that the source has a non-zero anisotropic stress with time dependence on a null-like support. Particle production instead requires less: only time dependence of the source on a time-like support."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high (for the statement; applicability to B&O's O(h^4) process is an inference, not claimed by Redi-Tesi)
- [RF-14] CLAIM: Khusnutdinov (2026, Eur. Phys. J. Plus 141, 532; arXiv:2508.11558) finds no massless-particle production (scalar and vector fields) in an exact plane-gravitational-wave spacetime, from closed-form Green's functions matching the DeWitt-Schwinger expansion; he also discusses "contrasting interpretations" based on Bogolyubov coefficients that predict massless particle creation. B&O cite it as [25] among the no-go results. This is the newest peer-reviewed plane-wave no-go.
  SOURCE: N. Khusnutdinov 2026, "Quest for particles production in the plane gravitational wave spacetime", Eur. Phys. J. Plus 141, 532, arXiv:2508.11558, https://arxiv.org/abs/2508.11558
  QUOTE: "The results coincide exactly with the DeWitt--Schwinger expansion, indicating no massless particles production in this background. Contrasting interpretations, based on Bogolyubov coefficient calculations predicting massless particle creation, are also addressed."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-15] CLAIM: Chakraborty et al. (2024, PRD 110, L021701) show scalar quanta are produced perturbatively in a linear GW background for arbitrary (non-plane-wave) profiles, applicable to compact-binary signals; so some particle production by GWs exists at first order in h for a localized/non-plane profile, in contrast to the plane-wave no-go. This is a different (linear-in-h, test-field, no-N^2) process than B&O's graviton fusion, and its size for photons or for real binaries was not extracted here.
  SOURCE: T. Chakraborty et al. 2024, "Particle creation in a linear gravitational wave background", Phys. Rev. D 110, L021701, arXiv:2404.01840, https://arxiv.org/abs/2404.01840
  QUOTE: "we show that scalar particles may indeed be produced in a perturbative manner. Our formulation is valid for any linear gravitational wave background profile, and is by no means restricted to monochromatic plane waves, in contrast to much of the earlier work on this topic. Thus, our work is directly applicable to gravitational wave signals from compact binary coalescen..."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium (abstract truncated; scalar field, not photons)
- [RF-16] CLAIM: Ai, Ellis & Pradler (Oct 2025) revisit processes in a gravitational-wave background with all-orders soft-graviton resummation and conclude that inclusive decay rates of matter in a GW background remain essentially (unchanged); the abstract is truncated in the extract. It is the nearest recent work on infrared safety of coherent-GW-background processes (cited by B&O as [15]) and bears on whether N-enhanced real emission/absorption terms cancel in inclusive rates. Not yet read in full; treat as a lead.
  SOURCE: W.-Y. Ai, S. A. R. Ellis, J. Pradler 2025, "Soft Gravitons, Hard Truths: Infrared Safety of Particle Processes in a Gravitational-Wave Background", arXiv:2510.27690, https://arxiv.org/abs/2510.27690
  QUOTE: "By extending the soft-graviton framework describing real and virtual processes in a gravitational wave background, and resumming them to all orders, we show that inclusive decay rates remain essential" [abstract truncated by the extraction at "essential..."]
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: low (truncated abstract; conclusion not verified)
- [RF-17] CLAIM: B&O's acknowledgements thank P. A. Cano for discussions, J. Garriga "for comments on the semiclassical calculations" and N. Rodd "for very valuable comments on a previous version of this work", so some informal review took place; the v1 to v2 change within four days (27 to 31 Jul 2026) was a reinterpretation of the same result (semiclassical origin) rather than a recalculation.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2, p.6, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "We would like to thank P. A. Cano for interesting dis- cussions and J. Garriga for comments on the semiclassi- cal calculations. We would also like to thank N. Rodd for very valuable comments on a previous version of this work."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

## Gaps
- No paper cites B&O: INSPIRE "refersto:arxiv:2607.24930" returned 0 results and the INSPIRE record shows 0 citations (checked 2026-10-13). No comment, rebuttal, erratum or published version found; none in the 2026 INSPIRE searches ("Skobelev graviton photon scattering", "Blas Oller graviton"). Rebuttal search belongs to the critiques facet; re-check INSPIRE before the report.
- arXiv API/search was rate-limited (HTTP 429/timeouts) during lit_search; INSPIRE and fetch_text on arxiv.org pages worked. WebSearch was not used (no hits needed beyond INSPIRE).
- Not read in full: Redi-Tesi 2606.28297 (26 pp.), Ai-Ellis-Pradler 2510.27690, Sawyer 1910.08835, Chakraborty 2404.01840, Garani et al. 2502.12249 (abstract only; massless-limit universal particle production by metric inhomogeneities, JHEP 08 037). No search hits found for conference talks or proposals on GW -> photon decay.
- Not extracted from B&O: the explicit statement in v1 vs v2 of eq. 6 phases and the SM S1-S12 derivations (owned by theory/idealizer); the claim numbers for Fig. 2 beyond ~1e6 photons/s for the merger panel; the eqs. 16-19 coefficients beyond those quoted.

