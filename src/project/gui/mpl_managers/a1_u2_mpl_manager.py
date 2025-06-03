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
            # on ax1_second_yaxis the force will be displayed
            # force is always inside range[-1, 1]
            self.ax1_second_yaxis.set_ylim([-1.1, 1.5])
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
            (self.line_force,) = self.ax1_second_yaxis.plot(
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
                r"$t \: (s)$",
                r"Deflection $ x (t)$ [ °]",
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

            # remove stuff
            self.remove_stuff()
            # legend
            ax1_line, ax1_label = self.ax1.get_legend_handles_labels()
            ax1_second_yaxis_line, ax1_second_yaxis_label = (
                self.ax1_second_yaxis.get_legend_handles_labels()
            )
            lines = ax1_line + ax1_second_yaxis_line
            labels = ax1_label + ax1_second_yaxis_label

            self.ax1_second_yaxis.legend(
                lines,
                labels,
                loc="upper right",
                framealpha=1.0,
            )

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
        self.update_axes_limits(sol_deflection, sol_force, mag)

        # fill in solutions for the blobs
        self.blobs_dict[self.blob] = sol_deflection
        self.update_blobs()

    def update_axes_limits(self, sol_deflection, sol_force, mag):
        """Update axes limits based on current data"""
        self.ax1.set_ylim([min(sol_deflection) * 1.1, max(sol_deflection) * 1.1])

        self.ax_bode.set_ylim(0, max(mag) * 1.1)

        for ax in [self.ax1, self.ax2_bode, self.ax_bode, self.ax1_second_yaxis]:
            ax.relim()
            ax.autoscale_view()
