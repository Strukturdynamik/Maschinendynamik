from typing import Any
import math
from ipycanvas import MultiCanvas
import ipywidgets.widgets as widgets
from ipywidgets import (
    VBox,
    AppLayout,
    GridspecLayout,
)

from .mpl_managers.a4_u1_mpl_manager import PlotManagerA4U1
from .gui_superclass import GUISuperclass
from ..utils.constants import (
    A4_U1_DEFAULT_C_MAX,
    A4_U1_START_VELOCITY,
    A4_U1_START_DEFLECTION,
    A4_U1_NUM_DATAPOINTS,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)


"""Module containing functions to build an interactive ui for displaying
    and manipulating animations.
"""

FIRST_FRAME_CHANGE: bool = False


class GUI(GUISuperclass):
    def __init__(self, default_c, default_d, animation_instance: Any):
        """Function to build interactive ui for displaying
        and manipulating animations.

        Args:
            default_c (int): Default value for parameter c.
            default_d (int): Default value for parameter d.
            animation_instance (Any): Animation that will be run inside the
                animation canvas (left side) of the GUI.

        Returns:
            Any: The application.
        """
        super().__init__()
        self.animation_instance = animation_instance
        # set constants as class variables
        self.default_c = default_c
        self.default_d = default_d

        # set up anim canvas
        self.mult_canvas_anim = MultiCanvas(
            n_canvases=5,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            layout=widgets.Layout(
                width="100%",
                height="100%",
            ),
        )
        self.animation_instance.anim_canvas = self.mult_canvas_anim
        # set up plot manager
        self.plot_manager = PlotManagerA4U1(animation_instance)

        # after inital set up, set up gui elements
        app_layout = self.make_gui()

        return app_layout

    def make_gui(self):
        """General function to coordinate gui elements."""

        # make control elements for parameters
        slider_d, slider_c, c_input_max, slider_defl, slider_v = (
            self.make_parameter_control_elements()
        )
        # make slider grid
        slider_grid = VBox([slider_d, slider_c, c_input_max, slider_defl, slider_v])

        # make titles
        animation_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Animation</strong>'
        )
        slider_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Variables</strong>'
        )
        anim_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Pendulum Animation</strong>'
        )
        graph_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Deflection Graph</strong>'
        )
        # make title grid
        title_grid = GridspecLayout(1, 3)
        title_grid[0, 0] = slider_title
        title_grid[0, 1] = anim_title
        title_grid[0, 2] = graph_title

        # make play control widget
        play_control_widget = self.make_play_control_element(A4_U1_NUM_DATAPOINTS)

        self.app_layout = self.place_and_coordinate_gui_elements(
            animation_title, play_control_widget, slider_grid, title_grid
        )

        # draw inital visual
        self.animation_instance._initial_visual()
        # draw first frame
        self.animation_instance._draw_first_frame()

    def make_parameter_control_elements(self) -> widgets:
        """Function to create and place parameter control elements.

        Returns:
            widgets: Sliders and control elements for the parameters.
        """
        slider_d = widgets.FloatSlider(
            value=round(self.default_d, 2),
            min=0.0,
            max=5.0,
            step=0.01,
            description="d",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_d = slider_d

        slider_c = widgets.FloatSlider(
            value=round(self.default_c, 2),
            min=0.1,
            max=round(A4_U1_DEFAULT_C_MAX, 2),
            step=0.01,
            description="c",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_c = slider_c

        c_input_max = widgets.BoundedFloatText(
            value=round(A4_U1_DEFAULT_C_MAX, 2),
            min=0.1,
            max=100,
            step=0.1,
            description="c max:",
            readout_format=".2f",
            disabled=False,
            layout=widgets.Layout(display="flex", width="50%"),
        )
        c_input_max.observe(self.on_value_change, names="value")
        self.c_input_max = c_input_max

        # starting conditions sliders
        min_v = round(0.0, 4)
        max_v = round(2.25, 4)
        slider_v = widgets.FloatSlider(
            value=round(A4_U1_START_VELOCITY, 4),
            min=min_v,
            max=max_v,
            step=0.0001,
            description="v₀",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_v = slider_v

        max_defl = round(math.pi, 4) / 10
        min_defl = round(math.pi, 4) / 30
        slider_defl = widgets.FloatSlider(
            value=round(A4_U1_START_DEFLECTION, 4),
            min=min_defl,
            max=max_defl,
            step=0.01,
            description="defl₀",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_defl = slider_defl

        # define observe functions
        slider_d.observe(self.on_value_change, names="value")
        slider_c.observe(self.on_value_change, names="value")
        slider_v.observe(self.on_value_change, names="value")
        slider_defl.observe(self.on_value_change, names="value")

        self.slider = [slider_d, slider_c, slider_v, slider_defl]

        return slider_d, slider_c, c_input_max, slider_defl, slider_v

    def place_and_coordinate_gui_elements(
        self,
        animation_title: widgets,
        play_control_widget: widgets,
        slider_grid: widgets,
        title_grid: widgets,
    ) -> widgets:
        """Function to place and coordinate all gui elements.

        Returns:
            widgets: Returns the App Layout.
        """

        # make grid for animation interaction
        anim_inter_grid = AppLayout(
            header=animation_title,
            left_sidebar=play_control_widget,  # anim_button,
            center=None,  # slider_frame,
            right_sidebar=None,
            footer=None,
            pane_widths=["100%", "0%", "0%"],
            pane_heights=["15%", "15%", "15%"],
        )

        # make grid for interacitve part
        interactive_grid = GridspecLayout(2, 1)
        interactive_grid[0, 0] = slider_grid
        interactive_grid[1, 0] = anim_inter_grid

        app_layout = AppLayout(
            header=title_grid,
            left_sidebar=interactive_grid,
            center=self.mult_canvas_anim,
            right_sidebar=self.plot_manager.output_deflection,  # self.plot_manager.fig.canvas,
            footer=None,
            pane_widths=["33%", "33%", "33%"],
            pane_heights=["10%", "90%", "0%"],
        )

        # make border on left side
        self.animation_instance.anim_canvas[4].begin_path()
        self.animation_instance.anim_canvas[4].move_to(0, 0)
        self.animation_instance.anim_canvas[4].line_to(
            0, self.animation_instance.anim_canvas[4].height
        )
        self.animation_instance.anim_canvas[4].stroke()
        # make border on right side
        self.animation_instance.anim_canvas[4].begin_path()
        self.animation_instance.anim_canvas[4].move_to(
            self.animation_instance.anim_canvas[4].width, 0
        )
        self.animation_instance.anim_canvas[4].line_to(
            self.animation_instance.anim_canvas[4].width,
            self.animation_instance.anim_canvas[4].height,
        )
        self.animation_instance.anim_canvas[4].stroke()

        return app_layout

    def reset_parameters(self, button):
        """Function to reset all parameters to default values.

        Args:
            button (widgets.Button): Button that triggers the reset.
        """

        # freeze the change of the graph
        self.freeze_change = True

        self.slider_d.value = self.default_d
        self.slider_c.value = self.default_c
        self.c_input_max.value = A4_U1_DEFAULT_C_MAX

        # unfreeze the change of the graph
        self.freeze_change = False

        # calculate default solution
        self.plot_manager.calc_and_plot_solutions()

    def on_value_change(self, change):
        """Unified observer for handling parameter slider value changes.

        Args:
            change (Any): Incoming user input.
        """
        widget = change.owner
        new_value = change["new"]

        match widget:
            case self.slider_d:
                self.animation_instance.d = new_value
                self.plot_manager.calc_and_plot_solutions()

            case self.slider_c:
                self.animation_instance.c = new_value
                self.plot_manager.calc_and_plot_solutions()

            case self.slider_v:
                self.animation_instance.start_velocity = new_value
                self.plot_manager.calc_and_plot_solutions()

            case self.slider_defl:
                self.animation_instance.start_deflection = new_value
                self.plot_manager.calc_and_plot_solutions()

            case self.c_input_max:
                self.slider_c.max = new_value

            case self.play:
                if new_value == True:
                    for s in self.slider:
                        s.disabled = True
                    self.c_input_max.disabled = True

            case self.play_slider:
                # if reset button pressed, enable controls
                if new_value == self.play.min:
                    for s in self.slider:
                        s.disabled = False
                    self.c_input_max.disabled = False
                    # disable repeat
                    self.play.repeat = False

                global FIRST_FRAME_CHANGE
                # animate blob in gaph
                self.plot_manager.update_blobs()

                # animate pendulum
                self.animation_instance.frame = new_value
                self.animation_instance._animate_visual()
                if FIRST_FRAME_CHANGE == False:
                    FIRST_FRAME_CHANGE = True
                    # self.calc_button.description = "Calculate"

                if new_value == A4_U1_NUM_DATAPOINTS - 1:
                    FIRST_FRAME_CHANGE = False
