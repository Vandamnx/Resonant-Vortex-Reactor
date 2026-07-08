<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Resonant Vortex Reactor (RVR)](#resonant-vortex-reactor-rvr)
  - [Current Architecture](#current-architecture)
  - [Simulations](#simulations)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Resonant Vortex Reactor (RVR)

**Status:** Active conceptual development — July 2026

The Resonant Vortex Reactor is a modular platform exploring macroscopic resonance, twist-force dynamics, and potential time-particle modulation effects through engineered magnetic-fluid systems.

Core architecture centers on the **Gali-Spinal Tube** — a high-RPM rotating system using an unbalanced whip head, magnetized magnetite sphere chain, double-headed ferrite core, and pure iron return path, operating with carrier fluids such as deionized water or Galinstan variants.

Two primary head configurations are under development:

- **Molecular Healing Head (v4.1)** — Focused on restorative molecular coherence and time-reversal-dominant dynamics.
- **Magnetic Plasma Production Head (v4.0.6)** — Focused on energy-oriented, time-forward-dominant operation.

---

## Current Architecture

Full technical specifications are maintained in:

- `specs/RVR_Spec_Sheet_v4.0.6.md` — Main project specification (architecture, materials, MHD principles, roadmap)
- `specs/v4.3.2.md` — Gali-Spinal Tube v4.3.2 detailed construction and performance specs
- `Time-particle-theory.md` — Foundational theoretical framework
- `Experimental Testing – Torsion-like Signatures (v4+).md` — Proposed experimental protocols

---

## Simulations

Runnable Python stubs are located in the `simulations/` folder:

```bash
cd simulations
python MHD_Lorentz_Sim.py          # Self-sustaining MHD loop
python Schumann_harmonics_sim.py   # Schumann + healing frequency composite
python Healing_head_sim.py         # Central healing field interference model