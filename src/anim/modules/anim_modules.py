from typing import Tuple, Any
from ipycanvas import Canvas
from abc import abstractmethod

"""Shape superclass.
"""


class Shape:
    """
    Abstract base class for geometric shapes used in visualizations.

    A shape can represent various geometrical primitives, such as:
    - Rectangle (defined by width and height)
    - Circle (defined by center and radius)
    - Triangle (defined by points A, B, C)
    - Spring (defined by start, end, number of nodes, and width)

    This class provides a flexible initializer that sets attributes
    based on the given parameters. Subclasses must implement the
    `draw` method to define their own rendering behavior.
    """

    def __init__(
        self,
        center: Tuple[int, int] | Any = None,
        width: int | Any = None,
        height: int | Any = None,
        radius: int | Any = None,
        A: Tuple[int, int] | Any = None,
        B: Tuple[int, int] | Any = None,
        C: Tuple[int, int] | Any = None,
        start: Tuple[int, int] | Any = None,
        end: Tuple[int, int] | Any = None,
        nodes: int | Any = None,
    ) -> None:
        """
        Initialize a Shape by setting attributes based on the provided parameters.

        Supported shapes:
        - Rectangle: requires `width` and `height`
        - Circle: requires `center` and `radius`
        - Triangle: requires points `A`, `B`, and `C`
        - Spring: requires `start`, `end`, `nodes`, and `width`

        Args:
            center (tuple[int, int] | Any, optional): Center point of the circle.
            width (int | Any, optional): Width (for rectangles or springs).
            height (int | Any, optional): Height (for rectangles).
            radius (int | Any, optional): Radius (for circles).
            A (tuple[int, int] | Any, optional): First vertex of a triangle.
            B (tuple[int, int] | Any, optional): Second vertex of a triangle.
            C (tuple[int, int] | Any, optional): Third vertex of a triangle.
            start (tuple[int, int] | Any, optional): Start point (for springs).
            end (tuple[int, int] | Any, optional): End point (for springs).
            nodes (int | Any, optional): Number of nodes (for springs).
        """
        shapes = [
            (  # check for rectangle
                width is not None and height is not None,
                {"_width": width, "_height": height},
            ),
            (  # check for circle
                radius is not None and center is not None,
                {"_center": center, "_radius": radius},
            ),
            (  # check for triangle polygone
                A is not None and B is not None and C is not None,
                {"_A": A, "_B": B, "_C": C},
            ),
            (  # check for spring
                start is not None
                and end is not None
                and nodes is not None
                and width is not None,
                {"_start": start, "_end": end, "_nodes": nodes, "_width": width},
            ),
        ]

        # Loop through conditions and assign attributes
        for condition, attributes in shapes:
            if condition:
                for attr, value in attributes.items():
                    setattr(self, attr, value)
                break

    @abstractmethod
    def draw(self, canvas: Canvas, pos: Tuple[int, int], fill: bool) -> None:
        """
        Draw the shape on a given canvas at the specified position.

        Args:
            canvas (Canvas): The canvas to render the shape on.
            pos (tuple[int, int]): Position offset for drawing the shape.
            fill (bool): Whether to fill the shape (True) or only outline it (False).
        """

        pass

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, new_center: int):
        self._center = new_center

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width: int):
        self._width = new_width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height: int):
        self._height = new_height

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, new_radius: int):
        self._radius = new_radius

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, new_A: int):
        self._A = new_A

    @property
    def B(self):
        return self._B

    @B.setter
    def B(self, new_B: int):
        self._B = new_B

    @property
    def C(self):
        return self._C

    @C.setter
    def C(self, new_C: int):
        self._C = new_C

    @property
    def start(self) -> Tuple[int, int] | Any:
        return self._start

    @start.setter
    def start(self, new_start: Tuple[int, int] | Any):
        self._start = new_start

    @property
    def end(self) -> Tuple[int, int] | Any:
        return self._end

    @end.setter
    def end(self, new_end: Tuple[int, int] | Any):
        self._end = new_end

    @property
    def nodes(self) -> int | Any:
        return self._nodes

    @nodes.setter
    def nodes(self, new_nodes: int | Any):
        self._nodes = new_nodes
