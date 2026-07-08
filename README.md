# Resonant Vortex Reactor (RVR)

Modular Observationalist Platform • Molecular Healing Head v4.1 • Magnetic Plasma Production Head v4.0.6

**Status:** Active conceptual development (July 2026)  
**Maintainer:** Josh Van Wechel (Vandamnx)  
**License:** To be determined

---

## Vision

A self-sustaining resonant vortex device that generates coherent molecular healing fields and controlled magnetic plasma through magnetohydrodynamic (MHD) principles, extreme magnetic field amplification via purified magnetite spheres, and precise frequency tuning to Earth’s natural resonances.

The system is designed as a modular platform:

- Molecular Healing Head (MHH v4.1) — restorative coherence at cellular scale
- Magnetic Plasma Production Head (v4.0.6) — high-intensity vortex plasma generation
- Long Spinal Coil / Gali-Spinal Tube — resonant waveguide and structural spine
- Grounded Observationalist architecture — anchored into landscape for field testing

---

## Current Architecture

See the detailed specification in `specs/RVR_Spec_Sheet_v4.0.6.md`.

---

## Simulations

Starter simulation stubs live in the `simulations/` folder:

- `MHD_Lorentz_Sim.py` — Core self-sustaining MHD loop physics
- `Schumann_harmonics_sim.py` — Schumann + healing frequency set + audio output
- `Healing_head_sim.py` — Central healing field coherence model (v4.1)

Run them with:

```bash
cd simulations
python MHD_Lorentz_Sim.py
python Schumann_harmonics_sim.py
python Healing_head_sim.py