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
