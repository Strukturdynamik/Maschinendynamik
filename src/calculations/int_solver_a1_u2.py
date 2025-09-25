import numpy as np
from scipy.integrate import odeint


class IntSolverAufgabe1Uebung2:
    def __init__(self) -> None:
        return None

    # Dauerlauf
    def state_space_settled(self, z, t, d, m, c, omega, f_hat):
        [x, x_p] = z  # Zustandsvektor
        delta = d / (3 * m)
        omega_0 = np.sqrt(2 * c / (3 * m))  # Resonanzfrequenz
        b0 = 2 / (3 * m)
        z_p = [
            x_p,
            -2 * delta * x_p - omega_0**2 * x + b0 * f_hat * np.cos(omega * t),
        ]
        return z_p

    # Hochlauf
    def state_space_accelerated(self, z, t, d, m, c, f_hat, alpha):
        [x, x_p] = z
        delta = d / (3 * m)
        omega_0 = np.sqrt(2 * c / (3 * m))
        b0 = 2 / (3 * m)
        z_p = [
            x_p,
            -2 * delta * x_p - omega_0**2 * x + b0 * f_hat * np.cos(0.5 * alpha * t**2),
        ]
        return z_p

    def integrate(self, func, start_deflection, start_velocity, t, *args):
        y0 = (start_deflection, start_velocity)
        x = odeint(func=func, y0=y0, t=t, args=args)[:, 0]
        return x
