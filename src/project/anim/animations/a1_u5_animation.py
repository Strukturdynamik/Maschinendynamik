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
    rotate_point,
)
from .anim_superclass import AnimationInstance
from ...calculations.int_solver_a1_u5 import IntSolverAufgabe1Uebung5
from src.project.utils.ext_utils.spring import spring_module

from ...utils.constants import (
    DEFAULT_FRAME,
    A1_U5_T,
    A1_U5_C_DEFAULT,
    A1_U5_J_S_DEFAULT,
    A1_U5_M_DEFAULT,
    A1_U5_S_0_DEFAULT,
    A1_U5_S_00_DEFAULT,
    A1_U5_PHI_0_DEFAULT,
    A1_U5_S_DOT_0_DEFAULT,
    A1_U5_PHI_DOT_0_DEFAULT,
    A1_U5_S_R_DEFAULT,
)


class Aufgabe1(AnimationInstance):
    def __init__(self, calculator: Any) -> None:
        super().__init__()
        self.calculator = IntSolverAufgabe1Uebung5()
        self.g = 9.81
        self.c = A1_U5_C_DEFAULT
        self.s_r = A1_U5_S_R_DEFAULT
        self.j_s = A1_U5_J_S_DEFAULT
        self.m = A1_U5_M_DEFAULT
        self.s_0 = A1_U5_S_0_DEFAULT
        self.s_00 = A1_U5_S_00_DEFAULT
        self.phi_0 = A1_U5_PHI_0_DEFAULT
        self.s_dot_0 = A1_U5_S_DOT_0_DEFAULT
        self.phi_dot_0 = A1_U5_PHI_DOT_0_DEFAULT
        self.t = A1_U5_T
        self.mode = "Linear"
        self.frame = DEFAULT_FRAME
        self.spring_nodes = 20

    def set_vars_and_coordinates(self):
        # canvas stuff
        self.still_canvas = self.anim_canvas[3]
        self.still_canvas.line_width = 1.5
        self.center_line_canvas = self.anim_canvas[1]
        self.center_line_canvas.line_width = 1.5
        self.still_canvas.fill_style = "white"
        self.rectangle_canvas = self.anim_canvas[2]
        self.rectangle_canvas.line_width = 1.5
        self.rectangle_canvas.fill_style = "#bebebe"
        self.spring_canvas = self.anim_canvas[0]
        self.spring_nodes = 25
        self.spring_width = abs_value(self.anim_canvas.width, 2)

        # coordinates
        self.general_x = abs_value(self.anim_canvas.width, 50)
        # bearingspoint
        self.bearing_point = [self.general_x, abs_value(self.anim_canvas.height, 15)]
        # default center line endpoint
        self.default_center_line = [
            self.general_x,
            abs_value(self.anim_canvas.height, 70),
        ]
        # default rectangle coords
        self.rect_x = self.general_x - abs_value(self.anim_canvas.width, 3)
        self.rect_y = abs_value(self.anim_canvas.height, 25)
        self.rect_width = abs_value(self.anim_canvas.width, 6)
        self.rect_height = abs_value(self.anim_canvas.height, 10)
        # rectangle bounds
        self.rect_upper_bound = abs_value(self.anim_canvas.height, 15)
        self.rect_bottom_bound = self.default_center_line[1] - self.rect_height

    def _initial_visual(self):
        # line above bearings
        x1 = self.general_x - abs_value(self.anim_canvas.width, 4)
        x2 = self.general_x + abs_value(self.anim_canvas.width, 4)
        y = self.bearing_point[1] - abs_value(self.anim_canvas.height, 4)
        draw_line_with_strokes(
            self.still_canvas,
            x1,
            y,
            x2,
            y,
            len_strokes=abs_value(self.anim_canvas.height, 2.5),
            num_strokes=6,
            angle=30,
            direction_strokes="top",
        )

        # line from bearing to line with strokes
        self.still_canvas.stroke_line(
            self.bearing_point[0], self.bearing_point[1], x1, y
        )
        self.still_canvas.stroke_line(
            self.bearing_point[0], self.bearing_point[1], x2, y
        )

        # make bearings
        self.still_canvas.fill_circle(
            self.bearing_point[0],
            self.bearing_point[1],
            abs_value(self.anim_canvas.height, 1),
        )
        self.still_canvas.stroke_circle(
            self.bearing_point[0],
            self.bearing_point[1],
            abs_value(self.anim_canvas.height, 1),
        )

    def _calculate(self):  # z_0 = (s_00, phi_0*np.pi/180, s_dot_0, phi_dot_0)
        # Nonlinear
        solution_nl = self.calculator.integrate(
            self.calculator.state_space_nonlinear,
            self.s_00,
            self.phi_0 * np.pi / 180,
            self.s_dot_0,
            self.phi_dot_0,
            self.t,
            self.c,
            self.m,
            self.s_0,
            self.g,
            self.j_s,
        )

        # Linear
        solution_l = self.calculator.integrate(
            self.calculator.state_space_linear,
            self.s_00,
            self.phi_0 * np.pi / 180,
            self.s_dot_0,
            self.phi_dot_0,
            self.t,
            self.m,
            self.c,
            self.s_r,
            self.g,
            self.j_s,
        )

        # spring solution
        s_nl = solution_nl[:, 0]
        s_l = solution_l[:, 0]

        # angle displacement solution
        phi_nl = solution_nl[:, 1] / np.pi * 180
        phi_l = solution_l[:, 1] / np.pi * 180

        if self.mode == "Linear":
            self.angle_sol = phi_l
            self.spring_sol = s_l
        if self.mode == "Nonlinear":
            self.angle_sol = phi_nl
            self.spring_sol = s_nl

        return s_nl, s_l, phi_nl, phi_l

    def _animate_visual(self):
        self.center_line_canvas.clear()
        self.rectangle_canvas.clear()
        self.spring_canvas.clear()

        curr_angle_sol = self.angle_sol[self.frame]
        curr_angle_sol = math.radians(curr_angle_sol)
        curr_spring_sol = self.spring_sol[self.frame]

        with hold_canvas(self.canvas):
            # rotate center line
            rotated_center = rotate_point(
                self.default_center_line[0],
                self.default_center_line[1],
                self.bearing_point[0],
                self.bearing_point[1],
                curr_angle_sol,
            )

            # draw center line
            self.center_line_canvas.stroke_line(
                self.bearing_point[0],
                self.bearing_point[1],
                rotated_center[0],
                rotated_center[1],
            )

            # rotated rectangle
            pivot_x = self.bearing_point[0]
            pivot_y = self.bearing_point[1]

            # map current rectangle frame
            mapped_spring_sol = map_value(
                curr_spring_sol,
                min(self.spring_sol),
                max(self.spring_sol),
                self.rect_upper_bound,
                self.rect_bottom_bound,
            )

            top_left = (self.rect_x, mapped_spring_sol)
            top_right = (self.rect_x + self.rect_width, mapped_spring_sol)
            bottom_left = (self.rect_x, mapped_spring_sol + self.rect_height)
            bottom_right = (
                self.rect_x + self.rect_width,
                mapped_spring_sol + self.rect_height,
            )

            rot_top_left = rotate_point(
                top_left[0], top_left[1], pivot_x, pivot_y, curr_angle_sol
            )
            rot_top_right = rotate_point(
                top_right[0], top_right[1], pivot_x, pivot_y, curr_angle_sol
            )
            rot_bottom_left = rotate_point(
                bottom_left[0], bottom_left[1], pivot_x, pivot_y, curr_angle_sol
            )
            rot_bottom_right = rotate_point(
                bottom_right[0], bottom_right[1], pivot_x, pivot_y, curr_angle_sol
            )

            # calculate spring anker point bottom
            spring_anker_x = (rot_top_left[0] + rot_top_right[0]) / 2
            spring_anker_y = (rot_top_left[1] + rot_top_right[1]) / 2
            spring_anker_point_bottom = [spring_anker_x, spring_anker_y]
            spring_anker_point_top = self.bearing_point

            # draw rectangle
            self.rectangle_canvas.fill_polygon(
                [rot_top_left, rot_top_right, rot_bottom_right, rot_bottom_left]
            )
            self.rectangle_canvas.stroke_polygon(
                [rot_top_left, rot_top_right, rot_bottom_right, rot_bottom_left]
            )

            # draw spring
            x_coords, y_coords = spring_module.spring(
                spring_anker_point_bottom,
                spring_anker_point_top,
                self.spring_nodes,
                self.spring_width,
            )
            spring_module.draw_spring(
                canvas=self.spring_canvas,
                x_coords=x_coords,
                y_coords=y_coords,
                spring_anker_point=self.bearing_point,
                width_offset=5,
                height_offset=5,
            )

    def _draw_first_frame(self):
        self.center_line_canvas.clear()
        self.rectangle_canvas.clear()
        self.spring_canvas.clear()

        curr_angle_sol = self.angle_sol[DEFAULT_FRAME]
        curr_angle_sol = math.radians(curr_angle_sol)
        curr_spring_sol = self.spring_sol[DEFAULT_FRAME]

        with hold_canvas(self.canvas):
            # rotate center line
            rotated_center = rotate_point(
                self.default_center_line[0],
                self.default_center_line[1],
                self.bearing_point[0],
                self.bearing_point[1],
                curr_angle_sol,
            )

            # draw center line
            self.center_line_canvas.stroke_line(
                self.bearing_point[0],
                self.bearing_point[1],
                rotated_center[0],
                rotated_center[1],
            )

            # rotated rectangle
            pivot_x = self.bearing_point[0]
            pivot_y = self.bearing_point[1]

            # map current rectangle frame
            mapped_spring_sol = map_value(
                curr_spring_sol,
                min(self.spring_sol),
                max(self.spring_sol),
                self.rect_upper_bound,
                self.rect_bottom_bound,
            )

            top_left = (self.rect_x, mapped_spring_sol)
            top_right = (self.rect_x + self.rect_width, mapped_spring_sol)
            bottom_left = (self.rect_x, mapped_spring_sol + self.rect_height)
            bottom_right = (
                self.rect_x + self.rect_width,
                mapped_spring_sol + self.rect_height,
            )

            rot_top_left = rotate_point(
                top_left[0], top_left[1], pivot_x, pivot_y, curr_angle_sol
            )
            rot_top_right = rotate_point(
                top_right[0], top_right[1], pivot_x, pivot_y, curr_angle_sol
            )
            rot_bottom_left = rotate_point(
                bottom_left[0], bottom_left[1], pivot_x, pivot_y, curr_angle_sol
            )
            rot_bottom_right = rotate_point(
                bottom_right[0], bottom_right[1], pivot_x, pivot_y, curr_angle_sol
            )

            # calculate spring anker point bottom
            spring_anker_x = (rot_top_left[0] + rot_top_right[0]) / 2
            spring_anker_y = (rot_top_left[1] + rot_top_right[1]) / 2
            spring_anker_point_bottom = [spring_anker_x, spring_anker_y]
            spring_anker_point_top = self.bearing_point

            # draw rectangle
            self.rectangle_canvas.fill_polygon(
                [rot_top_left, rot_top_right, rot_bottom_right, rot_bottom_left]
            )
            self.rectangle_canvas.stroke_polygon(
                [rot_top_left, rot_top_right, rot_bottom_right, rot_bottom_left]
            )

            # draw spring
            x_coords, y_coords = spring_module.spring(
                spring_anker_point_bottom,
                spring_anker_point_top,
                self.spring_nodes,
                self.spring_width,
            )
            spring_module.draw_spring(
                canvas=self.spring_canvas,
                x_coords=x_coords,
                y_coords=y_coords,
                spring_anker_point=self.bearing_point,
                width_offset=5,
                height_offset=5,
            )
