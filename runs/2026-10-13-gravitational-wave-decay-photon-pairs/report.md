# Do gravitational waves decay into photon pairs in vacuum? (test of Blas & Oller, arXiv:2607.24930): report
*Run 2026-10-13-gravitational-wave-decay-photon-pairs · 2026-10-14 · depth deep · question: "Do gravitational waves decay into photon pairs in vacuum, as Blas & Oller claim in 'Gravitational waves decay in vacuum' (arXiv:2607.24930)? Test their central result, the coherent-state graviton-fusion rate for g g → γγ, dP/dt = 3G²N²ω_s³σ_ω²/(25π) (their eq. 8): is it computed correctly, and is it the physically right quantity for a gravitational wave emitted by a real source ...? Then test the consequences they draw from it ..." (full wording in brief.md)*

Units: natural (ħ = c = 1) for coefficients and amplitudes; SI for astrophysical numbers, as marked. B&O = Blas & Oller v2. GW150914 inputs are B&O's (E = 2 M☉c², 150 Hz, σ_ω = 200 rad/s) unless stated. "Pairs" = photon pairs.

## Bottom line
No. Blas & Oller's arithmetic is right inside their model, but their eq. 8 is not a decay rate of a travelling wave. It is the total number of photon pairs (about three millionths of a pair for a GW150914-like merger) that their idealised, time-symmetric graviton packet makes once, near its focus, divided by the packet's duration. Reading it as a rate sustained along the path over-counts by 18 orders of magnitude and breaks the paper's own validity condition. Far from its source a wave becomes locally plane, plane waves make nothing, and whatever can fuse thins as 1/r². Confidence about 90%. Every consequence they draw falls or is unobservable by at least 30 orders of magnitude; near a real source the source's own field makes about 100 times more pairs than fusion, still unobservable.

## Ranked answers
| # | Candidate | In principle | In practice (horizon) | Key obstacle | Gap (orders of magnitude) | Credence |
|---|---|---|---|---|---|---|
| 1 | C6: sustained fusion only in multi-directional ensembles; eq. 14 = kinetic rate (8π/15)G²ρ², negligible | Yes: exact identity, re-derived by crossing the published Compton cross-section and by Monte Carlo; holds for unpolarised baths at T ≪ M_Pl | Unobservable at any planned sensitivity; < 1 pair per Hubble volume per Hubble time | Squeezed primordial correlators uncomputed; Sawyer's collective channel inert for allowed backgrounds | ≥ 71 (vs FIRAS μ); PIXIE-class headroom only 3–4 | 0.92 |
| 2 | C2 (null, narrowed): an outgoing wave's self-fusion converges (≤ 1/R by energy conservation; toys R⁻³); only ambient-background crossing gives a formal lifetime ≥ 5e124 s; nothing observable | Yes: free waves have null Fourier support; 1/r² dilution bound; plane-wave no-go results | Only large damping is testable (standard sirens ~1e-2) and is already excluded | No spin-2 in-in retarded calculation; memory and tails uncomputed; "within a few wavelengths" is toy-based | ≥ 72 (converted energy fraction vs siren reach) | 0.90 |
| 3 | C7 (narrowed): the N² yield is semiclassical second-order pair creation by the classical wave, ħ-free in pair number; not pair creation on h^(2) | Yes at tree level: background-field amplitude = coherent-state amplitude = kinetic rate; ħ counting verified | The ħ-free spontaneous term is 7.6e8 below the CMB-stimulated part, itself unobservable | Named mechanism (h^(2)) refuted; equivalence checked only for beams; "classical" overstated | n/a (interpretive) | 0.85 |
| 4 | C5 (narrowed): near a real source, pairs come mainly from the source's off-shell linear channel, N_lin = 0.034 G ω E/c⁵, ~100× B&O's fusion total | Yes: k = 67/(630π) computed; Redi–Tesi and Han–Lykken–Zhang normalisations agree; weak-field inspiral case robust | ~3e-4 pairs per GW150914; Hz-band photons evanescent in the ISM | Merger is strong-field (ka ≈ 1.07): k uncertain by O(1); flat-space linear formula applied to a BH binary | ≥ 40 (flux vs CMB foreground) | 0.80 |
| 5 | C3 (narrowed): eq. 8 is the per-packet yield of a time-symmetric (Pauli–Jordan) shell; the outgoing wave beyond 2–3 λ/2π yields 0.003–0.05 of it; a circular source's whole retarded total is ~0.003 (scalar toy) | State identity verified and backed by B&O's wording; "less" shown only in scalar toys; m = 0 sources can yield more | Changes nothing observable | Spin-2 selection rule: can a J_z = +2 rotator's near zone carry an orbital L = 0 part? | n/a | 0.65 |
| 6 | C4′: the N² fusion sub-piece of a real source is within ~3× of eq. 8 × T_eff (total, dominated by the linear channel, finite and unobservable) | Qualitative parts stand; size clause conceded (total ≈ 100× B&O); O(1) fusion share contradicted by every circular-pattern toy | Unobservable | Needs the r < c/ω strong-field region to restore O(1); computed nowhere | 2 (original size clause) | 0.25 |
| 7 | C8: GW → ULDM pairs at astrophysically relevant rates (eqs. 16–18) | No: eq. 17 needs a 5e-7 fractional band held for 1.3e12 s; a chirp supplies 12 s; an outgoing wave has no head-on pairs | ≤ 2 W·x_MW; fiducial masses disfavoured; no SMBH binary detected | Internal inconsistency: a 0.21-bandwidth merger fed into a 5e-7 resonance | 11–13 (power); 31 (W_φ/L_GW even at face value) | 0.03 |
| 8 | C1: sustained vacuum decay at the eq. 8 rate, lifetime τ_h, path depletion | No: the S-matrix total is finite (2.9e-6 pairs); the sustained reading over-counts 2e18; τσ = 7.2e5 breaks B&O's own condition; kinetic ceiling falls as r⁻² | Depletion 3e-66 unobservable; variant (b) excluded by GW150914's detection | No mechanism keeps a locally plane wave non-collinear | 18 (over-count); 38 (ceiling at 410 Mpc); 14 (variant b) | 0.02 |

Credences are independent viabilities (the slate is non-exclusive). C3 and C4′ compete on one sub-question (the size of the fusion sub-piece); they are split 0.65/0.25 with ~0.10 for neither (strong-field surprises).

## Why, candidate by candidate

**C6.** For: eq. 14's 8π/15 is reproduced by isotropic kinetic theory [M-CONSTRAINTS-01, M-DIALECTICIAN-09, M-IDEALIZER-05], by a Monte Carlo over three spectra (C6-0), and by crossing the published unpolarised gravitational-Compton cross-section [D-01] (C6-1), so it no longer rests on the toolkit; B&O's own substitution 3/(25π)·40π²/9 = 8π/15 is an identity, and their S8 P-representation is phase-randomised. The rate at ΔN_eff = 0.3 is 2.8e-109 pairs m⁻³ s⁻¹ (SI), ≥ 1e71 below FIRAS; conversion per Hubble time reaches O(1) only at T ≈ 0.4–0.9 M_Pl. Against: Sawyer's collective channel (G n scaling) accumulates an exponent ≤ 0.24 against the ~200 needed (C6-1). Test: in-in yield of two crossing coherent beams (cheap). 2× mover: a non-kinetic coefficient for phase-locked ensembles.

**C2.** For: a free wave's Fourier support is null [M-EXAMINER-06, exact]; the local rate (2π/5)G²T_mnT^mn vanishes for null stress [M-IDEALIZER-06]; bound A, P(>R) ≤ (GE/c⁴)²/(cTR), follows from 1/r² dilution even with head-on kinematics everywhere (C2-2; re-run in crux-C2): 2.9e-6 pairs beyond λ, 4.6e-25 beyond 410 Mpc. Toys give R⁻³ [M-EXAMINER-04, M-CONSTRAINTS-08, M-IDEALIZER-08]. The one dissent with a number (Jones–Singleton, 1e11 m) is excluded by GW150914's detection (e-fold length > 5.3e25 m [M-CONSTRAINTS-14]); Chakraborty et al.'s linear production breaks on-shell momentum conservation (C2-1). Conceded: a real wave crossing the ambient background has a formal lifetime 5e124–2e128 s (C2-0), which is C6's process. Against: no spin-2 in-in calculation; memory and tails are scaling arguments; the exponent is window-dependent. Test: spin-2 in-in yield beyond R for a retarded quadrupole; C2 needs slope ≤ −1. 2× mover (down): any computed far-zone time-like support that does not shrink with R.

**C7.** For: with N = E/(ħω), eq. 8's rate is 3G²E²ωσ²/(25πc¹⁰) with d ln R/d ln ħ = 0 [M-DIALECTICIAN-03, M-CONSTRAINTS-04, M-IDEALIZER-03]; the full tree background-field amplitude equals the kinetic two-beam rate ω⁴h⁴(1−cos θ)²/(1280πc³) to 1e-12 and is G- and ħ-free at fixed strain (C7-0, C7-2). Against: the named mechanism is wrong. In TT gauge the h^(2) (s-channel) and contact pieces are exactly zero in B&O's J_z = ±4 channel and photon exchange carries 100% (C7-1 log); h^(2)-only yields are off by factors from 0 (head-on R/L) to ∞ (R/R at 90°); only the sum is gauge invariant. The advocate conceded this and the misreading of D-16. Test: coherent-state in-in pair number vs the full second-order background-field yield on the same ⟨h⟩ for a localised packet. 2× mover: a leading-order mismatch there.

**C5.** For: the coefficient C5 had left open is now computed: k = 67/(630π) = 0.0339 (C4-1, C5-0, C5-1 analytic; C5-2's 4D Born integral 0.036, falling to 0.025 with a finite source). The 8π/5 normalisation comes independently from Redi–Tesi's c_J = 16 (preprint) and the peer-reviewed Han–Lykken–Zhang spin-2 width, and the same T̃ reproduces the quadrupole luminosity to 1e-6. GW150914: N_lin = 3.1e-4 pairs vs B&O's 2.9e-6 (ratio 107); GW170817 whole chirp 3.8e-5 vs 2.8e-8 (1.3e3) (C4-1 log). These scripts share one model (quadrupole T̃ at time-like q), so they count as one computed result with a two-source normalisation check, not three. Conceded: Hawking emission removed (unpaired, not GW-induced); the channel runs through the inspiral too, since M-MECHANIST-10 tested only a local phase speed. Against: merger is strong-field, k uncertain O(1); Rahvar's preprint normalisation differs by 5e3 (if right, it favours C5). Test: NR metric through the full second-order functional, split by q₀ band. 2× mover: a merger k below ~0.003.

**C3.** For: B&O write "coherent states as initial states" and build eq. 5 with "the Pauli-Jordan function" (C3-1 quotes), which closes D-71a; G_ret − G_adv as a free field is an imploding-then-re-expanding shell [M-EXAMINER-01, M-MECHANIST-07]; self-terms have zero time-like support, so the whole yield is in×out cross-term [M-EXAMINER-02/05]; retarded/time-symmetric = 1/12 and 0.020 for the monopole (exact), 0.028 at GW150914's bandwidth (C3-2), and 2.9e-3 for the circular (2,2) pattern over all space (C3-2 log). Crux C6 adds a reading: eq. 8 equals the kinetic rate of the packet's N gravitons spread isotropically over V_eff = 40π²/(9ωσ²), a ball of ≈ 1 λ. Where advocate and refuters disagree (C3-0, C3-1: the l = 2 near zone reverses the inequality), the deciding assumption is the source's m: the (ka)⁻⁶ growth is the signature of an L = 0 part of ψ², present for m = 0 (linear) quadrupoles and absent for the m = ±2 field of a rotating binary (crux C3; C3-2's direct (2,2) result). Against: every input is scalar; in spin-2 the pair could carry J_z = +4 partly as spin, so an orbital L = 0 part is not excluded. Test: spin-2 ratio B/A for a rigidly rotating quadrupole, split at r = 2/k. 2× mover: that sub-result.

**C4′.** For: the idealizer's standing-wave proxy reproduces B&O to O(1) (R(>1) ≈ 1.1 after the plateau correction), and no toy includes the r < c/ω region. Against: the size clause was conceded (total ≈ 100× B&O via the linear channel); the proxy is time-symmetric and so supports C3; circular-pattern toys give ≤ 0.03; pattern factors 0.3–0.6 are unverified; the C4-2 interference "~10×" is bounded at ≤ 3 by the q₀-band overlap (crux C4). Test: same as C3; ρ > 0.3 favours C4′.

### B&O's claims, one by one (Q1–Q5)
| Q | Claim | Verdict | Basis |
|---|---|---|---|
| Q1 | Eq. 6 amplitudes 8πG t²/s, u²/s; same helicity 0 | confirmed | KLT re-derivation to 7e-15 [M-MECHANIST-01]; crossing of [D-01] |
| Q1 | Eq. 7 real-sign "unpolarised" sum | right arithmetic, not a realisable state | for one axis it is the azimuthal maximum; the azimuth-integrated rate is the incoherent sum; per-axis range [0, 12/7]×B&O [M-MECHANIST-02, corrected form] |
| Q1 | 3/(25π); 7/(450π); τ_φ = (54/7)τ | confirmed within model | 4/25 exact, T_eff = 4π/(3σ) [M-IDEALIZER-01/02]; finite band −4.6% at σ/ω = 0.1 |
| Q1 | Eqs. 9–12, ħ counting | confirmed within model | [M-IDEALIZER-03, M-CONSTRAINTS-04]; eq. 12's "(ħω)²" is dimensionally ħω² |
| Q2 | Eq. 8 as a sustained rate; τ_h = 1.3e82 s; depletion | refuted: right arithmetic, wrong quantity | in-out total finite, 2.9e-6 pairs; over-count 2.0e18; τσ = 7.2e5 (C1-0/1/2) |
| Q2 | 2πδ(0) → T | right as bookkeeping of a per-packet total (T_eff = 2πJ_f/I_f⁴); wrong as a sustained rate | [M-DIALECTICIAN-02] |
| Q2 | Coherent in-state = a source's outgoing wave | refuted | Pauli–Jordan in-state is time-symmetric (C3-1 quotes; [M-EXAMINER-01]) |
| Q3 | Single plane wave or free packet keeps fusing | refuted | null support [M-EXAMINER-06]; θ⁴ collinear law with π/5 [M-DIALECTICIAN-10 corrected]; bound A |
| Q4 | Fig. 2 luminosities; footnote-4 flux at r = cτ | fall as luminosities | per-event totals 1e-8–1e-5 pairs; chirp recipe over-estimates its own model by (σ_b t_b/2π)² = 36 (GW170817, 100 Hz), ~4e19 (WD), so the "lower bound" is an upper bound [M-DIALECTICIAN-06]; ceiling at cτ is 2e-12 of R (C1-2) |
| Q4 | Eq. 14; ~1e-110 m⁻³ s⁻¹ | confirmed as the kinetic rate; matches ΔN_eff ≈ 0.1 | (C6); negligible by ≥ 1e71 |
| Q4 | (1 + 2f_γ) stimulation | stands only where photons propagate | f_γ = 3.8e8 is a Rayleigh–Jeans extrapolation 9 decades below ARCADE-2; evanescent for n_e > 2.8e-4 cm⁻³ and 1+z ≳ 1270 at 150 Hz [D-62, M-CONSTRAINTS-09] |
| Q4 | Eq. 19/S12 and the Fig. 3 μ, y, EBL, photofission bounds | fall | over-count X = σt_prop = 6.6e21–6.6e41; energy conservation broken at 1e10 eV (CX = 34); corrected bound never beats ΔN_eff; Hawking bounds ≥ 3e2 stronger; photofission needs ≥ 2.2 MeV photons [M-CONSTRAINTS-06/07/11, D-64] |
| Q4 | Eq. 16 (N_φ ≈ 6e87) | confirmed | 5.75e87 [M-EMPIRICIST-01] |
| Q4 | Eq. 17 (v⁶, 1/128) | undetermined | not re-derived [M-EMPIRICIST-07]; the brief's "1/16" is absent from v2 |
| Q4 | Eq. 18 (~1e14 W x_MW), "stellar" luminosities | refuted as applied | arithmetic gives 3.8e13–8.6e13 W·x; resonance shortfall 9.2e-12; ≤ 2 W·x in band; 1 L☉ needs x ≥ 2e26 (C8-0/1/2) |
| Q5 | Any detectable or constraining regime | none within 20 years | every channel ≥ 1e30 below detectability [D-45–D-47]; only large damping is testable and is excluded |

## Eliminated, and what eliminated them
- **C1** — verdicts/C1-0.md (calculation: the in-out total is finite and made within ~1/σ of the focus; a sustained count scales as k⁶ under boosts along the ray; over-count 2.0e18), C1-1.md (internal inconsistency: S6 sets T ~ 1/σ while S7 integrates to τ_h; τσ = 7.2e5), C1-2.md (calculation: kinetic ceiling G²E²σ/(5c⁸r²) drops below R beyond 0.8 λ and is 1.6e-38 of R at 410 Mpc). Variant (b) would attenuate GW150914 by exp(−6.3e13) [M-CONSTRAINTS-14]. No advocate crux exists, so nothing was conceded or rebutted.
- **C8** — verdicts/C8-0.md (calculation: 12 s in band vs 1.3e12 s needed; outgoing multipoles contain no incoming part), C8-1.md (internal inconsistency: a merger of bandwidth ε = 0.1–0.21 fed into a 5e-7 resonance; Lyman-α and dwarf-galaxy mass bounds), C8-2.md (calculation: best case over all binary masses 1.6 W·x_MW). No advocate crux.

## Assumptions every surviving answer shares
- Tree-level GR-EFT plus Maxwell with flat-space propagators; loop and strong-field corrections are O(1).
- The local kinetic rate describes a coherent packet to O(1). The toolkit's coherent/kinetic ratios 0.98 and 0.93 are unverified [M-IDEALIZER-14]; equality is verified only for monochromatic crossing beams. If the proxy failed by a factor growing with r, C2 and C6's "only" clause would fall together and C1 would revive.
- Scalar toys (monopole and l = 2, contact or s² vertex) transfer qualitatively to spin-2 Einstein–Maxwell: the exponent is window- and vertex-dependent, the convergence is not.
- B&O's GW150914 inputs; E = 3 M☉c² multiplies pair numbers by 2.25; σ/ω = 0.21 lies outside the narrow-band model.
- Redi–Tesi's linear functional applies to a compact binary's near-zone field (an inference, with its normalisation cross-checked by HLZ).
- Cold unmagnetised plasma dispersion with the quoted densities.

## What would change this verdict
1. **A spin-2 in-in (Schwinger–Keldysh) photon-pair yield at O(G²) beyond radius R for the retarded field of a quadrupole source, including second-order memory and tails, with no ambient background.** Slope d ln P(>R)/d ln R ≥ 0 would revive C1 and overturn the headline; ≤ −1 would lift C2 above 0.95. Who: coherent-state waveform groups [D-02, D-03], Redi & Tesi, or B&O. Nothing is published as of 2026-10-13; it is a tree-level, months-scale calculation.
2. **The same calculation's total B/A relative to eq. 8 × T_eff for a rigidly rotating (J_z = +2) source, split at r = 2/k; and an NR merger metric through the full second-order background-field functional (not the h^(2) Redi–Tesi form, which gives zero in the J_z = ±4 channel), split by q₀ band.** B/A flat and ≪ 0.1 confirms C3 (→ ~0.85); growth as (ka)⁻⁶ moves C4′ to ~0.6. A merger k below 3e-3 drops C5 below 0.4; a strong-field suppression of ~100 is needed to flip it.
3. **Standard-siren d_GW/d_EM at the 1e-2 level** (LVK IR1 from November 2026; O5 undated [D-70]) tests only large damping, already excluded by GW150914 (11.29% calibration) and GW170817 ([−0.17, +0.06]). Any detected path loss would overturn everything here; the expected null changes nothing.

## Key numbers
| Quantity | Value (units) | Source or calc |
|---|---|---|
| Eq. 8 pair rate, GW150914 | 1.40e-4 pairs/s (SI) | M-DIALECTICIAN-01; calc/falsifier-C1-0_sustained.py.log |
| T_eff (top hat) | 4π/(3σ) = 0.0209 s | M-DIALECTICIAN-02 |
| B&O per-packet total | 2.93e-6 pairs (6.6e-6 at E = 3 M☉c²) | M-IDEALIZER-09 |
| Sustained reading over 410 Mpc; over-count | 5.9e12 pairs; 2.0e18 | falsifier-C1-0 log |
| B&O validity τσ (needs ≪ 1) | 7.2e5 | M-DIALECTICIAN-01 |
| Energy fraction removed over the whole history (model) | 1.6e-84 | falsifier-C1-0 log |
| Face-value depletion over 410 Mpc | 3.3e-66 (2.5e-57 stimulated) | M-CONSTRAINTS-14 |
| Energy e-fold length required by GW150914's calibration | > 5.3e25 m | M-CONSTRAINTS-14 |
| Bound A, P(>R) ≤ (GE/c⁴)²/(cTR) | 2.9e-6 (R = λ); 4.6e-25 (410 Mpc) | falsifier-C2-2; crux-C2_discriminators |
| Toy yield beyond R (l = 2, m = 2) | 0.0632 (kR)⁻³ | M-IDEALIZER-08 |
| Ambient-background lifetime of a 150 Hz graviton | 5.2e124 s (ΔN_eff = 0.3) to 2.4e127 s (NANOGrav level) | C2-0; crux-C2 |
| Retarded/time-symmetric fusion ratio | 1/12 (p = 0), 0.020 (p = 2) monopole; 0.028 at σ/ω = 0.21; 2.9e-3 circular (2,2); ∝ (ka)⁻⁶ for (2,0) | M-EXAMINER-03; falsifier-C3-2_quadrupole.py.log |
| Linear-channel coefficient k | 67/(630π) = 0.0339 (0.025–0.036 with finite size) | falsifier-C4-1, C5-0, C5-2 logs |
| N_lin, GW150914 / GW170817 chirp | 3.1e-4 / 3.8e-5 pairs (ratios to fusion 107 / 1.3e3) | falsifier-C4-1_offshell_channel.py.log |
| Eq. 14 rate at ΔN_eff = 0.3; shortfall vs FIRAS | 2.8e-109 pairs m⁻³ s⁻¹; ≥ 1e71 | M-CONSTRAINTS-02/03 |
| s-channel (h^(2)) share of B&O's J_z = ±4 channel | 0 (photon exchange 100%); R/R at 90°: h^(2)-only 8.26 vs full 0 | falsifier-C7-1_schannel_vs_full.py.log |
| Plasma threshold for 150 Hz photons | n_e < 2.8e-4 cm⁻³; warm ISM f_p = 1.56 kHz; evanescent for 1+z > ~1270 | M-CONSTRAINTS-09, M-EXAMINER-10 |
| ULDM resonance: coherence needed / time in band | 1.32e12 s / 12 s (shortfall 9.2e-12); in-band W_φ ≤ 2 W·x_MW; best over masses 1.6 W·x_MW | M-EMPIRICIST-03; falsifier-C8-0/C8-2 logs |
| W_γ/L_GW (fusion) | 4e-85 | M-CONSTRAINTS-06 |
| Eq. 19 over-count X; energy-conservation corner | 6.6e21–6.6e41; CX = 34 at 1e10 eV | M-CONSTRAINTS-07 |

## Caveats
- Search-summary only: Deser 1975 [D-58] (dropped from C2's evidence), the O1/O2 calibration figure, and the COSI/IPTA/LuSEE dates. Abstract-only or unverifiable: Gibbons 1975 (massive scalar only), Garriga–Verdaguer, Dorca–Verdaguer, Sawyer, Chakraborty et al., Rogers & Peiris, Dalal & Kravtsov, Bar et al., Horlaville et al.
- Preprints relied on: B&O v2 itself (unrefereed, 0 citations); Redi & Tesi 2026; Khusnutdinov 2026 (journal reference per INSPIRE, unchecked); Rahvar 2026, whose normalisation differs from this run's k by 5e3 (unresolved; favours C5 if right); the Jones–Singleton essay.
- Unresolved: the collinear Bogoliubov dispute [D-51] (immaterial, since the amplitude vanishes there); a factor-2 ambiguity in the Redi–Tesi normalisation (C4-0: k = 0.017–0.068) and whether N_dec counts pairs or particles.
- Math checks: two refuted rows (M-MECHANIST-02, M-DIALECTICIAN-10). Neither changed a ranking; M-MECHANIST-02's corrected form sharpens the eq. 7 finding (no fixed polarisation realises B&O's real-sign value on one axis). Unverified and used only as down-factors: pattern coefficients 0.562/0.3125/0.225, coherent/kinetic 0.98/0.93, eq. 17's v⁶ and 1/128, the binning claim; the small-kR entries of M-IDEALIZER-08 were not independently integrated.
- Speculative physics used, labelled: ULDM; the Rayleigh–Jeans extrapolation of the CMB to Hz; B&O's N² fusion itself.
- Superseded inputs: GW150914's 2016 values (GWTC-1 not retrieved); E ≈ 3.1 M☉c² would raise pair numbers by ~2.4.
- No advocate crux exists for C1 or C8; their verdicts rest on the refuters' calculations alone. The checks/ folder was not read, per the brief.
- Papers to request: Deser 1975 (doi:10.1088/0305-4470/8/12/012), to fix whether the all-loop plane-wave no-go covers second-order Einstein–Maxwell; Garriga & Verdaguer 1991 (doi:10.1103/PhysRevD.43.391), for the explicit massless β and collinearity condition. Neither can revive C1, since both concern exact plane waves.
- B&O eqs. 18 and 20 are garbled in PDF extraction; the eq. 18 reconstruction assumes E_rel = (2–3)/65 Mc².

## Sources
- Blas & Oller, "Gravitational waves decay in vacuum", arXiv:2607.24930 v2 (preprint): https://arxiv.org/abs/2607.24930
- Redi & Tesi 2026, arXiv:2606.28297 (preprint): https://arxiv.org/abs/2606.28297
- Garani, Redi & Tesi, arXiv:2502.12249, JHEP 08 (2025) 037: https://arxiv.org/abs/2502.12249
- Khusnutdinov, arXiv:2508.11558 (EPJ Plus 141, 532 per INSPIRE): https://arxiv.org/abs/2508.11558
- Han, Lykken & Zhang, hep-ph/9811350 (spin-2 → γγ width): https://arxiv.org/abs/hep-ph/9811350
- Bjerrum-Bohr et al. 2015, Phys. Rev. D 91, 064008 (gravitational Compton amplitudes; Skobelev 1975 cross-section) [D-01]
- Chakraborty et al. 2024, Phys. Rev. D 110, L021701, arXiv:2404.01840: https://arxiv.org/abs/2404.01840
- Jones & Singleton 2015, arXiv:1505.04843: https://arxiv.org/abs/1505.04843; Jones, McDougall & Singleton 2017, PRD 95, 065010, arXiv:1610.02973: https://arxiv.org/abs/1610.02973
- Sawyer 2020, PRL 124, 101301, arXiv:1910.08835: https://arxiv.org/abs/1910.08835
- Dorca & Verdaguer, gr-qc/9403015: https://arxiv.org/abs/gr-qc/9403015
- Gibbons 1975, plane-wave no-go (abstract only) [D-56]; Deser 1975 (search summary only) [D-58]; Garriga & Verdaguer 1991, PRD 43, 391 (abstract) [D-59]
- Cristofoli et al. (coherent states as classical limits) [D-02]; Caron-Huot et al. (in-in waveforms) [D-03]; Ai, Ellis & Pradler 2025 [D-71c]
- Rahvar 2026, arXiv:2606.17178 (preprint): https://arxiv.org/abs/2606.17178
- Rogers & Peiris 2021, PRL 126, 071302; Dalal & Kravtsov 2022, PRD 106, 063517, arXiv:2203.05750: https://arxiv.org/abs/2203.05750; Bar et al. 2019, JCAP 07, 045, arXiv:1905.11745: https://arxiv.org/abs/1905.11745; Schive et al. 2014, PRL 113, 261302, arXiv:1407.7762: https://arxiv.org/abs/1407.7762
- Lagos et al. 2019, PRD 99, 083504 (GW170817 d_GW/d_EM) [D-71 via M-EMPIRICIST-05]; Horlaville et al. 2026, ApJ 1003, 229
- LIGO/Virgo GW150914 discovery paper (2016) [D-28–D-30]; LIGO O3B calibration [D-39]; LVK O1–O4a SGWB limit, arXiv:2508.20721: https://arxiv.org/abs/2508.20721 [D-34]; NANOGrav 15-yr [D-35]; COBE/FIRAS [D-08]; Planck 2018 [D-32]; ARCADE-2 [D-09]; Voyager 1 plasma density [D-07]
- Run files: runs/2026-10-13-gravitational-wave-decay-photon-pairs/{dossier.md, candidates.md, verdicts/C1-0 … C8-2.md, cruxes/C2–C7.md, math/*.md, calc/*.py.log}; toolkit qft_second_order.py, qft_production.py, gw_coherent_fusion.py
## What changed since checks/2026-10-11-blas-oller-gw-decay
*Added by the main session. That check is not a /conundrum run and has no ranked answers; this run ignored it, so the comparison is of conclusions.*
- **Agree, now independently re-derived:** eq. 8 is right inside B&O's model (4/25 per-packet total, 3/(25π) "rate"); their in-state carries the time-symmetric Pauli–Jordan field; there is no sustained decay, and the yield beyond R converges (check: R⁻³; here R⁻³ in toys plus a general ≤ 1/R bound, C2 at 0.90); eq. 14 = 8πG²ρ²/15 is the isotropic kinetic rate (C6 at 0.92); the binning "lower bound" is an overestimate; eq. 19/S12 over-counts (check 1.7e21 at one point; here 6.6e21–6.6e41); the pair number is ħ-free (C7); the eq. 18 arithmetic (3.8e13 W) and its ~1e-11–1e-12 resonance shortfall (C8 at 0.03).
- **Disagree on the size of near-source fusion:** the check's crude quadrupole estimate gave 0.3–0.7 of B&O's merger number, which is this run's C4′ (0.25). This run favours C3 (0.65): 0.003–0.05 for the outgoing wave, from scalar toys. Neither ran a spin-2 retarded calculation; decisive test 2 settles it.
- **New here:** the source's own off-shell linear channel makes ~100× more pairs than N² fusion (C5, 0.80); a Gibbons/Khusnutdinov/Redi–Tesi literature base; the plasma cutoff kills Hz–kHz photon propagation in the ISM and before z ≈ 1300; photofission needs ≥ 5e20 Hz.
- **Physical-pattern coefficients differ by 7–12%:** gw_coherent_fusion (default grid) gives 0.562 (circular binary), 0.3125 (linear quadrupole), 0.225 (isotropic_plus) of 3/(25π); the check gave 0.604, 0.337, 0.254 from two engines. The tool's own docstring shows its circular-binary value rising with a finer grid (0.562 → 0.583), so its default grid likely under-converges; both agree circular polarisation gives exactly 0. No ranking depends on this.
- **Eq. 17:** the check computed a resonant coefficient 1/16 (0.0624997); this run found no "1/16" in v2 and left eq. 17 (v⁶, 1/128) undetermined. The brief took "1/16" from the check's wording, so this needs one look at v2 eq. 17.
- **Update 2026-10-14 (main session):** the calculator's under-convergence is fixed in the toolkit copy. The CM photon-angle integrand has a cusp at cos θ* = 0, and splitting the Gauss rule there gives circular binary 0.6046, linear quadrupole 0.338 and isotropic_plus 0.241 of 3/(25π), matching the check. The lens values quoted above (0.562, 0.3125, 0.225) were 6–11% low; no ranking used them except as unverified down-factors.
