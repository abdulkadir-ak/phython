# Amendment v1.9 — Audit Response: Proven Rope-Repair Displacement Bound (C1), Unified Stage-5 Rule R-FINAL (C2), Verification Source and Claim Ledger (C3)

Base: Anaconda v4.2 only (`anaconda-wordpress-snippet-v4.2 (6).html`, 2,644 lines).
Status: design-only. No code changes, no implementation, all existing v4.2 functionality preserved.
Language: English.

All three audit demands are accepted without reservation. One of them exposes a genuine error in
v1.8; it is corrected here, not argued. Every number below was produced by the attached verification
script `v18_example.py` (numpy float64, 554 lines, sections A–D; complete source in §C3 and attached
as a separate file). The script is verification-only tooling; the Anaconda snippet itself is untouched.

---

## C1 — Rope-repair cumulative displacement: derivation, admission, corrected bound

### C1.1 The pass, formalized

Stage 8 processes segments k = 0…78 in fixed order, head to tail (identical in structure to the
native v4.2 follow-chain at L1505–1517, which anchors the head and drags rings 1…79 to exact
SEG = 0.1 u; in the design the pass runs on the post-absorption P):

    for k = 0 … 78:
        v_k ← Q[k+1] − Q[k]                     (current positions)
        L_k ← ‖v_k‖
        Q[k+1] ← Q[k] + SEG · v_k / L_k         (ring k+1 moves onto the SEG-sphere around ring k)

Definitions:

- `e_k⁰` = L_k(measured at pass start) − SEG — segment k's length error at pass start;
- `δ_{k+1}` = displacement of ring k+1 = `SEG·v̂_k − v_k`, hence **‖δ_{k+1}‖ = |L_k − SEG| = |e_k^cur|**
  exactly, because the move is along the current segment axis;
- ring 0 is never written (head-anchored, locomotion-owned — same contract as the native chain);
  ring k+1 is written only at step k. **Each ring moves at most once per pass.** There is no
  revisiting and therefore no accumulation by re-writing within a pass.

### C1.2 Audit question 1 — can a correction to one segment propagate? YES (Lemma P1, exact)

At step k, ring k has already been moved (by step k−1) by δ_k, and ring k+1 has not yet moved.
Segment k's current vector is therefore `v_k⁰ − δ_k`, where `v_k⁰` is its pass-start vector. Then

    |e_k^cur| = |‖v_k⁰ − δ_k‖ − SEG|
              ≤ |‖v_k⁰‖ − SEG| + ‖δ_k‖          (reverse triangle inequality — exact, no linearization)
              = |e_k⁰| + ‖δ_k‖ .

Since ‖δ_{k+1}‖ = |e_k^cur| and ‖δ_1‖ = |e_0⁰| (ring 0 unmoved), unrolling over the pass gives:

**Lemma P1 (propagation).** ‖δ_j‖ ≤ Σ_{k=0}^{j−1} |e_k⁰| for every ring j = 1…79.

So yes — repairing segment k−1 hands part or all of its displacement to segment k. In first-order
terms the transfer factor is `g_k = t̂_k · t̂_{k+1} ∈ [−1, 1]` (Cauchy–Schwarz): `g = +1` (collinear)
accumulates in full — the "slinky"; `g = −1` (hairpin fold) flips the sign and **cancels**;
`|g| < 1` attenuates. Equality in P1 holds exactly in the collinear stretched chain, so the
**collinear chain, not the hairpin, is the worst case** — measured in §C3 D2: on the same demand
field, the exact anti-aligned ladder (g = −1.000000) displaces its worst ring 0.000306 u uncapped,
while the collinear chain displaces its worst ring 0.017449 u.

### C1.3 Audit questions 2 & 3 — maximum displacement after all 79 segments; does 0.0045 hold for every configuration, including a hairpin?

**Theorem V1 (displacement bound).** If the pass input satisfies `Σ_{k=0}^{78} |e_k⁰| ≤ Λ`, then
every ring displacement in the pass satisfies `‖δ_j‖ ≤ Λ`, j = 1…79 — for **every** chain
configuration whatsoever. The proof (Lemma P1 + hypothesis) never references tangent directions;
hairpins, near-anti folds, and every other configuration are included by construction.

**Admission, as the audit demands.** v1.8's T6b-ii derivation — "cumulative is the chained sum over
the local arc ≈ ΣΔL ≈ 2×ΔL_max + margin" — was **empirical**: it silently assumed the nonzero-error
arc spans ≈ 2 segments. That is a property of the worked example, not of the input domain, and
presented as a universal bound it is **false**. The script demonstrates the refutation on v1.8's own
cap domain (§C3, test D1): a demand field admissible under all four v1.8 caps
(|a_i| = 0.003913 ≤ a_cap 0.020; ‖a‖₂ = 0.035000 = ℓ₂ boundary; |w⊥| = 0.007826 ≤ d_cap 0.020;
w∥ = 0) drives the uncapped pass to a ring displacement of **0.017449 u ≈ 3.9× the claimed 0.0045**.
Cap-chain arithmetic fixes the exact in-domain worst case, every step an exact inequality:

    Σ_k ΔL_k = Σ_k q_k²/(√(SEG²+q_k²)+SEG) ≤ Σ_k q_k²/(2·SEG) ≤ ‖w‖₂²/(2·SEG) ≤ 2‖a‖₂²/SEG
             = 2·0.035²/0.1 = 0.0245 u ,

(sagitta bound; ‖w‖₂ ≤ 2‖a‖₂ by the triangle inequality on the difference operator), i.e. the
uncapped echo could reach **5.4× the claimed bound**. The "0.0045 u" figure is hereby **labeled
EMPIRICAL and RETIRED as a guarantee**. What replaces it is a proven bound, obtained by making the
hypothesis of Theorem V1 true by construction.

### C1.4 Design correction C1 — cap 5 (the change that makes the bound a theorem)

**Cap 5 (new, appended after v1.8 §2.3 caps 1–4).** The absorption output must satisfy the
**total-sagitta budget** `Σ_k ΔL_k(δ*) ≤ Λ = 0.0042 u` per frame. Enforcement: deterministic
bisection on a single scaling factor s ∈ [0, 1] of the final admissible field — `total(s) =
Σ_k ΔL_k(s·δ*)` is continuous and strictly increasing wherever any differential is nonzero, with
total(0) = 0, so the root is unique; 80 fixed bisection iterations (interval width < 1e−24);
deterministic. Scaling commutes with the projection and with the differential-cap alternating
projection (both homogeneous), so the cap chain stays well-defined: drain → a_cap → ℓ₂ →
differential cap → cap 5. The unabsorbed remainder stays in _ro (absorbed + retained = demand
accounting unchanged).

**The repair pass itself stays exact (uncapped per segment).** Capping the pass would leave
residual length error in P (violating T6b-i, SEG ± 1e−5) and would merely defer the displacement
into the next frame's native Stage-3 renormalization — the error mass must go somewhere; the sound
place to bound it is the input sum. With cap 5 in place:

- **Proven (Th. V1):** max ring displacement per frame ≤ **0.0042 u**, every configuration,
  hairpins included;
- T6b-i is untouched: the pass still sets every segment to SEG exactly (fp rounding only; measured
  3.7e−16 in the worked example, 4.9e−16 over 300 randomized runs);
- the next frame's native Stage-3 pass is a length no-op (P enters exact) — **there is no hidden
  next-frame displacement channel**; the entire displacement enters once, bounded by Λ;
- **Λ = 0.0042 is not arbitrary:** (i) 2·ΔL(d_cap) = 0.003961 ≤ Λ, so contact arcs of ≤ 2
  full-d_cap segments never engage the cap (the worked example's ΣΔL = 0.002519 — 40% headroom —
  does not engage it either, and in 300 randomized runs it engaged 0 times); (ii) the repair echo
  fits the existing T6c/T6d budgets with **no budget change** (§C1.5); (iii) the T6b-ii trip-wire
  stays at 0.0045 = proven bound + 0.0003 margin (the wire now guards against implementation bugs,
  not against mathematics).

**Explicit answers to the four sub-questions:**

1. *Can a correction to one segment propagate through subsequent segments?* **Yes** — Lemma P1,
   quantified: the transfer is bounded by the predecessor's displacement, with factor g_k ∈ [−1, 1]
   (accumulate / attenuate / cancel), and the total is bounded by the input sum.
2. *Maximum displacement of any ring after all 79 segments are repaired?*
   `sup_j ‖δ_j‖ ≤ Σ_{k=0}^{78} |e_k⁰| ≤ Λ = 0.0042 u` per frame (proven). The extremal ring is the
   tail in the collinear case; measured realization 0.003893 u (D1, capped).
3. *Does 0.0045 hold for every configuration, including a hairpin?* The v1.8 claim did **not**
   (refuted by D1: 0.017449 u uncapped on a cap-admissible input). After C1 the **proven** bound is
   0.0042 u for every configuration — including the exact anti-aligned ladder (g = −1.000000;
   capped 0.0000532 u; uncapped only 0.000306 u because hairpin transfers cancel) and the 175° fold
   (capped 0.004102 u). The worst case is the collinear chain, not the hairpin.
4. *Empirical or mathematical?* Before C1: empirical (and false as a universal claim). After C1:
   **proven** (Theorem V1), conditional on cap 5, which is enforced deterministically; the
   condition is part of the design, not of the test coverage.

### C1.5 Audit demand — worst-case collision-clearance loss, recalculated on the proven cumulative bound

The repair pass runs after rendering; it moves rings without compensating _ro, so its displacement
is available next frame as a **clearance regression** ("repair echo"). v1.8 sized that echo as
2×0.0021 = 0.0042 u — an empirical echo estimate. It is now the **proven** worst case:
`echo = max_j ‖δ_j‖ ≤ Λ = 0.0042 u`. Note the echo is **not** the local 0.0021 u: propagation
(Lemma P1) doubles it at worst; sizing on the local value alone would understate the loss by 2×.

- **T6d (per-frame clearance regression ≤ 0.005 u):** echo 0.0042 ≤ 0.005 → margin **0.0008 u**.
  Budget unchanged, now proven.
- **T6c (minimum true clearance ≥ −0.0067 u):** 0.0025 (measurement/sagitta-inflation margin)
  + 0.0042 (proven echo) = 0.0067. Budget unchanged, now proven.
- **Without cap 5 the budgets were unsound:** the in-domain uncapped echo reaches 0.0245 u
  (measured realization 0.017449 u) — 4.9× the T6d budget. Cap 5 is what makes T6c/T6d theorems
  rather than hopes.
- **Drain promise unchanged:** cap 5 limits what is moved into P per frame; it does not touch the
  _ro drain schedule (k_abs·dt = 0.025 u per ring per frame), so the 0.22 u / 0.025 = 8.8 frames
  ≈ 0.15 s arithmetic of v1.8 §4.3 stands, and the v1.5 0.5 s acceptance deadline is enforced
  structurally by R-FINAL(d) below, not by drain arithmetic.

---

## C2 — Audit demand 2 — Stage-5: one explicit final rule (R-FINAL)

**Admission.** v1.8 §3's clarification asserted "condition R2(b) converts any long-lived FAULT into
R3 → R4 within 0.5 s" but did **not** carry the v1.5 0.5-second recovery condition as an explicit
clause. That was an error of omission.

**Answer to the question posed: R2 does not replace the v1.5 rule — both apply.** They are unified
into **R-FINAL**, which supersedes v1.8's R2 and carries the v1.5 recovery condition verbatim in
meaning. Clauses (a)–(c) are v1.8's R2(a)–(c), unchanged; clause (d) is the v1.5 rule, made precise.

**R-FINAL (the complete Stage-5 fault-band rule).** Stage 5 measures π = maximum penetration over
all render capsule pairs and obstacles on the candidate state X. Bands: π ≤ 0.005 → PASS (render,
silent); 0.005 < π ≤ 0.02 → FAULT band, governed by R-FINAL; π > 0.02 → R1 hard gate (never display;
R3). In the FAULT band, rendering a new pose is permitted **if and only if all four clauses hold**:

- **(a) Non-growing:** π(n) ≤ π(n−1) + 0.0005 u.
- **(b) Drainage:** the responsible _ro region shows ≥ 50% of the k_abs·dt schedule (0.025 u per
  frame since fault onset) drained cumulatively.
- **(c) Budget:** ≤ 12 rendered fault frames per rolling 600 frames (2%).
- **(d) Deadline (v1.5, retained):** a *demand spike* for window W is any frame with
  ‖a_W‖ ≥ 0.010 u; the spike *has ended* at the first frame following 5 consecutive frames with
  ‖a_W‖ < 0.010 u. Within 30 frames (0.5 s at 60 fps) of spike end, π must fall below 0.005 u.
  If it does not, band rendering is revoked from that frame onward **until a candidate passes R1
  with π ≤ 0.005 u (clean recovery)**, via R3 (single retry, step sizes ×0.5) then R4 (hold last
  safe frame) — the revocation is sticky and survives rolling-window budget resets.

Any clause failing → R3 → R4 → R5 (re-birth) exactly as v1.8 §3, unchanged. All quantities are
measured; all constants are fixed; there is no randomness and no undefined tie.

**Division of labor — why both the v1.8 clauses and the v1.5 deadline are needed.** Clause (c)
caps *cumulative exposure* (≤ 12 rendered band frames per 600); in a continuous stall it fires
first (12 frames ≈ 0.2 s < 0.5 s). Clause (d) is the *per-episode recovery contract*: it enforces
recovery regardless of the rolling count, and it closes the budget-reset re-entry hole — without
(d), a still-unrecovered fault could legally resume band rendering once the rolling 600-window
frees budget; (d)'s sticky revocation makes that impossible. Neither subsumes the other.
Demonstrated in §C3 test D4 on three synthetic series (rule logic, clearly labeled synthetic):
continuous stall → (c) fires at the 13th band frame, (d) fires at spike_end + 31, revocation
sticky; intermittent re-entry with (a)/(b)/(d) satisfied → (c) fires at the 13th band frame;
fast recovery → all four hold, 12 band frames rendered, PASS.

**Monotonicity clause (binding).** No later amendment may silently remove or weaken any R-FINAL
clause. Weakening requires a new acceptance rule that (i) quotes the removed clause verbatim,
(ii) proves the replacement dominates it clause-by-clause, and (iii) is separately approved.
Absent that, R-FINAL stands as written. This closes the audit's requirement that "no later
amendment silently removes an earlier safety requirement."

---
## C3 — Audit demand 3 — verification source and claim classification

**Complete source.** The complete source code of the verification script (554 lines, sections
A–D) is reproduced in full below and is attached as a separate file: **`v18_example.py`**
(verbatim copy of `scripts/v18_example.py`). Sections A–C are unchanged from the v1.8 baseline
except two annotated lines (the cap-5 check and the T6b trip-wire annotation); section D is new
in v1.9 and implements exactly the audits of C1/C2: the adversarial refutation (D1), the hairpin
extremes (D2), the randomized suite through the real projection path (D3), and the R-FINAL rule
checker (D4). The script is standalone numpy; it reads and modifies nothing in the product file.

**Fresh complete run output** (the exact stdout of the attached script):

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
  S2 stall at pi = 0.008: (c) fired = True (13th band frame); (d) fired = True (frame 36 = spike_end + 31 > 0.5 s);
      R3/R4 frames = 38; band rendering revoked until clean recovery
  S3 intermittent re-entry: (c) fired = True (18 band frames > 12 budget); (a)/(b)/(d) held = True/True/True

DONE

```

**Complete verification source** — `v18_example.py`, 554 lines, identical to the attached file `download/v18_example.py`:

```python
#!/usr/bin/env python3
"""
Amendment v1.8 + v1.9 (C1) verification for the Anaconda v4.2 design
(no product code touched).

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
        once missed, band rendering stays revoked until clean recovery."""
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
        if n > spike_end + 30:
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
      f"(d) fired = {not v['d']} (frame {5 + 31} = spike_end + 31 > 0.5 s);")
print(f"      R3/R4 frames = {n45}; band rendering revoked until clean recovery")
pi3 = np.concatenate([0.006 + 0.0004 * np.arange(6), np.full(8, 0.0050),
                      0.0055 + 0.0004 * np.arange(12), np.full(5, 0.0050)])
v, acts = rfinal(pi3, np.full(len(pi3), 0.8), 0)
print(f"  S3 intermittent re-entry: (c) fired = {not v['c']} "
      f"(18 band frames > 12 budget); (a)/(b)/(d) held = "
      f"{v['a']}/{v['b']}/{v['d']}")

print("\nDONE")
```

**Claim classification ledger.** Every load-bearing claim of v1.8 + v1.9, in the three categories
the audit demands. "Proven" = proof in amendment text, independent of test coverage. "Verified" =
numerically established by the attached script on the stated configurations. "Empirical" =
test-coverage-dependent; NOT presented as a universal guarantee; reliance and harness gate stated.

| # | Claim | Class | Where / reliance |
|---|---|---|---|
| 1 | Straight-chain projection = mean operator; a[13] = −0.020 ⇒ δ*[i].x = −0.00025 ∀i; Σδ* = Σa | **Proven** | v1.8 §1.2 (closed-form Gram inverse) |
| 2 | rank(C) = 79 for every configuration (no rank-deficient case exists) | **Proven** | v1.8 §1.3 (induction on rows) |
| 3 | κ(CCᵀ) ≤ 2594.2 for every configuration; straight chain worst | **Proven** | v1.8 §1.3 (reverse triangle + Dirichlet–Poincaré) |
| 4 | Anchored variant ⇒ null space {0} → rejected as vacuous for parallel absorption | **Proven** | v1.8 §1.4 |
| 5 | Rigid-component preservation Σa = Σδ* (translation never destroyed) | **Proven** | v1.8 §1.2 (𝟙 ∈ null(C)) |
| 6 | Exact combined length error ΔL = √((SEG+w∥)² + w⊥²) − SEG; strictly monotone in both inputs; no quadrature/linear combiner exists | **Proven** | v1.8 §2.1 (calculus) |
| 7 | Single-segment worst case ΔL_max = 0.0019805 u under caps 1–4 (T6a wire 0.0021) | **Proven** | v1.8 §2.3 (cap chain + #6) |
| 8 | Propagation Lemma P1: ‖δ_{k+1}‖ ≤ |e_k⁰| + ‖δ_k‖; transfer factor g ∈ [−1,1]; collinear = worst case, hairpin cancels | **Proven** | v1.9 §C1.2 (reverse triangle, geometry-free) |
| 9 | Displacement Theorem V1: max_j ‖δ_j‖ ≤ Σ_k |e_k⁰| ≤ Λ = 0.0042 u per frame, every configuration incl. hairpin, given cap 5 | **Proven** (conditional on cap 5, enforced by construction) | v1.9 §C1.3–C1.4 |
| 10 | Cap-5 bisection: total(s) strictly increasing ⇒ unique root; 80 fixed iterations, deterministic | **Proven** | v1.9 §C1.4 |
| 11 | In-frame exactness: post-pass ‖len − SEG‖ = fp rounding only (T6b-i, SEG ± 1e−5) | **Proven** (algorithm property) + **Verified** (3.7e−16 worked example; 4.9e−16 over 300 runs) | v1.9 §C1.4; script C/D |
| 12 | Next-frame Stage-3 no-op: no hidden next-frame displacement channel | **Proven** (from #11) | v1.9 §C1.4 |
| 13 | Differential-cap alternating projection converges (existence/convergence only; **rate is not proven**) | **Proven** (convergence) / **Empirical** (8-sweep rate, L2) | v1.8 §2.3 |
| 14 | Uncapped universal "0.0045" cumulative repair displacement | **RETIRED — was Empirical, false as universal** (refuted: 0.017449 u measured, 0.0245 u in-domain algebraic worst case) | v1.9 §C1.3; script D1 |
| 15 | Repaired system: capped max ring displacement ≤ 0.0042 u on collinear worst case / 175° fold / exact hairpin ladder / 300 randomized configs | **Verified** (0.003893 / 0.004102 / 0.0000532 / 0.000238) + **Proven** (Th. V1) | script D1–D3 |
| 16 | All sub-case-0 and worked-example numbers of v1.8 §1.2, §4 (rank 79, κ 1923.5, ‖Cδ*‖∞ 7.8e−19, ΔL 0.000636, ΣΔL 0.002519, retention 5.7%, render invariance 1.4e−17, repair identity dev 1.7e−18, cumulative 0.001042, clearances/regressions, frames 2–3, L1 residue) | **Verified** (script sections A–C, exact run output above) | v1.8 §4 |
| 17 | R-FINAL behavior: continuous stall → (c) at 13th band frame + (d) at spike_end+31, sticky revocation; intermittent re-entry → (c); fast recovery → all four hold | **Proven** (rule logic, deterministic given measurements) + **Verified** (D4 on synthetic series — rule logic only, no pipeline simulation) | v1.9 §C2; script D4 |
| 18 | Stage-4 K = 3 iteration count suffices for solvable-looking poses | **Empirical** (L3) — heuristic; NO safety claim rests on it: every display decision routes through the measured π gate R1–R5/R-FINAL | v1.8 §5 |
| 19 | L1 stall residue decays 2e−6/frame and drains under locomotion curvature (T7: ≤ 25% of peak within 2.0 s) | **Empirical** — bounded (≤ a_cap per event, ≤ 0.22 u overall), render-held, harness-gated T7 | v1.8 §1.5, §4.3 |
| 20 | Drain promise 0.15 s for representable residuals; 0.5 s acceptance deadline | Deadline is **rule-enforced** (R-FINAL(d), proven rule logic); the 0.15 s drain arithmetic is **cap-chain arithmetic** on tested configurations | v1.8 §4.3; v1.9 §C1.5, §C2 |
| 21 | Worked-example magnitudes (clearance values, per-ring fields, contact arcs) | **Empirical** — they exemplify the machinery on one configuration; they do not bound anything | v1.8 §4 |

---

## Strict verdict

**v1.8 as written is NOT ready for Stage-1 approval.** Three defects, all now corrected:

1. **C1 defect (the serious one):** the cumulative repair-displacement bound "0.0045 u" was an
   empirical worked-example observation presented with the force of a theorem. On v1.8's own input
   domain it is false — the script measures 0.017449 u on a field admissible under all four v1.8
   caps, and the in-domain algebraic worst case is 0.0245 u — which also means the T6c/T6d
   clearance budgets rested on an unsound footing.
2. **C2 defect:** the Stage-5 rule left the v1.5 0.5-second recovery condition in limbo — asserted
   as a consequence of R2(b) but never carried as a clause, so a later amendment could have
   silently dropped it.
3. **C3 defect:** the verification source was not attached and claims were not classified, leaving
   empirical results indistinguishable from guarantees.

**v1.8 + corrections C1–C3 (this v1.9) IS ready for Stage-1 approval**, conditional only on your
explicit acceptance of two binding design deltas — (i) **cap 5**, the absorption-side total-sagitta
budget Λ = 0.0042 u with deterministic bisection enforcement (design-side only; the repair pass
algorithm is unchanged; no product code touched), and (ii) **R-FINAL** with the strengthen-only
monotonicity clause. After these corrections, every safety-relevant number is either proven (proof
included above) or explicitly labeled empirical with its reliance and harness gate stated; no
empirical result is presented as a universal mathematical guarantee. The remaining empirical items
(#13 rate, #18, #19, #21) are recorded, bounded, and harness-gated, and none is load-bearing for
collision safety: the load-bearing path is caps 1–5 → Theorem V1 (echo ≤ 0.0042) → T6c/T6d →
Stage-5 gate on measured π.

Restrictions honored throughout: no code modification or implementation; Anaconda v4.2 remains the
sole base; all existing functionality preserved; English only.

---

## Change log vs v1.8

- **Retracted:** the T6b-ii derivation "chained sum over the local arc ≈ 2×ΔL_max" as a universal
  claim (labeled empirical; refuted by script D1: 0.017449 u measured, 0.0245 u in-domain worst).
- **Added:** cap 5 — total-sagitta budget Σ_k ΔL_k(δ*) ≤ Λ = 0.0042 u per frame, deterministic
  bisection enforcement, appended to the v1.8 §2.3 cap chain; Theorem V1 and Lemma P1 (proven
  displacement bound, every configuration incl. hairpin); next-frame Stage-3 no-op consequence;
  R-FINAL clause (d) (v1.5 0.5 s deadline, made precise, sticky revocation) and the binding
  monotonicity clause; script section D (D1 adversarial refutation, D2 hairpin extremes, D3
  300-run randomized suite, D4 R-FINAL checker) and the claim-classification ledger.
- **Unchanged:** repair pass algorithm (exact, uncapped); caps 1–4 and all their constants;
  T6a (0.0021), T6b-i (SEG ± 1e−5), T6b-ii wire (0.0045, now with proven 0.0003 headroom), T6c
  (−0.0067), T6d (0.005), T3, the π bands, R1/R3/R4/R5, L1–L3, T1–T7; the global 79-constraint
  projection and all v1.8 §1–§2 proofs.
