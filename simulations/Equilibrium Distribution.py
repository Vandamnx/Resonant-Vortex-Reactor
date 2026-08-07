def equilibrium(rho, ux, uy, uz):
    feq = np.zeros(rho.shape + (19,))
    usq = ux**2 + uy**2 + uz**2

    for i in range(19):
        cu = c[i,0]*ux + c[i,1]*uy + c[i,2]*uz
        feq[..., i] = w[i] * rho * (1 + cu/cs2 + 0.5*(cu/cs2)**2 - 0.5*usq/cs2)
    return feq