# Check: theory
status: final

Method: fetch_text.py --grep against arXiv full text for each quoted phrase. All sources opened as full text except PSW (abstract only, which is all the claim uses).

| Claim | Verdict | Note |
|---|---|---|
| RT-01 Natário metric, Thm 1.7 | verified | Metric, K_ij, θ=∇·X and Theorem 1.7 wording match. Scope (unit lapse, flat slices) is stated correctly. |
| RT-02 Natário zero-expansion ρ ≤ 0 | verified | ρ = -(1/16π)K_ijK^ij = -(v_s²/8π)[...] and θ=0 match the text. Alcubierre ρ formula comes via restatement, not rechecked. |
| RT-03 Olum 1998 | verified | Generic-condition sentence and WEC-violation conclusion match. The "Proof"/Raychaudhuri detail is consistent with the text seen. |
| RT-04 Santiago–Schuster–Visser NEC theorem | verified | Quotes match (the "slightly different reasons" sentence is on p. 30). Their text also says Lentz, Bobrick–Martire and Fell–Heisenberg only checked one observer class. |
| RT-05 ADM mass paper | verified | Zero ADM mass for Alcubierre and zero-expansion, hemisphere p̄<0 and the NEC violation all match. |
| RT-06 Gao–Wald Thm 1 | verified | "K′ could be far larger than K" caveat and the PSW link match. |
| RT-07 Visser–Bassett–Liberati | verified | Wording matches; the perturbative scope is stated correctly. |
| RT-08 Lentz energy scaling and WEC | verified | E_tot ~ C v_s² R²/w and "(few)×10^-1 M⊙ v_s" match. The DEC quote and the horizon statement match. Lentz's own paper says this is the same magnitude as the Alcubierre estimate. The "WEC satisfied" claim is Eulerian-only, and RT-04 contradicts it for all observers. |
| RT-09 Fell–Heisenberg numbers | verified | ρ_max 3.2e26 kg/m³, E ≈ 9.25e43 J, the black-hole remark and the WEC-violation-in-compact-regions concession all match. Minor: 1.78e47/9.25e43 ≈ 1900, so the ratio is about 5e-4 M_sun (3.3 orders). The paper says "four orders" and the note says "roughly 1e-4", which slightly understates the energy. |
| RT-10 Bobrick–Martire | verified | "requires propulsion", Class I and "slow down the time" quotes match. Van Den Broeck "equivalent to Alcubierre" is confirmed on p. 3 and in App. A.2. |
| RT-11 Fuchs et al. warp shell | verified | Shell parameters, "all of the energy conditions" and δt = 7.6 ns (Table 1) are confirmed, so the truncation gap is closed. Alcubierre 8.0, VdB 9.1 and Modified Time 6.7 match. The "negative energy density throughout space" quote concerns the acceleration approach and matches. The energy conditions are numerical, sampled over observers. |
| RT-12 Warp Factory | verified | The p. 2 quote matches. The sampled-observer point rests on the Fuchs text, which I did not recheck in detail. |
| RT-13 Andréasson bound | verified | Bound, Ω=1 Buchdahl and Ω=3 for DEC all match. The 48/49 arithmetic is correct: ((7)²-1)/49 = 48/49. |
| RT-14 PSW | verified | The abstract wording matches. The Schoen–Yau/Witten statement is unsourced, as the file admits; treat it as textbook, not as evidence. |

Most serious issue: none contradicted. The main caveat is the Fell–Heisenberg energy ratio (1e-4 stated vs about 5e-4 computed from the paper's own numbers).
