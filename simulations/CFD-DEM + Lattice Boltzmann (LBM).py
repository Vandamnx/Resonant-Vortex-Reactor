#!/usr/bin/env python3
"""
Gali-Spinal Tube – CFD-DEM + Lattice Boltzmann (LBM) Simulation
Clean combined module for magnetite sphere chain in a conducting fluid.

Features:
- D3Q19 Lattice Boltzmann fluid solver
- Discrete Element Method (DEM) for magnetite spheres
- Magnetic dipole–dipole forces
- Soft-sphere contact forces
- Stokes / simple drag
- Two-way momentum coupling
- Soft cylindrical wall
- Optional axial + rotational (whip) drive
"""

import numpy as np
from dataclasses import dataclass
from typing import List
import time

# ============================================================
# Simulation Parameters
# ============================================================
NX, NY, NZ = 32, 32, 64          # lattice size
TAU = 0.78                       # LBM relaxation time
DT_DEM = 3.0e-5                  # DEM time step
N_PARTICLES = 16
RADIUS = 1.2
RHO_PARTICLE = 5.3
MAG_STRENGTH = 28.0              # magnetic moment magnitude
STEPS = 1200
OUTPUT_EVERY = 200

AXIAL_DRIVE = 0.18               # body force along tube axis
ROT_DRIVE = 0.09                 # rotational / whip drive strength
SNAP_STEPS = [600]               # steps at which a collective snap occurs
SNAP_STRENGTH = 0.6

# ============================================================
# D3Q19 Lattice
# ============================================================
C = np.array([
    [0, 0, 0],
    [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1],
    [1, 1, 0], [-1, -1, 0], [1, -1, 0], [-1, 1, 0],
    [1, 0, 1], [-1, 0, -1], [1, 0, -1], [-1, 0, 1],
    [0, 1, 1], [0, -1, -1], [0, 1, -1], [0, -1, 1]
], dtype=np.float64)

W = np.array([1/3] + [1/18]*6 + [1/36]*12)
CS2 = 1.0 / 3.0

# ============================================================
# Particle data structure
# ============================================================
@dataclass
class Particle:
    pos: np.ndarray
    vel: np.ndarray
    radius: float
    mass: float
    mag: np.ndarray          # magnetic moment vector

# ============================================================
# LBM core
# ============================================================
def equilibrium(rho: np.ndarray, ux: np.ndarray, uy: np.ndarray, uz: np.ndarray) -> np.ndarray:
    feq = np.zeros(rho.shape + (19,))
    usq = ux**2 + uy**2 + uz**2
    for i in range(19):
        cu = C[i, 0]*ux + C[i, 1]*uy + C[i, 2]*uz
        feq[..., i] = W[i] * rho * (1.0 + cu/CS2 + 0.5*(cu/CS2)**2 - 0.5*usq/CS2)
    return feq


def lbm_step(f: np.ndarray, force: np.ndarray = None):
    """One full LBM collide-stream step with optional body force."""
    rho = np.sum(f, axis=-1)
    ux = np.sum(f * C[:, 0], axis=-1) / rho
    uy = np.sum(f * C[:, 1], axis=-1) / rho
    uz = np.sum(f * C[:, 2], axis=-1) / rho

    if force is not None:
        ux += force[..., 0] / (2.0 * rho)
        uy += force[..., 1] / (2.0 * rho)
        uz += force[..., 2] / (2.0 * rho)

    feq = equilibrium(rho, ux, uy, uz)
    f_col = f - (f - feq) / TAU

    f_new = np.zeros_like(f)
    for i in range(19):
        cx, cy, cz = C[i].astype(int)
        f_new[..., i] = np.roll(np.roll(np.roll(f_col[..., i], cx, axis=0), cy, axis=1), cz, axis=2)

    return f_new, rho, ux, uy, uz

# ============================================================
# DEM forces
# ============================================================
def magnetic_dipole_force(p1: Particle, p2: Particle, mu0: float = 1.0) -> np.ndarray:
    r_vec = p2.pos - p1.pos
    r = np.linalg.norm(r_vec) + 1e-9
    r_hat = r_vec / r
    m1, m2 = p1.mag, p2.mag
    return (3 * mu0 / (4 * np.pi * r**4)) * (
        np.dot(m1, m2) * r_hat
        + np.dot(m1, r_hat) * m2
        + np.dot(m2, r_hat) * m1
        - 5 * np.dot(m1, r_hat) * np.dot(m2, r_hat) * r_hat
    )


def contact_force(p1: Particle, p2: Particle, kn: float = 400.0, gamma: float = 10.0) -> np.ndarray:
    r_vec = p2.pos - p1.pos
    dist = np.linalg.norm(r_vec) + 1e-12
    overlap = p1.radius + p2.radius - dist
    if overlap <= 0.0:
        return np.zeros(3)
    r_hat = r_vec / dist
    v_rel = np.dot(p2.vel - p1.vel, r_hat)
    return (kn * overlap - gamma * v_rel) * r_hat


def stokes_drag(p: Particle, u_fluid: np.ndarray, eta: float = 0.08) -> np.ndarray:
    return 6.0 * np.pi * eta * p.radius * (u_fluid - p.vel)

# ============================================================
# Helpers
# ============================================================
def sample_velocity(ux, uy, uz, pos):
    ix = int(np.clip(pos[0], 0, NX - 1))
    iy = int(np.clip(pos[1], 0, NY - 1))
    iz = int(np.clip(pos[2], 0, NZ - 1))
    return np.array([ux[ix, iy, iz], uy[ix, iy, iz], uz[ix, iy, iz]])


def create_particles() -> List[Particle]:
    particles = []
    for i in range(N_PARTICLES):
        pos = np.array([
            NX / 2 + np.random.uniform(-1.2, 1.2),
            NY / 2 + np.random.uniform(-1.2, 1.2),
            5.0 + i * (2 * RADIUS + 0.3)
        ])
        vel = np.random.uniform(-0.01, 0.01, 3)
        mass = (4.0 / 3.0) * np.pi * RADIUS**3 * RHO_PARTICLE
        mag = np.array([0.0, 0.0, MAG_STRENGTH])
        particles.append(Particle(pos, vel, RADIUS, mass, mag))
    return particles

# ============================================================
# Main simulation
# ============================================================
def run_simulation():
    print("=" * 64)
    print("Gali-Spinal Tube  |  CFD-DEM + LBM")
    print("=" * 64)
    print(f"Particles : {N_PARTICLES}")
    print(f"Lattice   : {NX} × {NY} × {NZ}")
    print(f"MAG       : {MAG_STRENGTH}")
    print(f"ROT drive : {ROT_DRIVE}")
    print()

    # Initialise fluid at rest
    f = np.zeros((NX, NY, NZ, 19))
    for i in range(19):
        f[..., i] = W[i] * 1.0

    particles = create_particles()
    ux = uy = uz = np.zeros((NX, NY, NZ))

    start = time.time()

    for step in range(STEPS):
        forces = [np.zeros(3) for _ in particles]
        force_on_fluid = np.zeros((NX, NY, NZ, 3))

        # --- Magnetic + contact forces ---
        for i in range(N_PARTICLES):
            for j in range(i + 1, N_PARTICLES):
                fm = magnetic_dipole_force(particles[i], particles[j])
                fc = contact_force(particles[i], particles[j])
                forces[i] += fm + fc
                forces[j] -= fm + fc

        # --- Fluid drag + drives ---
        for i, p in enumerate(particles):
            u_f = sample_velocity(ux, uy, uz, p.pos) if step > 0 else np.zeros(3)
            fd = stokes_drag(p, u_f)
            forces[i] += fd

            # Axial drive
            forces[i][2] += p.mass * AXIAL_DRIVE

            # Rotational / whip drive
            rx = p.pos[0] - NX / 2
            ry = p.pos[1] - NY / 2
            forces[i][0] += -ROT_DRIVE * ry * p.mass
            forces[i][1] +=  ROT_DRIVE * rx * p.mass

            # Synchronized snap
            if step in SNAP_STEPS:
                forces[i][2] += p.mass * SNAP_STRENGTH

            # Reaction force onto fluid (simple nearest-cell)
            ix = int(np.clip(p.pos[0], 1, NX - 2))
            iy = int(np.clip(p.pos[1], 1, NY - 2))
            iz = int(np.clip(p.pos[2], 1, NZ - 2))
            force_on_fluid[ix, iy, iz] -= fd * 0.2

        # --- Integrate particles ---
        for i, p in enumerate(particles):
            acc = forces[i] / p.mass
            p.vel += acc * DT_DEM
            p.pos += p.vel * DT_DEM

            # Soft cylindrical wall
            rxy = np.sqrt((p.pos[0] - NX/2)**2 + (p.pos[1] - NY/2)**2)
            if rxy + p.radius > NX/2 - 1.5:
                radial = np.array([p.pos[0] - NX/2, p.pos[1] - NY/2, 0.0])
                radial /= (np.linalg.norm(radial) + 1e-9)
                p.pos[:2] -= radial[:2] * 0.4
                p.vel[:2] *= -0.4
            p.pos[2] = np.clip(p.pos[2], 2.0, NZ - 3)

        # --- LBM fluid step ---
        body_force = np.zeros((NX, NY, NZ, 3))
        body_force[..., 2] = 2.0e-5
        body_force += force_on_fluid
        f, rho, ux, uy, uz = lbm_step(f, force=body_force)

        # --- Diagnostics ---
        if step % OUTPUT_EVERY == 0 or step in SNAP_STEPS or step == STEPS - 1:
            zs = np.array([p.pos[2] for p in particles])
            speeds = np.array([np.linalg.norm(p.vel) for p in particles])
            Lz = sum((p.pos[0]-NX/2)*p.vel[1] - (p.pos[1]-NY/2)*p.vel[0] for p in particles)
            tag = "  << SNAP" if step in SNAP_STEPS else ""
            print(f"Step {step:4d} | spread={zs.std():5.2f}  "
                  f"|v|={speeds.mean():.4f}  max|v|={speeds.max():.4f}  "
                  f"Lz={Lz:7.3f}{tag}")

    print()
    print(f"Finished in {time.time() - start:.1f} s")
    print("=" * 64)
    return particles


if __name__ == "__main__":
    run_simulation()