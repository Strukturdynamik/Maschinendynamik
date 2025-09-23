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

from ..mpl_managers.a1_u5_mpl_manager import PlotManagerA1U5
from ..utils.constants import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    A1_U5_NUM_DATA_POINTS,
    A1_U5_C_DEFAULT,
    A1_U5_J_S_DEFAULT,
    A1_U5_J_S_MIN,
    A1_U5_J_S_MAX,
    A1_U5_M_DEFAULT,
    A1_U5_M_MIN,
    A1_U5_M_MAX,
    A1_U5_S_0_DEFAULT,
    A1_U5_S_0_MIN,
    A1_U5_S_0_MAX,
    A1_U5_S_00_DEFAULT,
    A1_U5_S_00_MIN,
    A1_U5_S_00_MAX,
    A1_U5_PHI_0_DEFAULT,
    A1_U5_PHI_0_MIN,
    A1_U5_PHI_0_MAX,
    A1_U5_S_DOT_0_DEFAULT,
    A1_U5_S_DOT_0_MIN,
    A1_U5_S_DOT_0_MAX,
    A1_U5_PHI_DOT_0_DEFAULT,
    A1_U5_PHI_DOT_0_MIN,
    A1_U5_PHI_DOT_0_MAX,
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
        self.plot_manager = PlotManagerA1U5(animation_instance)

        # after inital set up, set up gui elements
        app_layout = self.make_gui()

        return app_layout

    def make_gui(self):

        # make control elements for parameters
        (
            slider_j_s,
            slider_m,
            slider_c,
            slider_s_0,
            slider_s_00,
            slider_phi_0,
            slider_s_dot_0,
            slider_phi_dot_0,
            reset_button,
            radio_buttons,
        ) = self.make_parameter_control_elements()
        # make slider grid
        slider_grid = VBox(
            [
                slider_j_s,
                slider_m,
                slider_c,
                slider_s_0,
                slider_s_00,
                slider_phi_0,
                slider_s_dot_0,
                slider_phi_dot_0,
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
        play_control_widget = self.make_play_control_element(A1_U5_NUM_DATA_POINTS)

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
        self.animation_instance._draw_first_frame()

    def make_parameter_control_elements(self) -> widgets:

        slider_j_s = widgets.FloatSlider(
            value=A1_U5_J_S_DEFAULT,
            min=A1_U5_J_S_MIN,
            max=A1_U5_J_S_MAX,
            step=0.01,
            description="Jₛ",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_j_s = slider_j_s

        slider_m = widgets.FloatSlider(
            value=A1_U5_M_DEFAULT,
            min=A1_U5_M_MIN,
            max=A1_U5_M_MAX,
            step=0.01,
            description="m",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_m = slider_m

        slider_c = widgets.FloatSlider(
            value=5,
            min=0,
            max=10,
            step=0.01,
            description="c",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_c = slider_c

        slider_s_0 = widgets.FloatSlider(
            value=A1_U5_S_0_DEFAULT,
            min=A1_U5_S_0_MIN,
            max=A1_U5_S_0_MAX,
            step=0.01,
            description="s₀",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_s_0 = slider_s_0

        slider_s_00 = widgets.FloatSlider(
            value=A1_U5_S_00_DEFAULT,
            min=A1_U5_S_00_MIN,
            max=A1_U5_S_00_MAX,
            step=0.01,
            description="s₀₀",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_s_00 = slider_s_00

        slider_phi_0 = widgets.FloatSlider(
            value=A1_U5_PHI_0_DEFAULT,
            min=A1_U5_PHI_0_MIN,
            max=A1_U5_PHI_0_MAX,
            step=0.01,
            description="φ₀",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_phi_0 = slider_phi_0

        slider_s_dot_0 = widgets.FloatSlider(
            value=A1_U5_S_DOT_0_DEFAULT,
            min=A1_U5_S_DOT_0_MIN,
            max=A1_U5_S_DOT_0_MAX,
            step=0.01,
            description="ṡ₀",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_s_dot_0 = slider_s_dot_0

        slider_phi_dot_0 = widgets.FloatSlider(
            value=A1_U5_PHI_DOT_0_DEFAULT,
            min=A1_U5_PHI_DOT_0_MIN,
            max=A1_U5_PHI_DOT_0_MAX,
            step=0.01,
            description="φ̇₀",
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-9%", width="90%", display="flex"),
        )
        self.slider_phi_dot_0 = slider_phi_dot_0

        radio_buttons = widgets.RadioButtons(
            options=["Nonlinear", "Linear"],
            value="Linear",
            layout=widgets.Layout(top="-0%"),
            description="Mode",
            disabled=False,
            orientation="horizontal",
        )
        self.radio_buttons = radio_buttons

        reset_button = widgets.Button(
            description="Reset",
            layout=widgets.Layout(top="-0%", display="flex"),
            disabled=False,
        )
        self.reset_button = reset_button
        self.reset_button.on_click(self.reset_parameters)

        self.sliders = [
            slider_j_s,
            slider_m,
            slider_c,
            slider_s_0,
            slider_s_00,
            slider_phi_0,
            slider_s_dot_0,
            slider_phi_dot_0,
        ]

        self.sliders_and_radio_buttons = [
            slider_j_s,
            slider_m,
            slider_c,
            slider_s_0,
            slider_s_00,
            slider_phi_0,
            slider_s_dot_0,
            slider_phi_dot_0,
            self.radio_buttons,
        ]

        # define observe functions
        for s in self.sliders_and_radio_buttons:
            s.observe(self.on_value_change, names="value")

        return (
            slider_j_s,
            slider_m,
            slider_c,
            slider_s_0,
            slider_s_00,
            slider_phi_0,
            slider_s_dot_0,
            slider_phi_dot_0,
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
            self.plot_manager.fig_s_t.canvas,
            self.plot_manager.fig_s_phi.canvas,
        ]
        tab.children = children
        tab.titles = ["Spring Displacement", "Angle"]

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

        self.slider_j_s.value = A1_U5_J_S_DEFAULT
        self.slider_m.value = A1_U5_M_DEFAULT
        self.slider_c.value = A1_U5_C_DEFAULT
        self.slider_s_0.value = A1_U5_S_0_DEFAULT
        self.slider_s_00.value = A1_U5_S_00_DEFAULT
        self.slider_phi_0.value = A1_U5_PHI_0_DEFAULT
        self.slider_s_dot_0.value = A1_U5_S_DOT_0_DEFAULT
        self.slider_phi_dot_0 = A1_U5_PHI_DOT_0_DEFAULT
        self.radio_buttons.value = "Linear"

        # unfreeze the change of the graph
        self.freeze_change = False

        # calculate default solution
        self.plot_manager.calc_and_plot_solutions()
        self.animation_instance._draw_first_frame()

    def on_value_change(self, change):
        widget = change.owner
        new_value = change["new"]

        match widget:
            case self.slider_phi_dot_0:
                self.animation_instance.phi_dot_0 = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()
                    self.animation_instance._draw_first_frame()

            case self.slider_s_dot_0:
                self.animation_instance.s_dot_0 = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()
                    self.animation_instance._draw_first_frame()

            case self.slider_phi_0:
                self.animation_instance.phi_0 = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()
                    self.animation_instance._draw_first_frame()

            case self.slider_s_00:
                self.animation_instance.s_00 = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()
                    self.animation_instance._draw_first_frame()

            case self.slider_s_0:
                self.animation_instance.s_0 = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()
                    self.animation_instance._draw_first_frame()

            case self.slider_m:
                self.animation_instance.m = new_value
                new_s_r = (
                    new_value * self.animation_instance.g / self.animation_instance.c
                    + self.animation_instance.s_0
                )
                self.animation_instance.s_r = new_s_r
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()
                    self.animation_instance._draw_first_frame()

            case self.slider_j_s:
                self.animation_instance.j_s = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()
                    self.animation_instance._draw_first_frame()

            case self.slider_c:
                self.animation_instance.c = new_value
                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()
                    self.animation_instance._draw_first_frame()

            case self.radio_buttons:
                self.animation_instance.mode = new_value

                if not self.freeze_change:
                    self.plot_manager.calc_and_plot_solutions()
                    self.animation_instance._draw_first_frame()

            case self.play:
                if new_value == True:
                    for s in self.sliders:
                        s.disabled = True

            case self.play_slider:
                # if reset button pressed, enable controls
                if new_value == self.play.min:
                    for s in self.sliders:
                        s.disabled = False
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

                if new_value == A1_U5_NUM_DATA_POINTS - 1:
                    FIRST_FRAME_CHANGE = False
