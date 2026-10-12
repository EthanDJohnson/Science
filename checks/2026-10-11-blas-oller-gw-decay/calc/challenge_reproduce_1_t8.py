"""Challenge of Task A (reproduce): an INDEPENDENT covariant route to g g -> gamma gamma.

No spinors, no qft_second_order, no bo_common.  Gravity amplitude from KLT with the manifestly gauge-invariant
4-point Yang-Mills form A(1234) = c t8F^4/(s12 s23):
    M(1 gam,2 gam,3 h,4 h) = C0 * t8F^4(eps1*,eps2*,e3,e4) * t8F^4(e5,e5,e3,e4) / (s12 s23 s24)
photon = (4D vector) x (extra-dimension unit vector e5, i.e. adjoint scalar), graviton eps^{mu nu} = e^mu e^nu.
All momenta outgoing: p1 = q1, p2 = q2, p3 = -k1, p4 = -k2.  Incoming graviton tensors are NOT conjugated,
outgoing photon vectors ARE.  General TT tensors enter bilinearly through H = sum_a h_a e_a e_a.
The single overall constant C0 is fixed at ONE kinematic point so that |M| = 8 pi G u^2/s there (units 8 pi G = 1);
everything else (zeros, shapes, relative phases) is a prediction.
Parts: --part amps | pairs | ring
"""
import argparse, math, sys, time
import numpy as np

PI = math.pi
G5 = np.diag([1.0, -1, -1, -1, -1])


def v5(E, p3):
    out = np.zeros(np.broadcast_shapes(np.shape(E), np.shape(p3)[:-1]) + (5,), dtype=complex)
    out[..., 0] = E
    out[..., 1:4] = p3
    return out


def F(k, e):
    kl = k @ G5
    el = e @ G5
    return np.einsum('...i,...j->...ij', k, el) - np.einsum('...i,...j->...ij', e, kl)


def tr2(A, B):
    return np.einsum('...ij,...ji->...', A, B)


def mm(A, B):
    return np.einsum('...ij,...jk->...ik', A, B)


def t8(F1, F2, F3, F4):
    F12 = mm(F1, F2); F13 = mm(F1, F3)
    four = tr2(F12, mm(F3, F4)) + tr2(F13, mm(F2, F4)) + tr2(F13, mm(F4, F2))
    two = tr2(F1, F2) * tr2(F3, F4) + tr2(F1, F3) * tr2(F2, F4) + tr2(F1, F4) * tr2(F2, F3)
    return 8 * four - 2 * two


def dot(a, b):
    return np.einsum('...i,ij,...j->...', a, G5, b)


def frame(n):
    """polar frame (e_th, e_ph) for unit 3-vectors n (...,3); helicity vectors e_pm = (-+e_th - i e_ph)/sqrt2."""
    n = np.asarray(n, float)
    th = np.arccos(np.clip(n[..., 2], -1, 1)); ph = np.arctan2(n[..., 1], n[..., 0])
    eth = np.stack([np.cos(th) * np.cos(ph), np.cos(th) * np.sin(ph), -np.sin(th)], -1)
    eph = np.stack([-np.sin(ph), np.cos(ph), 0 * ph], -1)
    return eth, eph


def hel_vec(n, lam):
    eth, eph = frame(n)
    return (-lam * eth - 1j * eph) / math.sqrt(2)


E5 = np.zeros(5, complex); E5[4] = 1.0


def raw_amp(q1, q2, k1, k2, ep1, ep2, e3, e4):
    """q's, k's: 5-vectors (physical, positive energy); ep1, ep2 photon vectors (already conjugated); e3, e4 graviton
    vectors (graviton tensors e3 e3, e4 e4).  Returns t8 t8/(s12 s23 s24) without C0."""
    p1, p2, p3, p4 = q1, q2, -k1, -k2
    sh = np.broadcast_shapes(p1.shape, ep1.shape, e3.shape)
    e5 = np.broadcast_to(E5, sh)
    Fa = t8(F(p1, ep1), F(p2, ep2), F(p3, e3), F(p4, e4))
    Fb = t8(F(p1, e5), F(p2, e5), F(p3, e3), F(p4, e4))
    s12 = dot(p1 + p2, p1 + p2); s23 = dot(p2 + p3, p2 + p3); s24 = dot(p2 + p4, p2 + p4)
    return Fa * Fb / (s12 * s23 * s24)


def head_on(theta, phi, w=1.0):
    """gravitons along +-z with energy w; photon 1 at (theta,phi)."""
    n = np.stack([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)], -1)
    z = np.array([0, 0, 1.0])
    k1 = v5(w, w * z); k2 = v5(w, -w * z)
    q1 = v5(w * np.ones(np.shape(theta)), w * n); q2 = v5(w * np.ones(np.shape(theta)), -w * n)
    return k1, k2, q1, q2, n


def e5v(e3):
    out = np.zeros(e3.shape[:-1] + (5,), complex); out[..., 1:4] = e3; return out


def mand(k1, q1, q2):
    s = dot(k1 * 1 + 0, k1) * 0  # placeholder
    return s


C0 = None
SCALAR = False


def calibrate():
    global C0
    th, ph = 1.1, 0.3
    k1, k2, q1, q2, n = head_on(np.array(th), np.array(ph))
    z = np.array([0, 0, 1.0])
    e3 = e5v(hel_vec(z, +1)); e4 = e5v(hel_vec(-z, -1))  # physical helicities +2, -2
    ep1 = e5v(np.conj(hel_vec(n, +1))); ep2 = e5v(np.conj(hel_vec(-n, -1)))
    r = raw_amp(q1, q2, k1, k2, ep1, ep2, e3, e4)
    s = 4.0; u = dot(k1 - q2, k1 - q2).real
    C0 = (u ** 2 / s) / abs(r)
    return C0


def amp_scalar(q1, q2, k1, k2, e3, e4):
    """massless minimally coupled real scalars: KLT (YM+adjoint scalar)^2: C0 t8(e5,e5,e3,e4)^2/(s12 s23 s24).
    Same C0 as photons (the KLT/t8 normalisation is common); checked against |M| = tu/s below."""
    p1, p2, p3, p4 = q1, q2, -k1, -k2
    sh = np.broadcast_shapes(p1.shape, e3.shape)
    e5 = np.broadcast_to(E5, sh)
    Fb = t8(F(p1, e5), F(p2, e5), F(p3, e3), F(p4, e4))
    s12 = dot(p1 + p2, p1 + p2); s23 = dot(p2 + p3, p2 + p3); s24 = dot(p2 + p4, p2 + p4)
    return C0 * Fb * Fb / (s12 * s23 * s24)


def amp(q1, q2, k1, k2, ep1, ep2, e3, e4):
    return C0 * raw_amp(q1, q2, k1, k2, ep1, ep2, e3, e4)


def part_amps():
    print('C0 calibrated at ONE point ((+2,-2)->(+1,-1), theta=1.1, phi=0.3):', calibrate())
    # YM-side sanity: the t8F^4/(s12 s23) gluon amplitude has MHV magnitudes s12^2... check helicity-pattern zeros
    rng = np.random.default_rng(1)
    z = np.array([0, 0, 1.0])
    print('\n(1) head-on, all 16 physical helicity configs; |M|/(8piG) vs t^2/s, u^2/s (t=(k1-q1)^2, u=(k1-q2)^2)')
    worst = 0.0
    for th, ph in [(0.4, 0.2), (1.1, 2.0), (2.3, -1.0), (1.7, 0.9)]:
        k1, k2, q1, q2, n = head_on(np.array(th), np.array(ph))
        t = dot(k1 - q1, k1 - q1).real; u = dot(k1 - q2, k1 - q2).real; s = 4.0
        for l1 in (1, -1):
            for l2 in (1, -1):
                for m1 in (1, -1):
                    for m2 in (1, -1):
                        M = amp(q1, q2, k1, k2, e5v(np.conj(hel_vec(n, m1))), e5v(np.conj(hel_vec(-n, m2))),
                                e5v(hel_vec(z, l1)), e5v(hel_vec(-z, l2)))
                        a = abs(M)
                        if l1 == -l2 and m1 == -m2:
                            pred = u ** 2 / s if (l1 == m1) else t ** 2 / s
                            worst = max(worst, abs(a / pred - 1))
                            tag = 'u^2/s' if l1 == m1 else 't^2/s'
                            print(f'  th={th:.1f} ph={ph:+.1f} (l1,l2,m1,m2)=({2*l1:+d},{2*l2:+d},{m1:+d},{m2:+d}) |M|={a:.10f}  pred {tag}={pred:.10f}')
                        else:
                            worst_zero = a
                            if a > 1e-10:
                                print('  NONZERO forbidden config!', th, ph, l1, l2, m1, m2, a)
    print('  max |ratio-1| over allowed configs:', f'{worst:.2e}', '(all forbidden configs |M| < 1e-10)')
    # random lab kinematics (not head-on): magnitudes against t^2/s, u^2/s and zeros
    print('\n(2) random lab kinematics (boosted pairs): same check')
    worst = 0.0; zmax = 0.0
    for trial in range(200):
        K = rng.uniform(0.05, 1.9) * rng.normal(size=3); K = K / np.linalg.norm(K) * rng.uniform(0.05, 1.9)
        Kh = K / np.linalg.norm(K)
        a = rng.normal(size=3); a -= Kh * (a @ Kh); a /= np.linalg.norm(a)
        kk = math.sqrt(1 - (K @ K) / 4)
        k1v = K / 2 - kk * a; k2v = K / 2 + kk * a
        n = rng.normal(size=3); n /= np.linalg.norm(n)
        Q = np.concatenate([[2.0], K]); ss = 4 - K @ K
        # CM photons along +-n then boost along K
        def boost(p4):
            b = K / 2.0; g = 1 / math.sqrt(1 - b @ b); bp = b @ p4[1:]
            E = g * (p4[0] + bp); p = p4[1:] + ((g - 1) * bp / (b @ b) + g * p4[0]) * b
            return np.concatenate([[E], p])
        q1 = boost(np.concatenate([[math.sqrt(ss) / 2], math.sqrt(ss) / 2 * n]))
        q2 = boost(np.concatenate([[math.sqrt(ss) / 2], -math.sqrt(ss) / 2 * n]))
        k1 = v5(1.0, k1v); k2 = v5(1.0, k2v); Q1 = v5(q1[0], q1[1:]); Q2 = v5(q2[0], q2[1:])
        n1 = q1[1:] / np.linalg.norm(q1[1:]); n2 = q2[1:] / np.linalg.norm(q2[1:])
        t = dot(k1 - Q1, k1 - Q1).real; u = dot(k1 - Q2, k1 - Q2).real; s = dot(k1 + k2, k1 + k2).real
        for l1 in (1, -1):
            for l2 in (1, -1):
                for m1 in (1, -1):
                    for m2 in (1, -1):
                        M = abs(amp(Q1, Q2, k1, k2, e5v(np.conj(hel_vec(n1, m1))), e5v(np.conj(hel_vec(n2, m2))),
                                    e5v(hel_vec(k1v / 1.0, l1)), e5v(hel_vec(k2v, l2))))
                        if l1 == -l2 and m1 == -m2:
                            pred = u ** 2 / s if l1 == m1 else t ** 2 / s
                            worst = max(worst, abs(M / pred - 1))
                        else:
                            zmax = max(zmax, M)
    print(f'  200 random configs: max |ratio-1| (allowed) = {worst:.2e};  max |M| forbidden = {zmax:.2e}')


def part_pairs():
    calibrate()
    print('Per-pair, head-on, s=4 (omega=1): phi-averaged sum over photon helicities of |M|^2/(8piG)^2, integrated dcos')
    z = np.array([0, 0, 1.0])
    x, w = np.polynomial.legendre.leggauss(40)
    nph = 64
    ph = (np.arange(nph) + 0.5) * 2 * PI / nph
    TH, PH = np.meshgrid(np.arccos(x), ph, indexing='ij')
    k1, k2, q1, q2, n = head_on(TH, PH)
    eth, eph = frame(z[None, :])
    ex, ey = np.array([1.0, 0, 0]), np.array([0, 1.0, 0])
    # graviton tensors: lists of (coef, vector) with H = sum c v v; e_pm along +z and -z from my own frame
    ep_z = {l: hel_vec(z, l) for l in (1, -1)}; ep_mz = {l: hel_vec(-z, l) for l in (1, -1)}

    def tens_amp(H1, H2, m1, m2):
        tot = 0
        for c1, v1 in H1:
            for c2, v2 in H2:
                tot = tot + c1 * c2 * amp(q1, q2, k1, k2, e5v(np.conj(hel_vec(n, m1))), e5v(np.conj(hel_vec(-n, m2))),
                                          e5v(np.broadcast_to(v1, n.shape)), e5v(np.broadcast_to(v2, n.shape)))
        return tot

    # linear 'plus' along x for both (lab-fixed axes): xx - yy = (1/2)[(x+iy)(x+iy) + (x-iy)(x-iy)]
    s2 = 1 / math.sqrt(2)
    plus_x = [(0.5, ex + 1j * ey), (0.5, ex - 1j * ey)]  # |H|^2 = 2 (xx-yy); normalise to 1 below
    cross_x = [(-0.5j, ex + 1j * ey), (0.5j, ex - 1j * ey)]  # xy+yx
    R1 = [(1.0, ep_z[1])]; L2 = [(1.0, ep_mz[-1])]; R2 = [(1.0, ep_mz[1])]
    cases = {'plus(x) / plus(x) aligned': (plus_x, plus_x, 0.5), 'plus / cross': (plus_x, cross_x, 0.5),
             'R x L (phys +2,-2)': (R1, L2, 1.0), 'R x R (phys +2,+2)': (R1, R2, 1.0)}
    for name, (H1, H2, norm) in cases.items():
        S = 0
        for m1 in (1, -1):
            for m2 in (1, -1):
                S = S + abs(tens_amp(H1, H2, m1, m2)) ** 2
        S = S * norm  # normalise |H1|^2 |H2|^2 = 1  (xx-yy has |H|^2 = 2 -> factor 1/4; amplitude-squared factor)
        if norm == 0.5:
            S = S / 2.0  # total factor 1/4
        val = np.sum(w * S.mean(axis=1))
        print(f'  {name:28s}: int dcos <sum|M|^2>_phi = {val:.6f}')
    # B&O integrands
    xs, ws = x, w
    t = -2 * (1 - xs); u = -2 * (1 + xs); s = 4
    print(f'  B&O (t^2+u^2)^2/(2 s^2) integrated: {np.sum(ws * (t**2 + u**2)**2 / (2 * s**2)):.6f};'
          f'  (t^4+u^4)/(2s^2): {np.sum(ws * (t**4 + u**4) / (2 * s**2)):.6f};  ratio = {np.sum(ws*(t**4+u**4))/np.sum(ws*(t**2+u**2)**2):.6f} (6/7 = {6/7:.6f})')
    # cross term phi-structure at theta=40 deg for aligned plus/plus
    th = math.radians(40); phs = (np.arange(256)) * 2 * PI / 256
    k1, k2, qq1, qq2, nn = head_on(np.full(256, th), phs)
    tot = 0
    for m1 in (1, -1):
        for m2 in (1, -1):
            A = 0
            for c1, v1 in plus_x:
                for c2, v2 in plus_x:
                    A = A + c1 * c2 * amp(qq1, qq2, k1, k2, e5v(np.conj(hel_vec(nn, m1))), e5v(np.conj(hel_vec(-nn, m2))),
                                          e5v(np.broadcast_to(v1, nn.shape)), e5v(np.broadcast_to(v2, nn.shape)))
            tot = tot + abs(A) ** 2 / 4
    tt = -2 * (1 - math.cos(th)); uu = -2 * (1 + math.cos(th))
    cross = tot - (tt**4 + uu**4) / (2 * 16)
    fc = np.fft.rfft(cross) / 256
    k = np.argmax(np.abs(fc[1:])) + 1
    print(f'  theta=40: cross-term phi-mean {cross.mean():.2e}, dominant harmonic {k} amplitude {2*abs(fc[k]):.6f}, t^2u^2/s^2 = {tt**2*uu**2/16:.6f}')


# ------------------------------------------------------------------ ring / shell integral
def pattern_H(name, n):
    """returns list of (coef(...), vec(...,3)) with H = sum coef vec vec; normalisation applied later."""
    n = np.asarray(n, float)
    eth, eph = frame(n)
    if name == 'bo_plus':   # e_th e_th - e_ph e_ph = (1/2)[(e_th+i e_ph)^2 + (e_th - i e_ph)^2]
        return [(0.5 * np.ones(n.shape[:-1]), eth + 1j * eph), (0.5 * np.ones(n.shape[:-1]), eth - 1j * eph)]
    if name == 'binary':    # Lambda(n)(x+iy)(x+iy): TT projection of v v with v = x+iy -> project v transverse: (P v)(P v) - (1/2) P (v.P v)
        v = np.array([1.0, 1j, 0.0])
        vp = v - n * (n @ v)[..., None]
        # P v P v TT part: (Pv)(Pv) - 1/2 P (Pv.Pv);  write P = e_+ e_-^* ... use helicity projection instead
        hp = np.einsum('...i,...i->...', np.conj(hel_vec(n, 1)), vp) ** 2   # coefficient on e_+ e_+
        hm = np.einsum('...i,...i->...', np.conj(hel_vec(n, -1)), vp) ** 2
        return [(hp, hel_vec(n, 1)), (hm, hel_vec(n, -1))]
    if name == 'linear':
        st2 = 1 - n[..., 2] ** 2
        return [(0.25 * st2, eth + 1j * eph), (0.25 * st2, eth - 1j * eph)]
    raise ValueError


def pattern_norm2(name):
    """int dOmega |H|^2 with |H|^2 = sum |H_ij|^2."""
    x, w = np.polynomial.legendre.leggauss(40); nph = 80
    ph = (np.arange(nph) + 0.5) * 2 * PI / nph
    X, PH = np.meshgrid(x, ph, indexing='ij'); st = np.sqrt(1 - X**2)
    n = np.stack([st * np.cos(PH), st * np.sin(PH), X], -1)
    terms = pattern_H(name, n)
    Hm = sum(c[..., None, None] * np.einsum('...i,...j->...ij', v, v) for c, v in terms)
    return float(np.sum(w[:, None] * np.sum(np.abs(Hm)**2, axis=(-1, -2))) * 2 * PI / nph)


def ring_C(name, NK=8, NthK=8, nth=10, nph=24, na=128, model=False):
    """C in dP/dt = C G^2 N^2 w^3 sigma^2.  C = J/(8192 pi^5), J = int dK dOmega_K dOmega_cm sum_pol |int dalpha m|^2
    with tensors normalised to int dOmega |H|^2 = 8 pi (both helicities populated at Theta, B&O's N).  Patterns are
    axisymmetric about z (rate invariant), so dOmega_K -> 2 pi dcos theta_K."""
    norm = math.sqrt(8 * PI / pattern_norm2(name))
    xK, wK = np.polynomial.legendre.leggauss(NK); Ks = 1 + xK; wK = wK
    xt, wt = np.polynomial.legendre.leggauss(NthK)
    xg, wg = np.polynomial.legendre.leggauss(nth)
    phg = (np.arange(nph) + 0.5) * 2 * PI / nph
    al = (np.arange(na) + 0.5) * 2 * PI / na
    J = 0.0
    for K, wk in zip(Ks, wK):
        s = 4 - K * K; kk = math.sqrt(1 - K * K / 4)
        for ct, wct in zip(xt, wt):
            st = math.sqrt(1 - ct * ct)
            Kh = np.array([st, 0.0, ct])
            e1 = np.array([ct, 0.0, -st]); e2 = np.cross(Kh, e1)
            # photon CM directions n (nth x nph) in frame (e1,e2,Kh); ring alpha
            CG, PG, AL = np.meshgrid(xg, phg, al, indexing='ij')
            SG = np.sqrt(1 - CG**2)
            ncm = (SG * np.cos(PG))[..., None] * e1 + (SG * np.sin(PG))[..., None] * e2 + CG[..., None] * Kh
            a = np.cos(AL)[..., None] * e1 + np.sin(AL)[..., None] * e2
            k1v = K / 2 * Kh - kk * a; k2v = K / 2 * Kh + kk * a
            # boost CM photons along Kh with beta = K/2
            b = K / 2; g = 1 / math.sqrt(1 - b * b); E0 = math.sqrt(s) / 2
            def lab(sign):
                p = sign * E0 * ncm; pl = p @ Kh
                E = g * (E0 + b * pl)
                p3 = p + ((g - 1) * pl + g * b * E0)[..., None] * Kh
                return E, p3
            E1, p1 = lab(1); E2, p2 = lab(-1)
            q1 = v5(E1, p1); q2 = v5(E2, p2); k1 = v5(np.ones(AL.shape), k1v); k2 = v5(np.ones(AL.shape), k2v)
            n1 = p1 / np.linalg.norm(p1, axis=-1)[..., None]; n2 = p2 / np.linalg.norm(p2, axis=-1)[..., None]
            u1 = k1v; u2 = k2v
            T1 = pattern_H(name, u1); T2 = pattern_H(name, u2)
            Ssum = 0.0
            for m1 in (1, -1):
                for m2 in (1, -1):
                    ep1 = e5v(np.conj(hel_vec(n1, m1))); ep2 = e5v(np.conj(hel_vec(n2, m2)))
                    if model:
                        if m1 != m2:
                            continue
                        t = dot(k1 - q1, k1 - q1).real; u = dot(k1 - q2, k1 - q2).real
                        g1 = T1[0][0] * 2 * norm; g2 = T2[0][0] * 2 * norm  # real profile f_+ = f_- = g
                        A = g1 * g2 * (t**2 + u**2) / s
                    else:
                        A = 0
                        for c1, v1 in T1:
                            for c2, v2 in T2:
                                A = A + c1 * c2 * norm**2 * amp(q1, q2, k1, k2, ep1, ep2, e5v(v1), e5v(v2))
                    I = A.mean(axis=-1) * 2 * PI
                    Ssum = Ssum + np.abs(I)**2
            ang = np.sum(wg[:, None] * Ssum) * 2 * PI / nph
            J += wk * wct * 2 * PI * ang
    return J / (8192 * PI**5)


def part_ring(args):
    calibrate()
    ref = 3 / (25 * PI)
    grids = [dict(NK=6, NthK=6, nth=8, nph=20, na=96), dict(NK=8, NthK=8, nth=10, nph=24, na=160)]
    if args.grid is not None:
        grids = [grids[args.grid]]
    for gr in grids:
        t0 = time.time()
        Cm = ring_C('bo_plus', model=True, **gr)
        print(f'grid {gr}: B&O-model isotropic C/(3/(25pi)) = {Cm/ref:.6f}  [{time.time()-t0:.0f}s]')
        for name in args.patterns.split(','):
            t0 = time.time()
            C = ring_C(name, **gr)
            extra = ''
            if name == 'linear':
                Cl = ring_C('linear', model=True, **gr)
                extra = f';  B&O model same profile C/ref = {Cl/ref:.6f}, phys/model = {C/Cl:.5f}'
            print(f'   {name:8s}: C = {C:.8f}  C/(3/(25pi)) = {C/ref:.6f}{extra}  [{time.time()-t0:.0f}s]')
        sys.stdout.flush()


def part_K0():
    """K -> 0 limit: ring = great circle perp to Khat, CM = lab; ratio physical/model of the K-integrand for bo_plus."""
    calibrate()
    for Kv in (0.02, 0.05):
        for name in ('bo_plus',):
            r = []
            for gr in (dict(NK=1, NthK=8, nth=12, nph=32, na=256),):
                pass
        # direct evaluation of the K-integrand: reuse ring_C with a single K node by monkeypatching
    print('see part ring (K-resolved not implemented here)')



# ------------------------------------------------------------------ faster ring: helicity projection, nonzero channels only
def hproj(name, n):
    """helicity components h_a(n) = conj(e_a) . H . conj(e_a), a = +-1 (my own e_a convention)."""
    out = {}
    for a in (1, -1):
        ea = np.conj(hel_vec(n, a))
        out[a] = sum(c * np.einsum('...i,...i->...', ea, v) ** 2 for c, v in pattern_H(name, n))
    return out


def cgrid(nth):
    """photon CM polar grid: Gauss-Legendre on [-1,0] and [0,1] separately, each graded towards c = 0 by c = sgn y^2
    (the integrand has its collinear structure at c = 0, where the photon can be parallel to a ring graviton)."""
    y, wy = np.polynomial.legendre.leggauss(nth)
    y = (y + 1) / 2; wy = wy / 2          # on (0,1)
    c = y ** 2; wc = 2 * y * wy
    return np.concatenate([-c[::-1], c]), np.concatenate([wc[::-1], wc])


def _node(args):
    global SCALAR
    name, K, ct, nth, nph, na, model, norm, SCALAR = args if len(args) == 9 else (*args, False)
    calibrate()
    s = 4 - K * K; kk = math.sqrt(1 - K * K / 4)
    st = math.sqrt(1 - ct * ct)
    Kh = np.array([st, 0.0, ct]); e1 = np.array([ct, 0.0, -st]); e2 = np.cross(Kh, e1)
    xg, wg = cgrid(nth)
    phg = (np.arange(nph) + 0.5) * 2 * PI / nph
    al = (np.arange(na) + 0.5) * 2 * PI / na
    CG, PG, AL = np.meshgrid(xg, phg, al, indexing='ij')
    SG = np.sqrt(1 - CG ** 2)
    ncm = (SG * np.cos(PG))[..., None] * e1 + (SG * np.sin(PG))[..., None] * e2 + CG[..., None] * Kh
    a = np.cos(AL)[..., None] * e1 + np.sin(AL)[..., None] * e2
    k1v = K / 2 * Kh - kk * a; k2v = K / 2 * Kh + kk * a
    b = K / 2; g = 1 / math.sqrt(1 - b * b); E0 = math.sqrt(s) / 2

    def lab(sign):
        p = sign * E0 * ncm; pl = p @ Kh
        return g * (E0 + b * pl), p + ((g - 1) * pl + g * b * E0)[..., None] * Kh
    E1, p1 = lab(1); E2, p2 = lab(-1)
    q1 = v5(E1, p1); q2 = v5(E2, p2); k1 = v5(np.ones(AL.shape), k1v); k2 = v5(np.ones(AL.shape), k2v)
    n1 = p1 / np.linalg.norm(p1, axis=-1)[..., None]; n2 = p2 / np.linalg.norm(p2, axis=-1)[..., None]
    h1 = hproj(name, k1v); h2 = hproj(name, k2v)
    S = 0.0
    if SCALAR:
        if model:
            t = dot(k1 - q1, k1 - q1).real; u = dot(k1 - q2, k1 - q2).real
            gg = np.real(h1[1]) * np.real(h2[1]) * norm ** 2
            I = (gg * (-2 * t * u / s)).mean(-1) * 2 * PI
        else:
            A = 0
            for l in (1, -1):
                A = A + h1[l] * h2[-l] * norm ** 2 * amp_scalar(q1, q2, k1, k2, e5v(hel_vec(k1v, l)), e5v(hel_vec(k2v, -l)))
            I = A.mean(-1) * 2 * PI
        return float(np.sum(wg[:, None] * np.abs(I) ** 2) * 2 * PI / nph)
    if model:
        t = dot(k1 - q1, k1 - q1).real; u = dot(k1 - q2, k1 - q2).real
        gg = np.real(h1[1]) * np.real(h2[1]) * norm ** 2   # real profile f+ = f- (e_+ e_+ coefficient)
        I = (gg * (t ** 2 + u ** 2) / s).mean(-1) * 2 * PI
        S = 2 * np.abs(I) ** 2
    else:
        for m in (1, -1):
            ep1 = e5v(np.conj(hel_vec(n1, m))); ep2 = e5v(np.conj(hel_vec(n2, -m)))
            A = 0
            for l in (1, -1):
                A = A + h1[l] * h2[-l] * norm ** 2 * amp(q1, q2, k1, k2, ep1, ep2, e5v(hel_vec(k1v, l)), e5v(hel_vec(k2v, -l)))
            I = A.mean(-1) * 2 * PI
            S = S + np.abs(I) ** 2
    return float(np.sum(wg[:, None] * S) * 2 * PI / nph)


def ring_C2(name, NK, NthK, nth, nph, na, model=False, pool=None, scalar=False):
    norm = math.sqrt(8 * PI / pattern_norm2(name))
    xK, wK = np.polynomial.legendre.leggauss(NK); Ks = 1 + xK
    xt, wt = np.polynomial.legendre.leggauss(NthK)
    jobs = [(name, float(K), float(ct), nth, nph, na, model, norm, scalar) for K in Ks for ct in xt]
    vals = (pool.map(_node, jobs) if pool else list(map(_node, jobs)))
    vals = np.array(vals).reshape(NK, NthK)
    dJ = 2 * PI * (vals * wt[None, :]).sum(1)          # per K node
    C = float((wK * dJ).sum()) / (8192 * PI ** 5)
    return C, Ks, dJ


def part_ring2(args):
    import multiprocessing as mp
    ref = 3 / (25 * PI)
    gr = dict(NK=args.NK, NthK=args.NthK, nth=args.nth, nph=args.nph, na=args.na)
    with mp.Pool(4) as pool:
        t0 = time.time()
        Cm, Ks, dJm = ring_C2('bo_plus', model=True, pool=pool, **gr)
        print(f'grid {gr}: B&O-model isotropic C/(3/(25pi)) = {Cm/ref:.6f}  [{time.time()-t0:.0f}s]', flush=True)
        for name in args.patterns.split(','):
            t0 = time.time()
            C, Ks, dJ = ring_C2(name, pool=pool, **gr)
            line = f'   {name:8s}: C = {C:.8f}  C/(3/(25pi)) = {C/ref:.6f}'
            if name == 'linear':
                Cl, _, _ = ring_C2('linear', model=True, pool=pool, **gr)
                line += f';  B&O model same profile C/ref = {Cl/ref:.6f}, phys/model = {C/Cl:.5f}'
            if name == 'bo_plus':
                line += '\n      K-resolved phys/model: ' + ', '.join(f'K={k:.3f}:{r:.4f}' for k, r in zip(Ks, dJ / dJm))
            print(line + f'  [{time.time()-t0:.0f}s]', flush=True)


def part_invariant():
    """Rephasing invariant I = M_a(+2,-2->+1,-1) M_a(+2,-2->-1,+1)^* M_a'(+2,-2->-1,+1) M_a'(+2,-2->+1,-1)^*
    for two head-on graviton axes a, a' (same K = 0) and fixed photons.  Real positive eq.-6 amplitudes => arg I = 0."""
    calibrate()
    def M(axis, n, m):
        axis = axis / np.linalg.norm(axis)
        k1 = v5(1.0, axis); k2 = v5(1.0, -axis); q1 = v5(1.0, n); q2 = v5(1.0, -n)
        return complex(amp(q1, q2, k1, k2, e5v(np.conj(hel_vec(n, m))), e5v(np.conj(hel_vec(-n, -m))),
                           e5v(hel_vec(axis, 1)), e5v(hel_vec(-axis, -1))))
    for thp, php in [(60, 17), (100, 200), (35, 290)]:
        n = np.array([math.sin(math.radians(thp)) * math.cos(math.radians(php)),
                      math.sin(math.radians(thp)) * math.sin(math.radians(php)), math.cos(math.radians(thp))])
        a = np.array([0, 0, 1.0])
        out = []
        for tilt in (30, 60, 90):
            ap_ = np.array([math.sin(math.radians(tilt)), 0, math.cos(math.radians(tilt))])
            I = M(a, n, 1) * np.conj(M(a, n, -1)) * M(ap_, n, -1) * np.conj(M(ap_, n, 1))
            out.append(f'tilt {tilt}: arg I = {math.degrees(np.angle(I)):+.2f} deg')
        # rephasing test: same invariant with a different photon-frame convention (rotate e_th,e_ph by 0.7 rad)
        print(f'photons at ({thp},{php}) deg: ' + '; '.join(out))


def part_scalar(a):
    import multiprocessing as mp
    calibrate()
    # amplitude check: head-on, physical helicities
    z = np.array([0, 0, 1.0]); worst = 0; zmax = 0
    for th, ph in [(0.4, 0.2), (1.1, 2.0), (2.3, -1.0)]:
        k1, k2, q1, q2, n = head_on(np.array(th), np.array(ph))
        t = dot(k1 - q1, k1 - q1).real; u = dot(k1 - q2, k1 - q2).real
        for l1 in (1, -1):
            for l2 in (1, -1):
                M = abs(amp_scalar(q1, q2, k1, k2, e5v(hel_vec(z, l1)), e5v(hel_vec(-z, l2))))
                if l1 == -l2: worst = max(worst, abs(M / (t * u / 4) - 1))
                else: zmax = max(zmax, M)
    print(f'massless scalar: |M(+2,-2)|/(8piG) vs tu/s: max |ratio-1| = {worst:.2e}; same helicity max |M| = {zmax:.2e}'
          ' (= S10 at m = 0: A+- -> -8piG tu/s, A++ -> 0, labels = physical helicities)')
    ref = 7 / (450 * PI)
    gr = dict(NK=a.NK, NthK=a.NthK, nth=a.nth, nph=a.nph, na=a.na)
    with mp.Pool(4) as pool:
        Cm, _, _ = ring_C2('bo_plus', model=True, pool=pool, scalar=True, **gr)
        print(f'grid {gr}: B&O-model isotropic scalar C/(7/(450pi)) = {Cm/ref:.6f}', flush=True)
        for name in a.patterns.split(','):
            C, _, _ = ring_C2(name, pool=pool, scalar=True, **gr)
            line = f'   {name:8s}: C = {C:.6e}  C/(7/(450pi)) = {C/ref:.6f}'
            if name == 'linear':
                Cl, _, _ = ring_C2('linear', model=True, pool=pool, scalar=True, **gr)
                line += f';  B&O model same profile {Cl/ref:.6f}'
            print(line, flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', default='amps')
    ap.add_argument('--grid', type=int, default=None)
    ap.add_argument('--patterns', default='bo_plus,binary,linear')
    for k, v in dict(NK=6, NthK=6, nth=8, nph=20, na=256).items():
        ap.add_argument('--' + k, type=int, default=v)
    a = ap.parse_args()
    if a.part == 'amps': part_amps()
    elif a.part == 'pairs': part_pairs()
    elif a.part == 'ring': part_ring(a)
    elif a.part == 'ring2': part_ring2(a)
    elif a.part == 'invariant': part_invariant()
    elif a.part == 'scalar': part_scalar(a)

