import ipywidgets.widgets as widgets
import matplotlib.pyplot as plt
import numpy as np

from ...utils.constants import A1_U2_T
from .mpl_manager_superclass import PlotManagerSuperclass


class PlotManagerA1U2(PlotManagerSuperclass):
    def __init__(self, animation_instance):
        self.animation_instance = animation_instance
        self.blobs_dict = {}  # keys: blob, values: solutions for the blobs
        self.figure_lines_dict = {}  # keys: figure, values: list[lines for the figure]
        self.lines_sol_dict = {}  # key: lines, value: tuple(t arr, solution arr)
        self.axes = []  # list of axes
        self.t = A1_U2_T
        self.setup_plots()

    def setup_plots(self):
        """Initialize all matplotlib plots"""
        self.setup_deflection_plot()
        self.setup_bode_plot()
        self.set_plot_styles()
        self.calc_and_plot_solutions()

    def setup_deflection_plot(self):
        self.output_deflection = widgets.Output()
        with self.output_deflection:
            self.fig_deflection, self.ax1 = plt.subplots(figsize=(5, 5))
            # second y axis
            self.ax1_second_yaxis = self.ax1.twinx()
            # blob
            (self.blob,) = self.ax1.plot([], [], "bo")
            # lines
            (self.line_deflection,) = self.ax1.plot(
                [],
                [],
                color="blue",
                linewidth=0.75,
                linestyle="-",
                label="Deflection",
            )
            (self.line_force,) = self.ax1.plot(
                [],
                [],
                linewidth=0.65,
                linestyle="--",
                color="red",
                alpha=0.75,
                label="Force input",
            )

            self.configure_axes(
                self.ax1,
                r"$\boldsymbol{t} \: \boldsymbol{(s)}$",
                r"Deflection $ \boldsymbol{\Phi (t)}$ [ °]",
                "blue",
            )
            self.ax1_second_yaxis.set_ylabel(r"F [N]", color="red")

            # add to dict
            # blob
            self.blobs_dict[self.blob] = None
            # add figure and lines to figure_lines dict
            self.figure_lines_dict[self.fig_deflection] = [
                self.line_deflection,
                self.line_force,
            ]
            # add solutions for lines
            self.lines_sol_dict[self.line_deflection] = (self.t, None)
            self.lines_sol_dict[self.line_force] = (self.t, None)

            # remove stuff
            self.remove_stuff()
            # legend
            self.ax1.legend()

            plt.autoscale()
            plt.tight_layout()
            plt.show()

    def calc_and_plot_solutions(self):
        """Plot initial solutions"""

        sol_deflection, sol_force = self.animation_instance._calculate()
        omega_vec, omega_0, mag, mag_undamped, phase = (
            self.animation_instance.calc_bode_diagram()
        )

        # fill in the solutions in the line dict
        self.lines_sol_dict[self.line_deflection] = (
            self.t,
            sol_deflection,
        )
        self.lines_sol_dict[self.line_force] = (
            self.t,
            sol_force,
        )
        self.lines_sol_dict[self.line_bode_1_1] = (
            omega_vec / omega_0,
            mag,
        )
        self.lines_sol_dict[self.line_bode_1_2] = (
            omega_vec / omega_0,
            mag_undamped,
        )
        self.lines_sol_dict[self.line_bode_2] = (
            omega_vec / omega_0,
            phase,
        )

        # update plots
        self.update_plots()

        # update axes limits
        self.update_axes_limits(sol_deflection, mag)

        # fill in solutions for the blobs
        self.blobs_dict[self.blob] = sol_deflection
        self.update_blobs()

    def update_axes_limits(self, sol_deflection, mag):
        """Update axes limits based on current data"""
        self.ax1.set_ylim([min(sol_deflection) * 1.1, max(sol_deflection) * 1.1])

        self.ax_bode.set_ylim(0, max(mag) * 1.1)
        for ax in [self.ax1, self.ax_bode]:
            ax.relim()
            ax.autoscale_view()
