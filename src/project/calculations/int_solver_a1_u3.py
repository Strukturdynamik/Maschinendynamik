import numpy as np
from scipy.integrate import odeint

class IntSolverAufgabe1Uebung3:
    def __init__(self) -> None:
        return None

    def state_space_steady(self, x, t, m_u, m, d, c, e, omega):
        b2 = -m_u / m
        omega_0 = np.sqrt(c / m)
        delta = d / (2 * m)
        [z, z_p] = x
        x_p = [
            z_p,
            -2 * delta * z_p - omega_0**2 * z + b2 * e * omega**2 * np.sin(omega * t),
        ]
        return x_p

    def state_space_accelerated(self, x, t, m_u, m, d, c, e, alpha):
        delta = d / (2 * m)
        omega_0 = np.sqrt(c / m)
        b2 = -m_u / m
        [z, z_p] = x
        x_p = [
            z_p,
            -2 * delta * z_p
            - omega_0**2 * z
            - b2 * e * (alpha * t) ** 2 * np.sin(0.5 * alpha * t**2),
        ]
        return x_p

    def integrate(self, func, start_deflection, start_velocity, t, *args):

        x0 = (start_deflection, start_velocity)
        return odeint(func=func, y0=x0, t=t, args=args)[:, 0]
