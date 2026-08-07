def lbm_step(f, force, tau, epsilon=None):
    """
    f      : distribution function (nx,ny,nz,19)
    force  : external force field (nx,ny,nz,3)  ← this is where particle momentum source goes
    tau    : relaxation time
    epsilon: optional void fraction (nx,ny,nz) for porous media style coupling
    """
    # 1. Compute macroscopic fields
    rho, ux, uy, uz = compute_macro(f)

    # 2. Add force contribution to velocity (Guo forcing style, simplified)
    if force is not None:
        ux += force[...,0] / (2 * rho)
        uy += force[...,1] / (2 * rho)
        uz += force[...,2] / (2 * rho)

    # Optional: reduce density by void fraction (simple porosity model)
    if epsilon is not None:
        rho *= epsilon

    # 3. Equilibrium
    feq = equilibrium(rho, ux, uy, uz)

    # 4. Collision (BGK)
    f_col = f - (f - feq) / tau

    # 5. Streaming
    f_new = np.zeros_like(f)
    nx, ny, nz, _ = f.shape

    for i in range(19):
        cx, cy, cz = c[i]
        f_new[..., i] = np.roll(np.roll(np.roll(f_col[..., i], cx, axis=0), cy, axis=1), cz, axis=2)

    return f_new, rho, ux, uy, uz