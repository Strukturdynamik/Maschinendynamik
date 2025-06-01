import ipywidgets.widgets as widgets
import matplotlib.pyplot as plt
import numpy as np

from ...utils.constants import A4_U1_T
from .mpl_manager_superclass import PlotManagerSuperclass


class PlotManagerA4U1(PlotManagerSuperclass):
    def __init__(self, animation_instance):
        self.animation_instance = animation_instance
        self.blobs_dict = {}  # keys: blob, values: solutions for the blobs
        self.figure_lines_dict = {}  # keys: figure, values: list[lines for the figure]
        self.lines_sol_dict = {}  # key: lines, value: tuple(t arr, solution arr)
        self.axes = []  # list of axes
        self.t = A4_U1_T
        self.setup_plots()

    def setup_plots(self):
        """Initialize all matplotlib plots"""
        self.setup_deflection_plot()
        self.set_plot_styles()
        self.calc_and_plot_solutions()

    def setup_deflection_plot(self):
        self.output_deflection = widgets.Output()
        with self.output_deflection:
            self.fig_deflection, self.ax1 = plt.subplots(figsize=(5, 5))
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

            self.configure_axes(
                self.ax1,
                r"$t \: (s)$",
                r"Deflection $\Phi (t)$ [ °]",
                "blue",
            )

            # add to dict
            # blob
            self.blobs_dict[self.blob] = None
            # add figure and lines to figure_lines dict
            self.figure_lines_dict[self.fig_deflection] = [self.line_deflection]

            # remove stuff
            self.remove_stuff()
            # legend
            self.ax1.legend()

            plt.autoscale()
            plt.tight_layout()
            plt.show()

    def calc_and_plot_solutions(self):
        """Plot initial solutions"""

        sol_deflection = self.animation_instance._calculate()

        # fill in the solutions in the line dict
        self.lines_sol_dict[self.line_deflection] = (self.t, sol_deflection)

        # update plots
        self.update_plots()

        # update axes limits
        self.update_axes_limits(sol_deflection)

        # fill in solutions for the blobs
        self.blobs_dict[self.blob] = sol_deflection
        self.update_blobs()

    def update_axes_limits(self, sol_deflection):
        """Update axes limits based on current data"""
        self.ax1.set_ylim([min(sol_deflection) * 1.1, max(sol_deflection) * 1.1])
        self.ax1.relim()
        self.ax1.autoscale_view()
