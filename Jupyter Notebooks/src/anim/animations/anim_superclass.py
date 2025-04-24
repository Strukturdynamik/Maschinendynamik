from abc import abstractmethod
from typing import Optional, Any
from ipycanvas import Canvas


class AnimationInstance:
    """
    Abstract base class for an animation instance used in visualizing
    oscillating systems.

    This class provides a skeleton interface that enforces the implementation
    of key methods for drawing and animating visual elements, as well as
    computing the underlying data or logic for visualization.
    """

    def __init__(self) -> None:
        self.canvas: Canvas = None
        self.calculator: Any = None
        # self.is_running = threading.Event()  # Uncomment if you want to track animation state
        # self.is_calculating = threading.Event()  # Uncomment if you want to track calculation state
        # self._observer = None

    @abstractmethod
    def _animate_visual(self):
        """
        Abstract method to handle the continuous animation of a solution.

        This should update the canvas with animated transitions or stepwise
        changes based on the computed solution.
        """
        pass

    @abstractmethod
    def _calculate(self):
        """
        Abstract method to compute the solution based on user-defined parameters
        or input values.
        """
        pass

    @abstractmethod
    def _draw_first_frame(self):
        """
        Abstract method to draw the first visual frame on the canvas.

        Called before any user interaction begins.
        Helps in giving a preview or initial state of the system.
        """
        pass

    @abstractmethod
    def _initial_visual(self):
        """
        Abstract method to draw static modules or components of the visualization.

        Executed during setup before user interaction, such as rendering axes,
        UI boundaries, static labels, or any persistent visual elements.
        """
        pass
