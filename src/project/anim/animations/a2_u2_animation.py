from typing import Any, List
import numpy as np
import time
import os
import math
from ipycanvas import MultiCanvas, hold_canvas
from src.project.utils.helper import (
    abs_value,
    map_value,
    draw_line_with_strokes,
    ghetto_feder_daempfer_element_bottom,
    ghetto_feder_daempfer_element_top,
    draw_arrow,
)
from .anim_superclass import AnimationInstance
from ...calculations.int_solver_a2_u2 import IntSolverAufgabe2Uebung2
from src.project.utils.ext_utils.spring import spring_module

from ...utils.constants import (
    DEFAULT_FRAME,
    A2_U2_T,
    A2_U2_J_A_DEFAULT,
    A2_U2_L_DEFAULT,
    A2_U2_C_DEFAULT,
    A2_U2_D_DEFAULT,
    A2_U2_U_HAT_DEFAULT,
    A2_U2_PHI_0_DEFAULT,
    A2_U2_PHI_0_DOT_DEFAULT,
    A2_U2_OMEGA_DEFAULT,
    A2_U2_ALPHA_DEFAULT,
)


class Aufgabe2(AnimationInstance):
    def __init__(self, calculator: Any) -> None:
        super().__init__()
        self.calculator: Any = calculator
        self.calculator = IntSolverAufgabe2Uebung2()
        self.j_a = A2_U2_J_A_DEFAULT
        self.L = A2_U2_L_DEFAULT
        self.c = A2_U2_C_DEFAULT
        self.d = A2_U2_D_DEFAULT
        self.u_hat = A2_U2_U_HAT_DEFAULT
        self.phi_0 = A2_U2_PHI_0_DEFAULT
        self.phi_0_dot = A2_U2_PHI_0_DOT_DEFAULT
        self.omega = A2_U2_OMEGA_DEFAULT
        self.alpha = A2_U2_ALPHA_DEFAULT
        self.t = A2_U2_T
        self.mode = "Lineary Increasing"
        self.frame = DEFAULT_FRAME
        self.spring_nodes = 20

    def set_vars_and_coordinates(self):
        self.force_input_canvas = self.anim_canvas[0]
        self.rectangle_canvas = self.anim_canvas[1]
        self.spring_canvas = self.anim_canvas[2]
        self.still_canvas = self.anim_canvas[3]

        self.rectangle_canvas.line_width = 1.5
        self.force_input_canvas.line_width = 1.5
        self.spring_canvas.line_width = 1.5
        self.still_canvas.line_width = 1.5

        self.force_input_canvas.font = f"{abs_value(self.anim_canvas.width, 3)}px serif"

        self.rect_x = abs_value(self.anim_canvas.width, 10)
        self.rect_y = abs_value(self.anim_canvas.width, 45)
        self.rect_w = abs_value(self.anim_canvas.width, 85)
        self.rect_h = abs_value(self.anim_canvas.height, 2)

        # make fixed ball bearings
        self.bearings_r = abs_value(self.anim_canvas.width / 4, 3)
        self.bearings_x = self.rect_x + abs_value(self.anim_canvas.width, 10)
        self.bearings_y = self.rect_y + self.rect_h - self.bearings_r

        self.general_x = self.bearings_x + (self.rect_w / 6) * 5
        self.top_spring_default = self.rect_y
        self.top_spring_upper_bound = self.rect_y - abs_value(
            self.anim_canvas.height, 5
        )
        self.bottom_spring_upper_bound = self.rect_y + abs_value(
            self.anim_canvas.height, 20
        )

        self.bottom_spring_lower_bound = self.rect_y + abs_value(
            self.anim_canvas.height, 35
        )

    def _initial_visual(self):
        self.still_canvas.fill_style = "#FFFFFF"

        # draw line with strokes
        self.line_x = self.bearings_x - abs_value(self.anim_canvas.width, 4)
        self.line_y = self.bearings_y + abs_value(self.anim_canvas.height, 7)
        self.line_x_2 = self.bearings_x + abs_value(self.anim_canvas.width, 4)

        draw_line_with_strokes(
            self.still_canvas,
            self.line_x,
            self.line_y,
            self.line_x_2,
            self.line_y,
            len_strokes=abs_value(self.anim_canvas.height, 3),
            num_strokes=7,
            angle=30,
            direction_strokes="bottom",
        )

        self.still_canvas.stroke_line(
            self.bearings_x,
            self.bearings_y,
            self.line_x + abs_value(self.anim_canvas.width / 2, 1),
            self.line_y,
        )
        self.still_canvas.stroke_line(
            self.bearings_x,
            self.bearings_y,
            self.line_x_2 - abs_value(self.anim_canvas.width / 2, 1),
            self.line_y,
        )

        self.still_canvas.fill_circle(self.bearings_x, self.bearings_y, self.bearings_r)
        self.still_canvas.stroke_circle(
            self.bearings_x, self.bearings_y, self.bearings_r
        )

    def _calculate(self):

        # Dauerlauf
        if self.mode == "Constant":
            if self.omega == 0:
                solution = list(np.zeros(len(self.t)))
                anregung_sol = list(np.zeros(len(self.t)))
            else:
                solution = self.calculator.integrate(
                    self.calculator.state_space_steady,
                    self.phi_0,
                    self.phi_0_dot,
                    self.t,
                    self.L,
                    self.j_a,
                    self.u_hat,
                    self.d,
                    self.c,
                    self.omega,
                )
                anregung_sol = self.u_hat * np.cos(self.omega * self.t)

        # Hochlauf
        if self.mode == "Lineary Increasing":
            if self.omega == 0:
                solution = list(np.zeros(len(self.t)))
                anregung_sol = list(np.zeros(len(self.t)))
            else:
                solution = self.calculator.integrate(
                    self.calculator.state_space_accelerated,
                    self.phi_0,
                    self.phi_0_dot,
                    self.t,
                    self.L,
                    self.j_a,
                    self.u_hat,
                    self.d,
                    self.c,
                    self.alpha,
                )

                anregung_sol = self.u_hat * np.cos(0.5 * self.alpha * self.t**2)

        self.solution = solution
        self.anregung_sol = anregung_sol

        return self.solution, self.anregung_sol

    def calc_bode_diagram(self):
        omega_vec, omega_0, mag, mag_undamped, phase = self.calculator.calc_bode(
            self.t, self.d, self.c, self.L, self.j_a
        )
        return omega_vec, omega_0, mag, mag_undamped, phase

    def _animate_visual(self):
        curr_sol_top = self.solution[self.frame]

        curr_sol_bottom = self.anregung_sol[self.frame]
        mapped_value_bottom = map_value(
            curr_sol_bottom,
            min(self.anregung_sol),
            max(self.anregung_sol),
            self.bottom_spring_upper_bound,
            self.bottom_spring_lower_bound,
        )

        self.rectangle_canvas.fill_style = "#bebebe"

        self.rectangle_canvas.clear()
        self.force_input_canvas.clear()
        self.spring_canvas.clear()
        with hold_canvas(self.anim_canvas):
            # draw rectangle on self.rectangle_canvas
            ankerpoint_top = self.draw_rotating_angle(
                self.rectangle_canvas, -curr_sol_top
            )

            # draw spring damper element
            # draw black circle at end of rod
            self.spring_canvas.fill_circle(
                ankerpoint_top[0],
                ankerpoint_top[1],
                abs_value(self.anim_canvas.width / 4, 3),
            )

            # draw top of the feder daempfer element
            spring_anker_point_top = ghetto_feder_daempfer_element_top(
                self.spring_canvas,
                ankerpoint_top,
                fork_width=abs_value(self.anim_canvas.width, 4),
                anker_point_extension=abs_value(self.anim_canvas.width, 2),
                daempfer_fork_extension=abs_value(self.anim_canvas.width, 2),
                daempfer_fork_length=abs_value(self.anim_canvas.width, 4),
                daempfer_fork_width=abs_value(self.anim_canvas.width, 3),
                direction="vertical",
            )

            # ankerpoint_bottom = (self.rect_x + self.rect_w, self.rect_y + self.rect_h + abs_value(self.anim_canvas.height, 30))

            # force_input_point = (ankerpoint_top[0], mapped_value)
            anker_point_bottom = [
                self.general_x,
                mapped_value_bottom,
            ]

            spring_anker_point_bottom = ghetto_feder_daempfer_element_bottom(
                self.spring_canvas,
                anker_point_bottom,
                bottom_fork_extension=abs_value(self.anim_canvas.width, 2),
                bottom_fork_width=abs_value(self.anim_canvas.width, 4),
                daempfer_length=abs_value(self.anim_canvas.width, 4),
                daempfer_width=abs_value(self.anim_canvas.width, 2),
                direction="vertical",
            )

            # make the spring
            spring_width = abs_value(self.anim_canvas.width / 2, 5)
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
                spring_width,
            )

            # draw spring
            self.draw_spring(
                canvas=self.spring_canvas,
                x_coords=x_coords,
                y_coords=y_coords,
                spring_anker_point=spring_anker_point_top,
                width_offset=0,
                height_offset=0,
            )

            # draw force input under the spring damper element
            self.spring_canvas.fill_circle(
                self.general_x,  # force_input_point[0],
                mapped_value_bottom,  # force_input_point[1],
                abs_value(self.anim_canvas.width / 4, 3),
            )

            # draw arrow as force input under the spring damper element
            draw_arrow(
                self.force_input_canvas,
                self.general_x,
                mapped_value_bottom + abs_value(self.anim_canvas.height, 6),
                self.general_x,
                mapped_value_bottom,
                arrow_length=abs_value(self.anim_canvas.width, 2),
                base_length=abs_value(self.anim_canvas.width, 4),
                num_base_strokes=5,
                stroke_len=abs_value(self.anim_canvas.width / 2, 3),
                spacing_padding=1,
            )

            self.force_input_canvas.fill_text(
                "u(t)",
                self.general_x - abs_value(self.anim_canvas.width, 1),
                mapped_value_bottom + abs_value(self.anim_canvas.height, 11),
            )

    def _draw_first_frame(self):
        first_sol_top = self.solution[DEFAULT_FRAME]

        first_sol_bottom = self.anregung_sol[DEFAULT_FRAME]
        mapped_value_bottom = map_value(
            first_sol_bottom,
            min(self.anregung_sol),
            max(self.anregung_sol),
            self.bottom_spring_upper_bound,
            self.bottom_spring_lower_bound,
        )

        self.rectangle_canvas.fill_style = "#bebebe"

        # draw rectangle on self.rectangle_canvas
        ankerpoint_top = self.draw_rotating_angle(self.rectangle_canvas, -first_sol_top)

        # draw spring damper element
        # draw black circle at end of rod
        self.spring_canvas.fill_circle(
            ankerpoint_top[0],
            ankerpoint_top[1],
            abs_value(self.anim_canvas.width / 4, 3),
        )

        # draw top of the feder daempfer element
        spring_anker_point_top = ghetto_feder_daempfer_element_top(
            self.spring_canvas,
            ankerpoint_top,
            fork_width=abs_value(self.anim_canvas.width, 4),
            anker_point_extension=abs_value(self.anim_canvas.width, 2),
            daempfer_fork_extension=abs_value(self.anim_canvas.width, 2),
            daempfer_fork_length=abs_value(self.anim_canvas.width, 4),
            daempfer_fork_width=abs_value(self.anim_canvas.width, 3),
            direction="vertical",
        )

        anker_point_bottom = [
            self.general_x,
            mapped_value_bottom,
        ]

        spring_anker_point_bottom = ghetto_feder_daempfer_element_bottom(
            self.spring_canvas,
            anker_point_bottom,
            bottom_fork_extension=abs_value(self.anim_canvas.width, 2),
            bottom_fork_width=abs_value(self.anim_canvas.width, 4),
            daempfer_length=abs_value(self.anim_canvas.width, 4),
            daempfer_width=abs_value(self.anim_canvas.width, 2),
            direction="vertical",
        )

        # make the spring
        spring_width = abs_value(self.anim_canvas.width / 2, 5)
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
            spring_width,
        )

        # draw spring
        self.draw_spring(
            canvas=self.spring_canvas,
            x_coords=x_coords,
            y_coords=y_coords,
            spring_anker_point=spring_anker_point_top,
            width_offset=0,
            height_offset=0,
        )

        # draw force input under the spring damper element
        self.spring_canvas.fill_circle(
            self.general_x,
            mapped_value_bottom,
            abs_value(self.anim_canvas.width / 4, 3),
        )

    def draw_spring(
        self,
        canvas,
        x_coords,
        y_coords,
        spring_anker_point,
        width_offset,
        height_offset,
    ):

        if np.isscalar(x_coords):
            canvas.stroke_line(
                spring_anker_point[0] + width_offset,
                spring_anker_point[1] - height_offset,
                x_coords,
                y_coords,
            )
            canvas.stroke_line(
                x_coords,
                y_coords,
                x_coords,
                y_coords,
            )
        else:
            canvas.stroke_lines(list(zip(x_coords, y_coords)))
            index = len(x_coords) - 1
            canvas.stroke_line(
                x_coords[index],
                y_coords[index],
                x_coords[index],
                y_coords[index],
            )

    def draw_rotating_angle(self, canvas, angle: float):
        # Calculate the center point of the rectangle
        center_x = self.bearings_x
        center_y = self.bearings_y

        # Calculate the four corners relative to the center
        top_left = (center_x - self.rect_w / 6, center_y - self.rect_h / 2)
        top_right = (center_x + (self.rect_w / 6) * 5, center_y - self.rect_h / 2)
        bottom_left = (center_x - self.rect_w / 6, center_y + self.rect_h / 2)
        bottom_right = (center_x + (self.rect_w / 6) * 5, center_y + self.rect_h / 2)

        # Rotate all points around the center
        top_left_rot = self.rotate_point(*top_left, center_x, center_y, angle)
        top_right_rot = self.rotate_point(*top_right, center_x, center_y, angle)
        bottom_left_rot = self.rotate_point(*bottom_left, center_x, center_y, angle)
        bottom_right_rot = self.rotate_point(*bottom_right, center_x, center_y, angle)

        canvas.fill_polygon(
            [top_left_rot, top_right_rot, bottom_right_rot, bottom_left_rot]
        )
        canvas.stroke_polygon(
            [top_left_rot, top_right_rot, bottom_right_rot, bottom_left_rot]
        )

        return bottom_right_rot

    def rotate_point(self, x, y, pivot_x, pivot_y, angle):
        # Convert angle to radians if it's in degrees
        angle_rad = (
            math.radians(angle)
            if not isinstance(angle, float) or angle > 2 * math.pi
            else angle
        )

        x_new = (
            pivot_x
            + (x - pivot_x) * math.cos(angle_rad)
            - (y - pivot_y) * math.sin(angle_rad)
        )
        y_new = (
            pivot_y
            + (x - pivot_x) * math.sin(angle_rad)
            + (y - pivot_y) * math.cos(angle_rad)
        )
        return x_new, y_new
