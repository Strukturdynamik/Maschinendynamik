import numpy as np
from scipy.integrate import odeint
from scipy import signal as signal


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

    def integrate(self, func, phi_0, phi_0_dot, t, *args):
        x0 = (phi_0, phi_0_dot)
        return odeint(func=func, y0=x0, t=t, args=args)[:, 0]

    def calc_bode(self, t, d, c, l, j_a):
        b1 = (d * l) / j_a
        b0 = (c * l) / j_a
        delta = (d * l**2) / (2 * j_a)
        omega_0 = np.sqrt((c * l**2) / j_a)
        omega_vec = np.linspace(0, 2 * omega_0, t.size)

        num = np.array([0, b1, b0])
        den = np.array([1, 2 * delta, omega_0**2])
        G = signal.TransferFunction(num, den)

        # bode-values
        _, mag, phase = signal.bode(G, omega_vec)
        mag = 10 ** (mag / 20)

        G_undamped = signal.TransferFunction([0, 0, b0], [1, 0, omega_0**2])
        _, mag_undamped, phase_undamped = signal.bode(G_undamped, omega_vec)
        mag_undamped = 10 ** (mag_undamped / 20)

        return omega_vec, omega_0, mag, mag_undamped, phase
