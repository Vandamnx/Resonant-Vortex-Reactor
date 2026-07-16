"""
Torsion-like Torque Anomaly Simulation - Starter Model
Resonant Vortex Reactor (RVR) v4+ Testing Protocol

Simple 1D model of device acceleration with an additional 'torsion boost' term
that activates above sonic threshold.

Run: python torsion_torque_sim.py
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def device_dynamics(t, state, params):
    omega, torque_anomaly = state
    base_drive, drag_coeff, threshold, torsion_boost = params
    
    # Base drive and drag
    d_omega_dt = base_drive - drag_coeff * omega**2
    
    # Torsion-like anomaly activates above threshold
    if omega > threshold:
        d_omega_dt += torsion_boost * (omega - threshold)
    
    # Very simple anomaly accumulation (for visualization)
    d_anomaly_dt = 0.1 if omega > threshold else -0.05
    d_anomaly_dt = max(min(d_anomaly_dt, 0.5), -0.3)
    
    return [d_omega_dt, d_anomaly_dt]

# Parameters (tunable)
base_drive = 15.0          # Nominal drive torque term
drag_coeff = 0.12          # Fluid + mechanical drag
threshold = 25.0           # Sonic threshold RPM (normalized)
torsion_boost = 8.5        # Extra 'twist-force' contribution above threshold

params = [base_drive, drag_coeff, threshold, torsion_boost]

# Solve from rest
sol = solve_ivp(
    device_dynamics, 
    [0, 8], 
    [0.0, 0.0], 
    args=(params,), 
    dense_output=True, 
    rtol=1e-6
)

t = np.linspace(0, 8, 600)
omega, anomaly = sol.sol(t)

# Plotting
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, omega, linewidth=2.5, color='#00B4D8', label='Rotation Speed (RPM normalized)')
plt.axhline(y=threshold, color='#E63946', linestyle='--', label='Sonic Threshold')
plt.xlabel('Time (s)')
plt.ylabel('Rotation Speed')
plt.title('Device Acceleration with Torsion-Like Boost Above Threshold')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 1, 2)
plt.plot(t, anomaly, linewidth=2.0, color='#FF9F1C', label='Torsion Anomaly Strength')
plt.xlabel('Time (s)')
plt.ylabel('Anomaly Magnitude')
plt.title('Emergent Torsion Anomaly (activates above threshold)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("=== Torsion Torque Simulation Result ===")
print(f"Peak rotation speed: {omega[-1]:.2f}")
print(f"Maximum torsion anomaly: {max(anomaly):.3f}")
print("Note: Anomaly only appears after crossing sonic threshold with stable centroid.")
print("This is a simple starter model — next step is to integrate real sensor data.")
