# !/usr/bin/env python3

"""
Thixotropic structure kinetics for the Gali-Spinal outer annulus.

Stress:   tau = lam *tau_y0 + [K_inf + lam* (K0 - K_inf)] *gamma_dot**n
Kinetics: dlam/dt = k_plus * (1 - lam) - k_minus * gamma_dot**m* lam

lambda = 1  fully built plug
lambda = 0  fully broken
"""

from **future** import annotations

from dataclasses import dataclass

import numpy as np

@dataclass
class HBThixParams:
    tau_y0: float = 80.0      # static yield at lambda=1  [Pa]
    K0: float = 2.0           # consistency, built        [Pa s^n]
    K_inf: float = 0.3        # consistency, broken       [Pa s^n]
    n: float = 0.7            # flow index  (-)
    k_plus: float = 150.0     # rebuild rate              [1/s]
    k_minus: float = 0.02     # break coefficient         [s^{m-1}]
    m: float = 1.0            # shear-break exponent      (-)
    lam_min: float = 1e-4
    lam_max: float = 1.0

def apparent_viscosity(lam: float, gdot: float, p: HBThixParams) -> float:
    g = max(abs(gdot), 1e-12)
    tau = yield_stress(lam, p) + consistency(lam, p) * g**p.n
    return tau / g

def yield_stress(lam: float, p: HBThixParams) -> float:
    return lam * p.tau_y0

def consistency(lam: float, p: HBThixParams) -> float:
    return p.K_inf + lam * (p.K0 - p.K_inf)

def shear_stress(lam: float, gdot: float, p: HBThixParams) -> float:
    g = abs(gdot)
    return yield_stress(lam, p) + consistency(lam, p) * (g ** p.n)

def dlam_dt(lam: float, gdot: float, p: HBThixParams) -> float:
    build = p.k_plus *(1.0 - lam)
    break_= p.k_minus* (abs(gdot) ** p.m) * lam
    return build - break_

def lam_steady(gdot: float, p: HBThixParams) -> float:
    km = p.k_minus * (abs(gdot) ** p.m)
    den = p.k_plus + km
    if den <= 0.0:
        return p.lam_max
    return float(np.clip(p.k_plus / den, p.lam_min, p.lam_max))

# !/usr/bin/env python3

"""Adaptive-step thixotropic cycle (embedded Heun / RK2)."""

from **future** import annotations

from dataclasses import dataclass

import numpy as np

from thixotropic_kinetics import (  # or paste the earlier dataclasses in this file
    CycleSpec,
    HBThixParams,
    dlam_dt,
    gdot_schedule,
    shear_stress,
    wait_time,
)

@dataclass
class AdaptSpec:
    dt_min: float = 2e-7
    dt_max: float = 2e-4
    atol: float = 1e-4
    rtol: float = 1e-3
    safety: float = 0.8
    max_grow: float = 2.0
    max_shrink: float = 0.25
    snap_guard: float = 0.25   # max fraction of snap duration per step

def _heun_step(lam: float, gdot: float, dt: float, p: HBThixParams):
    """One Heun step. Returns (lam_heun, lam_euler, err)."""
    k1 = dlam_dt(lam, gdot, p)
    lam_e = lam + dt *k1
    k2 = dlam_dt(lam_e, gdot, p)
    lam_h = lam + 0.5* dt * (k1 + k2)
    lam_h = float(np.clip(lam_h, p.lam_min, p.lam_max))
    lam_e = float(np.clip(lam_e, p.lam_min, p.lam_max))
    err = abs(lam_h - lam_e)
    return lam_h, lam_e, err

def _next_snap_edge(t: float, spec: CycleSpec) -> tuple[float, float]:
    """Return (t_on, t_off) of the current or next snap pulse."""
    period = wait_time(spec)
    k = np.floor(t / period)
    t_on = k *period
    t_off = t_on + spec.snap_duration_s
    if t >= t_off - 1e-15:
        t_on = (k + 1)* period
        t_off = t_on + spec.snap_duration_s
    return t_on, t_off

def _limit_dt(t: float, dt: float, spec: CycleSpec, a: AdaptSpec) -> float:
    t_on, t_off = _next_snap_edge(t, spec)
    # do not step over a snap rising/falling edge
    for edge in (t_on, t_off):
        if edge > t + 1e-16:
            dt = min(dt, edge - t)
    dt = min(dt, a.snap_guard * spec.snap_duration_s)
    return float(np.clip(dt, a.dt_min, a.dt_max))

def run_cycle_adaptive(
    p: HBThixParams | None = None,
    spec: CycleSpec | None = None,
    adapt: AdaptSpec | None = None,
    lam0: float = 1.0,
) -> dict:
    p = p or HBThixParams()
    spec = spec or CycleSpec()
    a = adapt or AdaptSpec()

    t = 0.0
    lam = float(np.clip(lam0, p.lam_min, p.lam_max))
    dt = min(a.dt_max, 0.1 / max(p.k_plus, 1.0))

    ts, lams, gdots, taus, dts = [], [], [], [], []

    rejected = 0
    accepted = 0

    while t < spec.t_end - 1e-16:
        dt = _limit_dt(t, dt, spec, a)
        if t + dt > spec.t_end:
            dt = spec.t_end - t

        g = gdot_schedule(t + 0.5 * dt, spec)  # mid-step rate
        lam_h, _, err = _heun_step(lam, g, dt, p)

        scale = a.atol + a.rtol * max(abs(lam), abs(lam_h))
        rel = err / max(scale, 1e-16)

        if rel > 1.0 and dt > a.dt_min * 1.01:
            dt = max(a.dt_min, dt * a.safety * rel ** -0.5)
            dt = max(dt, a.max_shrink * dt / max(a.safety * rel ** -0.5, 1e-12))
            # simpler shrink:
            dt = max(a.dt_min, dt * max(a.max_shrink, a.safety / np.sqrt(rel)))
            rejected += 1
            continue

        # accept
        lam = lam_h
        t = t + dt
        accepted += 1

        ts.append(t)
        lams.append(lam)
        gdots.append(g)
        taus.append(shear_stress(lam, g, p))
        dts.append(dt)

        # grow dt
        if rel < 0.2:
            grow = a.max_grow
        else:
            grow = min(a.max_grow, a.safety * rel ** -0.5)
        dt = min(a.dt_max, dt * max(1.0, grow))

    ts = np.array(ts)
    lams = np.array(lams)
    gdots = np.array(gdots)
    taus = np.array(taus)
    power = taus * np.abs(gdots)

    tw = wait_time(spec)
    t_build = 1.0 / max(p.k_plus, 1e-12)
    break_figure = p.k_minus * (spec.snap_gdot ** p.m) * spec.snap_duration_s

    return {
        "t": ts,
        "lam": lams,
        "gdot": gdots,
        "tau": taus,
        "dt": np.array(dts),
        "power_density": power,
        "t_wait": tw,
        "t_build": t_build,
        "break_figure": break_figure,
        "rebuild_ok": t_build <= tw,
        "lam_end": float(lams[-1]),
        "mean_power": float(np.mean(power)),
        "accepted": accepted,
        "rejected": rejected,
        "params": p,
        "spec": spec,
    }

if **name** == "**main**":
    out = run_cycle_adaptive()
    print(
        f"steps={out['accepted']} rejected={out['rejected']} "
        f"dt[{out['dt'].min():.2e}, {out['dt'].max():.2e}] "
        f"t_wait={out['t_wait']*1e3:.2f} ms t_build={out['t_build']*1e3:.2f} ms "
        f"rebuild_ok={out['rebuild_ok']} break={out['break_figure']:.2f} "
        f"lam_end={out['lam_end']:.3f}"
    )

# ---------------------------------------------------------------------------

# Snap / rebuild cycle

# ---------------------------------------------------------------------------

@dataclass
class CycleSpec:
    rpm: float = 3600.0
    snaps_per_rev: int = 2
    snap_duration_s: float = 0.001
    snap_gdot: float = 800.0      # 1/s during snap
    coast_gdot: float = 5.0       # 1/s in the plug / dwell
    t_end: float = 0.05
    dt: float = 2e-5

def wait_time(spec: CycleSpec) -> float:
    f = spec.rpm / 60.0
    return 1.0 / max(spec.snaps_per_rev * f, 1e-12)

def gdot_schedule(t: float, spec: CycleSpec) -> float:
    """Square-pulse snaps, otherwise coast shear."""
    period = wait_time(spec)
    phase = t % period
    if phase < spec.snap_duration_s:
        return spec.snap_gdot
    return spec.coast_gdot

def run_cycle(
    p: HBThixParams | None = None,
    spec: CycleSpec | None = None,
    lam0: float = 1.0,
) -> dict:
    p = p or HBThixParams()
    spec = spec or CycleSpec()

    nstep = int(spec.t_end / spec.dt) + 1
    t = np.linspace(0.0, spec.t_end, nstep)
    lam = np.empty(nstep)
    gdot = np.empty(nstep)
    tau = np.empty(nstep)
    power = np.empty(nstep)  # Pa/s == W/m^3

    lam[0] = float(np.clip(lam0, p.lam_min, p.lam_max))
    gdot[0] = gdot_schedule(0.0, spec)
    tau[0] = shear_stress(lam[0], gdot[0], p)
    power[0] = tau[0] * abs(gdot[0])

    for i in range(1, nstep):
        g = gdot_schedule(t[i], spec)
        lam[i] = step_euler(lam[i - 1], g, spec.dt, p)
        gdot[i] = g
        tau[i] = shear_stress(lam[i], g, p)
        power[i] = tau[i] * abs(g)

    tw = wait_time(spec)
    rebuild_needed = 1.0 / max(p.k_plus, 1e-12)
    break_figure = p.k_minus * (spec.snap_gdot ** p.m) * spec.snap_duration_s

    return {
        "t": t,
        "lam": lam,
        "gdot": gdot,
        "tau": tau,
        "power_density": power,
        "t_wait": tw,
        "t_build": rebuild_needed,
        "break_figure": break_figure,   # ~2 or more => snap actually breaks
        "rebuild_ok": rebuild_needed <= tw,
        "lam_end": float(lam[-1]),
        "mean_power": float(np.mean(power)),
        "params": p,
        "spec": spec,
    }

# ---------------------------------------------------------------------------

# Fit helpers from bench traces  tau(t) at known gdot

# ---------------------------------------------------------------------------

def fit_k_plus_from_rebuild(t: np.ndarray, tau: np.ndarray) -> float:
    """
    tau(t) = tau_inf - (tau_inf - tau0) * exp(-k+ t)
    Use first/last samples; skip if the rise is too small.
    """
    t = np.asarray(t, dtype=float)
    tau = np.asarray(tau, dtype=float)
    tau0, tau_inf = tau[0], tau[-1]
    amp = tau_inf - tau0
    if amp <= 1e-9:
        return np.nan
    y = np.clip((tau_inf - tau) / amp, 1e-8, 1.0)
    # ln(y) = -k+ t
    A = t[:, None]
    k = float(-np.linalg.lstsq(A, np.log(y), rcond=None)[0][0])
    return max(k, 0.0)

def fit_k_minus_from_break(
    t: np.ndarray,
    tau: np.ndarray,
    gdot: float,
    k_plus: float,
) -> float:
    """
    At constant high gdot:
      lam -> lam_inf + (lam0 - lam_inf) exp(-(k+ + k- gdot^m) t)
    Approximate decay rate of tau as that exponent (m=1).
    """
    t = np.asarray(t, dtype=float)
    tau = np.asarray(tau, dtype=float)
    tau0, tau_inf = tau[0], tau[-1]
    amp = tau0 - tau_inf
    if amp <= 1e-9 or gdot <= 0.0:
        return np.nan
    y = np.clip((tau - tau_inf) / amp, 1e-8, 1.0)
    rate = float(-np.linalg.lstsq(t[:, None], np.log(y), rcond=None)[0][0])
    return max((rate - k_plus) / gdot, 0.0)

def print_report(out: dict) -> None:
    p: HBThixParams = out["params"]
    spec: CycleSpec = out["spec"]
    print("=== Thixotropic snap cycle ===")
    print(f"RPM {spec.rpm:.0f} | snaps/rev {spec.snaps_per_rev} | "
          f"t_wait {out['t_wait']*1e3:.2f} ms | t_build {out['t_build']*1e3:.2f} ms")
    print(f"rebuild_ok={out['rebuild_ok']}  break_figure={out['break_figure']:.2f} "
          f"(want >= ~2)")
    print(f"lambda: start=1 target, end={out['lam_end']:.3f}")
    print(f"mean dissipation {out['mean_power']:.1f} W/m^3")
    print(f"k+={p.k_plus:.1f} 1/s   k-={p.k_minus:.4f}   n={p.n}")

if **name** == "**main**":
    out = run_cycle()
    print_report(out)

    # Optional plot if matplotlib is present
    try:
        import matplotlib.pyplot as plt

        t, lam, tau, g = out["t"], out["lam"], out["tau"], out["gdot"]
        fig, ax = plt.subplots(3, 1, figsize=(8, 7), sharex=True)
        ax[0].plot(t * 1e3, g)
        ax[0].set_ylabel(r"$\dot{\gamma}$ (1/s)")
        ax[1].plot(t * 1e3, lam)
        ax[1].set_ylabel(r"$\lambda$")
        ax[1].set_ylim(0, 1.05)
        ax[2].plot(t * 1e3, tau)
        ax[2].set_ylabel(r"$\tau$ (Pa)")
        ax[2].set_xlabel("time (ms)")
        fig.tight_layout()
        fig.savefig("thixotropic_cycle.png", dpi=140)
        print("Wrote thixotropic_cycle.png")
    except Exception as exc:
        print("Plot skipped:", exc)
