from typing import Any
import numpy as np
from ipycanvas import MultiCanvas
import ipywidgets.widgets as widgets
from ipywidgets import (
    VBox,
    AppLayout,
    GridspecLayout,
)

from .gui_superclass import GUISuperclass
from ..mpl_managers.a2_u2_mpl_manager import PlotManagerA2U2
from ..utils.constants import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    A2_U2_NUM_DATA_POINTS,
    A2_U2_J_A_DEFAULT,
    A2_U2_J_A_MAX,
    A2_U2_J_A_MIN,
    A2_U2_L_DEFAULT,
    A2_U2_L_MAX,
    A2_U2_L_MIN,
    A2_U2_C_DEFAULT,
    A2_U2_C_MAX,
    A2_U2_C_MIN,
    A2_U2_D_DEFAULT,
    A2_U2_D_MAX,
    A2_U2_D_MIN,
    A2_U2_U_HAT_DEFAULT,
    A2_U2_U_HAT_MAX,
    A2_U2_U_HAT_MIN,
    A2_U2_PHI_0_DEFAULT,
    A2_U2_PHI_0_MAX,
    A2_U2_PHI_0_MIN,
    A2_U2_PHI_0_DOT_DEFAULT,
    A2_U2_PHI_0_DOT_MAX,
    A2_U2_PHI_0_DOT_MIN,
    A2_U2_OMEGA_DEFAULT,
    A2_U2_OMEGA_MAX,
    A2_U2_OMEGA_MIN,
    A2_U2_ALPHA_DEFAULT,
    A2_U2_ALPHA_MIN,
    A2_U2_ALPHA_MAX,
)

"""
See Superclass for additional documentation.
"""

FIRST_FRAME_CHANGE: bool = False


class GUI(GUISuperclass):
    def __init__(self, default_c, default_d, animation_instance: Any):
        super().__init__()
        self.animation_instance = animation_instance
        # set constants as class variables
        self.default_c = default_c
        self.default_d = default_d
        self.freeze_change = False

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
        self.plot_manager = PlotManagerA2U2(animation_instance)

        # after inital set up, set up gui elements
        app_layout = self.make_gui()

        return app_layout

    def make_gui(self):

        # make control elements for parameters
        (
            slider_d,
            slider_c,
            slider_ja,
            slider_L,
            slider_u_hat,
            slider_phi0,
            slider_phi0_dot,
            slider_omega,
            slider_alpha,
            radio_buttons,
            reset_button,
        ) = self.make_parameter_control_elements()
        # make slider grid
        slider_grid = VBox(
            [
                slider_d,
                slider_c,
                slider_ja,
                slider_L,
                slider_u_hat,
                slider_phi0,
                slider_phi0_dot,
                slider_omega,
                slider_alpha,
            ]
        )

        # make titles
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
        play_control_widget = self.make_play_control_element(A2_U2_NUM_DATA_POINTS)

        self.app_layout = self.place_and_coordinate_gui_elements(
            play_control_widget,
            slider_grid,
            title_grid,
            reset_button,
            radio_buttons,
        )
        # set vars
        self.animation_instance.set_vars_and_coordinates()
        # draw inital visual
        self.animation_instance._initial_visual()
        # draw first frame
        self.animation_instance.draw_first_frame()

    def make_parameter_control_elements(self) -> widgets:

        slider_c = widgets.FloatSlider(
            value=A2_U2_C_DEFAULT,
            min=A2_U2_C_MIN,
            max=A2_U2_C_MAX,
            step=0.01,
            description="c",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_c = slider_c

        slider_d = widgets.FloatSlider(
            value=A2_U2_D_DEFAULT,
            min=A2_U2_D_MIN,
            max=A2_U2_D_MAX,
            step=0.01,
            description="d",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_d = slider_d

        slider_ja = widgets.FloatSlider(
            value=A2_U2_J_A_DEFAULT,
            min=A2_U2_J_A_MIN,
            max=A2_U2_J_A_MAX,
            step=0.01,
            description="Jₐ",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_ja = slider_ja

        slider_L = widgets.FloatSlider(
            value=A2_U2_L_DEFAULT,
            min=A2_U2_L_MIN,
            max=A2_U2_L_MAX,
            step=0.01,
            description="L",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_L = slider_L

        slider_u_hat = widgets.FloatSlider(
            value=A2_U2_U_HAT_DEFAULT,
            min=A2_U2_U_HAT_MIN,
            max=A2_U2_U_HAT_MAX,
            step=0.01,
            description="û",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_u_hat = slider_u_hat

        slider_phi0 = widgets.FloatSlider(
            value=A2_U2_PHI_0_DEFAULT,
            min=A2_U2_PHI_0_MIN,
            max=A2_U2_PHI_0_MAX,
            step=0.01,
            description="φ₀",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_phi0 = slider_phi0

        slider_phi0_dot = widgets.FloatSlider(
            value=A2_U2_PHI_0_DOT_DEFAULT,
            min=A2_U2_PHI_0_DOT_MIN,
            max=A2_U2_PHI_0_DOT_MAX,
            step=0.01,
            description="φ̇₀",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_phi0_dot = slider_phi0_dot

        slider_omega = widgets.FloatSlider(
            value=A2_U2_OMEGA_DEFAULT,
            min=A2_U2_OMEGA_MIN,
            max=A2_U2_OMEGA_MAX,
            step=0.01,
            description="Ω",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_omega = slider_omega

        slider_alpha = widgets.FloatSlider(
            value=A2_U2_ALPHA_DEFAULT,
            min=A2_U2_ALPHA_MIN,
            max=A2_U2_ALPHA_MAX,
            step=0.01,
            description="α",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_alpha = slider_alpha

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
            disabled=False,
        )
        self.reset_button = reset_button
        self.reset_button.on_click(self.reset_parameters)

        self.sliders = [
            slider_d,
            slider_c,
            slider_ja,
            slider_L,
            slider_u_hat,
            slider_phi0,
            slider_phi0_dot,
            slider_omega,
            slider_alpha,
        ]

        self.sliders_and_radio_buttons = [
            slider_d,
            slider_c,
            slider_ja,
            slider_L,
            slider_u_hat,
            slider_phi0,
            slider_phi0_dot,
            slider_omega,
            slider_alpha,
            self.radio_buttons,
        ]

        # define observe functions
        for s in self.sliders_and_radio_buttons:
            s.observe(self.on_value_change, names="value")

        return (
            slider_d,
            slider_c,
            slider_ja,
            slider_L,
            slider_u_hat,
            slider_phi0,
            slider_phi0_dot,
            slider_omega,
            slider_alpha,
            reset_button,
            radio_buttons,
        )

    def place_and_coordinate_gui_elements(
        self,
        play_control_widget: widgets,
        slider_grid: widgets,
        title_grid: widgets,
        reset_button,
        radio_buttons,
    ) -> widgets:

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

        # freeze the change of the graph
        self.freeze_change = True

        self.slider_d.value = A2_U2_D_DEFAULT
        self.slider_c.value = A2_U2_C_DEFAULT
        self.slider_ja.value = A2_U2_J_A_DEFAULT
        self.slider_L.value = A2_U2_L_DEFAULT
        self.slider_u_hat.value = A2_U2_U_HAT_DEFAULT
        self.slider_phi0.value = A2_U2_PHI_0_DEFAULT
        self.slider_phi0_dot.value = A2_U2_PHI_0_DOT_DEFAULT
        self.slider_omega.value = A2_U2_OMEGA_DEFAULT
        self.slider_alpha.value = A2_U2_ALPHA_DEFAULT
        self.radio_buttons.value = "Lineary Increasing"

        # unfreeze the change of the graph
        self.freeze_change = False

        # calculate default solution
        self.plot_manager.calc_and_plot_solutions()

    def on_value_change(self, change):
        widget = change.owner
        new_value = change["new"]

        match widget:
            case self.slider_d:
                self.animation_instance.d = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_c:
                omega_0 = np.sqrt(
                    (new_value * self.slider_L.value**2) / self.slider_ja.value
                )
                self.slider_omega.max = 2 * omega_0
                self.animation_instance.c = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_ja:
                omega_0 = np.sqrt(
                    (self.slider_c.value * self.slider_L.value**2) / new_value
                )
                self.slider_omega.max = 2 * omega_0
                self.animation_instance.j_a = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_L:
                omega_0 = np.sqrt(
                    (self.slider_c.value * new_value**2) / self.slider_ja.value
                )
                self.slider_omega.max = 2 * omega_0
                self.animation_instance.L = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_u_hat:
                self.animation_instance.u_hat = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_phi0:
                new_value = np.pi * new_value / 180
                self.animation_instance.phi_0 = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_phi0_dot:
                self.animation_instance.phi_0_dot = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_omega:
                if new_value == 0:
                    temp_new_value = 0.1
                    self.slider_alpha.max = temp_new_value
                    self.slider_alpha.min = temp_new_value / 100
                else:
                    self.slider_alpha.max = new_value
                    self.slider_alpha.min = new_value / 100
                self.animation_instance.omega = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

            case self.slider_alpha:
                self.animation_instance.alpha = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()

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

            case self.play:
                if new_value == True:
                    for s in self.sliders:
                        s.disabled = True

            case self.play_slider:
                # if reset button pressed, enable controls
                if new_value == self.play.min:
                    for s in self.sliders:
                        s.disabled = False
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
                self.animation_instance.animate_visual()
                if FIRST_FRAME_CHANGE == False:
                    FIRST_FRAME_CHANGE = True

                if new_value == A2_U2_NUM_DATA_POINTS - 1:
                    FIRST_FRAME_CHANGE = False
