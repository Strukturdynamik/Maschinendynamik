import math
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
    NUM_DATAPOINTS_3,
    NUM_TIME_UNITS_AUFGABE_3,
    DEFAULT_FRAME,
    DEFAULT_M_3,
    DEFAULT_MU_3,
    DEFAULT_EPS_3,
    DEFAULT_Z0_3,
    DEFAULT_Z0D_3,
    DEFAULT_OMEGA_3,
    DEFAULT_ALPHA_3,
)

"""Module to animate the mechanical oscillation system of Übung 2, Aufgabe 1.
"""


class Aufgabe3(AnimationInstance):
    def __init__(self, calculator):
        super().__init__()
        self.calculator = calculator
        self.m = DEFAULT_M_3
        self.m_u = DEFAULT_MU_3
        self.eps = DEFAULT_EPS_3
        self.z0 = DEFAULT_Z0_3
        self.z0d = DEFAULT_Z0D_3
        self.omega = DEFAULT_OMEGA_3
        self.alpha = DEFAULT_ALPHA_3
        self.frame = DEFAULT_FRAME
        self.t = np.linspace(0, NUM_TIME_UNITS_AUFGABE_3, NUM_DATAPOINTS_3)
        self.spring_nodes = 20
        self.angle1_rad = math.radians(45)
        self.angle2_rad = math.radians(135)

    def _initial_visual(self):
        """Draw the inital visual for the visual representation of oscillation."""

        self.anim_canvas[6].line_width = 2.0
        # coordinates for the open square
        self.left_x1 = abs_value(self.anim_canvas.width, 30)
        self.left_y1 = abs_value(self.anim_canvas.width, 30)
        self.left_x2 = abs_value(self.anim_canvas.width, 30)
        self.left_y2 = abs_value(self.anim_canvas.width, 90)

        self.right_x1 = abs_value(self.anim_canvas.width, 60)
        self.right_y1 = abs_value(self.anim_canvas.width, 30)
        self.right_x2 = abs_value(self.anim_canvas.width, 60)
        self.right_y2 = abs_value(self.anim_canvas.width, 90)

        # draw the open square with lines
        draw_line_with_strokes(
            self.anim_canvas[6],
            self.left_x1,
            self.left_y1,
            self.left_x2,
            self.left_y2,
            len_strokes=abs_value(self.anim_canvas.width, 5),
            num_strokes=15,
            angle=30,
            direction_strokes="left",
        )
        draw_line_with_strokes(
            self.anim_canvas[6],
            self.left_x2,
            self.left_y2,
            self.right_x2,
            self.right_y2,
            len_strokes=abs_value(self.anim_canvas.width, 5),
            num_strokes=15,
            angle=30,
            direction_strokes="bottom",
        )
        draw_line_with_strokes(
            self.anim_canvas[6],
            self.right_x1,
            self.right_y1,
            self.right_x2,
            self.right_y2,
            len_strokes=abs_value(self.anim_canvas.width, 5),
            num_strokes=15,
            angle=210,
            direction_strokes="right",
        )

        # draw arrow with z label
        x1 = abs_value(self.anim_canvas.width, 15)
        y1 = abs_value(self.anim_canvas.width, 60)
        x2 = abs_value(self.anim_canvas.width, 15)
        y2 = abs_value(self.anim_canvas.width, 50)

        self.draw_arrow_a3(self.anim_canvas[6], x1, y1, x2, y2)

    def _calculate(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        # acc
        self.sol_acc = self.calculator.integrate(
            self.calculator.state_space_accelerated,
            self.t,
            self.z0,
            self.z0d,
            self.m_u,
            self.m,
            self.d,
            self.c,
            self.eps,
            self.alpha,
        )
        self.sol_acc_force = self.eps * np.sin(0.5 * self.alpha * self.t**2)

        # steady
        self.sol_steady = self.calculator.integrate(
            self.calculator.state_space_steady,
            self.t,
            self.z0,
            self.z0d,
            self.m_u,
            self.m,
            self.d,
            self.c,
            self.eps,
            self.omega,
        )
        self.sol_steady_force = self.eps * np.sin(self.omega * self.t)

        if self.mode == "Acceleration":
            self.solution = self.sol_acc
        elif self.mode == "Steady State":
            self.solution = self.sol_steady
        else:
            print(self.mode)
            raise ValueError("undefined state")

        return self.sol_acc, self.sol_acc_force, self.sol_steady, self.sol_steady_force

    def calc_bode_diagram(self):
        b2 = -self.m_u / self.m
        delta = self.d / (2 * self.m)
        omega_0 = np.sqrt(self.c / self.m)
        omega_vec = np.linspace(0, 2 * omega_0, self.t.size)

        num = np.array([b2, 0, 0])
        den = np.array([1, 2 * delta, omega_0**2])
        G = signal.TransferFunction(num, den)

        # bode-values
        _, mag, phase = signal.bode(G, omega_vec)
        mag = 10 ** (mag / 20)  # Umrechnung von dB auf abs

        G_undamped = signal.TransferFunction([b2, 0, 0], [1, 0, omega_0**2])
        _, mag_undamped, _ = signal.bode(G_undamped, omega_vec)
        mag_undamped = 10 ** (mag_undamped / 20)

        return omega_vec, omega_0, mag, mag_undamped, phase

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
            self.left_y1,
            self.left_y1 + abs_value(self.anim_canvas.width, 14),
        )

        with hold_canvas():
            self.anim_canvas[0].clear()  # big circle and small circle
            self.anim_canvas[2].clear()  # rect
            self.anim_canvas[3].clear()  # feder daempfer element
            self.anim_canvas[4].clear()  # spring
            # animate circle
            self.circ_zero_pos = (
                (self.left_x1 + self.right_x1) / 2,
                self.left_y1 - abs_value(self.anim_canvas.width, 15),
            )
            self.radius = (
                self.right_x1 - self.left_x1 - abs_value(self.anim_canvas.width, 4)
            ) / 2
            self.anim_canvas[0].stroke_circle(
                x=self.circ_zero_pos[0],
                y=mapped_curr_pos - abs_value(self.anim_canvas.width, 15),
                radius=self.radius,
            )
            # smaller circle inside big circle
            self.anim_canvas[0].stroke_circle(
                x=self.circ_zero_pos[0],
                y=mapped_curr_pos - abs_value(self.anim_canvas.width, 15),
                radius=abs_value(self.anim_canvas.width, 1),
            )

            # animate square
            square_left_upper_corner = (
                self.left_x1 + abs_value(self.anim_canvas.width, 2),
                mapped_curr_pos,
            )
            self.anim_canvas[2].fill_rect(
                square_left_upper_corner[0],
                square_left_upper_corner[1],
                self.square_width,
            )
            self.anim_canvas[2].stroke_rect(
                square_left_upper_corner[0],
                square_left_upper_corner[1],
                self.square_width,
            )

            # draw lines from circle to rect
            self.point1 = (
                self.circ_zero_pos[0] + self.radius * math.cos(self.angle1_rad),
                mapped_curr_pos
                - abs_value(self.anim_canvas.width, 15)
                + self.radius * math.sin(self.angle1_rad),
            )
            self.point2 = (
                self.circ_zero_pos[0] + self.radius * math.cos(self.angle2_rad),
                mapped_curr_pos
                - abs_value(self.anim_canvas.width, 15)
                + self.radius * math.sin(self.angle2_rad),
            )

            self.anim_canvas[0].stroke_line(
                self.point1[0],
                self.point1[1],
                square_left_upper_corner[0] + self.square_width,
                square_left_upper_corner[1],
            )

            self.anim_canvas[0].stroke_line(
                self.point2[0],
                self.point2[1],
                square_left_upper_corner[0],
                square_left_upper_corner[1],
            )

            # animate spring and feder daempfer element
            bottom_anker_point = [(self.left_x1 + self.right_x1) / 2, self.left_y2]
            anker_point_extension = abs_value(self.anim_canvas.width, 3)
            fork_width = abs_value(self.anim_canvas.width, 10)
            spring_anker_point_bottom = ghetto_feder_daempfer_element_bottom(
                canvas=self.anim_canvas[3],
                anker_point_bottom=bottom_anker_point,
                bottom_fork_extension=anker_point_extension,
                bottom_fork_width=fork_width,
                daempfer_length=abs_value(self.anim_canvas.width, 6),
                daempfer_width=abs_value(self.anim_canvas.width, 3),
                direction="vertical",
            )

            top_anker_point = [
                bottom_anker_point[0],
                mapped_curr_pos + self.square_width,
            ]
            anker_point_extension = abs_value(self.anim_canvas.width, 3)
            fork_width = abs_value(self.anim_canvas.width, 10)
            spring_anker_point_top = ghetto_feder_daempfer_element_top(
                canvas=self.anim_canvas[3],
                anker_point_top=top_anker_point,
                fork_width=fork_width,
                anker_point_extension=anker_point_extension,
                daempfer_fork_extension=abs_value(self.anim_canvas.width, 2),
                daempfer_fork_length=abs_value(self.anim_canvas.width, 10),
                daempfer_fork_width=abs_value(self.anim_canvas.width, 5),
                direction="vertical",
            )

            # draw spring
            spring_nodes = 15
            spring_width = abs_value(self.anim_canvas.width, 4)
            x_coords, y_coords = spring_module.spring(
                (
                    spring_anker_point_top[0],
                    spring_anker_point_top[1],
                ),
                (
                    spring_anker_point_bottom[0],
                    spring_anker_point_bottom[1],
                ),  # upper part
                spring_nodes,
                spring_width,
            )
            # draw spring
            self.anim_canvas[4].line_width = 1.5
            spring_module.draw_spring(
                canvas=self.anim_canvas[4],
                x_coords=x_coords,
                y_coords=y_coords,
                spring_anker_point=spring_anker_point_top,
                width_offset=0,
                height_offset=0,
                clear_x=0,
                clear_y=0,
            )

            # # Compute dot position based on current angle
            # point_x = self.circ_zero_pos[0] + self.radius * np.cos(curr_sol_vis)
            # point_y = self.circ_zero_pos[1] + self.radius * np.sin(curr_sol_vis)

            # # Draw the rotating dot
            # self.anim_canvas[5].fill_circle(
            #     point_x, point_y, abs_value(self.anim_canvas.width / 2, 1)
            # )

        return None

    def _draw_first_frame(self):
        self.anim_canvas[0].line_width = 1.5
        # draw circle in zero pos
        self.circ_zero_pos = (
            (self.left_x1 + self.right_x1) / 2,
            self.left_y1 - abs_value(self.anim_canvas.width, 15),
        )
        self.radius = (
            self.right_x1 - self.left_x1 - abs_value(self.anim_canvas.width, 4)
        ) / 2
        self.anim_canvas[0].stroke_circle(
            x=self.circ_zero_pos[0], y=self.circ_zero_pos[1], radius=self.radius
        )
        # smaller circle inside big circle
        self.anim_canvas[0].stroke_circle(
            x=self.circ_zero_pos[0],
            y=self.circ_zero_pos[1],
            radius=abs_value(self.anim_canvas.width, 1),
        )

        self.anim_canvas[2].line_width = 1.5
        self.anim_canvas[2].fill_style = "#bebebe"
        # draw square in zero position
        self.square_width = (
            self.right_x1 - self.left_x1 - abs_value(self.anim_canvas.width, 4)
        )
        square_left_upper_corner = (
            self.left_x1 + abs_value(self.anim_canvas.width, 2),
            self.left_y1,
        )
        self.anim_canvas[2].fill_rect(
            square_left_upper_corner[0], square_left_upper_corner[1], self.square_width
        )
        self.anim_canvas[2].stroke_rect(
            square_left_upper_corner[0], square_left_upper_corner[1], self.square_width
        )

        # draw text in zero position
        # self.anim_canvas[2].fill_style = "black"
        # self.anim_canvas[2].font = f"italic bold {abs_value(self.anim_canvas.width, 5)}px euklid"
        # square_middle_point = (square_left_upper_corner[0]+square_width/2, square_left_upper_corner[1]+square_width/2)
        # self.anim_canvas[2].fill_text("m0", square_middle_point[0] - abs_value(self.anim_canvas.width, 1), square_middle_point[1], max_width=abs_value(self.anim_canvas.width, 5))

        # draw lines from circle to rect

        self.point1 = (
            self.circ_zero_pos[0] + self.radius * math.cos(self.angle1_rad),
            self.circ_zero_pos[1] + self.radius * math.sin(self.angle1_rad),
        )
        self.point2 = (
            self.circ_zero_pos[0] + self.radius * math.cos(self.angle2_rad),
            self.circ_zero_pos[1] + self.radius * math.sin(self.angle2_rad),
        )

        self.anim_canvas[0].stroke_line(
            self.point1[0],
            self.point1[1],
            self.left_x1 + abs_value(self.anim_canvas.width, 2) + self.square_width,
            self.left_y1,
        )
        self.anim_canvas[0].stroke_line(
            self.point2[0],
            self.point2[1],
            self.left_x1 + abs_value(self.anim_canvas.width, 2),
            self.left_y1,
        )

        # draw the feder daempfer element
        self.anim_canvas[3].line_width = 1.5
        bottom_anker_point = [(self.left_x1 + self.right_x1) / 2, self.left_y2]
        anker_point_extension = abs_value(self.anim_canvas.width, 3)
        fork_width = abs_value(self.anim_canvas.width, 10)
        spring_anker_point_bottom = ghetto_feder_daempfer_element_bottom(
            canvas=self.anim_canvas[3],
            anker_point_bottom=bottom_anker_point,
            bottom_fork_extension=anker_point_extension,
            bottom_fork_width=fork_width,
            daempfer_length=abs_value(self.anim_canvas.width, 6),
            daempfer_width=abs_value(self.anim_canvas.width, 3),
            direction="vertical",
        )

        top_anker_point = [bottom_anker_point[0], self.left_y1 + self.square_width]
        anker_point_extension = abs_value(self.anim_canvas.width, 3)
        fork_width = abs_value(self.anim_canvas.width, 10)
        spring_anker_point_top = ghetto_feder_daempfer_element_top(
            canvas=self.anim_canvas[3],
            anker_point_top=top_anker_point,
            fork_width=fork_width,
            anker_point_extension=anker_point_extension,
            daempfer_fork_extension=abs_value(self.anim_canvas.width, 2),
            daempfer_fork_length=abs_value(self.anim_canvas.width, 10),
            daempfer_fork_width=abs_value(self.anim_canvas.width, 5),
            direction="vertical",
        )

        # draw spring
        spring_nodes = 15
        spring_width = abs_value(self.anim_canvas.width, 4)
        x_coords, y_coords = spring_module.spring(
            (
                spring_anker_point_top[0],
                spring_anker_point_top[1],
            ),
            (
                spring_anker_point_bottom[0],
                spring_anker_point_bottom[1],
            ),  # upper part
            spring_nodes,
            spring_width,
        )
        # draw spring
        self.anim_canvas[4].line_width = 1.5
        spring_module.draw_spring(
            canvas=self.anim_canvas[4],
            x_coords=x_coords,
            y_coords=y_coords,
            spring_anker_point=spring_anker_point_top,
            width_offset=0,
            height_offset=0,
            clear_x=0,
            clear_y=0,
        )

    def draw_arrow_a3(self, canvas, x1, y1, x2, y2):
        # draw main line
        canvas.stroke_line(x1, y1, x2, y2)

        # calculate the angle of the line
        angle = math.atan2(y2 - y1, x2 - x1)

        # calculate coordinates for the two arrowhead lines
        alpha = 30
        arrow_angle_rad = math.radians(alpha)
        arrow_lines_length = abs_value(canvas.width, 3)

        x3 = x2 - arrow_lines_length * math.cos(angle - arrow_angle_rad)
        y3 = y2 - arrow_lines_length * math.sin(angle - arrow_angle_rad)

        x4 = x2 - arrow_lines_length * math.cos(angle + arrow_angle_rad)
        y4 = y2 - arrow_lines_length * math.sin(angle + arrow_angle_rad)

        # strke arrow head lines
        canvas.stroke_line(x2, y2, x3, y3)
        canvas.stroke_line(x2, y2, x4, y4)

        # draw base line
        base_length = abs_value(canvas.width, 5)
        canvas.stroke_line(x1 - base_length / 2, y1, x1 + base_length / 2, y1)

        # add angled lines
        num_base_strokes = 5
        spacing_padding = 2
        line_space = math.ceil(base_length / num_base_strokes) + spacing_padding
        stroke_len = abs_value(canvas.width, 2)
        # calculate offsets
        alpha_offset = 40
        y_offset = math.cos(alpha_offset) * stroke_len
        x_offset = math.sin(alpha_offset) * stroke_len

        temp_start = (x1 - base_length / 2, y1)
        counter = 0
        while counter < num_base_strokes:
            canvas.stroke_line(
                temp_start[0],
                temp_start[1],
                temp_start[0] - x_offset,
                temp_start[1] - y_offset,
            )
            temp_start = (temp_start[0] + line_space, temp_start[1])
            counter += 1

        # label
        description_padding_x = 4
        description_padding_y = 3
        description_style = "italic"
        description_font_size = 5
        description_max_width = abs_value(canvas.width, 4)
        center = (
            x1 - abs_value(canvas.width, description_padding_x),
            y1 - abs_value(canvas.height, description_padding_y),
        )
        canvas.line_width = 0.9
        canvas.font = f"{description_style} {abs_value(canvas.width, description_font_size)}px euklid"
        canvas.fill_text(
            "y",
            center[0],
            center[1],
            max_width=abs_value(canvas.width, description_max_width),
        )
