# Per-cell fluid quantities (simple structured grid example)
@dataclass
class FluidCell:
    u: np.ndarray          # velocity (3,)
    p: float               # pressure
    epsilon: float         # void fraction (1 = empty, 0 = full of particles)
    force_p2f: np.ndarray  # momentum source from particles (3,)
    
    def map_particles_to_fluid(particles, fluid_grid, cell_size):
    """
    Simple Particle-In-Cell style mapping.
    fluid_grid is a 3-D array of FluidCell.
    """
    # Reset
    for cell in fluid_grid.flat:
        cell.epsilon = 1.0
        cell.force_p2f[:] = 0.0

    inv_cell_vol = 1.0 / (cell_size**3)

    for p in particles:
        # Find cell index
        idx = np.floor((p.pos - domain_min) / cell_size).astype(int)
        idx = np.clip(idx, 0, np.array(fluid_grid.shape) - 1)

        cell = fluid_grid[tuple(idx)]

        # Volume occupied by particle
        vol_p = (4/3) * np.pi * p.radius**3
        cell.epsilon -= vol_p * inv_cell_vol
        cell.epsilon = max(cell.epsilon, 0.05)   # avoid division by zero

        # Momentum source (drag reaction)
        # We store the opposite of the force the fluid exerted on the particle
        # (this will be computed after drag is known)
        
        def fluid_force_on_particle(p: Particle, u_fluid: np.ndarray, epsilon: float,
                            eta: float, rho: float) -> np.ndarray:
    """
    Di Felice-type drag (works better at higher solid fractions).
    """
    re_p = 2 * p.radius * np.linalg.norm(u_fluid - p.vel) * rho / eta
    re_p = max(re_p, 1e-6)

    # Di Felice correction
    chi = 3.7 - 0.65 * np.exp(-0.5 * (1.5 - np.log10(re_p))**2)
    Cd = (0.63 + 4.8 / np.sqrt(re_p))**2

    A = np.pi * p.radius**2
    drag = 0.5 * Cd * rho * np.linalg.norm(u_fluid - p.vel) * (u_fluid - p.vel)
    drag *= epsilon**(-chi)          # voidage correction

    return drag
    def run_coupled_simulation(particles, fluid_grid, params, t_end):
    t = 0.0
    dem_steps_per_cfd = int(params.dt_cfd / params.dt_dem)

    while t < t_end:
        # -------------------------------------------------
        # A. DEM sub-cycling
        # -------------------------------------------------
        for _ in range(dem_steps_per_cfd):
            forces = [np.zeros(3) for _ in particles]

            # Magnetic + contact forces (same as before)
            ...

            # Fluid → Particle forces
            for i, p in enumerate(particles):
                idx = get_cell_index(p.pos)
                cell = fluid_grid[idx]
                u_f = cell.u
                f_drag = fluid_force_on_particle(p, u_f, cell.epsilon,
                                                 params.eta_fluid, params.rho_fluid)
                forces[i] += f_drag + p.mass * params.gravity

                # Store reaction for later (Particle → Fluid)
                cell.force_p2f -= f_drag   # opposite force on fluid

            # Integrate particles
            ...

            t += params.dt_dem

        # -------------------------------------------------
        # B. CFD update (one step)
        # -------------------------------------------------
        # 1. Finalise void fraction & momentum sources
        map_particles_to_fluid(particles, fluid_grid, cell_size)

        # 2. Solve fluid equations with:
        #    - variable epsilon
        #    - body force = force_p2f / cell_volume
        #    (this is where a real CFD solver would be called)
        solve_fluid_step(fluid_grid, params)

        # 3. Clear force accumulators for next interval
        for cell in fluid_grid.flat:
            cell.force_p2f[:] = 0.0
            