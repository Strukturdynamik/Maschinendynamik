from ipycanvas import hold_canvas
from ...utils.helper import (
    abs_value,
    ghetto_feder_daempfer_element_top,
    ghetto_feder_daempfer_element_bottom,
    draw_line_with_strokes,
    rotate_point,
)
from .anim_superclass import AnimationInstance
from ..modules.shapes import Circle
from ...utils.ext_utils.spring import spring_module
from ...utils.constants import (
    A4_U1_T,
    DEFAULT_FRAME,
    A4_U1_DEFAULT_C,
    A4_U1_DEFAULT_D,
)

"""Module to animate the mechanical oscillation system of Übung 1, Aufgabe 4.

Reference:
    See "documentation\aufgaben_pdfs\A4_U1.pdf" for details.

This animation models a pendulum-like oscillating rectangle with an attached
circular mass and a vertical spring-damper element. It handles:

- Numerical calculation of angular displacement over time
- Initialization of static geometry (reference lines, anchor points)
- Drawing and animating the rotating block and attached circle
- Constructing and updating the spring-damper connection
- Integrating system parameters (mass, damping, stiffness) from defaults
"""


class Aufgabe4(AnimationInstance):
    def __init__(self, calculator, start_deflection, start_velocity, mass):
        super().__init__()
        self.calculator = calculator
        self.c = A4_U1_DEFAULT_C
        self.d = A4_U1_DEFAULT_D
        self.frame = DEFAULT_FRAME
        self.t = A4_U1_T
        self.start_deflection = start_deflection
        self.start_velocity = start_velocity
        self.mass = mass
        self.circ = Circle(center=(-1, -1), radius=-1)
        self.spring_nodes = 20

    def _initial_visual(self):
        """
        Draws the static background and reference geometry of the system.

        Includes:
        - Horizontal and vertical reference lines with stroke patterns
        - Bearing triangles at the reference lines
        - Circular anchor points at pivot locations
        - Rectangle dimensions and attached circle
        - Canvas layer translations for rotation about pivot

        Called once before the first frame is rendered.
        """

        # Set spring visual width
        self.spring_width = abs_value(self.anim_canvas.width, 5)

        # Coordinates for horizontal and vertical reference lines
        x_1_h = abs_value(self.anim_canvas.height, 30)
        y_1_h = abs_value(self.anim_canvas.height, 20)
        x_2_h = abs_value(self.anim_canvas.height, 40)
        y_2_h = abs_value(self.anim_canvas.height, 20)

        x_1_v = abs_value(self.anim_canvas.height, 10)
        y_1_v = abs_value(self.anim_canvas.height, 50)
        x_2_v = abs_value(self.anim_canvas.height, 10)
        y_2_v = abs_value(self.anim_canvas.height, 60)

        # Draw horizontal reference line
        self.anim_canvas[1].line_width = 2.0
        draw_line_with_strokes(
            canvas=self.anim_canvas[1],
            x_1=x_1_h,
            y_1=y_1_h,
            x_2=x_2_h,
            y_2=y_2_h,
            len_strokes=abs_value(self.anim_canvas.height, 2),
            num_strokes=5,
            angle=30,
            direction_strokes="top",
        )
        self.anim_canvas[1].line_width = 1.5

        # Draw triangle on horizontal line
        self.triangle_endpoint_x_h = x_1_h + ((x_2_h - x_1_h) / 2)
        self.triangle_endpoint_y_h = y_1_h + abs_value(self.anim_canvas.height, 5)
        self.anim_canvas[1].stroke_line(
            x_1_h + abs_value(self.anim_canvas.height, 1),
            y_1_h,
            self.triangle_endpoint_x_h,
            self.triangle_endpoint_y_h,
        )
        self.anim_canvas[1].stroke_line(
            x_2_h - abs_value(self.anim_canvas.height, 1),
            y_1_h,
            self.triangle_endpoint_x_h,
            self.triangle_endpoint_y_h,
        )

        # Draw vertical reference line
        draw_line_with_strokes(
            canvas=self.anim_canvas[1],
            x_1=x_1_v,
            y_1=y_1_v,
            x_2=x_2_v,
            y_2=y_2_v,
            len_strokes=abs_value(self.anim_canvas.height, 2),
            num_strokes=5,
            angle=40,
            direction_strokes="left",
        )

        # Draw triangle on vertical line
        self.triangle_endpoint_x_v = x_1_v + abs_value(self.anim_canvas.height, 5)
        self.triangle_endpoint_y_v = y_1_v + ((y_2_v - y_1_v) / 2)
        self.anim_canvas[1].stroke_line(
            x_1_v,
            y_1_v + abs_value(self.anim_canvas.height, 1),
            self.triangle_endpoint_x_v,
            self.triangle_endpoint_y_v,
        )
        self.anim_canvas[1].stroke_line(
            x_2_v,
            y_2_v - abs_value(self.anim_canvas.height, 1),
            self.triangle_endpoint_x_v,
            self.triangle_endpoint_y_v,
        )

        # Draw anchor circles
        self.anim_canvas[1].line_width = 2.5
        self.anim_canvas[1].fill_style = "#FFFFFF"
        self.radius_h = int(abs_value(self.anim_canvas.height, 1) / 1.5)
        self.anim_canvas[1].stroke_circle(
            x=self.triangle_endpoint_x_h,
            y=self.triangle_endpoint_y_h,
            radius=self.radius_h,
        )
        self.anim_canvas[1].fill_circle(
            x=self.triangle_endpoint_x_h,
            y=self.triangle_endpoint_y_h,
            radius=self.radius_h,
        )

        radius_v = int(abs_value(self.anim_canvas.height, 1) / 1.5)
        self.anim_canvas[1].stroke_circle(
            x=self.triangle_endpoint_x_v,
            y=self.triangle_endpoint_y_v,
            radius=radius_v,
        )
        self.anim_canvas[1].fill_circle(
            x=self.triangle_endpoint_x_v,
            y=self.triangle_endpoint_y_v,
            radius=radius_v,
        )

        # Set dimensions for dynamic rectangle and circle
        self.radius_v = radius_v
        self.anker_point_rec = (
            self.triangle_endpoint_x_v,
            self.triangle_endpoint_y_v - radius_v,
        )
        self.rec_width = abs_value(self.anim_canvas.height, 50)
        self.rec_height = self.radius_v * 2
        self.circ.radius = abs_value(self.anim_canvas.height, 10)
        self.circ.center = (
            self.rec_width + self.circ.radius,
            self.anker_point_rec[1] + self.radius_v,
        )

        # Set translations for different canvas layers
        for canvas_layer in [1, 2, 3]:
            self.anim_canvas[canvas_layer].translate(
                self.triangle_endpoint_x_v, self.triangle_endpoint_y_v
            )
            self.anim_canvas[canvas_layer].line_width = 1.5

        # Store key reference points
        self.bearings_point = (
            self.triangle_endpoint_x_h - self.triangle_endpoint_x_v,
            self.triangle_endpoint_y_h - self.triangle_endpoint_y_v + self.radius_h,
        )
        self.triangle_endpoint_x = self.triangle_endpoint_x_v
        self.triangle_endpoint_y = self.triangle_endpoint_y_v
        self.mid_point = self.triangle_endpoint_x_h

    def _draw_first_frame(self):
        """
        Renders the very first frame of the animation.

        - Positions the rectangle and circle at the initial angular deflection
        - Constructs the initial spring-damper connection
        """
        first_sol_vis = self.solution[DEFAULT_FRAME]
        self.draw_rotating_angle(-first_sol_vis)
        self.ghetto_spring_damper_element()

    def _calculate(self):
        """
        Computes the system’s angular displacement solution over time.

        Uses the provided calculator to numerically integrate the system’s
        equations of motion based on:
        - Initial angular displacement
        - Initial angular velocity
        - Damping constant (c)
        - Stiffness constant (d)
        - Mass (m)

        Returns:
            list[float]: Angular deflections for each simulation timestep.
        """
        self.anim_canvas[0].clear()
        solution = self.calculator.integrate(
            self.calculator.calculate,
            self.start_deflection,
            self.start_velocity,
            self.t,
            self.c,
            self.d,
            self.mass,
        )
        self.solution = solution
        return solution

    def _animate_visual(self):
        """
        Updates the dynamic animation for the current frame.

        Steps:
        - Computes the current angular displacement
        - Rotates the rectangle and attached circle
        - Updates the spring-damper visualization
        """
        curr_sol_vis = self.solution[self.frame]
        self.draw_rotating_angle(-curr_sol_vis)
        self.ghetto_spring_damper_element()

    def ghetto_spring_damper_element(self):
        """
        Draws the spring-damper element between the moving rectangle and the
        fixed bearing for the current frame.

        Procedure:
        - Clears the spring-damper canvas layers
        - Recomputes anchor points based on current rectangle rotation
        - Draws damper forks and extension elements
        - Generates spring geometry between anchors and renders it

        Called on every frame update to keep spring-damper aligned with motion.
        """
        self.spring_anker_point = (
            self.spring_anker_point[0] - self.triangle_endpoint_x,
            self.spring_anker_point[1] - self.triangle_endpoint_y,
        )

        with hold_canvas():
            self.anim_canvas[3].clear_rect(
                -self.triangle_endpoint_x,
                -self.triangle_endpoint_y,
                self.anim_canvas.width,
                self.anim_canvas.height,
            )

            self.anim_canvas[2].clear_rect(
                -self.triangle_endpoint_x,
                -self.triangle_endpoint_y,
                self.anim_canvas[2].width,
                self.anim_canvas[2].height,
            )

            anker_point_extension = abs_value(self.anim_canvas.width, 3)
            fork_width = abs_value(self.anim_canvas.width, 10)

            spring_anker_point_bottom = ghetto_feder_daempfer_element_bottom(
                canvas=self.anim_canvas[3],
                anker_point_bottom=self.spring_anker_point,
                bottom_fork_extension=anker_point_extension,
                bottom_fork_width=fork_width,
                daempfer_length=abs_value(self.anim_canvas.width, 6),
                daempfer_width=abs_value(self.anim_canvas.width, 3),
                direction="vertical",
            )

            spring_anker_point_top = ghetto_feder_daempfer_element_top(
                canvas=self.anim_canvas[3],
                anker_point_top=self.bearings_point,
                fork_width=fork_width,
                anker_point_extension=anker_point_extension,
                daempfer_fork_extension=abs_value(self.anim_canvas.width, 2),
                daempfer_fork_length=abs_value(self.anim_canvas.width, 10),
                daempfer_fork_width=abs_value(self.anim_canvas.width, 5),
                direction="vertical",
            )

            # Draw spring
            self.anim_canvas[2].clear_rect(
                -self.triangle_endpoint_x,
                -self.triangle_endpoint_y,
                self.anim_canvas.width,
                self.anim_canvas.height,
            )
            x_coords, y_coords = spring_module.spring(
                spring_anker_point_bottom,
                spring_anker_point_top,
                self.spring_nodes,
                self.spring_width,
            )
            spring_module.draw_spring(
                canvas=self.anim_canvas[2],
                x_coords=x_coords,
                y_coords=y_coords,
                spring_anker_point=self.spring_anker_point,
                width_offset=5,
                height_offset=5,
                # clear_x=-self.triangle_endpoint_x,
                # clear_y=-self.triangle_endpoint_y,
            )

    def draw_rotating_angle(self, angle: float):
        """
        Rotates and draws the rectangle and attached circle by a given angle.

        Args:
            angle (float): Rotation angle (in radians, counterclockwise positive).

        Procedure:
        - Rotates rectangle corner coordinates about the pivot
        - Updates spring anchor point based on rectangle’s rotated geometry
        - Clears and redraws the rectangle at new angle
        - Draws the attached circle at the rotated end of the rectangle
        """
        fixed_x = self.anker_point_rec[0]
        fixed_y = self.anker_point_rec[1] + self.radius_v

        top_left = (fixed_x, fixed_y - self.rec_height / 2)
        top_right = (fixed_x + self.rec_width, fixed_y - self.rec_height / 2)
        bottom_left = (fixed_x, fixed_y + self.rec_height / 2)
        bottom_right = (fixed_x + self.rec_width, fixed_y + self.rec_height / 2)

        top_left_rot = rotate_point(*top_left, fixed_x, fixed_y, angle)
        top_right_rot = rotate_point(*top_right, fixed_x, fixed_y, angle)
        bottom_left_rot = rotate_point(*bottom_left, fixed_x, fixed_y, angle)
        bottom_right_rot = rotate_point(*bottom_right, fixed_x, fixed_y, angle)

        self.spring_anker_point = (
            self.mid_point,
            (top_left_rot[1] + top_right_rot[1]) / 2,
        )

        self.anim_canvas[0].line_width = 1.5
        with hold_canvas():
            self.anim_canvas[0].clear()
            self.anim_canvas[0].fill_style = "#bebebe"
            self.anim_canvas[0].fill_polygon(
                [top_left_rot, top_right_rot, bottom_right_rot, bottom_left_rot]
            )
            self.anim_canvas[0].stroke_polygon(
                [top_left_rot, top_right_rot, bottom_right_rot, bottom_left_rot]
            )

            circle_center = rotate_point(
                fixed_x + self.rec_width, fixed_y, fixed_x, fixed_y, angle
            )
            self.anim_canvas[0].fill_circle(
                circle_center[0], circle_center[1], self.circ.radius
            )
            self.anim_canvas[0].stroke_circle(
                circle_center[0], circle_center[1], self.circ.radius
            )
