from typing import Tuple, Any
from ipycanvas import Canvas
from abc import abstractmethod

"""Shape superclass.
"""


class Shape:
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
        """Specific function for every shape that draws the shape at the given
            position.

        Args:
            canvas (Canvas): Canvas to draw the shape on.
            pos (Any): Position where shape is being drawn.
            fill (bool): Determines if the shape should be filled in addition
                to being drawn.
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
