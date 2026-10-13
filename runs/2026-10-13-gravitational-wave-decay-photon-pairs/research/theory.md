# Research: theory
status: final
Mandate: formal theory: graviton-photon amplitudes, plane-wave no-go results, coherent states/classical limits, in-in vs in-out, 2*pi*delta(0)->T
Access: lit_search INSPIRE ok, arXiv rate-limited (429/timeouts), Crossref ok; fetch_text on arxiv.org/pdf and projecteuclid worked; WebSearch used once (Deser)

## Claims



- [RT-01] CLAIM: B&O (arXiv:2607.24930, v as fetched from arxiv.org/pdf; version label not printed by the tool) define the model as a classical source T_s^{mu nu} coupled linearly to the graviton EFT through the S-matrix of their eq. (1), S = T exp[ i (8 pi G)^{1/2} Int dt d^3x h_mu nu T_s^{mu nu} ] with t_i -> -inf, t_f -> +inf, and take the coherent state D(f)|0> = S|0> as the state in which the dynamics is then evolved. So S_source|0> is used as an in-state; the field it carries is stated to be <f|h|f> = sqrt(8 pi G) Int d^4y Delta_rad(x-y) T_s(y) with Delta_rad called "the Pauli-Jordan function" (the Pauli-Jordan function is the commutator function, which is retarded minus advanced, not the retarded Green function, a point for Q2 and hidden premise 1).
  SOURCE: Blas & Oller 2026, Gravitational waves decay in vacuum, arXiv:2607.24930, p. 1-2, https://arxiv.org/pdf/2607.24930
  QUOTE: "Since D(fλ) satisfies D†(fλ)aλ(k) D(fλ) = aλ(k) + fs λ(k)1 [30], the dynamics is equivalent to substituting hµν by hµν +hc µν 1 in the quantum theory, where hc µν =⟨f| hµν|f⟩= √ 8πG Z d4y∆ rad(x−y)µναβTαβ s ,(5) is the classical radiated field by the source, and ∆rad(x− y)µναβ is the Pauli-Jordan function [30, 31]."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RT-02] CLAIM: B&O state that the field far from the source tends to an outgoing spherical wave packet h ~ cos(w_s (r-t))/r * exp(-(r-t)^2 sigma_w^2/2), a burst of duration dt ~ 1/sigma_w; they then approximate the profile by a narrow-band top-hat f_s(k) = Theta for k in [w_s - sigma_w/2, w_s + sigma_w/2] with Theta = sqrt(2 pi^2 N / (w_s sigma_w)) fixed by the mean graviton number N. The profile and polarisation pattern are therefore model inputs (hidden premise 4), and the amplitude depends on the angular pattern of the spherical wave only through what is "suppressed from now on" (the polarisation label).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, p. 2, https://arxiv.org/pdf/2607.24930
  QUOTE: "Assuming a localized source with frequency centered aroundω s with widthσ ω≪ω s (we suppress the polar- ization label from now on)f s ∝exp  − (k−ωs)2 2σ2ω  ,and far from the source, the classical field of Eq. (5) tends asymptotically to the outgoing spherical wave packet, hc µν(r−t)∝ cos(ωs(r−t)) r exp  −(r−t) 2σ2 ω/2  . This wave- form corresponds to a burst of durationδt∼1/σ ω and characteristic frequencyω s, approaching continuous emission for largeδt."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RT-03] CLAIM: B&O's fusion amplitude is the tree-level g g -> gamma gamma amplitude of Skobelev, which in their eq. (6) has only the helicity-conserving entries A++++ = A---- = 8 pi G t^2/s and A++-- = A-++... = 8 pi G u^2/s (the quoted text is garbled by PDF extraction; the entries as printed are "A++++ = A−−−− = 8πG t2 s" and "A++−− = A−−++ = 8πG u2 s"), with s = (k1+k2)^2, t = (k1-q1)^2, u = (k1-q2)^2. Their eq. (7) sums over them for an "unpolarized graviton state" as the single scalar combination (s^2 - 2tu)/s times delta_{mu1 mu2}, i.e. t^2 and u^2 entries are added with the same sign. Whether those labels are physical helicities or spin projections on a common axis, and whether the relative phase is +1, is for the mechanist; this is the item to test (hidden premise 2).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, p. 2, https://arxiv.org/pdf/2607.24930
  QUOTE: "It hence follows from Eq. (6) that the fusion amplitude, as- suming an unpolarized graviton state, can be expressed as Aµ1µ2(q1,q 2)= 4πG (2π)6 Z d3k1 2k1 Z d3k2 2k2 fs(k1)fs(k2) (7) × s2−2tu s (2π)4δ(q1 +q 2−k 1−k 2)δµ1µ2."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RT-04] CLAIM: B&O's own supplement (S3) shows the diagram with an on-shell intermediate graviton drops out: the s-channel term where one coherent graviton line carries K (K^2 = s = 0) requires collinear incoming momenta, where helicity conservation cannot be satisfied (+2 + 2 != +2) and the 3-graviton vertex vanishes. They conclude that this holds for every bilinear combination f f, f f*, f* f*, and "even if the initial and final coherent states were different". So the 1 -> 2 (graviton -> photon pair, and graviton line absorbing a second graviton into a photon pair via an on-shell graviton) channel is absent by their own argument; what remains is 2 -> 2 fusion with non-collinear incoming gravitons from the same wave packet (Q3 distinction).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, SM p. 9-10, https://arxiv.org/pdf/2607.24930
  QUOTE: "Moreover,K 0 =|K|requires the two incoming momenta to be collinear, implying helicity conservation, which cannot be satisfied because±2±2̸=±2. The amplitude also vanishes ats= 0, due to the derivative nature of gravitational couplings [cf. Eq. (6)]."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RT-05] CLAIM: B&O's rate step: in their supplement S6 the remaining energy-conserving delta function is replaced as 2 pi delta(0) -> T (interaction time) "so that P/T is the transition probability per unit time", justified by T ~ 1/sigma_w provided 1/sigma_w >> tau (the reaction time of their eq. 10). The main text says eq. (8) "is a probability per unit time for tau << dt ~ 1/sigma_w". The bound T ~ 1/sigma_w is the duration of the pulse itself (dt ~ 1/sigma_w), so T is a property of the packet at the source, not an independent propagation time; this is the hinge for hidden premise 3 (no mathematical statement that the wave keeps fusing as it propagates).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, SM p. 10 (S6) and p. 3 (after eq. 10), https://arxiv.org/pdf/2607.24930
  QUOTE: "With σω/ωs≪1, the remaining energy-conserving delta function is treated as 2πδ(0)→T, the interaction time, so that P/Tis the transition probability per unit time. This approximation improves for narrower bands sinceT∼1/σ ω, provided 1/σω≫τ, the reaction time, c.f. Eq. (10)."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RT-06] CLAIM: B&O's headline equations as printed: eq. (8) dP/dt = 3 G^2 N^2 w_s^3 sigma_w^2/(25 pi) (natural units), eq. (9) N_gamma(t) ~ G^2 N_0^2 6 w_s^3 sigma_w^2 t/(25 pi), eq. (10) tau = 25 pi / (6 G^2 E_rel^2 w_s sigma_w^2) with E_rel = N_0 w_s the energy in the wave front of width sigma_w (extraction of the printed text is flattened, see quote). Each reaction removes two gravitons and creates two photons; the coefficient 6/(25 pi) in eq. (9) is 2 x 3/(25 pi), consistent with photons = 2 x pairs, so eq. (8) is a pair rate. They state eq. (8) holds "for tau << dt ~ 1/sigma_w, with Poissonian uncertainty sqrt(sigma_w tau)".
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, p. 3, https://arxiv.org/pdf/2607.24930
  QUOTE: "= 3G2N2ω3 sσ2 ω 25π .(8) Each reaction removes two gravitons and generates two photons. As a result, the number of photons radiated is Nγ(t) =N 0−N(t), withN 0 the initial graviton number and, at leading order inG(see SM SB), Nγ(t)≈G 2N2 0 6ω3 sσ2 ωt 25π .(9) From this equation, the characteristic reaction time is τ= 25π 6G2E2 relωsσ2ω ,(10)"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RT-07] CLAIM: B&O say their computation is "equivalent to that of considering the creation of photons in a background h_c, once considered at second order (including in particular the induced metric sourced by the energy-momentum tensor of the GWs)", i.e. a semiclassical calculation on a second-order metric, (see RT-16 for their statement that hbar drops out); this is the same as saying the N^2 factor is a classical nonlinearity of Einstein-Maxwell fields acting on photon vacuum fluctuations (hidden premise 10). Also: B&O treat photon stimulated emission by CMB via W -> W (1 + 2 f_gamma) "in the average sense".
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, p. 2-3, https://arxiv.org/pdf/2607.24930
  QUOTE: "As a result, the calculation we will perform is equivalent to that of considering the creation of photons in a back- groundh c, once considered at second order (including in particular the induced metric sourced by the energy- momentum tensor of the GWs, cf. Fig. 1). To the best of our knowl- edge, this also supersedes previous semiclas- sical calculations."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RT-08] CLAIM: Gibbons (1975) proved, for a quantised massive scalar field on an exact plane sandwich gravitational wave of arbitrary profile and polarisation (classical c-number background), that no particles are produced, the Feynman propagator is computed exactly, and any reasonable regularised <T_mu nu> vanishes; he concludes that a gravitational wave far from its source propagates unhindered by quantum effects. Scope: scalar field (the paper states "spinless"), exact plane wave (infinite transverse extent, all rays parallel, no focusing/diffraction), test field on a fixed background (no graviton quantum fluctuations, no second-order backreaction of the wave stress tensor on the metric). It does not by itself cover a photon field, a spherical wave, or a wave-packet with second-order corrections, which is what B&O invoke.
  SOURCE: G. W. Gibbons 1975, Quantized Fields Propagating in Plane Wave Space-Times, Commun. Math. Phys. 45, 191, doi:10.1007/BF01629249 (open-access PDF, Project Euclid, version not stated)
  QUOTE: "It is shown that the time varying gravitational field of the wave produces no particles and the Feynman propagator for the problem is calculated exactly. This is used to show that any reasonable regularization of the vacuum expectation value of the energy momentum tensor of the field must vanish. This means that a gravitational wave far from its source will propagate without hindranc..."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RT-09] CLAIM: Khusnutdinov (2025/2026, EPJ Plus 141, 532) finds closed-form massless scalar and vector Green functions in a plane gravitational wave spacetime by three independent methods (direct solution, DeWitt and Hadamard recursion) and concludes no massless particle production, noting that older Bogolyubov-coefficient calculations that gave massless particle creation are "contrasting interpretations" he addresses. This supports the extension of Gibbons' no-go to massless scalars and vectors (photons) in exact plane-wave backgrounds, and also flags that the plane-wave no-go has been disputed in the literature (Q3).
  SOURCE: N. Khusnutdinov, Quest for particles production in the plane gravitational wave spacetime, Eur. Phys. J. Plus 141, 532 (2026), arXiv:2508.11558, doi:10.1140/epjp/s13360-026-07725-2
  QUOTE: "The results coincide exactly with the DeWitt–Schwinger expansion, indicating no massless particles production in this background. Contrasting interpretations, based on Bogolyubov coefficient calculations predicting massless particle creation, are also addressed."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RT-10] CLAIM: Redi and Tesi (2026) derive that for conformal fields (central charge c_J = 4/3 conformal scalar, 4 Weyl fermion, 16 gauge field) the pair-production yield from a classical metric perturbation h_mu nu is N_dec = 2 Im Gamma_1PI = -(c_J/(30720 pi)) Int d^4q/(2 pi)^4 theta(q^2) h_mu nu(q) Pi^{mu nu rho sigma}(q) h_rho sigma(-q), equivalently N_dec = (c_J/(2560 pi)) Int d^4q/(2 pi)^4 theta(q^2) W_{mu nu rho sigma}(q) W^{mu nu rho sigma}(-q) (linearised Weyl tensor W). The support is q^2 > 0 (time-like) only: "null-like tensor and vector perturbations do not produce particles", while GW emission is controlled by the same source correlator at q^2 = 0. This is the first-order (O(h^2) in the probability, i.e. G in the rate per source power) production that is a property of the source region where the metric has time-like Fourier support (near zone / non-radiative), not of an outgoing on-shell wave. Scope: sub-horizon, flat-space limit, linear in h in the amplitude. For photons c_J = 16 (conformal, so no mass-term subtlety).
  SOURCE: M. Redi, A. Tesi 2026, Particle Production from Inhomogeneities: the off-shell side of gravitational waves, arXiv:2606.28297, p. 4-6, https://arxiv.org/pdf/2606.28297
  QUOTE: "Ndec≡2ImΓ 1PI = cJ 2560π Z d4q (2π)4θ(q2)Wµνρσ(q)Wµνρσ(−q).(6) This makes manifest the geometric nature of particle production from metric inhomogeneities." and "Notice that null-like tensor and vector perturbations do not produce particles."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

## Gaps
- [RT-11] CLAIM: Khusnutdinov states the unresolved tension: the Green-function/vacuum-expectation approach (Gibbons; Garriga-Verdaguer with Pauli-Villars) gives zero particle production by a plane GW for scalars and, in his calculation, Maxwell photons (vanishing renormalised <T_mu nu>), whereas Bogolyubov-coefficient analyses (Jones, McDougall, Singleton and co-workers, refs [26-28] there) find beta nonzero only for massless particles exactly collinear with the GW (beta ~ delta(k_v + l_v), k_v = omega - k_x). He says created photons, if any, remain in the sandwich and leave with it, so they are not detectable after the wave passes, and this is an unresolved issue. So the plane-wave no-go is exact for massive fields and for non-collinear massless fields; only the exactly collinear massless sector is disputed, and it is the sector where B&O say the graviton-photon amplitude vanishes.
  SOURCE: N. Khusnutdinov, EPJ Plus 141, 532 (2026), arXiv:2508.11558, p. 2, 6-7, https://arxiv.org/pdf/2508.11558
  QUOTE: "For massive par- ticles,k v +l v >0, ensuringβ=0; for massless particles, the sum can vanish, allowingβ̸=0. This leads to an apparent tension between the DeWitt–Schwinger and Bogolyubov approaches in the context of plane gravitational wave backgrounds" and "The standard method based on the Green-function formalism [8] predicts no particle creation, whereas the Bogolyubov approach suggests a flux of photons in the direction of the GW . The aim of this paper is to draw the attention of the physics community to this unresolved issue."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RT-12] CLAIM: Khusnutdinov's text records the older literature: photon-graviton interaction in external electromagnetic fields, with cross sections scaling as (G/c^3)^2, was studied by Tourrenc (1970) and Skobelev (Sov. Phys. J. 18, 62, 1975) [his refs 23, 24]; the Gibbons scalar Green function equals its DeWitt-Schwinger expansion, hence "plane gravitational waves do not induce scalar particle production". This dates the Skobelev amplitude that B&O use, and shows the source of eq. (6) is a 1975 paper (not read directly here).
  SOURCE: N. Khusnutdinov 2026, arXiv:2508.11558, p. 2, https://arxiv.org/pdf/2508.11558
  QUOTE: "The Green function for a scalar field in a plane gravitational- wave spacetime was first derived by Gibbons [25], who demon- strated that it coincides exactly with its DeWitt–Schwinger ex- pansion. This result implies that plane gravitational waves do not induce scalar particle production."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RT-13] CLAIM: In the amplitude/KMOC literature the same sandwich of in and out is made explicit: Cristofoli, Gonzo, Kosower, O'Connell (PRD 106, 056007, 2022) say coherent states of massless bosons are the classical limit and they treat "observables both with incoming and with outgoing waves"; their formalism has distinct incoming-wave observables (a classical wave in the in-state, e.g. light deflection) and outgoing-wave observables (waveforms, expectation values of radiation fields in the out region). It is therefore not automatic that a displaced vacuum S_source|0> taken as in-state corresponds to the outgoing retarded field; it is the in-state that evolves to the out-state with extra radiation, and the retarded field (time asymmetric) emerges only when the in-in/Schwinger-Keldysh expectation value is taken.
  SOURCE: A. Cristofoli, R. Gonzo, D. A. Kosower, D. O'Connell, Waveforms from amplitudes, Phys. Rev. D 106, 056007 (2022), arXiv:2107.10193
  QUOTE: "We show how to compute classical wave observables using quantum scattering amplitudes. We discuss observables both with incoming and with outgoing waves. The required classical limits are naturally described by coherent states of massless bosons."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RT-14] CLAIM: Caron-Huot, Giroux, Hannesdottir, Mizera (JHEP 01 (2024) 139) argue that expectation values of radiation fields (waveforms) are not time-ordered S-matrix elements but inclusive observables with the time-ordering relaxed, computed on a Schwinger-Keldysh contour with retarded products, e.g. the waveform's reduction formula uses a retarded product R{...}. They stress that in-out (S-matrix, time-ordered, Feynman propagator) and in-in (expectation of an out operator in the in-state, retarded/commutator propagators) quantities differ in general; they agree for the first-order linear response but not necessarily at higher order. This is the formal basis for the in-out vs in-in question in Q2: B&O compute an in-out probability for the specific pair final state with a Feynman propagator and then show a "retarded" term; the number of photons in the final state N_gamma = <out|N|out> is an in-in quantity.
  SOURCE: S. Caron-Huot, M. Giroux, H. S. Hannesdottir, S. Mizera, What can be measured asymptotically?, JHEP 01 (2024) 139, arXiv:2308.02125, p. 1, 26
  QUOTE: "We argue that in addition to scattering amplitudes, a whole compendium of inclusive observables exists where the time-ordering is relaxed. These include expectation values of electromagnetic or gravitational radiation fields as well as out-of-time-order amplitudes." and "A natural choice of operator ordering can typically be determined from the physical question being asked. Let’s consider the problem of determining the expectation value of a certain field (e.g., electromagnetic or gravitational) following a collision, regardless of any other properties of the final state, as discussed in the introduction."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium
  (the sentence on agreement of in-in and in-out at first order is my inference, not quoted)

- [RT-15] CLAIM: The published gravitational Compton / graviton-photon amplitudes confirm the structure of B&O's eq. (6) up to crossing. Bjerrum-Bohr, Holstein, Plante, Vanhove (PRD 91, 064008, 2015) find that in the massless limit the only non-vanishing graviton-photon (gamma g -> gamma g) helicity amplitudes are D(++;++) = D(--;--) = 8 pi G s^2/t and D(--;++) = D(++;--) = 8 pi G u^2/t, giving the unpolarised invariant cross section dsigma/dt = 2 pi G^2 (s^4 + u^4)/(s^2 t^2) (sum of squares of the two helicity amplitudes, no cross term), "in agreement with" Skobelev. Crossing s <-> t gives the g g -> gamma gamma magnitudes 8 pi G t^2/s and 8 pi G u^2/s, the entries B&O print in eq. (6). Consequence for hidden premise 2: the unpolarised rate must add |t^2/s|^2 + |u^2/s|^2 (t^4 + u^4 over s^2), whereas B&O's eq. (7) amplitude is proportional to (s^2 - 2tu)/s = (t^2 + u^2)/s (using s + t + u = 0), i.e. the amplitudes for the two final photon helicity configurations added coherently with equal sign; whether that corresponds to a definite physical (linearly polarised) final state, and not to double counting, is for the mechanist. Scope: tree level, massless limit of the spin-1 gravitational Compton amplitude; the paper explains this massless limit needs care because the longitudinal mode of a massive spin-1 decouples.
  SOURCE: N. E. J. Bjerrum-Bohr, B. R. Holstein, L. Plante, P. Vanhove, Graviton-Photon Scattering, Phys. Rev. D 91, 064008 (2015), arXiv:1410.4148, p. 21-22, https://arxiv.org/pdf/1410.4148
  QUOTE: "We begin by noting that in the massless limit the only nonvanishing helicity amplitudes are D1(++; ++)m=0 = D1(−−;−−)m=0 = 8πG s2 t , D1(−−; ++)m=0 = D1(++;−−)m=0 = 8πG u2 t" and "= 2πG 2s4 +u4 s2t2 , (5.4) which agrees with the value calculated via conventional methods by Skobelev [35]."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RT-16] CLAIM: B&O themselves state the classical content of the result: with stimulated emission by a background photon bath, "all the hbar disappear, and our calculation corresponds to a classical process". Together with RT-07 (computation = photon creation in a second-order metric background h_c), this concedes the N^2 enhancement is classical nonlinearity acting on photon vacuum fluctuations, not a collective quantum decay (hidden premise 10); but 'classical process' for a photon pair from vacuum is not a classical Einstein-Maxwell solution (Maxwell is linear and homogeneous in F, so F = 0 stays a solution on any metric): the photons come from the quantised photon field's vacuum fluctuations in a time-dependent metric, as in Gibbons/Parker-type particle creation.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930, p. 3, https://arxiv.org/pdf/2607.24930
  QUOTE: "can see that all theℏdisappear, and our calculation cor- responds to a classical process."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium
  (second sentence of the claim, F = 0 stays a solution, is my own inference from the linearity of Maxwell's equations on a fixed metric; no source quoted for it)

- [RT-17] CLAIM: Jones, McDougall, Singleton (PRD 95, 065010, 2017) argued that tree-level g g -> gamma gamma implies that a gravitational wave should create massless particles, and computed the rate at which a plane GW creates a massless scalar field by Bogolyubov coefficients on a plane-wave background; Khusnutdinov (RT-11) identifies this family (with Garriga-Verdaguer's beta ~ delta(k_v + l_v) for exactly collinear massless modes) as the dissenting side of the Gibbons no-go. This is the closest prior claim to B&O's (a GW making massless pairs) and uses a plane wave, so its pair production is localised in the collinear sector that B&O's tree amplitude excludes. Not independently verified here: the sign, size and physical meaning of beta; flagged for critiques.
  SOURCE: P. Jones, P. McDougall, D. Singleton, Particle production in a gravitational wave background, Phys. Rev. D 95, 065010 (2017), arXiv:1610.02973 (abstract via INSPIRE)
  QUOTE: "We study the possibility that massless particles, such as photons, are produced by a gravitational wave. That such a process should occur is implied by tree-level Feynman diagrams such as two gravitons turning into two photons, i.e., g+g→γ+γ. Here we calculate the rate at which a gravitational wave creates a massless scalar field. This is done by placing the scalar field in the background of a pl…"
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RT-18] CLAIM: Garriga and Verdaguer (PRD 43, 391, 1991) treated massless and massive scalar particles in exact gravitational plane waves with Bogoliubov/scattering methods; their abstract states that the quantum scattering cross section coincides with the classical geodesic one, and that the field stress tensor between scattering states diverges where classical test particles focus (so the plane-wave background is singular there), Khusnutdinov (RT-11) credits them with the Pauli-Villars confirmation of Gibbons' vanishing renormalised <T_mu nu> for scalars. Full text not reachable.
  SOURCE: J. Garriga, E. Verdaguer, Scattering of quantum particles by gravitational plane waves, Phys. Rev. D 43, 391 (1991), doi:10.1103/PhysRevD.43.391 (abstract via INSPIRE)
  QUOTE: "We consider the coupling of quantum massless and massive scalar particles with exact gravitational plane waves. The cross section for scattering of the quantum particles by the waves is shown to coincide with the classical cross section for scattering of geodesics. The expectation value of the scalar field stress tensor between scattering states diverges at the points where classical test particl…"
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RT-19] CLAIM: Dorca and Verdaguer (Nucl. Phys. B 403, 770, 1993; PRD 50, 2631, 1994) show that particle creation does occur for a quantised scalar field when two gravitational plane waves collide head on (non-collinear/opposite momenta, here with focusing into a Killing-Cauchy horizon); they use wave-packet mode quantisation, in which the "one particle states defined with the wave packet modes have two labels, one gives information on the energy of the particle and the other on its trajectory", so creation is localised. This marks the theory boundary: a single plane wave makes none (Gibbons), two crossing waves can (consistent with B&O's requirement for 2 -> 2 fusion with K^2 = s > 0), but the Dorca-Verdaguer geometry is a nonlinear exact colliding-wave solution with a horizon, not two weak coherent-state packets in flat space.
  SOURCE: M. Dorca, E. Verdaguer, Particle creation in a colliding plane wave spacetime: wave packet quantization, PRD 50, 2631 (1994), arXiv:gr-qc/9403015, p. 1-3, https://arxiv.org/pdf/gr-qc/9403015
  QUOTE: "We use wave packet mode quantization to compute the creation of massless scalar quantum particles in a colliding plane wave spacetime. The b ackground spacetime represents the collision of two gravitational shock waves followed by trailing gravitational radiation which focus into a Killing-Cauchy horizon."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RT-20] CLAIM: Deser (J. Phys. A 8, 1972, 1975, "Plane waves do not polarize the vacuum") is the loop-level companion to Gibbons: on the available snippet only (a catalog snippet found by WebSearch, not confirmed as the abstract), gravitational plane waves, like their electromagnetic and Yang-Mills counterparts, are undistorted by vacuum polarisation to all loop orders if no cosmological term is induced. This concerns vacuum polarisation (in-in <T> and effective action) on an exact plane wave, not 2 -> 2 fusion of two non-collinear waves. Free copy blocked (bot-check); abstract not confirmed.
  SOURCE: S. Deser 1975, Plane waves do not polarize the vacuum, J. Phys. A 8, 1972, doi:10.1088/0305-4470/8/12/012
  SUMMARY: "gravitational plane waves, like their electromagnetic and Yang-Mills counterparts, are undistorted by vacuum polarization effects to all loop orders, if no cosmological term is induced" (WebSearch model paraphrase of a catalog snippet; not the paper's own words)
  ACCESS: search-summary
  STATUS: peer-reviewed
  CONFIDENCE: low

## Notes (derivations by the researcher, not sourced claims; check with the mechanist/examiner calculations)
- Kinematics (units hbar = c = 1): for two massless on-shell gravitons K = k1 + k2, K^2 = s = 2 w1 w2 (1 - cos theta_12) >= 0, zero only for exactly parallel k1, k2. A 1 -> 2 decay of a massless particle into two massless particles needs K^2 = 0 for the parent, so q1 and q2 must be collinear with it, where the g -> gamma gamma amplitude vanishes (no tree g gamma gamma vertex; the photon couples to the graviton only through T^{mu nu} bilinear in F, so the lowest vertex is h gamma gamma, giving 1 -> 2 only off shell, s = 0 is the threshold). 2 -> 2 fusion into gamma gamma needs s > 0: both partners from the same coherent state, with angle theta_12 set by the angular spread of the wave (for a spherical wave, the local angular spread at distance r is of order lambda/r times geometric factors, so s -> 0 as the wave becomes locally plane: the premise 5 question).
- On shell, s + t + u = 0, so s^2 - 2tu = t^2 + u^2 (B&O eq. 7 numerator is t^2 + u^2, whereas the incoherent sum over final helicities gives t^4 + u^4 by [RT-15]).
- The step 2 pi delta(0) -> T is standard for plane-wave in-states in stationary scattering (transition probability per time). For a finite coherent-state wave packet of duration dt ~ 1/sigma_w, the energy delta function acquires width ~ sigma_w and the total probability is finite: P_total ~ (rate) x dt only if the rate is constant over the packet; the packet is a pulse, so the instantaneous pair production is localised where the two interacting parts of the packet overlap (a spatial region of size ~ dt x c around the source, per the Redi-Tesi and Dorca-Verdaguer wave-packet localisation points RT-10, RT-19).

## Gaps
- Skobelev 1975 (Sov. Phys. J. 18, 62) and Boccaletti et al. (1970) original g g -> gamma gamma papers: no free copy found; the magnitudes were confirmed instead through Bjerrum-Bohr et al. (RT-15), which states agreement with Skobelev.
- Textbook statement of 2 pi delta(0) = T and its limits (Weinberg QFT Vol. 1 sec. 3.4; Peskin & Schroeder sec. 4.5): not fetchable; no quotable source on when a transition probability per unit time is valid for a finite wave packet. A fetch of Ishikawa et al. 1206.2593 found no matching phrase.
- Deser (1975) abstract not confirmed (bot check): PAPER TO REQUEST: 10.1088/0305-4470/8/12/012 | Plane waves do not polarize the vacuum | whether the all-loop statement covers photon production by a plane GW and what it assumes about the cosmological term.
- Garriga and Verdaguer (1991) full text not reachable: PAPER TO REQUEST: 10.1103/PhysRevD.43.391 | Scattering of quantum particles by gravitational plane waves | whether beta = 0 for photons/massless scalars at exactly collinear momenta, which is Khusnutdinov's flagged tension.
- No published KLT/double-copy derivation of the full g g -> gamma gamma amplitude with phases (the tool-box qft_second_order gives the same magnitudes, 8 pi G t^2/s, 8 pi G u^2/s, but is not a citable source). Phases between helicity amplitudes (hidden premise 2) are left to the mechanist.
- INSPIRE refersto search for papers citing arXiv:2607.24930 returned zero results (the paper has 0 citations in INSPIRE as of the search); no rebuttal found for this facet (critiques owns that).
- KMOC / Cristofoli et al. exact statement on in-state vs out-state classical field (retarded vs time-symmetric) was only partly verified (RT-13 abstract level plus section list); the specific sentence that a coherent in-state S|0> carries a time-symmetric field was not located.
- arXiv API rate limits (HTTP 429/timeouts) hit lit_search repeatedly; INSPIRE and fetch_text on arxiv.org/pdf worked.
