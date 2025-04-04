import ipywidgets.widgets as widgets
import matplotlib.pyplot as plt
import numpy as np

from ..utils.constants import NUM_TIME_UNITS_AUFGABE_3, NUM_DATAPOINTS_3


class PlotManager:
    def __init__(self, animation_instance):
        self.animation_instance = animation_instance
        self.setup_plots()

    def setup_plots(self):
        """Initialize all matplotlib plots"""
        self.setup_steady_state_plot()
        self.setup_acceleration_plot()
        self.setup_bode_plot()
        self.set_plot_styles()
        self.plot_initial_solutions()

    def setup_steady_state_plot(self):
        """Set up the steady state plot"""
        self.output_steady = widgets.Output()
        with self.output_steady:
            self.fig_steady_state, self.ax_steady = plt.subplots(figsize=(5, 5))
            self.configure_axes(self.ax_steady, "t [s]", "z [m]", "blue")
            self.ax_steady_second_yaxis = self.ax_steady.twinx()
            self.ax_steady_second_yaxis.set_ylabel(r"u [m]", color="red")
            (self.blob_steady,) = self.ax_steady.plot([], [], "bo")
            (self.line_steady,) = self.ax_steady.plot(
                [], [], color="blue", linewidth=0.75, linestyle="-", label="Deflection"
            )
            (self.line_anregung_steady,) = self.ax_steady.plot(
                [],
                [],
                linewidth=0.65,
                linestyle="--",
                color="red",
                alpha=0.75,
                label="Force input",
            )
            self.fig_steady_state.canvas.toolbar_visible = False
            self.fig_steady_state.canvas.header_visible = False
            self.fig_steady_state.canvas.footer_visible = False
            self.ax_steady.legend()
            plt.tight_layout()
            plt.show()

    def setup_acceleration_plot(self):
        """Set up the acceleration plot"""
        self.output_acc = widgets.Output()
        with self.output_acc:
            self.fig_acceleration, self.ax_acc = plt.subplots(figsize=(5, 5))
            self.configure_axes(self.ax_acc, "t [s]", "z [m]", "blue")
            self.ax_acc_2 = self.ax_acc.twinx()
            self.ax_acc_2.set_ylabel(r"u [m]", color="red")
            (self.blob_acc,) = self.ax_acc.plot([], [], "bo")
            (self.line_acc,) = self.ax_acc.plot(
                [], [], color="blue", linewidth=0.75, linestyle="-", label="Deflection"
            )
            (self.line_anregung_acc,) = self.ax_acc.plot(
                [],
                [],
                linewidth=0.65,
                linestyle="--",
                color="red",
                alpha=0.75,
                label="Force input",
            )
            self.fig_acceleration.canvas.toolbar_visible = False
            self.fig_acceleration.canvas.header_visible = False
            self.fig_acceleration.canvas.footer_visible = False
            self.ax_acc.legend()
            plt.tight_layout()
            plt.show()

    def setup_bode_plot(self):
        """Set up the Bode plot"""
        self.output_bode = widgets.Output()
        with self.output_bode:
            self.fig_bode = plt.figure(figsize=(5, 5))
            self.ax_steady_bode = self.fig_bode.add_subplot(2, 1, 1)
            self.ax2_bode = self.fig_bode.add_subplot(2, 1, 2)

            self.configure_axes(self.ax_steady_bode, "", r"$\hat{F}/e$ [abs]")
            self.configure_axes(
                self.ax2_bode, r"$\Omega$ / $\omega$", r"$phase_{z}$ [deg]"
            )

            (self.line_bode_1_1,) = self.ax_steady_bode.plot(
                [], [], linewidth=0.75, linestyle="--", color="red", label="mag"
            )
            (self.line_bode_1_2,) = self.ax_steady_bode.plot(
                [],
                [],
                linestyle="--",
                color="blue",
                alpha=0.25,
                linewidth=0.75,
                label="mag undamped",
            )
            (self.line_bod_2,) = self.ax2_bode.plot(
                [], [], linestyle="--", linewidth=0.75, color="red"
            )
            self.fig_bode.canvas.toolbar_visible = False
            self.fig_bode.canvas.header_visible = False
            self.fig_bode.canvas.footer_visible = False
            self.ax_steady_bode.legend()
            plt.tight_layout()
            plt.show()

    def configure_axes(self, ax, xlabel="", ylabel="", color=None):
        """Common axis configuration"""
        ax.grid(True)
        ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel, color=color) if color else ax.set_ylabel(ylabel)
        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_visible(False)

    def set_plot_styles(self):
        """Set common plot styles"""
        plt.rcParams["font.family"] = "Arial"
        plt.rcParams["mathtext.fontset"] = "stix"
        plt.rcParams["mathtext.rm"] = "serif"
        plt.rcParams["mathtext.it"] = "serif:italic"
        plt.rcParams["mathtext.bf"] = "serif:bold"

    def plot_initial_solutions(self):
        """Plot initial solutions"""
        self.t = np.linspace(0, NUM_TIME_UNITS_AUFGABE_3, NUM_DATAPOINTS_3)

        # Get initial solutions
        sol_acc, sol_acc_force, sol_steady, sol_steady_force = (
            self.animation_instance._calculate()
        )
        omega_vec, omega_0, mag, mag_undamped, phase = (
            self.animation_instance.calc_bode_diagram()
        )

        # Update plot data
        self.update_plots(
            sol_acc,
            sol_acc_force,
            sol_steady,
            sol_steady_force,
            omega_vec,
            omega_0,
            mag,
            mag_undamped,
            phase,
        )

    def update_plots(
        self,
        sol_acc,
        sol_acc_force,
        sol_steady,
        sol_steady_force,
        omega_vec,
        omega_0,
        mag,
        mag_undamped,
        phase,
    ):
        """Update all plots with new data"""
        # Update steady state plot
        self.line_steady.set_data(self.t, sol_steady)
        self.line_anregung_steady.set_data(self.t, sol_steady_force)

        # Update acceleration plot
        self.line_acc.set_data(self.t, sol_acc)
        self.line_anregung_acc.set_data(self.t, sol_acc_force)

        # Update Bode plot
        self.line_bode_1_1.set_data(omega_vec / omega_0, mag)
        self.line_bode_1_2.set_data(omega_vec / omega_0, mag_undamped)
        self.line_bod_2.set_data(omega_vec / omega_0, phase)

        # Update axes limits
        self.update_axes_limits(sol_acc, sol_steady, mag)

    def update_axes_limits(self, sol_acc, sol_steady, mag):
        """Update axes limits based on current data"""
        self.ax_acc.set_ylim([min(sol_acc) * 1.1, max(sol_acc) * 1.1])
        self.ax_steady.set_ylim([min(sol_steady) * 1.1, max(sol_steady) * 1.1])
        self.ax_steady_bode.set_ylim(0, max(mag) * 1.1)
        for ax in [self.ax_acc, self.ax_steady, self.ax_steady_bode]:
            ax.relim()
            ax.autoscale_view()

    def update_blobs(self, frame):
        """Update the position indicators on the plots"""
        x = [self.t[frame]]
        y_acc = [self.animation_instance.sol_acc[frame]]
        y_steady = [self.animation_instance.sol_steady[frame]]
        self.blob_acc.set_data(x, y_acc)
        self.blob_steady.set_data(x, y_steady)

        self.fig_steady_state.canvas.draw_idle()
        self.fig_acceleration.canvas.draw_idle()
