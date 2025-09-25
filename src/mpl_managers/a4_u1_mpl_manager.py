import ipywidgets.widgets as widgets
import matplotlib.pyplot as plt

from ..utils.constants import A4_U1_T
from .mpl_manager_superclass import PlotManagerSuperclass

"""
See Superclass for additional documentation.
"""


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
        """
        Set up and configure the deflection plot for angular displacement visualization.

        Creates a single-axis plot showing the angular deflection (Φ) over time.
        This plot is designed to visualize rotational or angular motion responses
        in degrees as a function of time in seconds.

        The plot includes:
        - A position indicator blob (blue circle) that shows the current time point
        - A solid blue line for deflection data with specified line properties
        - Properly formatted axes labels using LaTeX notation for mathematical symbols
        - Automatic scaling to accommodate varying data ranges
        - Clean UI with toolbar, header, and footer removed
        - Legend identifying the deflection line

        Visual Elements Created:
        - self.output_deflection: Widget output container for the plot
        - self.fig_deflection: Figure object for the deflection plot (5x5 inches)
        - self.ax1: Primary axes for deflection data
        - self.blob: Position indicator marker object (blue circle)
        - self.line_deflection: Line object for deflection response

        Styling Details:
        - Line color: Blue
        - Line width: 0.75 points
        - Line style: Solid (-)
        - Blob style: Blue circles ("bo")
        - X-axis label: Time in seconds (t) with LaTeX formatting
        - Y-axis label: Angular deflection in degrees (Φ) with LaTeX formatting

        Registration:
        - Adds blob to blobs_dict for position tracking (initialized to None)
        - Adds figure and line to figure_lines_dict for update management

        The plot uses autoscaling to dynamically adjust to the data range and
        tight_layout to optimize spacing between plot elements.
        """
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
