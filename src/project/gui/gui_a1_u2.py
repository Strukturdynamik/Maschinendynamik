import math
from ipycanvas import MultiCanvas
import ipywidgets.widgets as widgets
import numpy as np
from ipywidgets import (
    VBox,
    AppLayout,
    GridspecLayout,
)

from .mpl_managers.a1_u2_mpl_manager import PlotManagerA1U2
from .gui_superclass import GUISuperclass

from ..utils.constants import (
    A1_U2_T,
    A1_U2_NUM_DATA_POINTS,
    A1_U2_START_DEFLECTION,
    A1_U2_START_VELOCITY,
    A1_U2_DEFAULT_C_MAX,
    A1_U2_DEFAULT_C_MIN,
    A1_U2_DEFAULT_D_MAX,
    A1_U2_DEFAULT_D_MIN,
    A1_U2_DEFAULT_D_MAX,
    A1_U2_DEFAULT_M,
    A1_U2_DEFAULT_M_MIN,
    A1_U2_DEFAULT_M_MIN,
    A1_U2_DEFAULT_M_MAX,
    A1_U2_DEFAULT_F_HAT,
    A1_U2_DEFAULT_F_HAT_MIN,
    A1_U2_DEFAULT_F_HAT_MAX,
    A1_U2_DEFAULT_OMEGA,
    A1_U2_DEFAULT_OMEGA_MIN,
    A1_U2_DEFAULT_OMEGA_MAX,
    A1_U2_DEFAULT_ALPHA,
    A1_U2_DEFAULT_ALPHA_MIN,
    A1_U2_DEFAULT_ALPHA_MAX,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)


"""Module containing functions to build an interactive ui for displaying
    and manipulating animations.
"""

FIRST_FRAME_CHANGE: bool = False


class GUI(GUISuperclass):
    def __init__(
        self,
        default_c,
        default_d,
        animation_instance,
    ):
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

        # set constants as class variables
        self.default_c = default_c
        self.default_d = default_d
        self.animation_instance = animation_instance
        self.animation_instance.c = default_c
        self.animation_instance.d = default_d
        self.animation_instance.mode = "Lineary Increasing"
        self.freeze_change = False
        self.t = A1_U2_T

        # set up anim canvas
        self.mult_canvas_anim = MultiCanvas(
            n_canvases=10,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            layout=widgets.Layout(
                width="100%",
                height="100%",
            ),
        )
        self.animation_instance.anim_canvas = self.mult_canvas_anim

        # set up plot manager
        self.plot_manager = PlotManagerA1U2(self.animation_instance)

        # after inital set up, set up gui elements
        app_layout = self.make_gui()

        return app_layout

    def make_gui(self):
        """General function to coordinate gui elements."""

        # make control elements for parameters
        (
            slider_d,
            slider_c,
            c_input_max,
            slider_defl,
            slider_v,
            slider_m,
            slider_omega,
            slider_alpha,
            slider_f_hat,
            radio_buttons,
            reset_button,
        ) = self.make_parameter_control_elements()

        # make slider grid
        slider_grid = VBox(
            [
                slider_d,
                slider_c,
                c_input_max,
                slider_m,
                slider_omega,
                slider_alpha,
                slider_f_hat,
                slider_defl,
                slider_v,
            ],
            layout=widgets.Layout(top="-2%"),
        )

        slider_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Variables</strong>'
        )
        anim_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Pendulum Animation</strong>'
        )
        graph_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Graphs</strong>'
        )
        # make title grid
        title_grid = GridspecLayout(1, 3)
        title_grid[0, 0] = slider_title
        title_grid[0, 1] = anim_title
        title_grid[0, 2] = graph_title

        # make play control widget
        play_control_widget = self.make_play_control_element()

        self.app_layout = self.place_and_coordinate_gui_elements(
            play_control_widget,
            slider_grid,
            title_grid,
            reset_button,
            radio_buttons,
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
            value=self.default_d,
            min=A1_U2_DEFAULT_D_MIN,
            max=A1_U2_DEFAULT_D_MAX,
            step=1.0,
            description="d",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
            tooltip="damping coefficient",
        )
        self.slider_d = slider_d

        slider_c = widgets.FloatSlider(
            value=self.default_c,
            min=A1_U2_DEFAULT_C_MIN,
            max=A1_U2_DEFAULT_C_MAX,
            step=1.0,
            description="c",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
            tooltip="spring constant",
        )
        self.slider_c = slider_c

        slider_m = widgets.FloatSlider(
            value=A1_U2_DEFAULT_M,
            min=A1_U2_DEFAULT_M_MIN,
            max=A1_U2_DEFAULT_M_MAX,
            step=1.0,
            description="m",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
            tooltip="mass",
        )
        self.slider_m = slider_m

        c_input_max = widgets.BoundedFloatText(
            value=round(A1_U2_DEFAULT_C_MAX, 2),
            min=0.1,
            max=100,
            step=1.0,
            description="cₘₐₓ : ",
            readout_format=".2f",
            disabled=False,
            layout=widgets.Layout(display="flex", width="50%"),
        )
        c_input_max.observe(self.on_value_change, names="value")
        self.c_input_max = c_input_max

        # starting conditions sliders
        min_v = 0.0
        max_v = 5.0
        slider_v = widgets.FloatSlider(
            value=round(A1_U2_START_VELOCITY, 4),
            min=min_v,
            max=max_v,
            step=1.0,
            description="v₀",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-9%", width="88%", display="flex"),
            tooltip="initial velocity",
        )
        self.slider_v = slider_v

        max_defl = math.pi / 5
        min_defl = 0
        slider_defl = widgets.FloatSlider(
            value=round(A1_U2_START_DEFLECTION, 4),
            min=min_defl,
            max=max_defl,
            step=0.1,
            description="defl₀",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-9%", width="88%", display="flex"),
            tooltip="initial deflection",
        )
        self.slider_defl = slider_defl

        slider_omega = widgets.FloatSlider(
            value=A1_U2_DEFAULT_OMEGA,
            min=A1_U2_DEFAULT_OMEGA_MIN,
            max=A1_U2_DEFAULT_OMEGA_MAX,
            step=1.0,
            description="Ω",
            continuous_update=False,
            orientation="horizontal",
            disabled=True,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
            tooltip="angular frequency of the input",
        )
        self.slider_omega = slider_omega

        slider_alpha = widgets.FloatSlider(
            value=A1_U2_DEFAULT_ALPHA,
            min=A1_U2_DEFAULT_ALPHA_MIN,
            max=A1_U2_DEFAULT_ALPHA_MAX,
            step=0.01,
            description="α",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
            tooltip="angular acceleration of the input",
        )
        self.slider_alpha = slider_alpha

        slider_f_hat = widgets.FloatSlider(
            value=A1_U2_DEFAULT_F_HAT,
            min=A1_U2_DEFAULT_F_HAT_MIN,
            max=A1_U2_DEFAULT_F_HAT_MAX,
            step=0.01,
            description="F̂",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
            tooltip="F_Hat",
        )
        self.slider_f_hat = slider_f_hat

        radio_buttons = widgets.RadioButtons(
            options=["Lineary Increasing", "Constant"],
            value="Lineary Increasing",
            layout=widgets.Layout(top="-5%"),
            description="Exitation Frequency",
            disabled=False,
            orientation="horizontal",
        )
        self.radio_buttons = radio_buttons

        reset_button = widgets.Button(
            description="Reset",
            layout=widgets.Layout(top="-5%", display="flex"),
            diabled=False,
        )
        self.reset_button = reset_button
        self.reset_button.on_click(self.reset_parameters)

        self.sliders = [
            self.slider_d,
            self.slider_c,
            self.slider_v,
            self.slider_m,
            self.slider_defl,
            self.slider_omega,
            self.slider_alpha,
            self.slider_f_hat,
        ]

        self.sliders_and_radio_buttons = [
            self.slider_d,
            self.slider_c,
            self.slider_v,
            self.slider_m,
            self.slider_defl,
            self.slider_omega,
            self.slider_alpha,
            self.slider_f_hat,
            self.radio_buttons,
        ]

        # define observe functions
        for s in self.sliders_and_radio_buttons:
            s.observe(self.on_value_change, names="value")

        return (
            slider_d,
            slider_c,
            c_input_max,
            slider_defl,
            slider_v,
            slider_m,
            slider_omega,
            slider_alpha,
            slider_f_hat,
            reset_button,
            radio_buttons,
        )

    def make_play_control_element(self) -> widgets:
        """Function to create the play control element. Stop/restart/
            loop animation and slide through frames.

        Returns:
            widgets: Returns play control element.
        """
        play = widgets.Play(
            value=0,
            min=0,
            max=A1_U2_NUM_DATA_POINTS - 1,
            step=1,
            interval=25,
            description="Press play",
            disabled=False,
        )

        play_slider = widgets.IntSlider(
            disabled=False,
            min=0,
            max=A1_U2_NUM_DATA_POINTS - 1,
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

    def place_and_coordinate_gui_elements(
        self,
        play_control_widget: widgets,
        slider_grid: widgets,
        title_grid: widgets,
        reset_button,
        radio_buttons,
    ) -> widgets:
        """Function to place and coordinate all gui elements.

        Returns:
            widgets: Returns the App Layout.
        """

        # make layout for the interactive part of gui
        interactive_grid = AppLayout(
            header=slider_grid,
            left_sidebar=None,
            center=widgets.VBox([reset_button, radio_buttons]),
            right_sidebar=None,
            footer=VBox([play_control_widget]),
            pane_widths=["0%", "100%", "0%"],
            pane_heights=["55%", "25%", "20%"],
            layout=widgets.Layout(left="2%"),
        )

        # make tab for graphs
        tab = widgets.Tab()
        children = [
            self.plot_manager.fig_deflection.canvas,
            self.plot_manager.fig_bode.canvas,
        ]
        tab.children = children
        tab.titles = ["Deflection", "Bode Diagram"]

        app_layout = AppLayout(
            header=title_grid,
            left_sidebar=interactive_grid,
            center=self.mult_canvas_anim,
            right_sidebar=tab,
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
        self.c_input_max.value = A1_U2_DEFAULT_C_MAX
        self.slider_m.value = A1_U2_DEFAULT_M
        self.slider_omega.value = A1_U2_DEFAULT_OMEGA
        self.slider_alpha.value = A1_U2_DEFAULT_ALPHA
        self.slider_defl.value = A1_U2_START_DEFLECTION
        self.slider_v.value = A1_U2_START_VELOCITY
        self.radio_buttons.value = "Lineary Increasing"

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
            case self.radio_buttons:
                self.animation_instance.mode = new_value

                if self.animation_instance.mode == "Lineary Increasing":
                    self.slider_omega.disabled = True
                    self.slider_alpha.disabled = False

                else:
                    self.slider_omega.disabled = False
                    self.slider_alpha.disabled = True

                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_d:
                self.animation_instance.d = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_c:
                self.animation_instance.c = new_value
                omega_0 = np.sqrt(
                    2 * self.animation_instance.c / (3 * self.animation_instance.m)
                )
                self.slider_omega.max = omega_0
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_v:
                self.animation_instance.start_velocity = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_defl:
                self.animation_instance.start_deflection = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.c_input_max:
                self.slider_c.max = new_value

            case self.slider_m:
                self.animation_instance.m = new_value
                omega_0 = np.sqrt(
                    2 * self.animation_instance.c / (3 * self.animation_instance.m)
                )
                self.slider_omega.max = omega_0
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_omega:
                self.animation_instance.omega = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_alpha:
                self.animation_instance.alpha = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_f_hat:
                self.animation_instance.f_hat = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.play:
                if new_value == True:
                    for s in self.sliders:
                        s.disabled = True
                    self.c_input_max.disabled = True

            case self.play_slider:
                # if reset button pressed, enable controls
                if new_value == self.play.min:
                    for s in self.sliders:
                        s.disabled = False
                    self.c_input_max.disabled = False
                    # handle omega and alpha slider
                    if self.animation_instance.mode == "Lineary Increasing":
                        self.slider_omega.disabled = True
                        self.slider_alpha.disabled = False

                    else:
                        self.slider_omega.disabled = False
                        self.slider_alpha.disabled = True

                    # disable repeat
                    self.play.repeat = False

                global FIRST_FRAME_CHANGE
                # animate blob in gaph
                # animate blob in gaph
                self.plot_manager.update_blobs()

                # animate pendulum
                self.animation_instance.frame = new_value
                self.animation_instance._animate_visual()
                if FIRST_FRAME_CHANGE == False:
                    FIRST_FRAME_CHANGE = True

                if new_value == A1_U2_NUM_DATA_POINTS - 1:
                    FIRST_FRAME_CHANGE = False
