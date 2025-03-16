from typing import Any
import math
from ipycanvas import MultiCanvas
import ipywidgets.widgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import (
    VBox,
    AppLayout,
    GridspecLayout,
)


from ..utils.constants import (
    START_DEFLECTION,
    START_VELOCITY,
    DEFAULT_C_MAX,
    DEFAULT_M,
    DEFAULT_M_MAX,
    DEFAULT_OMEGA,
    DEFAULT_ALPHA,
    NUM_DATAPOINTS,
    NUM_TIME_UNITS_AUFGABE_1,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    X_LIM_START,
    X_LIM_END_AUFGABE_1,
    Y_LIM_START_AUFGABE_1,
    Y_LIM_END_AUFGABE_1,
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
        animation_instance: Any,
    ):
        """Function to build interactive ui for displaying
        and manipulating animations.
        """

        # set constants as class variables
        self.default_c = default_c
        self.default_d = default_d
        self.animation_instance = animation_instance
        self.animation_instance.mode = "Hochlauf"

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
        self.set_up_mpl()

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

    def set_up_mpl(self):
        """Set up the matplotlib outputs."""
        # Clear all existing figures to avoid duplicates
        plt.close("all")

        # set up output widget for deflection graph
        self.output_deflection = widgets.Output()
        with self.output_deflection:
            self.fig_deflection, self.ax1 = plt.subplots(figsize=(4.5, 4.5))
            self.ax1.grid(True)

            # set labels
            self.ax1.set_xlabel(
                r"$\boldsymbol{t} \: \boldsymbol{(s)}$",
            )

            self.ax1.set_ylabel(
                r"Deflection $ \boldsymbol{\Phi (t)}$ [ °]",
            )

            # remove spines
            self.ax1.spines["top"].set_visible(False)
            self.ax1.spines["right"].set_visible(False)
            self.ax1.spines["left"].set_visible(False)
            self.ax1.spines["bottom"].set_visible(False)

            # remove stuff
            self.fig_deflection.canvas.toolbar_visible = False
            self.fig_deflection.canvas.header_visible = False
            self.fig_deflection.canvas.footer_visible = False

            # make blob
            (self.blob,) = self.ax1.plot([], [], "ro", label="Blob")

            # set limits for axes
            self.ax1.set_xlim(X_LIM_START, X_LIM_END_AUFGABE_1)
            self.ax1.set_ylim(Y_LIM_START_AUFGABE_1, Y_LIM_END_AUFGABE_1)

            plt.tight_layout()
            plt.show()

        # set up output for bode diagramms
        self.output_bode = widgets.Output()
        with self.output_bode:
            self.fig_bode = plt.figure(figsize=(4, 4))
            # subplots (2 rows, 1 column)
            self.ax1_bode = self.fig_bode.add_subplot(2, 1, 1)  # first subplot
            self.ax2_bode = self.fig_bode.add_subplot(2, 1, 2)  # second subplot

            # add grid
            self.ax1_bode.grid(True)
            self.ax2_bode.grid(True)

            # labels ax1
            self.ax1_bode.set_ylabel(
                r"Magnitude [abs]",
            )

            # labels ax2
            self.ax2_bode.set_xlabel(
                r"$\Omega$ / $\omega_{0}$",
            )

            self.ax2_bode.set_ylabel(
                r"Phase [°]",
            )

            # remove spines
            self.ax1_bode.spines["top"].set_visible(False)
            self.ax1_bode.spines["right"].set_visible(False)
            self.ax1_bode.spines["left"].set_visible(False)
            self.ax1_bode.spines["bottom"].set_visible(False)

            self.ax2_bode.spines["top"].set_visible(False)
            self.ax2_bode.spines["right"].set_visible(False)
            self.ax2_bode.spines["left"].set_visible(False)
            self.ax2_bode.spines["bottom"].set_visible(False)

            # remove stuff
            self.fig_bode.canvas.toolbar_visible = False
            self.fig_bode.canvas.header_visible = False
            self.fig_bode.canvas.footer_visible = False

            # set limits for axes
            self.ax1_bode.set_xlim(0, 2)
            self.ax1_bode.set_ylim(0, 10)
            self.ax2_bode.set_xlim(0, 2)
            self.ax2_bode.set_ylim(-200, 10)

            plt.tight_layout()  # Adjust layout to prevent overlapping
            plt.show()

        # labels
        plt.rcParams["font.family"] = "Arial"
        plt.rcParams["mathtext.fontset"] = "stix"
        plt.rcParams["mathtext.rm"] = "serif"
        plt.rcParams["mathtext.it"] = "serif:italic"
        plt.rcParams["mathtext.bf"] = "serif:bold"

        # axes
        plt.axhline(0, color="black", linewidth=1)
        plt.axvline(0, color="black", linewidth=1)

        # plot default solutions
        self.t = np.linspace(0, NUM_TIME_UNITS_AUFGABE_1, NUM_DATAPOINTS)
        # amplitude solution
        solution = self.animation_instance._calculate()
        (self.line,) = self.ax1.plot(
            self.t, solution, color="red", linewidth=0.75, linestyle="--"
        )

        # Anregungsgraph
        # alpha = self.animation_instance.omega / 100
        # if animation_instance.mode == "Hochlauf":
        #     self.ax1.plot(
        #         self.t,
        #         np.cos(0.5 * self.animation_instance.alpha * self.t**2),
        #         linewidth=0.75,
        #         linestyle="-",
        #         color="blue",
        #     )

        # if animation_instance.mode == "Dauerlauf":
        #     self.ax1.plot(
        #         self.t,
        #         np.cos(self.animation_instance.omega * self.t),
        #         linewidth=0.75,
        #         linestyle="-",
        #         color="blue",
        #     )

        # bode diagram
        omega_vec, omega_0, mag, mag_undamped, phase = (
            self.animation_instance.calc_bode_diagram()
        )
        # ax1
        (self.line_bode_1_1,) = self.ax1_bode.plot(
            omega_vec / omega_0, mag, linewidth=0.75, linestyle="--", color="red"
        )
        (self.line_bode_1_2,) = self.ax1_bode.plot(
            omega_vec / omega_0,
            mag_undamped,
            linestyle="--",
            color="blue",
            alpha=0.25,
            linewidth=0.75,
        )
        # ax2
        (self.line_bod_2,) = self.ax2_bode.plot(
            omega_vec / omega_0, phase, linestyle="--", linewidth=0.75, color="red"
        )

    def gui_elements(self):
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
            radio_buttons,
        ) = self.variables_control_elements()

        # make slider grid
        slider_grid = VBox(
            [
                slider_d,
                slider_c,
                c_input_max,
                slider_m,
                slider_omega,
                slider_alpha,
                slider_defl,
                slider_v,
                radio_buttons,
            ]
        )

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
            animation_title, play_control_widget, slider_grid, title_grid
        )

        # draw inital visual
        self.animation_instance._initial_visual()
        # draw first frame
        self.animation_instance._draw_first_frame()

    def variables_control_elements(self) -> widgets:
        """Function to create and place parameter control elements

        Returns:
            widgets: Returns parameter Slider.
        """

        slider_d = widgets.FloatSlider(
            value=round(self.default_d, 2),
            min=0.0,
            max=20.0,
            step=0.01,
            description="d",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
        )
        self.slider_d = slider_d

        slider_c = widgets.FloatSlider(
            value=round(self.default_c, 2),
            min=0.1,
            max=round(DEFAULT_C_MAX, 2),
            step=0.01,
            description="c",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
        )
        self.slider_c = slider_c

        slider_m = widgets.FloatSlider(
            value=round(DEFAULT_M, 2),
            min=0.1,
            max=round(DEFAULT_M_MAX, 2),
            step=0.01,
            description="m",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
        )
        self.slider_m = slider_m

        c_input_max = widgets.BoundedFloatText(
            value=round(DEFAULT_C_MAX, 2),
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
            value=round(START_VELOCITY, 4),
            min=min_v,
            max=max_v,
            step=0.0001,
            description="v0",  # r"$v_{0}$",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-10%", width="88%", display="flex"),
        )
        self.slider_v = slider_v

        max_defl = round(math.pi, 4) / 10
        min_defl = round(math.pi, 4) / 30
        slider_defl = widgets.FloatSlider(
            value=round(START_DEFLECTION, 4),
            min=min_defl,
            max=max_defl,
            step=0.01,
            description="defl",  # r"$defl_{0}$",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".4f",
            layout=widgets.Layout(left="-10%", width="88%", display="flex"),
        )
        self.slider_defl = slider_defl

        slider_omega = widgets.FloatSlider(
            value=DEFAULT_OMEGA,
            min=0.0,
            max=5.0,
            step=0.01,
            description="Ω",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
        )
        self.slider_omega = slider_omega

        slider_alpha = widgets.FloatSlider(
            value=DEFAULT_ALPHA,
            min=0.0,
            max=5.0,
            step=0.01,
            description="α",
            continuous_update=False,
            orientation="horizontal",
            disabled=False,
            readout=True,
            readout_format=".2f",
            layout=widgets.Layout(left="-10%", width="90%", display="flex"),
        )
        self.slider_alpha = slider_alpha

        radio_buttons = widgets.RadioButtons(
            options=["Hochlauf", "Dauerlauf"],
            value="Hochlauf",
            layout={"width": "max-content"},
            description="",
            disabled=False,
            orientation="horizontal",
        )
        self.radio_buttons = radio_buttons

        self.slider = [
            slider_d,
            slider_c,
            slider_v,
            slider_m,
            slider_defl,
            slider_omega,
            slider_alpha,
        ]

        # define observe functions
        for s in self.slider:
            s.observe(self.on_value_change, names="value")
        radio_buttons.observe(self.on_value_change, names="value")

        return (
            slider_d,
            slider_c,
            c_input_max,
            slider_defl,
            slider_v,
            slider_m,
            slider_omega,
            slider_alpha,
            radio_buttons,
        )

    def play_control_element(self) -> widgets:
        """Function to create play control element.

        Returns:
            widgets: Returns play control element.
        """
        play = widgets.Play(
            value=0,
            min=0,
            max=NUM_DATAPOINTS - 1,
            step=1,
            interval=25,
            description="Press play",
            disabled=False,
        )

        play_slider = widgets.IntSlider(
            disabled=False,
            min=0,
            max=NUM_DATAPOINTS - 1,
            step=1,
            interval=25,
        )
        self.play_slider = play_slider
        self.play = play
        self.play.repeat.disabled = True
        widgets.jslink((play, "value"), (play_slider, "value"))
        play_control_widget = widgets.HBox([play, play_slider])
        play_slider.observe(self.on_value_change, names="value")
        play.observe(self.on_value_change, names="playing")

        return play_control_widget

    def place_gui_elements(
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
            left_sidebar=play_control_widget,
            center=None,
            right_sidebar=None,
            footer=None,
            pane_widths=["100%", "0%", "0%"],
            pane_heights=["15%", "15%", "15%"],
        )

        # make grid for interacitve part
        interactive_grid = GridspecLayout(2, 1)
        interactive_grid[0, 0] = slider_grid
        interactive_grid[1, 0] = anim_inter_grid

        # make tab for graphs
        tab = widgets.Tab()
        children = [self.fig_deflection.canvas, self.fig_bode.canvas]
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

    def calc_and_set_solution(self):
        """Calculate solution based on new parameters and set y data."""
        # calculate solution
        solution = self.animation_instance._calculate()
        # set new y data
        self.line.set_ydata(solution)
        self.fig_deflection.canvas.draw()  # Redraw the canvas
        # set blob
        x = [self.t[self.animation_instance.frame]]
        y = [self.animation_instance.solution[self.animation_instance.frame]]
        self.blob.set_data(x, y)
        self.ax1.relim()  # Recompute the limits
        self.ax1.autoscale_view()

        # update axes
        # self.ax1.set_xlim([self.t[0], self.t[-1]])  # Dynamically adjust x limits
        self.ax1.set_ylim([min(solution) * 1.1, max(solution) * 1.1])  # Scale y limits
        self.ax1.relim()  # Recompute limits
        self.ax1.autoscale_view()  # Autoscale view

        # calculate bode diagramm
        omega_vec, omega_0, mag, mag_undamped, phase = (
            self.animation_instance.calc_bode_diagram()
        )
        # first plot
        self.line_bode_1_1.set_ydata(mag)
        self.line_bode_1_1.set_xdata(omega_vec / omega_0)
        self.line_bode_1_2.set_ydata(mag_undamped)
        self.line_bode_1_2.set_xdata(omega_vec / omega_0)

        # # update axes
        # self.ax1_bode.relim()
        # self.ax1_bode.autoscale_view()

        # second plot
        self.line_bod_2.set_ydata(phase)
        self.line_bod_2.set_xdata(omega_vec / omega_0)

        # # update axes
        # self.ax2_bode.relim()
        # self.ax2_bode.autoscale_view()

        # # Redraw Bode figure
        # self.fig_bode.canvas.draw_idle()

    def on_value_change(self, change):
        """Unified observer for handling parameter slider value changes."""
        widget = change.owner
        new_value = change["new"]

        print("new value: ", new_value)

        match widget:
            case self.radio_buttons:
                self.animation_instance.mode = new_value
                self.calc_and_set_solution()

            case self.slider_d:
                self.animation_instance.d = new_value
                self.calc_and_set_solution()

            case self.slider_c:
                self.animation_instance.c = new_value
                omega_0 = np.sqrt(
                    2 * self.animation_instance.c / (3 * self.animation_instance.m)
                )
                self.slider_omega.max = omega_0
                self.calc_and_set_solution()

            case self.slider_v:
                self.animation_instance.start_velocity = new_value
                self.calc_and_set_solution()

            case self.slider_defl:
                self.animation_instance.start_deflection = new_value
                self.calc_and_set_solution()

            case self.c_input_max:
                self.slider_c.max = new_value

            case self.slider_m:
                self.animation_instance.m = new_value
                omega_0 = np.sqrt(
                    2 * self.animation_instance.c / (3 * self.animation_instance.m)
                )
                self.slider_omega.max = omega_0
                self.calc_and_set_solution()

            case self.slider_omega:
                self.animation_instance.omega = new_value
                self.calc_and_set_solution()

            case self.slider_alpha:
                self.animation_instance.alpha = new_value
                self.calc_and_set_solution()

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
                x = [self.t[new_value]]
                y = [self.animation_instance.solution[new_value]]
                self.blob.set_data(x, y)
                self.fig_deflection.canvas.draw_idle()

                # animate pendulum
                self.animation_instance.frame = new_value
                self.animation_instance._animate_visual()
                if FIRST_FRAME_CHANGE == False:
                    FIRST_FRAME_CHANGE = True

                if new_value == NUM_DATAPOINTS - 1:
                    FIRST_FRAME_CHANGE = False
