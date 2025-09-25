import math
from typing import Any, List
from ipycanvas import hold_canvas
import numpy as np
from scipy import signal as signal

from ...utils.helper import (
    abs_value,
    map_value,
    draw_line_with_strokes,
    draw_arrow,
    ghetto_feder_daempfer_element_top,
    ghetto_feder_daempfer_element_bottom,
)
from .anim_superclass import AnimationInstance
from ...utils.ext_utils.spring import spring_module

from ...utils.constants import (
    A1_U2_T,
    A1_U2_START_DEFLECTION_DEFAULT,
    A1_U2_START_VELOCITY_DEFAULT,
    A1_U2_DEFAULT_M,
    A1_U2_DEFAULT_OMEGA,
    A1_U2_DEFAULT_ALPHA,
    A1_U2_DEFAULT_F_HAT,
    DEFAULT_FRAME,
    A1_U2_START_DEFLECTION_MIN,
    A1_U2_START_DEFLECTION_MAX,
)

"""
Concrete implementation of `AnimationInstance` to animate the mechanical
oscillation system in Übung 2, Aufgabe 1
(documentation\aufgaben_pdfs\A1_U2.pdf).

This class handles the setup, numerical calculation, and visualization of a
forced damped oscillation system using a spring-damper model. It includes:

- Drawing static elements of the animation (walls, anchors, etc.)
- Computing the system response over time for different excitation modes
- Animating the oscillating mass with a visual spring-damper system
- Providing Bode diagram data for frequency response analysis
"""


class Aufgabe1(AnimationInstance):
    def __init__(self, calculator: Any) -> None:
        super().__init__()
        self.calculator: Any = calculator
        self.m = A1_U2_DEFAULT_M
        self.omega = A1_U2_DEFAULT_OMEGA
        self.alpha = A1_U2_DEFAULT_ALPHA
        self.f_hat = A1_U2_DEFAULT_F_HAT
        self.frame = DEFAULT_FRAME
        self.start_deflection = A1_U2_START_DEFLECTION_DEFAULT
        self.start_velocity = A1_U2_START_VELOCITY_DEFAULT
        self.spring_nodes = 20
        self.t = A1_U2_T

    def _initial_visual(self):
        """
        Draws the static base layout of the animation canvas.

        Elements drawn include:
        - Walls and floor with stroke patterns
        - Arrow indicating the x-axis (force direction)
        - Anchor point for the spring-damper system
        - Zero-deflection position of the oscillating mass
        - Initial geometry for the spring and damper

        This method is called once before the dynamic animation begins.
        """
        # canvas settings
        self.anim_canvas[6].stroke_style = "red"
        self.anim_canvas[6].line_width = 2.0
        self.anim_canvas[2].line_width = 1.5

        self.top_left_x = abs_value(self.anim_canvas.width, 10)
        top_left = [
            self.top_left_x,
            abs_value(self.anim_canvas.width, 30),
        ]
        bottom_left = [
            abs_value(self.anim_canvas.width, 10),
            abs_value(self.anim_canvas.width, 60),
        ]

        self.bottom_right_x = abs_value(self.anim_canvas.width, 90)
        bottom_right = [
            self.bottom_right_x,
            abs_value(self.anim_canvas.width, 60),
        ]

        # set boundaries for animating the circle
        self.x_min_bound = self.top_left_x + abs_value(self.anim_canvas.width, 36)
        self.x_max_bound = self.bottom_right_x - abs_value(self.anim_canvas.width, 15)

        # position of zero deflection
        self.zero_pos = [
            (self.x_min_bound + self.x_max_bound) / 2,
            (top_left[1] + bottom_left[1]) / 2,
        ]

        self.anim_canvas[4].line_width = 2.0
        draw_line_with_strokes(
            canvas=self.anim_canvas[4],
            x_1=top_left[0],
            y_1=top_left[1],
            x_2=bottom_left[0],
            y_2=bottom_left[1],
            len_strokes=abs_value(self.anim_canvas.height, 5),
            num_strokes=7,
            angle=40,
            direction_strokes="left",
        )
        draw_line_with_strokes(
            canvas=self.anim_canvas[4],
            x_1=bottom_left[0],
            y_1=bottom_left[1],
            x_2=bottom_right[0],
            y_2=bottom_right[1],
            len_strokes=abs_value(self.anim_canvas.height, 5),
            num_strokes=14,
            angle=40,
            direction_strokes="bottom",
        )

        # set anker point for feder dämpfer element
        self.anker_point = [
            self.top_left_x,
            (top_left[1] + bottom_left[1]) / 2,
        ]

        # set some class variables
        self.spring_width = abs_value(self.anim_canvas.width, 5)

        # make arrow for x
        self.anim_canvas[0].line_width = 1.5
        draw_arrow(
            canvas=self.anim_canvas[4],
            x1=self.zero_pos[0],
            y1=self.zero_pos[1] - abs_value(self.anim_canvas.width, 21),
            x2=self.zero_pos[0] + abs_value(self.anim_canvas.width, 10),
            y2=self.zero_pos[1] - abs_value(self.anim_canvas.width, 21),
            alpha=50,
            base_length=abs_value(self.anim_canvas.width, 5),
            num_base_strokes=3,
            stroke_len=abs_value(self.anim_canvas.width / 2, 5),
            spacing_padding=abs_value(self.anim_canvas.width, 1),
            description="x",
            description_padding_x=abs_value(self.anim_canvas.width / 4, 10),
            description_padding_y=-abs_value(self.anim_canvas.width / 3, 2),
            description_max_width=abs_value(self.anim_canvas.width, 2),
            description_font_size=abs_value(
                self.anim_canvas.width / 10, 10
            ),  # abs_value(self.anim_canvas.width / 10, 8),
            description_style="italic",
        )

        # bottom line to determine radius of circle
        self.bottom_line_y = bottom_left[1]
        self.radius = bottom_left[1] - (top_left[1] + bottom_left[1]) / 2

    def _calculate(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Calculates the system's displacement response over time.

        Depending on the selected mode, two excitation types can be simulated:
        - "Constant": Constant sinusoidal excitation with fixed frequency.
        - "Lineary Increasing": Frequency sweep with linearly increasing
          excitation frequency.

        Returns:
            tuple[np.ndarray, np.ndarray]:
                - solution: Displacement values over time
                - anregung_sol: Excitation signal values
        """

        # Dauerlauf
        if self.mode == "Constant":
            solution = self.calculator.integrate(
                self.calculator.state_space_settled,
                self.start_deflection,
                self.start_velocity,
                self.t,
                self.d,
                self.m,
                self.c,
                self.omega,
                self.f_hat,
            )
            anregung_sol = self.f_hat * np.cos(self.omega * self.t)
            arrow_sol = self.f_hat * np.cos(self.omega * self.t)
        # Hochlauf
        if self.mode == "Lineary Increasing":
            solution = self.calculator.integrate(
                self.calculator.state_space_accelerated,
                self.start_deflection,
                self.start_velocity,
                self.t,
                self.d,
                self.m,
                self.c,
                self.f_hat,
                self.alpha,
            )

            anregung_sol = self.f_hat * np.cos(0.5 * self.alpha * self.t**2)
            arrow_sol = self.f_hat * np.cos(0.5 * self.alpha * self.t**2)

        self.solution = solution
        self.anregung_sol = anregung_sol
        self.arrow_sol = arrow_sol

        if self.omega == 0:
            self.solution = list(np.zeros(len(self.t)))

        return self.solution, self.anregung_sol

    def calc_bode_diagram(
        self,
    ) -> tuple[np.ndarray, np.ndarray, List[float], List[float], List[float]]:
        """
        Computes the Bode diagram data for the system.

        This frequency response analysis illustrates how the system reacts
        to different excitation frequencies, both damped and undamped.

        Returns:
            tuple[np.ndarray, np.ndarray, List[float], List[float], List[float]]:
                - omega_vec: Array of excitation frequencies
                - omega_0: Natural frequency of the system
                - mag: Magnitude response (damped)
                - mag_undamped: Magnitude response (undamped)
                - phase: Phase shift in radians
        """
        delta = self.d / (3 * self.m)
        omega_0 = np.sqrt(2 * self.c / (3 * self.m))
        b0 = 2 / (3 * self.m)
        num = np.array([b0])
        omega_vec = np.linspace(0, 2 * omega_0, self.t.size)
        den = np.array([1, 2 * delta, omega_0**2])
        g = signal.TransferFunction(num, den)
        # bode-values
        _, mag, phase = signal.bode(g, omega_vec)
        mag = 10 ** (mag / 20)  # umrechnung von dB auf absoluten Wert

        g_undamped = signal.TransferFunction([b0], [1, 0, omega_0**2])
        _, mag_undamped, _ = signal.bode(g_undamped, omega_vec)
        mag_undamped = 10 ** (mag_undamped / 20)

        return omega_vec, omega_0, mag, mag_undamped, phase

    def animate_visual(self):
        """
        Updates and redraws all dynamic elements of the animation
        for the current frame.

        Drawn/updated elements include:
        - Oscillating mass (circle) at current displacement
        - Rotating dot on the oscillating mass (visual phase indicator)
        - Arrow indicating excitation force
        - Spring-damper system (updated geometry according to mass position)

        This method is called repeatedly for each frame during the animation loop.
        """
        # get current solution from frame
        curr_sol_vis = self.solution[self.frame]

        # map current position onto the canvas
        min_sol = min(self.solution)
        max_sol = max(self.solution)
        # catch f hat = 0 case
        if min_sol == max_sol or self.omega == 0:
            mapped_curr_pos = self.mapped_init_defl
            curr_sol_vis = self.mapped_init_defl
        else:
            mapped_curr_pos = map_value(
                curr_sol_vis,
                min_sol,
                max_sol,
                self.x_min_bound,
                self.x_max_bound,
            )

        with hold_canvas():
            # clear the canvas for animation
            self.anim_canvas[6].clear()  # force indicator
            self.anim_canvas[5].clear()  # dot
            self.anim_canvas[3].clear()  # circle
            self.anim_canvas[2].clear()  # feder daempfer element
            self.anim_canvas[1].clear()  # spring
            self.anim_canvas[0].clear()  # feder daempfer element

            self.anim_canvas[3].fill_style = "#bebebe"
            self.anim_canvas[3].line_width = 1.5

            # draw circle in current position
            self.anim_canvas[3].fill_circle(
                mapped_curr_pos, self.zero_pos[1], self.radius
            )
            self.anim_canvas[3].stroke_circle(
                mapped_curr_pos, self.zero_pos[1], self.radius
            )

            # small circle in middle
            self.anim_canvas[3].fill_style = "#FFFFFF"
            small_radius = abs_value(self.anim_canvas.width / 2, 2)
            self.anim_canvas[3].fill_circle(
                mapped_curr_pos, self.zero_pos[1], small_radius
            )
            self.anim_canvas[3].stroke_circle(
                mapped_curr_pos, self.zero_pos[1], small_radius
            )

            # rotating dot
            dot_radius = abs_value(
                self.anim_canvas.width / 2, 1
            )  # Size of the rotating dot
            orbit_radius = self.radius - abs_value(
                self.anim_canvas.width, 1
            )  # Keep it within the main circle

            # Compute dot position based on current angle
            dot_x = mapped_curr_pos + orbit_radius * math.cos(curr_sol_vis)
            dot_y = self.zero_pos[1] + orbit_radius * math.sin(curr_sol_vis)

            # Draw the rotating dot
            self.anim_canvas[5].fill_circle(dot_x, dot_y, dot_radius)

            # draw arrow indicating force
            min_sol_arrow = min(self.arrow_sol)
            max_sol_arrow = max(self.arrow_sol)
            arr_pos = self.arrow_sol[self.frame]
            if min_sol_arrow == max_sol_arrow or self.omega == 0:
                mapped_arr_sol = 0
            else:
                mapped_arr_sol = map_value(
                    arr_pos,
                    min_sol_arrow,
                    max_sol_arrow,
                    -self.radius,
                    self.radius,
                )

            draw_arrow(
                canvas=self.anim_canvas[6],
                x1=mapped_curr_pos,
                y1=self.zero_pos[1],
                x2=mapped_curr_pos + mapped_arr_sol,
                y2=self.zero_pos[1],
                arrow_length=abs_value(self.anim_canvas.width, 2),
            )

            # feder daempfer element
            anker_point_extension = abs_value(self.anim_canvas.width, 3)
            fork_width = abs_value(self.anim_canvas.width, 10)

            # make top part of feder daempfer element
            spring_anker_point_top = ghetto_feder_daempfer_element_top(
                canvas=self.anim_canvas[3],
                anker_point_top=self.anker_point,
                fork_width=fork_width,
                anker_point_extension=anker_point_extension,
                daempfer_fork_extension=abs_value(self.anim_canvas.width, 2),
                daempfer_fork_length=abs_value(self.anim_canvas.width, 10),
                daempfer_fork_width=abs_value(self.anim_canvas.width, 5),
                direction="left_to_right",
            )

            # make bottom part of feder daempfer element
            spring_anker_point_bottom = ghetto_feder_daempfer_element_bottom(
                canvas=self.anim_canvas[3],
                anker_point_bottom=[mapped_curr_pos - self.radius, self.zero_pos[1]],
                bottom_fork_extension=anker_point_extension,
                bottom_fork_width=fork_width,
                daempfer_length=abs_value(self.anim_canvas.width, 12),
                daempfer_width=abs_value(self.anim_canvas.width, 3),
                direction="left_to_right",
            )

            # draw line from feder daempfer element to circle
            self.anim_canvas[3].stroke_line(
                mapped_curr_pos - self.radius,
                self.zero_pos[1],
                mapped_curr_pos,
                self.zero_pos[1],
            )

            # animate spring in zero position
            x_coords, y_coords = spring_module.spring(
                (
                    spring_anker_point_top[0],
                    spring_anker_point_top[1],
                ),
                (
                    spring_anker_point_bottom[0],
                    spring_anker_point_bottom[1],
                ),  # upper part
                self.spring_nodes,
                self.spring_width,
            )

            # draw spring on canvas[2]
            spring_module.draw_spring(
                canvas=self.anim_canvas[2],
                x_coords=x_coords,
                y_coords=y_coords,
                spring_anker_point=spring_anker_point_top,
                width_offset=0,
                height_offset=0,
            )

    def draw_first_frame(self):
        """
        Renders the very first frame of the animation.

        Sets up the initial state of:
        - Oscillating mass at the mapped initial deflection
        - Center circle and markers
        - Static spring-damper elements in equilibrium position
        - Spring geometry based on default parameters

        Ensures the system is visually initialized before the animation begins.
        """
        self.anim_canvas[6].clear()  # force indicator
        self.anim_canvas[5].clear()  # dot
        self.anim_canvas[3].clear()  # circle
        self.anim_canvas[2].clear()  # feder daempfer element
        self.anim_canvas[1].clear()  # spring
        self.anim_canvas[0].clear()  # feder daempfer element
        self.anim_canvas[0].fill_style = "#bebebe"
        self.anim_canvas[0].line_width = 1.5

        # draw circle in position relative to zero position based on defl_0
        # map inital deflection
        self.mapped_init_defl = map_value(
            self.start_deflection,
            A1_U2_START_DEFLECTION_MIN,
            A1_U2_START_DEFLECTION_MAX,
            self.x_min_bound,
            self.x_max_bound,
        )
        self.anim_canvas[0].fill_circle(
            self.mapped_init_defl, self.zero_pos[1], self.radius
        )
        self.anim_canvas[0].stroke_circle(
            self.mapped_init_defl, self.zero_pos[1], self.radius
        )

        # small circle in middle
        self.anim_canvas[0].fill_style = "#FFFFFF"
        self.anim_canvas[0].fill_circle(
            self.mapped_init_defl,
            self.zero_pos[1],
            abs_value(self.anim_canvas.width / 2, 2),
        )
        self.anim_canvas[0].stroke_circle(
            self.mapped_init_defl,
            self.zero_pos[1],
            abs_value(self.anim_canvas.width / 2, 2),
        )

        # feder daempfer element
        anker_point_extension = abs_value(self.anim_canvas.width, 3)
        fork_width = abs_value(self.anim_canvas.width, 10)
        # make top part of feder daempfer element
        self.spring_anker_point_top = ghetto_feder_daempfer_element_top(
            canvas=self.anim_canvas[0],
            anker_point_top=self.anker_point,
            fork_width=fork_width,
            anker_point_extension=anker_point_extension,
            daempfer_fork_extension=abs_value(self.anim_canvas.width, 2),
            daempfer_fork_length=abs_value(self.anim_canvas.width, 10),
            daempfer_fork_width=abs_value(self.anim_canvas.width, 5),
            direction="left_to_right",
        )

        # make bottom part of feder daempfer element
        spring_anker_point_bottom = ghetto_feder_daempfer_element_bottom(
            canvas=self.anim_canvas[0],
            anker_point_bottom=[self.mapped_init_defl - self.radius, self.zero_pos[1]],
            bottom_fork_extension=anker_point_extension,
            bottom_fork_width=fork_width,
            daempfer_length=abs_value(self.anim_canvas.width, 12),
            daempfer_width=abs_value(self.anim_canvas.width, 3),
            direction="left_to_right",
        )

        # draw line from feder daempfer element to circle
        self.anim_canvas[0].stroke_line(
            self.mapped_init_defl - self.radius,
            self.zero_pos[1],
            self.mapped_init_defl,
            self.zero_pos[1],
        )

        # aniate spring in zero position
        x_coords, y_coords = spring_module.spring(
            (
                self.spring_anker_point_top[0],
                self.spring_anker_point_top[1],
            ),
            (
                spring_anker_point_bottom[0],
                spring_anker_point_bottom[1],
            ),  # upper part
            self.spring_nodes,
            self.spring_width,
        )
        # draw spring
        self.anim_canvas[1].line_width = 1.5
        spring_module.draw_spring(
            canvas=self.anim_canvas[1],
            x_coords=x_coords,
            y_coords=y_coords,
            spring_anker_point=self.spring_anker_point_top,
            width_offset=0,
            height_offset=0,
        )
