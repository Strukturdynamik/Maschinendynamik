from abc import abstractmethod
import threading


class AnimationInstance:
    def __init__(self) -> None:
        self.canvas = None
        self.calculator = None
        # self.is_running = threading.Event()
        # self.is_calculating = threading.Event()
        self._observer = None

    @abstractmethod
    def _animate_visual(self):
        pass
        """Function to animate the current solution.
        """

    @abstractmethod
    def _calculate(self):
        pass
        """Function to calculate the solution given the current state
        of parameters."""

    @abstractmethod
    def _draw_first_frame(self):
        pass
        """Function to draw the first frame of animation before
            user input on play element.
        """

    @abstractmethod
    def _initial_visual(self):
        pass
        """Function that draws the still modules of the animation
            before any button is pressed.
        """
