# Analysis: dialectician (resolve real contradictions)
status: final

## Method applied
Pick the three contradictions in the dossier where two well-supported claims cannot both hold as stated; state thesis and antithesis with evidence; find the regime (observer synchronisation, test-field vs self-consistent, one vs two length scales, energy bounded below or not) where both hold, or show which must yield; then make each synthesis predict something neither side predicted alone. Calculations are small, order-of-magnitude scripts in `calc/lens-dialectician_*.py`.

## Findings
1. **The achronal ANEC has now been proved in exactly the throat geometry that MMP and MM use.** Rosso 2020: [new: Rosso, JHEP 07 (2020) 023, arXiv:2005.06476, abstract, "We prove the achronal averaged null energy condition for general quantum field theories in the near horizon geometry of spherical extremal black holes (i.e. ${{\rm AdS}_2\times S^{d-2}}$), de Sitter and anti-de Sitter."] So an AdS₂×S² throat on its own cannot carry an ANEC-violating complete achronal null geodesic. MMP and MM become traversable only because the exterior return path, or the boundary coupling in Maldacena–Qi, makes the throat geodesics chronal [D-06, K-07(f)].
2. **Achronal-ANEC violation in a fixed background does not by itself give a shortcut.** [new: Ishibashi, Maeda & Mefford, PRD 100, 066008 (2019), arXiv:1903.11806, abstract, "we find holographic models which violate the achronal ANEC for $3+1$ and $4+1$-dimensional boundary theories ... The conformal boundary of our bubble solution is asymptotically flat and is causally proper in the sense that a "fastest null geodesics" connecting any two points on the boundary must lie entirely on the boundary."] The boundary metric is fixed, not self-consistent, so this is a test-field result like Urban–Olum [D-C3]. It shows that achronal-ANEC violation is necessary for a shortcut (Graham–Olum), not sufficient.
3. **Graham–Olum's own claim is about all wormholes, not only shortcuts.** [new: Graham & Olum, PRD 76, 064001 (2007), arXiv:0705.3193, abstract, "requiring only that there is no self-consistent space-time in semiclassical gravity in which ANEC is violated on a complete, {\em achronal} null geodesic. We indicate why such a condition might be expected to hold and show that it is sufficient to rule out wormholes and closed timelike curves."] Per the dossier, the wormholes ruled out are those connecting different asymptotically flat regions [K-07(a)]. Long one-ambient-space wormholes escape [K-07(f)].
4. **Maldacena–Milekhin assert that long wormholes cannot become time machines.** [new: Maldacena & Milekhin, PRD 103, 066007, arXiv:2008.06618, full-text p. 2, "they are allowed in the quantum theory, but with one catch, the time it takes to go through the wormhole should be longer than the time it takes to travel between the two mouths on the outside a" with footnote a: "This also implies that they can not be converted into time machines [4]."] Here [4] is Morris–Thorne–Yurtsever 1988. The paper also says (p. 7) "In deriving (2.12) we assumed that the distance d between the two black holes is smaller than 𝓁, d≪𝓁", and that coalescence by gravitational and dark-U(1) radiation "happens at time scales that are parametrically longer than the traversal time, π𝓁" [new: same source, full-text p. 7].
5. **The footnote in Finding 4 is false as kinematics, so it needs a dynamical condition.** Take exterior-synchronised clocks and let mouth B's clock fall behind by Δ, through MTY mouth motion or by sitting in a deeper potential. A signal B→A through the throat then takes T_thru − Δ, and one A→B takes T_thru + Δ. The B→A route is a shortcut once Δ > Δ_s = T_thru − d. A closed causal loop exists once Δ > Δ_CTC = T_thru + d.

   For MM's worked example (ℓ = 3×10³ ly, T_thru = πℓ/c = 9.4×10³ yr; [D-08, Q-02, Q-06]):

   | d (ly) | Δ_s (yr) | Δ_CTC (yr) | Time to Δ_s, mouth orbiting at 0.1c (rate ε = 5×10⁻³) | Same, mouth near a massive black hole (ε = 0.1) |
   |---|---|---|---|---|
   | 100 | 9.3×10³ | 9.5×10³ | 1.9×10⁶ yr | 9.3×10⁴ yr |
   | 1000 | 8.4×10³ | 1.04×10⁴ | 1.7×10⁶ yr | 8.4×10⁴ yr |

   A Galactic-scale potential difference (ε = 10⁻⁶) gives about 9×10⁹ yr. [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-dialectician_timeshift.py]

   Nothing in the long-wormhole construction stops Δ from accumulating at a rate ε > 0. So "cannot be converted" holds only if the mouth pair dies (coalesces, collapses from accreted matter [D-08], or loses traversability) before Δ reaches Δ_s. That requires lifetime × ε < T_thru − d. MM's coalescence time is only "parametrically longer" than πℓ, so MM do not show this inequality.
6. **Inside the shortcut window Δ_s < Δ < Δ_CTC, the B→A throat null geodesic is achronal.** Suppose two of its points were joined by a timelike curve. That curve would have to go through the exterior (cost ≥ d, more than the time T_thru − Δ available) or around the loop (cost (T_thru − Δ) + d > 0, which only makes it later). Below Δ_s the exterior is faster, so the geodesic is chronal, which is MMP's escape [D-06].

   This window is exactly where the self-consistent achronal ANEC [K-07(a)] forbids an ANEC-violating complete geodesic. The throat's ANEC along that geodesic stays negative: it is the same local Casimir stress [D-06]. So the conjecture predicts a protection threshold at Δ_s, a distance 2d before Hawking's chronology horizon at Δ_CTC [K-12]. (My own derivation; no source treats long-wormhole time shifts.)
7. **In a 2D toy, the supporting negative energy grows rather than shrinks as Δ grows.** For a 2D CFT on a loop identified as (t, x) ~ (t + Δ, x + L), the null energies are T_∓∓ = −(πc/12)/(L ∓ Δ)². I checked this against an explicit boost; for example L = 1, Δ = 0.9 gives T₋₋ = −26.18 both ways. The chirality that runs along the time-advancing direction is enhanced by (L/(L − Δ))².

   With L = T_thru + d, the enhancement at the shortcut onset Δ_s is ((T_thru + d)/(2d))²: 4.3 at d = ℓ, 27 at d = ℓ/3 and 2.3×10³ at d = ℓ/30. It diverges at the chronology horizon, a 2D analogue of the stress-tensor breakdown in Kay–Radzikowski–Wald [K-12], here with a negative sign. [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-dialectician_timeshift.py]

   The toy treats MMP's lowest-Landau-level fermions as a 2D CFT around one field-line loop [D-06]. It is not MMP's calculation.
8. **In the toy, the MMP energy balance runs away toward the chronology horizon once Δ ≳ 0.15 l₀.** I wrote MMP's E(l) = r_e³/(G l²) − q/(8l) [Q-10] with the twisted Casimir term.
   - At Δ = 0 it reproduces the minimum at l₀ = 16 r_e³/(G q) and E_min = −G q²/(256 r_e³).
   - It also reproduces |E_min|/M_e = (r_e/l₀)², which for γ = 2×10¹² equals Q-05's 2.5×10⁻²⁵ exactly. This is an analytic check on Q-05.
   - With the twist the equilibrium length shrinks: x = l/l₀ = 0.977 at δ = Δ/l₀ = 0.05 and 0.896 at δ = 0.10.
   - The metastable minimum disappears at δ_c = 0.1495. Above that the energy falls monotonically as l → Δ⁺, toward the null loop.

   So the quantum support does not supply the protection that the achronal ANEC needs. It pushes the other way. The protection must come from somewhere else: back-reaction beyond Q-10, the geometry of the mouths, quantum gravity, or the death of the mouth pair. [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-dialectician_timeshift.py] Toy assumptions: d ≪ l (MM's own assumption), Δ adiabatic, r_e fixed, energy evaluated in the mouths' rest frame.
9. **FGM 2019 is the sharpest case of Findings 5–8.** Its minimum transit is t_min = d + logs [D-07, Q-13], so Δ_s is only the log term: a tiny accumulated time shift turns it into a shortcut. Its background lives for a time of order d^{3/2} (G = c = 1) before merging [D-07], much longer than d, while traversability is "exponentially fragile" [D-07]. Read this way, the GSL-based "no fastest causal curve" argument FGM cite [D-07] predicts that any accumulated Δ comparable to the log term destroys traversability. That would be fragility working as chronology protection.
10. **EDM: the static solutions sit in the Planck regime that Ford–Roman allow.** Kain's static EDM throats are 75.28 to 498.4 l_P, that is 1.2×10⁻³³ to 8.1×10⁻³³ m [Q-18]. That is at most 0.10 of the Ford–Roman single-scale bound l_P/(2f²) = 5×10³ l_P = 8.1×10⁻³² m at f = 0.01 [Q-20]. They need a fermion of μ̄ = 0.2, which is 0.2 m_P = 4.4×10⁻⁹ kg, 4.8×10²¹ times the electron mass. The electron's gravitational strength is (m_e/m_P)² = 1.8×10⁻⁴⁵. So no electron-like member of this family is shown [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-dialectician_edm_scale.py]. Reading μ̄ as the fermion mass in Planck units is my interpretation of D-09/D-11. Kontou: a Planck-size throat "would not be traversable" [D-27].
11. **EDM: test-field ANEC violation versus no self-consistent solution has the same shape as Urban–Olum versus Graham–Olum.** Weinbaum finds positive-frequency Dirac fields violating ANEC on fixed wormhole backgrounds, but no two-ended self-consistent solution [D-12]. Every two-ended static solution found so far is either non-smooth with distributional sources (symmetric BKR [D-10b,c]) or uses negative-frequency modes (KZ, Kain, per Weinbaum [D-12]), that is, a classical field whose energy is not bounded below (brief, Definitions). Those that were evolved collapse to black holes [D-11].

    The BKR family connects two asymptotically flat ends [D-09], which is the class Graham–Olum say the self-consistent achronal ANEC rules out (Finding 3). So the conjecture and the numerics agree. The "no exotic matter" claim survives only where the Dirac energy is unbounded below, which is outside the semiclassical domain of the conjecture.
12. **Sycamore: both sides of D-C1 can hold, because the signatures are necessary, not sufficient.** Jafferis et al. reproduce the five signatures [D-16]. Kobrin–Schuster–Yao show that they arise from a learned, fully commuting Hamiltonian that does not thermalise [D-C1]. Size winding and a coupling-sign asymmetry are what any teleportation-by-size system shows. The gravitational reading adds a requirement: the asymmetry must be generic across operators, and must come with scrambling, at large N. Byun et al. (N = 8, chaotic) measure I_PT of order 0.01 [Q-39].

    Even a fully gravitational version is a two-sided GJW/MSY channel. There nothing arrives earlier than, or without, the coupling [D-01, D-02], and the information passed is ≲ const × bits exchanged [K-15]. So the experiment cannot bear on Q1 (shortcut) in either reading.

## Lens-specific outputs

### Contradiction 1 (central): long wormholes, time shifts, and the self-consistent achronal ANEC
- **Thesis.** Long quantum-supported wormholes are consistent semiclassical solutions. Their ANEC-violating null lines are chronal, so the self-consistent achronal ANEC does not touch them [D-06, D-08, K-07(f), D-27]. MM add that they "can not be converted into time machines" (Finding 4).
- **Antithesis.** Mouth clocks can be offset by motion or by gravitational redshift, the MTY mechanism. The offset grows without bound at rate ε, and any offset Δ > T_thru − d makes the throat route a shortcut, and Δ > T_thru + d a time machine (Finding 5). The self-consistent achronal ANEC "is sufficient to rule out wormholes and closed timelike curves" [Finding 3; K-07(a)].
- **Why they cannot both hold as stated.** Grant (i) that a long wormhole exists and lives for a time t_life, (ii) that ε > 0 is available, and (iii) that the conjecture holds. Then t_life·ε > T_thru − d is a contradiction.
- **Where both hold.** In the regime t_life·ε < T_thru − d: the mouth pair coalesces, collapses or loses traversability before the offset matures. Or the self-consistent back-reaction lengthens T_thru as fast as Δ grows, keeping T_thru − Δ ≥ d. MM's footnote is then true dynamically, not kinematically.
- **What must yield if neither escape operates.** The conjecture must yield, or the solution must cease to exist. My toy (Findings 7–8) shows the Casimir sector itself does not lengthen the throat. It shortens it, and the toy equilibrium is lost at Δ ≈ 0.15 l₀. The lengthening escape therefore needs physics outside the toy.
- **Synthesis.** Chronology protection for long wormholes, if it exists, acts at the shortcut threshold Δ_s = T_thru − d, not at Hawking's chronology horizon Δ_CTC = T_thru + d. The protecting agent cannot be the supporting quantum field, which strengthens there.
- **New predictions** (neither side made these):
  - (P1) A self-consistent semiclassical MMP or FGM-2019 solution with asymmetric mouth redshift either stops being stationary, or develops a growing T_thru, before Δ reaches T_thru − d. For FGM, that is a Δ of the order of the log term only.
  - (P2) If instead T_thru − Δ < d is found in a self-consistent solution, the self-consistent achronal ANEC is falsified without any CTC ever forming. The 2d-wide window in Δ is a clean test.
  - (P3) In the 2D sector, the chirality running along the time advance carries null energy enhanced by ((T_thru + d)/(2d))² at the shortcut onset: 4.3 for d = ℓ, about 2×10³ for d = ℓ/30.
- **Status.** Unresolved. The decisive calculation is P1.

### Contradiction 2: Einstein–Dirac(–Maxwell) "no exotic matter" vs no traversable EDM wormhole
- **Thesis.** Dirac fields hold a throat open "without needing any form of exotic matter" [D-09]. Asymmetric smooth static solutions exist [D-10c, D-C2]. Positive-frequency Dirac fields violate ANEC on fixed wormhole backgrounds [D-12].
- **Antithesis.** The symmetric solutions are not solutions [D-10b]. The asymmetric ones collapse to black holes and are not traversable [D-11]. No two-ended positive-frequency solution exists in the restricted ansatz [D-12]. The fields are exotic by the NEC definition [D-10a].
- **Where both hold.** "Exotic" splits along the brief's three-way distinction:
  - test-field ANEC violation by a positive-frequency field: real, like Casimir;
  - static self-consistent support: achieved only with negative-frequency modes (energy unbounded below) or distributional sources;
  - dynamical traversability: absent.
  Both sides are right about different items. "No exotic matter" is true of the matter's origin (ordinary fermions) and false of its stress tensor (NEC-violating) and of its state (negative-frequency).
- **What must yield.** The claim that EDM wormholes are physically meaningful traversable solutions yields, at least for spherical, definite-frequency, Planck-mass fermions.
- **New predictions:**
  - (P4) Any further two-ended asymptotically flat EDM solution, including Dzhunushaliev et al. 2026 [D-C2], will on inspection either use negative-frequency or non-normalisable modes, or collapse under evolution. This is the class Graham–Olum's conjecture excludes.
  - (P5) A positive-frequency EDM wormhole, if one exists, will be one-sided and long (T_thru > T_ext), like MMP. It will not be two-ended.
  - (P6) All EDM throats found will stay near the Planck scale with Planck-mass fermions (10⁻³³ m, μ ≈ 0.2 m_P; Finding 10). No macroscopic member follows from scaling.

### Contradiction 3: Sycamore "wormhole dynamics" vs "not gravitational" [D-C1]
- **Thesis.** Five gravitational signatures were observed [D-16].
- **Antithesis.** The Hamiltonian is commuting and non-thermalising, and the signatures appear only for the trained operators [D-C1].
- **Where both hold.** The signatures are features of teleportation by size winding, which gravity implies but which do not imply gravity. Both are right about different implications.
- **New predictions:**
  - (P7) In chaotic, larger-N hardware runs (Byun et al.'s N = 8 is the start [Q-39]), the coupling-sign asymmetry becomes operator-generic and peaks near the scrambling time, which grows like log N. A commuting learned model does not show this for untrained operators.
  - (P8) In either reading, the qubits teleported never exceed the classical communication carried by the coupling [K-15]. So no result from this programme can bear on the shortcut question Q1. It tests GJW's two-sided mechanism, not one-sided shortcuts.

### Thesis–antithesis ledger
| # | Thesis (evidence) | Antithesis (evidence) | Reconciling regime / definition | Which yields | Synthesis prediction |
|---|---|---|---|---|---|
| 1 | Long wormholes are consistent; they cannot become time machines [D-06, D-08, Finding 4] | A clock offset Δ grows at rate ε; Δ > T_thru − d gives a shortcut, Δ > T_thru + d gives CTCs; SC achronal ANEC forbids both [K-07, Finding 5] | t_life·ε < T_thru − d, or back-reaction lengthens T_thru | MM's footnote as kinematics yields; otherwise the conjecture or the solution | P1–P3: protection at Δ_s, not at Δ_CTC; the support field strengthens there (×4.3 to ×2×10³) |
| 2 | Dirac fields support throats without exotic matter [D-09, D-12 test-field] | No traversable self-consistent EDM wormhole [D-10, D-11, D-12] | "Exotic" by origin vs by stress tensor vs by state; test-field vs self-consistent | Physical-solution claim yields | P4–P6: two-ended solutions need negative-frequency modes; any survivor is one-sided and long; Planck scale |
| 3 | Sycamore shows wormhole dynamics [D-16] | Not gravitational [D-C1] | Signatures necessary, not sufficient | Neither as a fact claim; the gravitational interpretation is unproven | P7–P8: operator-generic asymmetry at large N; never tests Q1 |

## Calculations
- `runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-dialectician_timeshift.py` (log beside it):
  - (A) Shortcut and CTC thresholds under a mouth clock offset, for MM's worked example: T_thru = 9.4×10³ yr. With d = 100 ly, Δ_s = 9.3×10³ yr and Δ_CTC = 9.5×10³ yr. With d = 1000 ly, Δ_s = 8.4×10³ yr and Δ_CTC = 1.04×10⁴ yr. Accumulation time is Δ/ε, for example 1.7×10⁶ to 1.9×10⁶ yr at ε = 5×10⁻³.
  - (B) 2D twisted-circle Casimir T_∓∓ = −(πc/12)/(L ∓ Δ)², closed form against an explicit boost; they agree to printed precision at Δ/L = 0, 0.3, 0.9 and 0.99 (natural units, c_CFT = 1). Enhancement at the shortcut onset: 4.288 (d = ℓ), 27.17 (d = ℓ/3), 2268 (d = ℓ/30).
  - (C) Toy MMP energetics with the twist. The Δ = 0 limit reproduces Q-10's E_min = −G q²/(256 r_e³) and Q-05's 2.5×10⁻²⁵. The critical twist is δ_c = Δ_c/l₀ = 0.1495 (dimensionless).
- `runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-dialectician_edm_scale.py`:
  - Kain's EDM throats are 1.2×10⁻³³ to 8.1×10⁻³³ m (SI), at most 0.0997 of the Ford–Roman l_P/(2f²) at f = 0.01.
  - The required fermion mass is 0.2 m_P = 4.35×10⁻⁹ kg, 4.8×10²¹ m_e. The electron's (m_e/m_P)² is 1.75×10⁻⁴⁵.

## Candidate answers (at least 3; the null and a reframe count)
- [DIALECTICIAN-A] **No self-consistent traversable wormhole is a shortcut.** Every surviving construction (MMP, FGM 2019, MM) is long, with T_thru/T_ext ≥ 1, approaching 1 only in FGM 2019. Each is held open by chronal ANEC violation from quantum fields. The two-sided ones (GJW, MQ, FGM 2018) deliver nothing earlier than, or without, their coupling channel.
  - Status: surviving, conditional on the self-consistent achronal ANEC.
  - Synthesis: C1 together with Rosso's proof (Finding 1), which explains why an AdS₂ throat needs chronal routes to be traversable.
  - Distinguishing test: P1. A self-consistent MMP or FGM solution with asymmetric mouth redshift must lose stationarity or lengthen before Δ = T_thru − d.
  - Confidence: medium.
- [DIALECTICIAN-B] **Reframe: "is it a shortcut?" is the wrong invariant; "can its clock offset mature?" is the right one.**
  - A long wormhole is one accumulated mouth-clock offset (T_thru − d) away from a shortcut, and 2d further from a time machine. MM's "cannot be converted into time machines" holds only if mouth lifetime × redshift asymmetry < T_thru − d.
  - For MM that is about 9×10³ yr of offset, reached in about 10⁵ yr near a massive black hole (ε = 0.1) or about 2×10⁶ yr at 0.1c.
  - The self-consistent achronal ANEC then predicts chronology protection at the shortcut threshold, before Hawking's horizon. My 2D toy shows the Casimir support strengthens there by (T_thru + d)²/(2d)² and loses equilibrium at Δ ≈ 0.15 l₀.
  - Status: surviving (a reframe, untested).
  - Synthesis: C1.
  - Predictions: P1–P3. If a self-consistent solution enters the 2d-wide window without breaking down, the conjecture is falsified without any CTC forming.
  - Confidence: medium on the kinematics, low on the toy dynamics.
- [DIALECTICIAN-C] **"Held open without negative energy" fails in every working case; only the source of the negative energy differs.**
  - Every traversable construction violates the pointwise NEC at the throat [K-02] and the ANEC on some complete geodesic [K-01].
  - The source is either ordinary quantum fields in a Casimir-type state (MMP, MM, FGM, GJW, MQ: "ordinary matter" ≠ no negative energy) or a classical Dirac field with negative-frequency modes, whose energy is unbounded below (EDM).
  - What survives is the narrower claim that no achronal (or, for long wormholes, no self-consistent achronal) ANEC violation is needed.
  - Status: surviving.
  - Synthesis: C2 (three meanings of "exotic").
  - Predictions: P4–P6. Any new two-ended EDM solution uses negative-frequency modes or collapses. Any positive-frequency EDM survivor is one-sided and long. EDM throats stay at about 10⁻³³ m with Planck-mass fermions.
  - Confidence: high on the NEC/ANEC part, medium on P4–P6.
- [DIALECTICIAN-D] **Shortcuts are possible because the self-consistent achronal ANEC fails.**
  - Status: strained.
  - Why: every known achronal-ANEC violation is test-field or fixed-background (Urban–Olum [D-C3]; Ishibashi et al. [Finding 2]; Weinbaum's Dirac fields [D-12]). Ishibashi et al. show that such a violation can coexist with a causally proper boundary, so violation is not sufficient for a shortcut. On the other side, Rosso proves the condition in AdS₂×S² [Finding 1].
  - Synthesis: C1 and C2 both locate the violations in the non-self-consistent regime.
  - Distinguishing test: the same as P2.
  - Confidence: low.
- [DIALECTICIAN-E] **Null (in practice): no traversable wormhole can pass even 1 kg within about 100 years.**
  - The survivors are Planck-scale (EDM, 10⁻³³ m), perturbative with a few bits (GJW/MSY [K-15]), transient and fragile (FGM 2019 [D-07]), or need a labelled speculative sector with 10⁴ M_☉ mouths and refrigeration far below the CMB (MM [D-08, Q-04, Q-07]). None has a formation mechanism [D-08].
  - Status: surviving for in practice. It is not a verdict on in principle.
  - Synthesis: C2 and C3 (the lab programme cannot test Q1).
  - Distinguishing test: a formation mechanism for an MM-type mouth pair, or a detection of magnetically charged extremal black holes.
  - Confidence: high.
- [DIALECTICIAN-F] **"The 2022 processor experiment tested wormhole traversability."**
  - Status: eliminated as stated. It is reframed as a test of teleportation by size winding.
  - Why: the gravitational reading needs operator-generic, large-N chaotic behaviour that the learned commuting model lacks [D-C1]. And even a fully gravitational version tests a two-sided coupling channel, never a shortcut [D-01, D-02].
  - Synthesis: C3.
  - Prediction: P7–P8.
  - Confidence: medium.

## What would change my mind
- A source showing that the MMP or FGM 2019 constructions dynamically fix the mouths' relative redshift: for example, the symmetric binary orbit keeps Δ = 0, and no asymmetric placement is possible without destroying the solution. Then C1's antithesis loses its premise (ii), and MM's footnote stands as stated.
- A full MMP back-reaction computation in which the throat lengthens under a clock offset. That would overturn the toy in Finding 8 and confirm the "lengthening" escape.
- A self-consistent semiclassical solution violating ANEC on an achronal geodesic. That would move DIALECTICIAN-D to surviving and make B's window a live shortcut.
- A positive-frequency, smooth, two-ended EDM solution that survives evolution. That would refute P4.
- Hardware results in which a commuting or learned model reproduces operator-generic asymmetry and scrambling-time scaling. That would weaken P7 as a discriminator.

## Assumptions I relied on
- **Clock offsets.** Mouth clock offsets add to the throat transit as in MTY, with exterior-synchronised static observers at the mouths (brief, Definitions). Throat transit T_thru = πℓ/c is MM's external crossing time [Q-06].
- **Achronality.** The argument in Finding 6 that the B→A throat geodesic is achronal exactly in the window Δ_s < Δ < Δ_CTC is my own reasoning, not sourced.
- **The 2D toy.** It treats MMP's lowest-Landau-level fermions as a 2D CFT on a single loop of period L ≈ l (d ≪ l), uses the vacuum of the twisted identification, holds r_e fixed, and evaluates energy in the mouths' rest frame. It is not MMP's calculation, and the math lens should check it.
- **Redshift rates.** The ε values are illustrative: v²/(2c²) for orbital motion, and about 0.1 for a mouth parked deep in a massive black hole's potential. No source in the dossier gives the mouths' achievable redshift asymmetry.
- **EDM parameters.** μ̄ in Kain 2023 is read as the fermion mass in Planck units [D-09, D-11, Q-18]. The coupling comparison (0.03 vs √α ≈ 0.085) depends on the unit convention.
- **Theorem versus conjecture.** The Graham–Olum self-consistent achronal ANEC is treated as a conjecture [K-07(a)], and Rosso 2020 as a proof only in fixed AdS₂×S², dS and AdS backgrounds [Finding 1].
