# Research: frontier
status: final
Mandate: B&O itself (both versions, SM S1-S12), the 2025-2026 literature citing or cited by it, graviton coherent states, GW-induced particle production, DM production by GWs; newest first.
Access: lit_search INSPIRE ok (its arXiv endpoint timed out on every call); WebFetch not needed; fetch_text.py worked on arxiv.org/pdf and arxiv.org/abs. Date of search: 2026-10-30.

Headline for this facet: as of 2026-10-30 INSPIRE lists 0 citations of B&O and I found no comment, reply or erratum (see Gaps). The only indirect "frontier" evidence bearing on whether the effect exists is (i) B&O's own v1 -> v2 retreat from "quantum, vanishes semiclassically" to "classical, second-order metric", and (ii) three 2025-2026 papers (Redi-Tesi, Franchino-Vinas et al., Khusnutdinov) that locate particle production at time-like support / near the source and find none for null plane GWs. Page numbers are PDF pages of the version named.

## Claims

### A. B&O itself (arXiv:2607.24930; hep-ph; v1 27 Jul 2026, v2 31 Jul 2026; preprint, no journal ref in INSPIRE; 0 citations)

- [RF-01] CLAIM: B&O exists in two versions four days apart, and v2 reverses the paper's interpretation. v1 (title "Gravitational waves decay in vacuum: a low energy effect of quantized gravitation.") says the decay is "a quantum process forbidden classically and semi-classically" and that W_gamma "vanishes for hbar -> 0"; v2 (title without subtitle) says the effect "admits a semiclassical description once the metric is solved to second order", and that the hbar-dependence drops out when a photon background is present, so "our calculation corresponds to a classical process". The headline eq. 8, dP/dt = 3 G^2 N^2 omega_s^3 sigma_omega^2 / (25 pi) (natural units), and eqs. 9-12 are the same in both versions as extracted. Cite v2 for equations; v1 and v2 disagree on whether the effect is quantum.
  SOURCE: Blas & Oller 2026, "Gravitational waves decay in vacuum", arXiv:2607.24930v1 and v2, https://arxiv.org/pdf/2607.24930v1 and https://arxiv.org/pdf/2607.24930v2
  QUOTE: v1 abstract: "Classical gravitational waves (GWs) are stable in vacuum. We show that treated as coherent graviton states, they decay into photon pairs, a quantum process forbidden classically and semi- classically and enhanced by the graviton number squaredN 2." v1 p.2: "Restoring SI units (ω s =ℏω, σ ω =ℏδ ω) makes explicit thatW γ vanishes forℏ→0: the effect is of quantum na- ture, and neither classically nor semiclassically do GWs radiate photons in vacuum." v2 abstract: "We perform the calculation describing both gravity and the photons as quantized fields, though we show that the effect admits a semiclassical description once the metric is solved to second order." v2 p.3: "can see that all theℏdisappear, and our calculation cor- responds to a classical process."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-02] CLAIM: B&O's state and how it is used (eqs. 1-5, v2 p.1-2). The state is |f> = S|0> = D(f)|0>, with S the S-matrix of a classical source T_s^{mu nu} coupled linearly to the graviton field, time-ordered from t_i -> -infinity to t_f -> +infinity; <f|h|f> is "the classical radiated field by the source" with the Pauli-Jordan function (eq. 5), and "far from the source ... tends asymptotically to the outgoing spherical wave packet" proportional to cos(omega_s(r-t))/r times a Gaussian in (r-t). B&O then use |f> as the initial state of the fusion g g -> gamma gamma ("coherent states as initial states"). For the calculation the profile is replaced by a narrow-band top-hat f_s = Theta on k in [omega_s - sigma_omega/2, omega_s + sigma_omega/2] with Theta fixed by the mean graviton number N. The pair rate depends on the momentum-space profile only; no source position or distance enters eq. 8. This is the object behind hidden premise 1 (an out-state S|0> used as an in-state).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2 p.1-2, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "From Eq. (1), the final state after the source is active is |f⟩= ˆS|0⟩" ... "As a result, the evolution of the GW has to be studied with these coherent states as initial states, which, as we will see, implies their decay into light particles, photons in particular." ... "far from the source, the classical field of Eq. (5) tends asymptotically to the outgoing spherical wave packet"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-03] CLAIM: B&O's amplitude input and the "unpolarized" step (eqs. 6-7, v2 p.2). The helicity amplitudes are taken from Skobelev (1975) as A++++ = A---- proportional to 8 pi G t^2/s... and A++-- = A-++ proportional to 8 pi G u^2/s (only the extracted line is available; the exact fraction layout is garbled in the PDF text and should be re-read in the TeX/HTML), labelled by (graviton helicities; photon helicities) in brackets. Eq. 7 then states that "assuming an unpolarized graviton state" the fusion amplitude is proportional to (s^2 - 2tu)/s times delta_{mu1 mu2}, i.e. B&O combine the two helicity structures into one scalar weight before squaring. The text does not discuss phases or whether a single real convention exists for the helicity amplitudes (hidden premise 2). The s-channel graviton diagram (Fig. 1, diagram 2) is dropped on the argument that the coherent mode in the propagator would be on shell with s = 0 (SM SA); SM SA says "the intermediate graviton is forced on shell" and "the incoming gravitons [must be] collinear", where helicity conservation fails and the amplitude vanishes.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2 p.2 and SM SA p.9-10
  QUOTE: "It hence follows from Eq. (6) that the fusion amplitude, as- suming an unpolarized graviton state, can be expressed as" and (SM SA) "Moreover,K 0 =|K|requires the two incoming momenta to be collinear, implying helicity conservation, which cannot be satisfied because±2±2̸=±2. The amplitude also vanishes ats= 0, due to the derivative nature of gravitational couplings [cf. Eq. (6)]."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium (equation layout garbled by PDF extraction)

- [RF-04] CLAIM: The 2 pi delta(0) -> T step (SM SB, v2 p.10; identical in v1 p.10). The squared amplitude (eq. S6) carries an overall energy-conserving 2 pi delta(k1^0 + k2^0 - k1'^0 - k2'^0); B&O set it to the "interaction time" T and read P/T as the rate, with T ~ 1/sigma_omega. Main text (v2 p.3): eq. 8 "is a probability per unit time for tau << delta t ~ 1/sigma_omega, with Poissonian uncertainty sqrt(sigma_omega tau)" (as printed, "τ≪δt∼1/σ ω"). So the rate is the packet's total pair probability divided by its own duration; no propagation-time variable enters, which is the hinge for hidden premise 3.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2 SM SB p.10, https://arxiv.org/pdf/2607.24930v2
  QUOTE: "With σω/ωs≪1, the remaining energy-conserving delta function is treated as 2πδ(0)→T, the interaction time, so that P/Tis the transition probability per unit time. This approximation improves for narrower bands sinceT∼1/σ ω, provided 1/σω≫τ, the reaction time, c.f. Eq. (10)."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-05] CLAIM: B&O's definitions of reaction time and power (v2 p.3, eqs. 9-12): N_gamma(t) ~ G^2 N0^2 6 omega_s^3 sigma_omega^2 t/(25 pi); tau = 25 pi/(6 G^2 E_rel^2 omega_s sigma_omega^2) with E_rel = N0 omega_s "the total energy in the wave front of width sigma_omega"; W_gamma = 6 G^2 E_rel^2 omega_s^2 sigma_omega^2/(25 pi) (natural units), which they write in SI as 6 G^2 hbar E_rel^2 omega_s^2 delta_omega^2/(25 pi c^10) and as (3/(50 pi)) (r_m/l)^2 hbar omega^2 with r_m = 2 G E_rel/c^4 and l = c delta t. They tie the depletion time of the GW, tau_h = tau E_rel/omega_s, to the strain through "E_rel sigma_omega/(4 pi r^2) ~ omega_s^2 h_r^2/(32 pi G)", i.e. a spherical shell at radius r; eq. 8 itself has no r.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2 p.3
  QUOTE: "withE rel =N 0ωs the total energy in the wave front of width σ ω." / "For the burst-like configuration, the strain h r at distance rsatisfies" / "depleting at time τ h =τE rel/ωs (cf. Eq. (10))."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium (equation layout garbled; relations checked numerically in [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/frontier_sanity.py], see RF-06)

- [RF-06] CLAIM: Consistency check of B&O's own merger number, run on their stated inputs only (nu = 150 Hz, E_rel = 2 Msun c^2, t_m = 5 ms, M = 65 Msun, SI): eq. 11 and eq. 12 give the same W_gamma = 2.78e-35 W (r_m = 5.9e3 m, l = c t_m = 1.5e6 m, r_m/l = 3.9e-3, hbar omega = 6.2e-13 eV = 9.9e-32 J). That is L_gamma = W/(hbar omega) = 2.8e-4 photons/s, i.e. about 1.4e-6 photons over the 5 ms burst without the CMB factor. The CMB occupation at 150 Hz is f_gamma = 3.8e8 (T0 = 2.7255 K), so (1+2f) = 7.6e8 and L_gamma = 2.1e5 photons/s, the same order as B&O's quoted "~10^6 s^-1" (B&O's ~1e6 is a text value for the Fig. 2b point; my 2.1e5 is a reproduction from eq. 12 and the (1+2f) factor, not their plotted number). Therefore essentially the whole of B&O's quoted merger luminosity is the stimulated-emission factor (1+2f_gamma) ~ 7.6e8 on a vacuum yield of ~1e-6 photons per event. B&O's own (1+2f) is introduced "in the average sense" (v2 footnote 3) and photons of 150 Hz (6e-13 eV) lie far below the cosmic plasma frequency, a point for the engineering/constraints facets.
  SOURCE: B&O arXiv:2607.24930v2 eqs. 10-12, p.3-4 (inputs); script [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/frontier_sanity.py]
  QUOTE: "Along the nominal frequency L γ is larger than in panel a), though still modest,∼10 6 s−1." (B&O v2 p.4)
  ACCESS: full-text
  STATUS: preprint (inputs and quote); the arithmetic is mine and is analysis
  SETTING: analysis
  CONFIDENCE: medium (rests on reading "ℏω 2" in eq. 12 as hbar omega^2; eq. 11 independently gives the same number)

- [RF-07] CLAIM: B&O's own conclusions on binaries (v2 p.3-4, 6): the photon luminosities are "modest"; the discussion says they are "comparable to the Hawking luminosity of a black hole with the total mass that of the binary", and eq. 13 gives W_H/W_gamma ~ 1e2-1e3 for GW150914 (so W_gamma is 1e-3 to 1e-2 of the Hawking power). Footnote 4: "if the frequencies are below kHz, they are immediately absorbed by the interstellar medium"; the flux is estimated "by interpreting this luminosity as the number of photons produced per unit time at the sphere of radius tau". B&O say the photons that could propagate to detectors are only in "the leftmost corner of the allowed region in Fig. 2b), frequencies ... above keV". B&O make no claim that any individual binary photon signal is detectable.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2 p.3-4, 6
  QUOTE: "if the frequencies are below kHz, they are immediately absorbed by the interstellar medium [38]." / "the resulting photon luminosities are very weak, e.g., com- parable to the Hawking luminosity of a black hole with the total mass that of the binary."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-08] CLAIM: B&O's stochastic-background result (v2 p.4, SM SC): dP/(dt dV) = 8 pi G^2 rho_GW^2/15 (eq. 14, natural units), with number emissivity "2dP/dtdV ~ 1e-110 m^-3 s^-1" at the Planck-2018 N_eff bound, and depletion "negligible for all range of frequencies" (|Phi| ~ 1e-25 Hz^-1 up to z ~ 1e28 with rho_GW at its N_eff maximum). They say the single coherent-state rate (eq. 8) differs from the stochastic one by replacing "V omega_s sigma_omega^2 -> 40 pi^2/9", i.e. the coherent state's gain is that its effective volume is "roughly a wavelength volume": the enhancement is a statement about energy packed into ~lambda^3, not about propagation.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2 p.4
  QUOTE: "The number emissiv- ity is absolutely negligible, 2dP/dtdV≈10 −110 m−3s−1, assuming the N eff bounds on the energy density of GWs [7, 42]." / "for a coherent state the effective volume is reduced to 5λ 3 s/(9πϵ2), roughly a wavelength volume for the values ofϵwe consider, dra- matically enhancing the effective density relative to the incoherent case."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-09] CLAIM: B&O's ULDM channel (v2 p.4-5, SM SD): for omega_s >> m_DM, dP/dt = 7 G^2 N0^2 omega_s^3 sigma_omega^2/(450 pi) and tau_phi = (54/7) tau; in the resonant window m_DM <= omega_s <~ m_DM(1+v^2/2) with occupation N_phi, dP/dt ~ G^2 m_DM^5 N0^2 v^6 N_phi/128 (eq. 17, sigma_omega ~ m_DM v^2/2); occupation N_phi ~ 6e87 (1e-22 eV/m)^4 (1e-3/v)^3 (Omega_DM/0.26) x_MW (eq. 16, x_MW ~ 1e5 for the Milky Way halo); and W_phi ~ 1e14 x_MW (1e-21 eV/m_DM)^2 (v/1e-3)^3 W, "~1e54 s^-1 for m = 1e-21 eV" (eq. 18). The binary version uses m_DM ~ omega_s ~ ISCO frequency. B&O themselves write that "the rates to generate particles out of gravitational waves seem too small to have a clear significant effect" in the standard scenario and that this "may change" with ULDM occupation numbers; the SM SD rate formula (S11) is the source of the resonant coefficient.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2 p.4-5, SM SD p.11
  QUOTE: "After completing the calculation (cf. SM SD), forω s≫mDM the decay happens into states basically unoccupied anddP/dt= 7G 2N2 0ω3 sσ2 ω/450π. The result- ing reaction time isτ ϕ = (54/7)τ" / "Hence, Wϕ∼10 14 xMW 10−21 eV mDM 2 v 10−3 3 W,(18) corresponding to rates of emission of ∼10 54 s−1 for m= 10−21 eV."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium (prefactor layouts garbled)

- [RF-10] CLAIM: B&O's constraints (v2 p.5-6, Fig. 3, SM SE-SF) are upper bounds on sqrt(Gamma) eps E_rel/Msun in Gpc^(-3/2) yr^(-1/2) for "unspecified sources" with E_rel and omega_s as independent parameters, comoving density n~ and recurrence rate kappa, Gamma = n~ kappa; they use the UV/X-ray background model of Faucher-Giguere (2020), the Fermi-LAT isotropic gamma-ray background (100 MeV-820 GeV), COBE/FIRAS |mu| < 9e-5 and |y| < 1.5e-5, and D and 4He photofission (D threshold 2.23 MeV, 4He ~20 MeV; requires delta_D < 0.03 for the D bound). Each source is assumed to radiate W_gamma for its whole propagation time (SM SE: E_j(z) = W_gamma (1+z) times an integral over redshift of the source's emission). The paper says "Far from aiming at a complete study" and identifies no existing source population that saturates any bound.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930v2 p.5-6, SM SE-SF p.11-13
  QUOTE: "Far from aiming at a com- plete study, we now discuss a few possibilities to constrain√ ΓϵE rel/M⊙ as a function of the frequency of the GWs." / "From the COBE/FIRAS mea- surement [60] one finds|µ|<9×10 −5,which implies the bound shown by the black line in Fig. 3." / "Integrating Eq. (S25) to first order inδ D and requiringδ D <0.03 yields the bound shown by the green line in Fig. 3, labeled D photofission."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

### B. Related work, 2025-2026, newest first

- [RF-11] CLAIM: Ai, Ellis & Pradler (hep-ph; v1 31 Oct 2025, v2 28 Sep 2026 "corrected and improved interpretation of unchanged main result"), cited by B&O ref. [15]: Bose-enhanced graviton emission and absorption in a GW background look like they enhance decay rates of unstable particles at leading order, but resumming soft gravitons to all orders shows "inclusive decay rates remain essentially unchanged", with "Bose-enhanced emission and absorption in graviton spectra persist but compensate each other to all orders". Bearing on B&O: a second recent paper in which a leading-order Bose-enhanced effect from a coherent GW background is argued to cancel at inclusive level; it concerns matter decays, not g g -> gamma gamma, so it is an analogy and not a refutation.
  SOURCE: Ai, Ellis, Pradler, "Soft Gravitons, Hard Truths: Infrared Safety of Particle Processes in a Gravitational-Wave Background", arXiv:2510.27690v2, https://arxiv.org/abs/2510.27690
  QUOTE: "By extending the soft-graviton framework describing real and virtual processes in a gravitational wave background, and resumming them to all orders, we show that inclusive decay rates remain essentially unchanged. Bose-enhanced emission and absorption in graviton spectra persist but compensate each other to all orders; the mutual transparency between matter and gravitational radiation hence follows from infrared safety."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: high (for the abstract); relevance medium

- [RF-12] CLAIM: Fang et al. (gr-qc, 17 Aug 2026) and Miyauchi et al. (hep-ph, v1 9 Aug 2026, v2 26 Aug 2026): both argue that a detector or observer couples only to a particular wave-packet mode, so quantum features of the global source state (squeezing) are suppressed locally. Fang et al.: "macroscopically squeezed states appear classically thermal to a single detector" because of "a severe kinematic conflict in same-cone measurements". Miyauchi et al.: "a realistic detector couples only to a particular wave-packet mode" and "squeezing in global source modes need not remain observable". Bearing on B&O: these concern detection of quantum statistics, not photon production, but they are the 2026 literature on how a source's global graviton state (the kind of object eq. 3 is) relates to what a local observer or process sees; they do not test B&O's rate. STATUS: preprints, not reviewed.
  SOURCE: Fang, Guo, Lyu, Shu, Sun, Zhou, "Astrophysical Graviton Squeezing Can Be Hidden in the Far-Field", arXiv:2608.17015, https://arxiv.org/abs/2608.17015 ; Miyauchi, Omiya, Ota, Takeda, Tanaka, "The Challenge of Detecting Quantum Nature of Gravitational Waves", arXiv:2608.08803v2, https://arxiv.org/abs/2608.08803
  QUOTE: Fang et al. abstract: "Consequently, these macroscopically squeezed states appear classically thermal to a single detector." Miyauchi et al. abstract: "Because a realistic detector couples only to a particular wave-packet mode, squeezing in global source modes need not remain observable."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: high (abstracts); relevance low-medium

- [RF-13] CLAIM: Franchino-Vinas, Varacalli & Zanusso (arXiv:2608.25540, Aug 2026, heat-kernel, preprint; cites Redi-Tesi) compute the O(curvature^2) pair-creation probability of spin 0, 1/2 and 1 fields in a weak gravitational background and apply it to a point-mass binary. The probability has a threshold step function Theta(-4m^2 - p^2), i.e. support only at time-like momentum p (p0 = 2n omega for harmonic n of the orbital frequency, with |p| < p0); for massless fields n_min = 1 and "the n = 0 term does not contribute". For the white-dwarf binary HM Cancri (M = 0.5 Msun each, orbital angular speed 0.0195 Hz) they quote "a pair-creation rate of order 10^-28 s^-1" for a massless scalar (with the form-factor coefficient stripped), scaling as omega^(13/3) and M^(10/3); the created pairs are localised in the orbital plane, whereas GW power is maximal along the rotation axis. This is a published-in-preprint, source-attached, near-zone (non-radiative) pair creation calculation, the type of quantity the brief calls "near-source production"; it is independent of B&O and gives a far smaller number for a galactic binary than any naive N^2 scaling. It is for scalar test fields with a stripped O(1) form factor, in a point-mass nonrelativistic binary, not photons and not the radiation-zone field.
  SOURCE: Franchino-Vinas, Varacalli, Zanusso, "Pair creation in weak gravity and gauge backgrounds: spinning fields and binary stars", arXiv:2608.25540, https://arxiv.org/pdf/2608.25540 p.11-13
  QUOTE: "For HM Cancri, the numerical computation yields a pair-creation rate of order 10−28 s−1, which is far beyond the reach of current observational capabilities" / "Second, let us note that, in general, then= 0 term does not contribute, even for massless fields." / "On the other hand, the created pairs tend to be localized in the plane of the binary, whereas for gravitational waves the power is maximal along the system's axis of rotation [55]."
  ACCESS: full-text
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium (scalar test field, stripped form factor, preprint)

- [RF-14] CLAIM: Bao, Cheong, Rodd, Takach, Wang & Zhou (hep-ph, 29 Jul 2026; Rodd is thanked in B&O's acknowledgements for "comments on a previous version"): "all nonclassical effects are suppressed by extra powers of the weak coupling" and realistic detectors "couple to coarse-grained 'effective' modes, which often washes out nonclassical effects"; the abstract adds that their conclusions "rule out proposals to establish the quantization of gravity from observations of gravitational waves". This was posted two days after B&O v1 and is general, independent of mode occupancy; it does not mention B&O. It bears on the v1 claim that the decay is an effect "only possible by the quantum nature of the gravitational field", since v2 withdraws that statement; whether the N^2 g g -> gamma gamma yield counts as a "nonclassical effect" in their sense is not addressed.
  SOURCE: Bao et al., "Suppressed Quantum Effects of Weakly Coupled Waves", arXiv:2607.27313, https://arxiv.org/abs/2607.27313
  QUOTE: "Second, all nonclassical effects are suppressed by extra powers of the weak coupling, making them much harder to detect than the waves themselves."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: high (abstract); relevance medium

- [RF-15] CLAIM: Redi & Tesi (hep-ph, 26 Jun 2026, preprint; cited by B&O v2 as ref. [28] for "other limits where the process exists") show that on sub-horizon scales particle production by a classical, inhomogeneous metric perturbation is controlled by the unequal-time two-point function of the sourcing stress tensor evaluated at time-like momentum, q^mu q_mu > 0 (production of pairs), whereas GW emission is controlled by the same object at light-like momentum q^mu q_mu = 0; and they state that null (on-shell) tensor perturbations do not produce particles. They write the Weyl-squared contraction as W^2 = ... + (1/2)(q0^2 - q^2)^2 h_ij^2 for the tensor sector, which vanishes on the light cone. This is a cleaner statement of the "what a wave packet evades" question: a freely propagating on-shell GW (q^2 = 0) makes no pairs; production tracks the time-like (off-shell, near-source or in-matter) part of the source's field.
  SOURCE: Redi & Tesi, "Particle Production from Inhomogeneities: the off-shell side of gravitational waves", arXiv:2606.28297, https://arxiv.org/pdf/2606.28297 p.1, 3, 6
  QUOTE: "While GW production depends on the two-point function in the light-like region of momenta,qµqµ = 0, particle production is determined by the time-like region,q µqµ >0, corresponding for elementary particles to real production of particle pairs." and "Notice that null-like tensor and vector perturbations do not produce particles."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high (for the quoted statements); the paper is about classical backgrounds in the early Universe, scalar/vector/tensor test fields, not a direct test of B&O's coherent-state fusion

- [RF-16] CLAIM: Khusnutdinov (Eur. Phys. J. Plus 141, 532 (2026); arXiv:2508.11558v2): closed-form massless scalar and vector Green's functions in the plane-GW spacetime coincide with the DeWitt-Schwinger expansion, "indicating no massless particles production in this background"; the paper also addresses "contrasting interpretations, based on Bogolyubov coefficient calculations predicting massless particle creation". B&O cite it (ref. [25]) among the "no particle production occurs for an individual plane-wave GW" results. The result is for an exact plane wave, so it says nothing about packets with transverse structure.
  SOURCE: Khusnutdinov, "Quest for particles production in the plane gravitational wave spacetime", Eur. Phys. J. Plus 141, 532 (2026), arXiv:2508.11558, https://arxiv.org/abs/2508.11558
  QUOTE: "The results coincide exactly with the DeWitt–Schwinger expansion, indicating no massless particles production in this background. Contrasting interpretations, based on Bogolyubov coefficient calculations predicting massless particle creation, are also addressed."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high (abstract)

- [RF-17] CLAIM: Kanno, Soda & Taniguchi (Phys. Rev. Lett. 136, 061404 (2026); arXiv:2508.17947v2 16 Feb 2026), cited by B&O ref. [12]: for GW150914-like inspiral, "the coherent-state description reproduces classical gravitational waves at leading order, while next-order effects generate squeezed states of gravitons", with an estimated squeezing parameter ~1e-4 for GW150914. Bearing on B&O: it supports using a coherent state for a binary's GWs (eq. 3) but it describes the state as the source's radiated state, not an in-state for scattering, and 27 INSPIRE citations at time of search.
  SOURCE: Kanno, Soda, Taniguchi, "Coherent State Description of Gravitational Waves from Binary Black Holes", Phys. Rev. Lett. 136, 061404 (2026), https://arxiv.org/abs/2508.17947
  QUOTE: "We show that the coherent-state description reproduces classical gravitational waves at leading order, while next-order effects generate squeezed states of gravitons. For GW150914, we estimate the squeezing parameter to be $\sim 10^{-4}$. We find that gravitational waves from binary black holes are well described by a coherent state."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high (abstract)

### C. Direct predecessor and background just outside the five-year window

- [RF-18] CLAIM: Sawyer (Phys. Rev. Lett. 124, 101301 (2020); arXiv:1910.08835v3, Oct-Nov 2019) used the same lowest-order g g -> gamma gamma amplitudes with O(G^2) cross-sections and argued that "in dense clouds of pure gravitons there are collective effects utilizing these same amplitudes that under the right circumstances can lead to copious production of photons" (a "quantum break" on a time scale T_B in a multi-beam initial state in a periodic box). It states that coherent many-body graviton systems such as a LIGO wave "are essentially classical fields, at least in current descriptions". B&O cite it (ref. [16]) only as one of the "infrared-enhanced quantum collective effects in graviton systems". This is a different regime from B&O (exponential build-up in a multi-beam box versus a perturbative two-body fusion rate); I found no published test of either claim.
  SOURCE: Sawyer, "Quantum break in high intensity gravitational wave interactions", Phys. Rev. Lett. 124, 101301 (2020), arXiv:1910.08835, https://arxiv.org/pdf/1910.08835
  QUOTE: "The lowest order amplitudes for [graviton + graviton → photon + photon] lead to cross-sections of order G2, where G is the gravitational constant. These are too small to be of an y interest. However in dense clouds of pure gravitons there are collective effect s utilizing these same amplitudes that under the right circumstances can lead to copious productio n of photons."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-19] CLAIM: Cheong, Rodd & Wang (Phys. Rev. D 111, 015028 (2025); arXiv:2408.04696), the source of B&O's Glauber-Sudarshan P-representation treatment of the ULDM background (B&O refs. [49,50]): "for DM it is most likely that the density matrix takes the explicitly mixed form of a Gaussian over the basis of coherent states", and the classical-wave picture "emerges in the limit m << 10 eV". Bearing on hidden premise 9: this framework defines the coherence time and length of the DM field, which sets how long a resonance at omega_s ~ m_DM can build up; B&O's eq. 17 uses sigma_omega ~ m_DM v^2/2 as the DM bandwidth but does not compare the GW signal's duration to that coherence time in the text I read.
  SOURCE: Cheong, Rodd, Wang, "A Quantum Description of Wave Dark Matter", arXiv:2408.04696v2, https://arxiv.org/abs/2408.04696
  QUOTE: "Following fundamental results in quantum optics, we argue that for DM it is most likely that the density matrix takes the explicitly mixed form of a Gaussian over the basis of coherent states."
  ACCESS: abstract
  STATUS: peer-reviewed (PRD per B&O ref.; I did not open the published version)
  CONFIDENCE: medium

## Gaps
- No comment, reply, erratum or independent calculation of B&O's eq. 8 found. INSPIRE shows 0 citations for arXiv:2607.24930 (refersto search, 2026-10-30); WebSearch found none; lit_search's arXiv endpoint timed out every call so arXiv listings of newer comments were not checked directly. The critiques facet owns any rebuttal.
- Only the INSPIRE-listed papers that cite the same works (Sawyer, Kanno et al., Redi-Tesi) were checked; the INSPIRE records of recent listings may lag the arXiv by days.
- Equation layouts of B&O eqs. 6, 7, 10-12, 17, 18, S6, S11 are garbled in the PDF text extraction, so fractions were not quoted as equations; the TeX source (arXiv e-print) is the way to confirm exact forms. I did not independently re-derive eq. 8 (owner: idealizer/mechanist); only the eq. 11 vs eq. 12 consistency was checked.
- B&O Fig. 2 and Fig. 3 plotted values were not read from the figures; only B&O's text values (~1e6 s^-1; 1e14 W; 1e54 s^-1) are cited.
- The v1-to-v2 differences were compared in the main text and discussion only (v1 p.1-3, p.6; v2 p.1-6); the SM sections were spot-checked for the 2 pi delta(0) paragraph (same in both) and the propagator paragraph (v2 adds the Feynman/retarded discussion; no "retarded" match in v1).
- Not found: any published work that computes GW -> photon pairs with a retarded source in the radiation zone, or any peer-reviewed treatment of "decay of a freely propagating GW packet" other than the 2015 Jones-Singleton essay and the ones already in the older literature (theory/critiques facets).
- Search terms tried with no relevant hit: graviton fusion into photons; two gravitons annihilate into two photons; nonlinear gravitational wave Einstein-Maxwell second order photons; Skobelev graviton-photon (since 2021): only B&O returned.
