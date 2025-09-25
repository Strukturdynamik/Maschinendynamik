from abc import abstractmethod
from typing import Optional, Any
from ipycanvas import Canvas


class AnimationInstance:
    """
    Abstract base class for animation instances that visualize oscillating systems.

    This class defines a common interface for building animations.
    Subclasses must implement methods to compute system dynamics,
    draw static elements, render the first frame, and handle
    the continuous animation process.
    """

    def __init__(self) -> None:
        self.canvas: Canvas = None
        self.calculator: Any = None
        # self.is_running = threading.Event()  # Uncomment if you want to track animation state
        # self.is_calculating = threading.Event()  # Uncomment if you want to track calculation state
        # self._observer = None

    @abstractmethod
    def animate_visual(self):
        """
        Render the animation step for the current frame.

        Updates the canvas with the system's evolving state,
        based on previously computed solutions.
        """
        pass

    @abstractmethod
    def _calculate(self):
        """
        Compute the solution for the system's dynamics.

        This typically involves numerical integration or
        evaluation of the model using user-defined parameters.
        """
        pass

    @abstractmethod
    def draw_first_frame(self):
        """
        Draw the initial frame of the animation.

        Called once before the animation begins,
        to visualize the system in its starting state.
        """
        pass

    @abstractmethod
    def _initial_visual(self):
        """
        Draw all static elements of the visualization.

        Executed during setup to render reference structures
        such as axes, anchor points, labels, or other
        non-changing components.
        """
        pass
