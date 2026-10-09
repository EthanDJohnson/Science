# Research: frontier
status: final
Mandate: 2023-2026 work, newest first: new constructions after the 2024 shell (accelerating or superluminal positive-energy proposals, Rodal's irrotational drive), numerical-relativity simulations (Clough-Dietrich-Khan), Warp Factory follow-ups, conference talks. (Claims are roughly in order of discovery, not strictly by date; dates are in each claim. Newest: RF-01 (28 Sep 2026), RF-07 (3 Sep 2026), RF-02 (v4 13 Sep 2026).)
Access: lit_search INSPIRE ok, arXiv ok (abstract pages and PDFs via fetch_text.py); Crossref ok; publisher DOIs 10.1088/1361-6382/ad3ed9 and 10.1016/j.aop.2025.170147 had no free copy; WebFetch domains that worked: modernengineeringmarvels.com (press, no primary source)

## Claims

- [RF-01] CLAIM: Bolívar, Vasilev & Abellán (arXiv, submitted 28 Sep 2026) prove a sharp lower bound on the Eulerian negative energy of Natário (divergence-free shift) bubbles with unit lapse, flat interior radius R, wall thickness Δ, exterior stream speed v: E_min ~ v²R⁴/(4Δ³) as Δ→0, two powers of R/Δ above the earlier v²R²/Δ estimate. The bounded quantity is the Lobo-Visser Eulerian volume integral on the flat slice, which they state is slice- and observer-dependent and distinct from ADM mass. Bears on premise 9 (Natário is not free of negative Eulerian energy).
  SOURCE: Bolívar, Vasilev, Abellán 2026, "Zero expansion is not free: the sharp minimum of Eulerian negative energy in Natário warp drives", arXiv:2609.36211 (preprint), https://arxiv.org/abs/2609.36211
  QUOTE: "As the wall thins, $\mathcal{E}_{\min}\sim v^2R^4/(4\Delta^3)$ with sharp constant $1/4$, two powers of $R/\Delta$ above the earlier estimate $v^2R^2/\Delta$ applied to both Natário and Alcubierre bubbles. Incompressibility forces the flux displaced by the bubble to return through the wall, and the tangential shear of this return current dominates the energy."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-02] CLAIM: An T. Le's "Radiative steering of warp shells" (arXiv:2606.22531, v4 of 13 Sep 2026, substantially revised and retitled from earlier versions) constructs exact timelike junctions between a compact flat cavity and a Kinnersley photon-rocket exterior. Shells meet the strict surface DEC and steer subluminally under nonnegative radiation; successive burns obey m_f/m_i = e^(-3L) (L = exterior velocity-space path length). This is a start/stop/steer construction that works by emitting radiation, i.e. it is a photon rocket with a warp-style cavity, not a self-propelled drive. Self-gravitating settling after a turn is stated to be open.
  SOURCE: Le 2026, "Radiative steering of warp shells", arXiv:2606.22531v4 (preprint), https://arxiv.org/abs/2606.22531
  QUOTE: "The shells satisfy the strict surface dominant energy condition and steer subluminally under nonnegative radiation. Burns joined at static spheres give $m_f/m_i=e^{-3L}$ for exterior velocity-space path length $L$ ... Self-gravitating settling after a turn remains open."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-03] CLAIM: Le (arXiv:2602.18023, v6 of 24 Sep 2026) gives an observer-robust energy-condition test (S-lemma, 4x4 linear matrix inequalities; no Hawking-Ellis classification or rapidity cutoff needed) with interval-arithmetic certificates, implemented in the JAX toolkit Warpax. Comparing four warp geometries at matched parameters, global bounds establish NEC violation in all four bubble walls (including Rodal's irrotational profile); the Rodal profile has zero Eulerian momentum and is everywhere Type I, and the Eulerian reading misses about 73% of its sampled wall WEC violations. The type labels and fractions are numerical samples, distinct from the interval bounds. Directly relevant to premise 8 (numerical checks versus "all observers").
  SOURCE: Le 2026, "Observer-robust energy condition verification for warp drive spacetimes", arXiv:2602.18023v6 (preprint), https://arxiv.org/abs/2602.18023
  QUOTE: "At the reference parameters, the global bounds establish null-energy violation in all four bubble walls. The ideal irrotational Rodal profile has zero Eulerian momentum and is everywhere Type I; Type-IV regions are detected in the other sampled walls. For Rodal, the Eulerian reading misses about $73\%$ of the sampled wall weak-energy violations."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-04] CLAIM: Rodal (Gen. Relativ. Gravit. 58, 1 (2026), published 17 Dec 2025; arXiv:2512.18008) gives an explicit smooth irrotational (scalar-potential) unit-lapse flat-slice warp shift, globally Hawking-Ellis Type I. At identical parameters (rho, sigma, v/c) its peak proper-energy deficit is ~38x smaller than Alcubierre and ~2.6e3x smaller than Natário; peak NEC violation >60x smaller than Natário. Net slice-integrated proper energy is consistent with zero (|E+ - E-|/(E+ + E-) = 0.04% after far-field extrapolation). Title says "predominantly" positive: negative energy and NEC violation are reduced, not removed; this is not a positive-energy solution. Its speed regime is not stated in the abstract.
  SOURCE: Rodal 2026, "A warp drive with predominantly positive invariant energy density and global Hawking-Ellis Type I", Gen. Relativ. Gravit. 58, 1, doi:10.1007/s10714-025-03495-x; arXiv:2512.18008, https://arxiv.org/abs/2512.18008
  QUOTE: "its peak proper-energy deficit is reduced by a factor of $\approx 38$ relative to Alcubierre and $\approx 2.6 \times 10^{3}$ relative to Natário, and its peak NEC violation is more than $60 \times$ smaller than Natário. Crucially, the stress-energy is \emph{globally} Hawking-Ellis Type I"
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-05] CLAIM: Le's "Relativistic elastic shells" (arXiv:2605.25417, v3 of 17 Sep 2026; versions v1-v3 differ greatly in length, 2.5 MB to 151 KB) studies material support of a finite-thickness shell with a flat cavity. Results stated: non-negative isotropic pressure cannot support a static spherical shell of positive-density matter with two free vacuum faces; tangential elastic stress admits equilibria near relaxation which, in sufficiently weak gravity, obey the DEC and have subluminal sound speeds; static cavities are locally flat with clocks redshifted relative to infinity; nonlinear compression can give unbounded gradients; nonspherical even-parity and rotating stability are open. Relevant to premise 6 (matter model). Critiques facet owns the verdict on the 2024 shell; listed here as a frontier source for the matter-model question.
  SOURCE: Le 2026, "Relativistic elastic shells: material support and cavity geometry", arXiv:2605.25417v3 (preprint), https://arxiv.org/abs/2605.25417
  QUOTE: "Nonnegative isotropic pressure cannot support a static spherical shell of positive-density matter with two free vacuum faces, whereas tangential elastic stress admits equilibria near relaxation. For sufficiently weak gravity these equilibria obey the dominant energy condition and have subluminal sound speeds. Their static cavities are locally flat, with clocks redshifted relative to infinity."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-06] CLAIM: Garattini & Zatrimaylov (arXiv:2502.13153, v4 June 2026) embed an Alcubierre-type warp bubble in de Sitter space and report that if the bubble moves radially at the speed of the expansion of the universe, the energy density can be strictly non-negative, with the weak and null conditions satisfied only "up to a total divergence term that averages to zero". This is a cosmological-background, not asymptotically flat, construction; the energy conditions hold only in an averaged sense, so it does not meet the brief's pointwise WEC.
  SOURCE: Garattini & Zatrimaylov 2025, "Warp Drive in a De Sitter Universe", arXiv:2502.13153v4 (preprint), https://arxiv.org/abs/2502.13153
  QUOTE: "it is possible for the bubble to have strictly non--negative energy density, with the weak and null energy satisfied up to a total divergence term that averages to zero."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-07] CLAIM: Jusufi & Lobo (arXiv:2609.05554, 3 Sep 2026) propose a T-duality-inspired smooth Alcubierre profile f = 1 - r³/(r²+l²)^{3/2}, l² = R² + l₀², with closed-form E = -(15π/1024) v_s² l (geometric units) for the Eulerian volume integral. The authors state exotic matter remains necessary and that this is an effective ansatz, not derived from string-corrected field equations. Included as a negative-energy comparator: new in 2026 but not a positive-energy construction.
  SOURCE: Jusufi & Lobo 2026, "Quantum-gravity-inspired Alcubierre warp-drive geometries", arXiv:2609.05554 (preprint), https://arxiv.org/abs/2609.05554
  QUOTE: "In particular, $E=-(15\pi/1024)v_s^2 l$ in geometric units and $|\rho_E|$ is bounded by a constant times $v_s^2/l^2$. ... Exotic matter remains necessary, and neither semiclassical stability nor a modified quantum energy inequality is claimed without an explicit renormalized stress-tensor calculation."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: high

- [RF-08] CLAIM: Fell & Loeb (arXiv:2608.10800, 11 Aug 2026) simulate "zero ADM mass" warp-drive spacetimes in Earth's atmosphere: an aircraft-scale bubble moving relativistically would produce luminosities exceeding 1 TW; a warp drive above ~10% c in the atmosphere would produce a "brilliant glow". This is an observational-signature paper, not an energy-condition result; it assumes the bubble exists.
  SOURCE: Fell & Loeb 2026, "Radiative Signatures from Warp Drives Traveling Through the Earth's Atmosphere", arXiv:2608.10800 (preprint), https://arxiv.org/abs/2608.10800
  QUOTE: "Numerical simulations indicate that an aircraft-scale spacetime bubble moving at relativistic velocities would have a pronounced observational signature, where interaction with the atmosphere can produce luminosities exceeding one terawatt."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-09] CLAIM: Clough, Dietrich & Khan (Open J. Astrophys. 7, 2024; arXiv:2406.02466) numerically evolve an Alcubierre warp-drive "containment failure" with a stiff-fluid equation of state, computing the gravitational-wave signal and fluid energy fluxes. They present it as a study of the dynamical evolution and stability of spacetimes that violate the NEC, not as a positive-energy drive.
  SOURCE: Clough, Dietrich, Khan 2024, "What no one has seen before: gravitational waveforms from warp drive collapse", Open J. Astrophys. 7, doi:10.33232/001c.121868; arXiv:2406.02466, https://arxiv.org/abs/2406.02466
  QUOTE: "In this work, we study the signatures arising from a warp drive "containment failure", assuming a stiff equation of state for the fluid. We compute the emitted gravitational-wave signal and track the energy fluxes of the fluid."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-10] CLAIM: Lentz & Felton (arXiv:2405.19381, May 2024, PNNL-SA-198722) argue that sub- or superluminal warp-drive travel would produce detectable emissions (electromagnetic, particle, gravitational) and propose a simulation research program for coordinated multi-observatory searches. This is a technosignature proposal; it takes warp bubbles with "positive energy sources" as an assumption, and the abstract gives no energy-condition calculation.
  SOURCE: Lentz & Felton 2024, "Motivating Emissions from Positive Energy Warp Bubbles", arXiv:2405.19381 (preprint), https://arxiv.org/abs/2405.19381
  QUOTE: "we hypothesize that an advanced inter-planetary or interstellar civilization using warp drives at sub-luminal or super-luminal speeds will broadcast detectable emissions of their travels."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: high

- [RF-11] CLAIM: Barzegar, Buchert & Vigneron (arXiv, 18 Feb 2026) classify current warp-drive models by their restrictions within GR, prove "several new no-go theorems", and conclude viability is hard to support "not merely due to the violation of energy conditions". Theory facet should extract the theorems; listed here as the most recent review-style critique of the whole 2021-2024 family.
  SOURCE: Barzegar, Buchert, Vigneron 2026, "General formalism, classification, and demystification of the current warp-drive spacetimes", arXiv:2602.16495 (preprint), https://arxiv.org/abs/2602.16495
  QUOTE: "Our analysis shows that when the principles of General Relativity are applied correctly, most claims regarding physical warp drives must be reassessed, and it becomes highly challenging to justify or support the viability of such models, not merely due to the violation of energy conditions."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-12] CLAIM: Buchert & Frackowiak (Universe 12, 132, 2026; arXiv:2605.03653) give governing equations for the Natário class with a one-component coordinate velocity, analyse coordinate acceleration and vorticity, and report "an expected generic instability of the warp field" for their second (geodesic-assumption) example. They propose a relativistic Lagrangian-perturbation framework with spatial curvature and Szekeres class II solutions, linking warp fields to cosmology, and discuss "possible future paths towards physical warp drives within tilted fluid flows". Relevance: a 2026 attempt to treat warp-field dynamics (time dependence), which is the acceleration question of premise 5; no start/stop solution with energy conditions is claimed in the abstract.
  SOURCE: Buchert & Frackowiak 2026, "Novel Realizations of Warp Drive Spacetimes as Solutions of General Relativity", Universe 12, 132, doi:10.3390/universe12050132; arXiv:2605.03653, https://arxiv.org/abs/2605.03653
  QUOTE: "We analyze in detail the role of coordinate acceleration and coordinate vorticity, providing illustrations for both example solutions. For the second we find an expected generic instability of the warp field."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RF-13] CLAIM: Bolívar, Abellán & Vasilev (arXiv:2608.15000, 15 Aug 2026) prove a static "boundary obstruction" for an empty flat cavity inside a positive-density wall in the unit-lapse, flat-slice radial Painlevé-Gullstrand class: the Type-I source has p_r = -rho and p_perp = -rho - r rho'/2, so a regular nonnegative density that rises out of the cavity must violate the transverse NEC and WEC. Releasing the lapse, an incomplete-beta family gives regular hollow shells with flat cavities, Schwarzschild exteriors, no thin shells, and NEC/WEC/SEC/DEC on an explicit compactness interval. The authors stress it is a static theorem and construction, "not ... a transport result". Relevant to premises 4, 6, 7: the 2024-type shell escapes the obstruction by using a non-unit lapse / curved slice.
  SOURCE: Bolívar, Abellán, Vasilev 2026, "Boundary Obstructions and Lapse Freedom in Static Spherical Hollow Cores", arXiv:2608.15000 (preprint), https://arxiv.org/abs/2608.15000
  QUOTE: "A regular nonnegative density that rises out of the cavity must therefore violate the transverse null and weak energy conditions. ... when only the lapse is released, an incomplete-beta family gives regular hollow shells with flat cavities, Schwarzschild exteriors, no thin shells, and NEC/WEC/SEC/DEC on an explicit compactness interval."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-14] CLAIM: Chowdhury (Eur. Phys. J. C 85, 112, 2025; arXiv:2404.15948) extends the Alcubierre-Natário class to an infinite family via Martel-Poisson charts (Minkowski, AdS, dS backgrounds) with non-flat spatial metrics (conical singularities in 2+1 D), and analyses NEC violations, light-cone tilt and horizons. NEC violations remain; it is a negative-energy generalisation, not a positive-energy solution.
  SOURCE: Chowdhury 2025, "Warp Drives and Martel-Poisson charts", Eur. Phys. J. C 85, 112, doi:10.1140/epjc/s10052-025-13831-9; arXiv:2404.15948, https://arxiv.org/abs/2404.15948
  QUOTE: "We analyse the expansion/contraction of space and the (NEC) violations associated with these warp drives and find interesting scalings due to the global imprints of the conical defects."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RF-15] CLAIM: In Le's radiative-steering construction the acceleration momentum comes from emitted radiation: the exterior is a Kinnersley photon rocket, the Bondi four-momentum balance dP_B/du_B = -(integral of |N|²/4π + F) l-hat dΩ applies, zero matter flux leaves total Bondi momentum fixed, and for F ≥ 0 the radiated four-momentum is future causal. The Bondi news vanishes, so no gravitational-wave flux. Interior freely falling observers are inertial but "An observer needs a force to follow the accelerating cavity center". So this is a start/stop/steer construction that is not self-propelled: it is consistent with ADM/Bondi momentum conservation only because it burns mass, with mass cost from the relativistic rocket equation (Lemma 2.1). It therefore does not beat a photon rocket in momentum accounting; the claimed novelty is DEC-satisfying shells carrying a flat cavity through the burn.
  SOURCE: Le 2026, "Radiative steering of warp shells", arXiv:2606.22531v4 (preprint), https://arxiv.org/pdf/2606.22531
  QUOTE: "Anisotropic photon emission changes the total momentum. The Bondi news vanishes, so there is no gravitational-wave flux at infinity ... An observer needs a force to follow the accelerating cavity center; freely falling test observers in the interior are inertial." and "Zero flux leaves total Bondi momentum fixed."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-16] CLAIM: Scope note on RF-04: Rodal's figures and tables are computed for the light-speed case v = c; he states superluminal velocities "produce analogous qualitative behavior" and refers to an earlier reference for numerical detail on Alcubierre and Natário. He also notes superluminal warp drives generally have Cauchy horizons, limiting global use of the 3+1 split. So the "predominantly positive" claim has not been shown for a v well above c, and no travel-time (arrival-before-light) test is reported in the passages found.
  SOURCE: Rodal 2026, Gen. Relativ. Gravit. 58, 1; arXiv:2512.18008, https://arxiv.org/pdf/2512.18008
  QUOTE: "we restrict attention to the light-speed case here; superluminal warp-bubble velocities produce analogous qualitative behavior (as follows from the analytic expressions) and have been numerically detailed for the Alcubierre and Natário drives in Ref. [36]."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-17] CLAIM: Barzegar, Buchert & Vigneron state Theorem IV.32: "The Natário zero-expansion warp drive violates the WEC." Proof sketch given: with mean curvature K = 0 the Hamiltonian constraint gives Eulerian energy density proportional to -|K_ij|²/2 ≤ 0 on the flat slice, so the density is negative unless K ≡ 0 (Minkowski). Theorem IV.33 generalises: a non-vacuum spacetime with a vanishing-mean-curvature foliation and Ricci scalar R < 2Λ + |K|² violates the WEC. Direct bearing on premise 9: Natário's drive needs negative Eulerian energy, as Alcubierre's does (for unit lapse, flat slices). Also Error 26 of that paper states the Alcubierre WEC violation is independent of v, i.e. not tied to superluminal speed.
  SOURCE: Barzegar, Buchert, Vigneron 2026, arXiv:2602.16495 (preprint), https://arxiv.org/pdf/2602.16495
  QUOTE: "Theorem IV.32. The Natário zero-expansion warp drive violates the WEC. Proof. If K = I[K] = 0, then II[K] = -|K|²h/2 ≤ 0, which shows the violation of the WEC by the Hamilton constraint (3.11), unless K ≡ 0 identically, which yields exactly Minkowski spacetime" (PDF extraction garbled the superscripts; wording otherwise as printed)
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RF-18] CLAIM: Barzegar et al. directly dispute the 2021-2024 "physical warp drive" papers. They say the Lentz, Bobrick-Martire and Fell-Heisenberg claims "have been refuted correctly (fully or partially) by Santiago et al." and, of Fuchs et al. 2024, that "The construction proposed by Fuchs et al. [28] is not a solution to Einstein's equations", because the TOV equations were not solved (their Appendix B). They also say the notion of "constant velocity" there has no clear meaning without distinguishing u^i from u_i. This is a contested preprint critique; no published reply from the Fuchs/Helmerich/Martire group was found. The critiques facet owns the verdict, so treat this as a lead to the dispute, not a settled refutation.
  SOURCE: Barzegar, Buchert, Vigneron 2026, arXiv:2602.16495 (preprint), https://arxiv.org/pdf/2602.16495
  QUOTE: "Error 18. The construction proposed by Fuchs et al. [28] is not a solution to Einstein's equations; indeed, as we showed in Appendix B, the authors do not solve the Tolman-Oppenheimer-Volkoff (TOV) equations resulting from the Einstein equation in the given context."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RF-19] CLAIM: Fell & Loeb 2026 state that their atmospheric-signature results are "strictly for zero ADM mass warp drives, such as the Alcubierre metric, the Van den Broeck metric, and the Lentz metric", and that non-zero-ADM-mass (Bobrick-Martire-type) warp drives would behave differently because the curvature is non-zero throughout the space; sub-relativistic velocities are left to future work. So even the 2024 shell has no atmospheric-signature calculation yet.
  SOURCE: Fell & Loeb 2026, arXiv:2608.10800 (preprint), https://arxiv.org/pdf/2608.10800
  QUOTE: "The results of this study are strictly for zero ADM mass warp drives, such as the Alcubierre metric [25], the Van den Broeck metric [45], and the Lentz metric [1]. It has been shown in Bobrick and Martire [2] that generic warp drive spacetimes have non-zero ADM mass and thus a fundamentally distinct asymptotic structure than the zero ADM mass variants."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-20] CLAIM: Fell & Loeb cite Sellers et al. as showing that present-day gravitational-wave detectors are sensitive to rapidly and/or massively accelerating objects, "which would include non-zero ADM mass accelerating warp drive spacetimes". The Sellers et al. paper itself was not located in INSPIRE or Crossref in this run; this is a second-hand pointer to a possible detector test of acceleration (premise 5), unverified.
  SOURCE: Fell & Loeb 2026, arXiv:2608.10800 (preprint), https://arxiv.org/pdf/2608.10800 (citing "Sellers et al. [15]")
  QUOTE: "Sellers et al.[15] showed that present-day gravitational wave detectors are sensitive to rapidly and/or massive accelerating objects, which would include non-zero ADM mass accelerating warp drive spacetimes."
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: low

- [RF-21] CLAIM: Rodal (arXiv:2507.09724 v2, July 2025) argues that "low-energy" warp-drive concepts using a metamaterial-controlled spatially varying gravitational coupling κ(x) fail: a prescribed κ(x) in G^{μν} = κ(x)T^{μν} contradicts the contracted Bianchi identity (forcing ∇_μT^{μν} ≠ 0); a dynamical κ gives a scalar-tensor theory excluded by |γ-1| ≲ 1e-5 (Solar System, pulsar timing). Included as a frontier negative result on the "make the warp cheaper by changing G" class; the proposals it rebuts were not located in the literature search.
  SOURCE: Rodal 2025, "On the Infeasibility of Low-Energy Warp Drive via Metamaterial Gravitational Coupling", arXiv:2507.09724 (preprint), https://arxiv.org/abs/2507.09724
  QUOTE: "A prescribed, non-dynamical $\kappa(x)$ in the field equation $G^{\mu\nu} = \kappa(x)T^{\mu\nu}$ clashes with the contracted Bianchi identity, $\nabla_\mu G^{\mu\nu} \equiv 0$, forcing $\nabla_\mu T^{\mu\nu} \neq 0$ and thus violating local energy-momentum conservation."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-22] CLAIM: Rodal (Int. J. Theor. Phys. 63, 168, 2024; arXiv:2512.19837) finds Natário's spacetime is Petrov type I, and that at identical bubble parameters its curvature-invariant amplitudes are 35 times greater than Alcubierre's, "making Natário's concept even less viable"; momentum density is the critical quantity governing trajectory orientation. Note the arXiv posting (22 Dec 2025) is later than the journal year; confirm the journal reference with INSPIRE before citing. Bears on premise 9: the zero-expansion property does not reduce stress.
  SOURCE: Rodal 2024, "A Closer Look at Natário's Zero-Expansion Warp Drive", Int. J. Theor. Phys. 63, 168, doi:10.1007/s10773-024-05700-0; arXiv:2512.19837, https://arxiv.org/abs/2512.19837
  QUOTE: "We demonstrate that Natário's spacetime exhibits curvature invariant amplitudes 35 times greater than Alcubierre's, given identical warp-bubble parameters, making Natário's concept even less viable."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RF-23] CLAIM: [speculative: negative active mass] Shirokov (arXiv:2608.24577, 25 Aug 2026) evolves a "Bondi dipole" (positive mass plus phantom scalar of negative active gravitational mass) in 3+1 numerical relativity: a mass-matched pair released at rest self-accelerates as a unit to 0.056c by t = 400 (geometric units) with total signed momentum held at zero to ≲1%, and no detectable gravitational radiation. This is the only numerical-relativity self-propulsion result found, and it needs negative active mass, so it never counts toward "possible under established physics"; it is not a warp metric.
  SOURCE: Shirokov 2026, "The Bondi Dipole in Full Numerical Relativity: a Self-Accelerating Positive-Negative Mass Binary", arXiv:2608.24577 (preprint), https://arxiv.org/abs/2608.24577
  QUOTE: "a mass-matched pair released at rest accelerates as a unit. The midpoint moves $3.00\pm0.01$ by $t=200$ with the separation held to 1%, and reaches a speed of $0.056c$ by $t=400$ with the acceleration steady to 2%; the total signed momentum holds at zero to $\lesssim 1$%."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-24] CLAIM: Abellán et al. (CQG 41, 105011, 2024) add a non-uniform lapse as an extra degree of freedom to a spherical warp-based geometry and find a fluid with heat flow can be accommodated; Bolívar et al. (Annals Phys. 481, 170147, 2025) give a piecewise analytic treatment with trivial lapse and Painlevé-Gullstrand-type radial shift, which leads "naturally to an anisotropic energy-momentum tensor". Both are matter-content/lapse-freedom studies of the shell-type family; full texts are paywalled, only INSPIRE abstract fragments were read.
  SOURCE: Abellán et al. 2024, doi:10.1088/1361-6382/ad3ed9; Bolívar et al. 2025, doi:10.1016/j.aop.2025.170147 (INSPIRE abstracts, https://inspirehep.net/literature/2781928 and https://inspirehep.net/literature/2955748)
  QUOTE: "By allowing a non-uniform lapse function to evolve, we find that it is possible to accommodate a fluid that includes heat flow."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: low

## Gaps
- No post-2024 construction was found that is both superluminal (in the travel-time sense) and satisfies the WEC for all observers. Every 2025-2026 item found is subluminal, static/constant-velocity, negative-energy-reduced, or a critique.
- No accelerating positive-energy warp solution with solved dynamics was found. The nearest items are Le's radiative-steering shells (RF-02, RF-15; momentum from emitted photons) and Buchert & Frackowiak's warp-field dynamics (RF-12; generic instability in one example).
- Not located: Sellers et al. on gravitational-wave detectors and accelerating warp drives (cited as [15] by Fell & Loeb); Bian et al. on warp drives and the interstellar medium; Lentz's Marcel Grossmann reply and Lentz's 2023 "hyper-fast positive energy warp drives" proceedings (only a ResearchGate listing seen); the proposals Rodal rebuts on metamaterial coupling.
- Not read in full: the 2024 Fuchs et al. paper and Helmerich et al. (theory/quantitative facets own them); Le's 2602.18023 body tables (only abstract quoted; the 73% and Type-IV statements are the paper's own sampled results); Bolívar et al. 2609.36211 body.
- Not verified: author replies to Barzegar et al. 2026 or to Celmaster & Rubin 2025 (none found as of 1 Oct 2026 in INSPIRE citing-lists of Fuchs 2024, Lentz 2020, Bobrick-Martire, Fell-Heisenberg). Press pieces of Feb-Mar 2026 (modernengineeringmarvels.com) only restate the 2024 shell paper and give no new source.
- Several 2026 preprints are v1 or recently revised (Le's papers have 4 to 6 versions with large changes); treat their numbers as moving.
- No conference talk with results newer than the literature was found; WebSearch returned only press coverage.
- PAPER TO REQUEST: doi:10.1088/1361-6382/ad3ed9 | Spherical warp-based bubble with non-trivial lapse function and its consequences on matter content | whether the lapse freedom gives DEC-satisfying warp matter and with what sources
- PAPER TO REQUEST: doi:10.1016/j.aop.2025.170147 | Warp bubble geometries with anisotropic fluids: A piecewise analytical approach | whether its piecewise shells meet NEC/WEC/DEC for all observers
