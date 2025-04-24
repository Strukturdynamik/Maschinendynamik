from typing import List, Tuple
import numpy as np
from scipy.integrate import odeint
from scipy import signal as signal

"""Module to perform integration of differential equations to determine
    coordinates for graphs and animation.
"""


class IntSolverAufgabe4:
    def __init__(self) -> None:
        return None

    def calculate(
        self, x: Tuple[float, float], t: List[float], c: float, d: float, m: float
    ) -> Tuple[float, float]:
        """Calculates the derivatives of the system's state variables.

        Args:
            x (Tuple[float, float]): A tuple containing the current state variables
                                    of the system.
                        - x[0]: Angular displacement (phi).
                        - x[1]: Angular velocity (phi_dot).
            t (List[float]): The current time. This is not used in the equation but
                            is required by the solver.
            c (float): The spring constant (stiffness of the spring).
            d (float): The damping coefficient (resistance to motion due to damping).
            m (float): The mass of the system.

        Returns:
            Tuple[float, float]: A tuple containing the derivatives of the state variables.
                   - x_dot[0]: The derivative of the angular displacement (angular velocity).
                   - x_dot[1]: The derivative of the angular velocity (angular acceleration).
        """
        x_1, x_2 = x[0], x[1]

        x_dot = (x_2, -d / m * x_2 - c / m * x_1)
        return x_dot

    def integrate(
        self,
        func,
        start_deflection: float,
        start_velocity: float,
        t: List[float],
        *args,
    ):
        """This method solves the system's motion by numerically integrating the differential
        equations defined in the `calculate` method. It uses the initial conditions and system
        parameters to compute the system's angular displacement and velocity over time.

        Args:
            func (func): The function that defines the differential equations (in this case,
                the `calculate` method).
            start_deflection (float): The initial angular displacement of the system.
            start_velocity (float): The initial angular velocity of the system.
            t (List[float]): A time array over which the integration is performed.
            *args: Additional arguments to pass to the `func` (e.g., spring constant `c`,
                damping coefficient `d`, mass `m`).

        Returns:
            List[[float], [float]]: The solution to the differential equations, containing the
                angular displacement and velocity over time. Each row corresponds to a time step,
                and the columns represent the state variables (phi, phi_dot)
        """
        y_0 = (start_deflection, start_velocity)
        x = odeint(func=func, y0=y_0, t=t, args=args)[:, 0]

        return x


class IntSolverAufgabe1:
    def __init__(self) -> None:
        return None

    # Dauerlauf
    def state_space_settled(self, z, t, d, m, c, omega):
        delta = d / (3 * m)
        omega_0 = np.sqrt(2 * c / (3 * m))
        b0 = 2 / (3 * m)
        [x, x_p] = z  # Zustandsvektor
        z_p = [
            x_p,
            -2 * delta * x_p - omega_0**2 * x + b0 * np.cos(omega * t),
        ]  # Zustands-DGL
        return z_p

    # Hochlauf
    def state_space_accelerated(self, z, t, d, m, c, alpha):
        delta = d / (3 * m)
        omega_0 = np.sqrt(2 * c / (3 * m))
        b0 = 2 / (3 * m)
        [x, x_p] = z
        z_p = [
            x_p,
            -2 * delta * x_p - omega_0**2 * x + b0 * np.cos(0.5 * alpha * t**2),
        ]
        return z_p

    def integrate(self, func, t, start_deflection, start_velocity, *args):
        z0 = (start_deflection, start_velocity)
        return odeint(func=func, y0=z0, t=t, args=args)[:, 0]


class IntSolverAufgabe3:

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

    def integrate(self, func, t, z0, z0d, *args):

        x0 = (z0, z0d)
        return odeint(func=func, y0=x0, t=t, args=args)[:, 0]


class IntSolverAufgabe2:

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


def validate_solution(solution, correct_solution, relative_threshold=0.05):
    """Validates the student's solution against the correct solution.

    This function compares the student's solution with the correct solution at each time step.
    If the difference between the two solutions is within the specified threshold, the solution
    is considered valid.

    Args:
        solution (numpy.ndarray): The solution generated by the student's implementation.
        correct_solution (numpy.ndarray): The solution generated by the correct implementation.
        relative_threshold (float): The allowable difference between the two solutions at any time
            step indicated in percentage (decimal). Defaults to 0.05.

    Returns:
        bool: True if the student's solution is within the threshold of the correct solution,
                False otherwise.
    """
    # check if shape of solutions match
    if solution.shape != correct_solution.shape:
        print("Error: Your solution and the correct solution have different shapes.")
        return False

    # if solutions are equal, return True
    if np.array_equal(solution, correct_solution, equal_nan=False):
        print("Yor solution is correct!")
        return True

    # if solutions are not equal, compare solutions at each time step
    # if relative error is within threshold, consider the solution correct
    for j in range(len(solution)):
        # avoid division by zero for very small correct_solution values
        if abs(correct_solution[j]) < 1e-10:
            if abs(solution[j] - correct_solution[j]) > 1e-10:
                print(f"Solution mismatch at time step {j}.")
                print(f"Yours: {solution[j]}, Correct: {correct_solution[j]}")
                return False
        else:
            relative_error = abs(
                (solution[j] - correct_solution[j]) / correct_solution[j]
            )
            if relative_error > relative_threshold:
                print(f"Solution mismatch at time step {j}.")
                print(
                    f"Yours: {solution[j]}, Correct: {correct_solution[j]}, Relative Error: {relative_error}"
                )
                return False

    # If all checks pass, the solution is valid
    print("Yor solution is correct!")
    return True
