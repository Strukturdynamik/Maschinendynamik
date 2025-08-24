import numpy as np
from scipy.integrate import odeint

class IntSolverAufgabe2Uebung2:
    def __init__(self):
        return None

    def state_space_steady(self, x, t, l, j_a, u_hat, d, c, omega):
        delta = (d * l**2) / (2 * j_a)
        b1 = (d * l) / j_a
        b0 = (c * l) / j_a
        omega_0 = np.sqrt((c * l**2) / j_a)

        [phi, phi_dot] = x
        x_p = [
            phi_dot,
            -2 * delta * phi_dot
            - omega_0**2 * phi
            + b0 * u_hat * np.cos(omega * t)
            - b1 * u_hat * omega * np.sin(omega * t),
        ]
        return x_p

    def state_space_accelerated(self, x, t, l, j_a, u_hat, d, c, alpha):
        delta = (d * l**2) / (2 * j_a)
        b1 = (d * l) / j_a
        b0 = (c * l) / j_a
        omega_0 = np.sqrt((c * l**2) / j_a)

        [phi, phi_dot] = x
        x_p = [
            phi_dot,
            -2 * delta * phi_dot
            - omega_0**2 * phi
            + b0 * u_hat * np.cos(0.5 * alpha * t**2)
            - b1 * u_hat * alpha * t * np.sin(0.5 * alpha * t**2),
        ]
        return x_p

    def integrate(self, func, t, phi_0, phi_0_dot, *args):
        x0 = (phi_0, phi_0_dot)
        return odeint(func=func, y0=x0, t=t, args=args)[:, 0]