#!/usr/bin/env python3
"""
v4.3.1 Whip Base Resonance Simulation – Expanded Sensitivity Analysis
Resonant Vortex Reactor – Gali-Spinal Tube

Model: Short cantilever bending resonance (end-mass approximation)
f = (1 / 2π) * sqrt(3 * E * I / (m * L**3))
I = (b * h**3) / 12
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Materials
# ============================================================

materials = {
    "316L Stainless": {"E": 193e9, "density": 8000},
    "Nitinol (Austenite)": {"E": 75e9, "density": 6450},
}

def moment_of_inertia(b, h):
    return (b * h**3) / 12

def resonance_frequency(E, I, m, L):
    return (1 / (2 * np.pi)) * np.sqrt(3 * E * I / (m * L**3))

def strain_energy(E, I, delta, L):
    return (3 * E * I * delta**2) / (2 * L**3)

# ============================================================
# BASELINE (tuned geometry that hits the target band)
# ============================================================

print("=" * 70)
print("v4.3.1 Whip Base Resonance – Expanded Sensitivity Analysis")
print("Target band: 0.40 – 1.23 kHz")
print("=" * 70)
print()

L0 = 0.012          # 12 mm
b0 = 0.0045         # 4.5 mm
h0 = 0.00055        # 0.55 mm
tip0 = 0.0018       # 1.8 g
gal0 = 0.08         # 8 %

print("BASELINE GEOMETRY")
print(f"  L = {L0*1000:.1f} mm | section {b0*1000:.1f} × {h0*1000:.2f} mm | tip = {tip0*1000:.1f} g | Galinstan +{gal0*100:.0f}%")
print()

for name, props in materials.items():
    E, dens = props["E"], props["density"]
    beam_mass = dens * b0 * h0 * L0
    m_eff = 0.23 * beam_mass + tip0 * (1 + gal0)
    I = moment_of_inertia(b0, h0)
    f = resonance_frequency(E, I, m_eff, L0)
    U = strain_energy(E, I, 0.001, L0)
    print(f"  {name:22s} → {f:6.0f} Hz ({f/1000:.2f} kHz) | U ≈ {U:.3f} J")
print()

# ============================================================
# 1. SENSITIVITY TO LENGTH
# ============================================================

print("-" * 70)
print("1. SENSITIVITY TO EFFECTIVE LENGTH (fixed section & tip mass)")
print("-" * 70)

L_vals = np.array([0.008, 0.010, 0.012, 0.014, 0.016, 0.018])
print(f"{'L (mm)':>8} | {'316L (kHz)':>12} | {'Nitinol (kHz)':>14}")
print("-" * 40)
for L in L_vals:
    row = f"{L*1000:8.1f}"
    for name, props in materials.items():
        E, dens = props["E"], props["density"]
        beam_mass = dens * b0 * h0 * L
        m_eff = 0.23 * beam_mass + tip0 * (1 + gal0)
        I = moment_of_inertia(b0, h0)
        f = resonance_frequency(E, I, m_eff, L) / 1000
        row += f" | {f:12.2f}"
    print(row)
print()

# ============================================================
# 2. SENSITIVITY TO THICKNESS
# ============================================================

print("-" * 70)
print("2. SENSITIVITY TO THICKNESS h (L=12 mm, fixed width & tip)")
print("-" * 70)

h_vals = np.array([0.00040, 0.00050, 0.00055, 0.00065, 0.00080])
print(f"{'h (mm)':>8} | {'316L (kHz)':>12} | {'Nitinol (kHz)':>14}")
print("-" * 40)
for h in h_vals:
    row = f"{h*1000:8.2f}"
    for name, props in materials.items():
        E, dens = props["E"], props["density"]
        beam_mass = dens * b0 * h * L0
        m_eff = 0.23 * beam_mass + tip0 * (1 + gal0)
        I = moment_of_inertia(b0, h)
        f = resonance_frequency(E, I, m_eff, L0) / 1000
        row += f" | {f:12.2f}"
    print(row)
print()

# ============================================================
# 3. SENSITIVITY TO TIP MASS
# ============================================================

print("-" * 70)
print("3. SENSITIVITY TO TIP MASS (L=12 mm, fixed section)")
print("-" * 70)

tip_vals = np.array([0.0010, 0.0015, 0.0018, 0.0025, 0.0035, 0.0050])
print(f"{'Tip (g)':>8} | {'316L (kHz)':>12} | {'Nitinol (kHz)':>14}")
print("-" * 40)
for tip in tip_vals:
    row = f"{tip*1000:8.1f}"
    for name, props in materials.items():
        E, dens = props["E"], props["density"]
        beam_mass = dens * b0 * h0 * L0
        m_eff = 0.23 * beam_mass + tip * (1 + gal0)
        I = moment_of_inertia(b0, h0)
        f = resonance_frequency(E, I, m_eff, L0) / 1000
        row += f" | {f:12.2f}"
    print(row)
print()

# ============================================================
# 4. SENSITIVITY TO GALINSTAN LOADING
# ============================================================

print("-" * 70)
print("4. SENSITIVITY TO GALINSTAN MASS LOADING (L=12 mm)")
print("-" * 70)

gal_vals = np.array([0.00, 0.05, 0.08, 0.12, 0.20])
print(f"{'Gal %':>8} | {'316L (kHz)':>12} | {'Nitinol (kHz)':>14}")
print("-" * 40)
for gal in gal_vals:
    row = f"{gal*100:7.0f}%"
    for name, props in materials.items():
        E, dens = props["E"], props["density"]
        beam_mass = dens * b0 * h0 * L0
        m_eff = 0.23 * beam_mass + tip0 * (1 + gal)
        I = moment_of_inertia(b0, h0)
        f = resonance_frequency(E, I, m_eff, L0) / 1000
        row += f" | {f:12.2f}"
    print(row)
print()

# ============================================================
# 5. DESIGN POINTS THAT HIT SPECIFIC TARGET FREQUENCIES
# ============================================================

print("-" * 70)
print("5. DESIGN POINTS AIMED AT SPECIFIC FREQUENCIES (316L Stainless)")
print("-" * 70)
print("Target frequencies: 0.50, 0.70, 1.00 kHz")
print()

targets = [500, 700, 1000]  # Hz
for target in targets:
    best_L = None
    best_f = None
    for L in np.linspace(0.007, 0.018, 50):
        beam_mass = 8000 * b0 * h0 * L
        m_eff = 0.23 * beam_mass + tip0 * (1 + gal0)
        I = moment_of_inertia(b0, h0)
        f = resonance_frequency(193e9, I, m_eff, L)
        if best_L is None or abs(f - target) < abs(best_f - target):
            best_L = L
            best_f = f
    print(f"  Target {target/1000:.2f} kHz → L ≈ {best_L*1000:.1f} mm  (actual {best_f:.0f} Hz)")

print()
print("=" * 70)
print("Sensitivity analysis complete.")
print("Key takeaway: Frequency is most sensitive to length and thickness.")
print("Tip mass and Galinstan loading produce smaller, secondary shifts.")
print("=" * 70)