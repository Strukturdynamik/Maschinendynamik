import ipywidgets.widgets as widgets
import matplotlib.pyplot as plt
import numpy as np

from ..utils.constants import A1_U5_T
from .mpl_manager_superclass import PlotManagerSuperclass


class PlotManagerA1U5(PlotManagerSuperclass):
    def __init__(self, animation_instance):
        self.animation_instance = animation_instance
        self.blobs_dict = {}
        self.figure_lines_dict = {}
        self.lines_sol_dict = {}
        self.axes = []
        self.t = A1_U5_T
        self.setup_plots()

    def setup_plots(self):
        """Initialize all matplotlib plots"""
        self.setup_s_t_plot()
        self.setup_s_phi_plot()
        self.set_plot_styles()
        self.calc_and_plot_solutions()

    def setup_s_t_plot(self):
        self.output_s_t = widgets.Output()
        with self.output_s_t:
            self.fig_s_t, self.ax_s = plt.subplots(figsize=(5, 5))

            # blob
            (self.blob_s,) = self.ax_s.plot([], [], "bo")

            # lines
            (self.line_nonlinear_s,) = self.ax_s.plot(
                [],
                [],
                color="blue",
                linewidth=0.75,
                linestyle="-",
                label="Nonlinear",
            )
            (self.line_linear_s,) = self.ax_s.plot(
                [],
                [],
                linewidth=0.65,
                linestyle="--",
                color="red",
                alpha=0.75,
                label="Linear",
            )

            self.configure_axes(
                self.ax_s,
                r"$t \: (s)$",
                r"$s[m]$",
            )

            self.figure_lines_dict[self.fig_s_t] = [
                self.line_nonlinear_s,
                self.line_linear_s,
            ]

            self.remove_stuff()
            plt.autoscale()
            plt.tight_layout()
            plt.show()

    def setup_s_phi_plot(self):
        self.output_s_phi = widgets.Output()
        with self.output_s_phi:
            self.fig_s_phi, self.ax_phi = plt.subplots(figsize=(5, 5))

            # blob
            (self.blob_phi,) = self.ax_phi.plot([], [], "bo")

            (self.line_nonlinear_phi,) = self.ax_phi.plot(
                [],
                [],
                color="blue",
                linewidth=0.75,
                linestyle="-",
                label="Nonlinear",
            )
            (self.line_linear_phi,) = self.ax_phi.plot(
                [],
                [],
                linewidth=0.65,
                linestyle="--",
                color="red",
                alpha=0.75,
                label="Linear",
            )

            self.configure_axes(
                self.ax_phi,
                r"$t \: (s)$",
                r"$\varphi [°]$",
            )

            self.figure_lines_dict[self.fig_s_phi] = [
                self.line_nonlinear_phi,
                self.line_linear_phi,
            ]

            self.remove_stuff()
            plt.autoscale()
            plt.tight_layout()
            plt.show()

    def calc_and_plot_solutions(self):
        """Calculate and plot initial solutions for all visualizations."""
        s_nl, s_l, phi_nl, phi_l = self.animation_instance._calculate()

        self.lines_sol_dict[self.line_nonlinear_s] = (self.t, s_nl)
        self.lines_sol_dict[self.line_linear_s] = (self.t, s_l)
        self.lines_sol_dict[self.line_nonlinear_phi] = (self.t, phi_nl)
        self.lines_sol_dict[self.line_linear_phi] = (self.t, phi_l)

        self.blobs_dict[self.blob_s] = s_nl
        self.blobs_dict[self.blob_phi] = phi_nl

        self.update_plots()
        self.update_axes_limits(s_nl, s_l, phi_nl, phi_l)
        self.update_blobs()

    def update_axes_limits(self, s_nl, s_l, phi_nl, phi_l):
        """Update axes limits based on current data ranges."""

        # s max and min
        s_max = max([max(s_nl), max(s_l)])
        s_min = min([min(s_nl), min(s_l)])

        # phi max and min
        phi_max = max([max(phi_nl), max(phi_l)])
        phi_min = min([min(phi_nl), min(phi_l)])

        # pad limits
        # s
        if s_max > 0:
            s_max *= 1.1
        else:
            s_max = s_max + abs(s_max) * 1.1

        if s_min > 0:
            s_min = s_min - s_min * 0.1
        else:
            s_min = s_min - abs(s_min) * 0.1

        # phi
        if phi_max > 0:
            phi_max *= 1.1
        else:
            phi_max = phi_max + abs(phi_max) * 1.1

        if phi_min > 0:
            phi_min = phi_min - phi_min * 0.1
        else:
            phi_min = phi_min - abs(phi_min) * 0.1

        self.ax_s.set_ylim([s_min, s_max])
        self.ax_phi.set_ylim([phi_min, phi_max])

        for ax in [self.ax_s, self.ax_phi]:
            ax.relim()
            ax.autoscale_view()
