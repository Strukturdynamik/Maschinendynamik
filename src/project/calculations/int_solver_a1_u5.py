import numpy as np
from scipy.integrate import odeint


class IntSolverAufgabe1Uebung5:
    def __init__(self) -> None:
        return None

    # Non Linear
    def state_space_nonlinear(self, z, t, c, m, s_0, g, j_s):
        (s, phi, s_dot, phi_dot) = z
        z_dot = (
            s_dot,
            phi_dot,
            s * phi_dot**2 + g * np.cos(phi) - c / m * (s - s_0),
            -(m * g * s * np.sin(phi) + 2 * m * s * s_dot * phi_dot) / (j_s + m * s**2),
        )
        return z_dot

    # Linear
    def state_space_linear(self, z, t, m, c, s_r, g, j_s):
        (s, phi, s_dot, phi_dot) = z
        z_dot = (
            s_dot,
            phi_dot,
            -c / m * (s - s_r),
            -m * g * s_r / (j_s + m * s_r**2) * phi,
        )
        return z_dot

    def integrate(self, func, init_displ, init_defl, init_vel, init_ang_vel, t, *args):
        y0 = (init_displ, init_defl, init_vel, init_ang_vel)
        x = odeint(func=func, y0=y0, t=t, args=args)  # [:, 0]
        return x
