# Amendment v1.8 — Corrected Projection Mathematics, Combined Error Bound, Stage-5 Failure Semantics, Recomputed Worked Example

Base: Anaconda v4.2 snippet only (`anaconda-wordpress-snippet-v4.2 (6).html`, 2,644 lines).
Status: design-only. No code changes, no implementation. All existing v4.2 functionality preserved.
All numeric claims below were produced and re-checked by the verification script
`scripts/v18_example.py` (numpy float64); no hand arithmetic is used anywhere in this document.

---

## §0 Findings accepted

All four findings of the v1.7 audit are accepted.

1. The §4 displacement field of v1.7 ("spreads across rings 9–16 at −0.0025 u/ring") is **retracted in full**. It follows from neither the stated full-chain projection nor any anchored variant analyzed here; it was the transcription of an unstated local-anchor mental model into a global-system equation. Your recalculated value (uniform **−0.00025 u per ring across all 80 rings**) is **confirmed exactly** (§1.2) and adopted.
2. The combined bound "0.0031 u" is **retracted**. It is invalid twice over: the combiner (quadrature) is not the exact combination rule, and its 0.0025 parallel input does not exist in the corrected system. Exact analysis and the corrected bound are in §2.
3. Stage 5 had no deterministic failure semantics. They are now defined as rules R1–R5 (§3). The system never displays a new pose with π > 0.02 u.
4. The worked example is recomputed end-to-end with the corrected projection and combined bound (§4); no v1.7 numbers are retained.

---

## §1 Finding 1 — the stated projection, recalculated exactly

### 1.1 The system as stated

Rings 0…79 (N = 80), segments k = 0…78 (M = 79), SEG = 0.1 u. For a demand field
a ∈ ℝ^(80×3) the admissibility constraint matrix is

    C ∈ ℝ^(79×240),   row k:  δ ↦ (δ[k+1] − δ[k]) · t̂_k

and the projection is `δ* = a − Cᵀ(CCᵀ)⁻¹Ca` — the orthogonal projection of a onto
null(C), the first-order isometry fields. For the straight chain along x, t̂_k = x̂ for all k,
so C = B ⊗ x̂ᵀ with B the 79×80 incidence matrix (B[k,k] = −1, B[k,k+1] = +1), and all 79
constraints read δ[k+1].x − δ[k].x = 0, i.e. **δ[i+1].x = δ[i].x** — exactly as you stated.

### 1.2 Exact recalculation — your value is confirmed

**Theorem (straight chain).** null(C) intersected with the x-block is span{𝟙}; the orthogonal
projection onto it is the mean operator. Hence

    δ*[i].x = (Σ_i a[i].x) / 80   for every i,  and  δ*[i].y,z = a[i].y,z (unconstrained).

With the single-ring target a[13] = −0.020 x̂:

    δ*[i].x = −0.020 / 80 = −0.00025 u   for ALL i ∈ {0,…,79}.  ∎

Step-by-step (machine-verified): Ca has exactly two nonzeros, (Ca)₁₂ = −0.020, (Ca)₁₃ = +0.020.
With the closed-form inverse of the tridiagonal Gram matrix,
[(BBᵀ)⁻¹]ₖₗ = (min(k,l)+1)(79−max(k,l))/80, the solve gives the tent function
u_k = −0.00025(k+1) for k ≤ 12 and u_k = +0.00025(79−k) for k ≥ 13
(u₁₂ = −0.003250, u₁₃ = +0.016500). Then (Cᵀu)_i = u_{i−1} − u_i = +0.00025 for every i
(endpoints included), so δ* = a − Cᵀu gives δ*[13] = −0.020 + 0.01975 = −0.00025 and
δ*[i] = −0.00025 elsewhere. Measured: min = max = −0.00025000, Σδ* = −0.02000000
(the translation component is preserved: rigid motions lie in null(C), so the projection
never destroys them — verified in the general example too: Σa = Σδ* to 1.8e−19).

There are no anchors in this system, and none are needed: the field is applied as a **rigid
slide of the whole material chain** — the unique first-order-isometric representative of a
tangent-parallel correction. Its segment differentials are zero (measured 3.5e−18), so the
length error is zero at **all** orders, not just first.

### 1.3 Rank, solvability, conditioning — universal proofs (no rank-deficient case exists)

**Rank theorem.** For EVERY chain configuration with SEG > 0 (guaranteed by the Stage-3 rope
pass), rank(C) = 79.

*Proof.* Rows are functionals r_k(δ) = (δ[k+1] − δ[k])·t̂_k with |t̂_k| = 1. Suppose Σ α_k r_k = 0.
Evaluate at δ = e₀ ⊗ u for arbitrary unit u ∈ ℝ³: only r_0 touches ring 0, giving
−α₀ (u·t̂₀) = 0 ∀u, hence α₀ = 0. Inductively, evaluate at δ = e_j ⊗ u: the identity
α_{j−1}(u·t̂_{j−1}) − α_j(u·t̂_j) = 0 ∀u with α_{j−1} = 0 forces α_j = 0. All α vanish. ∎

This closes your rank question categorically: near-parallel tangents, hairpins, folds — no
configuration reduces the rank. (The measured near-anti fold of §4 has t̂₁₁·t̂₁₂ = −0.999848
and rank 79/79, κ = 1923.5.)

**Solvability.** G = CCᵀ is a Gram matrix of 79 independent rows, hence symmetric positive
definite; the Cholesky solve is unique and δ* is the unique least-norm admissible field.

**Conditioning (configuration-independent).** For x ∈ ℝ⁷⁹ (edge coefficients), with the
convention x₋₁ = x₇₉ = 0:

    xᵀGx = Σ_{j=0}^{79} ‖x_{j−1}t̂_{j−1} − x_j t̂_j‖²
         ≥ Σ_{j=0}^{79} (|x_{j−1}| − |x_j|)²        (reverse triangle)
         ≥ λ_D ‖x‖²,   λ_D = 2 − 2cos(π/80) = 0.00154193   (Dirichlet–Poincaré on the pinned path)
    xᵀGx ≤ 4‖x‖²                                    (triangle inequality)

so **κ(G) ≤ 4/λ_D = 2594.2 for every configuration**, with the straight chain the worst case
(measured: det = 80, λ_min = 0.00154193, λ_max = 3.998458, κ = 2593.2). In float64
(ε = 2.2e−16) a backward-stable Cholesky solve yields relative error ≤ c·κ·ε ≈ 6e−13, so the
design tolerance on the tangential residual is |w∥| ≤ 1e−12 u (three orders of headroom;
measured 7.8e−19 in §4).

### 1.4 The anchored variant you asked about — constructed, proven, rejected

Adding fixed anchors at rings 9 and 16 (x-block: δ[9].x = 0, δ[16].x = 0) to the 79 telescoping
rows: the telescoping rows span exactly the mean-zero functionals on ℝ⁸⁰ (dimension 79);
e₉ is outside that span (e₉(𝟙) = 1 ≠ 0); e₁₆ = e₉ + Σ_{k=9}^{15}(e_{k+1} − e_k) lies in
span(e₉, telescoping rows). Hence the combined rank is 80 = ambient dimension, the constraint
system is consistent (0 satisfies everything) and solvable, and the null space is {0}.
Consequence: the projection maps **every** tangent-parallel demand to zero — the anchored
system is mathematically sound but functionally dead for parallel absorption. It is therefore
**rejected**; partial anchoring (the windowed idea) is retired per §1.5.

### 1.5 Design decision and consequences

v1.8 binds the absorption stage to the stated **global 79-constraint projection**:

- **Tangent-parallel correction → rigid yield.** Absorbed as a body-wide slide; zero length
  error at all orders; render-neutral by the paired transfer. Per ring the single-event slide is
  −0.00025 u (0.25 mm) — invisible; cumulatively the slide equals the total parallel correction
  absorbed, bounded by the residual cap (0.22 u worst case, typically the contact depth).
  Physically this is a rope transmitting a longitudinal push — correct behavior, not an artifact.
- **Tangent-normal correction → local absorption.** Sagitta error only, ≤ 0.0019804 u per
  segment (§2), repaired by Stage 8.
- **Non-representable components stay in _ro** (Fix 2's intent), now with a provable mechanism
  and exact accounting: absorbed + retained = demand, always (measured retention 5.7% in §4).
- The windowed 47-constraint admissibility system of Fix 2 is **retired**: every
  window-admissible field is globally admissible, the global system's rank and conditioning are
  proven for all configurations, and its per-frame cost is one tridiagonal solve (O(n)). The
  windowed consensus/core-filter/capacity machinery is retained for **demand computation only**.

**Limitation L1 (recorded, bounded, testable).** After the rigid part is absorbed, a zero-sum
parallel *gradient* remains in _ro and its re-drain projects to ≈ 0 (sub-case 0: frame-2 slide
−1e−9 u/ring; §4 frame 3: a 0.0022 u residue decaying 2e−6/frame). It is not lost and not
dangerous: render is held (π unaffected), the magnitude is bounded by a_cap per event and the
0.22 u cap overall, and it drains once locomotion curvature re-orients the local tangent frame
so the residue becomes locally representable. Harness gate T7 is added: after any scripted
contact event, the event-region ‖_ro‖ must fall below 25% of its peak within 2.0 s of scripted
locomotion. Contingency (not adopted): a tangential tolerance w∥ ≤ 0.001 u variant.

---

## §2 Finding 2 — exact combined segment-length error

### 2.1 Exact formula

Let the segment k have pre-length SEG (exact after Stage 3) and unit tangent t̂, and let the
absorption transfer produce the differential w = Δ[k+1] − Δ[k] = w∥ t̂ + w⊥, w⊥ ⊥ t̂. Then

    |v'| = √((SEG + w∥)² + ‖w⊥‖²),      ΔL = |v'| − SEG.

ΔL is strictly increasing in both w∥ and ‖w⊥‖ on the physical domain SEG + w∥ > 0, so the
worst case for bounds p = |w∥|, q = ‖w⊥‖ is ΔL ≤ √((SEG+p)² + q²) − SEG. Special cases:
pure parallel gives ΔL = w∥ (first order); pure perpendicular gives the sagitta
ΔL = q²/(√(SEG²+q²)+SEG) ≈ q²/2SEG (second order). **There is no quadrature rule and no
linear rule — the single square root is the exact combiner.** The linear sum is a safe upper
bound: ΔL ≤ p + q²/2SEG.

### 2.2 Verdict on the claimed 0.0031 u — invalid, and unsafe

Taking v1.7's own inputs at face value (p = 0.0025, q = 0.020):

- exact combined error: √(0.1025² + 0.02²) − 0.1 = **0.0044330 u**;
- quadrature ("RSS"): √(0.0019804² + 0.0025²) = 0.0031893 u — **under-estimates the exact
  value by 28.1%**, so the v1.7 claim was not merely mis-derived, it was unsafe;
- linear sum: 0.0044804 u (valid upper bound).

Additionally the 0.0025 input itself was an artifact of the retracted §4 field: after the
corrected projection the tangential differential is ≤ 1e−12 u by construction (§1.3), and the
perpendicular differential is capped directly (§2.3). Both inputs of the 0.0031 claim are gone.

### 2.3 Corrected bound architecture

Caps, applied in this fixed order (determinism):

1. **Drain cap:** per-ring demand a_i = _ro_i · min(1, k_abs·dt/‖_ro_i‖), k_abs·dt = 0.025 u at 60 fps.
2. **Per-ring cap (Fix 3, accepted):** |a_i| ≤ a_cap = 0.020 u.
3. **Frame ℓ₂ budget:** ‖a‖ ≤ A = 0.035 u (body) / 0.05 u (neck); otherwise scale a ← a·A/‖a‖
   (the projection is linear, so scaling commutes with it).
4. **Differential cap (new, explicit):** the applied field must satisfy
   |Δ[i+1] − Δ[i]| ≤ d_cap = 0.020 u for every segment. Enforcement: deterministic alternating
   projection between the subspace {Cδ = 0} and the convex differential ball (8 sweeps, then
   verification to 1e−6; on failure scale the demand by 0.5 and restart, ≤ 3 retries; else absorb
   nothing this frame and log). Both sets are closed convex with non-empty intersection (0),
   so von Neumann iteration converges; the fixed sweep order makes the result deterministic.

With (1)–(4), on every segment: |w∥| ≤ 1e−12 and ‖w⊥‖ ≤ d_cap + 1e−6, hence

    **ΔL_max = √((SEG + 1e−12)² + (d_cap + 1e−6)²) − SEG = 0.0019805 u ≈ 0.0019804 u.**

This re-derives the Fix-3 boundary error — which v1.6 asserted and v1.7 mis-combined — as an
actual theorem. Without the differential cap the adversarial bound would be
√(SEG² + (2A)²) − SEG = 0.0221 u; the cap is what makes the bound tight. In the §4 example
the cap never engaged (max ‖w⊥‖ = 0.011296 → measured ΔL_max = 0.000636).

### 2.4 Updated threshold table (supersedes v1.6/v1.7 values)

| Test | v1.6/v1.7 | v1.8 | Derivation |
|---|---|---|---|
| T6a: max per-segment ΔL before repair | 0.0020 + 1e−5 | **0.0021 u** (value kept) | ΔL_max = 0.0019804 (§2.3) + solver tolerance + margin |
| T6b-i: post-repair segment length | SEG ± 1e−5 | **SEG ± 1e−5** (kept) | Lemma-1 exactness (measured 3.7e−16) |
| T6b-ii: max cumulative repair displacement of a ring | \|δ\| ≤ 0.0021 | **0.0045 u** (updated) | local identity \|δ_k\| = \|ΔL_k\| is exact (measured dev 1.7e−18); cumulative is the chained sum over the local arc ≈ ΣΔL ≈ 2×ΔL_max + margin; harness trip-wire (measured 0.001042) |
| T6c: minimum true clearance | ≥ −0.0025 | **≥ −0.0067 u** (updated) | measurement/sagitta-inflation margin 0.0025 + repair echo 2×0.0021 = 0.0042 |
| T6d: per-frame clearance regression | ≥ −0.005 | **≥ −0.005 u** (kept) | repair echo 0.0042 of the 0.005 budget (measured 0.000003) |
| T3: render neutrality of absorption | ≤ 0.0025 | **≤ 0.0025 u** (kept) | paired transfer exact to fp rounding (measured 1.4e−17) |
| π bands (acceptance rule) | 0.005 / 0.02 | **unchanged** | independent of these derivations |

### 2.5 Repair-versus-absorption, quantified (closes the v1.5 Case-B loose end)

The Stage-8 repair displacement δ = SEG·v'/|v'| − v' is parallel to v'; it removes exactly the
tangent-parallel excess (Lemma 1). Its component against a freshly absorbed normal correction
of size w⊥ is δ·n̂ = −(ΔL/|v'|)·w⊥, i.e. a loss fraction ΔL/|v'| ≈ ΔL/SEG ≤ **1.94% per repaired
segment** (0.0019804/0.1019804). First-order loss is zero — for the projected field the repair
has nothing tangent-parallel to remove beyond the second-order sagitta. The ≤ 0.0021 u echo is
visible to the next frame's solver (X' = X + δ_rep), which re-demands it if it re-penetrates:
self-healing, and directly measured in §4 (next-frame π = 0; clearances unchanged).

---

## §3 Finding 3 — Stage-5 deterministic failure semantics

Stage 5 measures π = maximum penetration over all render capsule pairs and obstacles
(continuous capsule distance, sagitta-inflated radii) on the candidate state X, and applies
rules R1–R5. All quantities are measured; all constants are fixed; band boundaries are
inclusive/exclusive as written; there is no randomness and no undefined tie.

- **R1 (hard render gate).** A new pose is displayed if and only if π ≤ 0.02 u. No code path
  can display a new pose with π > 0.02 u.
- **R2 (bands).** π ≤ 0.005 → PASS, render, silent. 0.005 < π ≤ 0.02 → FAULT: render is
  permitted only while ALL of (a) π(n) ≤ π(n−1) + 0.0005 (non-growing), (b) the responsible
  _ro region shows drain progress ≥ 50% of the k_abs·dt schedule cumulatively since fault
  onset, and (c) ≤ 12 fault frames in the rolling last 600 (2%). If any fails → R3.
- **R3 (single retry).** Discard the candidate; re-run Stage 4 once from the pre-solve state
  with all solver step sizes × 0.5; re-validate. If the retry satisfies R1 (and R2 if in band),
  render it (log fault if in band). Else → R4.
- **R4 (hold last safe frame).** Re-display the last displayed pose bit-identically (body state
  frozen; ambient water/wave visuals may continue — they are not part of π's body contract).
  The held pose's π against the *current* environment is measured and logged but does not gate
  (no new pose is shown). Every held frame still runs Stage 4 at full budget on the frozen
  state; the first candidate passing R1/R2 resumes normal rendering and resets hold_count.
- **R5 (re-birth, stuck-hold escape).** If hold_count reaches 120 frames (2.0 s at 60 fps):
  set P ← X_frozen, _ro ← 0, renormalize P to exact SEG (the render is unchanged by the
  assignment by construction; the renormalization result is a *candidate*, not a display, and
  must still pass R1/R2). Reset hold_count and continue. This is the deterministic escape from
  degenerate solver states and cannot itself display a violating frame.

Clarifications demanded by the audit:

- **"Solver cannot find a valid configuration":** Stage 4 is a bounded relaxation (K = 3
  alternating iterations) — it always outputs; failure manifests as R1 violation and is handled
  by R3/R4. There is no separate branch and no unproven "Stage 4 will restore" claim: the gate
  is π, measured, every frame.
- **"Tier-2/Tier-3 exhausted":** the Tiers are constraints on how the solver may deform the
  body while fixing penetration, not consumable resources. There is no exhausted state; if the
  solver cannot reach π ≤ 0.005 within them, the result lands in the FAULT band or R3/R4 by
  the rules above.
- **Bootstrap:** the spawn pose is safe by construction, so R4 always has a last displayed pose.
- **Fault-band persistence is impossible:** condition R2(b) converts any long-lived FAULT into
  R3 → R4 within 0.5 s.

---

## §4 Finding 4 — recomputed worked example (all numbers machine-verified)

Verification script: `scripts/v18_example.py`. Wave = 0 (collision-safety layers validated in
isolation); planar presentation (x–z, ride height y = 0.02) for printability; the mathematics
is fully 3-D and the code is 3-D.

### 4.1 Setup

80 rings, SEG = 0.1 u, body capsule radius 0.05 u. Chain: straight along +x, then a fold over
segments 10–13 with directions θ₁₀ = 85°, θ₁₁ = 170°, θ₁₂ = 351°, θ₁₃ = 356°, straight
afterwards — the joint t̂₁₁·t̂₁₂ = **−0.999848** is the requested near-anti
(near-rank-deficient-looking) configuration. Two wall obstacles (finite segments in x–z,
radius 0.03): wall A from (0.80, 0.175) to (1.25, 0.175) above the fold; wall B from
(5.95, 0.165) to (6.45, 0.165) above the far body (index distance from contact A ≥ 46; the
|i−j| ≥ 9 self-collision rule is satisfied throughout).

Selected positions (x / y / z): P[10] = (+1.0000, 0.0200, +0.0000), P[11] = (+1.0087, 0.0200, +0.0996),
P[12] = (+0.9102, 0.0200, +0.1170), P[13] = (+1.0090, 0.0200, +0.1013),
P[14] = (+1.1088, 0.0200, +0.0944), P[62] = (+5.9088, 0.0200, +0.0944), P[67] = (+6.4088, 0.0200, +0.0944).

Post-solve residual _ro (the K = 3 staggered solve's output; pushes along −ẑ; derived by a
fixed-point clearance sweep to a +0.0025 u margin with Tier-3 strain relief; verified):
rings 10: 0.0071, 11: 0.0071, 12: 0.0245, 13: 0.0088, 14: 0.0019, 15: 0.0019, 16: 0.0009;
rings 62–67: 0.0119, ring 68: 0.0109. Wall A therefore interacts with segments (10,11), (11,12),
(12,13), (13,14) — four interacting segments with rings 11/12/13 shared between adjacent
segments; wall B adds the second contact.

Solve quality: all ring/midpoint penetrations cleared to ≥ +0.0025; true continuous render
clearance +0.002112 (A) and +0.002114 (B) (the continuous minimum sits between checked bases,
0.0004 under the basis target — still deep in the PASS band); render strain −1.52% … +0.70%
(Tier-3 limit ±5%); max residual ring-to-ring differential 0.0174 ≤ d_cap.

### 4.2 Frame 1

**Caps.** Drain cap 0.025: no ring clipped. a_cap 0.020: ring 12 clipped (0.0245 → 0.020).
ℓ₂ budget 0.035: ‖a‖ = 0.039406 → scale ×0.888195 → ‖a‖ = 0.035000.

**Projection.** Built from the current P (exact SEG). rank(C) = 79/79; κ(CCᵀ) = 1923.5
(universal bound 2594.2); ‖Cδ*‖∞ = 7.8e−19; max |w∥| = 7.8e−19; max ‖w⊥‖ = 0.011296
(differential cap not engaged). Rigid-component preservation: Σa = Σδ* = (0, 0, −0.115400)
to 1.8e−19. Far-field leakage outside the contact zones: ≤ 3.4e−05 u/ring. Retained in _ro:
‖a − δ*‖ = 0.001993 (5.7% of the demand — the fold-apex in-plane gradient, §1.5/L1).

δ*_z per ring — arc A (9…17): 0, −0.00633, −0.00634, −0.01746, −0.00799, −0.00181, −0.00166, −0.00083, 0;
arc B (60…68): 0, 0, −0.01053, −0.01055, −0.01055, −0.01055, −0.01055, −0.01055, −0.00970.

**Combined-error audit at the worst segment (11, i.e. rings 11→12):**
w∥ = +2.2e−19, w⊥ = 0.011296 → ΔL = √((0.1 + 2.2e−19)² + 0.011296²) − 0.1 = **0.000636**
(single-segment bound 0.001980; ΣΔL over all segments = 0.002519). T6a PASS.

**Paired transfer.** P += δ*, _ro −= δ*: render invariance max |ΔX| = 1.4e−17 (T3 PASS).

**Stage-8 repair.** Isolated Lemma-1 identity |δ| = |ΔL| exact to 1.7e−18; chained-pass local
deviation 2.0e−04 (second-order chaining, as expected); cumulative ring displacement ≤ 0.001042
(T6b PASS); post-repair max |len − SEG| = 3.7e−16 (T6b-i PASS).

**Next-frame validation (X' = P_repaired + _ro').** Wall A: +0.002112 → +0.002112 (regression
0.000000); wall B: +0.002114 → +0.002110 (regression 0.000003); π(next frame) = 0 → PASS band.
T6c PASS (+0.002110 ≥ −0.0067); T6d PASS (0.000003 ≤ 0.005).

**Final positions, arc A (x / z): P → P+δ* → P_repaired, then _ro':**

| ring | P | P+δ* | P_repaired | _ro' (x, z) |
|---|---|---|---|---|
| 10 | (+1.0000, +0.0000) | (+1.0000, −0.0063) | (+0.9998, −0.0063) | (+0.000000, −0.000794) |
| 11 | (+1.0087, +0.0996) | (+1.0088, +0.0933) | (+1.0088, +0.0933) | (−0.000064, −0.000788) |
| 12 | (+0.9102, +0.1170) | (+0.9083, +0.0995) | (+0.9090, +0.0995) | (+0.001898, −0.007047) |
| 13 | (+1.0090, +0.1013) | (+1.0086, +0.0933) | (+1.0088, +0.0933) | (+0.000398, −0.000855) |
| 14 | (+1.1088, +0.0944) | (+1.1088, +0.0926) | (+1.1088, +0.0926) | (−0.000034, −0.000053) |
| 15 | (+1.2088, +0.0944) | (+1.2088, +0.0927) | (+1.2088, +0.0927) | (−0.000034, −0.000209) |
| 16 | (+1.3088, +0.0944) | (+1.3088, +0.0935) | (+1.3088, +0.0935) | (−0.000034, −0.000104) |

### 4.3 Frames 2–3 (drain continuation)

- Frame 2: ‖a‖ = 0.008222, max ΔL = 0.000187, max repair 0.000187; residual max arc A/B =
  0.002225 / 0.000178.
- Frame 3: ‖a‖ = 0.002382, max ΔL ≈ 0; residual max arc A/B = 0.002222 / 0.000185. The arc-B
  residue is drained; the arc-A residue is the fold-apex gradient (z-components ≤ 3e−5,
  vector sum −3.9e−7) — the L1 stall mode of §1.5, live: it decays 2e−6/frame until locomotion
  curvature re-orients the fold's tangent frame. Bounded (≤ a_cap per event, ≤ 0.22 cap
  overall), render-held, T7-gated.

Worst-case full-cap drainage: 0.22 u / 0.025 u per frame = 8.8 frames ≈ 0.15 s ≤ 0.5 s — the
acceptance rule's drain promise holds for representable residuals.

### 4.4 Audit-requirement map

| Requirement | Where shown |
|---|---|
| Corrected projection produces the stated numbers | §1.2 (−0.00025 uniform), §4.2 (rank 79, κ 1923.5, ‖Cδ*‖∞ 7.8e−19) |
| Combined parallel+perpendicular error, exact | §2.1 formula; §4.2 worst segment (w∥ 2.2e−19, w⊥ 0.011296 → ΔL 0.000636) |
| Shared rings, ≥3 interacting segments, near-parallel config | §4.1 (t̂₁₁·t̂₁₂ = −0.999848; segments (10,11)–(13,14); rings 11/12/13 shared) |
| Absorption → rope repair → next-frame validation with real numbers | §4.2 tables; T6a–T6d all PASS |
| No old numbers retained | v1.7 §4 retracted (§0); sub-case 0 replaces it |

---

## §5 Strict verdict

**v1.7 as written was not mathematically complete**: its §4 example did not follow from its own
equations (your correction is exact and adopted), its combined error bound used an invalid
combiner and an invalid input, and Stage 5 had no failure semantics.

**After these corrections (v1.8 superseding v1.7 §4 and patching the rest), the design is
mathematically complete for Stage-1 purposes and is CONDITIONALLY VALID.** The conditions —
recorded limitations, each bounded and harness-gated — are:

- **L1:** zero-sum tangent-parallel gradient residues stall in _ro (measured decay 2e−6/frame)
  until locomotion curvature re-orients the local tangent frame; bounded per event by a_cap and
  overall by the 0.22 u cap; render correctness unaffected; gate T7 (drainage ≤ 25% of peak
  within 2.0 s of scripted locomotion). Contingency specified, not adopted.
- **L2:** the differential-cap enforcement converges by alternating projection (guaranteed for
  two closed convex sets with non-empty intersection) but the sweep count is empirical
  (8 sweeps + deterministic scale-fallback), not a closed-form rate.
- **L3:** Stage-4's K = 3 iteration count remains heuristic; no safety claim rests on it, since
  every display decision routes through the Stage-5 gate R1–R5.

With L1–L3 on record and T1–T7 as implementation gates: **Stage 1 is ready to proceed to S2
upon your explicit approval.** Implementation, when approved, starts at S1 (3-D vertical
infrastructure, zero visual change) and remains gated by T1–T7 through S6. Until then: no code
changes, Anaconda v4.2 remains the sole base, all existing functionality preserved.

---

## §6 Change log vs v1.7

- **Retracted:** §4's rings-9–16 displacement field and every number derived from it
  (−0.0025 u/ring; the 0.0025 parallel contribution; the 0.0031 combined bound).
- **Adopted:** your uniform −0.00025 u result as the stated system's exact output; the global
  79-constraint projection as the sole admissibility mechanism (windowed Fix-2 constraints
  retired to demand computation); no anchors (anchored variant proven rank-80/null-{0} and
  rejected as vacuous for parallel absorption).
- **Proven:** rank(C) = 79 for every configuration; κ(CCᵀ) ≤ 2594.2 universally; rigid-component
  preservation; the exact combined length-error formula; ΔL_max = 0.0019804 u under the cap
  chain (drain 0.025 → a_cap 0.020 → ℓ₂ 0.035/0.05 → differential d_cap 0.020).
- **Updated:** T6b-ii 0.0021 → 0.0045; T6c −0.0025 → −0.0067 (budget decomposition given).
  T6a, T6b-i, T6d, T3, and the π bands keep their values, now with correct derivations.
- **Added:** deterministic Stage-5 rules R1–R5 (hard gate π ≤ 0.02; bands; single retry; hold;
  re-birth); differential cap with deterministic enforcement; harness gate T7; limitations
  L1–L3.
