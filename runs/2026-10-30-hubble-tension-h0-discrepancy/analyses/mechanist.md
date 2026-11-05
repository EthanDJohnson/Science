# Analysis: mechanist (causes and mechanisms)
status: final

## Method applied
For each candidate cause of the ~0.15-0.19 mag (5-6 km/s/Mpc) gap I wrote the causal chain: the process, what it acts on, what sustains it and what ends it. I classified the phenomenon and named the theory that governs it, then cited each link or marked it ASSUMED. I sized every ladder and early-side systematic against its published budget [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-mechanist_sizes.py]. I then asked which classes of measurement each mechanism can physically reach (its "reach") and compared that with the observed pattern of H0 values.

## Findings
1. **Framing.** What disagrees is the luminosity scale of local candles (anchors → Cepheid/TRGB/JAGB → SN Ia M_B) against the r_d ruler, which is calibrated by CMB or BBN physics. The two are connected through the expansion history [D-03, D-06, D-21, D-70]. Every mechanism therefore acts on one of three things:
   - the **ruler** (r_d);
   - the **candles** (anchors → primary indicator → SN);
   - the **bridge** (H(z), G_eff, local inhomogeneity).
2. **Size of the gap** [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-mechanist_sizes.py], from [D-20, D-22, D-24, D-44, D-45].
   - H0DN-corrected 73.264 vs CMB-SPA 67.19: 6.07 km/s/Mpc = 9.0% = 0.188 mag (naive 6.8σ).
   - SH0ES 2025 73.49 vs CMB-SPA: 0.195 mag. R22 73.04 vs CMB-SPA: 0.181 mag.
   - Against BAO+BBN 68.50 the gap is smaller: 0.146 mag (H0DN) and 0.153 mag (SH0ES 2025).
   - CCHP TRGB 70.39 vs CMB-SPA: 0.101 mag (1.6σ naive).
   - SH0ES–CCHP: 0.094 mag, about half the gap.
   - Reference gap used below: 0.188 mag, equivalent to a 9.0% error in the distance scale.
   - Stated directly in M_B (ladder −19.253 vs inverse ladder −19.375/−19.394) the gap is 0.12–0.14 mag. These come from different SN systems [D-21].
3. **Single ladder mechanisms, each taken alone** [calc: same file].
   - **Cepheid photometry/crowding.** Needs a +0.188 mag HST bias. JWST−HST is measured at −0.01 ± 0.03 mag, so the needed bias lies 6.6σ from the measurement [D-09, D-78]. The bound comes from the SH0ES team and covers photometry only.
   - **Cepheid metallicity.** Dropping the term moves H0DN by only 0.012 mag (73.50 → 73.08) [D-23], so the effective anchor–host lever is ≈ 0.05 dex. To produce 0.188 mag the slope would have to be wrong by 3.5 mag/dex, about 68σ of γ = −0.234 ± 0.052 mag/dex [D-21].
   - **Cepheid dust/R_V.** The whole reddening correction is ~0.03 mag, so 6.3 times the entire correction would be needed. Host-specific R moves H0 *up* by 0.8 km/s/Mpc, the wrong sign [D-15].
   - **Anchors.** Needs a coherent 9.0% distance error in every anchor. NGC 4258 is known to 0.97% (9σ) and the MW residual parallax offset is 0.9% (~10σ) [D-32, D-86]. Leave-one-anchor-out results stay at 73.08–73.61 [D-23].
   - **Peculiar velocities / flows.** A coherent outflow of ~1350–1900 km/s at z ≈ 0.05–0.07 would be needed. My reference that bulk flows are a few hundred km/s is ASSUMED; the ΛCDM cosmic variance of local H0 is 0.31 km/s/Mpc [D-10]. A disputed partial lever exists: Dong 2026's host-PV correction is 0.087 mag (46% of the gap) in a forward Pantheon+ analysis, while the Laniakea flow model moves H0 the other way (+0.6 km/s/Mpc) [D-82, D-36].
4. **SN-rung and selection levers are each partial, 15–45% of the gap** [calc: same file].
   - Wojtak & Hjorth (two populations/colour): 0.048–0.077 mag (25–41%) [D-35].
   - Percival (Cepheid selection): 0.042 mag from the cut-off, 0.030 from the distance prior, 0.078 if all three add (42%) [D-88].
   - Pantheon+ vs CSP photometry compilation: about 0.038 mag [D-25].
   - A naive sum of the three largest disputed levers (Wojtak & Hjorth conservative, Percival cut-off, Dong PV) is 0.177 mag, 94% of the gap. This is an upper envelope: their overlap is unknown and SH0ES has accepted none of them [D-99].
5. **Early-side analysis systematics need 9–60σ shifts** [calc: same file]. I used the run's background calculator (flat ΛCDM, HS96 z_*, ω_b = 0.02237, ω_c = 0.1200).
   - θ_*: d ln h/d ln θ_* = 5.1. Moving 67.19 → 73.26 needs θ_* off by 1.69%, about 59σ of its 0.03% precision [D-40].
   - ω_c: at fixed θ_*, d ln h/d ln ω_c = −0.62 (background only). ω_c would have to be ~14% low, about 14σ with an ASSUMED 1% Planck precision on ω_c.
   - BAO+BBN: r_d would have to fall 6.5% against the 0.72% precision on h·r_d (9σ), or ω_b would have to rise ×1.69 against D/H at about 1% [D-45, D-46].
   - Per experiment: Planck PR4, ACT DR6 and SPT-3G would each need their own same-sign bias of 10.6–11.0σ [D-41, D-42, D-43].
   - PR4 removes the A_L preference and H0 stays low [D-79a].
   - The only element all early-side routes share is the physics model itself (recombination, BBN). An error there is new physics, not an analysis systematic.
6. **SN Ia progenitor-environment step (a mechanism the dossier lists only as a gap, §6).**
   - Rigault et al. measure the step: [new: Rigault et al. 2020, A&A 644 A176, arXiv:1806.03849, abstract, "the SNeIa in predominantly younger environments are DY=0.163\pm0.029 mag (5.7 sigma) fainter than those in predominantly older environments after conventional light-curve standardization"]. Fitted jointly with a 0.064 mag mass step, it is "DY=0.129\pm0.032 mag" (same abstract).
   - ZTF DR2 confirms it: [new: Ginolin et al. 2025, A&A 695 A140, arXiv:2405.20965, abstract, "we find it to be greater than 0.12 mag regardless of the considered environmental tracer used (local or global colour and stellar mass), all measured at the $\geq 5\sigma$ level, increased to $\sim0.17\pm0.01$ mag when accounting for the stretch-non linearity"].
   - The mass step already applied to SNe is [new: Jones et al. 2018, ApJ 867 108, arXiv:1805.05911, abstract, "a shift of 0.06 mag across a low to high mass boundary (the mass step)"]. The same abstract finds the local effect "insignificant in the targeted low-$z$ sample".
   - Causal sign: Cepheid hosts are star-forming, so calibrator SNe sit mostly in young environments (ASSUMED as a fraction), and young environments give fainter SNe. Applying the calibrators' M_B to a Hubble flow of mixed age makes Hubble-flow distances too short and H0 too high, which is the right sign.
   - Size: γ_env × Δf_young, minus what the applied mass step already removes. With γ_env = 0.17 mag and Δf = 0.5 (ASSUMED), the offset is ≤ 0.085 mag (≤ 45% of the gap). The full 0.188 mag would need Δf > 1, which is impossible.
   - It cannot move SBF, Tully–Fisher, masers or time delays.
7. **Reach test: no single candle-side mechanism reaches every high channel.**
   - H0DN without Cepheids: 72.5 ± 1.3. Without SNe Ia: 73.4 ± 1.8; replacing SNe with galaxy indicators changes H0 by < 0.1 [D-23].
   - Non-Cepheid, non-SN ladders sit high: SBF 73.8 ± 0.7 ± 2.3 [D-29]; Tully–Fisher 73.3 ± 2.1 ± 3.5 [D-30]. SH0ES-side TRGB and JAGB give 72.1–73.3 [D-27, D-28, D-26].
   - So a Cepheid-only mechanism (crowding, metallicity, dust, P–L, a Cepheid fifth force) can remove at most ~0.8 km/s/Mpc from the network. An SN-only mechanism (standardisation, environment, compilation) can barely move the network's central value.
   - The mechanisms that do reach every ladder channel are the anchors (excluded, finding 3) and Hubble-flow peculiar velocities (which act on SNe, SBF, TF and masers alike; disputed, finding 3).
8. **Channels that use no ladder sit in the middle** [calc: same file].
   - TDCOSMO-2026 71.1 +2.4/−2.3 [D-31], masers 71.6 ± 3.7 (stat only) [D-32], sirens 71.7 +9.4/−7.5 [D-33].
   - Weighted mean: 71.27 ± 1.93 km/s/Mpc. That is 2.1σ above CMB-SPA and 1.0σ below H0DN, and carries 67 ± 32% of the gap.
   - Adding SBF and TF (which share the anchors) gives 72.39 ± 1.41, 3.6σ above CMB-SPA. This is consistent with the TDCOSMO companion's 3.7σ no-SN and 2.7σ no-ladder figures [D-90].
   - These channels physically share nothing with Cepheid crowding, metallicity or SN standardisation. A pure candle-systematic explanation therefore predicts that they converge to ~67–68 as their precision improves. So far they lean high, but by only ~2σ.
9. **The SH0ES–CCHP split is not sampling noise alone** [calc: same file].
   - CCHP's σ_SN term (0.70 km/s/Mpc over 24 SNe) implies about 0.105 mag scatter per SN. Adding an ASSUMED 0.06 mag error per host, a subset mean of 24 of 35 hosts should differ from the full-sample mean by σ ≈ 0.014 mag (11 of 35: 0.030 mag).
   - The observed differences are 0.084 mag (70.39 vs 73.18) and 0.134 mag (68.81 vs 73.18). Sample selection can carry ~2σ of this, which fits Li's "2σ" for the 11 extra hosts [D-27] and the HST prediction of 71.2 for CCHP's subset [D-28]. The rest needs calibration choices.
   - Calibration choices of the right size exist: the JAGB field-to-field difference within NGC 4258 is 0.11 mag (59% of the gap) [D-26], and CCHP's sole anchor is NGC 4258 [D-24]. Ground JAGB vs HST TRGB differs by 0.17 mag [D-81]. The SN compilation adds 0.038 mag [D-25].
   - Mechanistically, the split is a TRGB/JAGB zero-point and sample/compilation problem at one anchor. It is not a physical Cepheid-vs-TRGB difference: SH0ES-side TRGB/JAGB on the full host set give 72–73 [D-27, D-28].
10. **Early-time new physics: how much of the gap it closes without a SH0ES prior** [calc: same file].
    - ACT DR6: EDE 69.9 closes 45%, PMF 69.1 closes 31%, modified recombination 69.6 closes 40% [D-52].
    - Planck NPIPE EDE (95% upper bound) 69.5 closes 38% [D-53]. Electron-density fluctuations 69.3 close 35% [D-95].
    - The most favourable fits close more: Poulin 2026 EDE (profile likelihood) 71.0 closes 63%, and eROSITA+ 71.4 closes 69% [D-53, D-94].
    - The residual is always ≥ 0.056 mag, consistent with the sound-horizon-only no-go [D-73].
11. **Late-time H(z) reaches only the bridge between r_d and z ~ 0.01–2, and the inverse ladder pins it.**
    - BAO + uncalibrated SNe fix H0·r_d, and with the standard r_d any H(z) gives ≈ 67 [D-70, D-07, D-48]. DESI w0wa moves H0 *down* (63.6–67.5) [D-12, D-51].
    - The only late-time escape changes the candle, not H(z): a G_eff/M_B transition [D-92].
    - Size needed: Hubble-flow SNe 0.188 mag brighter than calibrators. That is G_HF/G_local = 0.891 if L ∝ M_Ch ∝ G^−1.5 (ASSUMED Arnett scaling), matching the μ_G ≈ 0.9 of [D-92].
    - The transition must sit between ~41 and ~94 Mpc (z ≈ 0.01–0.023) [calc: same file].
12. **Local structure needs 20σ.** A 9.0% local excess is 20σ of the ΛCDM 0.31 km/s/Mpc [D-10, D-37]. The SN Hubble diagram excludes |δ| > 20% at 4–5σ [D-11]. A void cannot reach the time delays at z ~ 0.3–0.7 [D-31], which still sit at 71.
13. **A mechanism the dossier omits: a screened fifth force acting on Cepheids.** [new: Desmond, Jain & Sakstein 2019, PRD 100 043537, arXiv:1907.03778, abstract, "if the Cepheids with direct distance measurements from parallax or water masers are screened but a significant fraction of those in other galaxies are not, neglecting the difference between their underlying period--luminosity relations biases the local $H_0$ measurement high"]. Its reach is limited to channels with unscreened stellar candles. It cannot move TDCOSMO, masers or CMB/BAO. It must also act on TRGB and JAGB, which agree with Cepheids at ≤ 0.05 mag [D-26, D-28], so it is strained by the reach test (finding 7).

## Lens-specific outputs

### A. Causal chains

| # | Mechanism | Process (what produces it) | Acts on | Sustained by | Ended by / limited by | Class; governing theory | Weakest link |
|---|---|---|---|---|---|---|---|
| L1 | Cepheid crowding/blending | unresolved flux adds to Cepheid photometry in distant hosts [D-09] | Cepheid m_H in SN hosts more than in anchors | crowding grows with distance (ASSUMED) | JWST resolution; HST−JWST −0.01 ± 0.03 [D-78] | measurement artefact; photometry/PSF | JWST bound (6.6σ); SH0ES-team only |
| L2 | Cepheid metallicity term | Z-dependent P–L zero point [D-21] | anchor vs host Cepheids | metallicity contrast anchor–host | 4 anchors spanning Z; lever 0.012 mag [D-23] | material/stellar property; stellar pulsation | needs 68σ slope error |
| L3 | Cepheid/host dust (R_V) | extinction-law mismatch [D-15] | Cepheid colours | dust in star-forming hosts | Wesenheit/NIR; total correction 0.03 mag | material property; dust extinction | 6x the whole correction; host-R moves H0 up |
| L4 | Anchor distance error | maser model, DEB surface-brightness relation, Gaia zero point [D-32, D-86] | absolute zero point of every ladder | shared NGC 4258 / LMC / MW | anchors mutually consistent [D-23] | measurement artefact; geometry | 9–10σ per anchor, all coherent |
| L5 | SN standardisation, colour/dust two-population | different colour–luminosity relation in calibrators [D-35] | calibrator SN M_B vs Hubble flow | host-type difference (star-forming calibrators) | colour-matched samples; 0.05–0.08 mag | material property; dust + SN physics | "no obvious physical basis" (authors) [D-82]; partial only |
| L6 | SN progenitor-age/environment step | younger progenitors give fainter standardised SNe (finding 6) | calibrator SNe (young) vs mixed Hubble flow | calibrator selection requires Cepheids (star formation) | partly absorbed by the 0.06 mag mass step; ≤ 0.085 mag | stellar population physics; SN Ia progenitor astrophysics | young-fraction difference ≥ 1 needed for the full gap; ASSUMED fractions |
| L7 | Calibrator selection (Cepheid cut-off, Malmquist-type) | flux-limited Cepheid detection biases P–L in hosts [D-88] | host P–L intercepts | detection limits | completeness modelling; −0.2 to −2.6 km/s/Mpc | statistical/measurement artefact | 1.3–2.3σ evidence; no reply yet |
| L8 | Hubble-flow peculiar velocities | coherent flows bias cz at 0.023 < z < 0.15 [D-82, D-36] | every Hubble-flow tracer (SN, SBF, TF, masers) | large-scale structure | ΛCDM σ = 0.31 km/s/Mpc [D-10]; signs disagree between analyses | classical gravity; ΛCDM structure formation | needs ~1350–1900 km/s coherent; Dong vs Laniakea sign conflict |
| L9 | TRGB/JAGB zero point at one anchor | tip-edge and JAGB-mode measure; field selection in NGC 4258 [D-26, D-81] | CCHP calibration (NGC 4258 sole anchor) | single-anchor design | multi-anchor TRGB; 0.11 mag field difference | measurement artefact; stellar evolution (RGB tip, carbon stars) | explains SH0ES–CCHP, not ladder–CMB |
| E1 | CMB foregrounds/likelihood (A_L) | residual foreground or lensing excess biases ω_c, θ_* | Planck H0 | Planck-specific processing | PR4 removes A_L [D-79a]; ACT, SPT independent [D-02] | measurement artefact; CMB likelihood | needs a same-sign ~11σ bias in 3 instruments |
| E2 | BAO reconstruction / fiducial bias; BBN rates | shifts D/r_d, ω_b | BAO+BBN H0 | template assumptions | DESI ⊥ θ_* consistent [D-45] | measurement artefact; BAO/BBN | needs 9σ in h·r_d or ω_b ×1.69 |
| N1 | Early dark energy | scalar field frozen by Hubble friction, then oscillates [D-14] | H(z) for z ~ 3000–5000 → r_s ↓ | potential energy; fine-tuned V | dilutes faster than radiation after z_c; f_EDE < 0.06–0.07 (95%) [D-75] | new particle/field; scalar field in GR | data allow only 38–69% of gap; S8 pressure; "why then" |
| N2 | ΔN_eff / SIDR | extra radiation raises pre-recombination H [D-04] | r_s ↓ (needs N_eff ≈ 4.2–4.6) [D-56] | relativistic species | damping tail; ACT N_eff = 2.86 ± 0.13 [D-74] | new particle; standard-model extension | ~10σ from ACT N_eff |
| N3 | Varying m_e / modified recombination | earlier recombination raises z_*, cuts r_s [D-76] | r_s and the damping tail | time variation of a constant | DESI DR2: lowers Ω_m [D-76]; ACT 69.6 [D-52] | new interaction; atomic physics with varying constants | fails once DESI DR2 added |
| N4 | Primordial magnetic fields | baryon clumping speeds recombination [D-96] | r_s | primordial field | ACT 69.1; fails H0-Olympics criteria with more data [D-17] | classical field (MHD) | closes 31% only |
| N5 | Late-time DE (phantom, w0wa, IDE) | changes H(z) at z < 2 | D(z) between r_d and today | DE dynamics | inverse ladder fixes H0·r_d [D-70]; DESI moves H0 down [D-12] | new field/fluid; GR + DE | cannot raise H0 with standard r_d |
| N6 | G_eff / M_B transition at z ≈ 0.01 | G drops ~11% beyond ~40–90 Mpc → M_Ch ↑ → SNe brighter [D-92] | Hubble-flow SN M_B (and any G-dependent candle) | modified gravity | must leave masers/time delays (geometric) unaffected | new interaction; modified gravity | why at 40–94 Mpc (non-Copernican coincidence); masers/TD 71 not 67 |
| S1 | Local void / bulk flow | underdensity → local outflow δH/H ≈ −fδ/3 [D-37] | all z < 0.15 tracers | gravitational instability | ΛCDM σ 0.31; SN diagram |δ| < 20% [D-10, D-11] | classical gravity; ΛCDM structure | needs 20σ; TD at z ~ 0.5 also high |
| X1 | Null: several partial systematics + fluctuation | L5–L9 each 15–45% | ladders | independent analysis choices | convergence of independent channels | mixed measurement artefacts | needs ≥ 2–3 disputed levers to add same-sign; SBF/TF also high |

### B. Required size vs published budget (reference gap 0.188 mag = 9.0% in H0)

| Sub-hypothesis | Needed | Measured/bounded | Ratio or σ | Verdict |
|---|---|---|---|---|
| Cepheid crowding | +0.188 mag | −0.01 ± 0.03 mag [D-78] | 6.6σ | eliminated as sole cause |
| Cepheid metallicity | slope error 3.5 mag/dex | γ = −0.234 ± 0.052 [D-21]; lever 0.012 mag [D-23] | ~68σ | eliminated |
| Cepheid dust/R | 0.188 mag | whole correction 0.03 mag [D-15] | 6.3x | eliminated |
| Anchor scale | 9.0% coherent | NGC 4258 0.97%, MW 0.9% [D-32, D-86] | 9–10σ each | eliminated |
| SN colour/2-pop | 0.188 mag | 0.048–0.077 mag claimed [D-35] | 25–41% | partial, contested |
| SN environment | 0.188 mag | ≤ 0.085 mag at Δf = 0.5 (ASSUMED) | ≤ 45% | partial |
| Cepheid selection | 0.188 mag | 0.006–0.078 mag [D-88] | 3–42% | partial, preprint |
| Peculiar velocities | ~1350–1900 km/s coherent | Dong 0.087 mag (46%); Laniakea −0.019 mag [D-82, D-36] | sign disputed | partial, contested |
| SN compilation | 0.188 mag | 0.038 mag [D-25] | 20% | partial |
| θ_* error | 1.69% | 0.03% [D-40] | ~59σ | eliminated |
| ω_c error at fixed θ_* | −14% | ~1% (ASSUMED) | ~14σ | eliminated |
| BAO h·r_d / BBN ω_b | 6.5% / ×1.69 | 0.72% / ~1% [D-45, D-46] | 9σ / excluded | eliminated |
| Per-CMB-experiment bias | +5.6 to +6.8 km/s/Mpc | σ 0.52–0.64 | 10.6–11.0σ each, same sign | eliminated |

### C. Reach matrix: which measurement classes each mechanism moves (↓ moves the high local value down; ↑ moves the early value up; 0 = no physical effect)

| Mechanism | Cepheid-SN | TRGB/JAGB-SN | SBF/TF | Time delays | Masers | Sirens | CMB ΛCDM | BAO+BBN | Inverse ladder | Collateral |
|---|---|---|---|---|---|---|---|---|---|---|
| Cepheid-only (L1–L3, L7, fifth force) | ↓ | 0 | 0 (SBF via TRGB) | 0 | 0 | 0 | 0 | 0 | 0 | none |
| SN-only (L5, L6, compilation) | ↓ | ↓ | 0 | 0 | 0 | 0 | 0 | 0 | 0 (shape only) | SN host-dependence of residuals |
| Anchors (L4) | ↓ | ↓ | ↓ | 0 | 0 (geometry; shares NGC 4258 method) | 0 | 0 | 0 | 0 | anchor–anchor tension |
| Peculiar velocities (L8) | ↓ | ↓ | ↓ | 0 | ↓ | small | 0 | 0 | 0 | dipole in residuals |
| Early-time new physics (N1–N4) | 0 | 0 | 0 | small (Ω_m prior) | 0 | 0 | ↑ | ↑ | ↑ (r_d smaller) | S8 ↑, n_s ↑, ω_c ↑ (EDE); N_eff (N2) |
| Late-time H(z) (N5) | 0 | 0 | 0 | small | 0 | 0 | ↓ or ↑ | ~0 | 0 (H0·r_d fixed) | w0wa lowers H0 |
| G_eff transition (N6) | 0 (calibrators local) | 0 | ? (if G-dependent) | 0 | 0 → would read ~67 | 0 | 0 | 0 | absorbs M_B | growth/S8 change |
| Local void (S1) | ↓ | ↓ | ↓ | 0 | ↓ | 0 | 0 | 0 | 0 | SN diagram kink at void edge |
| Observed pattern | 73.5 | 70.4 (CCHP) / 72–73 (SH0ES-side) | 73.8 / 73.3 | 71.1 | 71.6 | 71.7 | 66.5–67.6 | 68.5 | 67.2–67.7 | S8 ≈ Planck (1–3σ), N_eff 2.86 |

Reading the matrix: no single entry with a nonzero reach on both sides has survived. The pattern has every ladder at 72–74, one-step channels at ~71 ± 2, and every r_d route at 67–68.5. The mechanisms that fit it are either (i) a ruler-side change (N1–N4) plus a residual on the candle side, or (ii) a set of several candle-side levers, including one that reaches all Hubble-flow tracers (L8), plus a ~1–2σ upward fluctuation of the one-step channels. The one-step channels are what decide between these.

### D. Weakest links (the real test of each chain)
- Ladder systematic: no single cause reaches SBF, TF and SH0ES-side TRGB/JAGB except anchors (excluded) and flows (disputed in sign) (findings 3, 7).
- Early analysis systematic: needs the same sign in three independent CMB instruments and in BBN-calibrated BAO, each at ~9–11σ (finding 5).
- Early new physics: fitted to all data it closes 31–69% of the gap, not 100% (finding 10; [D-73]).
- Late new physics: H(z) is pinned by the inverse ladder; only an M_B/G transition escapes, and it needs a coincidence at 40–94 Mpc (finding 11).
- Local structure: a 20σ ΛCDM fluctuation (finding 12).
- Null (several partial levers): the levers are contested preprints, and SBF/TF stay at ~73 (findings 4, 7).

## Calculations
- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-mechanist_sizes.py` (log beside it). Units are km/s/Mpc and mag; flat FRW background from `runs/.../tools/cosmo_background.py`. It computes:
  - **A.** Gaps in mag: 0.188 mag (H0DN vs CMB-SPA), 0.195 (SH0ES 2025), 0.146 (H0DN vs BAO+BBN); SH0ES–CCHP 0.094 mag.
  - **B.** Ladder sub-hypothesis sizes: crowding 6.6σ; metallicity 3.5 mag/dex (68σ); dust 6.3x; anchors 9–10σ; flows 1355–1897 km/s; W&H 0.048–0.077 mag; Percival 0.006–0.078 mag; Dong 0.087 mag; naive sum of the three largest disputed levers 0.177 mag.
  - **C.** Early side: d ln h/d ln θ_* = 5.12, giving a 1.69% θ_* shift (59σ); d ln h/d ln ω_c = −0.62, giving a −13.9% ω_c shift; r_d −6.5% (9σ) or ω_b ×1.69; per-CMB biases 10.6–11.0σ.
  - **D.** One-step mean 71.27 ± 1.93 (2.1σ from CMB-SPA, 1.0σ from H0DN); no-SN set 72.39 ± 1.41 (3.6σ).
  - **E.** G_HF/G_local = 0.891 (Arnett scaling ASSUMED); transition window 41–94 Mpc.
  - **F.** Void: 20σ of ΛCDM cosmic variance.
  - **G.** Fraction of the gap closed by early models without SH0ES: 31–45% (ACT/Planck), 63–69% (Poulin 2026, eROSITA).
  - **H.** SH0ES–CCHP: per-SN 0.105 mag; subset-noise σ 0.014–0.033 mag against observed splits of 0.084–0.134 mag; NGC 4258 JAGB field difference = 59% of the gap.

## Candidate answers (at least 3; the null and a reframe count)
- [MECHANIST-A] **The null is several partial candle-side systematics plus a modest fluctuation.** Several partial effects in the ladder's SN and calibration rungs add in the same direction: SN progenitor-environment/colour standardisation (≤ 0.05–0.085 mag), Cepheid selection (≤ 0.04–0.08 mag), Hubble-flow peculiar-velocity modelling (disputed, up to 0.087 mag) and SN photometry compilation (~0.04 mag). Together with a ~1–2σ upward fluctuation of the one-step channels, they account for the 0.15–0.19 mag gap with no single dominant cause. | status: strained | Why: each lever is measured or proposed at the right sign and at 15–45% size (findings 4, 6). But the effects are contested preprints whose overlap is unknown, and SBF/TF (73.8, 73.3) and H0DN-without-SNe (73.4) are not reached by the SN levers (finding 7). | Test: (1) Repeat the calibration with Hubble-flow SNe restricted to young/star-forming local environments: this lowers H0 by ≥ 0.05 mag if L6 matters and by ≈ 0 if not. (2) Time delays at 1.5% (TDCOSMO with ~40 lenses) plus maser/siren updates should converge to 67–68.5 if this candidate is right, and stay at ≥ 71 if not. | confidence: medium
- [MECHANIST-B] **Early-time new physics shrinks r_d by ~4–6% and closes about half the gap.** The best representative is EDE-like extra energy before recombination; varying m_e, PMF and recombination variants are sub-hypotheses. The rest of the gap (0.06–0.12 mag) has to come from candle-side systematics as in A, or from an upward fluctuation. | status: surviving (as a partial cause only) | Why: it is the only class that acts on the ruler and so moves CMB, BAO+BBN and the inverse ladder together (reach matrix). Fitted without SH0ES it reaches 69.1–71.4 km/s/Mpc (31–69% of the gap) (finding 10; [D-52, D-53, D-94]). The no-go [D-73] forbids a full solution. ΔN_eff and varying m_e are disfavoured by ACT N_eff and DESI DR2 [D-74, D-76]. | Test: the CMB damping tail and TE/EE from SPT-3G Ext-10k/Simons Observatory constrain f_EDE to ~0.02 (a target ASSUMED here). Under ΛCDM the BAO+BBN, CMB and inverse-ladder values must stay mutually consistent at 67–68.5. Under EDE, a CMB-independent equality-scale H0 [D-50] sits at the ΛCDM-ruler value, while the ruler routes rise. | confidence: medium
- [MECHANIST-C] **Reframe: the anomaly is the candle zero point M_B (0.12–0.19 mag) against the r_d ruler, not H0.** Within that framing the SH0ES–CCHP split (0.084–0.134 mag) is a TRGB/JAGB zero-point and sample/compilation problem at the single NGC 4258 anchor. It is not a Cepheid-vs-TRGB physics difference. | status: surviving | Why: late-time H(z) cannot move H0·r_d (finding 11), so every viable mechanism acts on M_B or on r_d. Calibration choices of the needed size exist at NGC 4258 (0.11 mag JAGB field difference; 0.17 mag ground JAGB vs TRGB) (finding 9). SH0ES-side TRGB/JAGB reproduce 72–73. | Test: a multi-anchor TRGB/JAGB calibration (LMC + NGC 4258 + MW Gaia DR4 parallaxes of RGB-tip stars) applied by both teams to the same 35+ hosts with one SN compilation. If the split disappears, the remaining question is purely M_B vs r_d. | confidence: medium-high
- [MECHANIST-D] **Single-rung ladder systematic** (crowding, metallicity, dust, anchors, or one SN effect) explaining the whole gap. | status: eliminated | Why: each sits 6.6σ to ~68σ from its published bound, or reaches only one channel while SBF, TF and SH0ES-side TRGB/JAGB stay high (findings 3, 7). | Test: already tested by JWST and the leave-one-out variants. | confidence: high
- [MECHANIST-E] **Early-universe analysis systematic** (Planck foregrounds/A_L, BAO reconstruction, BBN rates). | status: eliminated | Why: it needs a same-sign 10.6–11σ bias in three instruments, a 59σ θ_* error, or a 9σ BAO error (finding 5). PR4 removed A_L and H0 stayed low [D-79a]. | Test: no further test is needed beyond SO/SPT consistency. | confidence: high
- [MECHANIST-F] **Late-time new physics.** Variants: (F1) H(z) changes from phantom/w0wa/IDE; (F2) a G_eff/M_B transition at 40–94 Mpc. | status: F1 eliminated; F2 strained | Why: F1 cannot change H0·r_d, and DESI w0wa lowers H0 [D-70, D-12]. F2 needs G_HF/G_local = 0.89 and an ad hoc transition scale, and it predicts that the geometric channels (masers at 50–130 Mpc, time delays) read ~67 (finding 11). They read 71–72 ± 2–4. | Test: maser and time-delay H0 at ≤ 2% (F2 predicts 67); SN Ia M_B measured in hosts at 40–100 Mpc with JWST TRGB (a step at the transition). | confidence: medium
- [MECHANIST-G] **Local structure** (void or bulk flow in ΛCDM). | status: eliminated | Why: it needs a 20σ ΛCDM fluctuation; the SN diagram excludes |δ| > 20%; and time delays at z ~ 0.5 also sit above the CMB value (finding 12). | Test: SN Hubble-diagram convergence at 0.15 < z < 0.4 (ZTF/LSST). | confidence: high

## What would change my mind
- Time-delay, maser and siren H0 converging at ≤ 1.5% on 67–68.5 would promote A (candle systematics) to the leading candidate and demote B. Converging on 72–74 would kill A and leave B strained too, since early physics closes ≤ 69% of the gap.
- A demonstration that Hubble-flow SNe in young local environments give the same M_B as old ones after the mass step would drop L6 from A.
- An SPT-3G/SO damping-tail bound of f_EDE < 0.02 would eliminate the EDE variant of B.
- A peer-reviewed, agreed peculiar-velocity correction for Pantheon+ of −2 to −3 km/s/Mpc would make flows (L8) the leading single lever, because it is the only candle-side mechanism that reaches every Hubble-flow tracer.
- A CCHP multi-anchor TRGB at ≥ 72 would settle the SH0ES–CCHP split as calibration, as in C.

## Assumptions I relied on
- The H0DN-corrected 73.264 and CMB-SPA 67.19 are representative reference values. Their correlations are ignored in my naive σ figures; the statistician owns the correlated values.
- The background-only derivative d ln h/d ln ω_c = −0.62 (HS96 z_* fit, no perturbations). A full Boltzmann treatment differs, but not enough to change "≥ 9σ".
- Planck σ(ω_c) ≈ 1%, typical anchor precision ≈ 1%, and typical bulk flows of a few hundred km/s: background knowledge, not dossier values.
- The young-progenitor fraction difference between calibrator and Hubble-flow SNe (0.3–0.5) is ASSUMED. The existing mass step absorbs part of the environment effect by an unknown amount.
- L_peak ∝ M_Ch ∝ G^−1.5 (Arnett) for the G_eff sizing. Other luminosity–G scalings change the needed ratio and possibly its sign.
- Per-host primary-distance error of 0.06 mag in the SH0ES–CCHP noise estimate (ASSUMED).
- The weighted mean of the one-step channels treats the maser stat-only error as total and symmetrises asymmetric errors.
