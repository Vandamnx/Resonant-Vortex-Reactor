"""
Fluid Dynamics Simulation with CSV Export
Resonant Vortex Reactor (RVR) v4+ - Tuned High-RPM Version

Generates time-series data and saves to CSV.

Run: python fluid_dynamics_with_csv.py
"""

import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd

def fluid_dynamics(t, state, params):
    v, pressure = state
    drive, viscosity, density, sphere_factor, threshold = params
    drive_force = drive * v if v > threshold else drive * 0.6 * v
    drag = viscosity * v**2 + sphere_factor * density * v**3
    dvdt = drive_force - drag
    dpdt = 0.8 * v**2 if v > threshold else 0.3 * v**2
    return [dvdt, dpdt]

# High-RPM parameters
drive = 52.0
viscosity = 0.085
density = 6440
sphere_factor = 0.032
threshold = 18.0

params = [drive, viscosity, density, sphere_factor, threshold]

sol = solve_ivp(fluid_dynamics, [0, 40], [0.0, 0.0], args=(params,), dense_output=True, rtol=1e-6)

t = np.linspace(0, 40, 1600)
v, pressure = sol.sol(t)

# Create DataFrame
df = pd.DataFrame({
    'time_s': t,
    'fluid_velocity': v,
    'vortex_pressure': pressure,
    'power_proxy': v * pressure,
    'above_threshold': (v > threshold).astype(int)
})

# Save to CSV
csv_filename = 'rvr_fluid_dynamics_high_rpm_data.csv'
df.to_csv(csv_filename, index=False)

print(f"CSV data saved to: {csv_filename}")
print(f"Rows: {len(df)}")
print(f"Peak velocity: {v.max():.2f}")
print(f"Max pressure: {pressure.max():.3f}")
print("Columns: time_s, fluid_velocity, vortex_pressure, power_proxy, above_threshold")
