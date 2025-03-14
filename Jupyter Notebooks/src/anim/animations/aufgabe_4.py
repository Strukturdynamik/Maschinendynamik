import time
import math
from ipycanvas import hold_canvas
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets.widgets as widgets
import time

from ..modules.shapes import Spring, Rectangle
from ...utils.helper import (
    abs_value,
    ghetto_feder_daempfer_element_top,
    draw_line_with_strokes,
    rotate_point,
)
from .anim_superclass import AnimationInstance
from ..modules.shapes import Rectangle, Circle
from ...utils.ext_utils.spring import spring_module

from ...utils.constants import (
    NUM_TIME_UNITS_AUFGABE_4,
    NUM_DATAPOINTS,
    DEFAULT_C,
    DEFAULT_D,
    DEFAULT_FRAME,
)


class Aufgabe4(AnimationInstance):

    def __init__(self, calculator, start_deflection, start_velocity, mass):
        super().__init__()
        self.calculator = calculator
        self.c = DEFAULT_C
        self.d = DEFAULT_D
        self.frame = DEFAULT_FRAME
        self.start_deflection = start_deflection
        self.start_velocity = start_velocity
        self.mass = mass
        self.circ = Circle(center=(-1, -1), radius=-1)
        self.rec = Rectangle(width=-1, height=-1)
        self.t = np.linspace(0, NUM_TIME_UNITS_AUFGABE_4, NUM_DATAPOINTS)
        self.spring_nodes = 20

    def _initial_visual(self):
        """Draw the inital visual for the visual representation of oscillation."""
        # set some class attributes
        self.spring_width = abs_value(self.anim_canvas.width, 5)

        # draw inital lines
        # coordinates
        x_1_h = abs_value(self.anim_canvas.height, 30)
        y_1_h = abs_value(self.anim_canvas.height, 20)
        x_2_h = abs_value(self.anim_canvas.height, 40)
        y_2_h = abs_value(self.anim_canvas.height, 20)

        x_1_v = abs_value(self.anim_canvas.height, 10)
        y_1_v = abs_value(self.anim_canvas.height, 50)
        x_2_v = abs_value(self.anim_canvas.height, 10)
        y_2_v = abs_value(self.anim_canvas.height, 60)

        # horizontal
        self.anim_canvas[1].line_width = 2.0
        draw_line_with_strokes(
            canvas=self.anim_canvas[1],
            x_1=x_1_h,
            y_1=y_1_h,
            x_2=x_2_h,
            y_2=y_2_h,
            len_strokes=abs_value(self.anim_canvas.height, 2),
            num_strokes=5,
            alpha=30,
            direction_strokes="top",
        )
        self.anim_canvas[1].line_width = 1.5

        # triangle on horizontal line
        triangle_endpoint_x_h = x_1_h + ((x_2_h - x_1_h) / 2)
        triangle_endpoint_y_h = y_1_h + abs_value(self.anim_canvas.height, 5)
        self.anim_canvas[1].stroke_line(
            x_1_h + abs_value(self.anim_canvas.height, 1),
            y_1_h,
            triangle_endpoint_x_h,
            triangle_endpoint_y_h,
        )
        self.anim_canvas[1].stroke_line(
            x_2_h - abs_value(self.anim_canvas.height, 1),
            y_1_h,
            triangle_endpoint_x_h,
            triangle_endpoint_y_h,
        )

        # vertical line
        self.anim_canvas[1].line_width = 1.5
        draw_line_with_strokes(
            canvas=self.anim_canvas[1],
            x_1=x_1_v,
            y_1=y_1_v,
            x_2=x_2_v,
            y_2=y_2_v,
            len_strokes=abs_value(self.anim_canvas.height, 2),
            num_strokes=5,
            alpha=40,
            direction_strokes="left",
        )

        self.anim_canvas[1].line_width = 1.5

        # triangle on vertical line
        triangle_endpoint_x_v = x_1_v + abs_value(self.anim_canvas.height, 5)
        triangle_endpoint_y_v = y_1_v + ((y_2_v - y_1_v) / 2)
        self.anim_canvas[1].stroke_line(
            x_1_v,
            y_1_v + abs_value(self.anim_canvas.height, 1),
            triangle_endpoint_x_v,
            triangle_endpoint_y_v,
        )
        self.anim_canvas[1].stroke_line(
            x_2_v,
            y_2_v
            - abs_value(
                self.anim_canvas.height,
                1,
            ),
            triangle_endpoint_x_v,
            triangle_endpoint_y_v,
        )

        # make circles
        self.anim_canvas[1].line_width = 2.5
        self.anim_canvas[1].fill_style = "#FFFFFF"

        # horizontal
        radius_h = int(abs_value(self.anim_canvas.height, 1) / 1.5)
        self.anim_canvas[1].stroke_circle(
            x=triangle_endpoint_x_h,
            y=triangle_endpoint_y_h,
            radius=radius_h,
        )

        self.anim_canvas[1].fill_circle(
            x=triangle_endpoint_x_h,
            y=triangle_endpoint_y_h,
            radius=radius_h,
        )

        # vertical
        radius_v = int(abs_value(self.anim_canvas.height, 1) / 1.5)
        self.anim_canvas[1].stroke_circle(
            x=triangle_endpoint_x_v,
            y=triangle_endpoint_y_v,
            radius=radius_v,
        )

        # set anker point for rectanlge and circle
        self.radius_v = radius_v
        self.anker_point_rec = (triangle_endpoint_x_v, triangle_endpoint_y_v - radius_v)
        self.rec.width = abs_value(self.anim_canvas.height, 50)
        self.rec.height = self.radius_v * 2
        self.circ.radius = abs_value(self.anim_canvas.height, 10)

        self.circ.center = (
            self.rec.width + self.circ.radius,
            self.anker_point_rec[1] + self.radius_v,
        )

        # fill circle after rectangle
        self.anim_canvas[1].fill_style = "#FFFFFF"
        self.anim_canvas[1].fill_circle(
            x=triangle_endpoint_x_v,
            y=triangle_endpoint_y_v,
            radius=radius_v,
        )

        # translate for feder daempfer element
        self.anim_canvas[2].translate(triangle_endpoint_x_v, triangle_endpoint_y_v)
        self.anim_canvas[3].translate(triangle_endpoint_x_v, triangle_endpoint_y_v)

        # translate for convenience --> change later
        self.anim_canvas[1].translate(triangle_endpoint_x_v, triangle_endpoint_y_v)

        # set line width for feder daempfer element
        self.anim_canvas[1].line_width = 1.5
        self.anim_canvas[2].line_width = 1.5
        self.anim_canvas[3].line_width = 1.5

        # set some coordinates
        self.bearings_point = (
            triangle_endpoint_x_h - triangle_endpoint_x_v,
            triangle_endpoint_y_h - triangle_endpoint_y_v + radius_h,
        )
        self.triangle_endpoint_x = triangle_endpoint_x_v
        self.triangle_endpoint_y = triangle_endpoint_y_v
        self.mid_point = triangle_endpoint_x_h

        # top part of feder daempfer element
        self.p_3 = ghetto_feder_daempfer_element_top(
            canvas=self.anim_canvas[1],
            anker_point_top=self.bearings_point,
            fork_width=abs_value(self.anim_canvas.width, 10),
            anker_point_extension=abs_value(self.anim_canvas.width, 5),
            daempfer_fork_extension=abs_value(self.anim_canvas.width, 5),
            daempfer_fork_length=abs_value(self.anim_canvas.width, 10),
            daempfer_fork_width=abs_value(self.anim_canvas.width, 5),
            direction="vertical",
        )

    def _draw_first_frame(self):
        # animate first frame
        first_sol_vis = self.solution[DEFAULT_FRAME]
        self.draw_rotating_angle(-first_sol_vis)
        # feder daempfer element
        self.ghetto_feder_daempfer_element()

    def _calculate(self):
        """Function to calculate the solution given the current inputs."""
        # clear visual representation
        self.anim_canvas[0].clear()

        # calculate
        solution = self.calculator.integrate(
            self.calculator.calculate,
            self.start_deflection,  # START_DEFLECTION,
            self.start_velocity,  # START_VELOCITY,
            self.t,  # t
            self.c,  # c
            self.d,  # d
            self.mass,  # m
        )
        self.solution = solution[:, 0]
        return solution[:, 0]

    def _animate_visual(self):
        # animate current frame for visual
        curr_sol_vis = self.solution[self.frame]
        self.draw_rotating_angle(-curr_sol_vis)

        self.anim_canvas[2].clear()
        self.ghetto_feder_daempfer_element()
        # self.feder_daempfer_element(curr_sol_vis)

    def ghetto_feder_daempfer_element(self):
        # translate spring anker point
        self.spring_anker_point = (
            self.spring_anker_point[0] - self.triangle_endpoint_x,
            self.spring_anker_point[1] - self.triangle_endpoint_y,
        )

        with hold_canvas():
            self.anim_canvas[2].clear_rect(
                -self.triangle_endpoint_x,
                -self.triangle_endpoint_y,
                self.anim_canvas.width,
                self.anim_canvas.height,
            )

            # horizontal line bottom element
            width = abs_value(self.anim_canvas.width, 5)
            height = abs_value(self.anim_canvas.width, 2)
            self.anim_canvas[2].stroke_line(
                self.spring_anker_point[0] - width,
                self.spring_anker_point[1] - height,
                self.spring_anker_point[0] + width,
                self.spring_anker_point[1] - height,
            )

            # inside fork thing
            self.anim_canvas[2].stroke_line(
                self.spring_anker_point[0] - width,
                self.spring_anker_point[1] - height,
                self.spring_anker_point[0] - width,
                self.spring_anker_point[1]
                - height
                - abs_value(self.anim_canvas.width, 10),
            )
            self.anim_canvas[2].stroke_line(
                self.spring_anker_point[0]
                - width
                - abs_value(self.anim_canvas.width, 1),
                self.spring_anker_point[1]
                - height
                - abs_value(self.anim_canvas.width, 10),
                self.spring_anker_point[0]
                - width
                + abs_value(self.anim_canvas.width, 1),
                self.spring_anker_point[1]
                - height
                - abs_value(self.anim_canvas.width, 10),
            )

            # small vertical line
            self.anim_canvas[2].stroke_line(
                self.spring_anker_point[0],
                self.spring_anker_point[1] - height,
                self.spring_anker_point[0],
                self.spring_anker_point[1],
                # + abs_value(self.anim_canvas.width, 1),  # little padding
            )

        # draw spring
        x_coords, y_coords = spring_module.spring(
            (
                self.spring_anker_point[0] + width,
                self.spring_anker_point[1] - height,
            ),  # bottom part
            (self.p_3[0], self.p_3[1]),  # upper part
            self.spring_nodes,
            self.spring_width,
        )
        spring_module.draw_spring(
            canvas=self.anim_canvas[3],
            x_coords=x_coords,
            y_coords=y_coords,
            spring_anker_point=self.spring_anker_point,
            width_offset=width,
            height_offset=height,
            clear_x=-self.triangle_endpoint_x,
            clear_y=-self.triangle_endpoint_y,
        )
        # with hold_canvas():
        #     self.anim_canvas[3].clear_rect(
        #         -self.triangle_endpoint_x,
        #         -self.triangle_endpoint_y,
        #         self.anim_canvas.width,
        #         self.anim_canvas.height,
        #     )
        #     if np.isscalar(x_coords):
        #         self.anim_canvas[3].stroke_line(
        #             self.spring_anker_point[0] + width,
        #             self.spring_anker_point[1] - height,
        #             x_coords,
        #             y_coords,
        #         )
        #         self.anim_canvas[3].stroke_line(
        #             x_coords,
        #             y_coords,
        #             x_coords + abs_value(self.anim_canvas.width, 2),
        #             y_coords,
        #         )
        #     else:
        #         self.anim_canvas[3].stroke_lines(list(zip(x_coords, y_coords)))
        #         index = len(x_coords) - 1
        #         self.anim_canvas[3].stroke_line(
        #             x_coords[index],
        #             y_coords[index],
        #             x_coords[index] + abs_value(self.anim_canvas.width, 2),
        #             y_coords[index],
        #         )

        return None

    def draw_rotating_angle(self, angle):
        """Function to draw the rectangle and circle at given angle.

        Args:
            angle (int): Current angle.
        """
        # Calculate the coordinates of the four corners
        fixed_x = self.anker_point_rec[0]
        fixed_y = self.anker_point_rec[1] + self.radius_v
        top_left = (
            fixed_x,
            fixed_y - self.rec.height / 2,
        )
        top_right = (
            fixed_x + self.rec.width,
            fixed_y - self.rec.height / 2,
        )
        bottom_left = (
            fixed_x,
            fixed_y + self.rec.height / 2,
        )
        bottom_right = (
            fixed_x + self.rec.width,
            fixed_y + self.rec.height / 2,
        )

        # Rotate the corners around the fixed point
        top_left_rot = rotate_point(*top_left, fixed_x, fixed_y, angle)
        top_right_rot = rotate_point(*top_right, fixed_x, fixed_y, angle)
        bottom_left_rot = rotate_point(*bottom_left, fixed_x, fixed_y, angle)
        bottom_right_rot = rotate_point(*bottom_right, fixed_x, fixed_y, angle)

        # anker point for spring
        self.spring_anker_point = (
            self.mid_point,  # (top_left_rot[0] + top_right_rot[0]) / 2,
            (top_left_rot[1] + top_right_rot[1]) / 2,
        )

        self.anim_canvas[0].line_width = 1.5
        with hold_canvas():
            self.anim_canvas[0].clear()
            # draw the rectangle using the rotated points
            self.anim_canvas[0].fill_style = "#bebebe"
            self.anim_canvas[0].fill_polygon(
                [top_left_rot, top_right_rot, bottom_right_rot, bottom_left_rot]
            )
            self.anim_canvas[0].stroke_polygon(
                [top_left_rot, top_right_rot, bottom_right_rot, bottom_left_rot]
            )

            # get center of circle
            circle_center = rotate_point(
                fixed_x + self.rec.width, fixed_y, fixed_x, fixed_y, angle
            )

            # draw circle
            self.anim_canvas[0].fill_circle(
                circle_center[0], circle_center[1], self.circ.radius
            )
            self.anim_canvas[0].stroke_circle(
                circle_center[0], circle_center[1], self.circ.radius
            )
