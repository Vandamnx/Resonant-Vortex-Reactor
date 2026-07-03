"""
MHD Lorentz Force Self-Sustaining Loop - Starter Stub
Resonant Vortex Reactor (RVR) Project - Version 4.0.6 / 4.1

This simple 1D model demonstrates the core physics:
At equilibrium, Lorentz electromagnetic drive exactly cancels fluid drag
→ self-sustaining perpetual circulation becomes possible.

Governing equation (normalized mass m=1):
    dv/dt = (σ V B² L) v - (C_d ρ A) v²

Run: python mhd_lorentz_stub.py
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def lorentz_mhd(t, v, params):
    sigma, V, B, L, Cd, rho, A = params
    # dv/dt = (sigma*V*B**2*L) * v - (Cd*rho*A) * v**2
    dvdt = (sigma * V * B**2 * L) * v - (Cd * rho * A) * v**2
    return [dvdt]


# === TUNABLE PARAMETERS (realistic starting point for Galinstan system) ===
sigma = 3.4e6      # electrical conductivity of Galinstan (S/m) — very high
V = 0.05           # effective volume / geometry factor
B = 0.8            # magnetic field strength from magnetite spheres (Tesla)
L = 2.0            # characteristic length of current path (m)
Cd = 0.8           # drag coefficient (depends on tube shape & surface)
rho = 6440         # density of Galinstan (kg/m³)
A = 0.0005         # cross-sectional area of the loop (m²)

params = [sigma, V, B, L, Cd, rho, A]

# Solve the ODE from a small initial velocity
sol = solve_ivp(
    lorentz_mhd, 
    [0, 20], 
    [0.05],           # initial velocity m/s
    args=(params,), 
    dense_output=True, 
    rtol=1e-6
)

t = np.linspace(0, 20, 800)
v = sol.sol(t)[0]

# === Plotting ===
plt.figure(figsize=(9, 5))
plt.plot(t, v, linewidth=2.2, color='#00B4D8', label='Flow velocity')
plt.axhline(y=v[-1], color='#E63946', linestyle='--', linewidth=1.5,
            label=f'Terminal velocity ≈ {v[-1]:.4f} m/s')
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Flow Velocity (m/s)', fontsize=12)
plt.title('MHD Lorentz Drive vs Fluid Drag\nSelf-Sustaining Terminal Velocity (Galinstan loop)', fontsize=13)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("=== MHD Self-Sustaining Loop Result ===")
print(f"Terminal velocity reached: {v[-1]:.5f} m/s")
print("At equilibrium: Lorentz force exactly cancels drag → perpetual circulation possible")
print("\nNext steps: Increase B (more spheres or stronger magnetization) or sigma to raise terminal velocity.")
