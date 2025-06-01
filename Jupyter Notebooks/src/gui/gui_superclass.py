from abc import abstractmethod

import ipywidgets.widgets as widgets


class GUISuperclass:

    def __init__(self):
        self.animation_instance = None
        self.plot_manager = None
        pass

    @abstractmethod
    def make_gui(self):
        """Creates the GUI. This method should be implemented by subclasses."""
        pass

    @abstractmethod
    def make_parameter_control_elements(self) -> widgets:
        """Function to create and place parameter control elements. This method
        should be implemented by subclasses."""
        pass

    @abstractmethod
    def make_play_control_element(self) -> widgets:
        """Function to create the play control element. Stop/restart/
            loop animation and slide through frames.This method should
        be implemented by subclasses."""
        pass

    @abstractmethod
    def place_and_coordinate_gui_elements(
        self, play_control_widget, slider_grid, title_grid, reset_button, radio_button
    ) -> widgets:
        """Function to place and coordinate all gui elements. This method
        should be implemented by subclasses."""
        pass

    @abstractmethod
    def reset_parameters(self, button):
        """Function to reset all parameters to their default values. This method
        should be implemented by subclasses."""
        pass

    @abstractmethod
    def on_value_change(self, change):
        """Function to handle value changes in the GUI. This method should be
        implemented by subclasses."""
        pass
