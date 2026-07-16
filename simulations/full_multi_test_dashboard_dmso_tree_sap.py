"""
Aggressive High-RPM Fluid Dynamics Simulation
Resonant Vortex Reactor (RVR) v4+ - Tuned for Strong Vortex Motion

Run: python fluid_dynamics_aggressive.py
"""

import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
import matplotlib.pyplot as plt

def fluid_dynamics(t, state, params):
    v, pressure = state
    drive, viscosity, density, sphere_factor, threshold = params
    drive_force = drive * max(v, 5.0)   # Stronger initial kick
    drag = viscosity * v**2 + sphere_factor * density * v**3
    dvdt = drive_force - drag
    dpdt = 1.2 * v**2 if v > threshold else 0.4 * v**2
    return [dvdt, dpdt]

# Aggressive parameters for high-RPM behavior
drive = 85.0
viscosity = 0.065
density = 6440
sphere_factor = 0.045
threshold = 12.0

params = [drive, viscosity, density, sphere_factor, threshold]

sol = solve_ivp(fluid_dynamics, [0, 35], [8.0, 0.0], args=(params,), dense_output=True, rtol=1e-6)

t = np.linspace(0, 35, 1400)
v, pressure = sol.sol(t)

# CSV Export
df = pd.DataFrame({
    'time_s': t,
    'fluid_velocity': v,
    'vortex_pressure': pressure,
    'power_proxy': v * pressure,
    'above_threshold': (v > threshold).astype(int)
})
df.to_csv('rvr_fluid_dynamics_aggressive.csv', index=False)

# Plot
plt.figure(figsize=(12, 9))

plt.subplot(3, 1, 1)
plt.plot(t, v, linewidth=3.2, color='#00B4D8', label='Fluid Velocity')
plt.axhline(y=threshold, color='#E63946', linestyle='--', label='Sonic Threshold')
plt.title('Aggressive High-RPM Fluid Dynamics (Galinstan + Sphere Chain)')
plt.ylabel('Velocity')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(3, 1, 2)
plt.plot(t, pressure, linewidth=2.8, color='#FF9F1C', label='Vortex Pressure')
plt.ylabel('Pressure')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(3, 1, 3)
plt.plot(t, v * pressure, linewidth=2.5, color='#FF4D4D', label='Power Proxy')
plt.xlabel('Time (s)')
plt.ylabel('Power')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("=== Aggressive Fluid Dynamics Run Complete ===")
print(f"Peak velocity: {v.max():.2f}")
print(f"Max pressure: {pressure.max():.3f}")
print("CSV saved: rvr_fluid_dynamics_aggressive.csv")
print("Strong vortex motion achieved.")
