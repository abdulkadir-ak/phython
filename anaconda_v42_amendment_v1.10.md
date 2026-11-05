# Amendment v1.10 — Audit Response C4: Pairwise Clearance-Loss Bound (Th. V2/V3), New Self-Collision Gate T6e, Strict R-FINAL Horizon

Base: Anaconda v4.2 only (`anaconda-wordpress-snippet-v4.2 (6).html`, 2,644 lines).
Status: design-only. No code changes, no implementation, all existing v4.2 functionality preserved.
Language: English.
Verification: attached `v18_example.py` (729 lines, sections A–E; verbatim copy of
`scripts/v18_example.py`), numpy float64, fresh complete run output included below.

The audit is correct: Theorem V1 (v1.9) bounds **individual** ring displacement (≤ Λ = 0.0042 u),
and clearance is a **pairwise** quantity — by the triangle inequality two rings moving in opposite
directions can change their separation by up to 2Λ = 0.0084 u. C4 resolves what that ceiling
applies to, proves the stronger bound that exists for static obstacles, adds the missing
self-collision gate, and fixes the R-FINAL horizon off-by-one.

---

## C4.1 — Q1: maximum separation change between any two rings (Theorem V2 — proven)

For rings i < j let D_ij = ‖Q_j − Q_i‖ before the pass and D'_ij = ‖Q'_j − Q'_i‖ after the complete
pass, with ring displacements δ_i = Q'_i − Q_i, δ_j = Q'_j − Q_j. Then, exactly (no linearization):

    |D'_ij − D_ij| = | ‖(Q_j − Q_i) + (δ_j − δ_i)‖ − ‖Q_j − Q_i‖ |
                   ≤ ‖δ_j − δ_i‖            (reverse triangle inequality)
                   ≤ ‖δ_j‖ + ‖δ_i‖          (triangle inequality)
                   ≤ Λ + Λ = 2Λ = 0.0084 u  (Theorem V1, each ring ≤ Λ).

**Theorem V2.** After the complete head-to-tail repair pass, the separation of ANY ring pair
i ≠ j changes by at most **2Λ = 0.0084 u**, for every chain configuration and every adversarial
displacement direction pair. The proof uses no assumption about the directions of δ_i, δ_j.

**Refinement R1 (adjacent pairs — exact identity).** The pass sets each adjacent separation to
exactly SEG, so |ΔD_{k,k+1}| = |SEG − L_k⁰| = |e_k⁰| ≤ 0.0021 u (T6a domain). Verified exact to
fp (E4: identity deviation 1.7e−16).

**Refinement R2 (co-directed straight intervals — exact).** If every segment between i and j has
the same unit direction u (parallel, same orientation), the pass makes the interval perfectly
uniform: D'_ij = (j−i)·SEG and D_ij = (j−i)·SEG + Σ_{k=i}^{j−1} e_k⁰, so
|ΔD_ij| = |Σ_{interval} e_k⁰| ≤ Λ — the displacements telescope (they are prefix sums of the same
error sequence). This is why rigid-translation configurations produce no separation change.

## C4.2 — Q2: does the individual bound permit a pairwise loss of 0.0084 u?

**Yes, as a ring-pair ceiling**: ‖δ_j − δ_i‖ ≤ 2Λ is proven and cannot be improved to Λ in general
(the anti-parallel construction below measures cos(δ_i, δ_j) = −0.9966). Whether 2Λ materializes
as a *clearance loss* depends on what the second body is:

- **Static obstacle (wall/prop):** ≤ Λ = 0.0042 u — Theorem V3 (the obstacle does not move);
- **Self-collision pair (|i−j| ≥ 9):** ≤ 2Λ = 0.0084 u — Theorem V2;
- **Adjacent rings:** ≤ 0.0021 u — Refinement R1.

A further geometric effect limits how much of 2Λ is realizable: the separation change is the
**projection** of δ_j − δ_i onto the chord direction. The measured anti-parallel construction
(gentle 180° U-turn) produces cos(δ_i, δ_j) = −0.9892 yet only 0.206Λ of separation change,
because the U-turn chord is perpendicular to the headings. A chord-aligned construction
(long forward leg + 20-segment 180° arc + short return leg) recovers **1.599Λ = 0.006718 u**
(measured, cap-admissible field: sum|e| = 0.004200 = Λ exactly). Conclusion: no universal bound
below ≈ 1.6Λ is admissible; the proven ceiling 2Λ is adopted for design.

## C4.3 — Q3: the stronger bound that exists — Theorem V3 (complete proof)

**Theorem V3 (capsule vs static obstacle).** Let A = [Q_i, Q_{i+1}] be a body capsule (the
continuous segment; radius unchanged by repair), A' = [Q_i + δ_i, Q_{i+1} + δ_{i+1}] its
post-repair image, and W a static obstacle (wall/prop segment, fixed radius). Then

    |d(A', W) − d(A, W)| ≤ max(‖δ_i‖, ‖δ_{i+1}‖) ≤ Λ = 0.0042 u.

*Proof.* Every point of A' is p' = (1−t)(Q_i + δ_i) + t(Q_{i+1} + δ_{i+1}) = q + m(t) with
q = (1−t)Q_i + tQ_{i+1} ∈ A and m(t) = (1−t)δ_i + tδ_{i+1}, so ‖m(t)‖ ≤ (1−t)‖δ_i‖ + t‖δ_{i+1}‖ ≤
max(‖δ_i‖, ‖δ_{i+1}‖) ≤ Λ (convexity of the norm — no same-direction assumption). Hence
d(p', W) ≥ d(q, W) − Λ, and taking the infimum over p' ∈ A': d(A', W) ≥ d(A, W) − Λ. The symmetric
argument (every q ∈ A is within Λ of some p' ∈ A') gives the reverse inequality. ∎

**Capsule–capsule (self-collision).** The same Hausdorff argument gives
|d(A', B') − d(A, B)| ≤ d_H(A', A) + d_H(B', B) ≤ Λ_A + Λ_B ≤ 2Λ for every capsule pair —
the capsule-level form of Theorem V2, covering the continuous geometry (every surface point,
not only ring centers; radii are constant under repair, so the bounds transfer to the
sagitta-inflated π measurement unchanged).

**Why no universal bound below 2Λ exists for self-pairs (transmission analysis).** The exact
per-step displacement dynamics δ_{k+1} = (SEG − ‖v_k⁰ − δ_k‖)·ŵ_k has the first-order form
δ_{k+1} = P_k δ_k − e_k⁰ t̂_k (P_k = orthogonal projector onto the segment-k direction; the
first-order form is used only for this analysis, never for an adopted bound). Consequences:
displacement magnitude transmits along the chain with per-joint factor |cos θ| ≤ 1 and, on gentle
turns, the world-direction **rotates with the chain**; a gentle 180° arc therefore yields
anti-parallel near-maximal displacements at its two ends (measured cos = −0.9966) — so any bound
‖δ_j − δ_i‖ < 2Λ is false in general. The measured constructions bracket the true separation-loss
supremum: 0.206Λ (chord-perpendicular geometry) to **1.599Λ** (chord-aligned geometry); the exact
supremum is unresolved within [1.599Λ, 2Λ], and no design decision depends on narrowing it — all
thresholds are sized on the proven ceiling 2Λ.

## C4.4 — Q4: threshold recalculation

T6c and T6d are **static-obstacle** quantities (the harness measures wall clearance — walls do not
move), so the proven governing bound is Λ (Theorem V3), not 2Λ:

| Threshold | Value | Status |
|---|---|---|
| T6d (per-frame obstacle-clearance regression) | ≤ 0.005 u | **UNCHANGED** — echo ≤ Λ = 0.0042 (Th. V3), margin 0.0008; the v1.8/v1.9 heuristic "2×0.0021 echo" is upgraded to a theorem |
| T6c (minimum true obstacle clearance) | ≥ −0.0067 u | **UNCHANGED** — 0.0025 measurement margin + 0.0042 proven echo (Th. V3) |
| **T6e (NEW: per-frame self-collision clearance regression, all \|i−j\| ≥ 9 capsule pairs)** | ≤ 2Λ = 0.0084 u | **ADDED** — governed by Th. V2; verified E1–E3 |
| T6a / T6b-i / T6b-ii / T3 | 0.0021 / SEG ± 1e−5 / 0.0045 wire / 0.0025 | unchanged (T6b-ii = proven Λ + 0.0003 margin, Th. V1) |
| cap 5 (Λ = 0.0042), caps 1–4, π bands 0.005/0.02, R1–R5 | — | unchanged (π is a measured quantity; no derivation needed) |

**Recorded limitation L4.** Under the adversarial chord-aligned field, the self-collision echo
(≤ 2Λ = 0.0084) can take a self-pair solved at the +0.0025 u margin to −0.0059 u for one frame —
inside the FAULT band (0.005, 0.02], far below the R1 hard gate (0.02). Runtime handling: the
measured-π gate R-FINAL governs the band, and the next frame's Stage-4 solver re-demands the
penetration (self-healing, v1.8 §2.5). Harness gate: T6e. Considered and **rejected** alternative:
reduce Λ to 0.0025 so that 2Λ = 0.005 fits T6d unchanged — rejected because it would engage cap 5
on the worked example (ΣΔL = 0.002519 > 0.0025), slow broad-field absorption, and perturb verified
numbers, with no safety benefit since T6e covers the pairwise exposure.

## C4.5 — Q5: coverage of pairs and continuous geometry

- **All ring pairs**, including every |i−j| ≥ 9 self-collision pair: Th. V2 (E1: 3160 pairs ×
  300 randomized configs, max 0.000182 ≤ 2Λ; E2: adversarial 0.006718 ≤ 2Λ).
- **Adjacent pairs:** R1 exact identity (E4: 0.001980 ≤ 0.0021, identity exact to 1.7e−16).
- **Continuous capsule geometry** — every point of every capsule surface, not only ring centers:
  Th. V3's convex-combination + Hausdorff proof covers the whole segment; E3 measures true
  segment–segment distances (self-pair 0.006693 ≤ 2Λ; static wall 0.003032 / 0.003473 ≤ Λ).
- Radii are constant under repair (only centers move), so the bounds apply verbatim to the
  sagitta-inflated radii used by the π measurement.

## C4.6 — Additional R-FINAL check: the deadline horizon

**Confirmed.** The v1.9 rule and checker used `n > spike_end + 30`, which displays the horizon
frame spike_end + 30 in the fault band even though the deadline ("π < 0.005 within 30 frames of
spike end") is already missed **at** that frame — exactly one extra FAULT frame.

**Fix (rule and checker agree exactly).** Clause (d) now reads: band rendering is revoked from the
**first frame n ≥ spike_end + 30 whose candidate has π(n) ≥ 0.005 u** — the horizon frame itself is
not displayed. Consequences: post-spike band exposure ≤ 29 frames < 0.5 s; "π < 0.005 within 30
frames" is enforced exactly; the revocation remains sticky until clean recovery (π ≤ 0.005 passes
R1). D4 re-verified with the strict horizon: S1 (fast recovery) and S3 (intermittent re-entry)
unchanged; S2 (continuous stall): (c) fires at the 13th band frame, (d) fires at frame
35 = spike_end + 30 with the horizon frame not displayed, R3/R4 thereafter.

## Assumptions

- **A1 (cap domain).** Stage-8 input satisfies |e_k⁰| ≤ 0.0019804 u and Σ_k |e_k⁰| ≤ Λ = 0.0042 u
  (caps 1–5, enforced by construction; E2 constructions are checked against the full domain,
  with the failing cap named when rejected).
- **A2 (static obstacles within the frame).** T6c/T6d/T6e obstacle and self-pair regressions are
  measured within one frame's pipeline; obstacle motion between frames is outside these bounds
  (it is handled by the per-frame re-solve and the measured-π gate).
- **A3 (pass contract).** One repair pass per frame; ring 0 anchored (native v4.2 contract,
  L1505–1517).
- **A4 (scale separation).** SEG = 0.1 u ≫ displacements (≤ 0.0042 u). First-order reasoning is
  used ONLY in the transmission/tightness analysis; every adopted bound (V1, V2, V3, R1, R2) is
  exact.
- **A5 (arithmetic).** float64; test tolerances 1e−9 (bounds) / 1e−12 (identities).

---
## Verification output and source

**Fresh complete run output** (exact stdout of the attached script; sections A-D behaviorally identical to v1.9, D4 with the strict horizon, E new):

```
==============================================================================
A. SUB-CASE 0 : straight chain along x, single parallel demand at ring 13
==============================================================================
delta*_x  min -0.00025000  max -0.00025000   (uniform)
sum delta*_x = -0.02000000  (= demand total: translation preserved)
-0.020/80 = -0.00025000
tent u_12 = -0.003250  u_13 = +0.016500
det = 80.0000  lam_min = 0.00154193  lam_max = 3.998458  kappa = 2593.2
Poincare 2-2cos(pi/80) = 0.00154193  kappa <= 4/that = 2594.2
Green check [30,55]: 9.30000000 vs 9.30000000
max segment differential = 3.47e-18  -> dL = 0 (rigid slide)
post-absorption residual: ring 13 -0.019750, others +0.000250, sum +0.00e+00, ||ro'|| = 0.019875
frame-2 projected slide/ring = -0.000000000  -> parallel-gradient stall confirmed

==============================================================================
B/C. WORKED EXAMPLE : near-anti fold + two wall contacts, full pipeline
==============================================================================

-- geometry (x / y / z) --
  P[ 9] = (+0.9000, 0.0200, +0.0000)
  P[10] = (+1.0000, 0.0200, +0.0000)
  P[11] = (+1.0087, 0.0200, +0.0996)
  P[12] = (+0.9102, 0.0200, +0.1170)
  P[13] = (+1.0090, 0.0200, +0.1013)
  P[14] = (+1.1088, 0.0200, +0.0944)
  P[15] = (+1.2088, 0.0200, +0.0944)
  P[62] = (+5.9088, 0.0200, +0.0944)
  P[65] = (+6.2088, 0.0200, +0.0944)
  P[67] = (+6.4088, 0.0200, +0.0944)
  P[68] = (+6.5088, 0.0200, +0.0944)
near-anti joint t11.t12 = -0.999848

-- derived residual field (rings with nonzero bump) --
  10:0.0071  11:0.0071  12:0.0245  13:0.0088  14:0.0019  15:0.0019  16:0.0009  62:0.0119  63:0.0119  64:0.0119  65:0.0119  66:0.0119  67:0.0119  68:0.0109
  max ring-to-ring differential of residual = 0.0174 (d_cap 0.02 -> OK)
  clearance-after-solve check (target <= -0.0025): violations = []
  render strain: min -1.52%  max +0.70%  (Tier-3 +/-5%)
  pre-projection differential max = 0.0174 (d_cap 0.02)
  render clearance (true segment-segment): wall A +0.002112  wall B +0.002114

-- caps --
  drain cap 0.025: clipped rings = 0
  a_cap 0.02: clipped rings = 1 (ring 12 |ro| = 0.0245)
  l2 0.035: ||a|| pre = 0.039406 -> scale x0.888195, post = 0.035000

-- projection --
  rank(C) = 79/79   kappa(CC^T) = 1923.5  (universal bound 2594.2)
  ||C delta*||_inf = 7.793e-19
  max |w_par| = 7.793e-19   max |w_perp| = 0.011296 (d_cap 0.02 -> OK)
  max dL = 0.000636 at segment 11 (w_par +2.17e-19, w_perp 0.011296); single-segment bound 0.001980
  total stretch sum(dL) = 0.002519
  C1 cap-5 check: sum(dL) = 0.002519 <= LAMBDA = 0.0042  -> cap 5 not engaged
  far-field leakage max|delta*_i| = 3.383e-05
  retained ||a - delta*|| = 0.001993 (5.7% of demand)
  rigid-component preservation: sum(a) = (+0.000000,+0.000000,-0.115400)  sum(delta*) = (+0.000000,+0.000000,-0.115400)  max dev = 1.76e-19
  per-ring delta*_z on arc A (rings 9..17):
   -0.00000 -0.00633 -0.00634 -0.01746 -0.00799 -0.00181 -0.00166 -0.00083 -0.00000
  per-ring delta*_z on arc B (rings 60..68):
   -0.00000 -0.00000 -0.01053 -0.01055 -0.01055 -0.01055 -0.01055 -0.01055 -0.00970

-- paired transfer: render invariance max|dX| = 1.388e-17

-- Stage-8 rope repair --
  isolated identity |delta| = |dL|: 0.001980400000 vs 0.001980400000  (dev 1.73e-18)
  chained pass: max ||delta_local(k)| - |dL_k|| = 2.00e-04 (2nd-order chaining, expected)
  cumulative ring displacement max = 0.001042
  post-repair max|len - SEG| = 3.747e-16

-- next-frame validation (X' = P_repaired + _ro') --
  wall A: +0.002112 -> +0.002112   (regression +0.000000)
  wall B: +0.002114 -> +0.002110   (regression +0.000003)
  pi(next frame) = 0.000000  -> PASS band
  T6a |dL| <= 0.0021        : 0.000636   PASS
  T6b |disp_rep| <= 0.0045  : 0.001042   PASS  (wire; proven bound 0.0042 + 0.0003 margin, Th. V1)
  T6c clearance >= -0.0067  : +0.002110   PASS
  T6d regression <= 0.005   : 0.000003   PASS

-- final positions, arc A (x / z): P -> P+delta* -> P_repaired, and _ro' --
  ring 10: (+1.0000,+0.0000) -> (+1.0000,-0.0063) -> (+0.9998,-0.0063)   ro'=(+0.000000,-0.000794)
  ring 11: (+1.0087,+0.0996) -> (+1.0088,+0.0933) -> (+1.0088,+0.0933)   ro'=(-0.000064,-0.000788)
  ring 12: (+0.9102,+0.1170) -> (+0.9083,+0.0995) -> (+0.9090,+0.0995)   ro'=(+0.001898,-0.007047)
  ring 13: (+1.0090,+0.1013) -> (+1.0086,+0.0933) -> (+1.0088,+0.0933)   ro'=(+0.000398,-0.000855)
  ring 14: (+1.1088,+0.0944) -> (+1.1088,+0.0926) -> (+1.1088,+0.0926)   ro'=(-0.000034,-0.000053)
  ring 15: (+1.2088,+0.0944) -> (+1.2088,+0.0927) -> (+1.2088,+0.0927)   ro'=(-0.000034,-0.000209)
  ring 16: (+1.3088,+0.0944) -> (+1.3088,+0.0935) -> (+1.3088,+0.0935)   ro'=(-0.000034,-0.000104)

-- frames 2-3 (drain continuation) --
  frame 2: ||a|| = 0.008222  max dL = 0.000187  max|rep| = 0.000187  residual max arcA/arcB = 0.002225 / 0.000178
  frame 3: ||a|| = 0.002382  max dL = 0.000000  max|rep| = 0.000000  residual max arcA/arcB = 0.002222 / 0.000185
  arc-A residual detail after frame 3 (rings 10..16, z-component):
   10:-0.000009 11:+0.000006 12:-0.000004 13:+0.000007 14:-0.000002 15:+0.000022 16:-0.000001
  sum_z arc-A residual = -0.00000039 (near-zero-sum gradient -> L1 stall mode)

==============================================================================
D. Amendment v1.9 C1: rope-repair displacement bound (Th. P1 / Th. V1)
==============================================================================

  per-segment domain bound sqrt(SEG^2+d_cap^2)-SEG = 0.0019804   (T6a wire 0.0021)
  cap-5 budget LAMBDA = 0.0042 = 2 x 0.0021;  2 x dL(d_cap) = 0.003961 <= LAMBDA  (<=2 full-d_cap segments never engage cap 5)

D1  collinear chain, anti-correlated normal zigzag demand
  admissible under v1.8 caps 1-4: |delta_i| = 0.003913 <= a_cap 0.020;  ||delta||_2 = 0.035000 <= l2 0.035;
  |w_perp| = 0.007826 <= d_cap 0.02;  |w_par| = 0
  e_input per segment = 0.0003058   SUM over 79 = 0.0241568
  UNCAPPED pass: max ring displacement = 0.017449
  -> v1.8 T6b-ii '0.0045' presented as a universal bound is REFUTED
     on v1.8's own input domain (it was empirical, worked-example-only)
  with cap 5: s* = 0.416707   sum e = 0.0042000 <= 0.0042
  capped pass: max ring displacement = 0.003892958   <= LAMBDA + 1e-9  PASS (Th. V1)

D2  hairpin extremes (same demand field as D1)
  anti-aligned ladder: min g_k = t_k.t_(k+1) = -1.000000
  UNCAPPED: 0.000306  (g = -1: transfers cancel -> benign)
  capped:   0.000053165   PASS
  single 175-deg fold at segment 30: UNCAPPED 0.017610   capped 0.004102177  PASS

D3  randomized suite: 300 configs x real projection + caps + repair
  cap-5 engaged in 0/300 runs;  max |w_par| = 2.91e-18
  max sum|e_input|  = 0.0008741   <= LAMBDA + 1e-9  OK
  max ring displacement = 0.000238344   <= LAMBDA + 1e-9  PASS (Th. V1)
  max post-repair |len - SEG| = 4.86e-16   (in-frame exactness)

D4  Stage-5 R-FINAL checker (synthetic pi/drain series; rule logic)
  S1 fast recovery (12 band frames, clean by frame 12 < 32): a/b/c/d all hold = True; actions: 12x FAULT-RENDER -> PASS
  S2 stall at pi = 0.008: (c) fired = True (13th band frame); (d) fired = True (frame 35 = spike_end + 30, horizon frame not displayed);
      R3/R4 frames = 38; band rendering revoked until clean recovery
  S3 intermittent re-entry: (c) fired = True (18 band frames > 12 budget); (a)/(b)/(d) held = True/True/True

==============================================================================
E. Amendment v1.10 C4: pairwise clearance loss (Th. V2 / Th. V3)
==============================================================================

  Th. V2 (any ring pair i,j): |D'_ij - D_ij| <= ||d_j - d_i|| <= 2*LAMBDA = 0.0084
  Th. V3 (capsule vs STATIC obstacle): |dd| <= max endpoint motion <= LAMBDA = 0.0042

E1  pairwise separation-change sweep (300 randomized configs)
  max ring displacement     = 0.000174663   <= LAMBDA   PASS (Th. V1)
  max |dD| ALL pairs        = 0.000181880   <= 2*LAMBDA PASS (Th. V2)
  max |dD| |i-j| >= 9 pairs = 0.000181880   <= 2*LAMBDA PASS (Th. V2)

E2  adversarial constructions: cap-boundary stretch field + U-turn
  anti-parallel demo: sawtooth + U76 (chord perp):
    sum|e| = 0.003961 <= LAMBDA;  |d_i| = 0.003811 (ring 2),  |d_j| = 0.003477 (ring 77),  cos(d_i,d_j) = -0.9892
    pair (2,77) separation change = 0.000863 = 0.206 x LAMBDA
    max |dD| all pairs = 0.003741 = 0.891 x LAMBDA   <= 2*LAMBDA  PASS (Th. V2)
  chord-aligned:     zigzag-4 + leg 51 + U20:
    sum|e| = 0.004200 <= LAMBDA;  |d_i| = 0.003928 (ring 4),  |d_j| = 0.003032 (ring 77),  cos(d_i,d_j) = -0.9966
    pair (4,77) separation change = 0.006632 = 1.579 x LAMBDA
    max |dD| all pairs = 0.006718 = 1.599 x LAMBDA   <= 2*LAMBDA  PASS (Th. V2)
  chord-aligned:     ramp-teeth + leg 45 + U20: NOT in-domain (violates: ||offsets||_2 > l2)
  constructive lower bound of the pairwise supremum: 0.006718 = 1.599 x LAMBDA;
  proven supremum (Th. V2) = 2*LAMBDA = 0.0084; design bound adopted: 2*LAMBDA

E3  capsule-level checks (segment-segment distance, not ring centers)
  chord-aligned case: self-pair capsules (4,5) vs (77,78): 4.772261 -> 4.778954   |dd| = 0.006693   <= 2*LAMBDA  PASS (Th. V2)
  chord-aligned case: STATIC-wall clearance, capsule (77,78): 0.040000 -> 0.036968   |dd| = 0.003032   <= LAMBDA  PASS (Th. V3)
  anti-parallel case: self-pair capsules (2,3) vs (77,78): 4.834521 -> 4.834352   |dd| = 0.000170   <= 2*LAMBDA  PASS (Th. V2)
  anti-parallel case: STATIC-wall clearance, capsule (77,78): 0.040000 -> 0.036527   |dd| = 0.003473   <= LAMBDA  PASS (Th. V3)

E4  adjacent-pair identity (exact repair)
  max |dD_adjacent - |e_k|| = 1.67e-16   (identity |dD| = |e_k| exact to fp)
  max adjacent |dD| = 0.001980 <= 0.0021 (T6a domain): PASS

DONE

```

**Complete verification source** — `v18_example.py`, 729 lines, identical to the attached file `download/v18_example.py`:

```python
#!/usr/bin/env python3
"""
Amendment v1.8 + v1.9 (C1) + v1.10 (C4) verification for the Anaconda
v4.2 design (no product code touched).

A. Sub-case 0 : straight 80-ring chain, single parallel demand at ring 13
                -> full-chain admissibility projection delta* = a - C^T (C C^T)^-1 C a
B. Universal rank / conditioning numerics vs measured values
C. Worked example: near-anti fold + two wall contacts, full frame pipeline:
   residual derivation (clearance sweep + Tier-3 strain relief) ->
   caps (drain, a_cap, l2) -> global projection -> differential-cap check ->
   paired transfer (render neutrality) -> Stage-8 rope repair (local vs
   cumulative) -> next-frame validation -> frames 2-3 (drain / L1-stall).
D. Amendment v1.9 C1 verification: rope-repair displacement bound.
   D1 collinear worst case (refutes the uncapped universal 0.0045 claim,
      then proves the capped 0.0042 bound), D2 hairpin extremes (anti-aligned
      ladder g=-1, single 175-deg fold), D3 randomized suite (300 configs
      through the real projection + caps 1-5 + repair), D4 Stage-5 R-FINAL
      rule checker on synthetic series.
E. Amendment v1.10 C4 verification: pairwise clearance loss.
   E1 pairwise separation-change sweep (all pairs and |i-j| >= 9), E2
   adversarial constructions (anti-parallel demo vs chord-aligned tightness),
   E3 continuous capsule geometry (self-pair + static wall), E4 adjacent-pair
   identity; D4 fixed to the strict R-FINAL horizon (n >= spike_end + 30).
"""
import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=200)
SEG = 0.1
N = 80
M = N - 1

# ---------------------------------------------------------------------------
def seg_point_dist_2d(p, a, b):
    d = b - a
    dd = d @ d
    t = 0.0 if dd == 0 else np.clip((p - a) @ d / dd, 0.0, 1.0)
    return np.linalg.norm(p - (a + t * d))

def seg_seg_dist_2d(p1, p2, q1, q2):
    ts = np.linspace(0, 1, 201)
    P = p1[None, :] + ts[:, None] * (p2 - p1)[None, :]
    Q = q1[None, :] + ts[:, None] * (q2 - q1)[None, :]
    return np.linalg.norm(P[:, None, :] - Q[None, :, :], axis=2).min()

def build_C(P):
    T = (P[1:] - P[:-1]) / SEG
    C = np.zeros((M, 3 * N))
    for k in range(M):
        C[k, 3 * (k + 1):3 * (k + 2)] += T[k]
        C[k, 3 * k:3 * k + 3]         -= T[k]
    return C, T

def project(C, a_flat):
    G = C @ C.T
    u = np.linalg.solve(G, C @ a_flat)
    return a_flat - C.T @ u, G, u

def apply_caps(ro_vecs):
    """drain cap -> per-ring a_cap -> l2 budget.  Returns a, and cap report."""
    a = ro_vecs.copy()
    sc = np.minimum(1.0, kabs_dt / np.maximum(np.linalg.norm(a, axis=1), 1e-12))
    a *= sc[:, None]
    n_drain = int(np.sum(sc < 1.0 - 1e-12))
    na = np.linalg.norm(a, axis=1)
    n_acap = int(np.sum(na > A_CAP + 1e-12))
    a[na > A_CAP] *= (A_CAP / na[na > A_CAP])[:, None]
    n2 = np.linalg.norm(a)
    scale2 = min(1.0, L2_CAP / n2)
    if scale2 < 1.0:
        a *= scale2
    return a, n_drain, n_acap, n2, scale2

def repair(Pin):
    """Stage-8 forward renormalization; returns P', cumulative disp, local |dL|."""
    Pw = Pin.copy()
    disp = np.zeros((N, 3))
    loc = np.zeros(M)
    for k in range(M):
        v = Pw[k + 1] - Pw[k]
        L = np.linalg.norm(v)
        loc[k] = L - SEG
        tgt = Pw[k] + SEG * v / L
        disp[k + 1] = tgt - Pw[k + 1]
        Pw[k + 1] = tgt
    return Pw, disp, loc

def min_clearance(wall, lo, hi, Xs):
    a, b, r = wall
    best = 1e9
    for i in range(lo, hi):
        best = min(best, seg_seg_dist_2d(Xs[i, [0, 2]], Xs[i + 1, [0, 2]], a, b) - r - R_BODY)
    return best

def dL_of(delta, T):
    w = delta[1:] - delta[:-1]
    dot = np.einsum('ij,ij->i', w, T)
    wperp = np.linalg.norm(w - dot[:, None] * T, axis=1)
    return np.sqrt((SEG + np.abs(dot)) ** 2 + wperp ** 2) - SEG, np.abs(dot), wperp

# constants (60 fps)
kabs_dt = 0.025      # drain per frame
A_CAP   = 0.020      # per-ring per-frame transfer cap (Fix 3)
L2_CAP  = 0.035      # body l2 budget per frame
D_CAP   = 0.020      # ring-to-ring differential cap
LAMBDA  = 0.0042     # v1.9 C1 cap 5: total-sagitta budget per frame
R_BODY  = 0.05
MARGIN  = 0.0025     # solve target margin

# ===========================================================================
print("=" * 78)
print("A. SUB-CASE 0 : straight chain along x, single parallel demand at ring 13")
print("=" * 78)
Bx = np.zeros((M, N))
for k in range(M):
    Bx[k, k] = -1.0
    Bx[k, k + 1] = 1.0
a0 = np.zeros(N)
a0[13] = -0.020
G0 = Bx @ Bx.T
u0 = np.linalg.solve(G0, Bx @ a0)
dx0 = a0 - Bx.T @ u0
print(f"delta*_x  min {dx0.min():+.8f}  max {dx0.max():+.8f}   (uniform)")
print(f"sum delta*_x = {dx0.sum():+.8f}  (= demand total: translation preserved)")
print(f"-0.020/80 = {-0.020/80:+.8f}")
print(f"tent u_12 = {u0[12]:+.6f}  u_13 = {u0[13]:+.6f}")
lam0 = np.linalg.eigvalsh(G0)
print(f"det = {np.linalg.det(G0):.4f}  lam_min = {lam0.min():.8f}  "
      f"lam_max = {lam0.max():.6f}  kappa = {lam0.max()/lam0.min():.1f}")
print(f"Poincare 2-2cos(pi/80) = {2-2*np.cos(np.pi/80):.8f}  "
      f"kappa <= 4/that = {4/(2-2*np.cos(np.pi/80)):.1f}")
Ginv = np.linalg.inv(G0)
print(f"Green check [30,55]: {Ginv[30,55]:.8f} vs "
      f"{(min(30,55)+1)*(79-max(30,55))/80:.8f}")
w0 = np.diff(dx0)
print(f"max segment differential = {np.abs(w0).max():.2e}  -> dL = 0 (rigid slide)")
ro1p = a0 - dx0
print(f"post-absorption residual: ring 13 {ro1p[13]:+.6f}, others {ro1p[0]:+.6f}, "
      f"sum {ro1p.sum():+.2e}, ||ro'|| = {np.linalg.norm(ro1p):.6f}")
u2 = np.linalg.solve(G0, Bx @ ro1p)
dx2 = ro1p - Bx.T @ u2
print(f"frame-2 projected slide/ring = {dx2[0]:+.9f}  -> parallel-gradient stall confirmed")

# ===========================================================================
print()
print("=" * 78)
print("B/C. WORKED EXAMPLE : near-anti fold + two wall contacts, full pipeline")
print("=" * 78)

th = np.zeros(M)
th[10] = np.deg2rad(85.0)
th[11] = np.deg2rad(170.0)
th[12] = np.deg2rad(351.0)
th[13] = np.deg2rad(356.0)
P = np.zeros((N, 3))
P[:, 1] = 0.02
for k in range(M):
    P[k + 1] = P[k] + SEG * np.array([np.cos(th[k]), 0.0, np.sin(th[k])])

print("\n-- geometry (x / y / z) --")
for i in [9, 10, 11, 12, 13, 14, 15, 62, 65, 67, 68]:
    print(f"  P[{i:2d}] = ({P[i,0]:+.4f}, {P[i,1]:.4f}, {P[i,2]:+.4f})")
T0 = (P[1:] - P[:-1]) / SEG
print(f"near-anti joint t11.t12 = {T0[11] @ T0[12]:+.6f}")

WALL_A = (np.array([0.80, 0.175]), np.array([1.25, 0.175]), 0.03)
WALL_B = (np.array([5.95, 0.165]), np.array([6.45, 0.165]), 0.03)

def pen(i, wall, Xs=None):
    a, b, r = wall
    Xs = P if Xs is None else Xs
    return (r + R_BODY) - seg_point_dist_2d(Xs[i, [0, 2]], a, b)

def pen_mid(i, wall, Xs=None):
    a, b, r = wall
    Xs = P if Xs is None else Xs
    mid = 0.5 * (Xs[i] + Xs[i + 1])
    return (r + R_BODY) - seg_point_dist_2d(mid[[0, 2]], a, b)

# ---- derive the post-solve residual field ---------------------------------
def derive_bump(wall, arc):
    b = {i: 0.0 for i in arc}
    segs = list(arc)[:-1]
    # fixed-point clearance sweep on the LIVE bumped state
    for _ in range(400):
        worst = 0.0
        X = P.copy()
        X[:, 2] -= np.array([b.get(i, 0.0) for i in range(N)])
        for i in arc:
            p = pen(i, wall, X)
            if p > -MARGIN + 1e-12:
                b[i] += (p + MARGIN) * 1.001 + 1e-9
                worst = max(worst, p + MARGIN)
        X = P.copy()                      # rebuild: ring raises took effect
        X[:, 2] -= np.array([b.get(i, 0.0) for i in range(N)])
        for i in segs:
            pm = pen_mid(i, wall, X)
            if pm > -MARGIN + 1e-12:
                if b[i] <= b[i + 1]:
                    b[i] += (pm + MARGIN) * 1.001 + 1e-9
                else:
                    b[i + 1] += (pm + MARGIN) * 1.001 + 1e-9
                worst = max(worst, pm + MARGIN)
        if worst == 0.0:
            break
    # Tier-3 compression relief: raise-to-max (monotone, never lowers)
    for _ in range(400):
        ch = False
        for i in segs:
            w = np.array([0.0, 0.0, -(b[i + 1] - b[i])])
            Lv = np.linalg.norm(SEG * T0[i] + w)
            if (Lv - SEG) / SEG < -0.04:
                m = max(b[i], b[i + 1])
                if abs(b[i] - m) > 1e-12 or abs(b[i + 1] - m) > 1e-12:
                    b[i] = m
                    b[i + 1] = m
                    ch = True
        if not ch:
            break
    return b

bumpA = derive_bump(WALL_A, range(9, 18))
bumpB = derive_bump(WALL_B, range(58, 69))
bump = np.zeros(N)
for i, v in bumpA.items():
    bump[i] = max(bump[i], v)
for i, v in bumpB.items():
    bump[i] = max(bump[i], v)
ro = np.zeros((N, 3))
ro[:, 2] = -bump

print("\n-- derived residual field (rings with nonzero bump) --")
sup = [i for i in range(N) if bump[i] > 1e-9]
print("  " + "  ".join(f"{i}:{bump[i]:.4f}" for i in sup))
diff_pre = np.abs(bump[1:] - bump[:-1]).max()
print(f"  max ring-to-ring differential of residual = {diff_pre:.4f} "
      f"(d_cap {D_CAP} -> {'OK' if diff_pre <= D_CAP + 1e-9 else 'VIOLATION'})")

# verification of solve quality on the render state X = P + ro
X = P + ro
okA = all(pen(i, WALL_A, X) <= -MARGIN + 1e-9 or pen(i, WALL_A, X) < 0 for i in range(9, 18))
viol = []
for wall, arc in ((WALL_A, range(9, 18)), (WALL_B, range(58, 69))):
    for i in arc:
        if pen(i, wall, X) > -MARGIN + 1e-9:
            viol.append(("ring", i, pen(i, wall, X)))
    for i in list(arc)[:-1]:
        if pen_mid(i, wall, X) > -MARGIN + 1e-9:
            viol.append(("mid", i, pen_mid(i, wall, X)))
print(f"  clearance-after-solve check (target <= -{MARGIN}): violations = {viol}")
Lx = np.linalg.norm(X[1:] - X[:-1], axis=1)
strain = (Lx - SEG) / SEG * 100
print(f"  render strain: min {strain.min():+.2f}%  max {strain.max():+.2f}%  "
      f"(Tier-3 +/-5%)")
print(f"  pre-projection differential max = "
      f"{np.linalg.norm(ro[1:] - ro[:-1], axis=1).max():.4f} (d_cap {D_CAP})")

preA = min_clearance(WALL_A, 9, 18, X)
preB = min_clearance(WALL_B, 58, 69, X)
print(f"  render clearance (true segment-segment): wall A {preA:+.6f}  "
      f"wall B {preB:+.6f}")

# ---- caps -------------------------------------------------------------------
a, n_drain, n_acap, n2pre, scale2 = apply_caps(ro)
print("\n-- caps --")
print(f"  drain cap {kabs_dt}: clipped rings = {n_drain}")
print(f"  a_cap {A_CAP}: clipped rings = {n_acap} "
      f"(ring 12 |ro| = {np.linalg.norm(ro[12]):.4f})")
print(f"  l2 {L2_CAP}: ||a|| pre = {n2pre:.6f} -> scale x{scale2:.6f}, "
      f"post = {np.linalg.norm(a):.6f}")

# ---- projection --------------------------------------------------------------
C, T = build_C(P)
delta, G, u = project(C, a.reshape(-1))
delta = delta.reshape(N, 3)
rankC = np.linalg.matrix_rank(C)
kap = np.linalg.cond(G)
print("\n-- projection --")
print(f"  rank(C) = {rankC}/{M}   kappa(CC^T) = {kap:.1f}  (universal bound 2594.2)")
print(f"  ||C delta*||_inf = {np.abs(C @ delta.reshape(-1)).max():.3e}")
dL, wpar, wperp = dL_of(delta, T)
print(f"  max |w_par| = {wpar.max():.3e}   max |w_perp| = {wperp.max():.6f} "
      f"(d_cap {D_CAP} -> {'OK' if wperp.max() <= D_CAP + 1e-9 else 'CLIP'})")
im = int(np.argmax(dL))
print(f"  max dL = {dL[im]:.6f} at segment {im} "
      f"(w_par {wpar[im]:+.2e}, w_perp {wperp[im]:.6f}); "
      f"single-segment bound {np.sqrt(SEG**2 + D_CAP**2) - SEG:.6f}")
print(f"  total stretch sum(dL) = {dL.sum():.6f}")
print(f"  C1 cap-5 check: sum(dL) = {dL.sum():.6f} <= LAMBDA = {LAMBDA}  -> "
      f"{'cap 5 not engaged' if dL.sum() <= LAMBDA + 1e-12 else 'SCALE DOWN'}")
far = [i for i in range(N) if not (8 <= i <= 18 or 59 <= i <= 69)]
print(f"  far-field leakage max|delta*_i| = {np.linalg.norm(delta[far],axis=1).max():.3e}")
print(f"  retained ||a - delta*|| = {np.linalg.norm((a - delta).ravel()):.6f} "
      f"({100*np.linalg.norm((a-delta).ravel())/np.linalg.norm(a):.1f}% of demand)")
sa = a.reshape(N, 3).sum(axis=0)
sd = delta.sum(axis=0)
print(f"  rigid-component preservation: sum(a) = ({sa[0]:+.6f},{sa[1]:+.6f},{sa[2]:+.6f})  "
      f"sum(delta*) = ({sd[0]:+.6f},{sd[1]:+.6f},{sd[2]:+.6f})  "
      f"max dev = {np.abs(sa - sd).max():.2e}")
print("  per-ring delta*_z on arc A (rings 9..17):")
print("   " + " ".join(f"{delta[i,2]:+.5f}" for i in range(9, 18)))
print("  per-ring delta*_z on arc B (rings 60..68):")
print("   " + " ".join(f"{delta[i,2]:+.5f}" for i in range(60, 69)))

# ---- paired transfer ----------------------------------------------------------
Xb = P + ro
P2 = P + delta
ro2 = ro - delta
print(f"\n-- paired transfer: render invariance max|dX| = "
      f"{np.abs(Xb - (P2 + ro2)).max():.3e}")

# ---- Stage-8 repair ------------------------------------------------------------
P2, disp, loc = repair(P2)
Lpost = np.linalg.norm(P2[1:] - P2[:-1], axis=1)
print("\n-- Stage-8 rope repair --")
# isolated single-segment Lemma-1 identity: v' arbitrary, delta = SEG v'/|v'| - v'
rng = np.random.default_rng(7)
vp = rng.normal(size=3)
vp = vp / np.linalg.norm(vp) * (SEG + 0.0019804)
dl_iso = SEG * vp / np.linalg.norm(vp) - vp
print(f"  isolated identity |delta| = |dL|: {np.linalg.norm(dl_iso):.12f} vs "
      f"{abs(np.linalg.norm(vp) - SEG):.12f}  (dev "
      f"{abs(np.linalg.norm(dl_iso) - abs(np.linalg.norm(vp) - SEG)):.2e})")
loc_corr = np.linalg.norm(np.diff(P2 - (P + delta), axis=0), axis=1)
print(f"  chained pass: max ||delta_local(k)| - |dL_k|| = "
      f"{np.abs(loc_corr - np.abs(dL)).max():.2e} (2nd-order chaining, expected)")
print(f"  cumulative ring displacement max = {np.linalg.norm(disp, axis=1).max():.6f}")
print(f"  post-repair max|len - SEG| = {np.abs(Lpost - SEG).max():.3e}")

# ---- next-frame validation ------------------------------------------------------
Xn = P2 + ro2
postA = min_clearance(WALL_A, 9, 18, Xn)
postB = min_clearance(WALL_B, 58, 69, Xn)
regA, regB = preA - postA, preB - postB
print("\n-- next-frame validation (X' = P_repaired + _ro') --")
print(f"  wall A: {preA:+.6f} -> {postA:+.6f}   (regression {regA:+.6f})")
print(f"  wall B: {preB:+.6f} -> {postB:+.6f}   (regression {regB:+.6f})")
pi_next = max(0.0, -min(postA, postB))
print(f"  pi(next frame) = {pi_next:.6f}  -> "
      f"{'PASS band' if pi_next <= 0.005 else 'FAULT band' if pi_next <= 0.02 else 'RETRY'}")
print(f"  T6a |dL| <= 0.0021        : {dL.max():.6f}   "
      f"{'PASS' if dL.max() <= 0.0021 else 'FAIL'}")
print(f"  T6b |disp_rep| <= 0.0045  : {np.linalg.norm(disp, axis=1).max():.6f}   "
      f"{'PASS' if np.linalg.norm(disp, axis=1).max() <= 0.0045 else 'FAIL'}"
      f"  (wire; proven bound {LAMBDA} + 0.0003 margin, Th. V1)")
print(f"  T6c clearance >= -0.0067  : {min(postA, postB):+.6f}   "
      f"{'PASS' if min(postA, postB) >= -0.0067 else 'FAIL'}")
print(f"  T6d regression <= 0.005   : {max(regA, regB):.6f}   "
      f"{'PASS' if max(regA, regB) <= 0.005 else 'FAIL'}")
print("\n-- final positions, arc A (x / z): P -> P+delta* -> P_repaired, and _ro' --")
for i in range(10, 17):
    print(f"  ring {i:2d}: ({P[i,0]:+.4f},{P[i,2]:+.4f}) -> "
          f"({(P+delta)[i,0]:+.4f},{(P+delta)[i,2]:+.4f}) -> "
          f"({P2[i,0]:+.4f},{P2[i,2]:+.4f})   ro'=({ro2[i,0]:+.6f},{ro2[i,2]:+.6f})")

# ---- frames 2-3 -------------------------------------------------------------------
print("\n-- frames 2-3 (drain continuation) --")
P_cur, ro_cur = P2, ro2
for fr in (2, 3):
    a, nd, nc, n2p, s2 = apply_caps(ro_cur)
    Cf, Tf = build_C(P_cur)
    d, _, _ = project(Cf, a.reshape(-1))
    d = d.reshape(N, 3)
    dLf, _, _ = dL_of(d, Tf)
    Pf = P_cur + d
    ro_cur = ro_cur - d
    Pf, dispf, _ = repair(Pf)
    P_cur = Pf
    rn = (np.linalg.norm(ro_cur[9:18], axis=1).max(),
          np.linalg.norm(ro_cur[58:69], axis=1).max())
    print(f"  frame {fr}: ||a|| = {np.linalg.norm(a):.6f}  max dL = {dLf.max():.6f}  "
          f"max|rep| = {np.linalg.norm(dispf, axis=1).max():.6f}  "
          f"residual max arcA/arcB = {rn[0]:.6f} / {rn[1]:.6f}")
    if fr == 3:
        print("  arc-A residual detail after frame 3 (rings 10..16, z-component):")
        print("   " + " ".join(f"{i}:{ro_cur[i,2]:+.6f}" for i in range(10, 17)))
        print(f"  sum_z arc-A residual = {ro_cur[9:18, 2].sum():+.8f} "
              f"(near-zero-sum gradient -> L1 stall mode)")

# ===========================================================================
print()
print("=" * 78)
print("D. Amendment v1.9 C1: rope-repair displacement bound (Th. P1 / Th. V1)")
print("=" * 78)
e_dom = np.sqrt(SEG**2 + D_CAP**2) - SEG
print(f"\n  per-segment domain bound sqrt(SEG^2+d_cap^2)-SEG = {e_dom:.7f}"
      f"   (T6a wire 0.0021)")
print(f"  cap-5 budget LAMBDA = {LAMBDA} = 2 x 0.0021;"
      f"  2 x dL(d_cap) = {2 * e_dom:.6f} <= LAMBDA  "
      f"(<=2 full-d_cap segments never engage cap 5)")

def sum_scale(wperp):
    """C1 cap 5: largest s in [0,1] with sum_k dL(s*w_k) <= LAMBDA.
    total(s) is continuous, strictly increasing where any w_k != 0, and
    total(0) = 0, so the root is unique; 80 fixed bisection steps are
    deterministic (interval width < 1e-24)."""
    def total(s):
        q = s * wperp
        return np.sum(np.sqrt(SEG * SEG + q * q) - SEG)
    if total(1.0) <= LAMBDA:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if total(mid) <= LAMBDA:
            lo = mid
        else:
            hi = mid
    return lo

def max_rep_disp(Pin):
    _, disp, _ = repair(Pin.copy())
    return np.linalg.norm(disp, axis=1).max()

# -- D1: collinear worst case (every transfer factor g_k = +1) --------------
print("\nD1  collinear chain, anti-correlated normal zigzag demand")
Ps = np.zeros((N, 3)); Ps[:, 0] = SEG * np.arange(N); Ps[:, 1] = 0.02
h = L2_CAP / np.sqrt(N)          # ||delta||_2 = 0.035 exactly (l2 boundary)
dlt = np.zeros((N, 3)); dlt[:, 2] = h * (-1.0) ** np.arange(N)
wp = np.linalg.norm(dlt[1:] - dlt[:-1], axis=1)
ein = np.sqrt(SEG**2 + wp**2) - SEG
print(f"  admissible under v1.8 caps 1-4: |delta_i| = {h:.6f} <= a_cap 0.020;"
      f"  ||delta||_2 = {np.linalg.norm(dlt):.6f} <= l2 0.035;")
print(f"  |w_perp| = {wp.max():.6f} <= d_cap {D_CAP};  |w_par| = 0")
print(f"  e_input per segment = {ein.max():.7f}   SUM over 79 = {ein.sum():.7f}")
d_u = max_rep_disp(Ps + dlt)
print(f"  UNCAPPED pass: max ring displacement = {d_u:.6f}")
if d_u > 0.0045:
    print("  -> v1.8 T6b-ii '0.0045' presented as a universal bound is REFUTED")
    print("     on v1.8's own input domain (it was empirical, worked-example-only)")
s1 = sum_scale(wp)
ein1 = np.sqrt(SEG**2 + (s1 * wp)**2) - SEG
d_c = max_rep_disp(Ps + dlt * s1)
print(f"  with cap 5: s* = {s1:.6f}   sum e = {ein1.sum():.7f} <= {LAMBDA}")
print(f"  capped pass: max ring displacement = {d_c:.9f}   "
      f"{'<= LAMBDA + 1e-9  PASS (Th. V1)' if d_c <= LAMBDA + 1e-9 else 'FAIL'}")

# -- D2: hairpin extremes ---------------------------------------------------
print("\nD2  hairpin extremes (same demand field as D1)")
th2 = np.array([0.0 if k % 2 == 0 else np.pi for k in range(M)])
Ph = np.zeros((N, 3)); Ph[:, 1] = 0.02
for k in range(M):
    Ph[k + 1] = Ph[k] + SEG * np.array([np.cos(th2[k]), 0.0, np.sin(th2[k])])
T2 = (Ph[1:] - Ph[:-1]) / SEG
gmin = min(T2[k] @ T2[k + 1] for k in range(M - 1))
d2u = max_rep_disp(Ph + dlt); d2c = max_rep_disp(Ph + dlt * s1)
print(f"  anti-aligned ladder: min g_k = t_k.t_(k+1) = {gmin:+.6f}")
print(f"  UNCAPPED: {d2u:.6f}  (g = -1: transfers cancel -> benign)")
print(f"  capped:   {d2c:.9f}   "
      f"{'PASS' if d2c <= LAMBDA + 1e-9 else 'FAIL'}")
th3 = np.full(M, np.deg2rad(2.0)); th3[30] = np.deg2rad(175.0)
Pf = np.zeros((N, 3)); Pf[:, 1] = 0.02
for k in range(M):
    Pf[k + 1] = Pf[k] + SEG * np.array([np.cos(th3[k]), 0.0, np.sin(th3[k])])
d3u = max_rep_disp(Pf + dlt); d3c = max_rep_disp(Pf + dlt * s1)
print(f"  single 175-deg fold at segment 30: UNCAPPED {d3u:.6f}   "
      f"capped {d3c:.9f}  {'PASS' if d3c <= LAMBDA + 1e-9 else 'FAIL'}")

# -- D3: randomized suite through the real projection -----------------------
print("\nD3  randomized suite: 300 configs x real projection + caps + repair")
rng = np.random.default_rng(42)
worst = 0.0; engaged = 0; max_post = 0.0; max_sum = 0.0; max_wpar = 0.0
for t in range(300):
    thw = rng.normal(0.0, 0.9, M)
    if t % 3 == 0:  # inject a sharp fold (hairpin-family configurations)
        thw[rng.integers(5, M - 5)] += rng.choice([-1.0, 1.0]) * rng.uniform(2.6, 3.0)
    Pr = np.zeros((N, 3)); Pr[:, 1] = 0.02
    for k in range(M):
        Pr[k + 1] = Pr[k] + SEG * np.array([np.cos(thw[k]), 0.0, np.sin(thw[k])])
    a = np.zeros((N, 3))
    for m in (1, 2, 3):
        amp = rng.uniform(0.002, 0.010); ph = rng.uniform(0, 2 * np.pi)
        a[:, 0] += amp * np.sin(2 * np.pi * m * np.arange(N) / N + ph)
        a[:, 2] += amp * np.cos(2 * np.pi * m * np.arange(N) / N + ph)
    na = np.linalg.norm(a, axis=1)                      # cap 1: drain
    a *= np.minimum(1.0, kabs_dt / np.maximum(na, 1e-12))[:, None]
    na = np.linalg.norm(a, axis=1)                      # cap 2: a_cap
    a[na > A_CAP] *= (A_CAP / na[na > A_CAP])[:, None]
    n2 = np.linalg.norm(a)                              # cap 3: l2
    if n2 > L2_CAP:
        a *= L2_CAP / n2
    C, T = build_C(Pr)                                  # global projection
    d, _, _ = project(C, a.reshape(-1)); d = d.reshape(N, 3)
    wv = d[1:] - d[:-1]
    dot = np.einsum('ij,ij->i', wv, T)
    wper = np.linalg.norm(wv - dot[:, None] * T, axis=1)
    max_wpar = max(max_wpar, np.abs(dot).max())
    s = sum_scale(wper)                                 # cap 5 (v1.9 C1)
    if s < 1.0 - 1e-12:
        engaged += 1
    d = d * s
    dL = np.sqrt((SEG + np.abs(dot) * s) ** 2 + (wper * s) ** 2) - SEG
    max_sum = max(max_sum, dL.sum())
    Pr_rep, disp, _ = repair(Pr + d)                    # Stage-8 pass
    worst = max(worst, np.linalg.norm(disp, axis=1).max())
    Lp = np.linalg.norm(Pr_rep[1:] - Pr_rep[:-1], axis=1)
    max_post = max(max_post, np.abs(Lp - SEG).max())
print(f"  cap-5 engaged in {engaged}/300 runs;  max |w_par| = {max_wpar:.2e}")
print(f"  max sum|e_input|  = {max_sum:.7f}   "
      f"{'<= LAMBDA + 1e-9  OK' if max_sum <= LAMBDA + 1e-9 else 'VIOLATION'}")
print(f"  max ring displacement = {worst:.9f}   "
      f"{'<= LAMBDA + 1e-9  PASS (Th. V1)' if worst <= LAMBDA + 1e-9 else 'FAIL'}")
print(f"  max post-repair |len - SEG| = {max_post:.2e}   (in-frame exactness)")

# -- D4: Stage-5 R-FINAL rule checker (synthetic series; rule logic only) ---
print("\nD4  Stage-5 R-FINAL checker (synthetic pi/drain series; rule logic)")
def rfinal(pi, drained, spike_end):
    """R-FINAL: render in FAULT band iff ALL clauses hold.
    (a) non-growing: pi[n] <= pi[n-1] + 0.0005
    (b) drainage:    >= 50% of the k_abs*dt schedule drained since onset
        (synthetic input: drained[n] = drained fraction, 0.025 u/frame sched.)
    (c) budget:      <= 12 rendered fault frames per rolling 600
        (series < 600 frames -> total count; noted simplification)
    (d) deadline:    pi < 0.005 by frame spike_end+30 (0.5 s at 60 fps);
        revocation from the FIRST frame n >= spike_end+30 whose candidate has
        pi >= 0.005 - the horizon frame itself is not displayed (v1.10 C4
        fix: no extra fault frame; rule and checker agree exactly)."""
    acts = []; ff = 0; revoked = False
    v = dict(a=True, b=True, c=True, d=True)
    for n in range(len(pi)):
        p = pi[n]
        if p <= 0.005:
            acts.append("PASS"); continue
        if p > 0.02:
            acts.append("R3/R4"); continue
        ok = True
        if n > 0 and p > pi[n - 1] + 0.0005:
            ok = False; v['a'] = False
        if drained[n] < 0.5:
            ok = False; v['b'] = False
        if n >= spike_end + 30:
            ok = False; v['d'] = False; revoked = True
        if revoked:
            ok = False
        if ff + 1 > 12:
            ok = False; v['c'] = False
        if ok:
            ff += 1; acts.append("FAULT-RENDER")
        else:
            acts.append("R3/R4")
    return v, acts

pi1 = np.concatenate([np.linspace(0.012, 0.0055, 12), np.full(23, 0.004)])
v, acts = rfinal(pi1, np.linspace(0.6, 1.0, 35), 2)
print(f"  S1 fast recovery (12 band frames, clean by frame 12 < 32): "
      f"a/b/c/d all hold = {all(v.values())}; "
      f"actions: {acts.count('FAULT-RENDER')}x FAULT-RENDER -> PASS")
pi2 = np.full(50, 0.008)
v, acts = rfinal(pi2, np.full(50, 0.8), 5)
n45 = acts.count("R3/R4")
print(f"  S2 stall at pi = 0.008: (c) fired = {not v['c']} (13th band frame); "
      f"(d) fired = {not v['d']} (frame {5 + 30} = spike_end + 30, horizon "
      f"frame not displayed);")
print(f"      R3/R4 frames = {n45}; band rendering revoked until clean recovery")
pi3 = np.concatenate([0.006 + 0.0004 * np.arange(6), np.full(8, 0.0050),
                      0.0055 + 0.0004 * np.arange(12), np.full(5, 0.0050)])
v, acts = rfinal(pi3, np.full(len(pi3), 0.8), 0)
print(f"  S3 intermittent re-entry: (c) fired = {not v['c']} "
      f"(18 band frames > 12 budget); (a)/(b)/(d) held = "
      f"{v['a']}/{v['b']}/{v['d']}")

# ===========================================================================
print()
print("=" * 78)
print("E. Amendment v1.10 C4: pairwise clearance loss (Th. V2 / Th. V3)")
print("=" * 78)
PAIR = 2 * LAMBDA
print(f"\n  Th. V2 (any ring pair i,j): |D'_ij - D_ij| <= ||d_j - d_i||"
      f" <= 2*LAMBDA = {PAIR:.4f}")
print(f"  Th. V3 (capsule vs STATIC obstacle): |dd| <= max endpoint motion"
      f" <= LAMBDA = {LAMBDA:.4f}")

def pair_deltas(Pa, Pb):
    """max |D'_ij - D_ij| over all pairs and over self-collision |i-j| >= 9."""
    D0 = np.linalg.norm(Pa[:, None, :] - Pa[None, :, :], axis=-1)
    D1 = np.linalg.norm(Pb[:, None, :] - Pb[None, :, :], axis=-1)
    dD = np.abs(D1 - D0)
    return dD[np.triu_indices(N, k=1)].max(), dD[np.triu_indices(N, k=9)].max()

# -- E1: pairwise sweep, 300 fresh randomized configs (seed 43) --------------
print("\nE1  pairwise separation-change sweep (300 randomized configs)")
rng = np.random.default_rng(43)
w_all = w_far = w_disp = 0.0
for t in range(300):
    thw = rng.normal(0.0, 0.9, M)
    if t % 3 == 0:
        thw[rng.integers(5, M - 5)] += rng.choice([-1.0, 1.0]) * rng.uniform(2.6, 3.0)
    Pr = np.zeros((N, 3)); Pr[:, 1] = 0.02
    for k in range(M):
        Pr[k + 1] = Pr[k] + SEG * np.array([np.cos(thw[k]), 0.0, np.sin(thw[k])])
    a = np.zeros((N, 3))
    for m in (1, 2, 3):
        amp = rng.uniform(0.002, 0.010); ph = rng.uniform(0, 2 * np.pi)
        a[:, 0] += amp * np.sin(2 * np.pi * m * np.arange(N) / N + ph)
        a[:, 2] += amp * np.cos(2 * np.pi * m * np.arange(N) / N + ph)
    na = np.linalg.norm(a, axis=1)
    a *= np.minimum(1.0, kabs_dt / np.maximum(na, 1e-12))[:, None]
    na = np.linalg.norm(a, axis=1)
    a[na > A_CAP] *= (A_CAP / na[na > A_CAP])[:, None]
    n2 = np.linalg.norm(a)
    if n2 > L2_CAP:
        a *= L2_CAP / n2
    C, T = build_C(Pr)
    d, _, _ = project(C, a.reshape(-1)); d = d.reshape(N, 3)
    wv = d[1:] - d[:-1]
    dot = np.einsum('ij,ij->i', wv, T)
    d *= sum_scale(np.linalg.norm(wv - dot[:, None] * T, axis=1))
    Pr_rep, disp, _ = repair(Pr + d)
    ma, mf = pair_deltas(Pr + d, Pr_rep)
    w_all = max(w_all, ma); w_far = max(w_far, mf)
    w_disp = max(w_disp, np.linalg.norm(disp, axis=1).max())
print(f"  max ring displacement     = {w_disp:.9f}   "
      f"{'<= LAMBDA   PASS (Th. V1)' if w_disp <= LAMBDA + 1e-9 else 'FAIL'}")
print(f"  max |dD| ALL pairs        = {w_all:.9f}   "
      f"{'<= 2*LAMBDA PASS (Th. V2)' if w_all <= PAIR + 1e-9 else 'FAIL'}")
print(f"  max |dD| |i-j| >= 9 pairs = {w_far:.9f}   "
      f"{'<= 2*LAMBDA PASS (Th. V2)' if w_far <= PAIR + 1e-9 else 'FAIL'}")

# -- E2: adversarial constructions (tightness of Th. V2) ---------------------
print("\nE2  adversarial constructions: cap-boundary stretch field + U-turn")

def uturn_case(prof, leg, n_arc):
    """prof: z-offsets on rings 0..len(prof)-1 (the stretch mass; their
    sagitta = the pass-start length errors); then `leg` straight +x segments
    (exact SEG); then n_arc segments turning pi uniformly (exact SEG); then
    straight -x to the tail.  Returns (P0, offsets, first-stretched count)."""
    s0 = len(prof) - 1
    th = np.zeros(M)
    for k in range(s0 + leg, min(s0 + leg + n_arc, M)):
        th[k] = (k - s0 - leg + 1) * (np.pi / n_arc)
    for k in range(s0 + leg + n_arc, M):
        th[k] = np.pi
    P0 = np.zeros((N, 3)); P0[:, 1] = 0.02
    for k in range(M):
        P0[k + 1] = P0[k] + SEG * np.array([np.cos(th[k]), 0.0, np.sin(th[k])])
    dlt = np.zeros((N, 3)); dlt[:len(prof), 2] = prof
    return P0, dlt, s0

def in_domain(P0, dlt):
    """Check the constructed state against the full cap domain (1-5);
    returns (ok, failed-clause names)."""
    X = P0 + dlt
    e = np.linalg.norm(X[1:] - X[:-1], axis=1) - SEG
    w = np.linalg.norm(dlt[1:] - dlt[:-1], axis=1)
    checks = (
        ("per-segment |e| > dL_max", np.abs(e).max() <= np.sqrt(SEG**2 + D_CAP**2) - SEG + 1e-12),
        ("sum|e| > LAMBDA", np.abs(e).sum() <= LAMBDA + 1e-12),
        ("|w| > d_cap", w.max() <= D_CAP + 1e-12),
        ("|offset| > a_cap", np.abs(dlt).max() <= A_CAP + 1e-12),
        ("||offsets||_2 > l2", np.linalg.norm(dlt) <= L2_CAP + 1e-12))
    bad = [nm for nm, okc in checks if not okc]
    return (not bad), bad

best = 0.0
for name, prof0, leg, n_arc in (
        ("anti-parallel demo: sawtooth + U76 (chord perp)",
         np.array([0.0, 0.02, 0.0]), 0, 76),
        ("chord-aligned:     zigzag-4 + leg 51 + U20",
         np.array([0.0, 0.01, -0.01, 0.01, 0.0]), 51, 20),
        ("chord-aligned:     ramp-teeth + leg 45 + U20",
         np.array([0.0, .005, .01, .015, .02, 0.0, .005, .01, .015, .02, 0.0]),
         45, 20)):
    prof = prof0 * sum_scale(np.abs(np.diff(prof0)))   # cap-5 scaling
    P0, dlt, s0 = uturn_case(prof, leg, n_arc)
    X0 = P0 + dlt
    e_in = np.linalg.norm(X0[1:] - X0[:-1], axis=1) - SEG
    ok_dom, why = in_domain(P0, dlt)
    if not ok_dom:
        print(f"  {name}: NOT in-domain (violates: {'; '.join(why)})")
        continue
    Pr_rep, disp, _ = repair(X0)
    j = M - 2                                      # ring on the return leg
    di = np.linalg.norm(disp[s0]); dj = np.linalg.norm(disp[j])
    cosd = disp[s0] @ disp[j] / max(di * dj, 1e-30)
    D0 = np.linalg.norm(X0[j] - X0[s0])
    D1 = np.linalg.norm(Pr_rep[j] - Pr_rep[s0])
    ma, mf = pair_deltas(X0, Pr_rep)
    print(f"  {name}:")
    print(f"    sum|e| = {np.abs(e_in).sum():.6f} <= LAMBDA;  |d_i| = {di:.6f} "
          f"(ring {s0}),  |d_j| = {dj:.6f} (ring {j}),  cos(d_i,d_j) = {cosd:+.4f}")
    print(f"    pair ({s0},{j}) separation change = {abs(D1 - D0):.6f} = "
          f"{abs(D1 - D0)/LAMBDA:.3f} x LAMBDA")
    print(f"    max |dD| all pairs = {ma:.6f} = {ma/LAMBDA:.3f} x LAMBDA   "
          f"{'<= 2*LAMBDA  PASS (Th. V2)' if ma <= PAIR + 1e-9 else 'FAIL'}")
    best = max(best, ma)
print(f"  constructive lower bound of the pairwise supremum: {best:.6f} "
      f"= {best/LAMBDA:.3f} x LAMBDA;")
print(f"  proven supremum (Th. V2) = 2*LAMBDA = {PAIR:.4f}; design bound adopted:"
      f" 2*LAMBDA")

# -- E3: continuous capsule geometry -----------------------------------------
print("\nE3  capsule-level checks (segment-segment distance, not ring centers)")
for tag, prof0, leg, n_arc in (
        ("chord-aligned case", np.array([0.0, 0.01, -0.01, 0.01, 0.0]), 51, 20),
        ("anti-parallel case", np.array([0.0, 0.02, 0.0]), 0, 76)):
    prof = prof0 * sum_scale(np.abs(np.diff(prof0)))
    P0, dlt, s0 = uturn_case(prof, leg, n_arc)
    X0 = P0 + dlt
    Pr_rep, disp, _ = repair(X0)
    j = M - 2
    A0 = (X0[s0, [0, 2]], X0[s0 + 1, [0, 2]])
    A1 = (Pr_rep[s0, [0, 2]], Pr_rep[s0 + 1, [0, 2]])
    B0 = (X0[j, [0, 2]], X0[j + 1, [0, 2]])
    B1 = (Pr_rep[j, [0, 2]], Pr_rep[j + 1, [0, 2]])
    ds0 = seg_seg_dist_2d(A0[0], A0[1], B0[0], B0[1])
    ds1 = seg_seg_dist_2d(A1[0], A1[1], B1[0], B1[1])
    print(f"  {tag}: self-pair capsules ({s0},{s0+1}) vs ({j},{j+1}): "
          f"{ds0:.6f} -> {ds1:.6f}   |dd| = {abs(ds1 - ds0):.6f}   "
          f"{'<= 2*LAMBDA  PASS (Th. V2)' if abs(ds1 - ds0) <= PAIR + 1e-9 else 'FAIL'}")
    xw = X0[j, 0] + 0.04
    wall = (np.array([xw, X0[j, 2] - 0.15]), np.array([xw, X0[j, 2] + 0.15]))
    dw0 = seg_seg_dist_2d(B0[0], B0[1], wall[0], wall[1])
    dw1 = seg_seg_dist_2d(B1[0], B1[1], wall[0], wall[1])
    print(f"  {tag}: STATIC-wall clearance, capsule ({j},{j+1}): "
          f"{dw0:.6f} -> {dw1:.6f}   |dd| = {abs(dw1 - dw0):.6f}   "
          f"{'<= LAMBDA  PASS (Th. V3)' if abs(dw1 - dw0) <= LAMBDA + 1e-9 else 'FAIL'}")

# -- E4: adjacent-pair identity (exact repair) --------------------------------
print("\nE4  adjacent-pair identity (exact repair)")
X0 = P0 + dlt
e_in = np.linalg.norm(X0[1:] - X0[:-1], axis=1) - SEG
d_adj = np.abs(np.linalg.norm(Pr_rep[1:] - Pr_rep[:-1], axis=1)
               - np.linalg.norm(X0[1:] - X0[:-1], axis=1))
print(f"  max |dD_adjacent - |e_k|| = {np.abs(d_adj - np.abs(e_in)).max():.2e}"
      f"   (identity |dD| = |e_k| exact to fp)")
print(f"  max adjacent |dD| = {d_adj.max():.6f} <= 0.0021 (T6a domain): "
      f"{'PASS' if d_adj.max() <= 0.0021 + 1e-12 else 'FAIL'}")

print("\nDONE")
```

## Claim classification (C4 addendum to the v1.9 ledger)

| # | Claim | Class | Where / reliance |
|---|---|---|---|
| 22 | **Theorem V2**: \|ΔD_ij\| ≤ ‖δ_j − δ_i‖ ≤ 2Λ = 0.0084 u for every ring pair, every configuration, adversarial directions included | **Proven** (exact: reverse triangle + Th. V1) + **Verified** (E1: max 0.000182 over 3160 pairs × 300 configs; E2/E3 adversarial 0.006718 / 0.006693 ≤ 0.0084) | v1.10 §C4.1; script E |
| 23 | **Theorem V3**: capsule-vs-static-obstacle distance change ≤ Λ = 0.0042 u (continuous capsules, convexity + Hausdorff, no same-direction assumption) | **Proven** (exact) + **Verified** (E3 walls: 0.003032 / 0.003473; C-section regressions 0.000000 / 0.000003) | v1.10 §C4.3 |
| 24 | **R1**: adjacent-pair identity \|ΔD\| = \|e_k⁰\| ≤ 0.0021 (exact repair) | **Proven** (identity) + **Verified** (E4: deviation 1.7e−16; max 0.001980) | v1.10 §C4.1 |
| 25 | **R2**: co-directed straight intervals telescope: \|ΔD\| = \|Σ_{interval} e_k⁰\| ≤ Λ | **Proven** (exact, rotation of the collinear computation) | v1.10 §C4.1 |
| 26 | Transmission recursion δ_{k+1} = P_kδ_k − e_k⁰t̂_k; displacement rotates with the chain on gentle turns; gentle π-turns create anti-parallel near-maximal displacements | **Analytic tool (first-order)** — labeled as such; used only for tightness exploration, never for an adopted bound; supporting measurements: cos(δ_i,δ_j) = −0.9892 / −0.9966 (E2) | v1.10 §C4.3 |
| 27 | Pairwise separation-loss supremum | **UNRESOLVED within [1.599Λ measured, 2Λ proven]** — constructive lower bound 0.006718 (E2, cap-admissible, sum\|e\| = Λ exactly); no design decision depends on narrowing it: T6e uses the proven 2Λ | v1.10 §C4.2–C4.3 |
| 28 | T6e gate (self-collision per-frame regression ≤ 0.0084) holds on the tested domain | **Proven** (Th. V2 at capsule level) + **Verified** (E1/E3) | v1.10 §C4.4 |
| 29 | R-FINAL strict horizon: no fault frame displayed at or beyond spike_end + 30; rule = checker | **Proven** (rule logic) + **Verified** (D4 S1/S2/S3 with the fixed checker) | v1.10 §C4.6 |
| 30 | Adversarial self-pair one-frame penetration ≤ 0.0059 u < R1 0.02; handled by R-FINAL + next-frame self-healing | **Arithmetic from proven bounds** (0.0025 margin − 2Λ) ; the self-healing behavior itself remains **Verified** (v1.8 §4.2) / **Empirical** at scale | L4, v1.10 §C4.4 |

## Every affected threshold or test

| Item | Change |
|---|---|
| T6a (per-segment ΔL ≤ 0.0021) | unchanged |
| T6b-i (post-repair SEG ± 1e−5) | unchanged |
| T6b-ii (ring-displacement wire 0.0045 = proven Λ + 0.0003) | unchanged |
| T6c (min true obstacle clearance ≥ −0.0067) | value unchanged; justification upgraded (heuristic → Th. V3) |
| T6d (per-frame obstacle-clearance regression ≤ 0.005) | value unchanged; justification upgraded (heuristic → Th. V3) |
| **T6e (self-collision per-frame regression ≤ 2Λ = 0.0084)** | **NEW** |
| cap 5 (Λ = 0.0042), caps 1–4 | unchanged |
| π bands (0.005 / 0.02), R1–R5 | unchanged (measured quantities) |
| R-FINAL(d) | **AMENDED**: strict horizon — revocation from the first frame n ≥ spike_end + 30 with π ≥ 0.005; horizon frame not displayed; rule = checker |
| Script | D4 checker fixed; **E1–E4 added**; sections A–C byte-identical behavior (same seeds, same numbers) |

---

## Strict verdict

**v1.9 as written is NOT mathematically ready for Stage-1 approval.** Three gaps, all now closed:
(1) the pairwise clearance question was open — the audit's 0.0084 u ceiling is real for ring pairs
and was covered by no gate; (2) the T6c/T6d obstacle-echo justification was implicit rather than
proven (the values were correct — Theorem V3 now proves them, and shows why they did not need the
2Λ ceiling: obstacles are static); (3) the R-FINAL deadline checker permitted exactly one extra
fault frame at the horizon.

**v1.8 + C1–C4 (this v1.10) IS mathematically ready for Stage-1 approval**, conditional only on
your explicit acceptance of the two binding deltas introduced here — **T6e** (self-collision
per-frame clearance regression ≤ 2Λ = 0.0084 u) and the **strict R-FINAL horizon** — together with
the recorded limitation **L4** (adversarial one-frame self-pair penetration ≤ 0.0059 u, handled by
the measured-π fault band and next-frame self-healing). The safety-relevant structure is now fully
proven end-to-end: caps 1–5 → Theorem V1 (ring ≤ 0.0042) → Theorem V2 (ring-pair ≤ 0.0084) /
Theorem V3 (obstacle ≤ 0.0042) → T6c/T6d/T6e → Stage-5 measured-π gate. Every remaining
numerical/empirical item is labeled as such with its harness gate; none is load-bearing for
collision safety. No product code has been touched at any point; Anaconda v4.2 remains the sole
base; all existing functionality is preserved.

---

## Change log vs v1.9

- **Proven and added:** Theorem V2 (pairwise separation ceiling 2Λ, all pairs, exact); Theorem V3
  (capsule-vs-static-obstacle ≤ Λ, continuous geometry, convexity + Hausdorff); Refinements R1
  (adjacent identity) and R2 (straight-interval telescoping); transmission analysis (first-order,
  labeled analytic tool).
- **Added:** harness gate **T6e** (self-collision per-frame regression ≤ 0.0084 u); limitation
  **L4**; rejected-alternative record (Λ → 0.0025).
- **Fixed:** R-FINAL(d) horizon — `n > spike_end + 30` → `n ≥ spike_end + 30` in both the rule
  text and the checker (no extra fault frame; D4 re-verified).
- **Unchanged:** caps 1–5 and all constants; the repair pass algorithm; T6a/T6b/T6c/T6d values;
  π bands; R1–R5 (other than (d)); L1–L3; T1–T7; the global projection and all v1.8/v1.9 proofs.
- **Script:** section E added (E1 pairwise sweep, E2 adversarial constructions with named-cap
  domain checking, E3 continuous capsule geometry, E4 adjacent identity); D4 updated to the strict
  horizon; sections A–C behaviorally identical (same seeds and outputs).
