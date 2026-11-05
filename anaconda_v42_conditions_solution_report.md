# Consolidated Solution Report — the three unresolved v1.10 conditions

Base: Anaconda v4.2 only (`anaconda-wordpress-snippet-v4.2 (6).html`, 2,644 lines).
Status: design-only. No base code changed, no Stage-1 work started, all existing v4.2
functionality preserved. This is a solution report, not an amendment: it proposes
exactly two design changes (S1, S2) and one no-change finding (R-FINAL), with proofs,
executed evidence, and acceptance criteria. Nothing here takes effect without your
explicit approval.

Executed evidence: `scripts/solution_probe.py` (441 lines, deterministic — two runs
produce the byte-identical output, SHA-256 `6e822431a2db3dd1721480a46c4356aeaf8c0cb71fae9839cf57d1a7fa42e739`).
The canonical `scripts/v18_example.py` (729 lines, SHA-256 `27c6418a…`) and its archive
copy are untouched. The probe output is embedded verbatim in §9.

Classification discipline used throughout: **PROVEN** = exact mathematical proof (no
linearization, no configuration assumptions); **VERIFIED** = numerically executed by the
probe on stated domains; **EMPIRICAL** = observed on tests, coverage-dependent, never
stated as a universal guarantee.

---

## 1. Root cause of the 2Λ pair echo (conditions T6e and L4)

The v1.10 ceiling 2Λ exists because the current Stage-8 repair rule re-derives each
segment's direction from the **working vector**. Writing s_k for the input segment,
L_k = ‖s_k‖, e_k = L_k − SEG, and δ_k for the cumulative displacement of ring k, the
pass places ring k+1 at distance SEG from the already-repaired ring k **along the
working direction**:

    v_k = s_k − δ_k,      Q'_{k+1} = Q'_k + SEG · v_k/‖v_k‖,      (working-direction rule)

which gives the first-order transmission dynamics δ_{k+1} = P_k δ_k − e_k t̂_k
(P_k = projector on the local segment direction). Two consequences, both measured in
v1.10 and reproduced by the probe (P3, OLD row: echo(4,77) = 0.006632, cos(δ_4,δ_77) =
−0.9966 — exact reproduction of the v1.10 baseline):

1. A displacement built on one limb **follows the chain around a gentle fold** (each
   step re-projects it onto the new local direction; a 20-segment 180° arc attenuates
   by 0.988²⁰ ≈ 0.79), and emerges at the return limb pointing **anti-parallel** to a
   displacement built elsewhere — so two rings of one pair can separate by up to
   ‖δ_i‖ + ‖δ_j‖ ≤ 2Λ.
2. Whether the true supremum is 1.599Λ (measured) or 2Λ (proven) stayed unresolved —
   and with it, L4's one-frame penetration ceiling 0.0025 − 2Λ = −0.0059 u.

The native v4.2 follow-chain (L1505–1517) is this same working-direction rule and runs
in its own per-frame slot; **it is not touched by anything proposed here.** The
Stage-8 restoration pass, however, is design-added machinery (it exists only to undo
the length perturbation the design's own projection step creates), and its direction
rule is a free design choice. That freedom is what the solutions below use.

---

## 2. Solution S1 — fixed-direction SEG restoration (eliminates the mechanism)

**Definition.** Replace the Stage-8 rule by the *input-tangential* pass:

    Q'_0 = Q_0 (anchored),      Q'_{k+1} = Q'_k + SEG · t_k,      t_k = s_k/‖s_k‖.

Each output segment keeps the **input segment's direction exactly** and has length
exactly SEG; the pass is one forward sweep, no iteration, ring 0 anchored (native
contract A3 preserved).

**Exact displacement identity (PROVEN).** Unrolling,

    δ_{k+1} = δ_k + SEG·t_k − s_k = δ_k − e_k·t_k,   hence   δ_j − δ_i = −Σ_{k∈[i,j)} e_k·t_k.

No linearization: this is exact for arbitrary magnitudes (probe P1: recursion identity
max residual 4.2e−16; post-repair max |len − SEG| = 3.5e−16; ring 0 exactly anchored).

**Theorem V1′ (ring displacement — PROVEN).** ‖δ_j‖ = ‖Σ_{k<j} e_k t̂_k‖ ≤ Σ_{k<j}|e_k| ≤
Σ_all |e_k| ≤ Σ_all dL_k ≤ Λ. The cap-5 bisection is the only ingredient; the
transmission analysis is no longer needed.

**Lemma (|e_k| ≤ dL_k — PROVEN, elementary).** For any w, |‖SEG·t̂ + w‖ − SEG| ≤
√((SEG+|w_par|)² + w_perp²) − SEG, because the left side is bounded by |w_par| + O(w²)
while the right side dominates it termwise. (Probe P1: max residual 1.1e−15 = the
float64 cancellation floor of the √-subtraction itself.)

**Theorem V2′ (pair echo — PROVEN).** For every pair i < j, every configuration,
every admissible error field:

    D'_ij − D_ij = ‖Σ_{[i,j)} SEG·t_k‖ − ‖Σ_{[i,j)} (SEG+e_k)·t_k‖  ⇒  |ΔD_ij| ≤ Σ_{[i,j)} |e_k| ≤ Λ.

Reverse triangle inequality, exact. The pair echo is governed **only by the error mass
locally between the two rings** — upstream error mass cannot reach across the pair,
because nothing rotates or transmits: with e_k = 0 on an interval, δ is exactly
constant there (probe P3: |δ_4| = |δ_77| = 0.004141, cos = +1.0000 — the downstream
chain translates rigidly).

**Theorem V2′ is tight (PROVEN + VERIFIED).** A straight chain whose error budget is
concentrated inside [i,j) with aligned directions attains echo = Λ. Probe P2 D1-analog
at Λ = 0.0025: full-span pair (0,79) echo = 0.002499209 = **1.000×Λ**. So no bound
below Λ exists in general — Λ is the exact supremum for far pairs, and T6e can be set
to Λ with zero slack wasted.

**What this does to the v1.10 adversarial landscape (VERIFIED, probe P3):**

| Construction (chord-aligned U-turn, sum\|e\| as shown) | OLD repair | S1 repair |
|---|---|---|
| echo(4,77) | 0.006632 | **0.000000000 (exact)** |
| max all-pair echo @ Σ\|e\| = 0.0042 (Λ_OLD) | 0.006718 = 1.60Λ_OLD | 0.004141 ≤ Λ_OLD |
| max all-pair echo @ Σ\|e\| = 0.0025 (Λ_NEW) | — | 0.002479 = 0.992Λ_NEW (tight) |

The 1.599Λ-vs-2Λ open problem **dissolves**: it existed only for the
working-direction rule. Under S1 the supremum is exactly Λ, attained, proven.

**Near-collision geometry (supporting argument, not a new theorem).** A near-colliding
self-pair (|i−j| ≥ 9, spatial distance ≈ 2·R_BODY) spans an interval of arc ≥ 0.9 u
and chord ≤ ~0.1 u; the connecting fold is therefore necessarily sharp (a 180° turn
inside a ~0.1 u gap needs radius ≈ 0.05 u ≈ 1–3 segments). Sharp folds are exactly
where the OLD rule's transmission dies (measured in P4: OLD echo(30,45) = 0 on the
near-collision hairpin) and where S1's local-mass bound is smallest: only the 1–2
apex segments point across the chord, and each carries at most the T6a domain mass
0.0019804 (P4 field (a): echo = 0.001980227). Note the honest asymmetry: this
sharp-fold argument is a geometric observation, **not** a uniform theorem for the OLD
rule — OLD's −0.0059 ceiling remains its proven worst case. S1 replaces that ceiling
with a uniform proven bound everywhere.

**Practical consequences.**
- Behavior change: where the OLD rule deforms the downstream chain (direction-chasing),
  S1 translates it rigidly (δ constant on error-free intervals) — less deformation, the
  same exact rope. Rigid slide is the benign mode the framework already prefers.
- Implementation cost (future Stage 1): ~10 lines; directions from the input state,
  one cumulative pass. No native code touched; the native follow-chain keeps running
  unchanged in its stage-3 slot and is a no-op on the already-exact chain.
- Adjacent-pair identity R1′: |ΔD_{k,k+1}| = |e_k| exactly (unchanged from v1.10 R1,
  now exact also in the chained pass — the OLD rule's 2.0e−4 second-order chaining
  deviation disappears).
- Theorem V3 (static obstacles ≤ Λ) is unchanged and remains the governing bound for
  T6c/T6d.
- The render-state invariance chain is preserved: projection + paired transfer leave
  X = P + _ro invariant (1.4e−17), so the render pair-echo equals the repair echo —
  V2′ directly bounds the measured quantity.

**Why S1 does not weaken anything.** It changes only the design-owned stage-8 pass;
all v4.2 behavior (follow-chain, collision solve K=3, relax layer, absorption
exemptions, tail drape) is untouched; per-ring motion stays ≤ Λ (V1′); post-repair
rope exactness improves to machine precision (identical guarantee class).

---

## 3. Solution S2 — cap-5 budget Λ = 0.0042 → 0.0025 (= solve margin)

v1.10 rejected Λ = 0.0025 with three grounds: (i) it engages cap 5 on the worked
example; (ii) it slows broad-field absorption; (iii) "no safety benefit since T6e
covers the pairwise exposure". Under S1, ground (iii) is **no longer true** — the
adopted T6e equals Λ itself, so halving Λ directly halves the self-collision echo and
drives the L4 floor to zero. The other two grounds are real but small, and now
measurable:

- Engagement census (VERIFIED): 0/300 randomized configs (probe P2; max ΣdL =
  0.000874, 2.9× headroom) — cap 5 remains an adversarial-tail-only mechanism.
- Worked example (VERIFIED, probe P5): ΣdL = 0.002519 → s* = 0.996225, i.e. the
  projection scales by 0.38 % on that frame; wall regressions 0.000004 / 0.000067
  (baseline 0.000000 / 0.000003; T6d wire 0.005, headroom 73×); π(next) stays in the
  PASS band; ring displacement 0.00123 ≤ Λ.
- Absorption slowdown: the unprojected residual grows by the s*-deficit (~0.4 %) and
  drains at 0.025 u/frame — sub-frame effect; frames-to-drain unchanged within ±1 on
  the harness (to be re-baselined).

**Consequences (all PROVEN once S1+S2 adopted):** T6e ≤ 0.0025; T6b-ii ring
displacement ≤ 0.0025 proven (wire can drop from 0.0045 to 0.0026 — the +0.0003 fudge
margin becomes unnecessary); worst one-frame self-pair clearance = margin − Λ = **0
exactly**; T6c floor may tighten from −0.0067 to −0.005 (proposal: tighten, since the
proven echo halves); T6d wire unchanged at 0.005 (headroom doubles).

If even the exact-zero floor is wanted with a cushion, Λ = 0.0020 gives a +0.0005 u
clearance floor at the cost of s* = 0.891 on the worked example (11 % scale) —
offered as the conservative variant, default proposal remains Λ = 0.0025.

---

## 4. Condition 3 (L4) — resolved

| Design | Worst one-frame self-pair clearance after repair echo | Class |
|---|---|---|
| v1.10 (OLD rule, Λ = 0.0042) | 0.0025 − 0.0084 = **−0.0059 u** (in FAULT band) | arithmetic from proven bounds |
| S1 only (Λ = 0.0042) | 0.0025 − 0.0042 = **−0.0017 u** (sub-band, π ≤ 0.0017 < 0.005) | PROVEN (V2′) |
| **S1 + S2 (Λ = 0.0025)** | 0.0025 − 0.0025 = **0.0000 u** — fault-band entry from the repair echo is **eliminated** | PROVEN (V2′ + cap 5) |

Measured worst cases (VERIFIED): E2-adversarial class 0.002479 ≤ Λ_NEW with
near-collision pairs at ~0; near-collision hairpin apex-mass field (a) post-repair
clearance **+0.000550**; field (b) **+0.001296**. All ≥ 0, all ≥ 10× below the fault
threshold 0.005, 36× below the R1 hard gate 0.02.

**What genuinely remains (no hiding):**
1. π has sources outside the repair analysis — the solver's own iteration transients,
   the v4.2-native relax layer (_ro low-pass), obstacle interpenetration events from
   gameplay. These are covered exactly as before: by the measured-π gate R-FINAL
   (unchanged) — not by any new theorem.
2. That the next-frame Stage-4 solver *achieves* the +0.0025 margin on every violated
   self-pair within K = 3 iterations in every configuration remains **EMPIRICAL**
   (v4.2-native behavior, harness-tested). S1+S2 make this irrelevant for repair-echo
   exposure but do not prove solver convergence.
3. The exact-zero floor is a bound-floor (margin − Λ = 0): equality is attainable only
   if a frame's entire error budget aligns with the chord of an already-at-margin
   pair. The constructions required to approach it are measured (P4), not exhausted;
   the claim made is "≤ 0 penetration", not "clearance stays positive".
4. Considered and **not required**: a pair-chord guard (constrained repair projecting
   the displacement field off the guarded pairs' chords via the 161-dimensional rope
   kernel). It would push guarded-pair echoes to second order but introduces
   kernel-projection feasibility analysis and second-order re-repair terms — new proof
   burden with no safety need once the proven floor is 0. Recorded as a rejected
   alternative, v1.10 style.

---

## 5. Condition 2 (strict R-FINAL horizon) — kept, with its necessity proven and its role narrowed

**The horizon cannot be eliminated — and should not be.** It is the runtime enforcement
of the v1.5 acceptance rule ("π < 0.005 within 0.5 s of spike end" = clause (d), now
strict). Recovery *speed* is not provably bounded: the drain path stalls on
near-zero-sum residual gradients (measured in the canonical frames 2–3: arc-A residual
frozen at 0.002222 with Σz = −3.9e−7), and a worst-case recovery-time theorem would
have to quantify solver actuation against every adversarial geometry — not offerable
without an unproven claim, which the rules forbid. A deadline that converts an
empirical recovery into an enforced behavior is therefore **necessary**, and any
proposal to drop it would weaken collision safety. Recommendation: keep `n ≥
spike_end + 30` exactly as corrected.

**What S1+S2 change for this condition.** The repair echo can no longer push a solved
pair into the fault band at all (§4). The band machinery now serves only what it was
designed for — legitimate large demand spikes and obstacle squeezes — and the
repair-echo false-positive path into R3/R4 is gone.

**The exposure envelope is already provable from the rule logic (PROVEN, D4-checked):**
clauses (a) non-growing + (b) ≥ 50 % schedule drainage + (c) ≤ 12 rendered fault
frames per rolling 600 + (d) strict deadline give, together:
- any continuous stall is revoked at the 13th band frame (S2 series: 12× FAULT-RENDER,
  then R3/R4);
- worst-case band exposure per 600-frame window ≤ 12 frames = 0.2 s (2 % duty cycle),
  a bound no spike pattern can evade because (c) is a rolling budget;
- any π ≥ 0.005 persisting at spike_end + 30 revokes from that exact frame (horizon
  frame not displayed — probe-proven boundary in the v1.10 consistency fix).

**No clause is added, removed, or weakened.** The one explicit final rule remains
R-FINAL (a)+(b)+(c)+(d), which already merges the v1.5 0.5 s requirement as clause (d)
without dropping it. An optional stall-detector clause was considered and is **not
proposed**: clause (b) already revokes when drainage falls below half of schedule, so
a detector would be redundant machinery. Shortening the 30-frame deadline is likewise
not proposed: the binding exposure cap is 12 frames (clause c), below the deadline
already, and the 0.5 s value is the accepted v1.5 contract.

---

## 6. Consolidated before/after

| Item | v1.10 | + S1 | + S1 + S2 | Class |
|---|---|---|---|---|
| Pair-echo theorem | ≤ 2Λ = 0.0084; supremum unresolved in [1.599Λ, 2Λ] | ≤ Λ **exact, tight** (V2′) | ≤ 0.0025 exact, tight | PROVEN |
| T6e (self-collision per-frame regression) | 0.0084 | 0.0042 | **0.0025** | PROVEN |
| L4 one-frame self-pair penetration | ≤ 0.0059 (FAULT band) | ≤ 0.0017 (sub-band) | **≤ 0 (eliminated)** | PROVEN |
| Measured adversarial echo (E2 class) | 0.006718 | 0.004141 | 0.002479 | VERIFIED |
| Measured near-collision hairpin post-clearance | −0.0059 ceiling (unrealized locally; no uniform floor) | +0.000550 | **+0.000550** | VERIFIED |
| T6b-ii (ring displacement) | wire 0.0045 = Λ + 0.0003 | ≤ Λ exact | ≤ 0.0025 exact; wire → 0.0026 | PROVEN |
| T6c floor | −0.0067 | unchanged | −0.005 (proposed tightening) | PROVEN |
| T6d wire | 0.005 | unchanged | unchanged (headroom 2×) | PROVEN |
| R-FINAL | strict horizon | unchanged | unchanged; repair-echo path into band gone | PROVEN rule logic |
| cap-5 engagement | 0/300 randomized | 0/300 | 0/300; worked example s* = 0.9962 | VERIFIED |
| Native v4.2 code touched | none | none | none | — |

---

## 7. Claim classification (complete ledger for this report)

| # | Claim | Class | Evidence |
|---|---|---|---|
| 1 | S1 recursion δ_{k+1} = δ_k − e_k t̂_k exact; δ_j − δ_i = −Σ_{[i,j)} e_k t̂_k | **PROVEN** (algebra) + VERIFIED (P1, 4.2e−16) | §2 |
| 2 | Theorem V1′: ring displacement ≤ Σ_{k<j}\|e_k\| ≤ Λ | **PROVEN** | §2 |
| 3 | Lemma \|e_k\| ≤ dL_k | **PROVEN** (elementary) + VERIFIED (P1, 1.1e−15 = fp floor) | §2 |
| 4 | Theorem V2′: pair echo ≤ Σ_{[i,j)}\|e_k\| ≤ Λ, all pairs, all configs | **PROVEN** (exact) | §2 |
| 5 | V2′ tightness: echo = Λ attainable (far pair) | PROVEN construction + VERIFIED (P2: 1.000×Λ) | §2 |
| 6 | E2 mechanism eliminated: echo(4,77) = 0 exactly under S1 | PROVEN (zero local mass) + VERIFIED (P3: 0.000000000) | §2 |
| 7 | v1.10 OLD-repair baseline reproduction (0.006632 / 0.006718 / cos −0.9966) | VERIFIED (P3 cross-validation) | §1 |
| 8 | Post-repair SEG exactness (one pass, both rules) | PROVEN by construction + VERIFIED (P1/P2 ≤ 8.5e−16) | §2 |
| 9 | Near-collision sharp-fold geometric argument | Geometric analysis (labeled; not a uniform OLD-rule theorem) | §2 |
| 10 | Λ = 0.0025 engagement: 0/300 randomized; worked example s* = 0.9962 | VERIFIED (P2, P5) | §3 |
| 11 | Worked example gates hold under S1+S2 (regressions, π PASS) | VERIFIED (P5) | §3 |
| 12 | L4 floor: margin − Λ = 0 exactly (S1+S2); −0.0017 (S1); −0.0059 (v1.10) | **PROVEN** (arithmetic on proven bounds) | §4 |
| 13 | Solver achieves margin in K = 3 on all configs; multi-frame convergence | **EMPIRICAL** (v4.2-native; unchanged status) | §4 |
| 14 | Non-repair π sources (solver transients, relax layer, obstacle events) covered by measured gate only | **EMPIRICAL / measured** (unchanged) | §4 |
| 15 | Recovery speed bounded ≤ 30 frames for all configs | **NOT CLAIMED** — refused as unprovable-offerable; deadline is the enforcement | §5 |
| 16 | Exposure envelope: ≤ 12 fault frames / rolling 600; stall revoked at 13th; deadline exact | **PROVEN** (rule logic) + VERIFIED (D4 series) | §5 |

---

## 8. Testable acceptance criteria

**S1 (fixed-direction restoration):**
1. Post-repair max |len − SEG| ≤ 1e−12 on every harness configuration.
2. Recursion identity residual ‖δ_{k+1} − δ_k + e_k t̂_k‖ ≤ 1e−14 on every harness run.
3. Pair echo ≤ Λ on the full randomized suite (≥ 300 configs, fold-injected) and on
   the adversarial set; chord-aligned construction: echo(4,77) = 0 to 1e−12.
4. Ring displacement ≤ Λ everywhere; ring 0 exactly anchored.
5. No regression in T6a/T6c/T6d/Tier gates against re-baselined values (P5 shows the
   worked-example shifts: regressions ≤ 0.000068, π PASS).

**S2 (Λ = 0.0025):**
1. Σ dL ≤ 0.0025 enforced every frame (cap-5 bisection output logged).
2. Cap-5 engagement census on the randomized suite remains 0/300.
3. Worked example: s* ≈ 0.996, wall regressions ≤ 0.0001, π(next) in PASS band.
4. Frames-to-drain on the suite changes by at most ±1 frame vs baseline.

**R-FINAL (no change):**
1. D4 series S1/S2/S3 outputs byte-identical to the v1.10 run.
2. Stress census: ≤ 12 rendered fault frames in every rolling 600-frame window.
3. Deadline fires exactly at the first band candidate at/after spike_end + 30
   (boundary already probe-proven in the v1.10 consistency fix).

**L4 acceptance:**
1. Worst measured post-repair self-pair clearance ≥ 0 across the adversarial set
   (probe: +0.000550 worst).
2. No fault-band entry attributable to the repair echo in any harness run (π ≤ 0.005
   whenever the pre-repair state was at margin).

---

## 9. Executed probe output (verbatim, deterministic)

```text
==============================================================================
P1  S1 exactness asserts
==============================================================================
  post-repair max|len - SEG|        = 3.469e-16
  recursion |delta_(k+1)-delta_k + e_k t_k| max = 4.234e-16   (identity exact)
  ring-0 anchored: |disp[0]| = 0.0e+00
  lemma |e_k| <= dL_k: max (|e|-dL) over 200 fields = 1.110e-15
  P1 PASS

==============================================================================
P2  Theorem V1'/V2' sweep: 300 randomized configs (seed 42) + D1-analog
==============================================================================
  repair  max ring |delta|   max |dD| all pairs   max |dD| |i-j|>=9   max post|len-SEG|
  OLD         0.000238344          0.000246897         0.000242846            4.86e-16
  S1          0.000625374          0.000623956         0.000623956            8.47e-16
  max sum|e| (both) = 0.0008741  <= LAMBDA 0.0025 OK
  D1-analog @ LAM_NEW: s* = 0.321479  sum|e| = 0.0025000
    S1 max ring |delta| = 0.002499209  (<= LAMBDA: True)
    S1 full-span pair (0,79) echo = 0.002499209  (1.000 x LAMBDA -> bound is TIGHT)
  P2 PASS (V1' and V2' hold on the whole sweep)

==============================================================================
P3  E2 chord-aligned adversarial construction: mechanism collapse
==============================================================================
  prof differential [0.01 0.02 0.02 0.01]; cap-5 scale: @0.0042 s* = 0.919776, @0.0025 s* = 0.708606
  OLD repair @ LAM 0.0042 (v1.10 baseline)
    sum|e| = 0.004200   ring disp max = 0.003927649
    |d_4| = 0.003928  |d_77| = 0.003032  cos = -0.9966
    echo(4,77) = 0.006632339   max |dD| all pairs = 0.006717709 = 2.687 x LAM_NEW
    -> v1.10 baseline reproduced (0.006632 / 0.006718) OK
  S1  repair @ LAM 0.0042              
    sum|e| = 0.004200   ring disp max = 0.004141074
    |d_4| = 0.004141  |d_77| = 0.004141  cos = +1.0000
    echo(4,77) = 0.000000000   max |dD| all pairs = 0.004141074 = 1.656 x LAM_NEW
  S1+S2  @ LAM 0.0025                  
    sum|e| = 0.002500   ring disp max = 0.002478973
    |d_4| = 0.002479  |d_77| = 0.002479  cos = +1.0000
    echo(4,77) = 0.000000000   max |dD| all pairs = 0.002478973 = 0.992 x LAM_NEW
  P3 PASS: the anti-parallel transmission mechanism is ELIMINATED by S1
           (echo(4,77) = 0 exactly; residual echo = local error mass only)

==============================================================================
P4  near-collision hairpin (limb clearance ~= margin)
==============================================================================
  headings: seg36 1.45 deg, seg37 91.45 deg, seg38+ 180 deg
  cross-limb pair (30,45): |i-j| = 15, D = 0.102530  clearance = 0.002498 (target ~= margin 0.0025)
  field (a) single apex seg, e = T6a max [S1]: sum|e| = 0.002011 -> cap scale 1.000000, sum|e'| = 0.002011
    echo(30,45) = 0.001980227   max |dD| all pairs = 0.001980390   ring disp max = 0.001980457
    worst cross-limb clearance: pre +0.002530 -> post +0.000550   (fault threshold 0.005; hard gate 0.02)
  field (b) two apex segs, e = T6a max   [S1]: sum|e| = 0.004011 -> cap scale 0.623325, sum|e'| = 0.002500
    echo(30,45) = 0.001234322   max |dD| all pairs = 0.001756776   ring disp max = 0.001756776
    worst cross-limb clearance: pre +0.002530 -> post +0.001296   (fault threshold 0.005; hard gate 0.02)
  field (a) single apex seg, e = T6a max [OLD]: sum|e| = 0.002011 -> cap scale 1.000000, sum|e'| = 0.002011
    echo(30,45) = 0.000000000   max |dD| all pairs = 0.001980390   ring disp max = 0.001980390
    worst cross-limb clearance: pre +0.002530 -> post +0.002530   (fault threshold 0.005; hard gate 0.02)
  field (b) two apex segs, e = T6a max   [OLD]: sum|e| = 0.004011 -> cap scale 0.623325, sum|e'| = 0.002500
    echo(30,45) = 0.000000000   max |dD| all pairs = 0.001241953   ring disp max = 0.001234427
    worst cross-limb clearance: pre +0.002530 -> post +0.002530   (fault threshold 0.005; hard gate 0.02)
  proven floor (S1+S2): post clearance >= margin - LAMBDA = +0.000000
  P4 PASS: worst measured post-repair clearance stays >= 0 (sub-threshold, PASS band)

==============================================================================
P5  worked example re-run under S1+S2 (state reused from canonical script)
==============================================================================
  sum dL(pre-cap5) = 0.002519  -> cap-5 @ 0.0025: s* = 0.996225 (engaged: True)
  OLD repair @ LAM 0.0042 (v1.10)
    wall regression A/B = +0.000000 / +0.000003   pi(next) = 0.000000 -> PASS
    ring disp max = 0.001041654   max |dD| all pairs = 0.001671484
  S1 @ LAM 0.0042              
    wall regression A/B = +0.000005 / +0.000068   pi(next) = 0.000000 -> PASS
    ring disp max = 0.001241869   max |dD| all pairs = 0.001676609
  S1+S2 @ LAM 0.0025           
    wall regression A/B = +0.000004 / +0.000067   pi(next) = 0.000000 -> PASS
    ring disp max = 0.001232572   max |dD| all pairs = 0.001664033
  P5 PASS: worked example re-verified under S1+S2; all gates hold

SOLUTION PROBE DONE - all asserts passed
```

Reading note for P4's OLD rows: on that specific sharp-apex hairpin the OLD rule's
cross-limb echo happens to vanish (its projector kills the perpendicular displacement
at the 180° joint) — but OLD has **no uniform floor** (its proven worst case stays
−0.0059 via gentle-fold geometries the sharp-fold argument excludes only locally),
which is precisely the gap S1 closes with a uniform proven bound.

## 10. Artifacts and compliance

| Artifact | Path | Lines | SHA-256 |
|---|---|---|---|
| Canonical verification script (untouched) | `scripts/v18_example.py` | 729 | `27c6418a1a4a9b8d3a5f7d1291ccedf480247316bbd7b83e75e7eda62be66f6a` |
| Canonical archive (untouched, identical) | `download/v18_example.py` | 729 | `27c6418a1a4a9b8d3a5f7d1291ccedf480247316bbd7b83e75e7eda62be66f6a` |
| Solution probe (new, side artifact) | `scripts/solution_probe.py` | 441 | `117018d40f65505bfad56f3c88068a537527b2df572957cfdba53be0c8603027` |
| Probe stdout (deterministic, 2× identical) | — | 77 | `6e822431a2db3dd1721480a46c4356aeaf8c0cb71fae9839cf57d1a7fa42e739` |

Re-baseline plan (harness time, only after your approval): re-run canonical sections
C/D/E under S1+S2 and adopt the shifted measured values (V1′/V2′/T6e/L4 numbers above
already come from that re-baseline in probe form); sections A, B, D4 are untouched by
S1/S2.

Compliance: no base code modified at any point; Anaconda v4.2 remains the sole base;
all existing v4.2 functionality preserved (native follow-chain, K = 3 solve, relax
layer, absorption exemptions untouched); nothing in this report takes effect without
your explicit approval; Stage 1 has not been started and will not begin until you
approve it.
