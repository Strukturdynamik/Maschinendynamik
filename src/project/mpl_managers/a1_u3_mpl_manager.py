import ipywidgets.widgets as widgets
import matplotlib.pyplot as plt

from ..utils.constants import A1_U3_T
from .mpl_manager_superclass import PlotManagerSuperclass

"""
See Superclass for additional documentation.
"""

class PlotManagerA1U3(PlotManagerSuperclass):
    def __init__(self, animation_instance):
        self.animation_instance = animation_instance
        self.blobs_dict = {}  # keys: blob, values: solutions for the blobs
        self.figure_lines_dict = {}  # keys: figure, values: list[lines for the figure]
        self.lines_sol_dict = {}  # key: lines, value: tuple(t arr, solution arr)
        self.axes = []  # list of axes
        self.t = A1_U3_T
        self.setup_plots()

    def setup_plots(self):
        """Initialize all matplotlib plots"""
        self.setup_deflection_plot()
        self.setup_bode_plot()
        self.setup_ground_force()
        self.set_plot_styles()
        self.calc_and_plot_solutions()

    def setup_deflection_plot(self):
        """
        Set up and configure the deflection plot with dual y-axes.
        
        Creates a figure with two y-axes:
        - Primary y-axis (left): Shows system deflection in degrees with blue styling
        - Secondary y-axis (right): Shows force input in Newtons with red styling
        
        The plot includes:
        - A position indicator blob (blue circle) that shows current time point
        - A solid blue line for deflection data
        - A dashed red line for force input data
        - Pre-configured axis limits for force display (-1.1 to 1.5)
        - Combined legend showing both deflection and force labels
        - Clean UI with toolbar, header, and footer removed
        
        The method registers all visual elements in the manager's dictionaries
        for future updates and applies consistent styling and layout.
        
        Visual Elements Created:
        - self.output_deflection: Widget output container for the plot
        - self.fig_deflection: Figure object for the deflection plot
        - self.ax1: Primary axes for deflection data (left y-axis)
        - self.ax1_second_yaxis: Secondary axes for force data (right y-axis)
        - self.blob: Position indicator marker object
        - self.line_deflection: Line object for deflection response
        - self.line_force: Line object for force input
        
        Registration:
        - Adds blob to blobs_dict for position tracking
        - Adds figure and lines to figure_lines_dict for update management
        """
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

        # def setup_ground_force(self):
        #     """Set up the Bode Ground Force plot"""
        #     self.output_ground_force = widgets.Output()
        #     with self.output_ground_force:
        #         self.fig_ground_force, self.ax2_ground_force = plt.figure(figsize=(5, 5))
        #         # self.ax_ground_force = self.fig_ground_force.add_subplot(2, 1, 1)
        #         # self.ax2_ground_force = self.fig_ground_force.add_subplot(2, 1, 2)
        #         # self.configure_axes(self.ax_ground_force, "", r"$\hat{F}_{B}/e$ [abs]")
        #         self.configure_axes(
        #             self.ax2_ground_force,
        #             r"$\Omega$ / $\omega_{0}$",
        #             r"$\phi_{\hat{F}_{B}}$ [deg]",
        #         )

        #         # (self.line_ground_force_1,) = self.ax_ground_force.semilogx(
        #         #     [], [], linestyle="-", linewidth=0.75, color="green"
        #         # )
        #         (self.line_ground_force_2,) = self.ax2_ground_force.semilogx(
        #             [], [], linewidth=0.75, linestyle="-", color="red"
        #         )

        #         # add figure and lines to figure_lines dict
        #         self.figure_lines_dict[self.fig_ground_force] = [
        #             self.line_ground_force_2,
        #             # self.line_ground_force_1,
        #         ]

        #         # remove stuff
        #         self.remove_stuff()

        #         self.ax_ground_force.legend()
        #         plt.tight_layout()
        #         plt.show()

    def setup_ground_force(self):
        """
        Set up and configure the ground force transmission Bode plot.
        
        Creates a semilogarithmic plot showing the magnitude of ground force transmission
        (F̂_B/e) as a function of frequency. This plot visualizes how much force is 
        transmitted to the ground across different excitation frequencies, which is
        particularly important for vibration isolation analysis.
        
        The plot features:
        - Logarithmic x-axis for frequency ratio (Ω/ω₀)
        - Linear y-axis for normalized ground force magnitude [abs]
        - Green solid line for ground force transmission data
        - Clean UI with toolbar, header, and footer removed
        - Pre-configured axes labels using LaTeX notation for mathematical symbols
        
        Visual Elements Created:
        - self.output_ground_force: Widget output container for the plot
        - self.fig_ground_force: Figure object for the ground force plot
        - self.ax_ground_force: Axes object with semilog scaling
        - self.line_ground_force_1: Line object for ground force magnitude response
        
        Registration:
        - Adds figure and line to figure_lines_dict for update management
        
        Note: This plot uses semilogx (logarithmic x-axis, linear y-axis) which is
        typical for Bode magnitude plots to properly display the frequency response
        across multiple decades of frequency ratios.
        """
        self.output_ground_force = widgets.Output()
        with self.output_ground_force:
            # Correct figure and axes creation
            self.fig_ground_force, self.ax_ground_force = plt.subplots(figsize=(5, 5))

            self.configure_axes(self.ax_ground_force, "", r"$\hat{F}_{B}/e$ [abs]")

            (self.line_ground_force_1,) = self.ax_ground_force.semilogx(
                [], [], linestyle="-", linewidth=0.75, color="green"
            )

            # add figure and lines to figure_lines dict
            self.figure_lines_dict[self.fig_ground_force] = [
                self.line_ground_force_1,
            ]

            self.remove_stuff()
            self.ax_ground_force.legend()
            plt.tight_layout()
            plt.show()

    def calc_and_plot_solutions(self):
        (
            sol_deflection,
            sol_force,
        ) = self.animation_instance._calculate()

        omega_vec, omega_0, mag, mag_undamped, phase = (
            self.animation_instance.calc_bode_diagram()
        )

        (
            omega_vec_ground_force,
            omega_ground_force,
            mag_ground_force,
            phase_ground_force,
        ) = self.animation_instance.calc_ground_force()

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

        x_ground_force = omega_vec_ground_force / omega_ground_force
        self.lines_sol_dict[self.line_ground_force_1] = (
            x_ground_force,
            mag_ground_force,
        )
        # self.lines_sol_dict[self.line_ground_force_2] = (
        #     x_ground_force,
        #     phase_ground_force,
        # )

        # update plots
        self.update_plots()

        # update axes limits
        self.update_axes_limits(
            sol_deflection,
            mag,
            mag_ground_force,
        )

        # fill in solutions for the blobs
        self.blobs_dict[self.blob] = sol_deflection
        self.update_blobs()

    def update_axes_limits(
        self,
        sol_deflection,
        mag,
        mag_ground_force,
    ):
        min_defl = min(sol_deflection)
        max_defl = max(sol_deflection)
        # min_phase_ground_force = min(phase_ground_force)
        # max_phase_ground_force = max(phase_ground_force)
        max_mag_ground_force = max(mag_ground_force)
        max_mag = max(mag)

        self.ax1.set_ylim([min_defl * 1.1, max_defl * 1.1])
        self.ax_bode.set_ylim(0.001, max_mag * 1.1)

        self.ax_ground_force.set_autoscaley_on(False)
        self.ax_ground_force.set_ylim(0, max_mag_ground_force * 1.1)
        self.ax_ground_force.set_xlim(10**-1, 10**3)

        # Update other axes
        for ax in [
            self.ax1,
            self.ax2_bode,
            self.ax_bode,
            self.ax1_second_yaxis,
        ]:
            ax.relim()
            ax.autoscale_view()
