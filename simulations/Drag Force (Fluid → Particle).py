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