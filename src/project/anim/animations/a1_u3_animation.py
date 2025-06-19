import math
from typing import Any, List
from ipycanvas import hold_canvas, MultiCanvas
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
    A1_U3_T,
    A1_U3_START_DEFLECTION_DEFAULT,
    A1_U3_START_VELOCITY_DEFAULT,
    A1_U3_DEFAULT_M,
    A1_U3_DEFAULT_OMEGA,
    A1_U3_DEFAULT_ALPHA,
    A1_U3_DEFAULT_MU,
    A1_U3_DEFAULT_EPS,
    DEFAULT_FRAME,
)

"""
    Concrete implementation of AnimationInstance to animate the mechanical
    oscillation system in Übung 2, Aufgabe 1
    (Jupyter Notebooks\resources\documents\Übung_2_Aufg1.pdf)

    This class handles the setup, calculation, and visualization of the
    forced damped oscillation system using a spring-damper model. It includes:
    - Drawing static elements of the animation that won't change over time
    - Calculating the system's response over time for two excitation modes
    - Animate the oscillating system to represent the solution
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
        self.frame = DEFAULT_FRAME
        self.start_deflection = A1_U3_START_DEFLECTION_DEFAULT
        self.start_velocity = A1_U3_START_VELOCITY_DEFAULT
        self.spring_nodes = 20
        self.t = A1_U3_T

    def set_canvas_var(self):
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
        self.rect_x = abs_value(self.canvas_width, 30)
        self.rect_y = abs_value(self.canvas_height, 40)
        self.rect_w = abs_value(self.canvas_width, 25)
        self.rect_h = self.rect_w
        self.dot_radius = abs_value(
                self.anim_canvas.width / 2, 1
            )  # Size of the rotating dot

    def _initial_visual(self):
        # define important coordinates

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
        """Calculates the deflection response of the system over time.

        Depending on user input, it can simulate two modes of
        excitation:
        - "Constant": Simulates a constant external force.
        - "Lineary Increasing": Simulates a linearly increasing frequency.

        Uses the system's calculator to solve the differential equations.

        Returns:
            tuple[np.ndarray, np.ndarray]:
                solution (displacement values over time),
                anregung_sol (excitation function values).
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
                self.alpha,
            )
            anregung_sol = np.cos(self.omega * self.t)
            arrow_sol = np.cos(self.omega * self.t)
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
                self.omega,
            )

            anregung_sol = np.cos(0.5 * self.alpha * self.t**2)
            arrow_sol = np.cos(0.5 * self.alpha * self.t**2)

        self.solution = solution
        self.anregung_sol = anregung_sol
        self.arrow_sol = arrow_sol


        #########################
        # Parameters
        amplitude = 1.0      # amplitude of the sine wave
        frequency = 1.0      # in Hz
        phase = 0.0          # in radians

        # Sine wave: y(t) = A * sin(2πft + phase)
        y = amplitude * np.sin(2 * np.pi * frequency * self.t + phase)
        solution = y 
        ##########################

        return solution, anregung_sol

    def calc_bode_diagram(
        self,
    ):
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

    def _animate_visual(self):
        # get current solution from frame
        curr_sol_vis = self.solution[self.frame]

        # map current position onto the canvas
        min_sol = min(self.solution)
        max_sol = max(self.solution)
        mapped_curr_pos = map_value(
            curr_sol_vis,
            min_sol,
            max_sol,
            self.rect_y,
            self.rect_y + self.rect_h,
        )

        with hold_canvas(): 
            self.rect_layer.clear()
            self.circ_layer.clear()
            self.spring_layer.clear()
            self.text_layer.clear()


            # rect 
            self.rect_layer.fill_rect(self.rect_x, mapped_curr_pos, self.rect_w, self.rect_h)
            self.rect_layer.stroke_rect(self.rect_x, mapped_curr_pos, self.rect_w, self.rect_h)

            # circ and connection line 
            circ_y = mapped_curr_pos - abs_value(self.canvas_height, 15)
            self.circ_layer.stroke_line(self.rect_x, mapped_curr_pos, self.circ_x, circ_y)
            self.circ_layer.stroke_line(
            self.rect_x + self.rect_w, mapped_curr_pos, self.circ_x, circ_y
        )
            # big circle 
            self.circ_layer.stroke_circle(self.circ_x, circ_y, self.circ_r)
            self.circ_layer.fill_circle(self.circ_x, circ_y, self.circ_r)

            # small circle 
            self.circ_layer.stroke_circle(self.circ_x, circ_y, abs_value(self.canvas_width, 1))
            self.circ_layer.fill_circle(self.circ_x, circ_y, abs_value(self.canvas_width, 1))

            # rotating dot
            dot_x = self.circ_x + self.circ_r * math.cos(curr_sol_vis)
            dot_y = self.circ_y + self.circ_r * math.sin(curr_sol_vis)

            # Draw the rotating dot

            # fix later
            self.circ_layer.fill_style = "black"
            self.circ_layer.fill_circle(dot_x, dot_y, self.dot_radius)
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
            anker_point_bottom = (self.rect_x + self.rect_w / 2, mapped_curr_pos+self.rect_h)
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
                clear_x=self.canvas_width,
                clear_y=self.canvas_height,
            )

            # text, only animate m
            self.text_layer.fill_text(
            "m₀",
            self.rect_x + self.rect_w / 2 - abs_value(self.canvas_width, 3),
            mapped_curr_pos + self.rect_h / 2 + abs_value(self.canvas_height, 2))



    def _draw_first_frame(self):
        # === Layer 1: Rectangle ===
        self.rect_layer.line_width = 1.5
        self.rect_layer.fill_style = "#bebebe"
        self.rect_layer.fill_rect(self.rect_x, self.rect_y, self.rect_w, self.rect_h)
        self.rect_layer.stroke_rect(self.rect_x, self.rect_y, self.rect_w, self.rect_h)

        # === Layer 2: Circle and Connecting Lines ===
        self.circ_r = abs_value(self.canvas_height, 13)
        self.circ_x = self.rect_x + self.rect_w / 2
        self.circ_y = self.rect_y - abs_value(self.canvas_height, 15)

        self.circ_layer.stroke_line(self.rect_x, self.rect_y, self.circ_x, self.circ_y)
        self.circ_layer.stroke_line(
            self.rect_x + self.rect_w, self.rect_y, self.circ_x, self.circ_y
        )

        self.circ_layer.fill_style = "white"
        self.circ_layer.line_width = 1.5
        self.circ_layer.stroke_circle(self.circ_x, self.circ_y, self.circ_r)
        self.circ_layer.fill_circle(self.circ_x, self.circ_y, self.circ_r)

        self.circ_layer.line_width = 1.0
        self.circ_layer.stroke_circle(self.circ_x, self.circ_y, abs_value(self.canvas_width, 1))
        self.circ_layer.fill_circle(self.circ_x, self.circ_y, abs_value(self.canvas_width, 1))

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
        self.anker_point_bottom = (self.rect_x + self.rect_w / 2, self.rect_y + self.rect_h)
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
            clear_x=self.canvas_width,
            clear_y=self.canvas_height,
        )

        # === Layer 4: Text ===
        self.text_layer.fill_style = "black"
        self.text_layer.font = f"{abs_value(self.canvas_height, 5)}px sans-serif"
        self.text_layer.fill_text(
            "m₀",
            self.rect_x + self.rect_w / 2 - abs_value(self.canvas_width, 3),
            self.rect_y + self.rect_h / 2 + abs_value(self.canvas_height, 2),
        )
        self.text_layer.fill_text(
            "c",
            self.rect_x + abs_value(self.canvas_width, 5),
            self.rect_y + abs_value(self.canvas_width, 40),
        )
        self.text_layer.fill_text(
            "d",
            self.rect_x + abs_value(self.canvas_width, 18),
            self.rect_y + abs_value(self.canvas_width, 40),
        )
