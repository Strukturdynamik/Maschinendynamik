import time
import numpy as np
from typing import Tuple, Any, List
from ipycanvas import Canvas, hold_canvas

from .anim_modules import Shape
from ...utils.ext_utils.spring import spring_module
from ...utils.helper import abs_value

"""Module containing specific shapes implementing the Shape superclass.
"""


class Circle(Shape):
    def __init__(
        self,
        center: Tuple[int, int],
        radius: int | Any = None,
    ) -> None:
        """Circle class.

        Args:
            center (Tuple[int, int]): Center position of circle.
                Defaults to None.
            radius (int | Any, optional): Radius of circle.
                Defaults to None.
        """
        super().__init__(center=center, radius=radius)

    def draw(self, canvas: Canvas, pos: Tuple[int, int], fill: bool) -> None:
        """Function to draw circle at given position.

        Args:
            canvas (Canvas): Canvas to draw on.
            pos (Tuple[int, int]): Position where circle is drawn.
            fill (bool): Determines if the shape should be filled in addition
                to being drawn.
        """
        with hold_canvas():
            # canvas.clear()
            canvas.stroke_circle(x=pos[0], y=pos[0], radius=self.radius)
            if fill:
                canvas.fill_circle(x=pos[0], y=pos[0], radius=self.radius)
            # time.sleep(0.02)


class Rectangle(Shape):
    def __init__(
        self,
        width: int | Any = None,
        height: int | Any = None,
    ) -> None:
        """Rectangle class.

        Args:
            width (int | Any, optional): Width of rectangle.
                Defaults to None.
            height (int | Any, optional): Height of rectangle.
                Defaults to None.
        """
        super().__init__(width=width, height=height)

    def draw(
        self,
        canvas: Canvas,
        pos: Tuple[int, int],
        fill: bool,
    ) -> None:
        """Function to draw rectangle at given position.

        Args:
            canvas (Canvas): Canvas to draw on.
            pos (Tuple[int, int]): Position where rectangle is drawn.
            fill (bool): Determines if the shape should be filled in addition
                to being drawn.
        """
        # canvas.fill_style = "#bebebe"
        # canvas.font = f"{abs_value(canvas.width, 3)}px euklid"
        with hold_canvas():
            # canvas.clear()
            canvas.stroke_rect(
                x=pos[0] + abs_value(canvas.width, 2),
                y=pos[1] - self.height / 2,
                width=self.width,
                height=self.height,
            )
            if fill:
                canvas.fill_rect(
                    x=pos[0] + abs_value(canvas.width, 2),
                    y=pos[1] - self.height / 2,
                    width=self.width,
                    height=self.height,
                )


class Triangle(Shape):
    def __init__(
        self,
        A: Tuple[int, int] | Any = None,
        B: Tuple[int, int] | Any = None,
        C: Tuple[int, int] | Any = None,
    ) -> None:
        """Triangle class.

        Args:
            A (Tuple[int, int] | Any, optional): Point A. Defaults to None.
            B (Tuple[int, int] | Any, optional): Point B. Defaults to None.
            C (Tuple[int, int] | Any, optional): Point C. Defaults to None.
        """
        super().__init__(A=A, B=B, C=C)

    def draw(self, canvas: Canvas, pos: Tuple[int, int], fill: bool) -> None:
        """_summary_

        Args:
            canvas (Canvas): _description_
            pos (Tuple[int, int]): _description_
        """
        pass


class Spring(Shape):
    def __init__(
        self, start: Tuple[int, int], end: Tuple[int, int], nodes: int, width: float
    ) -> None:
        """Spring will be drawn from start to endpoint. See
            external_utilities for documentation of spring.

        Args:
            start (List[int]): Start point for spring.
            end (List[int]): End point for spring.
            nodes (int): Number of nodes representing the
                coils of the spring.
            width (float): Width of spring.
        """
        super().__init__(start=start, end=end, nodes=nodes, width=width)

    def draw(
        self,
        canvas: Canvas,
        pos: Tuple[int, int],
    ) -> None:
        """Draw a mechanical spring from start point to current position.

        Args:
            canvas (Canvas): Canvas to draw on.
            pos (Tuple[int, int]): Current endpoint for spring.
        """

        with hold_canvas():
            canvas.clear()
            x_coords, y_coords = spring_module.spring(
                [self._start[0], self._start[1]],
                pos,
                self._nodes,
                self._width,
            )

            if np.isscalar(x_coords):
                canvas.stroke_line(self._start[0], self._start[1], x_coords, y_coords)
                canvas.stroke_line(
                    x_coords, y_coords, x_coords + abs_value(canvas.width, 2), y_coords
                )
            else:
                canvas.stroke_lines(list(zip(x_coords, y_coords)))
                index = len(x_coords) - 1
                canvas.stroke_line(
                    x_coords[index],
                    y_coords[index],
                    x_coords[index] + abs_value(canvas.width, 2),
                    y_coords[index],
                )
