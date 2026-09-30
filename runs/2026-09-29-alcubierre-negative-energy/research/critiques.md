# Research: critiques
Mandate: objections, no-go theorems, instabilities, failed or debunked proposals, and conflicting results on Alcubierre-type warp drives
Access: lit_search INSPIRE ok, arXiv ok (many queries returned only INSPIRE hits); WebFetch not used; WebSearch used once (White 2021 lookup); arXiv PDFs read via fetch_text.py

Conventions: G = c = 1 unless a claim says SI. "Eulerian" = observers normal to the t = const slices. Delta conventions are stated per claim. Numbers marked (ours) are conversions by this researcher, not in the source.

## Claims
- [RC-01] CLAIM: Santiago, Schuster and Visser (2022) argue that the three 2021 positive-energy papers (Lentz; Bobrick-Martire; Fell-Heisenberg) only assert positivity of the energy density for one family of observers (co-moving Eulerian), which does not establish the weak energy condition (WEC), because WEC needs every timelike observer to measure rho >= 0. Their own conclusion is that, within the framework adopted by those papers, all physically reasonable warp drives violate the WEC and the strong and dominant energy conditions, and under plausible subsidiary conditions the NEC too. Scope: classical GR; the framework is Natario-class (unit lapse, flat spatial slices, Minkowski exterior). It is not a proof about Bobrick-Martire shells with non-flat slicing in general.
  SOURCE: Santiago, Schuster, Visser 2022, "Generic warp drives violate the null energy condition", Phys. Rev. D 105, 064038, arXiv:2105.03079, https://arxiv.org/pdf/2105.03079
  QUOTE: "These claims are at best incomplete, since the arguments as presented only assert but do not prove the existence of one set of timelike observers, the co-moving Eulerian observers, who see relatively "nice" physics. While these particular observers might arguably see a positive energy density, the WEC requires all timelike observers to see positive energy density."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-02] CLAIM: Santiago et al. give an explicit mechanism for why Eulerian positivity does not imply WEC: a stress-energy with rest-frame density rho0 > 0 and Gamma > 1 is seen with density rho0 gamma^2 (1 - Gamma^2 v^2) by an observer moving at speed v, which is negative for |v| > 1/Gamma (subluminal observers). They add that for a zero-vorticity drive (Hawking-Ellis type I), non-negative Eulerian density plus the NEC implies WEC, so checking rho >= 0 alone is insufficient and the NEC must also be checked.
  SOURCE: Santiago, Schuster, Visser 2022, arXiv:2105.03079, https://arxiv.org/pdf/2105.03079
  QUOTE: "For a suﬃciently rapidly moving but still subluminal observer, with |v| > 1/Γ, the energy density will be seen to be negative. So in this example the WEC is violated."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-03] CLAIM: Santiago et al. show Natario zero-expansion drives violate the NEC: rho + p-bar = -(1/8pi) tr(K^2) <= 0, strictly negative in any non-trivial case. They cite Natario's theorem 1.7 that any generic warp spacetime of this class violates either the SEC or the WEC (with Minkowski as the trivial exception), say it also covers Lentz/Fell-Heisenberg zero-vorticity drives, and sharpen it to "there must be violations of the SEC". Scope: unit-lapse, flat-slice warp metrics with asymptotic falloff to Minkowski.
  SOURCE: Santiago, Schuster, Visser 2022, arXiv:2105.03079, https://arxiv.org/pdf/2105.03079
  QUOTE: "ρ + ¯p =− 1 8π tr ( K 2) ≤ 0. (7.9) And the same non-triviality argument again shows that any Nat´ ario zero-expansion warp drive also violates the NEC." and "in any generic warp spacetime, (Alcubierre, Nat´ ario zero-expansion, and, yes, it even applies to Lentz/Fell–Heisenberg zero-vorticity warp drives), there must be violations of either the SEC or the WEC."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-04] CLAIM: What each 2021 paper actually checks, per Santiago et al.: all agree on the Eulerian density rho = G_nn/8pi = (1/16pi)(K^2 - tr K^2); Lentz and Fell-Heisenberg try to force it positive; Bobrick-Martire compute only it. Fell-Heisenberg's "hidden geometric structure" is the identity K^2 - tr(K^2) = 2 tr cof(K_ij), which Santiago et al. call "less useful than one might hope". They say all three should also compute the stresses T_ij.
  SOURCE: Santiago, Schuster, Visser 2022, arXiv:2105.03079, https://arxiv.org/pdf/2105.03079
  QUOTE: "(Everyone agrees with this. This is the quantity that Lentz [1] and Fell–Heisenberg [3] eventually try to force to be positive. This is the only quantity Bobrick–Martire [ 2] explicitly calculate.)" and "What Lentz [1], and Bobrick–Martire [ 2], and Fell–Heisenberg [3] should be doing is to also calculate all of the stress components Tij."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-05] CLAIM: Lentz's reply (2022 proceedings summary) to Santiago et al. is that their divergence-theorem argument (Eulerian energy of a Natario-class soliton = total divergence + a negative-definite vorticity term, (1/16pi)[d_i(N^i d_j N^j - N^j d_j N^i) - (1/2) omega_i omega^i], so total Eulerian energy is non-positive) "does not hold" for his soliton because his Eulerian density is not smooth at the x = 0 and y = 0 boundaries where stress-energy sources are placed. He himself lists as remaining challenges to autonomous superluminal travel "the dominant energy condition, horizons, and the identification of a creation mechanism". Status: author's own defence; the boundary-source loophole is the disputed point.
  SOURCE: Lentz 2023 (Marcel Grossmann 16 proceedings), "Hyper-fast positive energy warp drives", arXiv:2201.00652, https://arxiv.org/pdf/2201.00652
  QUOTE: "This argument does not hold in the case of Lentz 2021 19 as the Eulerian energy density of the example positive energy soliton is smooth save for the boundaries x = 0 and y = 0" and "Remaining challenges to autonomous superluminal travel, such as the dominant energy condition, horizons, and the identiﬁcation of a creation mechanism are also discussed."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RC-06] CLAIM: Celmaster and Rubin (2025 preprint, 79 pp.) claim that Lentz's warp drive does not satisfy the WEC: direct calculation of the Eulerian energy-momentum tensor finds regions of negative energy density; they identify several derivation errors in Lentz's paper; a modified Lentz geometry that respects Lentz's stated equalities and inequalities "still violates the WEC even in the Eulerian reference frame". This is the strongest published rebuttal specific to Lentz, but it is a preprint (no journal reference on the INSPIRE listing).
  SOURCE: Celmaster and Rubin 2025, "Violations of the Weak Energy Condition for Lentz Warp Drives", arXiv:2511.18251, https://arxiv.org/pdf/2511.18251
  QUOTE: "We demonstrate that Lentz's claim is incorrect. We begin with a direct calculation of the energy-momentum tensor of Lentz's warp drive in a Eulerian reference frame, and show that there are spacetime regions where the energy density is negative. We then examine the theoretical basis of Lentz's investigation and identify several derivation errors."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RC-07] CLAIM: Rodal (2026, Gen. Relativ. Gravit. 58) builds a fully explicit irrotational (zero-vorticity) warp drive with unit lapse and flat slices, globally Hawking-Ellis Type I, and reports it reduces but does not eliminate WEC/NEC violation: peak proper-energy deficit reduced by a factor about 38 relative to Alcubierre and about 2.6e3 relative to Natario (at identical profile parameters as stated in the paper, which I did not reproduce), peak NEC violation more than 60 times smaller than Natario. The title says "predominantly positive", not "positive": it is consistent with Santiago et al.'s no-go, not a counterexample.
  SOURCE: Rodal 2026, "A warp drive with predominantly positive invariant energy density and global Hawking-Ellis Type I", Gen. Relativ. Gravit. 58, 1, arXiv:2512.18008, https://arxiv.org/pdf/2512.18008
  QUOTE: "solution exhibits significantly reduced local NEC/WEC stress: its peak proper–energy deficit is reduced by a factor of ≈38 relative to Alcubierre and ≈2.6×10 3 relative to Nat´ ario, and its peak NEC violation is more than 60× smaller than Nat´ ario."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RC-08] CLAIM: Olum (1998) proves, for a definition of superluminal travel as a path faster than any neighbouring null path (with no conjugate points), that the WEC must fail somewhere, i.e. negative energy is required. In its worked example a Casimir plate pair gives T_ab = (pi^2/720 d^4) diag(-1,1,1,-3) and R_ab K^a K^b = -2 pi^3/(45 d^4) for a null geodesic normal to the plates (plate separation d; natural units), so Casimir negative energy can indeed advance a null ray. Scope: needs his definition of "superluminal"; it is a definitional theorem about effective speed relative to neighbouring null paths in a non-flat spacetime with a global null congruence. Baird (RC-17) disputes its reach.
  SOURCE: Olum 1998, "Superluminal travel requires negative energies", Phys. Rev. Lett. 81, 3567, arXiv:gr-qc/9805003, https://arxiv.org/pdf/gr-qc/9805003
  QUOTE: "I investigate the relationship between faster-than-light travel and weak-energy-condition violation, i.e., negative energy densities. In a general spacetime it is difficult to define faster-than-light travel, and I give an example of a metric which appears to allow superluminal travel, but in fact is just flat space." and "The electromagnetic stress-energy tensor between the plates is Tab = π 2 720d4 diag(−1, 1, 1, −3)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-09] CLAIM: Visser, Bassett and Liberati (2000, perturbative) show in linearised gravity that the NEC forces light cones to contract (Shapiro delay is always a delay), so "effective" superluminal travel by tipping light cones is always associated with NEC violation. Scope: perturbative around Minkowski; not a non-perturbative theorem (the non-perturbative extension is Olum's and Santiago et al.'s).
  SOURCE: Visser, Bassett, Liberati 2000, "Superluminal censorship", Nucl. Phys. B Proc. Suppl. 88, 267, arXiv:gr-qc/9810026, https://arxiv.org/pdf/gr-qc/9810026
  QUOTE: "We argue that "effective" superluminal travel, potentially caused by the tipping over of light cones in Einstein gravity, is always associated with violations of the null energy condition (NEC). This is most easily seen by working perturbatively around Minkowski spacetime, where we use linearized Einstein gravity to show that the NEC forces the light cones to contract (narrow)."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-10] CLAIM: Pfenning and Ford (1997) apply the Ford-Roman quantum inequality to the Alcubierre metric: the bubble wall thickness is only a few hundred Planck lengths (Delta <= 10^2 v_b L_Planck for their sampling parameter alpha = 1/10, Pfenning-Ford Delta convention, v_b in units of c), and for R = 100 m the total negative energy is E <= -6.2e70 v_b L_Planck ~ -6.2e65 v_b grams, i.e. about -6.2e62 v_b kg (ours: 1 g = 1e-3 kg), which they express as about 3e20 galaxy masses times v_b. Scope: free-field, flat-space quantum inequality applied where the wall is treated as locally flat; result depends on the sampling-time assumption.
  SOURCE: Pfenning and Ford 1997, "The unphysical nature of 'warp drive'", Class. Quantum Grav. 14, 1743, arXiv:gr-qc/9702026, https://arxiv.org/pdf/gr-qc/9702026
  QUOTE: "It will be shown that the bubble wall thickness is on the order of only a few hundred Planck lengths. Then we will show that the total integrated energy density needed to maintain the warp metric with such thin walls is physically unattainable." and "E ≤ −6. 2 × 1070 vb LPlanck ∼ − 6. 2 × 1065 vb grams. (29)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-11] CLAIM: The Pfenning-Ford trade-off between speed and energy: raising the bubble speed thickens the allowed wall (Delta <= 10^2 v_b L_Planck) but the required negative energy rises in proportion to v_b ("for every order of magnitude by which the velocity increases, the total negative energy required ... also increases by the same magnitude"), so the drive stays out of reach for any v_b. This is the paper's own scaling in the Planck-thin-wall regime, not the E ~ v^2 R^2/Delta scaling at fixed Delta.
  SOURCE: Pfenning and Ford 1997, arXiv:gr-qc/9702026, https://arxiv.org/pdf/gr-qc/9702026
  QUOTE: "One might note that by making the velocity of the bubble, vb, very large then we can make the walls thicker, however this causes another problem. For every order of magnitude by which the velocity increases, the total negative energy required to generate the warp metric also increases by the same magnitude."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-12] CLAIM: Van Den Broeck (1999) reduces the total negative mass from the Pfenning-Ford figure to a few solar masses, but only by a geometry whose ship-carrying pocket hangs on a microscopic neck: his numbers are alpha = 1e17, Delta-tilde = 1e-15 m, R-tilde = 1e-15 m, R = 3e-15 m (femtometre-scale outer bubble, with a ~100 m interior volume via the huge spatial expansion factor), positive energy in the wall region 4.9e30 kg (~2.5 M_sun, ours: /1.989e30), and the wall is kept above about ten Planck lengths of curvature radius. It relies on Pfenning-Ford's bound Delta <= 10^2 v_s L_P and on the free-field Ford-Roman inequality; it inherits horizon, control and semiclassical objections. Both the smaller negative energy and the comparable positive energy (a few M_sun each) are needed.
  SOURCE: Van Den Broeck 1999, "A 'warp drive' with more reasonable total energy requirements", Class. Quantum Grav. 16, 3973, arXiv:gr-qc/9905084, https://arxiv.org/pdf/gr-qc/9905084
  QUOTE: "A spacetime is presented for which the total negative mass needed is of the order of a few solar masses, accompanied by a comparable amount of positive energy." and "We will choose the following numbers for α , ˜∆, ˜R, and R: α = 10 17, ˜∆ = 10 −15 m, ˜R = 10 −15 m, R = 3 × 10−15 m." and "The amount of positive energy in the region w > 0. 981 is EII, + = 4. 9 × 1030kg."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-13] CLAIM: Everett and Roman (1997) state the horizon objection: an observer at the centre of the Alcubierre bubble is causally separated from the outer bubble wall, so cannot create a bubble on demand or control one. Their Krasnikov-tube fix removes that objection, but the one-way trip time cannot be shortened; only the round-trip time as measured by Earth clocks can be made arbitrarily short. The tube still needs negative energy density. Krasnikov (1998) reaches the same time-shortening limit under stated assumptions.
  SOURCE: Everett and Roman 1997, "A superluminal subway: the Krasnikov tube", Phys. Rev. D 56, 2100, arXiv:gr-qc/9702049, https://arxiv.org/pdf/gr-qc/9702049 ; Krasnikov 1998, "Hyperfast travel in general relativity", Phys. Rev. D 57, 4760, arXiv:gr-qc/9511068
  QUOTE: "The "warp drive" metric recently presented by Alcubierre has the problem that an observer at the center of the warp bubble is causally separated from the outer edge of the bubble wall. Hence such an observer can neither create a warp bubble on demand nor control one once it has been created." (Everett-Roman); "It is argued that under some reasonable assumptions in globally hyperbolic spacetimes the traveller cannot hasten reaching the destination." (Krasnikov)
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-14] CLAIM: Hiscock (1997) computed <T_mu nu> of a free conformally invariant scalar field in a 2D reduction of the Alcubierre spacetime and found the stress-energy diverges if the apparent velocity exceeds the speed of light; he concluded that if this persists in four dimensions, engineering warp drive behaviour would be implausible even for an arbitrarily advanced civilization. Scope: 2D reduction, one conformal scalar, a static (Boulware-like) vacuum choice, which Finazzi et al. later argue is not what dynamical formation selects.
  SOURCE: Hiscock 1997, "Quantum effects in the Alcubierre warp drive spacetime", Class. Quantum Grav. 14, L183, arXiv:gr-qc/9707024, https://arxiv.org/pdf/gr-qc/9707024
  QUOTE: "The stress-energy is found to diverge if the apparent velocity of the spaceship exceeds the speed of light. If such behavior occurs in four dimensions, then it appears implausible that "warp drive" behavior in a spacetime could be engineered, even by an arbitrarily advanced civilization."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-15] CLAIM: Finazzi, Liberati and Barcelo (2009), for a superluminal bubble formed dynamically from Minkowski space: (a) an observer at the bubble centre sees a thermal flux of Hawking particles at T_H = kappa/2pi, generically "extremely high" if the exotic matter comes from a quantum field obeying quantum inequalities; (b) the renormalized stress-energy tensor (RSET) grows exponentially in time near and on the front (white-horizon) wall, with backreaction becoming strong within a time of order 1/kappa after the white horizon forms, so the geometry is unstable against semiclassical backreaction. Scope: 2D scalar-field model with a regular formation history; the authors note the Cauchy-horizon divergence would be avoided if the superluminal drive were sustained only for a finite time.
  SOURCE: Finazzi, Liberati, Barcelo 2009, "Semiclassical instability of dynamical warp drives", Phys. Rev. D 79, 124017, arXiv:0904.0141, https://arxiv.org/pdf/0904.0141
  QUOTE: "On one side, an observer located at the center of a superluminal warp-drive bubble would generically experience a thermal flux of Hawking particles. On the other side, such Hawking flux will be generically extremely high if the exotic matter supporting the warp drive has its origin in a quantum field satisfying some form of quantum inequalities. Most of all, we find that the RSET will exponentially grow in time close to, and on, the front wall of the superluminal bubble. Consequently, one is led to conclude that the warp-drive geometries are unstable against semiclassical backreaction."  Also: "In a very short time after the white horizon is formed (of the order of 1/κ ), the backreaction of the RSET in this region of spacetime is no longer negligible but rather very strong."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-16] CLAIM: Lobo and Visser (2004) verify the non-perturbative energy-condition violation of Alcubierre and Natario drives and then show the NEC is violated everywhere even in the weak-field, slow (v << c) limit: G_tt + sum_i G_ii = -2 Tr(K^2) < 0 with K = O(v). The negative-energy requirement therefore persists to arbitrarily low bubble speed and is not a purely superluminal effect. Scope: Alcubierre and Natario metrics (flat slices, unit lapse).
  SOURCE: Lobo and Visser 2004, "Fundamental limitations on 'warp drive' spacetimes", Class. Quantum Grav. 21, 5871, arXiv:gr-qc/0406083, https://arxiv.org/pdf/gr-qc/0406083
  QUOTE: "But from Appendix B we have Gˆtˆt + ∑ ˆı Gˆıˆı = −2Tr(K 2) (28) which is manifestly negative, and so the NEC is violated everywhere. Note that K is O(v) and so we again see that the NEC violations persist to arbitrarily low warp bubble velocity."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-17] CLAIM: Bobrick and Martire (2021) themselves concede: negative energy is "a general property of any superluminal drive (Olum 1998, Visser et al. 2000)"; superluminal motion allows closed timelike loops and violates the NEC; superluminal bubbles have black-hole-like and white-hole-like horizons and the quantum instabilities of Finazzi et al. Their positive-energy result is only "the first general model for subluminal positive-energy, spherically symmetric warp drives"; for superluminal drives they claim only solutions that "satisfy quantum inequalities". They further say any warp drive "is a shell of regular or exotic material moving inertially", so needs propulsion, and no self-consistent solution self-accelerates from rest. So the Bobrick-Martire "positive-energy" drive is subluminal, and the shell-plus-propulsion picture answers hidden premise 6 negatively for present solutions.
  SOURCE: Bobrick and Martire 2021, "Introducing physical warp drives", Class. Quantum Grav. 38, 105009, arXiv:2102.06824, https://arxiv.org/pdf/2102.06824
  QUOTE: "Although negative energy densities are a general property of any superluminal drive (Olum 1998, Visser et al. 2000), the energy density is also negative at subluminal speeds for the Alcubierre drive, even in the weak-ﬁeld approximation (Lobo & Visser 2004)." and "We present the ﬁrst general model for subluminal positive-energy, spherically symmetric warp drives; construct superluminal warp- drive solutions which satisfy quantum inequalities" and "Generally, there are no self- consistent warp drive solutions proposed in the literature which can self-accelerate at all from zero velocities, not to mention gain superluminal speeds."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-18] CLAIM: Fell and Heisenberg (2021) state that the classical superluminal solitons require negative energy densities and that the Alcubierre soliton has horizons rendering it uncontrollable; they claim a superluminal soliton with positive semi-definite Eulerian energy, with example total energy requirements "four orders of magnitude smaller than the solar mass" (about 2e26 kg by our conversion; i.e. of order 0.1 Jupiter mass; their example parameters not reproduced here). The claim is about Eulerian positivity; Santiago et al. (RC-01 to RC-04) show that this does not deliver WEC or NEC. Their abstract says "within a certain subclass", so the claim is not general.
  SOURCE: Fell and Heisenberg 2021, "Positive energy warp drive from hidden geometric structures", Class. Quantum Grav. 38, 155020, arXiv:2104.06488, https://arxiv.org/pdf/2104.06488
  QUOTE: "A modest numerical analysis is carried out on a set of example conﬁgurations, ﬁnding total energy requirements four orders of magnitude smaller than the solar mass." and "ts horizons that would render the soliton uncontrollable [9]."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RC-19] CLAIM: Shoshany and Snodgrass (2024) give a concrete warp-drive realization of the special-relativistic argument that superluminal travel enables time travel: by generalizing the warp metric to a non-unit lapse, the drive can switch between reference frames in a purely geometric way, and (their abstract continues) closed timelike curves follow. Everett (1996) earlier showed by a simple modification of Alcubierre's metric that closed causal loops can be constructed. Both are constructions, not proofs that a physical drive must have CTCs; chronology protection is a conjecture.
  SOURCE: Shoshany and Snodgrass 2024, "Warp drives and closed timelike curves", Class. Quantum Grav. 41, 205005, arXiv:2309.10072, https://arxiv.org/pdf/2309.10072 ; Everett 1996, "Warp drive and causality", Phys. Rev. D 53, 7365
  QUOTE: "In this paper we provide a concrete realization of this argument in a curved general-relativistic spacetime, using warp drives as the means of faster-than-light travel. By generalizing the usual warp drive metric to allow for a non-unit lapse function, we allow the warp drive to switch between reference frames in a purely geometric way." (Shoshany-Snodgrass, full text); "We verify this conjecture by exhibiting a simple modificat…" (Everett, abstract as truncated by lit_search)
  ACCESS: full-text (Shoshany-Snodgrass); abstract (Everett)
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RC-20] CLAIM: The White et al. (2021) Casimir-cavity "intersection with the Alcubierre metric" is a qualitative shape match, not a source demonstration. They used worldline numerics for a massless scalar field with Dirichlet boundaries in 3+1 D; they state the technique "can currently only assess idealized behaviour for bounding geometry and cannot assess any frequency dependence of materials" and ignores temperature; the match is between the two-dimensional negative energy-density field around a pillar in a parallel-plate cavity and a plot of the Alcubierre density; the paper says the correlation "would suggest that chip-scale experiments might be explored to attempt to measure tiny signatures illustrative of the presence of the conjectured phenomenon: a real, albeit humble, warp bubble". The toy model is a 1 micrometre sphere in a 4 micrometre cylinder. It gives no metric, no stress components other than the density, and no total-energy or spatial-scale match to a ship-carrying bubble. I found no published independent critique or replication (see Gaps); this assessment is ours from the paper's own stated limits.
  SOURCE: White, Vera, Han, Bruccoleri, MacArthur 2021, "Worldline numerics applied to custom Casimir geometry generates unanticipated intersection with Alcubierre warp metric", Eur. Phys. J. C 81, 677, https://inspirehep.net/files/51f07591f837da882babef2da4c800c3
  QUOTE: "the worldline numeric approach for the Casimir phe- nomenon is based on (massless) scalar ﬁelds, the technique can currently only assess idealized behaviour for bounding geometry and cannot assess any frequency dependence of materials." and "This qualitative correlation would suggest that chip-scale experiments might be explored to attempt to measure tiny signatures illustrative of the presence of the conjectured phenomenon: a real, albeit humble, warp bubble."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-21] CLAIM: McMonigal, Lewis and O'Byrne (2012) trace null and massive test-particle geodesics through Alcubierre bubbles at sub- and superluminal speeds. For a superluminal bubble some particles are captured at the front of the bubble and never reach the ship, while others are ejected without reaching it; particles catching the ship from behind arrive with blueshift b = E_observed/E_emitted between 0 and 1, head-on ones with b >= 1 (b measured on the ship, test particles, no backreaction). Their effects-on-the-surroundings discussion (front-wall pile-up, energy release at stopping) is not confirmed here since the relevant text was not read. Scope: test particles in the Alcubierre metric only.
  SOURCE: McMonigal, Lewis, O'Byrne 2012, "The Alcubierre warp drive: on the matter of matter", Phys. Rev. D 85, 064024, arXiv:1202.5708, https://arxiv.org/pdf/1202.5708
  QUOTE: "Particles in the P + are captured in the front of the bub- ble and never reach the ship, and similarly particles in the "slow" matter regions are ejected from the bubble without ever reaching the ship" and "Particles in the B + region, i.e. catching up to the ship from behind, have a blueshift of 0 < b ≤ 1"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RC-22] CLAIM: Baird (1999) is a counter to Olum: hyper-fast travel without exotic matter if information is sent in only one direction along a delivery path and the set-up is restricted; only the abstract was read; no journal reference on the arXiv listing, and I found no citations that adopt it as a warp-drive route.
  SOURCE: Baird 1999, "Hyper-fast travel without negative energy", arXiv:gr-qc/9903068, http://arxiv.org/abs/gr-qc/9903068
  QUOTE: "However, this condition can be created without exotic matter if we are only sending information along the delivery path in one particular direction, and restrict ourselves to exper…"
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: low

- [RC-23] CLAIM: Le (2026 preprint) proposes an "observer-robust" test of warp energy conditions using the S-lemma, casting NEC, WEC and SEC as 4x4 linear matrix inequalities over all admissible causal directions (two tests for DEC), avoiding Hawking-Ellis classification and rapidity cutoffs. This is a method addressing the Santiago et al. objection (test all observers, not only Eulerian); I did not read its numerical results.
  SOURCE: Le 2026, "Observer-robust energy condition verification for warp drive spacetimes", arXiv:2602.18023, https://arxiv.org/pdf/2602.18023
  QUOTE: "Energy-condition tests for warp-drive spacetimes must account for all admissible causal directions at each point. We use the classical S-lemma to express the null, weak, and strong conditions as 4×4 linear matrix inequalities; the dominant condition requires two such tests."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: low

## Gaps
- Ford-Roman quantum inequality original papers (and Fewster's rigorous QEIs) not opened; the QI bounds are used only as cited in Pfenning-Ford and Van Den Broeck. The QI is for free fields; no interacting-field or curved-space bound on the warp wall was checked.
- Lobo-Visser's estimate of ship-mass versus exotic-mass in the weak-field limit was not extracted.
- Bobrick-Martire's own quantitative energies (e.g. subluminal shell masses) and Natario 2002 not opened (assumed covered by the theory/quantitative facets).
- No published critique or replication of White et al. 2021 found in INSPIRE/web search; nothing on whether the claimed "chip-scale" experiment was performed.
- No published critique specifically of Bobrick-Martire's superluminal "quantum inequality-satisfying" solution beyond Santiago et al.; no published Fell-Heisenberg reply found.
- The Celmaster-Rubin and Rodal papers are recent; whether Lentz or others have responded is unknown (Lentz's 2022 proceedings predate them).
- Tidal-force objections and Natario ship-survival were not searched (belongs to the constraints lens/other facets); Krasnikov's Ford-Roman-type "tube" negative energy amounts not extracted.
- Unread: Everett 1996 full text (abstract only, truncated); Visser-Bassett-Liberati non-perturbative claims; Alcubierre-Lobo review; Gauthier/other experiments.
