from abc import abstractmethod

import ipywidgets.widgets as widgets


class GUISuperclass:
    """
    Abstract base class for creating interactive GUI controllers.
    
    This class provides a foundation for building interactive graphical user interfaces
    that control animations and visualizations. It defines the common structure and
    functionality that all GUI subclasses should implement, including play controls,
    parameter adjustments, and event handling.
    
    Attributes:
        animation_instance: Reference to the animation controller instance that
                           manages the simulation and visualization logic
        plot_manager: Reference to the plot manager instance that handles
                     figure creation and updating
        play_slider (widgets.IntSlider): Slider widget for manual frame navigation
        play (widgets.Play): Play/pause button widget for animation control
    """

    def __init__(self):
        self.animation_instance = None
        self.plot_manager = None
        pass

    def make_play_control_element(self, num_data_points) -> widgets:
        """
        Create the play control element with stop/restart/loop animation and frame slider.
        
        Constructs a linked play button and slider widget that allows users to:
        - Play/pause the animation
        - Manually navigate through frames using the slider
        - Control animation speed through the interval parameter
        - Loop through the animation sequence
        
        The play button and slider are JavaScript-linked so they stay synchronized,
        and both widgets are configured to trigger the on_value_change callback.
        
        Args:
            num_data_points (int): The total number of frames/data points in the animation.
                                 Determines the maximum value for the slider and play widget.
        
        Returns:
            widgets.HBox: A horizontal box containing the play button and slider widgets,
                         ready for placement in the GUI layout.
        """
        play = widgets.Play(
            value=0,
            min=0,
            max=num_data_points - 1,
            step=1,
            interval=25,
            description="Press play",
            disabled=False,
        )

        play_slider = widgets.IntSlider(
            disabled=False,
            min=0,
            max=num_data_points - 1,
            step=1,
            interval=25,
        )
        self.play_slider = play_slider
        self.play = play
        widgets.jslink((play, "value"), (play_slider, "value"))
        play_control_widget = widgets.HBox([play, play_slider])
        play_slider.observe(self.on_value_change, names="value")
        play.observe(self.on_value_change, names="playing")

        return play_control_widget

    @abstractmethod
    def make_gui(self):
        """
        Create the complete GUI layout.
        
        This method should be implemented by subclasses to construct the entire
        graphical user interface, including all control elements, plots, and
        layout containers. It serves as the main entry point for GUI construction.
        """
        pass

    @abstractmethod
    def make_parameter_control_elements(self) -> widgets:
        """
        Create and arrange parameter control elements.
        
        This method should be implemented by subclasses to create interactive
        controls (sliders, dropdowns, buttons, etc.) that allow users to adjust
        simulation parameters in real-time.
        
        Returns:
            widgets: A container widget (GridBox, VBox, HBox, etc.) holding all
                    parameter control elements in an organized layout.
        """
        pass

    @abstractmethod
    def place_and_coordinate_gui_elements(
        self, play_control_widget, slider_grid, title_grid, reset_button, radio_button
    ) -> widgets:
        """
        Arrange and coordinate all GUI elements in the final layout.
        
        This method should be implemented by subclasses to position all GUI
        components (control elements, plots, labels, etc.) in a logical and
        visually appealing layout. It also establishes any necessary coordination
        between different UI elements.
        
        Args:
            play_control_widget (widgets.HBox): The play/slider control element
            slider_grid (widgets.GridBox): Grid container for parameter sliders
            title_grid (widgets.GridBox): Grid container for titles and labels
            reset_button (widgets.Button): Button for resetting parameters
            radio_button (widgets.RadioButtons): Radio button group for mode selection
            
        Returns:
            widgets: The complete GUI layout container ready for display.
        """
        pass

    @abstractmethod
    def reset_parameters(self, button):
        """
        Reset all parameters to their default values.
        
        This method should be implemented by subclasses to handle resetting
        all adjustable parameters to their initial/default values when the
        reset button is clicked.
        
        Args:
            button (widgets.Button): The reset button that triggered this callback
        """
        pass

    @abstractmethod
    def on_value_change(self, change):
        """
        Handle value changes in GUI elements.
        
        This method should be implemented by subclasses to respond to changes
        in any of the interactive GUI elements (sliders, buttons, dropdowns, etc.).
        Typical actions include updating the simulation, refreshing plots, or
        modifying visualization parameters.
        
        Args:
            change (dict): A dictionary containing information about the change event,
                          including the widget that changed and its new value.
        """
        pass
