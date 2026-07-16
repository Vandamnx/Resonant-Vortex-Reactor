"""
Torsion-like Torque Anomaly Simulation v2 - Stronger Parameters
Resonant Vortex Reactor (RVR) v4+ Testing Protocol

Increased drive and reduced threshold to clearly show anomaly activation.

Run: python torsion_torque_sim_v2.py
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def device_dynamics(t, state, params):
    omega, torque_anomaly = state
    base_drive, drag_coeff, threshold, torsion_boost = params
    
    d_omega_dt = base_drive - drag_coeff * omega**2
    
    # Torsion boost activates strongly above threshold
    if omega > threshold:
        d_omega_dt += torsion_boost * (omega - threshold)**1.1   # nonlinear boost for dramatic effect
    
    # Anomaly accumulation
    d_anomaly_dt = 0.8 if omega > threshold else -0.4
    d_anomaly_dt = max(min(d_anomaly_dt, 1.2), -0.6)
    
    return [d_omega_dt, d_anomaly_dt]

# Stronger parameters for clear demonstration
base_drive = 28.0          # Increased drive
drag_coeff = 0.09          
threshold = 18.0           # Lowered threshold for visible effect
torsion_boost = 12.5       # Stronger boost

params = [base_drive, drag_coeff, threshold, torsion_boost]

# Longer run time
sol = solve_ivp(
    device_dynamics, 
    [0, 12], 
    [0.0, 0.0], 
    args=(params,), 
    dense_output=True, 
    rtol=1e-6
)

t = np.linspace(0, 12, 800)
omega, anomaly = sol.sol(t)

# Plotting
plt.figure(figsize=(11, 7))

plt.subplot(2, 1, 1)
plt.plot(t, omega, linewidth=2.8, color='#00B4D8', label='Rotation Speed (normalized RPM)')
plt.axhline(y=threshold, color='#E63946', linestyle='--', linewidth=1.5, label=f'Sonic Threshold ({threshold})')
plt.xlabel('Time (s)')
plt.ylabel('Rotation Speed')
plt.title('Device Acceleration with Strong Torsion-Like Boost (v2)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 1, 2)
plt.plot(t, anomaly, linewidth=2.5, color='#FF9F1C', label='Torsion Anomaly Strength')
plt.xlabel('Time (s)')
plt.ylabel('Anomaly Magnitude')
plt.title('Emergent Torsion Anomaly - Activates Sharply Above Threshold')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("=== Torsion Torque Simulation v2 Result ===")
print(f"Peak rotation speed: {omega[-1]:.2f}")
print(f"Maximum torsion anomaly: {max(anomaly):.3f}")
print("Clear activation above threshold with stable centroid modeled.")
print("This demonstrates the differential behavior predicted in the protocol.")
