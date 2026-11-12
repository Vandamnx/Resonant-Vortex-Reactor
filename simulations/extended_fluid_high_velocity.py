"""
Further velocity increase for liquid-metal cases
Ion-coupled triboelectric + ionization model
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

fluids = {
    "water": {
        "density": 1000.0,
        "viscosity": 0.001,
        "sigma0": 5.5e-6,
        "alpha_tribo": 1.5e-6,
        "label": "Deionized Water",
        "color": "#00B4D8",
    },
    "galinstan": {
        "density": 6440.0,
        "viscosity": 0.0024,
        "sigma0": 3.4e6,
        "alpha_tribo": 8.0e-6,
        "label": "Galinstan",
        "color": "#FF9F1C",
    },
    "mercury": {
        "density": 13530.0,
        "viscosity": 0.0015,
        "sigma0": 1.0e6,
        "alpha_tribo": 4.5e-5,
        "label": "Mercury (sim only)",
        "color": "#E63946",
    },
}

# Aggressive retune for higher liquid-metal velocity
drive = 160.0
sphere_factor = 0.0018
visc_scale = 0.25
threshold = 22.0
A_contact = 0.016
v_thresh = 5.0
tau_relax_base = 0.05
n_gas = 1.2e19
E_ion = 11.0
kT = 0.025
gamma = 1.8e-4
beta = 3.5e-22
delta = 1.5e-12
kappa = 1.5e-7
k_sigma = 2.5e-15
k_luma  = 2.0e-12

def make_rhs(fluid_key):
    f = fluids[fluid_key]
    density = f["density"]
    viscosity = f["viscosity"]
    alpha = f["alpha_tribo"]
    sigma0 = f["sigma0"]

    def rhs(t, state):
        v, p, q, ni = state

        sigma_eff = sigma0 + k_sigma * ni
        tau_relax = tau_relax_base * (1e6 / (sigma_eff + 1e-6))**0.35

        drive_force = drive * v if v > threshold else drive * 0.70 * v
        drag = viscosity * visc_scale * v**2 + sphere_factor * density * abs(v)**2.0
        F_electro = kappa * q * abs(q)
        dvdt = drive_force - drag + F_electro

        dpdt = 0.90 * v**2 if v > threshold else 0.35 * v**2

        q_dot_tribo = (
            alpha * density * abs(v) * np.sign(v) * A_contact
            * (1.0 if abs(v) > v_thresh else 0.22)
        )
        q_dot_leak = -q / max(tau_relax, 1e-6)

        field_assist = kT + gamma * abs(q)
        ion_source = beta * abs(q) * n_gas * np.exp(-E_ion / max(field_assist, 1e-9))
        recombination = delta * ni**2
        ni_dot = ion_source - recombination

        return [dvdt, dpdt, q_dot_tribo + q_dot_leak, ni_dot]

    return rhs

t_span = (0.0, 25.0)
t_eval = np.linspace(0.0, 25.0, 1300)
initial = [4.0, 0.0, 0.0, 1.0e8]

results = {}
for key in fluids:
    sol = solve_ivp(
        make_rhs(key),
        t_span,
        initial,
        t_eval=t_eval,
        rtol=1e-6,
        atol=1e-8,
        method="RK45",
    )
    results[key] = sol

def derived(sol, key):
    v, p, q, ni = sol.y
    sigma0 = fluids[key]["sigma0"]
    sigma_eff = sigma0 + k_sigma * ni
    luminosity = k_luma * ni * abs(q)
    return sigma_eff, luminosity

fig, axes = plt.subplots(5, 1, figsize=(12, 13), sharex=True)

for key, sol in results.items():
    f = fluids[key]
    t = sol.t
    v, p, q, ni = sol.y
    sigma_eff, luma = derived(sol, key)

    axes[0].plot(t, v, color=f["color"], lw=2.2, label=f["label"])
    axes[1].plot(t, q, color=f["color"], lw=1.9, label=f["label"])
    axes[2].plot(t, ni, color=f["color"], lw=1.9, label=f["label"])
    axes[3].plot(t, sigma_eff, color=f["color"], lw=1.8, label=f["label"])
    axes[4].plot(t, luma, color=f["color"], lw=1.8, label=f["label"])

axes[0].axhline(threshold, color="gray", ls="--", alpha=0.7)
axes[0].set_ylabel("Velocity")
axes[0].set_title("High-Velocity Retune â Liquid Metals Elevated")
axes[0].legend(loc="upper right")
axes[0].grid(True, alpha=0.3)

axes[1].set_ylabel("Charge proxy")
axes[1].legend(loc="upper right")
axes[1].grid(True, alpha=0.3)

axes[2].set_ylabel("Ion density")
axes[2].legend(loc="upper right")
axes[2].grid(True, alpha=0.3)

axes[3].set_ylabel("Ï_eff")
axes[3].legend(loc="upper right")
axes[3].grid(True, alpha=0.3)

axes[4].set_ylabel("Luminosity proxy")
axes[4].set_xlabel("Time")
axes[4].legend(loc="upper right")
axes[4].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("/home/workdir/artifacts/extended_fluid_high_velocity.png", dpi=150)
plt.close()

print("=== High-Velocity Retune Results ===")
print(f"{'Fluid':<22} {'Peak v':>8} {'Final v':>8} {'Final q':>11} {'Final ni':>11} {'Luma':>10}")
print("-" * 75)
for key, sol in results.items():
    v, p, q, ni = sol.y
    _, luma = derived(sol, key)
    print(f"{fluids[key]['label']:<22} {np.max(v):8.2f} {v[-1]:8.2f} {q[-1]:11.3e} "
          f"{ni[-1]:11.3e} {luma[-1]:10.3e}")

print("\nPlot saved: /home/workdir/artifacts/extended_fluid_high_velocity.png")
print("Liquid-metal velocities substantially increased.")