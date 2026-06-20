"""
Resonant Vortex Reactor - Healing v4.6 Simulation
Simple physics-based model for temperature effects, MR viscosity, and estimated output.

This is an educational starter script. Real-world results will vary.
"""

import numpy as np
import matplotlib.pyplot as plt

# ==================== PARAMETERS ====================
# Base parameters for Healing v4.6 Land Version
BASE_TEMP = 30.0          # °C (center of sweet spot)
MIN_TEMP = 15.0
MAX_TEMP = 45.0
RESIN_PERCENT = 10.0      # % resin in carrier (sweet spot ~8-12%)

# Estimated performance at optimal conditions
OPTIMAL_OUTPUT_W = 180.0  # Watts (midpoint of 120-220W range)
OPTIMAL_RPM = 50000       # Average sphere/whip RPM

# Simple viscosity model (arbitrary units for demo)
def viscosity_vs_temp(temp_c):
    """Higher temp = lower viscosity (better flow up to a point)"""
    # Simple linear approximation around sweet spot
    return max(0.5, 2.0 - 0.05 * (temp_c - 20))

def estimated_output(temp_c, resin_pct):
    """Rough model: output peaks around 25-35°C and optimal resin %"""
    temp_factor = max(0.3, 1.0 - 0.04 * abs(temp_c - 30))
    resin_factor = max(0.6, 1.0 - 0.05 * abs(resin_pct - 10))
    return OPTIMAL_OUTPUT_W * temp_factor * resin_factor

def estimated_rpm(temp_c):
    """Higher viscosity at low temp reduces effective RPM"""
    visc = viscosity_vs_temp(temp_c)
    return int(OPTIMAL_RPM * (1.2 / visc))

# ==================== SIMULATION ====================
def run_simulation():
    print("=== Healing v4.6 Resonant Vortex Reactor Simulation ===\n")
    print(f"Resin mix: {RESIN_PERCENT}%")
    print(f"Optimal temp range: 25–35°C\n")

    temps = np.linspace(MIN_TEMP, MAX_TEMP, 13)
    results = []

    print(f"{'Temp (°C)':<10} {'Viscosity':<12} {'Est. RPM':<12} {'Est. Output (W)':<18}")
    print("-" * 55)

    for t in temps:
        visc = viscosity_vs_temp(t)
        rpm = estimated_rpm(t)
        output = estimated_output(t, RESIN_PERCENT)
        results.append((t, visc, rpm, output))
        print(f"{t:<10.1f} {visc:<12.2f} {rpm:<12} {output:<18.1f}")

    # Find best temperature
    best = max(results, key=lambda x: x[3])
    print(f"\nBest performance around: {best[0]:.1f}°C → ~{best[3]:.0f}W")

    # Optional plotting
    try:
        plot_results(temps, results)
    except:
        print("\n(Install matplotlib for plots: pip install matplotlib)")

def plot_results(temps, results):
    outputs = [r[3] for r in results]
    rpms = [r[2] for r in results]

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Temperature (°C)')
    ax1.set_ylabel('Estimated Output (W)', color=color)
    ax1.plot(temps, outputs, color=color, marker='o', label='Output (W)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.axvspan(25, 35, alpha=0.2, color='green', label='Sweet Spot (25-35°C)')

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Estimated RPM', color=color)
    ax2.plot(temps, rpms, color=color, marker='s', linestyle='--', label='RPM')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Healing v4.6 - Temperature vs Performance (Simple Model)')
    fig.tight_layout()
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    run_simulation()
    print("\nSimulation complete. Modify parameters and re-run to explore!")
```

This is a clean, educational starter script. It includes:
- Temperature vs viscosity model
- Estimated output and RPM calculations
- Console table + optional matplotlib plots
- Clear comments

The user can run it locally and expand it (add more physics, Monte Carlo, etc.).

Now, save it and tell the user it's ready for the repo (e.g., in a `simulations/` or root folder).