# Independent check: Blas & Oller, "Gravitational waves decay in vacuum", arXiv:2607.24930 (v2)

Check folder: `checks/2026-10-11-blas-oller-gw-decay/`. Units are natural (ħ = c = 1) unless SI is stated.

## Conventions

- **Pairs vs photons.** "Pairs" means photon pairs; photons = 2 × pairs. B&O's eq. 8 is a pair rate; their eq. 9 counts photons.
- **In-out vs in-in.** "In-out" is an S-matrix probability for a pair final state. At O(G²) it equals the in-in mean number of pairs for the same initial state. B&O and this check differ in the initial state and field, not in this bookkeeping.
- **Rate vs total.** "Rate" means pairs per unit time; "total" means pairs over the whole history. Numbers are totals over the whole packet and not per volume, except eq. 14, which is per volume.
- **Provenance.** Every number below is printed by a script in `calc/`, with its log in `notes/`.
  - The fast and medium scripts were re-run in the foreground on 2026-10-12 and matched their stored logs exactly.
  - The long scripts were re-run earlier the same day, and their logs match the original runs: `taskA3b --part bo_plus/module`, `taskA4 --part bo/physical`, `taskC2`, `taskD2 --part a/c`, `challenge_delta_1_usage`/`vector_quad`, `challenge_stochastic_1_indep`, `challenge_reproduce_1_t8 --part ring2/scalar`.
  - The one difference is `taskC2`, which now uses 4e7 samples; its log was updated.
- **Quotes.** B&O are quoted only from `fetch_text.py --grep` output. The PDF extraction drops spaces and splits hyphenated words, and quotes keep those artefacts.

## 1. Bottom line

**Within B&O's idealised model the calculation is right.** This covers:
- the tree-level magnitudes of gg → γγ (eq. 6) and gg → φφ (S10);
- the S6 integral, giving dP/dt = 3G²N²ω³σ²/(25π) pairs per unit time (eq. 8);
- the stochastic-background rate 8πG²ρ²/15 per volume (eq. 14);
- the drop-out of coherent intermediate gravitons (SA);
- the ħ counting (eqs. 11-12).

**The model does not describe a gravitational wave travelling away from its source.** There are two separate defects.

1. **Helicity phases are dropped.**
   - Eq. 7 adds the eq.-6 amplitudes as real positive numbers, and no phase convention makes them all real at once.
   - For physical coherent states the coefficient becomes 0.25-0.60 of 3/(25π), depending on the polarisation pattern. It is exactly 0 for a circularly polarised wave.
2. **The field is wrong.**
   - B&O's state |f> = S_source|0>, used as an *in*-state, carries the Pauli-Jordan field: an incoming spherical shell that focuses on the source position and then re-expands.
   - Almost all of the eq.-8 probability is generated at that focus, within about a wavelength of the source, around the emission time.
   - The 2πδ(0) → T step turns a finite in-out total of (4/25)G²N²ω³σ pairs into a "rate". That rate is the peak of a sinc⁴ time profile with effective duration 4π/(3σ).

**A physical outgoing wave produces pairs only near its source.**
- The yield beyond r_min falls as r_min⁻³. The rate while the shell passes radius r falls as r⁻⁴.
- So there is no sustained decay, no reaction time and no depletion along the path.
- This contradicts eqs. 9-12, S7, footnote 4 ("sphere of radius τ") and the eq. 19/S12 cosmological integration.

**Near-source production is not computed.** Production within about λ/2π of the source depends on the source model.
- A crude quadrupole estimate there gives 0.3-0.7 of B&O's merger number.
- So we do **not** claim that B&O's merger numbers are orders of magnitude too large.
- We claim they describe the wrong process: near-source production while the source radiates, not decay of the wave in vacuum.

## 2. What the paper claims (verbatim, via fetch_text.py)

- **Abstract (p. 1):** "We show that gravitational waves (GW), treated as coherent graviton states, decay into photon pairs in vacuum. The process, even if suppressed byG 2, is lifted by two effects combined: the expected factor of the graviton number squared,N 2, and the coherence o"
- **Eq. 5 field (p. 2):** "far from the source, the classical field of Eq. (5) tends asymptotically to the outgoing spherical wave packet, hc µν(r−t)∝ cos(ωs(r−t)) r exp  −(r−t) 2σ2 ω/2  ."
  - This uses a Gaussian f_s. Eq. 7 and S6 use a top hat.
- **Eq. 6 (p. 2):** "A++++ =A−−−− = 8πG t2 s ,(6) A++−− =A−−++ = 8πG u2 s , where s = (k1 +k 2)2, t = (k1−q 1)2, and u = (k 1−q 2)2 are the usual Mandelstam variables."
- **Eq. 7 (p. 2):** "the fusion amplitude, as- suming an unpolarized graviton state, can be expressed as Aµ1µ2(q1,q 2)= 4πG (2π)6 Z d3k1 2k1 Z d3k2 2k2 fs(k1)fs(k2) (7) × s2−2tu s (2π)4δ(q1 +q 2−k 1−k 2)δµ1µ2. This expression is based on the use of the Feynman prop- agator in diagram 2) of Fig. 1."
- **Eq. 8 (p. 3):** "summing their helicities, with a factor 1/2 for photon indistin- guishability, giving (see SM SB) dP dt = 3G2N2ω3 sσ2 ω 25π .(8) Each reaction removes two gravitons and generates two photons."
- **Eqs. 9-10 (p. 3):** "Nγ(t)≈G 2N2 0 6ω3 sσ2 ωt 25π .(9) From this equation, the characteristic reaction time is τ= 25π 6G2E2 relωsσ2ω ,(10) withE rel =N 0ωs the total energy in the wave front of widthσ ω. Equation (8) is a probability per unit time for τ≪δt∼1/σ ω, with Poissonian uncertainty√σωτ."
- **ħ (p. 3):** "Being linear inℏ means that the quantumness of this number comes from the energy of photons, confirming the semiclassical origin for the gravitational field."
- **Depletion (p. 3):** "and is reduced as the GW decays, depleting at timeτ h =τE rel/ωs (cf. Eq. (10))."
- **Footnote 4 (p. 3):** "The flux can be estimated by interpreting this luminosity as the number of photons produced per unit time at the sphere of ra- diusτ."
- **CMB (p. 3):** "replaces 3 Wγ →W γ(1 + 2fγ(ωs)) in all the previous formulae"; footnote 3: "this effect is considered in the average sense."
- **Binning (p. 3):** "Dividing the GW into fractional bandwidth binsϵyields a lower bound on the emissivity, as any residual coher- ence between bins is neglected."
- **SB/S6 (p. 10):** "the remaining energy-conserving delta function is treated as 2πδ(0)→T, the interaction time, so that P/Tis the transition probability per unit time. This approximation improves for narrower bands sinceT∼1/σ ω, provided 1/σω≫τ, the reaction time"
- **Eq. 14 (p. 4):** "dP dtdV = 8πG2 15 ρ2 GW,(14) withρ GW the GW energy density. The number emissiv- ity is absolutely negligible, 2dP/dtdV≈10 −110 m−3s−1"
- **Effective volume (p. 4):** "for a coherent state the effective volume is reduced to 5λ 3 s/(9πϵ2), roughly a wavelength volume for the values ofϵwe consider"
- **S10 (p. 11):** "At ++ =− 8πGm 4 s (t−m 2)(u−m 2) =A t −−,A t +− =− 8πG(m 4−tu) 2 s (t−m 2)(u−m 2) =A t −+,(S10) the latter equalities follow from parity symmetry."
- **Scalars (p. 5):** "dP/dt= 7G 2N2 0ω3 sσ2 ω/450π. The result- ing reaction time isτ ϕ = (54/7)τ"; eq. 18: "Wϕ∼10 14xMW 10−21 eV mDM 2 v 10−3 3 W,(18)"
- **SE/S12 (p. 11):** "The total energy radiated by GW j and observed at redshiftzisE j(z) =W γ(1 +z) Rzj z dz′ (1+z′)4 (1+zj)6H(z ′), contained within the GW propagation sphere"

## 3. Verdicts

Legend:
- **confirmed**: the result is right, and it is about the right quantity.
- **RA-WQ**: right arithmetic, wrong physical quantity.
- **refuted**: the result is wrong.
- **undetermined**: not settled by this check.

| # | B&O claim | Verdict | Key numbers (script) |
|---|---|---|---|
| 1 | Eq. 6 magnitudes and zero pattern | **confirmed** as common-axis spin projections; physical-helicity reading **refuted** | Nonzero only for opposite physical graviton and opposite photon helicities; \|M\|/(8πG) = t²/s or u²/s to <1e-10 (taskA1). Third route (t8 KLT): max \|ratio−1\| 8.1e-15 head-on, 8.8e-9 over 200 lab configurations (challenge_reproduce_1_t8 amps) |
| 2 | Eq. 6 usable as real positive numbers, as eq. 7 needs | **refuted** | Rephasing-invariant arg I = +63.87, −17.09, −125.78° (taskA1; reproduced by challenge t8 invariant) |
| 3 | Eq. 7 coherent "unpolarized" amplitude | **RA-WQ** | Per head-on pair: physical 6.4 vs B&O 7.466667 (ratio 6/7); plus×cross 6.4 vs 5.333; R×R physically 0 (taskA2, challenge t8 pairs) |
| 4 | Eq. 8 / S6 coefficient 3/(25π) within the model | **confirmed** | sympy exact; engine ratio 1.000000000000 (taskA3); independent hand derivation (challenge_reproduce_1_analytic, challenge_spacetime_1_handS6) |
| 5 | δ(0) → T | **confirmed within the idealisation**; it gives the peak rate | P_total = (4/25)G²N²ω³σ pairs; T_eff = 4π/(3σ) = 4.18879/σ; R(t) = R(0) sinc⁴(σt/2) (taskC1; taskC2 MC; challenge_delta_1_vector_quad) |
| 6 | Eq. 8 for physical coherent states | **RA-WQ** | C/(3/(25π)): bo_plus 0.25391, binary 0.604477, linear 0.337429, circular 0 (taskA3b). Independent integrator: 0.2533 / 0.6045 / 0.3374 |
| 6a | Eq. 8 coefficient as a property of N, ω, σ alone | **refuted**: it depends on profile shape and polarisation pattern | Gaussian (eq. 5's profile) vs top hat (eq. 7's), at equal N and σ: peak rate ×4π, P_tot ×3.7599 (taskC1 (e), critic_report_checks) |
| 7 | Eq. 5 field "tends asymptotically to the outgoing" packet | **RA-WQ**: true at late times, but the in-state carries the Pauli-Jordan field | In-fraction 1.000 at tω = −30 and 0.500 at 0 (Gaussian, l=0); the retarded field has in-fraction 0 at all t (taskB_field_structure) |
| 8 | Where the eq.-8 probability is generated | **RA-WQ**: at the focus | l=0: 0.850 inside 1λ, 0.0225 outside 1λ. l=2 is spread over 1-2λ: 0.494 inside 1λ, 0.821 inside 2λ (taskB_where_grid) |
| 9 | V_eff = 5λ³/(9πε²) | **RA-WQ** | 17.68λ³ at ε = 0.1; this is the focal region (taskB_pj_exact, taskD1) |
| 10 | Algebra of eqs. 9, 10, S7 | **confirmed** | Eq. 9 at t = τ gives exactly 1 photon, so τ is the time to the first photon (taskC3, challenge_spacetime_2) |
| 11 | Sustained decay, depletion at τ_h, footnote-4 sphere | **refuted** | Yield beyond r_min ∝ r_min⁻³ (local slope −3.000 at 1000λ, taskB_outgoing); same for l=2 (taskB_outgoing_l2) |
| 12 | Steady-source L_γ (Fig. 2) | **RA-WQ**; comparison with true near-zone production **undetermined** | B&O as applied: 0.0382 G²L²ω. Outgoing wave beyond λ (monopole proxy × C_coh): 3.6e-5. l=2 at r_min = 1/ω: about 0.3-0.7 of B&O (challenge_spacetime_1_nearzone, challenge_spacetime_2) |
| 13 | Binning gives a "lower bound" | **refuted** (it is an overestimate); size **contested** | Eq. 8 / in-out average over a chirped bin ≈ (σt_ε)²/(4π²). Inside B&O's allowed region: max 6.991e3, median σt_ε = 2.684, i.e. O(1) (challenge_delta_1_usage (d), taskC3 (d)) |
| 14 | Eq. 19/S12: each event radiates W_γ for the whole propagation time | **refuted** | Energy per event in their own model is W_γ × 4π/(3σ). S12 overcounts by 3σ/(4πH), e.g. 1.66e21 at ω_s = 1e-10 eV, z = 0 (taskC3 (c), challenge_delta_1_hbar) |
| 15 | ħ counting of eqs. 11-12 | **confirmed** | Pair rate is ħ-free at fixed classical (E, ω, δ); W_γ ∝ ħ¹; eq. 12 = eq. 11 iff dt = 1/δ (taskC4) |
| 16 | "N² coherent enhancement" | **confirmed as classical phase coherence**; its size is set by the idealised focus | P_tot = (1/400)h⁴(ωr)⁴(ω/δ), ħ-free (taskC4 (iii)); eq. 14 is also N² (taskC4 (iv)) |
| 17 | Eq. 14 = 8πG²ρ²/15 | **confirmed** | Γ/ρ² = 1.675516081915 for any isotropic unpolarised spectrum (taskD1, taskB_luminosity_check); MC 1.67540 ± 0.00090 (challenge_stochastic_1_indep) |
| 18 | Emissivity ~1e-110 m⁻³ s⁻¹ | **confirmed**, at the low end | 2Γ = 5.19e-109 photons m⁻³ s⁻¹ at ΔN_eff = 0.29; 1e-110 needs ΔN_eff = 0.040 (taskD1 (d)) |
| 19 | Eq. 15/S9, \|Φ\| ~ 1e-25 Hz⁻¹ | **confirmed** | \|Φ\| = 3.16e-25 s with constant g_*, 5.09e-25 s with g_* steps (taskD1 (e)); plasma caveat in §4.4 |
| 20 | CMB factor 1+2f "in the average sense" | **confirmed** as an approximation | The exact factor is 1+f₁+f₂. Its average is 5% (ring model) to 8% (incoherent gas) above 1+2f in the Rayleigh-Jeans limit (taskD2) |
| 21 | SA: coherent intermediate gravitons drop out | **confirmed** at tree level | Displacement identity holds exactly; collinear on-shell vertex vanishes to 4e-16 (taskD3) |
| 22 | S10 helicity amplitudes | **confirmed**; labels are physical helicities, unlike eq. 6 | max \|module/S10 − 1\| = 7.3e-12 (taskA4 amps; challenge t8 scalar at m = 0) |
| 23 | 7/(450π), τ_φ = (54/7)τ, S11 at m = 0, within the model | **confirmed** | scalar/photon = 7/54 exactly (taskA4, taskD4, challenge_reproduce_1_analytic) |
| 24 | Same, for physical states | **RA-WQ** | C/(7/(450π)): binary 0.474540, linear 0.265626, bo_plus 0.198875 (independent coarser grid: 0.1916), circular 0. Physical τ_φ/τ = 9.80-9.85, not 54/7 = 7.71 (taskA4 physical; challenge_stochastic_1_indep H) |
| 25 | Finite-m S11 interference term | **undetermined**; S11 is the coherent real-sign model | S11 / coherent model = 1.000000 to 1.000021; incoherent / S11 = 0.64-1.00 (taskA4 bo) |
| 26 | Eqs. 16-17 (ULDM occupation; resonant coefficient 1/16) | **confirmed** | Coefficient 0.0624997 at δ = 1e-6 (taskD4; challenge_stochastic_1_indep E) |
| 27 | Eq. 18, W_φ ~ 1e14 W | **right arithmetic for a different quantity** (3.78e13 W); applicability **undetermined** | Crude band-filling estimate suppresses it by ~1.1e-12; the resonant band needs 1/(mv²/2) = 4.2e4 yr vs t_m = 1.4e6 s (taskD4 (4)) |
| 28 | C_coh = 0.409, used only in our in-in numbers | **undetermined** | Module only (taskB_ring_coherence) |
| 29 | B&O's validity condition τ ≪ δt ~ 1/σ at the merger anchors | Holds **only with** CMB stimulation | Vacuum: τ/t_m = 7.2e5. With (1+2f): τ = 4.7e-6 s, τ/t_m = 9.5e-4 (critic_report_checks) |

## 4. Evidence by topic

### 4.1 Amplitudes, labels and phases (Task A)

**Three independent routes agree on the full complex amplitude:**
1. qft_second_order, the new module.
2. A spinor-helicity KLT closed form in `bo_common.py`, which does not import the module. The module/spinor ratio is 1 to 1e-12 for random lab kinematics and random complex TT tensors (taskA1).
3. A covariant t8F⁴ KLT route with no spinors (`challenge_reproduce_1_t8.py`). Its normalisation C0 = 1/16 is calibrated at one point; the shapes, zeros and phases are predictions.

**Helicity labels.**
- In physical helicities, only (+2,−2) or (−2,+2) gravitons with opposite photon helicities give nonzero amplitudes:
  - |M| = 8πG u²/s for (2,−2,1,−1);
  - |M| = 8πG t²/s for (2,−2,−1,1).
- Eq. 6 is reproduced only if its labels are spin projections on a common axis: the graviton axis along k₁ and the photon axis along q₂.
- A rephasing-invariant product shows that no phase convention makes all the eq.-6 amplitudes real at once (item 2). So eq. 6 is right for |M| only.

**What this does to eq. 7.**
- The J_z = +4 and −4 channels cannot interfere once the photon azimuth is integrated. Their cross term goes as cos 8φ and has zero mean; its amplitude at 40° is 0.170714 = t²u²/s².
- B&O's real-coefficient rule keeps that cross term as a constant.
- The same rule makes the rate depend wrongly on the relative orientation of two linear polarisations: 5.333 vs the physical 6.4 for plus×cross.
- Read literally (f_l f_l A_ll), eq. 7 gives a nonzero rate for R×R, which is physically zero.

**Physical coherent shells.** The "unpolarised isotropic" state has no unique physical realisation (hairy-ball theorem). Coefficients C/(3/(25π)) for the patterns tried:

| Pattern | Spinor engine | Independent integrator (challenge) |
|---|---|---|
| Literal real-f shell (bo_plus) | 0.25391 | 0.253343 (still converging upward; the pattern is singular at the poles) |
| Circular-binary quadrupole | 0.604477 | 0.604489 |
| Linear quadrupole | 0.337429 | 0.337436 |
| Pure circular | 0 | — |

- The spinor engine agrees with the module to ≤5e-11 on identical grids.
- On the linear-quadrupole profile, B&O's own model gives 0.891084.
- So eq. 8 overestimates by 1.7× to 4×, and the factor depends on the pattern.

**Profile dependence (new in this critic pass).**
- B&O state eq. 5 with a Gaussian f_s but evaluate eq. 7 and S6 with a top hat.
- At equal N and equal σ parameter, the Gaussian gives a 4π larger peak rate and a 3.7599× larger total (taskC1 (e), critic_report_checks).
- At equal rms bandwidth Δ, the totals are 0.5543 (top hat) and 0.8508 (Gaussian) G²N²ω³Δ.
- So "3/(25π)" is specific to the top hat. The effect is an O(1)-O(10) factor.

### 4.2 The 2πδ(0) → T step (Tasks A and C)

**Kept exactly, the energy delta gives a finite in-out total.**
- P_tot = (4/25)G²N²ω³σ pairs, i.e. 0.16 in these units. The value approaches this limit (0.1592265 at σ/ω = 0.01).
- The pair production follows R(t) = R(0) sinc⁴(σt/2), with R(0) equal to eq. 8. For example, taskC1 (d) gives 0.49946 at σt = 2, against the sinc⁴ value 0.50137.
- So eq. 8 is the *peak* rate, and T_eff = 4π/(3σ).

**Cross-checks.**
- sympy: the Irwin-Hall density is 2/3.
- Exact-kinematics quadrature.
- Monte Carlo (taskC2): 0.15253 ± 0.00012 at σ/ω = 0.1, against the quadrature value 0.15265.
- An independent explicit-vector quadrature (challenge_delta_1_vector_quad) agrees to 7 digits.

**Steelman.** B&O take T ~ 1/σ, so their idealisation is legitimate as an average rate over the packet.

**What breaks** is using that rate as a constant over times ≫ 1/σ.
- Eq. 9 exceeds the in-out total for t > 4π/(3σ).
- In B&O's own model, the fraction of a packet ever converted is (4π/3)/(στ_h). For their SB example (E_rel = M_⊙c², ε = 0.15, ω_s = 1e4 eV) that is 2.4e-36, not "depletion" (taskC3 (b)).

### 4.3 Space-time structure (Task B)

**The B&O in-state is the free Pauli-Jordan field.**
- It is incoming at early times (in-fraction 1.000 at tω = −30 for the Gaussian shell) and outgoing at late times.
- At t = 0 it forms a focus. The focus amplitude is 2.00 ωr_obs (l=0) or 0.60 ωr_obs (l=2) times the shell amplitude at radius r_obs (taskB_field_structure).

**Steelman.**
- After the source switches off, the advanced field vanishes, so the Pauli-Jordan field equals the retarded field there. B&O's statement that the field tends to the outgoing packet is therefore true.
- B&O also note that they use the Feynman propagator for the *internal* graviton, and that the extra term vanishes against coherent states.

**Why the steelman fails.**
- The problem is the *external* state. The S-matrix integrates over all times, including the fictitious incoming half of the field.
- The claim that the relevant field is the retarded, outgoing-only one when the source is kept inside the time-ordered product is an analytic argument. It was not checked numerically.

**Where the probability arises** (taskB_where_grid):
- l=0: windows inside 0.5/1/2λ keep 0.608/0.850/0.953 of the total. Removing the focus (keeping only r > 1λ) leaves 0.0225.
- l=2 is more spread out: 0.093/0.494/0.821 inside 0.5/1/2λ.
- The time-resolved rate peaks at t = 0 with FWHM ~1.5/σ.
- B&O's "effective volume", 17.68λ³ at ε = 0.1, is this focus (taskB_pj_exact).

**A physical outgoing wave.** This is the outgoing half of B&O's packet, switched on beyond r_min:

| r_min | Yield / B&O exact total (× C_coh) |
|---|---|
| λ/2π | 1.75e-3 |
| λ | 2.4e-5 |
| 10λ | 2.9e-8 |
| 100λ | 3.0e-11 |

- The local slope tends to −3.000. Three window shapes give coefficients that differ by up to 2.2×.
- The rate while the shell passes radius r goes as r⁻⁴.
- This is a formation-length effect: pairs at radius r have s ~ 4ω/r.
- l=2 with its near-field terms behaves the same way, with K_l2/K_l0 → 15/7 (taskB_outgoing, taskB_outgoing_l2).
- An independent radial transform gives local slopes −2.70 and −2.86, trending to −3 (challenge_spacetime_2 C).

**GW150914-like anchors** (E_rel = 2M_⊙c², 150 Hz, t_m = 5 ms; SI). B&O's numbers as applied:
- dP/dt = 1.3975e-4 pairs/s.
- τ = 3.5779e3 s.
- Rate × t_m = 6.987e-7 pairs.
- Photon rate 2.795e-4 /s, or 2.1164e5 /s with 1+2f, where f(150 Hz) = 3.786e8.

In-in yield of the outgoing wave over the merger (monopole proxy × C_coh × binary factor g; taskB_outgoing (i)):

| Beyond r_min | Pairs | × (1+2f) |
|---|---|---|
| λ/2π (318 km) | 1.9e-9 | 1.4 |
| λ (2000 km) | 2.6e-11 | 0.020 |
| 10λ | 3.2e-14 | — |

**Near zone (weakened by challenge).**
- A quadrupole wave including its 1/r² and 1/r³ terms gives 254.5× the monopole yield at ωr_min = 1. Our own two windows give 111-126×.
- That lifts the 318 km number to 2.1e-7 to 4.9e-7 pairs, which is 0.30-0.70 of B&O's rate × t_m (challenge_spacetime_1_nearzone, challenge_spacetime_2 D).
- But 1/k = 318 km is about the Kepler separation (339 km, v = 0.53). So r ~ λ/2π lies inside the strong-field source region, which is not modelled (challenge_spacetime_1_source_scale).
- Conclusion: production beyond about λ is robustly small and falling. Production inside the source region is comparable to B&O's number and depends on the source model.

**Footnote-4 sphere and the validity condition** (critic_report_checks):
- **Vacuum:** cτ = 1.07e12 m = 5.4e5 wavelengths, and τ/t_m = 7.2e5. B&O's condition τ ≪ δt fails.
- **With CMB stimulation:** B&O apply (1+2f) "in all the previous formulae". Then τ = 4.7e-6 s and τ/t_m = 9.5e-4, so the condition holds. The sphere radius is cτ = 1.4 km, about 7e-4 wavelengths, deep inside the source region.
- An earlier challenge said the condition "fails by six orders of magnitude". That is true only without stimulation and is corrected here.
- Either way the qualitative conclusion stands: physical production happens at the source while it radiates.

**Steady source** (taskB_outgoing (g)):
- B&O's mapping (N = E/ω, σ = 1/t) gives (3/(25π))G²L²ω = 0.0382 G²L²ω.
- The free Pauli-Jordan standing wave of the same luminosity gives 1.34 G²L²ω (32π/75, scalar proxy).
- An outgoing wave beyond λ gives 3.6e-5 (× C_coh), or 1.4e-6 with the binary factor g = 0.0397.

### 4.4 Stochastic background, CMB, cosmology, scalars (Task D)

**Eq. 14** is exact for any isotropic unpolarised spectrum, because σv ∝ k₁k₂ factorises (taskD1 (c)).
- Same-helicity pairs give zero.
- Eq. 14 does not distinguish the two readings of eq. 6's labels only when the helicity fraction is p = 1/2. For a polarised background the rate is 4p(1−p) × eq. 14.
- Eq. 14 describes a homogeneous background, so the focus problem does not affect it.

**Emissivity.**
- 1e-110 m⁻³ s⁻¹ corresponds to ΔN_eff = 0.040.
- At the 2σ bound ΔN_eff = 0.29 it is 51.9× higher, and still negligible (challenge_stochastic_1_indep C).

**|Φ| ~ 1e-25** is confirmed: 3.16e-25 s (taskD1 (e)).
- Plasma caveat: in the relativistic e⁺e⁻ era, photons of energy ~k are below the plasma cutoff (k/T = 1.8e-9 at 100 Hz).
- So integrating S9 to z ~ 1e28 overstates even this tiny depletion.

**CMB 1+2f.**
- The net-rate formula N₁N₂(1+f₁+f₂) − f₁f₂(1+N₁+N₂) is reproduced by exact short-time evolution (taskD2 (a)).
- In the Rayleigh-Jeans limit the averaged factor is 1.0496× (ring model) to 1.0787× (incoherent gas) larger than 1+2f.

**SA** is confirmed by the displacement identity and by the vanishing of the on-shell collinear 3-point vertex: max |ε·T| = 4.08e-16 (taskD3).

**Scalars.**
- S10, 7/54 and 1/16 are confirmed within the model.
- For physical states the scalar coefficients are 0.27-0.47 of 7/(450π), and τ_φ/τ ≈ 9.8 instead of 54/7.

**Eq. 18** (taskD4).
- The arithmetic gives 3.78e13 W, against B&O's "~1e14".
- But the resonant band (mv²/2 = 7.6e-13 s⁻¹) is about 1e-6 of the merger bandwidth.
- The τ ≪ 1/σ requirement would also need 4.2e4 yr.
- So whether eq. 18 applies to a merger is doubtful.

### 4.5 ħ and the N² enhancement (Task C)

- Eq. 8 and P_tot contain no ħ at fixed classical (E_rel, ω, δ).
- The pair number is a quartic functional of the classical strain: P_tot = (1/400)h⁴(ωr)⁴(ω/δ).
- B&O's "linear in ħ" remark and their semiclassical reading are therefore right.
- The N² is (E/ħω)², compensated by G²/(ħc⁵)². It is not a quantum-coherence bonus.
- Its *size* comes from a small effective volume, the focus, not from an extra power of N. Eq. 14 is also quadratic in graviton number.

## 5. Use of the new modules, and independent cross-checks

| Module output used | Independent cross-check | Status |
|---|---|---|
| amplitude_gg_to_photons (complex, any tensors) | Spinor KLT (bo_common.py); covariant t8 KLT (challenge t8) | Agree to 1e-12 / 8.8e-9 |
| Massless and massive scalar amplitudes | S10 closed form; spinor <3\|1\|4]⁴/(s₁₂s₁₃s₁₄); t8 at m = 0 | Agree to 7e-12 |
| sigma_total, beams_pair_rate | Own quadrature of the closed form; BHPV eq. 5.6 Compton crossing; lab-frame Monte Carlo | Agree to 4.5e-15; MC to 1e-3 |
| Physical-shell coefficients | Spinor engine (primary); independent integrator (challenge) | Binary and linear agree to ≤0.01%; bo_plus within 0.2% after grid refinement |
| **C_coh = 0.409** (ring coherence) | **None** | **Undetermined.** It enters only our in-in near-zone and steady numbers, as an O(1) factor. No verdict rests on it |
| qft_production | Not used | — |

**Usage caveats for the modules.**
- Exactly collinear configurations carry a physical phase discontinuity, so coherent integrals need dense sampling near the poles.
- beams_pair_rate's "local rate × overlap volume" picture fails for a single curved wave: it gives r⁻⁵ where the exact answer is r⁻³.

## 6. Open questions and remaining caveats

1. **Near-source production (r < λ/2π) is not computed.** It needs the binary's near-zone field and matter-graviton vertices, and the scalar proxy and C_coh may not hold there. This is why item 12 is undetermined.
2. **The retarded-field claim is analytic only.** The statement that the physical in-in field is the retarded one (source inside the time-ordered product) was not checked numerically.
3. **Attributing yield to "r > r_min" is window-dependent** up to log² factors: window-free 5.4e-4 vs windowed 8.6e-5 at λ. The r⁻³ scaling is robust.
4. **The finite-m scalar channel is incomplete.** The physical replacement for S11's same/opposite-helicity interference term was not computed.
5. **The physical polarisation pattern is not unique.** No unique pattern corresponds to B&O's isotropic idealisation. The patterns tried give 0.25-0.60; a circularly polarised wave gives 0.
6. **Eq. 6 and S10 use different label conventions** (common-axis vs physical). This is harmless for B&O's f₊ = f₋ states but matters for any polarised application.

## 7. Scripts and logs

All scripts are in `calc/` and all logs in `notes/`. Run them from the check folder with `python3 calc/<script> [args]`.

- **Task A**
  - `taskA1_helicity_labels.py`
  - `taskA2_pair_phases.py`
  - `taskA3_S6_rate.py`
  - `taskA3b_physical_shell.py --part {bo_plus --grid 1|2, smooth, aux, module}`
  - `taskA4_scalar_channel.py --part {amps, bo, physical}`
  - Shared: `bo_common.py`, `bo_ring.py`
- **Task B** (index: `notes/taskB_scripts.txt`)
  - `taskB_field_structure.py`
  - `taskB_pj_exact.py`
  - `taskB_where_grid.py`
  - `taskB_outgoing.py`
  - `taskB_outgoing_l2.py`
  - `taskB_luminosity_check.py`
  - `taskB_ring_coherence.py`
  - Shared: `taskB_common.py`
- **Task C**
  - `taskC1_exact_Ptot.py`
  - `taskC2_mc_Ptot.py`
  - `taskC3_usage_consistency.py`
  - `taskC4_hbar_classical.py`
- **Task D**
  - `taskD1_sgwb_rate.py`
  - `taskD2_cmb_stimulation.py --part {a,b,c}` (the full run takes more than 10 minutes)
  - `taskD3_SA_coherent_intermediate.py`
  - `taskD4_uldm.py`
- **Challenges**
  - `challenge_reproduce_1_analytic.py`
  - `challenge_reproduce_1_t8.py --part {amps, invariant, pairs, scalar, ring2}`
  - `challenge_spacetime_1_handS6.py`
  - `challenge_spacetime_1_nearzone.py`
  - `challenge_spacetime_1_source_scale.py`
  - `challenge_spacetime_2_numerics.py`
  - `challenge_delta_1_{hbar,usage,vector_quad}.py`
  - `challenge_stochastic_1_{indep,forward_jz}.py`
- **Critic pass**
  - `critic_report_checks.py`: the validity condition with and without CMB stimulation, and the Gaussian/top-hat ratio.
- **Notes**
  - `notes/taskA_derivation_notes.md`: normalisation and helicity-label derivation.

## 8. Corrections (2026-10-27)

Found while writing the reader's summary (`summary/`), by two adversarial reviewers checking it against this report and the logs.
- **Section 1, near-source production.** The 0.3-0.7 estimate counts pairs made *beyond* r_min = λ/2π by the quadrupole wave with its near-field terms. Production *inside* λ/2π is what was not computed. "A crude quadrupole estimate there" should read "just outside it".
- **Section 2, abstract.** The truncated quote ends "and the coherence of the wave" (fetch_text.py on the arXiv abstract page, 2026-10-27).
- **Item 13, binning.** The overestimate (σt_ε)²/(4π²) is computed only for bins lasting many cycles (σt_ε > 50 in `challenge_delta_1_usage.py`). The median allowed bin has σt_ε = 2.684, where the formula does not apply and no ratio was computed. "Refuted" should be read as "not a guaranteed lower bound", and the size is open, not just contested.
- **Section 5 and the README.** No script imports `qft_production.py`. Fourteen import `qft_second_order.py`. The README sentence saying otherwise is fixed.
- **Item 9.** ε = 0.1 is this check's choice. B&O's worked examples use ε = 0.15, where V_eff = 7.86 λ³ (`notes/taskB_pj_exact.log`).

=== END CONTENT ===

Files written or changed this pass, all in `/home/user/Science/checks/2026-10-11-blas-oller-gw-decay/`:
- `calc/critic_report_checks.py`
- `notes/critic_report_checks.log`
- `notes/taskB_field_structure.log`
- `notes/taskB_luminosity_check.log`
- `notes/taskB_outgoing.log`
- `notes/taskB_outgoing_l2.log`
- `notes/taskB_pj_exact.log`
- `notes/taskB_ring_coherence.log`
- `notes/taskB_where_grid.log`
- `notes/challenge_spacetime_1_handS6.log`
- `notes/challenge_spacetime_1_nearzone.log`
- `notes/challenge_spacetime_1_source_scale.log`
- `notes/challenge_spacetime_2_numerics.log`
- `notes/taskC2.log` (updated)
- `notes/taskD2_a.log`
- `notes/taskD2_b.log`
- `notes/taskD2_c.log`
- `notes/taskB_scripts.txt` (last line edited)
