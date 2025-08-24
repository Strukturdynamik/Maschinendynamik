import numpy as np
from typing import Tuple, Any
from ipycanvas import Canvas, hold_canvas

from .anim_modules import Shape
from ...utils.ext_utils.spring import spring_module
from ...utils.helper import abs_value


"""
Module containing specific shape implementations that extend the Shape superclass.

Available shapes:
- Circle
- Rectangle
- Triangle
- Spring
"""


class Circle(Shape):
    """
    Circle shape implementation.

    Defined by a center and a radius.
    """

    def __init__(
        self,
        center: Tuple[int, int],
        radius: int | Any = None,
    ) -> None:
        """
        Initialize a circle.

        Args:
            center (tuple[int, int]): Center position of the circle.
            radius (int | Any, optional): Radius of the circle. Defaults to None.
        """
        super().__init__(center=center, radius=radius)

    def draw(self, canvas: Canvas, pos: Tuple[int, int], fill: bool) -> None:
        """
        Draw the circle at a given position.

        Args:
            canvas (Canvas): Canvas to draw on.
            pos (tuple[int, int]): Position offset for drawing the circle.
            fill (bool): Whether to fill the circle or only draw its outline.
        """
        with hold_canvas():
            canvas.stroke_circle(x=pos[0], y=pos[1], radius=self.radius)
            if fill:
                canvas.fill_circle(x=pos[0], y=pos[1], radius=self.radius)


class Rectangle(Shape):
    """
    Rectangle shape implementation.

    Defined by its width and height.
    """

    def __init__(
        self,
        width: int | Any = None,
        height: int | Any = None,
    ) -> None:
        """
        Initialize a rectangle.

        Args:
            width (int | Any, optional): Width of the rectangle. Defaults to None.
            height (int | Any, optional): Height of the rectangle. Defaults to None.
        """
        super().__init__(width=width, height=height)

    def draw(self, canvas: Canvas, pos: Tuple[int, int], fill: bool) -> None:
        """
        Draw the rectangle at a given position.

        Args:
            canvas (Canvas): Canvas to draw on.
            pos (tuple[int, int]): Position offset for drawing the rectangle.
            fill (bool): Whether to fill the rectangle or only draw its outline.
        """
        with hold_canvas():
            x = pos[0] + abs_value(canvas.width, 2)
            y = pos[1] - self.height / 2
            canvas.stroke_rect(x=x, y=y, width=self.width, height=self.height)
            if fill:
                canvas.fill_rect(x=x, y=y, width=self.width, height=self.height)


class Triangle(Shape):
    """
    Triangle shape implementation.

    Defined by its three vertices A, B, and C.
    """

    def __init__(
        self,
        A: Tuple[int, int] | Any = None,
        B: Tuple[int, int] | Any = None,
        C: Tuple[int, int] | Any = None,
    ) -> None:
        """
        Initialize a triangle.

        Args:
            A (tuple[int, int] | Any, optional): First vertex. Defaults to None.
            B (tuple[int, int] | Any, optional): Second vertex. Defaults to None.
            C (tuple[int, int] | Any, optional): Third vertex. Defaults to None.
        """
        super().__init__(A=A, B=B, C=C)

    def draw(self, canvas: Canvas, pos: Tuple[int, int], fill: bool) -> None:
        """
        Draw the triangle.

        Args:
            canvas (Canvas): Canvas to draw on.
            pos (tuple[int, int]): Position offset for drawing the triangle.
            fill (bool): Whether to fill the triangle or only draw its outline.
        """
        # TODO: Implement drawing logic
        pass


class Spring(Shape):
    """
    Spring shape implementation.

    A spring is drawn between a start point and an endpoint, with a 
    configurable number of coils (nodes) and width.
    """

    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        nodes: int,
        width: float,
    ) -> None:
        """
        Initialize a spring.

        Args:
            start (tuple[int, int]): Start point of the spring.
            end (tuple[int, int]): End point of the spring.
            nodes (int): Number of nodes representing the coils.
            width (float): Width of the spring.
        """
        super().__init__(start=start, end=end, nodes=nodes, width=width)

    def draw(self, canvas: Canvas, pos: Tuple[int, int]) -> None:
        """
        Draw the spring from the start point to the given position.

        Args:
            canvas (Canvas): Canvas to draw on.
            pos (tuple[int, int]): Current endpoint for the spring.
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
                # Simple straight line spring
                canvas.stroke_line(self._start[0], self._start[1], x_coords, y_coords)
                canvas.stroke_line(
                    x_coords,
                    y_coords,
                    x_coords + abs_value(canvas.width, 2),
                    y_coords,
                )
            else:
                # Coiled spring
                canvas.stroke_lines(list(zip(x_coords, y_coords)))
                index = len(x_coords) - 1
                canvas.stroke_line(
                    x_coords[index],
                    y_coords[index],
                    x_coords[index] + abs_value(canvas.width, 2),
                    y_coords[index],
                )
