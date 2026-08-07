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