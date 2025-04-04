import numpy as np
from ipycanvas import MultiCanvas
import ipywidgets.widgets as widgets
from ipywidgets import (
    VBox,
    AppLayout,
    GridspecLayout,
)

from .mpl_manager_3 import PlotManager
from ..utils.constants import (
    DEFAULT_D_MIN_3,
    DEFAULT_D_MAX_3,
    DEFAULT_M_3,
    DEFAULT_M_MIN_3,
    DEFAULT_M_MAX_3,
    DEFAULT_MU_3,
    DEFAULT_MU_MIN_3,
    DEFAULT_MU_MAX_3,
    DEFAULT_C_MIN_3,
    DEFAULT_C_MAX_3,
    DEFAULT_EPS_3,
    DEFAULT_EPS_MIN_3,
    DEFAULT_EPS_MAX_3,
    DEFAULT_Z0_3,
    DEFAULT_Z0_MIN_3,
    DEFAULT_Z0_MAX_3,
    DEFAULT_Z0D_3,
    DEFAULT_Z0D_MIN_3,
    DEFAULT_Z0D_MAX_3,
    DEFAULT_OMEGA_3,
    DEFAULT_OMEGA_MAX_3,
    DEFAULT_OMEGA_MIN_3,
    DEFAULT_ALPHA_3,
    DEFAULT_ALPHA_MIN_3,
    DEFAULT_ALPHA_MAX_3,
    NUM_DATAPOINTS_3,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)


"""Module containing functions to build an interactive ui for displaying
    and manipulating animations.
"""

FIRST_FRAME_CHANGE: bool = False


class GUI:
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
        self.animation_instance.mode = "Acceleration"
        self.freeze_change = False

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

        # set up mpl
        self.plot_manager = PlotManager(animation_instance)

        # set up calc button
        # self.calc_button = widgets.Button(
        #     description="Calculate",
        #     disabled=False,
        #     button_style="",
        #     layout=widgets.Layout(width="15%", display="flex", top="5%"),
        # )
        # self.calc_button.on_click(lambda b: self.calc_button_click(b))

        # after inital set up, set up gui elements
        app_layout = self.gui_elements()

        return app_layout

    def gui_elements(self):
        """General function to coordinate gui elements."""

        # make control elements for parameters
        (
            slider_d,
            slider_c,
            c_input_max,
            slider_m,
            slider_mu,
            slider_eps,
            slider_z0,
            slider_z0d,
            slider_omega,
            slider_alpha,
            reset_button,
            radio_buttons,
        ) = self.variables_control_elements()

        # make slider grid
        slider_grid = VBox(
            [
                slider_d,
                slider_c,
                c_input_max,
                slider_m,
                slider_mu,
                slider_eps,
                slider_z0,
                slider_z0d,
                slider_omega,
                slider_alpha,
            ],
            layout=widgets.Layout(top="-2%"),
        )

        # make titles
        slider_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Variables</strong>'
        )
        anim_title = widgets.HTML(
            '<strong style="font-family: Arial, sans-serif;">Animation</strong>'
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
        play_control_widget = self.play_control_element()

        self.app_layout = self.place_gui_elements(
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

    def variables_control_elements(self) -> widgets:
        """Function to create and place parameter control elements.

        Returns:
            widgets: Sliders and control elements for the parameters.
        """

        slider_d = widgets.FloatSlider(
            value=self.default_d,
            min=DEFAULT_D_MIN_3,
            max=DEFAULT_D_MAX_3,
            step=1.0,
            description="d",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
            tooltip="damping coefficient",
        )
        self.slider_d = slider_d

        slider_c = widgets.FloatSlider(
            value=self.default_c,
            min=DEFAULT_C_MIN_3,
            max=DEFAULT_C_MAX_3,
            step=1.0,
            description="c",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
            tooltip="spring constant",
        )
        self.slider_c = slider_c

        c_input_max = widgets.BoundedFloatText(
            value=round(DEFAULT_C_MAX_3, 2),
            min=DEFAULT_C_MIN_3,
            max=2 * DEFAULT_C_MAX_3,
            step=1.0,
            description="c max:",
            readout_format=".2f",
            disabled=False,
            layout=widgets.Layout(display="flex", width="50%"),
        )
        c_input_max.observe(self.on_value_change, names="value")
        self.c_input_max = c_input_max

        slider_m = widgets.FloatSlider(
            value=DEFAULT_M_3,
            min=DEFAULT_M_MIN_3,
            max=DEFAULT_M_MAX_3,
            step=1.0,
            description="m",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
            tooltip="mass",
        )
        self.slider_m = slider_m

        slider_mu = widgets.FloatSlider(
            value=DEFAULT_MU_3,
            min=DEFAULT_MU_MIN_3,
            max=DEFAULT_MU_MAX_3,
            step=1.0,
            description="mu",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
            tooltip="mu",
        )
        self.slider_mu = slider_mu

        slider_eps = widgets.FloatSlider(
            value=DEFAULT_EPS_3,
            min=DEFAULT_EPS_MIN_3,
            max=DEFAULT_EPS_MAX_3,
            step=1.0,
            description="ε",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
            tooltip="eps",
        )
        self.slider_eps = slider_eps

        slider_z0 = widgets.FloatSlider(
            value=DEFAULT_Z0_3,
            min=DEFAULT_Z0_MIN_3,
            max=DEFAULT_Z0_MAX_3,
            step=1.0,
            description="z0",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
            tooltip="z0",
        )
        self.slider_z0 = slider_z0

        slider_z0d = widgets.FloatSlider(
            value=DEFAULT_Z0D_3,
            min=DEFAULT_Z0D_MIN_3,
            max=DEFAULT_Z0D_MAX_3,
            step=1.0,
            description="z0d",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
            tooltip="z0d",
        )
        self.slider_z0d = slider_z0d

        slider_omega = widgets.FloatSlider(
            value=DEFAULT_OMEGA_3,
            min=DEFAULT_OMEGA_MIN_3,
            max=DEFAULT_OMEGA_MAX_3,
            step=1.0,
            description="Ω",
            continuous_update=False,
            orientation="horizontal",
            disabled=True,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
            tooltip="omega",
        )
        self.slider_omega = slider_omega

        slider_alpha = widgets.FloatSlider(
            value=DEFAULT_ALPHA_3,
            min=DEFAULT_ALPHA_MIN_3,
            max=DEFAULT_ALPHA_MAX_3,
            step=1.0,
            description="α",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
            tooltip="alpha",
        )
        self.slider_alpha = slider_alpha

        radio_buttons = widgets.RadioButtons(
            options=["Acceleration", "Steady State"],
            value="Acceleration",
            # layout=widgets.Layout(top="-5%"),
            description="Exitation Frequency",
            disabled=False,
            orientation="horizontal",
        )
        self.radio_buttons = radio_buttons

        reset_button = widgets.Button(
            description="Reset",
            layout=widgets.Layout(display="flex"),
            diabled=False,
        )
        self.reset_button = reset_button
        self.reset_button.on_click(self.reset_parameters)

        self.sliders = [
            self.slider_d,
            self.slider_c,
            self.slider_m,
            self.slider_mu,
            self.slider_eps,
            self.slider_z0,
            self.slider_z0d,
            self.slider_omega,
            self.slider_alpha,
        ]

        self.sliders_and_radio_buttons = [
            self.slider_d,
            self.slider_c,
            self.slider_m,
            self.slider_mu,
            self.slider_eps,
            self.slider_z0,
            self.slider_z0d,
            self.slider_omega,
            self.slider_alpha,
            self.radio_buttons,
        ]

        # define observe functions
        for s in self.sliders_and_radio_buttons:
            s.observe(self.on_value_change, names="value")

        return (
            self.slider_d,
            self.slider_c,
            self.c_input_max,
            self.slider_m,
            self.slider_mu,
            self.slider_eps,
            self.slider_z0,
            self.slider_z0d,
            self.slider_omega,
            self.slider_alpha,
            self.reset_button,
            self.radio_buttons,
        )

    def play_control_element(self) -> widgets:
        """Function to create the play control element. Stop/restart/
            loop animation and slide through frames.

        Returns:
            widgets: Returns play control element.
        """
        play = widgets.Play(
            value=0,
            min=0,
            max=NUM_DATAPOINTS_3 - 1,
            step=1,
            interval=25,
            description="Press play",
            disabled=False,
        )

        play_slider = widgets.IntSlider(
            disabled=False,
            min=0,
            max=NUM_DATAPOINTS_3 - 1,
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

    def place_gui_elements(
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
            pane_heights=["60%", "20%", "20%"],
            layout=widgets.Layout(left="2%"),
        )

        # make tab for graphs
        tab = widgets.Tab()
        children = [
            self.plot_manager.fig_steady_state.canvas,
            self.plot_manager.fig_acceleration.canvas,
            self.plot_manager.fig_bode.canvas,
        ]
        tab.children = children
        tab.titles = ["Steady State", "Acceleration", "Bode Diagram"]

        app_layout = AppLayout(
            header=title_grid,
            left_sidebar=interactive_grid,
            center=self.mult_canvas_anim,
            right_sidebar=tab,
            footer=None,
            pane_widths=["33%", "33%", "33%"],
            pane_heights=["10%", "90%", "0%"],
        )

        # # make border on left side
        # self.animation_instance.anim_canvas[4].begin_path()
        # self.animation_instance.anim_canvas[4].move_to(0, 0)
        # self.animation_instance.anim_canvas[4].line_to(
        #     0, self.animation_instance.anim_canvas[4].height
        # )
        # self.animation_instance.anim_canvas[4].stroke()
        # # make border on right side
        # self.animation_instance.anim_canvas[4].begin_path()
        # self.animation_instance.anim_canvas[4].move_to(
        #     self.animation_instance.anim_canvas[4].width, 0
        # )
        # self.animation_instance.anim_canvas[4].line_to(
        #     self.animation_instance.anim_canvas[4].width,
        #     self.animation_instance.anim_canvas[4].height,
        # )
        # self.animation_instance.anim_canvas[4].stroke()

        return app_layout

    def calc_and_set_solution(self):
        """Calculate new solution and update plots"""
        sol_acc, sol_acc_force, sol_steady, sol_steady_force = (
            self.animation_instance._calculate()
        )
        omega_vec, omega_0, mag, mag_undamped, phase = (
            self.animation_instance.calc_bode_diagram()
        )

        self.plot_manager.update_plots(
            sol_acc,
            sol_acc_force,
            sol_steady,
            sol_steady_force,
            omega_vec,
            omega_0,
            mag,
            mag_undamped,
            phase,
        )

        # Update blob position
        self.plot_manager.update_blobs(self.animation_instance.frame)

    def reset_parameters(self, button):
        """Function to reset all parameters to default values.

        Args:
            button (widgets.Button): Button that triggers the reset.
        """

        # freeze the change of the graph
        self.freeze_change = True

        self.slider_d.value = self.default_d
        self.slider_c.value = self.default_c
        self.c_input_max.value = DEFAULT_C_MAX_3
        self.slider_m.value = DEFAULT_M_3

        self.radio_buttons.value = "Acceleration"

        # unfreeze the change of the graph
        self.freeze_change = False

        # calculate default solution
        self.calc_and_set_solution()

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

                if self.animation_instance.mode == "Acceleration":
                    self.slider_omega.disabled = True
                    self.slider_alpha.disabled = False

                else:
                    self.slider_omega.disabled = False
                    self.slider_alpha.disabled = True

                if not self.freeze_change:
                    self.calc_and_set_solution()

            case self.slider_d:
                self.animation_instance.d = new_value
                if not self.freeze_change:
                    self.calc_and_set_solution()

            case self.slider_c:
                self.animation_instance.c = new_value
                omega_0 = np.sqrt(self.animation_instance.c / self.animation_instance.m)
                self.slider_omega.max = omega_0
                if not self.freeze_change:
                    self.calc_and_set_solution()

            case self.c_input_max:
                # reset c max to min if user input is smaller than min
                if new_value < self.c_input_max.min:
                    self.c_input_max.value = self.c_input_max.min
                self.slider_c.max = new_value

            case self.slider_m:
                self.animation_instance.m = new_value
                omega_0 = np.sqrt(self.animation_instance.c / self.animation_instance.m)
                self.slider_omega.max = omega_0
                if not self.freeze_change:
                    self.calc_and_set_solution()

            case self.slider_mu:
                self.animation_instance.m_u = new_value
                if not self.freeze_change:
                    self.calc_and_set_solution()

            case self.slider_eps:
                self.animation_instance.eps = new_value
                if not self.freeze_change:
                    self.calc_and_set_solution()

            case self.slider_z0:
                self.animation_instance.z0 = new_value
                if not self.freeze_change:
                    self.calc_and_set_solution()

            case self.slider_z0d:
                self.animation_instance.z0d = new_value
                if not self.freeze_change:
                    self.calc_and_set_solution()

            case self.slider_omega:
                self.animation_instance.omega = new_value
                if not self.freeze_change:
                    self.calc_and_set_solution()

            case self.slider_alpha:
                self.animation_instance.alpha = new_value
                if not self.freeze_change:
                    self.calc_and_set_solution()

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
                    if self.animation_instance.mode == "Acceleration":
                        self.slider_omega.disabled = True
                        self.slider_alpha.disabled = False

                    else:
                        self.slider_omega.disabled = False
                        self.slider_alpha.disabled = True

                    # disable repeat
                    self.play.repeat = False

                global FIRST_FRAME_CHANGE
                # # blob in acc
                # x = [self.t[new_value]]
                # y_acc = [self.animation_instance.sol_acc[new_value]]
                # y_steady = [self.animation_instance.sol_steady[new_value]]
                # self.blob_acc.set_data(x, y_acc)
                # self.blob_steady.set_data(x, y_steady)

                # self.fig_steady_state.canvas.draw_idle()
                # self.fig_acceleration.canvas.draw_idle()
                self.plot_manager.update_blobs(self.animation_instance.frame)

                # animate oscillating system
                self.animation_instance.frame = new_value
                self.animation_instance._animate_visual()
                if FIRST_FRAME_CHANGE == False:
                    FIRST_FRAME_CHANGE = True

                if new_value == NUM_DATAPOINTS_3 - 1:
                    FIRST_FRAME_CHANGE = False
