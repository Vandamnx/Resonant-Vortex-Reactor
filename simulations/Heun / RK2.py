#!/usr/bin/env python3
"""Adaptive-step thixotropic cycle (embedded Heun / RK2)."""

from __future__ import annotations

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
    lam_e = lam + dt * k1
    k2 = dlam_dt(lam_e, gdot, p)
    lam_h = lam + 0.5 * dt * (k1 + k2)
    lam_h = float(np.clip(lam_h, p.lam_min, p.lam_max))
    lam_e = float(np.clip(lam_e, p.lam_min, p.lam_max))
    err = abs(lam_h - lam_e)
    return lam_h, lam_e, err


def _next_snap_edge(t: float, spec: CycleSpec) -> tuple[float, float]:
    """Return (t_on, t_off) of the current or next snap pulse."""
    period = wait_time(spec)
    k = np.floor(t / period)
    t_on = k * period
    t_off = t_on + spec.snap_duration_s
    if t >= t_off - 1e-15:
        t_on = (k + 1) * period
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


if __name__ == "__main__":
    out = run_cycle_adaptive()
    print(
        f"steps={out['accepted']} rejected={out['rejected']} "
        f"dt[{out['dt'].min():.2e}, {out['dt'].max():.2e}] "
        f"t_wait={out['t_wait']*1e3:.2f} ms t_build={out['t_build']*1e3:.2f} ms "
        f"rebuild_ok={out['rebuild_ok']} break={out['break_figure']:.2f} "
        f"lam_end={out['lam_end']:.3f}"
    )