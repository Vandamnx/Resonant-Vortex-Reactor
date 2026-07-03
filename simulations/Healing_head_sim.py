"""
Resonant Vortex Reactor (RVR) – Molecular Healing Head v4.1 Simulation
Starter stub for central field coherence modeling

This script models the conceptual "healing field" at the center of the
5-fold symmetric Molecular Healing Head (MHH v4.1).

Core ideas modeled:
- Multi-frequency input (Schumann 7.83 Hz fundamental + healing harmonics)
- Constructive interference at the central node (starburst)
- Magnetic field amplification from highly purified magnetite spheres
- Ion node balance (+ ionized / – de-ionized)
- Resulting restorative molecular coherence field

This is an educational conceptual model only.
Real device physics is significantly more complex.

Run: python Healing_head_sim.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.fft import fft, fftfreq

# ============================================================
#                        PARAMETERS
# ============================================================

fs = 44100                    # sample rate (Hz)
duration = 5.0                # seconds
t = np.linspace(0, duration, int(fs * duration))

# === Frequency set from project spec ===
frequencies = [7.83, 432, 528, 741]   # Schumann + healing sweet spots

# === Device parameters (tune these) ===
num_spheres = 100_000         # highly purified magnetite (Fe3O4) spheres
B_base = 0.8                  # base magnetic field contribution (Tesla)
B_boost = 1.0 + (num_spheres / 100_000) * 0.6   # simplistic amplification factor

ion_balance = 0.65            # 0.0 = all de-ion (blue), 1.0 = all ionized (green)
                              # 0.65 = slightly more + ion nodes active (healing bias)

# ============================================================
#                    CENTRAL FIELD MODEL
# ============================================================

def generate_central_he