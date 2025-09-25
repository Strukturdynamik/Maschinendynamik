import math
from typing import Any
from ipycanvas import hold_canvas
import numpy as np
from scipy import signal as signal

from ...utils.helper import (
    abs_value,
    map_value,
    draw_line_with_strokes,
    ghetto_feder_daempfer_element_top,
    ghetto_feder_daempfer_element_bottom,
)
from .anim_superclass import AnimationInstance
from ...utils.ext_utils.spring import spring_module

from ...utils.constants import (
    A1_U3_T,
    A1_U3_DEFAULT_M,
    A1_U3_START_DEFLECTION_DEFAULT,
    A1_U3_START_VELOCITY_DEFAULT,
    A1_U3_DEFAULT_M,
    A1_U3_DEFAULT_OMEGA,
    A1_U3_DEFAULT_ALPHA,
    A1_U3_DEFAULT_MU,
    A1_U3_DEFAULT_EPS,
    A1_U3_START_DEFLECTION_MIN,
    A1_U3_START_DEFLECTION_MAX,
    DEFAULT_FRAME,
)

"""
Concrete implementation of `AnimationInstance` to animate the mechanical
oscillation system in Übung 3, Aufgabe 1
(documentation\aufgaben_pdfs\A1_U3.pdf).

This class handles the setup, numerical calculation, and visualization of a
forced vibration system with a secondary (base) excitation. It includes:

- Defining canvas layers and geometry for all visual elements
- Drawing static background structures and the spring-damper layout
- Computing the system response over time for different excitation modes
- Animating the oscillating mass and force transmission
- Providing Bode diagram and ground force analysis for frequency response
"""


class Aufgabe1(AnimationInstance):
    def __init__(self, calculator: Any) -> None:
        super().__init__()
        self.calculator: Any = calculator
        self.m = A1_U3_DEFAULT_M
        self.omega = A1_U3_DEFAULT_OMEGA
        self.alpha = A1_U3_DEFAULT_ALPHA
        self.eps = A1_U3_DEFAULT_EPS
        self.m_u = A1_U3_DEFAULT_MU
        self.m = A1_U3_DEFAULT_M
        self.frame = DEFAULT_FRAME
        self.start_deflection = A1_U3_START_DEFLECTION_DEFAULT
        self.start_velocity = A1_U3_START_VELOCITY_DEFAULT
        self.spring_nodes = 20
        self.t = A1_U3_T

    def set_canvas_var(self):
        """
        Initializes and assigns canvas layer variables for the animation.

        Layers:
        - bg_layer: Background frame with boundaries
        - rect_layer: Rectangular mass representation
        - circ_layer: Circle and connecting geometry
        - spring_layer: Spring-damper elements
        - text_layer: Labels and annotations
        """
        self.canvas_width, self.canvas_height = (
            self.anim_canvas.width,
            self.anim_canvas.height,
        )

        self.bg_layer = self.anim_canvas[0]
        self.rect_layer = self.anim_canvas[1]
        self.circ_layer = self.anim_canvas[2]
        self.spring_layer = self.anim_canvas[3]
        self.text_layer = self.anim_canvas[4]

    def def_coords(self):
        """
        Defines key coordinates and dimensions for the visual system.

        Includes:
        - Position and size of the rectangular block
        - Orbit and radius for the circular component
        - Deflection bounds (min, max, midpoint)
        - Radius of the rotating dot
        """
        self.rect_x = abs_value(self.canvas_width, 30)
        self.rect_y = abs_value(self.canvas_height, 40)
        self.rect_w = abs_value(self.canvas_width, 25)
        self.rect_h = self.rect_w
        self.dot_radius = abs_value(
            self.anim_canvas.width / 2, 1
        )  # Size of the rotating dot

        self.min_bound = self.rect_y
        self.max_bound = self.rect_y + self.rect_h * 0.5
        self.mid_point = (self.min_bound + self.max_bound) / 2

    def _initial_visual(self):
        """
        Draws the static background and base structures of the animation.

        Includes:
        - Left, right, and bottom frame lines with stroke patterns
        - Base positions for the oscillating rectangle and circle
        - Initialization of key reference points

        Called once before the dynamic animation begins.
        """
        self.circ_r = abs_value(self.canvas_height, 13)
        self.dot_radius = abs_value(self.canvas_height / 2, 3)
        self.orbit_radius = self.circ_r

        # === Layer 0: Background Frame with Strokes ===
        self.bg_layer.line_width = 1.5

        # Frame left
        left_x1 = self.rect_x - abs_value(self.canvas_width, 2)
        left_y1 = self.rect_y
        left_x2 = left_x1
        left_y2 = left_y1 + abs_value(self.canvas_height, 50)

        # Frame bottom
        self.bottom_x1 = left_x2
        self.bottom_y1 = left_y2
        bottom_x2 = self.bottom_x1 + self.rect_w + abs_value(self.canvas_width, 4)
        bottom_y2 = self.bottom_y1

        # Frame right
        right_x1 = bottom_x2
        right_y1 = bottom_y2
        right_x2 = right_x1
        right_y2 = left_y1

        draw_line_with_strokes(
            self.bg_layer,
            right_x1,
            right_y1,
            right_x2,
            right_y2,
            len_strokes=abs_value(self.canvas_width, 5),
            num_strokes=180,
            angle=5,
            direction_strokes="right",
        )

        draw_line_with_strokes(
            self.bg_layer,
            self.bottom_x1,
            self.bottom_y1,
            bottom_x2,
            bottom_y2,
            len_strokes=abs_value(self.canvas_width, 5),
            num_strokes=10,
            angle=30,
            direction_strokes="bottom",
        )

        draw_line_with_strokes(
            self.bg_layer,
            left_x1,
            left_y1,
            left_x2,
            left_y2,
            len_strokes=abs_value(self.canvas_width, 5),
            num_strokes=10,
            angle=30,
            direction_strokes="left",
        )

    def _calculate(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Calculates the system's displacement response over time.

        Two excitation types can be simulated:
        - "Constant": Sinusoidal excitation with fixed frequency.
        - "Lineary Increasing": Frequency sweep with linearly increasing frequency.

        Returns:
            tuple[np.ndarray, np.ndarray]:
                - solution: Displacement values over time
                - anregung_sol: Excitation signal values
        """

        # Dauerlauf
        if self.mode == "Constant":
            solution = self.calculator.integrate(
                self.calculator.state_space_steady,
                self.start_deflection,
                self.start_velocity,
                self.t,
                self.m_u,
                self.m,
                self.d,
                self.c,
                self.eps,
            )

            anregung_sol = self.eps * np.sin(self.omega * self.t)
        # Hochlauf
        if self.mode == "Lineary Increasing":
            solution = self.calculator.integrate(
                self.calculator.state_space_accelerated,
                self.start_deflection,
                self.start_velocity,
                self.t,
                self.m_u,
                self.m,
                self.d,
                self.c,
                self.eps,
                self.alpha,
            )

            anregung_sol = self.eps * np.sin(0.5 * self.alpha * self.t**2)

        self.solution = solution
        self.anregung_sol = anregung_sol

        return solution, anregung_sol

    def calc_bode_diagram(self):
        """
        Computes the Bode diagram data for the current system configuration.

        Analyzes frequency response of the system by evaluating:
        - Damped magnitude response
        - Undamped magnitude response
        - Phase response

        Returns:
            tuple[np.ndarray, float, np.ndarray, np.ndarray, np.ndarray]:
                - omega_vec: Frequency vector
                - omega: Natural frequency of the system
                - mag: Damped magnitude response
                - mag_undamped: Undamped magnitude response
                - phase: Phase shift in radians
        """
        b2 = -self.m_u / self.m
        delta = self.d / (2 * self.m)
        omega_vec = np.linspace(0, 2 * self.omega, len(self.t))

        num = np.array([b2, 0, 0])
        den = np.array([1, 2 * delta, self.omega**2])
        G = signal.TransferFunction(num, den)
        _, mag, phase = signal.bode(G, omega_vec)
        mag = 10 ** (mag / 20)  # Umrechnung von dB auf abs

        G_undamped = signal.TransferFunction([b2, 0, 0], [1, 0, self.omega**2])
        _, mag_undamped, _ = signal.bode(G_undamped, omega_vec)
        mag_undamped = 10 ** (mag_undamped / 20)

        return omega_vec, self.omega, mag, mag_undamped, phase

    def calc_ground_force(self):
        """
        Computes the ground force transfer function for the system.

        This analysis shows how base excitation is transmitted to the ground,
        depending on damping, mass, and excitation frequency.

        Returns:
            tuple[np.ndarray, float, np.ndarray, np.ndarray]:
                - Omega_vec: Frequency vector
                - omega_0: Natural frequency of the system
                - mag: Magnitude of ground force response
                - phase: Phase shift of ground force response
        """
        omega_0 = np.sqrt(self.c / self.m)
        delta = self.d / (2 * self.m)
        num = np.array([-2 * delta * self.m_u, -self.m_u * self.omega**2, 0, 0])
        den = np.array([1, 2 * delta, self.omega**2])
        G = signal.TransferFunction(num, den)
        Omega_vec, mag, phase = signal.bode(G)
        mag = 10 ** (mag / 20)

        return Omega_vec, omega_0, mag, phase

    def _animate_visual(self):
        """
        Updates and redraws all dynamic elements of the animation
        for the current frame.

        Drawn/updated elements include:
        - Rectangular oscillating mass
        - Circle and connecting geometry above the block
        - Rotating dot indicating excitation phase
        - Spring-damper elements attached to the mass
        - Label showing the mass ("m₀")

        Called repeatedly for each frame during the animation loop.
        """
        # get current solution from frame
        curr_sol_vis = self.solution[self.frame]
        curr_force = self.anregung_sol[self.frame]
        # map current position onto the canvas
        min_sol = min(self.solution)
        max_sol = max(self.solution)
        min_force = min(self.anregung_sol)
        max_force = max(self.anregung_sol)
        mapped_curr_pos = map_value(
            curr_sol_vis,
            min_sol,
            max_sol,
            self.rect_y,
            self.rect_y + self.rect_h * 0.5,
        )
        norm_defl = map_value(curr_force, min_force, max_force, -1, 1)

        with hold_canvas():
            self.text_layer.clear()
            self.rect_layer.clear()
            self.circ_layer.clear()
            self.spring_layer.clear()

            # rect
            self.rect_layer.fill_rect(
                self.rect_x, mapped_curr_pos, self.rect_w, self.rect_h
            )
            self.rect_layer.stroke_rect(
                self.rect_x, mapped_curr_pos, self.rect_w, self.rect_h
            )

            # circ and connection line
            circ_y = mapped_curr_pos - abs_value(self.canvas_height, 15)
            self.circ_layer.stroke_line(
                self.rect_x, mapped_curr_pos, self.circ_x, circ_y
            )
            self.circ_layer.stroke_line(
                self.rect_x + self.rect_w, mapped_curr_pos, self.circ_x, circ_y
            )
            # big circle
            self.circ_layer.fill_circle(self.circ_x, circ_y, self.circ_r)
            self.circ_layer.stroke_circle(self.circ_x, circ_y, self.circ_r)

            # small circle
            self.circ_layer.fill_circle(
                self.circ_x, circ_y, abs_value(self.canvas_width, 1)
            )
            self.circ_layer.stroke_circle(
                self.circ_x, circ_y, abs_value(self.canvas_width, 1)
            )

            # map to angle: 0..2π
            angle = norm_defl * 2 * math.pi - math.pi / 2

            # dot coordinates
            dot_x = self.circ_x + self.orbit_radius * math.cos(angle)
            dot_y = circ_y + self.orbit_radius * math.sin(angle)

            self.circ_layer.fill_style = "black"
            self.circ_layer.fill_circle(dot_x, dot_y, self.dot_radius)
            self.circ_layer.stroke_circle(dot_x, dot_y, self.dot_radius)
            self.circ_layer.fill_style = "white"

            # Top Fork
            # static change later no need to redraw
            spring_anker_point_top = ghetto_feder_daempfer_element_top(
                self.spring_layer,
                self.anker_point_top,
                fork_width=abs_value(self.canvas_width, 4),
                anker_point_extension=abs_value(self.canvas_width, 2),
                daempfer_fork_extension=abs_value(self.canvas_width, 3),
                daempfer_fork_length=abs_value(self.canvas_width, 5),
                daempfer_fork_width=abs_value(self.canvas_width, 4),
                direction="vertical",
                top_to_bottom=False,
            )

            # Bottom Fork
            anker_point_bottom = (
                self.rect_x + self.rect_w / 2,
                mapped_curr_pos + self.rect_h,
            )
            spring_anker_point_bottom = ghetto_feder_daempfer_element_bottom(
                self.spring_layer,
                anker_point_bottom,
                bottom_fork_extension=abs_value(self.canvas_width, 2),
                bottom_fork_width=abs_value(self.canvas_width, 4),
                daempfer_length=abs_value(self.canvas_width, 4),
                daempfer_width=abs_value(self.canvas_width, 3),
                direction="vertical",
                top_to_bottom=False,
            )

            # spring
            x_coords, y_coords = spring_module.spring(
                spring_anker_point_top,
                spring_anker_point_bottom,
                self.spring_nodes,
                self.spring_width,
            )
            spring_module.draw_spring(
                canvas=self.spring_layer,
                x_coords=x_coords,
                y_coords=y_coords,
                spring_anker_point=spring_anker_point_top,
                width_offset=0,
                height_offset=0,
            )

            # text, only animate m
            self.text_layer.fill_text(
                "m₀",
                self.rect_x + self.rect_w / 2 - abs_value(self.canvas_width, 3),
                mapped_curr_pos + self.rect_h / 2 + abs_value(self.canvas_height, 2),
            )

    def _draw_first_frame(self):
        """
        Renders the first static frame of the animation.

        Initializes:
        - Oscillating rectangular block at mapped initial deflection
        - Circle and connecting lines in default position
        - Spring-damper system in equilibrium
        - Text labels for the mass ("m₀")

        Ensures the system is visually initialized before the animation begins.
        """
        self.rect_layer.clear()
        self.circ_layer.clear()
        self.spring_layer.clear()
        self.text_layer.clear()

        # draw circle in position relative to zero position based on defl_0
        # map inital deflection
        self.mapped_init_defl = map_value(
            self.start_deflection,
            A1_U3_START_DEFLECTION_MIN,
            A1_U3_START_DEFLECTION_MAX,
            self.max_bound,
            self.min_bound,
        )

        # === Layer 1: Rectangle ===
        self.rect_layer.line_width = 1.5
        self.rect_layer.fill_style = "#bebebe"
        self.rect_layer.fill_rect(
            self.rect_x, self.mapped_init_defl, self.rect_w, self.rect_h
        )
        self.rect_layer.stroke_rect(
            self.rect_x, self.mapped_init_defl, self.rect_w, self.rect_h
        )

        # === Layer 2: Circle and Connecting Lines ===
        self.circ_x = self.rect_x + self.rect_w / 2
        self.circ_y = self.mapped_init_defl - abs_value(self.canvas_height, 15)

        self.circ_layer.stroke_line(
            self.rect_x, self.mapped_init_defl, self.circ_x, self.circ_y
        )
        self.circ_layer.stroke_line(
            self.rect_x + self.rect_w, self.mapped_init_defl, self.circ_x, self.circ_y
        )

        self.circ_layer.fill_style = "white"
        self.circ_layer.line_width = 1.5
        self.circ_layer.fill_circle(self.circ_x, self.circ_y, self.circ_r)
        self.circ_layer.stroke_circle(self.circ_x, self.circ_y, self.circ_r)

        self.circ_layer.line_width = 1.0
        self.circ_layer.fill_circle(
            self.circ_x, self.circ_y, abs_value(self.canvas_width, 1)
        )
        self.circ_layer.stroke_circle(
            self.circ_x, self.circ_y, abs_value(self.canvas_width, 1)
        )

        # === Layer 3: Spring-Damper System ===
        self.spring_layer.line_width = 1.5

        # Top Fork
        self.anker_point_top = (
            self.bottom_x1 + (self.rect_w + abs_value(self.canvas_width, 4)) / 2,
            self.bottom_y1,
        )
        spring_anker_point_top = ghetto_feder_daempfer_element_top(
            self.spring_layer,
            self.anker_point_top,
            fork_width=abs_value(self.canvas_width, 4),
            anker_point_extension=abs_value(self.canvas_width, 2),
            daempfer_fork_extension=abs_value(self.canvas_width, 3),
            daempfer_fork_length=abs_value(self.canvas_width, 5),
            daempfer_fork_width=abs_value(self.canvas_width, 4),
            direction="vertical",
            top_to_bottom=False,
        )

        # Bottom Fork
        self.anker_point_bottom = (
            self.rect_x + self.rect_w / 2,
            self.mapped_init_defl + self.rect_h,
        )
        spring_anker_point_bottom = ghetto_feder_daempfer_element_bottom(
            self.spring_layer,
            self.anker_point_bottom,
            bottom_fork_extension=abs_value(self.canvas_width, 2),
            bottom_fork_width=abs_value(self.canvas_width, 4),
            daempfer_length=abs_value(self.canvas_width, 4),
            daempfer_width=abs_value(self.canvas_width, 3),
            direction="vertical",
            top_to_bottom=False,
        )

        # Spring
        self.spring_nodes = 20
        self.spring_width = abs_value(self.canvas_width, 2)
        x_coords, y_coords = spring_module.spring(
            spring_anker_point_top,
            spring_anker_point_bottom,
            self.spring_nodes,
            self.spring_width,
        )
        spring_module.draw_spring(
            canvas=self.spring_layer,
            x_coords=x_coords,
            y_coords=y_coords,
            spring_anker_point=spring_anker_point_top,
            width_offset=0,
            height_offset=0,
        )

        # === Layer 4: Text ===
        self.text_layer.fill_style = "black"
        self.text_layer.font = f"{abs_value(self.canvas_height, 5)}px sans-serif"
        self.text_layer.fill_text(
            "m₀",
            self.rect_x + self.rect_w / 2 - abs_value(self.canvas_width, 3),
            self.mapped_init_defl + self.rect_h / 2 + abs_value(self.canvas_height, 2),
        )
