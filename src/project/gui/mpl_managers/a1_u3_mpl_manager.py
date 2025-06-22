import ipywidgets.widgets as widgets
import matplotlib.pyplot as plt
import numpy as np

from ...utils.constants import A1_U3_T
from .mpl_manager_superclass import PlotManagerSuperclass


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

    def setup_ground_force(self):
        """Set up the Bode Ground Force plot"""
        self.output_ground_force = widgets.Output()
        with self.output_ground_force:
            self.fig_ground_force = plt.figure(figsize=(5, 5))
            self.ax_ground_force = self.fig_ground_force.add_subplot(2, 1, 1)
            self.ax2_ground_force = self.fig_ground_force.add_subplot(2, 1, 2)
            self.configure_axes(self.ax_ground_force, "", r"$\hat{F}_{B}/e$ [abs]")
            self.configure_axes(
                self.ax2_ground_force,
                r"$\Omega$ / $\omega_{0}$",
                r"$\phi_{\hat{F}_{B}}$ [deg]",
            )

            (self.line_ground_force_1,) = self.ax_ground_force.semilogx(
                [], [], linewidth=0.75, linestyle="-", color="red"
            )
            (self.line_ground_force_2,) = self.ax2_ground_force.semilogx(
                [], [], linestyle="-", linewidth=0.75, color="red"
            )

            # add figure and lines to figure_lines dict
            self.figure_lines_dict[self.fig_ground_force] = [
                self.line_ground_force_1,
                self.line_ground_force_2,
            ]

            # remove stuff
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

        self.lines_sol_dict[self.line_ground_force_1] = (
            omega_vec_ground_force / omega_ground_force,
            mag_ground_force,
        )

        print(f"{(omega_vec_ground_force / omega_ground_force)[:5]=}")
        print()
        print(f"{phase_ground_force[:5]=}")
        self.lines_sol_dict[self.line_ground_force_2] = (
            omega_vec_ground_force / omega_ground_force,
            phase_ground_force,
        )

        # update plots
        self.update_plots()

        # update axes limits
        self.update_axes_limits(
            sol_deflection, mag, mag_ground_force, phase_ground_force
        )

        # fill in solutions for the blobs
        self.blobs_dict[self.blob] = sol_deflection
        self.update_blobs()

    def update_axes_limits(
        self, sol_deflection, mag, mag_ground_force, phase_ground_force
    ):
        """Update axes limits based on current data"""
        self.ax1.set_ylim([min(sol_deflection) * 1.1, max(sol_deflection) * 1.1])

        self.ax_bode.set_ylim(0, max(mag) * 1.1)

        self.ax_ground_force.set_ylim(0, max(mag_ground_force) * 1.1)
        self.ax2_ground_force.set_ylim(
            min(phase_ground_force) * 1.1, max(phase_ground_force) * 1.1
        )

        for ax in [
            self.ax1,
            self.ax2_bode,
            self.ax_bode,
            self.ax1_second_yaxis,
            self.ax_ground_force,
            self.ax2_ground_force,
        ]:
            ax.relim()
            ax.autoscale_view()
