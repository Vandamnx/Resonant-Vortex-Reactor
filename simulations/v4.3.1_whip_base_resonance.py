#!/usr/bin/env python3
"""
v4.3.1 Whip Base Resonance Simulation
Resonant Vortex Reactor – Gali-Spinal Tube

Includes:
- Baseline geometry tuned to original 0.40–1.23 kHz target
- Locked-in HIGH-FREQUENCY design point (~3.68 kHz)
- Full sensitivity analysis

Model: Short cantilever bending resonance (end-mass approximation)
f = (1 / 2π) * sqrt(3 * E * I / (m * L**3))
I = (b * h**3) / 12
"""

import numpy as np

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
# 1. ORIGINAL TARGET-BAND BASELINE (0.40–1.23 kHz)
# ============================================================

print("=" * 70)
print("v4.3.1 Whip Base Resonance Simulation")
print("=" * 70)
print()

print("1. ORIGINAL TARGET-BAND BASELINE (0.40–1.23 kHz range)")
print("-" * 70)

L0 = 0.012
b0 = 0.0045
h0 = 0.00055
tip0 = 0.0018
gal0 = 0.08

print(f"Geometry: L = {L0*1000:.1f} mm | {b0*1000:.1f} × {h0*1000:.2f} mm | tip = {tip0*1000:.1f} g | Gal +{gal0*100:.0f}%")
print()

for name, props in materials.items():
    E, dens = props["E"], props["density"]
    beam_mass = dens * b0 * h0 * L0
    m_eff = 0.23 * beam_mass + tip0 * (1 + gal0)
    I = moment_of_inertia(b0, h0)
    f = resonance_frequency(E, I, m_eff, L0)
    U = strain_energy(E, I, 0.001, L0)
    print(f"  {name:22s} → {f:6.0f} Hz ({f/1000:.2f} kHz) | U ≈ {U:.3f} J @ 1.0 mm")
print()

# ============================================================
# 2. LOCKED-IN HIGH-FREQUENCY DESIGN POINT
# ============================================================

print("2. LOCKED-IN HIGH-FREQUENCY DESIGN POINT")
print("-" * 70)

L_hf = 0.0065          # 6.5 mm
b_hf = 0.0040          # 4.0 mm
h_hf = 0.00095         # 0.95 mm
tip_hf = 0.0010        # 1.0 g
gal_hf = 0.08

print(f"Geometry: L = {L_hf*1000:.1f} mm | {b_hf*1000:.1f} × {h_hf*1000:.2f} mm | tip = {tip_hf*1000:.1f} g | Gal +{gal_hf*100:.0f}%")
print()

for name, props in materials.items():
    E, dens = props["E"], props["density"]
    beam_mass = dens * b_hf * h_hf * L_hf
    m_eff = 0.23 * beam_mass + tip_hf * (1 + gal_hf)
    I = moment_of_inertia(b_hf, h_hf)
    f = resonance_frequency(E, I, m_eff, L_hf)
    U = strain_energy(E, I, 0.0008, L_hf)
    marker = "  ← PRIMARY" if "316L" in name else ""
    print(f"  {name:22s} → {f:6.0f} Hz ({f/1000:.2f} kHz) | U ≈ {U:.3f} J @ 0.8 mm{marker}")
print()

print("Recommended primary design: 316L Stainless @ ~3.68 kHz")
print()

# ============================================================
# 3. SENSITIVITY SUMMARY (High-Frequency Point)
# ============================================================

print("3. SENSITIVITY AROUND HIGH-FREQUENCY POINT (316L only)")
print("-" * 70)

print("Length variation:")
for L in [0.0055, 0.0060, 0.0065, 0.0070, 0.0075]:
    beam_mass = 8000 * b_hf * h_hf * L
    m_eff = 0.23 * beam_mass + tip_hf * 1.08
    I = moment_of_inertia(b_hf, h_hf)
    f = resonance_frequency(193e9, I, m_eff, L)
    print(f"  L = {L*1000:.1f} mm → {f:.0f} Hz ({f/1000:.2f} kHz)")

print()
print("Thickness variation (L = 6.5 mm):")
for h in [0.00080, 0.00090, 0.00095, 0.00105, 0.00115]:
    beam_mass = 8000 * b_hf * h * L_hf
    m_eff = 0.23 * beam_mass + tip_hf * 1.08
    I = moment_of_inertia(b_hf, h)
    f = resonance_frequency(193e9, I, m_eff, L_hf)
    print(f"  h = {h*1000:.2f} mm → {f:.0f} Hz ({f/1000:.2f} kHz)")

print()
print("Tip mass variation (L = 6.5 mm):")
for tip in [0.0007, 0.0010, 0.0013, 0.0016, 0.0020]:
    beam_mass = 8000 * b_hf * h_hf * L_hf
    m_eff = 0.23 * beam_mass + tip * 1.08
    I = moment_of_inertia(b_hf, h_hf)
    f = resonance_frequency(193e9, I, m_eff, L_hf)
    print(f"  tip = {tip*1000:.1f} g → {f:.0f} Hz ({f/1000:.2f} kHz)")

print()
print("=" * 70)
print("Script complete.")
print("Primary recommendation: 6.5 mm × 4.0×0.95 mm × 1.0 g tip → ~3.68 kHz (316L)")
print("=" * 70)
