"""
Full Multi-Test Dashboard Simulation
Resonant Vortex Reactor (RVR) v4+ Testing Protocols

Simulates:
1. Spin-Dependent Torque Anomaly (long run)
2. Yellow vs Green Node Phase Shift
3. Micro-Anomaly Rate Changes
4. Gyroscopic/Inertial Drift

Run: python full_multi_test_dashboard.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# === Shared time base ===
t = np.linspace(0, 45, 1800)   # Longer run (45 seconds)

# 1. Torsion Torque Anomaly (longer, stronger)
def torsion_dynamics(t, state, params):
    omega, anomaly = state
    base_drive, drag, threshold, boost = params
    d_omega = base_drive - drag * omega**2
    if omega > threshold:
        d_omega += boost * (omega - threshold)**1.15
    d_anomaly = 2.2 if omega > threshold else -1.1
    return [d_omega, d_anomaly]

params_torsion = [35.0, 0.082, 14.0, 22.0]
sol = solve_ivp(torsion_dynamics, [0, 45], [0.0, 0.0], args=(params_torsion,), dense_output=True)
omega, torsion_anomaly = sol.sol(t)

# 2. Node Phase Shift (Yellow vs Green)
yellow_node = np.sin(2 * np.pi * 5.1 * t) + 0.35 * np.sin(2 * np.pi * 14.8 * t) + 0.12 * np.random.randn(len(t))
green_node = np.sin(2 * np.pi * 2.9 * t) + 0.28 * np.sin(2 * np.pi * 7.83 * t)
green_grounded = green_node + 0.18 * np.sin(2 * np.pi * 1.4 * t)

# 3. Micro-Anomaly Rate
base_rate = 0.8
anomaly_rate = base_rate + 4.5 * (omega > 18).astype(float) + 1.2 * np.sin(2 * np.pi * 0.4 * t)

# 4. Gyroscopic Drift
gyro_drift = 0.3 * np.cumsum((omega > 20).astype(float)) * 0.015 + 0.08 * np.random.randn(len(t))

# === Dashboard Plot ===
fig, axs = plt.subplots(4, 1, figsize=(12, 14))

# Torque
axs[0].plot(t, omega, color='#00B4D8', linewidth=2.8, label='Rotation Speed')
axs[0].axhline(y=14, color='#E63946', linestyle='--', label='Sonic Threshold')
axs[0].set_title('1. Spin-Dependent Torque Anomaly (Long Run)')
axs[0].set_ylabel('Speed')
axs[0].legend()
axs[0].grid(True, alpha=0.3)

# Nodes
axs[1].plot(t, yellow_node, color='#FFCC00', alpha=0.9, label='Yellow (Ionizing)')
axs[1].plot(t, green_grounded, color='#00CC66', linewidth=2.2, label='Green + Grounding')
axs[1].set_title('2. Yellow vs Green Node Phase Shift')
axs[1].set_ylabel('Amplitude')
axs[1].legend()
axs[1].grid(True, alpha=0.3)

# Micro-Anomalies
axs[2].plot(t, anomaly_rate, color='#FF6B6B', linewidth=2.2, label='Micro-Anomaly Rate')
axs[2].set_title('3. Micro-Anomaly Rate Changes')
axs[2].set_ylabel('Rate')
axs[2].legend()
axs[2].grid(True, alpha=0.3)

# Gyro
axs[3].plot(t, gyro_drift, color='#C77DFF', linewidth=2.0, label='Gyroscopic Drift')
axs[3].set_title('4. Gyroscopic / Inertial Anomalies')
axs[3].set_xlabel('Time (s)')
axs[3].set_ylabel('Drift')
axs[3].legend()
axs[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("=== Full Multi-Test Dashboard Simulation Complete ===")
print(f"Peak rotation: {omega[-1]:.2f}")
print(f"Max torsion anomaly: {max(torsion_anomaly):.3f}")
print("Yellow vs Green differential clearly visible.")
print("Micro-anomaly rate spikes above threshold.")
print("Gyro drift accumulates with high-RPM operation.")
print("This dashboard models the core predictions from your v4+ protocols.")
