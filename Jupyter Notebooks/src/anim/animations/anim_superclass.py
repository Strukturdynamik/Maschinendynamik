from abc import abstractmethod
from typing import Tuple, List
import time
from threading import Thread
import threading
from ipywidgets import IntProgress
from IPython.display import display


class AnimationInstance:
    def __init__(self) -> None:
        self.canvas = None
        self.calculator = None
        self.is_running = threading.Event()
        self.is_calculating = threading.Event()
        self._observer = None

    @abstractmethod
    def _animate_visual(self):
        pass
        """Function to animate the visualization.
        """

    @abstractmethod
    def _calculate(self):
        pass
        """Function to calculate solution.
        """

    @abstractmethod
    def _draw_first_frame(self):
        pass
        """Function to draw the first frame of animation before
            "start" button is pressed.

        Args:
            canvas (Canvas): Canvas to be drawn on.
        """

    @abstractmethod
    def _initial_visual(self):
        pass
        """Function that draws the still modules of the animation
            before any button is pressed.
        """
