from typing import List, Tuple
from scipy.integrate import odeint
from scipy import signal as signal

"""
This module provides numerical solvers for integrating differential equations 
associated with oscillatory systems. 

Each solver class represents a specific exercise or scenario and implements 
the corresponding state-space formulations. The solutions can then be used 
for visualization in graphs and animations.
"""


class IntSolverAufgabe4Uebung1:
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