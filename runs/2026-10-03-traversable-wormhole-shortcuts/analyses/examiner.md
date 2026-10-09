# Analysis: examiner (Socrates: examine the question before answering it)
status: final

## Method applied
I defined the loaded terms ("sooner than light through the surrounding space", "negative energy", "long" and "short", "traversable", "payload") and tested whether each definition holds up. I then tested each hidden premise in the brief, plus four more I found, for support, falsifier and what the question becomes if the premise is false. I looked for nearby questions that are better posed. I also own the brief's worked calculation, "the shortcut test": T_thru/T_ext and τ_thru for each one-sided construction, and the earlier-than-channel test for each two-sided one [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-examiner_shortcut.py].

## Findings

1. **The brief's operational shortcut test depends on conventions. An invariant version exists.** T_thru/T_ext needs an emission time at A, and therefore clock synchronisation between the mouths. That synchronisation is ambiguous for orbiting mouths or mouths moving relative to each other, and it is exactly what mouth motion changes. The invariant observable is this:
   - send two signals from **one emission event** near A, one through the throat and one through the exterior;
   - record both arrivals on **one clock** at B;
   - the wormhole is a shortcut iff Δ_B = t_B(exterior) − t_B(throat) > 0.

   No synchronisation is needed, and the result matches the brief's causal definition (an event reachable through the throat that is not reachable through the exterior). This version is used below. The ratio is reported only where a static synchronisation exists. [D-02] [D-07]

2. **For one-sided wormholes, "shortcut" is a property of the geometry plus a throat time shift Δ, and it is directional.** Take static mouths with exterior-synchronised clocks. The throat identifies time t at A with time t + Δ at B. Through-throat arrival is T_w + Δ for A→B and T_w − Δ for B→A.
   - A→B is a shortcut iff Δ < D/c − T_w.
   - Closed timelike curves appear iff |Δ| > T_w + D/c.
   - So a "long" wormhole (T_w > D/c) becomes a **one-way shortcut**, without yet being a time machine, inside a window of width 2D/c.
   - For MM at d = ℓ (Q-02): a one-way shortcut needs Δ < −6.42×10³ yr, and CTCs need |Δ| > 1.24×10⁴ yr (SI) [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-examiner_shortcut.py].

   The static MM and MMP solutions have Δ = 0 by symmetry. Their "not a shortcut" status is a statement about that state, not about the topology. This tests hidden premise 6 (shortcut ⇒ time machine): the shortcut condition and the CTC condition are separate thresholds on Δ. A shortcut does not by itself create a time machine. Making one needs a second ingredient: changing Δ, a second wormhole, or relative motion (compare Everett–Roman's two tubes [K-13]). The mechanist owns the mouth-motion numbers.

3. **The classical constructions (Ellis/Morris–Thorne, Visser thin shell) are shortcuts by design. The ratio is a free parameter, not a result.**
   - Ellis throat, b₀ = 1 m, observers at r_obs = 10 m, Δ = 0: T_thru = 6.64×10⁻⁸ s. T_thru/T_ext = 2.0×10⁻² at D = 1 km, 1.3×10⁻¹⁰ at 1 AU and 2.1×10⁻¹⁵ at 1 ly (SI).
   - A payload at 0.1c local speed: τ_thru = 6.6×10⁻⁷ s.
   - Schwarzschild thin shell, M = 1 M_☉, a = 10 km, observers at 100 km: T_thru = 6.52×10⁻⁴ s (infinity clocks). T_thru/T_ext = 2.0×10⁻² at D = 10⁴ km, 1.3×10⁻⁶ at 1 AU and 2.1×10⁻¹¹ at 1 ly. The exterior weak-field Shapiro delay is included and is at most 5×10⁻⁴ s.

   [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-examiner_shortcut.py]

   GR "solved in reverse" accepts any D (Graham–Olum: "Given a desired spacetime geometry, one simply solves Einstein's equations in reverse" [new: Graham & Olum 2007, arXiv:0705.3193, full-text, "Given a desired spacetime geometry, one simply solves Einstein's equations in reverse to determine the stress-energy tensor Tab needed to produce it."]). So the shortcut question for these rows reduces entirely to whether their stress tensor is admissible [D-15] [Q-24] to [Q-29].

4. **The surviving quantum-supported one-sided constructions are not shortcuts under the brief's definition.**
   - **MM 2020:** T_thru = πℓ/c = 9.42×10³ yr. T_thru/T_ext = π at d = ℓ, 31 at d = 0.1ℓ and 314 at d = 0.01ℓ. τ_thru ≈ πr_e/c = 0.157 s [calc] [Q-06]. MM state "the time through the wormhole is always longer than through the outside, π𝓁 > d" [new: Maldacena & Milekhin, arXiv:2008.06618 p. 7, full-text, "Even when we do not make that assumption we find that the time through the wormhole is always longer than through the outside, π𝓁 > d."].
   - **MMP:** the transit-to-separation ratio exceeds 2 [Q-12] [D-06].
   - **FGM 2019:** t_min = d + logs, so the ratio approaches 1 from above, approaching but not crossing [Q-13] [D-07].

   None of these was recomputed from a metric except MM's.

5. **"Long" in MM is temporal, not spatial. That breaks the brief's phrase "longer than the path outside".**
   - I matched MM's AdS₂×S² throat (their eq. 2.7) to the extremal exterior (their eq. 2.4) [new: arXiv:2008.06618 p. 4, full-text, "ds2 =r2 e [ −(ρ2 + 1)dτ 2 + dρ2 (ρ2 + 1) + (dθ2 + sin2θdφ2) ] , −ρc≤ρ≤ρc"].
   - The proper radial length between static observers at r = 2r_e is 8.99×10⁸ m, or 3.0 light-seconds. It is independent of the matching point ρ_c from 10³ to 10⁹, and the closed form is 2r_e[ln(2γ) + 1].
   - The light time remains 9.42×10³ yr [calc].
   - So the throat is about 10 orders of magnitude **shorter in length** than ℓ = 3×10³ ly. The delay comes entirely from the lapse (redshift, γ = ℓ/r_e = 1.9×10¹²).

   A geometric "path length" test would call MM a spectacular shortcut, and a causal test calls it a detour. Only the causal test matters for achronality and causality.

6. **The proper-time benefit of MM is a free relativistic ride, not faster-than-light travel.**
   - At d = ℓ, τ/T_ext = 1.66×10⁻¹².
   - A rocket through the exterior needs γ_eq = 6.0×10¹¹ to match it. That costs (γ−1)mc² = 5.4×10²⁸ J for 1 kg and 3.8×10³⁰ J for 70 kg (SI).
   - The wormhole supplies that boost gravitationally and takes it back on exit [calc]. MM call the ratio "the boost factor that a particle that starts non-relativistic outside would acquire at the center of the wormhole" [new: arXiv:2008.06618 p. 7, full-text].

   This answers hidden premise 4: a non-shortcut wormhole is not useless. Its value is the proper-time ratio, and the CMB blueshift problem [D-08] is the same γ² problem a γ ≈ 10¹² rocket would face.

7. **Payload back-reaction in MM is small in conserved energy.**
   - The payload's mc²/|E_bin| is 2.0×10⁻¹⁰ for 1 kg and 1.4×10⁻⁸ for 70 kg.
   - Its locally boosted energy at the throat centre is 1.7×10²⁹ J for 1 kg and 1.2×10³¹ J for 70 kg [calc] [Q-02].

   The relevant danger is accumulated infalling matter and radiation, as MM say [D-08], not a single payload's conserved energy. Whether the boosted local energy matters is a question for the payload's own gravitational field in the throat; nobody here computed it.

8. **Two-sided constructions: the comparison channel is the wormhole in another description, so "earlier than the channel" is answered "no" by construction.**
   - GJW: the message must enter about R ln(R/(h l_P)) before the coupling (4.6R to 138R for R/l_P = 10² to 10⁶⁰) [calc] [Q-15]. It emerges after the coupling acts, and nothing passes with the coupling off [D-01].
   - The number of quanta that pass is at most a constant times the bits the coupling exchanges [D-02] [K-15].
   - MSY: GR forbids "send[ing] a signal through the wormhole faster than we can send it through the outside" [D-02].
   - So nothing arrives earlier than the channel or without it. Maldacena–Qi has the same structure with an eternal coupling [D-04].

   The two-sided rows answer a different question: whether the boundary interaction has a faithful bulk-geometric description. They do not answer whether there is a shortcut.

9. **Graham–Olum's theorem does NOT directly cover one-sided shortcuts. The brief and dossier risk over-reading it.**
   - Their topological-censorship result is restricted to simply connected spacetimes, so it rules out only wormholes "which connect one asymptotically flat region to another, not those which connect a region to itself" [new: Graham & Olum 2007, arXiv:0705.3193 p. 5, full-text, "the wormholes we rule out are only those which connect one asymptotically flat region to another, not those which connect a region to itself."].
   - They give the long one-sided wormhole as the counterexample, whose fastest through-paths "are chronal" [new: same, p. 6, full-text, "We can still find fastest paths through the wormhole, but they are chronal."].
   - That a one-sided **shortcut** forces an achronal complete null geodesic through the throat, and hence an ANEC violation forbidden by Condition 1, is my reading of their argument. Kontou says the achronal ANEC "seems to prohibit" such wormholes [D-27], and FGM call it "general arguments (GSL)", not a theorem [D-07].

   So even granting the conjecture, the no-shortcut conclusion for one-sided wormholes is one argued step beyond any proven theorem.

10. **The brief's "negative energy" (WEC) is not the deciding quantity.**
    - Pointwise NEC/WEC violation is forced at any throat [K-02] and is generic in QFT [K-11]. So "without negative energy" is answered "no" for every row, trivially.
    - The question that separates the constructions is: does ANEC fail on a complete *achronal* null geodesic through the throat, in a self-consistent semiclassical state?
    - MMP violates ANEC only on chronal null lines [D-06], and Ellis and thin-shell violate it on the radial geodesic [Q-25] [Q-29].
    - For BKR, the critics' point that "no exotic matter" is a definitional slip [D-10a] is the same point. Under the brief's own definition (exotic = classical NEC violation), BKR's classical Dirac field *is* exotic.

11. **BKR is two-sided, so it is never a shortcut. Its significance is instead as a potential counterexample to the conjecture.**
    - BKR connects two asymptotically flat regions [D-09], which is the class Graham–Olum rule out (finding 9).
    - A genuine, self-consistent, traversable BKR solution would therefore conflict with self-consistent achronal ANEC, unless the classical Dirac "wavefunction" is not a semiclassical ⟨T⟩. In that case it lies outside the conjecture's scope, and inside the brief's "classical fields whose energy is not bounded below" category.
    - Kain's non-traversability [D-11] and Weinbaum's static obstruction [D-12] are consistent with the conjecture.

12. **Classical shortcut geometries need speculative matter and are unstable.**
    - The Ellis shortcut of finding 3 needs a ghost or phantom scalar, which is labelled speculative.
    - Every static ghost-scalar wormhole has an unstable mode, and positive-energy infall collapses it [D-13].
    - Thin shells need σ < 0 and "perverse" sound speeds at a > 3M [D-14] [Q-30].

    So shortcuts exist in principle only with labelled extensions, and only as unstable configurations. Stability under perturbations, including the payload, is a separate unanswered requirement.

## Lens-specific outputs

### A. Loaded terms: definitions and whether they survive

| Term | Brief's definition | Problem found | Definition that survives |
|---|---|---|---|
| "Sooner than light through the surrounding space" | T_thru < T_ext with exterior-synchronised static observers | (i) Needs synchronisation, which is ambiguous for moving or orbiting mouths. (ii) Ignores the throat time shift Δ, so the answer is directional. (iii) Undefined for two-sided constructions. | Δ_B = t_B(ext) − t_B(thru) > 0 for a single emission event, both arrivals read on one clock at B, stated for each direction (findings 1 and 2) |
| "Longer than the path outside" | Implicitly a length | MM's throat is 3.0 light-s long against ℓ = 3×10³ ly, yet it takes 9.4×10³ yr (finding 5) | Use arrival time (causal structure), never proper length |
| "Negative energy" | WEC violation for some observer | Forced at every throat and generic in QFT; does not discriminate between constructions | ANEC sign on complete null geodesics, split into achronal and chronal; plus the source class: QFT vacuum, classical exotic matter, or classical Dirac field |
| "Without exotic matter" | No classical NEC violation | BKR's classical Dirac field violates the NEC, so by the brief's own words it is exotic [D-10] [D-11] | Keep the brief's definition and report that BKR fails it |
| "Two-sided: earlier than the channel" | Arrives before, or without, the boundary coupling | The bulk wormhole and the coupling are two descriptions of one process | Ask instead: quanta transferred ≤ bits exchanged? (MSY) |
| "Traversable" | A causal curve crosses before closing | Kain 2023: null rays end in a black hole, although the static solution exists [D-11]. Freivogel 2026: transmission depends on the probe [D-C5]. | Traversable *for a stated probe* (frequency, charge) over a stated window |
| "Payload" | 1 kg and a 70 kg human | Its conserved energy is tiny against |E_bin| (finding 7). The hazard is accumulated infall and boosted radiation. | Track the payload's energy plus the integrated infall flux over the transit time (9.4×10³ yr exterior for MM) |

### B. Hidden premises

| # | Premise | Support | What would falsify it | If false, the question becomes | My verdict |
|---|---|---|---|---|---|
| 1 | "Sooner than light" is well defined for every construction | Causal definition is invariant (finding 1) | — | — | **Partly false.** It holds for one-sided constructions via the single-emission-event test, but is directional through Δ. For two-sided ones it collapses: the channel and the wormhole are dual descriptions (finding 8). |
| 2 | Holding a throat open requires "negative energy" in the asker's sense | K-02, K-11 | A throat with NEC ≥ 0 everywhere (excluded by K-02 in GR) | The real constraint is achronal ANEC | True but trivial. The decisive quantity is achronal ANEC (finding 10). |
| 3 | Post-2016 constructions avoid negative energy | Authors' wording ("ordinary matter") | — | — | **False.** MMP, MM, GJW, MQ and FGM all use negative null energy from QFT [D-01] [D-04] [D-05] [D-06]. BKR uses NEC-violating classical Dirac fields [D-10] [D-11]. |
| 4 | A non-shortcut wormhole is useless | — | Proper-time saving with no propellant (finding 6) | Q1 is replaced by a proper-time question: τ/T_ext | **False.** MM gives τ/T_ext = 1.7×10⁻¹², which a rocket would match only at γ = 6×10¹¹ (3.8×10³⁰ J for 70 kg). |
| 5 | Self-consistent achronal ANEC is established | No counterexample (Kontou 2024) [D-27] | A self-consistent semiclassical state with ANEC < 0 on an achronal line | Shortcuts and CTCs return in principle | **False as stated.** It is a conjecture [K-07a] [D-C3]. Its coverage of one-sided shortcuts is a further argued step (finding 9). |
| 6 | Shortcut ⇒ time machine, and chronology protection stops it | MTY-style arguments | The separate Δ thresholds (finding 2) | Shortcut and time machine are separate questions, both controlled by Δ | **False as a logical link.** They are different thresholds. A long wormhole can become a time machine (|Δ| > T_w + D/c) without first being a static shortcut. Chronology protection is a conjecture with support [K-12]. |
| 7 | The 2022 experiment created or tested a wormhole | Jafferis framing | Kobrin et al. [D-C1] | It becomes a test of the teleportation-by-size-winding protocol | False for "created" [D-16]. "Tested" is contested. |
| 8 | Astronomical searches constrain the relevant wormholes | Q-40 to Q-45 | MM/MMP mouths look like extremal charged black holes [D-22] [D-24] | — | **Mostly false** for the surviving constructions. |
| 9 | A wormhole can be created at all | — | Geroch/Tipler not retrieved | — | Open. No formation mechanism exists for MM [D-08]. |
| 10 | A payload can be scaled up | — | MSY/Freivogel bounds for two-sided constructions [K-15] [K-16] | — | Two-sided: false (a few bits). MM: conserved energy is not the limit (finding 7). |
| 11 | AdS/2D results transfer to 4D asymptotically flat spacetime | MMP and FGM 2019 are 4D | — | — | Partially. 4D versions exist, but only as long or near-minimal (non-shortcut) wormholes. |
| 12 (new) | "Shortcut" is a property of the geometry | — | Finding 2 (Δ dependence) | Shortcut-ness is a property of the state (Δ) and is directional | **False.** |
| 13 (new) | "Long wormhole" means a long throat | MMP/MM wording | Finding 5 | "Long" means large lapse ratio γ, not length | **False** for MM. |
| 14 (new) | Graham–Olum rule out one-sided shortcuts | Kontou "seems to prohibit" | Graham–Olum's own scope sentence (finding 9) | No-shortcut for one-sided wormholes rests on an argued, not proven, extension | **Unproven.** |
| 15 (new) | A static solution being NEC-violating and regular implies traversable | — | Kain 2023 [D-11] | Dynamical traversability must be checked separately | **False.** |

### C. The shortcut test (the owned calculation)

Δ = 0 unless stated. Observers are static on the facing sides of the mouths. Units are SI. [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-examiner_shortcut.py]

| Construction | Sided | T_thru | T_ext (D) | T_thru/T_ext | τ_thru | Shortcut? |
|---|---|---|---|---|---|---|
| Ellis, b₀ = 1 m, r_obs = 10 m | one-sided embedding (designer) | 6.64×10⁻⁸ s | 3.27×10⁻⁶ s (1 km); 499 s (1 AU); 3.16×10⁷ s (1 ly) | 2.0×10⁻²; 1.3×10⁻¹⁰; 2.1×10⁻¹⁵ | 6.6×10⁻⁷ s at 0.1c | Yes, by choice of D; needs achronal ANEC violation |
| Ellis, as two-sided (2 asymptotic regions) | two-sided | — | no exterior | n/a | — | n/a; ruled out by Graham–Olum's theorem if Condition 1 holds |
| Thin shell, Schwarzschild M = 1 M_☉, a = 10 km, r_obs = 100 km | one-sided embedding | 6.52×10⁻⁴ s (∞ clocks); 6.42×10⁻⁴ s (observer clocks) | 3.28×10⁻² s (10⁴ km); 499 s (1 AU); 3.16×10⁷ s (1 ly) | 2.0×10⁻²; 1.3×10⁻⁶; 2.1×10⁻¹¹ | 6.2×10⁻³ s at 0.1c | Yes, by choice of D |
| MM 2020 (r_e = 1.5×10⁷ m, ℓ = 3×10³ ly) | one-sided | 9.42×10³ yr | 3×10³ yr (d = ℓ); 300 yr (0.1ℓ); 30 yr (0.01ℓ) | π; 31; 314 | ≈ 0.157 s | No (at Δ = 0). One-way shortcut needs Δ < −6.4×10³ yr (d = ℓ). |
| MMP 2018 | one-sided | ∼πℓ (∝ q²) | d | > 2 (quoted from FGM) [Q-12] | ∼ r_E ∼ q | No (not recomputed) |
| FGM 2019 | one-sided (4D AF) | d + logs | d | → 1⁺ [Q-13] | not given | No: approaches but does not cross (quoted) |
| BKR / EDM | two-sided | — | — | n/a | — | n/a; Kain: not traversable [D-11] |
| GJW + MSY | two-sided | arrives after the coupling; insertion ∼R ln(R/(h l_P)) before it | channel acts at t = 0 | never earlier; nothing without the coupling | — | No (structural) |
| Maldacena–Qi | two-sided | bulk crossing via the eternal coupling | — | not earlier (structural; not computed) | — | No |
| FGM 2018 quotient | two-sided / quotient | t* = −(ℓ²/r₊) ln(\|ΔV\|/(2ℓ)) [Q-14] | no ambient comparison | n/a | — | n/a |

Additional MM figures:
- proper throat length: 8.99×10⁸ m (3.0 light-s);
- rocket-equivalent γ = 6.0×10¹¹;
- rocket-equivalent kinetic energy: 5.4×10²⁸ J (1 kg), 3.8×10³⁰ J (70 kg);
- CTC threshold: |Δ| > 1.24×10⁴ yr (d = ℓ).

### D. Reframes
- **R1: from "faster than light" to "faster on the traveller's clock".** This is the useful question for the surviving constructions. It has a clear answer: yes, by about 12 orders of magnitude (MM), with a gravitational boost replacing propellant, at the cost of an ambient space colder than 10⁻²⁶ eV and a formation mechanism nobody has [D-08] [Q-07].
- **R2: from "is it a shortcut?" to "can Δ be changed?".** Under Condition 1, a long wormhole with a static symmetric Δ is allowed. The shortcut and time-machine questions both become: what happens to the Casimir support when mouth motion or a potential difference pushes Δ past D/c − T_w? A "shortcut protection" prediction follows: the ANEC-violating support must fail, or the throat close, before the through-throat geodesic becomes achronal. This would be a semiclassical calculation on MMP with relatively moving mouths. None was found in the dossier.
- **R3, two-sided: from "faster than the channel" to "does the bulk geometry faithfully describe the channel's information transfer?".** This is a holography question, and it is the one the Sycamore debate is really about [D-C1].

### E. The hardest questions any answer must survive
1. For a claimed one-sided shortcut: from a single emission event near A, read on one clock at B, is t_B(exterior) − t_B(throat) > 0? In which direction, and with what time shift Δ? A ratio quoted without Δ and direction is incomplete.
2. Is there a complete **achronal** null geodesic through the throat, and what is ∫T_kk dλ on it, in which **self-consistent** semiclassical state? (A test-field background like Urban–Olum's does not count [D-C3].)
3. Graham–Olum's theorem assumes simple connectedness. What argument extends it to a wormhole connecting a region to itself, and is that argument a theorem or a GSL-based heuristic [D-07] [D-27]?
4. For MM/MMP: if one mouth is moved, or placed in a different potential, so that Δ < D/c − T_w (MM, d = ℓ: Δ < −6.4×10³ yr), what does the fermion Casimir stress do on the newly achronal geodesic? Does the wormhole close first?
5. For two-sided protocols: does any qubit arrive before the coupling acts, or in excess of the bits it exchanges (MSY [K-15]; Freivogel [K-16])? If not, what makes the bulk description more than a re-description of teleportation?
6. Does the construction use only established fields at the scale claimed? MMP works with Standard Model fields only at sizes ≲ 1/TeV [Q-11]. MM's human-scale version needs RS II plus a dark U(1) [D-08]. Any "in principle" answer must label which.
7. Is the claimed traversability dynamical? Does a probe actually pass, for which frequencies and charges (Kain 2023 [D-11]; Freivogel 2026 [D-C5]), and does the wormhole survive the probe (Kain 2026 [D-13])?
8. Is the proper-time benefit real once the traveller's boosted environment is included? MM's γ ≈ 1.9×10¹² boosts ambient photons by γ² [D-08], and the locally boosted payload energy is 1.2×10³¹ J for 70 kg [calc]. Does the throat survive a human's boosted stress-energy and the accumulated infall over 9.4×10³ yr of exterior time?
9. For BKR-type classical Dirac support: is the matter a semiclassical ⟨T⟩ (inside the conjecture's scope) or a classical field with energy unbounded below (outside it)? Answers that use BKR either way must say which.
10. For any "shortcut in principle" answer using phantom matter: what stabilises it against the unstable mode [D-13], and does the stabiliser itself obey NEC?

## Calculations
- `runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-examiner_shortcut.py` (log `.py.log` beside it). It uses `wormhole_tools.py` for the Ellis and thin-shell transits, and its own matching of MM eqs (2.4) and (2.7). Results (SI):
  - **Ellis** (b₀ = 1 m, r_obs = 10 m): T_thru = 6.6378×10⁻⁸ s. Ratio 2.031×10⁻² (D = 1 km), 1.330×10⁻¹⁰ (1 AU), 2.103×10⁻¹⁵ (1 ly). At r_obs = 100 m: 2.500×10⁻¹, 1.337×10⁻⁹, 2.114×10⁻¹⁴. τ = 6.60×10⁻⁷ s at 0.1c (r_obs = 10 m).
  - **Thin shell** (M = 1 M_☉, a = 10 km, r_obs = 100 km): T_thru = 6.5209×10⁻⁴ s (∞ clocks), proper length 1.8749×10⁵ m. Ratio 1.989×10⁻² (D = 10⁴ km), 1.307×10⁻⁶ (1 AU), 2.066×10⁻¹¹ (1 ly). τ = 6.22×10⁻³ s at 0.1c.
  - **MM, times:** γ = ℓ/r_e = 1.892×10¹²; T_thru = 9.4248×10³ yr; τ = 0.1572 s; ratio π, 31.4, 314 at d = ℓ, 0.1ℓ, 0.01ℓ; τ/T_ext = 1.66×10⁻¹² at d = ℓ.
  - **MM, length and payload:**
    - proper throat length 8.9886×10⁸ m (2.998 light-s), the same for ρ_c = 10³, 10⁶ and 10⁹;
    - rocket-equivalent γ_eq = 6.023×10¹¹, with kinetic energy 5.41×10²⁸ J (1 kg) and 3.79×10³⁰ J (70 kg);
    - payload mc²/|E_bin| = 2.0×10⁻¹⁰ (1 kg) and 1.4×10⁻⁸ (70 kg);
    - locally boosted payload energy 1.70×10²⁹ J (1 kg) and 1.19×10³¹ J (70 kg).
  - **Δ thresholds:**
    - MM at d = ℓ: shortcut A→B needs Δ < −6.4248×10³ yr; CTC needs |Δ| > 1.2425×10⁴ yr.
    - MM at d = 0.01ℓ: Δ < −9.3948×10³ yr for a shortcut; |Δ| > 9.4548×10³ yr for CTCs.
    - Ellis at D = 1 ly: |Δ| up to about 1 yr keeps the shortcut without CTCs.
  - **GJW:** insertion lead ln(R/l_P) = 4.6, 23 and 138 in units of R, for R/l_P = 10², 10¹⁰ and 10⁶⁰.
- Approximations:
  - the one-sided embedding of two-sheet metrics is valid only for D ≫ r_obs;
  - the thin-shell Shapiro delay is weak-field and radial;
  - the MM matching t = ℓτ, ρ = ℓ(r − r_e)/r_e² is my own (consistent with MM's rescaling (2.8) and with the T_thru → πℓ check);
  - MMP, FGM and MQ values are quoted, not recomputed.

## Candidate answers (at least 3; the null and a reframe count)
- [EXAMINER-A] **Null (within established semiclassical physics).** No traversable wormhole consistent with established physics is a shortcut.
  - Every consistent one-sided construction has T_thru/T_ext ≥ 1: MM gives π at d = ℓ, MMP more than 2, FGM 2019 approaches 1 from above.
  - Two-sided ones deliver nothing earlier than, or without, their coupling.
  - Shortcuts exist only as designer classical geometries, with ratios as small as 2×10⁻¹⁵ at 1 ly, which need achronal-ANEC-violating matter.
  - **status:** surviving.
  - **why:** findings 3, 4 and 8; Graham–Olum for two-sided; Kontou and FGM for one-sided.
  - **distinguishing test:** a self-consistent semiclassical 4D solution with Δ_B > 0 would refute it; the FGM 2019 → 1⁺ approach and the MSY bits bound would be its signature.
  - **confidence:** medium-high. The one-sided step rests on an argued extension of a conjecture (finding 9).
- [EXAMINER-B] **Reframe (the premise "longer than the path outside" is wrong, and non-shortcuts are not useless).** The surviving wormholes are short in length and long in time.
  - MM's throat is 3.0 light-s long, yet takes 9.4×10³ yr of exterior time, while the traveller ages 0.157 s.
  - So the right question is the proper-time ratio, τ/T_ext = 1.7×10⁻¹². A rocket would match it only at γ = 6×10¹¹, for 3.8×10³⁰ J for 70 kg.
  - The wormhole is a propellant-free time-dilation device, not a faster-than-light channel.
  - **status:** surviving.
  - **why:** findings 5 and 6.
  - **distinguishing prediction:** for any such wormhole, τ_thru/T_thru ≈ r_e/ℓ = 1/γ, and T_thru exceeds d/c. A shortcut candidate would instead have T_thru < d/c, whatever τ is.
  - **confidence:** medium. The physics is MM's own; the length matching is mine.
- [EXAMINER-C] **Reframe ("shortcut" is a property of the state, not the geometry).** For a one-sided wormhole, shortcut-ness depends on the throat time shift Δ and is directional.
  - A long wormhole becomes a one-way shortcut at Δ < D/c − T_w (MM, d = ℓ: −6.4×10³ yr) and a time machine at |Δ| > T_w + D/c (1.24×10⁴ yr).
  - If the conjecture holds, the support must fail before Δ crosses D/c − T_w ("shortcut protection").
  - **status:** strained. The kinematics is solid; the protection prediction is my inference, and no source computes MMP with Δ ≠ 0.
  - **distinguishing test:** a semiclassical MMP/FGM calculation with mouths in relative motion or at different potentials. Does ∫T_kk on the newly achronal geodesic turn non-negative, or does the throat close, as Δ approaches D/c − T_w?
  - **confidence:** low-medium.
- [EXAMINER-D] **Shortcut in principle only with labelled speculative matter, and unstable.** Ghost or phantom-scalar Ellis and thin-shell wormholes are shortcuts by construction, and Condition 1 does not constrain classical phantom fields. But every static ghost-scalar wormhole has an unstable mode, and positive-energy infall closes it.
  - **status:** strained. It is allowed only under labelled extensions, and stability fails.
  - **distinguishing test:** a stabilised phantom shortcut, numerically evolved with a payload, staying open.
  - **confidence:** medium (that it is unstable as built).
- [EXAMINER-E] **Two-sided collapse.** For GJW, MSY, MQ and FGM 2018, "earlier than the channel" has a structural no.
  - The message emerges after the coupling, with no coupling it does not arrive, and quanta ≲ bits exchanged.
  - The meaningful question is whether the bulk geometry faithfully represents the channel (the Sycamore dispute).
  - **status:** surviving.
  - **distinguishing test:** a hardware run where the transferred fidelity, as a function of coupling sign and time, follows the size-winding/shockwave prediction for a *chaotic* Hamiltonian (Byun et al. 2026 direction [F-05]), against a commuting one.
  - **confidence:** high on "not earlier"; low on what the experiments test.
- [EXAMINER-F] **Shortcut if the conjecture fails.** If a self-consistent semiclassical state violates ANEC on an achronal geodesic (an Urban–Olum-type violation made self-consistent), one-sided shortcuts and CTCs return in principle.
  - **status:** strained. There are no known self-consistent counterexamples [D-27].
  - **distinguishing test:** a self-consistent back-reacted calculation of the Urban–Olum setup.
  - **confidence:** low.

## What would change my mind
- A source showing that Graham–Olum's Condition 1 rigorously excludes one-sided shortcuts, not only inter-universe wormholes. That would upgrade [EXAMINER-A] and weaken the "argued step" caveat.
- A computation of MMP or FGM with Δ ≠ 0 showing the wormhole stays open past the shortcut threshold. That would refute the protection half of [EXAMINER-C] and strain [EXAMINER-A].
- A correct MM proper-length calculation from the full numerical metric showing the throat is not short in length. That would weaken [EXAMINER-B]'s "short in length" half; the τ/T_ext half stands on MM's own statements.
- A self-consistent traversable BKR-type solution [D-C2] would be a counterexample to the conjecture if its Dirac field counts as a semiclassical ⟨T⟩.

## Assumptions I relied on
- The static MM/MMP solutions have Δ = 0 (symmetric identification). Neither paper discusses Δ; this is my reading.
- The one-sided embeddings of the Ellis and thin-shell metrics treat each mouth as isolated (D ≫ r_obs), with Δ = 0 and observers on the facing sides.
- MM numbers: r_e = 1.5×10⁷ m and ℓ ≈ 3×10³ ly (Q-01, Q-02). MM's ℓ and d are treated as independent, subject to πℓ > d.
- The MM interior–exterior matching is the standard near-horizon map. The overlap region 1 ≪ ρ_c ≪ γ is respected in the calculation.
- MMP, FGM 2019, GJW and MQ transit figures are quoted from the dossier, not recomputed.
- Unit systems: SI throughout the table. Dossier geometric and natural-unit values are cited as they are given.
