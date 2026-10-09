# Research: frontier
status: final
Mandate: wormhole and energy-condition work of the last five years (about 2021-2026), newest first, each labelled with its evidential status; relaunch 2026-10-08 adds the warp-run carry-over (only where it bears on wormholes) and a search for work newer than 2026-10-01. Claims RF-01..RF-21 are from the first pass (ordered by discovery); the newest-first index is at the end under "Index by date".
Access: lit_search INSPIRE ok, arXiv intermittently blocked (HTTP 429 on several queries); fetch_text.py on arxiv.org/pdf worked for all papers quoted; WebSearch used once (search-summary only). No WebFetch needed.

Scope note: "frontier" here = post-2020 work plus the 2020 Maldacena-Milekhin and 2021 Blazquez-Salcedo et al. papers as the baseline they react to. Units: natural units (hbar = c = 1) unless stated; SI where stated.

## Claims

- [RF-01] CLAIM: Kain (2023, PRD 108, 044019) numerically evolved the asymmetric, smooth static Einstein-Dirac-Maxwell (EDM) wormholes (parameters mu-bar = 0.2, e-bar/sqrt(4 pi) = 0.03) forward in time and found in every case that black holes form, connected by the wormhole. Null geodesics can cross the throat but are trapped inside a black hole and cannot reach arbitrary distance on the other side. He concludes EDM wormholes are NOT traversable. This is the most direct dynamical critique of the "no exotic matter" claim. Scope: spherical symmetry, the specific parameter set simulated; he explicitly does not rule out some other asymmetric solution behaving differently.
  SOURCE: B. Kain, 2023, "Are Einstein-Dirac-Maxwell wormholes traversable?", Phys. Rev. D 108, 044019, https://arxiv.org/abs/2305.11217
  QUOTE: "In all cases considered, our simulations indicate that black holes form that are connected by the wormhole. Although there exist null geodesics that travel through the wormhole, we find that they are trapped inside a black hole and are unable to travel arbitrarily far away. We conclude that Einstein-Dirac-Maxwell wormholes are not traversable."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-02] CLAIM: In Kain's static EDM solutions the static throat radius R0 is only about 75 to 500 Planck lengths (Table I: R0/l_P between 75.28 and 498.4 for the listed f0 values, at mu-bar = 0.2, e-bar/sqrt(4 pi) = 0.03), "roughly two orders of magnitude larger than the Planck length". The static solutions violate the NEC (T^r_r - T^t_t < 0, by his criterion, Eq. 40). So even the static EDM wormholes found so far are microscopic in the units used; no payload of 1 kg or a human could pass. Scope: only the parameter values tabulated; the paper does not scan for macroscopic throats. (Scaling to other mu-bar, e-bar not computed here.)
  SOURCE: B. Kain, 2023, PRD 108, 044019, https://arxiv.org/abs/2305.11217
  QUOTE: "We can see that, for these solutions, the radius is roughly two orders of magnitude larger than the Planck length." ... "The solutions are regular everywhere and violate the null energy condition."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RF-03] CLAIM: Konoplya and Zhidenko (2022, PRL 128, 091104) criticise the symmetric EDM wormholes of Blazquez-Salcedo, Knoll and Radu: mirror symmetry forces non-smooth gravitational and matter fields at the throat (higher derivatives discontinuous), the sign of the fermion charge density must flip at the throat so that particles and antiparticles coexist without annihilation, and a "membrane of matter" with specific properties sits at the throat. They then construct asymmetric, smooth solutions, and conclude "this gives us the hope that such kind of wormholes could exist in nature". Scope: classical Dirac fields; the follow-up numerical dynamics (RF-01) later undercut the hope.
  SOURCE: R. A. Konoplya, A. Zhidenko, 2022, "Traversable Wormholes in General Relativity", Phys. Rev. Lett. 128, 091104, https://arxiv.org/abs/2106.05034
  QUOTE: "the mirror symmetry relatively the throat leads to the nonsmoothness of gravitational and matter fields. In particular, one must postulate changing of the sign of the fermionic charge density at the throat, requiring coexistence of particle and antiparti- cles without annihilation and posing a membrane of matter at the throat with specific properties."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-04] CLAIM: Observational follow-ups treat the EDM wormholes as real compact objects: Churilova, Konoplya, Stuchlik and Zhidenko (JCAP 10 (2021) 010) compute quasinormal modes, echoes and shadows for "wormholes without exotic matter" (EDM and Randall-Sundrum II brane-world solutions), and Stuchlik et al. (EPJ Plus 136, 1127, 2021) compute epicyclic frequencies for quasi-periodic oscillations in microquasars and AGN. Evidential status: model predictions for a hypothetical object; no detection; and given RF-01 their physical premise is in doubt. Only the abstract was read.
  SOURCE: Churilova et al. 2021, JCAP 10 010, https://arxiv.org/abs/2107.05977 ; Stuchlik et al. 2021, Eur. Phys. J. Plus 136 1127, https://arxiv.org/abs/2110.10569
  QUOTE: "An analytical solution representing traversable asymptotically flat and symmetric wormholes was obtained without adding exotic matter in two different theories independently: in the Einstein-Maxwell-Dirac theory and in the second Randall-Sundrum brane-world model." (Churilova et al. abstract as printed by lit_search)
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RF-05] CLAIM: Maldacena-Milekhin (2020/21) "humanly traversable" wormhole: tidal-force requirement for a human is a_tidal ~ size/r_e^2 < 20 g (20 g for short durations, g = 9.8 m/s^2) with size about 0.5 m, giving throat (extremal magnetic black hole radius) r_e > 1.5e7 m, i.e. about 0.05 s of light travel time (SI units). Free-fermion version in 4D would need N_f > 1e52 species for a 1e3 kg spaceship (condition |E_bin| > 1e3 kg with r_e > 1e7 m), too many for a UV cutoff, which is why they invoke Randall-Sundrum II (a speculative beyond-Standard-Model extension). Note this "20 g" tidal criterion is their own; the brief asks it be checked against Morris-Thorne 1988 (Earth gravity, about 1 g): the paper uses a much looser value.
  SOURCE: J. Maldacena, A. Milekhin, 2021, "Humanly traversable wormholes", Phys. Rev. D 103, 066007, https://arxiv.org/abs/2008.06618
  QUOTE: "20g >a∼ size r2 e → re > 1.5×107m∼.05s (3.26) where we assumed that the size is about 0 .5m" and "re|Ebin|∝ Nf(g2Nf)> 107m× 103kg →Nf > 1052 (2.16) This value of Nf is too large if we want the UV cutoff"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-06] CLAIM: In Maldacena-Milekhin the human-traversable wormhole is not a shortcut: the traveller's proper time is short (under about a second for a trip across the Galaxy) while exterior observers see tens of thousands of years. The traveller acquires a very large boost factor gamma at the centre, and a CMB photon falling in has its energy blue-shifted by the same factor, which they list as a practical problem requiring a cold, flat ambient space. From outside the object looks like a charged intermediate-mass black hole. Scope: model requires Randall-Sundrum II sector, magnetic charge, and a cold flat environment; one-sided in the sense that both mouths sit in ambient space.
  SOURCE: Maldacena, Milekhin 2021, PRD 103, 066007, https://arxiv.org/abs/2008.06618
  QUOTE: "Using them, one could travel in less than a second between distant points in our galaxy. A second for the observer that goes through the wormhole. It would be tens of thousands of years for somebody looking from the outside." and "From the outside they resemble intermediate mass charged black holes."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-07] CLAIM: Maldacena-Milekhin state that the useful application for a small version of the wormhole is secrecy, not speed: with mouths in the same system, traversal time is comparable to the distance, so the wormhole would be used "to send very secret signals or qubits", with huge tidal forces. This supports hidden premise 4 (a non-shortcut is not useless) but is a speculative remark, not a computed result.
  SOURCE: Maldacena, Milekhin 2021, PRD 103, 066007, https://arxiv.org/abs/2008.06618
  QUOTE: "Of course, it is very small and the tidal forces would be huge. But we could use them to send very secret signals or qubits."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RF-08] CLAIM: Fu, Grado-White and Marolf 2019 (CQG 36, 245018): asymptotically flat 4D wormholes between oppositely charged black holes, made traversable by perturbative back-reaction of quantum fields in Hartle-Hawking states, reach minimum transit time t_min = d + logs (c = 1; d = mouth separation; "logs" = terms logarithmic in d and black-hole parameters). That is smaller than for the eternal Maldacena-Milekhin-Popov wormholes by more than a factor of 2 and approaches the minimum allowed by the achronal ANEC (no shortcut, so T_thru/T_ext >= 1 up to log terms). Traversability is exponentially fragile (destroyed by exponentially small perturbations), the background is unstable (black holes fall together on a timescale ~ d^{3/2}), so this is a perturbative result requiring engineered cosmic strings or anchors. Scope: preprint-then-journal, perturbative, specified quantum states.
  SOURCE: Z. Fu, B. Grado-White, D. Marolf, 2019, "Traversable Asymptotically Flat Wormholes with Short Transit Times", Class. Quantum Grav. 36, 245018, https://arxiv.org/abs/1908.03273
  QUOTE: "a wormhole with mouths separated by a distance d becomes traversable with a minimum transit time tmin transit = d + logs. Thus tmin transit d is smaller than for the eternally traversable MMP wormholes by more than a factor of 2, and approaches the value that, at least in higher dimensions, would be the theoretical minimum." and "However, in such cases traversability is exponentially fragile, and can be destroyed by exponentially small perturbations."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-09] CLAIM: Emparan, Grado-White, Marolf and Tomasevic (JHEP 05 (2021) 032) extend the 4D asymptotically flat quantum-supported wormhole to multi-mouth wormholes: the three-mouth case has fundamental group F_2 rather than F_3, and a small black hole inserted in a throat can carry a further wormhole to a third region. Asymptotic flatness holds "up to the presence of possible magnetic fluxes or cosmic strings that extend to infinity". Evidential status: perturbative-quantum-field construction in Einstein-Maxwell plus charged fields; no creation mechanism or payload analysis.
  SOURCE: R. Emparan, B. Grado-White, D. Marolf, M. Tomasevic, 2021, "Multi-mouth Traversable Wormholes", JHEP 05, 032, https://arxiv.org/abs/2012.07821
  QUOTE: "Our solutions are asymptotically flat up to the presence of possible magnetic fluxes or cosmic strings that extend to infinity. The construction begins with a two-mouth traversable wormhole supported by backreaction from quantum fields."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-10] CLAIM: Bilotta (2023, preprint arXiv:2304.07356) argues that a double-trace deformation of the near-horizon, near-extremal region of Kerr (nNHEK) with scalar fields averaged over the Kerr spheroid yields a negative average null energy and a traversable wormhole, avoiding the superradiant modes. This is the first move from Reissner-Nordstrom / BTZ-like backgrounds toward astrophysically relevant rotating black holes. Limits stated by the author: the state off-axis is irregular because of superradiance, a nonperturbative 4D asymptotically flat description is only commented on, and the construction is perturbative with the deformation coupling two boundaries. He notes the standard logic: a traversable wormhole must violate ANEC, and achronal ANEC "has been proven to hold ... in the absence of gravity and is conjectured to be true in gravity", so one needs a shorter exterior geodesic.
  SOURCE: R. Bilotta, 2023, "A Traversable Wormhole from the Kerr Black Hole", arXiv preprint 2304.07356, https://arxiv.org/abs/2304.07356
  QUOTE: "we show that a double-trace deformation to the near-horizon, near-extremal region of Kerr yields a traversable wormhole. We also comment on the potential for a fully nonperturbative approach to a four-dimensional rotating traversable wormhole in asymptotically flat space." and "it has been proven that the ANEC holds along achronal geodesics in the absence of gravity [3,4] and is conjectured to be true in gravity [5]."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RF-11] CLAIM: Kontou (2024, Universe 10, 291) reviews wormhole restrictions from quantum energy inequalities. Key framing: the achronal ANEC (free of counterexamples in semiclassical gravity) is sufficient to rule out causality violations in asymptotically flat spacetimes and seems to prohibit shortcut wormholes, but 'long' wormholes (travel through the throat takes longer than outside) have no complete achronal null geodesics through them and so escape it; null QEIs, the smeared null energy condition (SNEC) and double smeared null energy condition (DSNEC) then apply. She applies SNEC and DSNEC to the Maldacena-Milekhin-Popov long wormhole, with the DSNEC constraint stated to be a new result. The DSNEC currently makes sense only in Minkowski space or at scales well below the curvature scale (derived for minimally coupled scalars in flat space). It also describes the old Casimir-plate stabilisation proposal as speculative, with spontaneous production by tunnelling suggested without details.
  SOURCE: E.-A. Kontou, 2024, "Wormhole Restrictions from Quantum Energy Inequalities", Universe 10, 291, https://arxiv.org/abs/2405.05963
  QUOTE: "While the achronal ANEC seems to prohibit wormholes as “shortcuts” 1, a different kind of wormhole still seems possible: the ‘long’ wormhole. This is a wormhole where it takes longer for an observer to travel through the throat than the outside spacetime." and "‘Long’ wormholes circumvent the problem of the achronal ANEC, as there are no complete achronal null geodesics passing through them. In this case, null QEIs could provide restrictions."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-12] CLAIM: The conventional statement of the achronal ANEC crux as of 2024: the ANEC over achronal null geodesics satisfying the semiclassical Einstein equation "is free of counterexamples in semiclassical gravity", and it suffices to exclude causality violations in asymptotically flat spacetimes. This is a review statement (absence of counterexamples), not a proof of the self-consistent version; the proofs exist only in flat space or holographic settings.
  SOURCE: Kontou 2024, Universe 10, 291, https://arxiv.org/abs/2405.05963
  QUOTE: "The ANEC over achronal null geodesics that satisfies the (semiclassical) Einstein equation is free of counterexamples in semiclassical gravity. More importantly, it is sufficient to rule out the existence of causality violations in asymptotically flat spacetimes [6]."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RF-13] CLAIM: The 2022 Nature experiment (Jafferis et al., Nature 612, 51; Sycamore, 9 qubits in the original) ran a teleportation protocol with a Hamiltonian learned by machine learning to mimic a sparse SYK model. Kobrin, Schuster and Yao (2023, preprint) comment that the learned Hamiltonian has seven Majorana fermions with five fully commuting terms, and that (i) it does not thermalize, (ii) the teleportation signal only resembles SYK for the operators used in training, (iii) the perfect size winding is a generic feature of small, fully commuting models and does not persist to larger or non-commuting ones. Evidential status of the critique: arXiv comment, not peer reviewed in a journal as far as found.
  SOURCE: B. Kobrin, T. Schuster, N. Yao, 2023, "Comment on 'Traversable wormhole dynamics on a quantum processor'", arXiv:2302.07897, https://arxiv.org/abs/2302.07897
  QUOTE: "(i) in contrast to these claims, the learned Hamiltonian does not exhibit thermalization; (ii) the teleportation signal only resembles the SYK model for operators that were used in the machine-learning training; (iii) the observed perfect size winding is in fact a generic feature of small-size, fully-commuting models, and does not appear to persist in larger-size fully-commuting models or in non-commuting models at equivalent system sizes."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-14] CLAIM: The authors' reply (Jafferis et al., 2023, arXiv:2303.15423) argues the Kobrin et al. numerics are "consistent" with theirs on two key points (size winding is the mechanism, and the system thermalizes and scrambles at the teleportation time), that the objections concern "counterfactual scenarios outside of the experiment", that all fermions show size winding at 2 <~ t <~ 5 (the claim otherwise is an artifact of analysing only t = 2.8), and that a large added non-commuting term preserves size winding. So the dispute is whether the learned dynamics are "gravitational", not whether the circuit ran. Neither side claims a spacetime wormhole was created; the experiment used a few qubits and teleportation, not a payload through spacetime.
  SOURCE: D. Jafferis et al., 2023, "Comment on 'Comment on Traversable wormhole dynamics on a quantum processor'", arXiv:2303.15423, https://arxiv.org/abs/2303.15423
  QUOTE: "We observe that the comment of Kobrin et al. [1] is consistent with Jafferis et al. [2] on key points: i) the microscopic mechanism of the experimentally observed teleportation is size winding and ii) the system thermalizes and scrambles at the time of teleportation. These properties are consistent with a gravitational interpretation of the teleportation dynamics, as opposed to the late-time dynamics."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-15] CLAIM: A 2026 follow-up (Byun, Kim, Lee, arXiv:2604.10090v2, 24 May 2026) reports a quantum-processor teleportation using a chaotic binary-sparse N = 8 SYK model and describes itself as "the first quantum-hardware realization of the TW protocol driven by an explicitly chaotic Hamiltonian". It states the debate directly: "recent theoretical scrutiny has questioned whether extremely sparse SYK constructions, including the machine-learned Hamiltonian of Ref. [6], faithfully retain the requisite chaotic features". This shows the Sycamore critique is still driving the frontier and that no experiment has yet shown the full gravitational signature at scale. Evidential status: preprint, not yet peer reviewed (as seen); the claim of "first" is the authors'.
  SOURCE: M. Byun, K.-Y. Kim, H. Lee, 2026, "Quantum simulation of traversable-wormhole-inspired quantum teleportation in a chaotic binary sparse SYK model", arXiv:2604.10090, https://arxiv.org/abs/2604.10090
  QUOTE: "To the best of our knowledge, this constitutes the first quantum-hardware realization of the TW protocol driven by an explicitly chaotic Hamiltonian."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RF-16] CLAIM: The same 2026 preprint gives the standard restatement of why the wormhole in these protocols is traversable only because of ANEC violation and not a shortcut in a shared ambient space: the eternal Einstein-Rosen bridge is non-traversable since NEC forbids causal signal transmission between boundaries, and a negative-energy shockwave violating ANEC opens a causal channel; in the large-N limit, this is dual to quantum teleportation. This confirms that the two-sided AdS/SYK constructions compare against the boundary coupling channel, not against a surrounding space (hidden premise 1).
  SOURCE: Byun, Kim, Lee 2026, arXiv:2604.10090, https://arxiv.org/abs/2604.10090
  QUOTE: "A central object in this program is the eternal Einstein–Rosen bridge [8], a wormhole geometry that is classically non-traversable because the null energy con- dition forbids causal signal transmission between its two asymptotic boundaries. However, this restriction can be circumvented: the introduction of a negative-energy shockwave violates the averaged null energy condition (ANEC), thereby opening a causal channel through the wormhole [9]."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RF-17] CLAIM: Shapoval et al. (Quantum 7, 1138, 2023, "Towards Quantum Gravity in the Lab on Quantum Processors") studied the teleportation protocol on quantum processors as a route to quantum-gravity experiments; Weinstein (2023, arXiv:2308.00697) is a commentary on the learned-Hamiltonian debate. Only the INSPIRE entries were read (titles and abstract snippets), so these are pointers, not evidence.
  SOURCE: I. Shapoval et al. 2023, Quantum 7 1138, https://arxiv.org/abs/2205.14081 ; G. Weinstein 2023, https://arxiv.org/abs/2308.00697
  QUOTE: "Recent works have designed a special teleportation protocol that realizes a surprisin…" (abstract snippet as printed by lit_search, truncated)
  ACCESS: abstract
  STATUS: peer-reviewed (Shapoval); preprint (Weinstein)
  CONFIDENCE: low

- [RF-18] CLAIM: Recent holographic work keeps extending double-trace-deformation wormholes (AdS only): Ahn et al. (PRD 109, 066016, 2024) study conserved-current (U(1)) double-trace deformations of black branes; Liu and Miao (arXiv:2501.02324, 2025) study "Traversable Wormhole in AdS and Entanglement". The standard statement in these papers is that a traversable wormhole generally violates the ANEC. All are asymptotically AdS with the coupling between two boundaries as the non-gravitational channel, so none addresses 4D asymptotically flat spacetime. Search summary only.
  SOURCE: Ahn et al. 2024, https://arxiv.org/abs/2206.03434 ; Liu, Miao 2025, https://arxiv.org/abs/2501.02324
  SUMMARY: "Recent work studies traversable wormholes made traversable by a double trace deformation, where coupling the two asymptotic boundaries of a black brane geometry with conserved current operators causes the quantum matter stress-energy tensor to violate ANEC." and "The abstract notes that a traversable wormhole generally violates the averaged null energy condition." (WebSearch model summary)
  ACCESS: search-summary
  STATUS: preprint
  CONFIDENCE: low

- [RF-19] CLAIM: Speculative, fringe-adjacent proposals with classical modified-gravity or Casimir-style supports continue to appear: "Hyperbolic Casimir-like wormhole" (Avalos et al., Eur. Phys. J. C 85, 793, 2025) obtains exact Morris-Thorne-type solutions in hyperbolic symmetry whose Casimir-like stress is negative; "On the wormhole-warp drive correspondence" (Garattini et al., JCAP 08 (2024) 061) embeds a warp drive in a wormhole background by generalising the Natario-Alcubierre definition. Evidential status: classical solution-generating exercises that assume a stress tensor of the required sign; they do not show such a source can be built and do not engage the achronal ANEC or QEIs in the portion read (abstracts only). STATUS: speculative.
  SOURCE: Avalos et al. 2025, https://arxiv.org/abs/2507.17906 ; Garattini et al. 2024, https://arxiv.org/abs/2401.15136
  QUOTE: "In the conventional form of studying wormhole geometry, traversability requires the presence of exotic matter, which also provides negative gravity effects to keep the wormhole throat open. Using hyperbolic symmetry we obtain a solution already provided with negativ…" (abstract snippet, truncated, as printed by lit_search)
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: low

- [RF-20] CLAIM: Bilotta also reviews the 4D nonperturbative construction (Maldacena-Milekhin-Popov): Einstein-Maxwell plus charged massless fermions, where fermion Landau levels in the magnetic field give a 2D CFT whose negative null energy keeps the wormhole open; the interior is unstable to large fluctuations in energy; "this work was later extended to show that by tuning specific parameters in the wormhole, it could be made safe for human travel". This is a secondary description and consistent with the original MMP/MM statements.
  SOURCE: Bilotta 2023, arXiv:2304.07356, https://arxiv.org/abs/2304.07356
  QUOTE: "The wormhole geometry is constructed explicitly in Einstein Maxwell theory plus charged, massless fermions. The fermions provide the negative energy required to keep the wormhole open."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RF-21] CLAIM: Maldacena-Milekhin geometry: the extremal magnetically charged black hole f = (1 - r_e/r)^2 with r_e = sqrt(pi q) l_p / g_4 and M_e = r_e / G_4 (q the integer magnetic charge, g_4 the gauge coupling, l_p = sqrt(G_4), natural units). The near-throat region is a segment of AdS2 x S2 with the sphere of constant radius r_e, joined to the exterior black hole at rho = +/- rho_c. The central claim for size: with large q the magnetic field B = q/(2 r_e^2) is much larger than the inverse sphere size, so the matter theory flows to a 2D CFT with central charge c_2 proportional to the flux. For r_e > 1.5e7 m (RF-05), M_e = r_e c^2/G would be of order 1e34 kg (about 1e4 solar masses) in SI (my arithmetic: r_e c^2/G = 1.5e7 m x 1.35e27 kg/m = 2e34 kg; this is the extremal-mass relation quoted, not a figure printed in the paper). The magnetic charge needed is of order r_e g_4/(sqrt(pi) l_p) elementary Dirac units, astronomically large.
  SOURCE: Maldacena, Milekhin 2021, PRD 103, 066007, https://arxiv.org/abs/2008.06618
  QUOTE: "f = ( 1− re r )2 , r e≡ √πqlp g4 , l p≡ √ G4 , M e = re G4 (2.5) where q is the (integer) magnetic charge and Me the mass at extremality."
  ACCESS: full-text
  STATUS: peer-reviewed (formula); the SI mass conversion is my own arithmetic and should be checked in a calc script
  CONFIDENCE: medium

- [RF-22] CLAIM: Weinbaum (Phys. Rev. D 114, 084004, 2026; arXiv:2607.28738, July 2026; 76 pages) is the newest and most sweeping critique of the Einstein-Dirac(-Maxwell) wormholes. He argues that the BKR/Konoplya-Zhidenko papers "did not properly take into account that single-particle states do not self-interact electromagnetically and that the mode functions of single-particle states are of positive frequency". Two-part result: (a) classical positive-frequency Dirac fields on certain FIXED wormhole geometries can violate ANEC, so the Dirac field is in principle a candidate source; (b) once back-reaction is included in the Einstein-Dirac system and a numerical search is made, the conditions for a reflection-symmetric throat "cannot be satisfied", so no valid traversable solution exists. Scope: classical Dirac field, the Einstein-Dirac system as he formulates it (how far the Maxwell-coupled case is covered was not checked); I read the abstract and the p. 45 summary passage only, not the derivation. It supersedes nothing: it adds a static-existence no-go to Kain's dynamical no-go (RF-01). Whether BKR/Konoplya-Zhidenko have replied is not known (INSPIRE shows 0 citations for it at search time).
  SOURCE: R. J. Weinbaum, 2026, "Obstructions to traversable wormholes in Einstein-Dirac theory", Phys. Rev. D 114, 084004, doi:10.1103/g89c-gqyf; arXiv:2607.28738, https://arxiv.org/abs/2607.28738
  QUOTE: "these works did not properly take into account that single-particle states do not self-interact electromagnetically and that the mode functions of single-particle states are of positive frequency. In this paper, we show that classical, positive-frequency Dirac fields on certain fixed wormhole geometries can violate ANEC, so they are indeed candidates for sourcing traversable wormholes." and (p. 45) "numerical search to argue that the conditions required for a reflection-symmetric wormhole throat cannot be satisfied. These facts together support the conclusion that traversable wormhole solutions do not exist as valid solutions to the Einstein-Dirac equations."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RF-23] CLAIM: Freivogel et al. (arXiv:2606.12528, v2, June 2026; 69 pages) compute low-frequency scattering in the 4D Maldacena-Milekhin-Popov (MMP) wormhole and show traversability depends on the probe. Neutral and charged scalars: on time scales of order the light-crossing time the transmission is parametrically suppressed (most of the signal is reflected or temporarily trapped in the throat), scaling as sigma_r ~ A (omega r_e)^2 with A the mouth area, and at late times the accumulated cross-section approaches half the black-hole absorption cross-section (the trapped signal leaks out through either mouth with about equal probability). There are resonant frequencies with perfect transmission. Charged massless fermions instead traverse "with essentially unit probability at low energies", by a mechanism analogous to the Callan-Rubakov effect. This bears directly on the signal/payload question (Q1, Q3) and hidden premise 10: a scalar signal through the MMP throat is mostly reflected at low frequency, a fermion is not. Scope: the MMP wormhole with its test-field approximation (no back-reaction of the probe); the 2018 Freivogel et al. information-bound paper is a different paper.
  SOURCE: B. Freivogel et al., 2026, "How traversable is a traversable wormhole?", arXiv:2606.12528 (preprint), https://arxiv.org/abs/2606.12528
  QUOTE: "On time scales of order the light-crossing time after sending in a signal, the transmission is parametrically suppressed, with most of the incoming signal reflected or temporarily trapped inside the wormhole throat. As time progresses, the trapped signal gradually leaks out, so that at late times the accumulated transmission cross-section approaches one half of the corresponding black hole absorption cross-section." and "Charged massless fermions tell a very different story. Unlike scalars, they traverse the wormhole with essentially unit probability at low energies."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-24] CLAIM: Sadhukhan (arXiv:2609.33511, Sept 2026; arXiv:2610.09847, Oct 2026 - the second has an arXiv number of October 2026 and so is newer than 2026-10-01) studies linear stability of the MMP wormhole, previously only argued. Paper 1 (polar metric / axial gauge sector): the throat equations are "consistent only if the fermions respond to the perturbation", computed from the 2D conformal anomaly including the trace part "that MMP discard", and this response must come with an induced Hall current. Paper 2 (axial metric / polar gauge sector): the lowest-Landau-level fermions respond with the exact Schwinger current, giving the electric field a screening mass; within the O(alpha) truncation "the sector has no growing mode for l>=2". These are the first sector-by-sector linear-perturbation analyses of the 4D quantum-supported throat found, with stability results so far in the two sectors treated; the full perturbation problem is not complete in what I read, and the rest of the abstract of paper 1 (text after "With both effects included") was not read. Scope: linear, MMP background with q >> 1 and l << sqrt(q); assumes only the lowest Landau level responds. Single-author preprints, not refereed.
  SOURCE: A. Sadhukhan, 2026, "Polar-metric/axial-gauge perturbations of the Maldacena-Milekhin-Popov wormhole", arXiv:2609.33511 (preprint), https://arxiv.org/abs/2609.33511 ; "Axial-metric/polar-gauge perturbations of the Maldacena-Milekhin-Popov wormhole", arXiv:2610.09847 (preprint), https://arxiv.org/abs/2610.09847
  QUOTE: "We show that the throat equations are consistent only if the fermions respond to the perturbation, computed exactly from the two-dimensional conformal anomaly with the full stress tensor including the trace part that MMP discard. This response must be accompanied by an induced Hall current of the fermions." (2609.33511) and "Within theO(α) truncation the sector has no growing mode forl≥2." (2610.09847, p. 30)
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RF-25] CLAIM: Kanai et al. (Phys. Rev. D 113, 064026, 2026; arXiv:2511.21017) recast wormholes as perturbations of near-horizon geometries of near-extremal Reissner-Nordstrom black holes (4D) and equal-angular-momenta Myers-Perry black holes (5D). With negative Casimir energy as the source this reproduces MMP. They then prove a no-go: such perturbative constructions "cannot be realized within the effective field theory approach to higher-derivative corrections", irrespective of the form of the correction terms, because enhanced near-horizon symmetries constrain the effective energy-momentum tensor so as to prevent a traversable throat. Bears on hidden premise 3 and on the Einstein-Gauss-Bonnet / f(R) route in the brief: higher-derivative gravity corrections alone cannot hold open an MMP-type throat in this near-horizon perturbative setting; the negative energy must be a Casimir (quantum matter) source. Scope: perturbation around the near-horizon geometries named; the abstract I read ends mid-sentence ("prevents the formation of the traversable throat structur...").
  SOURCE: T. Kanai et al., 2026, "Wormholes as perturbations of near-horizon black hole geometries: No-go theorems within effective field theories", Phys. Rev. D 113, 064026, doi:10.1103/dsnv-gq47; arXiv:2511.21017, https://arxiv.org/abs/2511.21017
  QUOTE: "We then show that, in contrast, such perturbative constructions cannot be realized within the effective field theory approach to higher-derivative corrections. Remarkably, this conclusion holds irrespective of the specific form of the correction terms. The key observa- tion is that the enhanced symmetries in the near-horizon region severely constrain the effective energy–momentum tensor near the throat."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RF-26] CLAIM: Mondal et al. (arXiv:2511.22671, Nov 2025) compute scalar and gauge-field perturbations of the MMP wormhole as test fields. The throat is "astronomically" long in the tortoise coordinate: the throat contributes J ~ pi L_wh/2 ~ 2.2e35 in r_* (units of the problem, presumably geometric/natural; the paper's mouths have barriers only O(10^2) wide), with two photon-sphere barriers peaked at r = 2 r_e separated by a field-free cavity; direct time-domain evolution would need ~1e33 grid points, so they use Numerov scattering amplitudes and sum echo trains and cavity quasinormal modes. For the classic "echoes" test (Q4) this means the MMP wormhole produces echoes after a delay set by the enormous tortoise length of the throat, not by the 0.05 s light-crossing time of the humanly-sized mouth. The numerical echo delay and amplitude were not read; the preprint's own quantity is the tortoise-coordinate cavity width.
  SOURCE: R. Mondal et al., 2025, "Echoes of the Maldacena-Milekhin-Popov traversable wormhole", arXiv:2511.22671 (preprint), https://arxiv.org/abs/2511.22671
  QUOTE: "In the tortoise coordinate these two barriers are onlyO(10 2) wide but sit a distance 2D≃πL wh∼10 35 apart, which puts direct time-domain evolution out of reach."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RF-27] CLAIM: Lu, Yang and Zheng (arXiv:2603.26051, March 2026) cast the Gao-Jafferis-Wall (GJW) protocol in AdS2 as a quantum channel and compute its quantum channel capacity: it is governed by the time derivative of an out-of-time-ordered correlator (operator size growth), is bounded above by the Einstein-gravity limit through the chaos bound, and gives "a natural benchmark for quantum simulations of traversable wormholes". Their rough bound on information transfer is the number of transmitted phi particles, |p+| Delta p+ ~< |a+| / G_N ~ g, and they note the protocol is "one-shot". This is the newest quantitative statement of how much information a GJW wormhole passes (hidden premise 10, Q3), in AdS2 only; stringy corrections give submaximal chaos and slower growth. Direct bearing on hidden premise 1: the channel is evaluated with the double-trace coupling, i.e. the boundary channel the brief says to compare against. Not 4D flat.
  SOURCE: J. Lu, Z. Yang, J. Zheng, 2026, "Quantum Channel Capacity of Traversable Wormhole", arXiv:2603.26051 (preprint), https://arxiv.org/abs/2603.26051
  QUOTE: "We show that this capacity is governed by the time derivative of an out-of-time-ordered correlator, hence by operator size growth in the holographic dual, and that its growth is bounded above by the Einstein gravity limit. The channel capacity therefore provides a natural benchmark for quantum simulations of traversable wormholes."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RF-28] CLAIM: Djogama et al. (arXiv:2605.05011, May 2026) construct the double-trace-deformation traversable wormhole in the two-sided near-horizon, near-extremal Kerr background with FERMION fields (all earlier double-trace constructions used bosons), within Kerr/CFT. Together with Bilotta's boson version (RF-10) this is the second Kerr-based construction; both are perturbative, two-sided, coupling two boundaries, and neither addresses a 4D asymptotically flat nonperturbative solution or the achronal-ANEC shortcut test. Abstract only was read.
  SOURCE: M. Z. Djogama et al., 2026, "Kerr/CFT Traversable Wormhole with Fermionic Double-Trace Deformation", arXiv:2605.05011 (preprint), https://arxiv.org/abs/2605.05011
  QUOTE: "The construction of a traversable wormhole with double-trace deformation has been achieved so far by using boson fields as the perturbation. In this work, we study double-trace deformation with fermion fields in the two-sided Kerr background to open a traversable wormhole."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-29] CLAIM: Two 2026 preprints challenge the standard "local NEC violation = negative ANEC" reading. Chakrabarti (arXiv:2609.39468, Sept 2026) argues that the volume-integrated null energy of a traversable wormhole "can even be positive" even though the pointwise NEC is violated at the throat, and proposes a classification by the global integrated measure. This is a classical Morris-Thorne-type statement about a volume integral, not the ANEC line integral along the throat geodesic, so it does not conflict with the Hochberg-Visser result; hidden premise 2 asks that the two be kept apart. Pastén et al. (Class. Quantum Grav. 43, 115014, 2026; arXiv:2602.00524) formulate traversability as a local covariant null-defocusing condition from the Raychaudhuri equation and prove that unimodular gravity, which preserves local causal structure, cannot support traversable wormholes without the same violation. Abstract-level reading only for both.
  SOURCE: S. Chakrabarti, 2026, "Global Integrated Null Energy Contribution: Classification of Traversable Wormholes", arXiv:2609.39468 (preprint), https://arxiv.org/abs/2609.39468 ; E. Pastén et al., 2026, "Null Raychaudhuri equation and the impossibility of traversable wormholes in unimodular gravity", Class. Quantum Grav. 43, 115014, doi:10.1088/1361-6382/ae73df; arXiv:2602.00524, https://arxiv.org/abs/2602.00524
  QUOTE: "We argue that the local violation of null energy condition at the throat of a traversable wormhole does not necessarily indicate that the total volume integrated null energy contribution is negative. It is already known that it can be arbitrarily close to zero. We show that it can even be positive" (Chakrabarti) ; "We formulate wormhole traversability as a purely local and covariant null defocusing condition derived from the Raychaudhuri equation, independently of any specific metric ansatz." (Pastén et al., abstract as printed by lit_search)
  ACCESS: abstract
  STATUS: preprint (Chakrabarti); peer-reviewed (Pastén et al.)
  CONFIDENCE: medium

- [RF-30] CLAIM: Junior et al. (arXiv:2608.08208, Aug 2026) build "black bounce" solutions in GR sourced by a canonical scalar non-minimally coupled to linear electrodynamics in which the regular black hole or traversable wormhole "is supported by ordinary bulk matter, with the necessary exoticity confined to an infinitesimally thin defect at the bounce". This restates the standard result: the NEC violation is not removed but concentrated in a thin shell (a thin-shell wormhole in effect), so it is not a "no negative energy" construction. Blázquez-Salcedo et al. (arXiv:2607.18399, July 2026) give nonradial quasinormal-mode spectra for charged Ellis-Bronnikov wormholes supported by a phantom scalar (classical exotic matter) in Einstein-Maxwell theory. Abstract-level reading only.
  SOURCE: E. L. B. Junior et al., 2026, "Black bounce sourced by non-minimally coupled linear electrodynamics and a canonical scalar field through a thin shell at the throat", arXiv:2608.08208 (preprint), https://arxiv.org/abs/2608.08208 ; J. L. Blázquez-Salcedo et al., 2026, "Nonradial perturbations of static charged wormholes", arXiv:2607.18399 (preprint), https://arxiv.org/abs/2607.18399
  QUOTE: "establishing a self-consistent framework in which regular black holes and traversable wormholes are supported by ordinary bulk matter, with the necessary exoticity confined to an infinitesimally thin defect at the bounce." (Junior et al., abstract as printed by lit_search)
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RF-31] CLAIM: Carried from the warp-drive run, narrowed to its bearing on wormholes: An T. Le (arXiv:2602.18023, v6, 2026) gives an observer-robust test for the null, weak and strong energy conditions that uses the S-lemma to write each as a 4x4 linear matrix inequality, requiring "neither Hawking-Ellis classification nor a rapidity cutoff". The method is for any stress tensor, so it could be applied to a Morris-Thorne or thin-shell throat to certify the NEC violation for all null directions; Le applies it to warp bubbles only, and this run has not applied it to a wormhole. Preprint with several large revisions.
  SOURCE: A. T. Le, 2026, "Observer-robust energy condition verification for warp drive spacetimes", arXiv:2602.18023v6 (preprint), https://arxiv.org/abs/2602.18023
  QUOTE: "We use the classical S-lemma to express the null, weak, and strong conditions as $4\times4$ linear matrix inequalities; the dominant condition requires two such tests. These criteria require neither Hawking-Ellis classification nor a rapidity cutoff."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RF-03; re-verified (only the sentences quoted here; the earlier claim's "global bounds establish NEC violation in all four bubble walls" and the 73% figure are warp-specific and are not carried)

## Index by date (newest first; arXiv number gives the month of first posting)
- Oct 2026: RF-24 (Sadhukhan, axial-metric/polar-gauge MMP stability, arXiv:2610.09847). The only item found dated after 2026-10-01.
- Sep 2026: RF-24 (Sadhukhan 2609.33511), RF-29 (Chakrabarti 2609.39468). Mizutani et al. 2609.24159 (gravitating chiral quark soliton, Einstein-Dirac) appeared in the citing list of BKR and was not read.
- Aug 2026: RF-30 (Junior et al. 2608.08208).
- Jul 2026: RF-22 (Weinbaum 2607.28738, PRD 114 084004), RF-30 (Blazquez-Salcedo et al. 2607.18399).
- Jun 2026: RF-23 (Freivogel et al. 2606.12528).
- May 2026: RF-28 (Djogama et al. 2605.05011), RF-15/16 (Byun, Kim, Lee 2604.10090 v2, 24 May 2026).
- Mar 2026: RF-27 (Lu, Yang, Zheng 2603.26051).
- Feb 2026: RF-29 (Pastén et al. 2602.00524), RF-31 (Le 2602.18023).
- 2025: RF-26 (Mondal et al. 2511.22671, Nov), RF-25 (Kanai et al. 2511.21017, Nov; PRD 113 in 2026), RF-19 (Avalos et al., EPJC 85 793), RF-18 (Liu, Miao 2501.02324).
- 2024: RF-11/12 (Kontou), RF-18 (Ahn et al.), RF-19 (Garattini et al.).
- 2023: RF-01/02 (Kain), RF-10/20 (Bilotta), RF-13/14 (Kobrin et al. and reply), RF-17.
- 2021-2022: RF-03 (Konoplya, Zhidenko 2022), RF-04, RF-05..07 and RF-21 (Maldacena-Milekhin 2021), RF-09 (Emparan et al. 2021).

## Gaps
- Update 2026-10-08: Weinbaum (RF-22) is the follow-up after Kain that I had not found at first pass; no reply by Blazquez-Salcedo, Knoll, Radu or Konoplya-Zhidenko to Kain or Weinbaum was found (INSPIRE citing list of arXiv:2010.07317 showed 8 recent hits, none a reply). Weinbaum's p. 45 conclusion rests on a derivation I did not check; the critiques facet should read sections III-V before relying on it.
- The only item dated after 2026-10-01 is Sadhukhan's second MMP paper (RF-24). No new energy-condition or achronal-ANEC theorem was found that postdates 2026-10-01. Nothing from the warp run postdates 2026-10-01 either.
- Warp-run items deliberately not carried because they are warp-only: Natario/Rodal/Bolivar et al. bubble results, Le's radiative steering and elastic shells, Barzegar et al.'s theorems (Theorem IV.32 is about the Natario drive). Clough-Dietrich-Khan (2024) numerical evolution of an NEC-violating warp spacetime is a possible methodological analogue for evolving a throat; not re-verified, not carried.
- Earlier gap, now partly filled: previously "no published follow-up after Kain (2023)"; see Weinbaum above. Konoplya-Zhidenko's asymmetric smooth solutions were the only post-BKR static fix found at first pass; their dynamical stability is exactly what Kain tested, and Weinbaum's static no-go (RF-22) now bears on them too (his treatment of the asymmetric branch was not read).
- Not searched this relaunch: microlensing, EHT, gravitational-wave echo and magnetic-monopole constraints (engineering facet's remit).
- No 2023-2026 paper found that proves or refutes the self-consistent achronal ANEC in 4D gravity; the only items found are Kontou 2024's review statement and Bilotta's restatement. Not found: a 2025-2026 update to Freivogel et al. or Maldacena-Stanford-Yang bounds on information through traversable wormholes (arXiv rate-limited during those searches).
- arXiv API returned HTTP 429 for several queries (MMP follow-ups, Kerr/dark sector), so the sweep of 2024-2026 hep-th preprints is incomplete.
- No quantum-hardware wormhole experiment other than Jafferis 2022 (Google Sycamore) and Byun 2026 found; I did not confirm any trapped-ion or Quantinuum realisation, nor the Brown et al. "Quantum gravity in the lab" teleportation-by-size paper (not opened).
- No astronomical observation or lab experiment results (microlensing, EHT, echoes, monopole searches) were collected: outside this facet's quoted evidence, apart from RF-04's model-prediction papers.
- The Casimir-plate stabilisation mechanism of Kontou's ref [73] was only seen as a one-sentence description; the original source was not identified here.
- Not verified: the SI mass for the Maldacena-Milekhin human-sized wormhole (RF-21) needs a calc script; I did not run one.
