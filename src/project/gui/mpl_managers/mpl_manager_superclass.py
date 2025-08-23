from abc import abstractmethod
import matplotlib.pyplot as plt
from ipywidgets import widgets


class PlotManagerSuperclass:

    def __init__(self):
        pass

    def configure_axes(self, ax, xlabel="", ylabel="", color=None):
        """Common axis configuration"""
        ax.grid(True)
        ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel, color=color) if color else ax.set_ylabel(ylabel)
        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_visible(False)
        pass

    def remove_stuff(self):
        """Remove unnecessary stuff from the plot"""
        for fig, _ in self.figure_lines_dict.items():
            fig.canvas.toolbar_visible = False
            fig.canvas.header_visible = False
            fig.canvas.footer_visible = False

    def set_plot_styles(self):
        """Set common plot styles"""
        plt.rcParams["font.family"] = "Arial"
        plt.rcParams["mathtext.fontset"] = "stix"
        plt.rcParams["mathtext.rm"] = "serif"
        plt.rcParams["mathtext.it"] = "serif:italic"
        plt.rcParams["mathtext.bf"] = "serif:bold"

    def update_blobs(self):
        """Update the position indicators on the plots"""
        # get the time for the current frame
        frame = self.animation_instance.frame
        x = [self.t[frame]]

        # set the data for each blob
        for blob, sol in self.blobs_dict.items():
            y = [sol[frame]]
            blob.set_data(x, y)

        # redraw the canvas
        for fig, _ in self.figure_lines_dict.items():
            fig.canvas.draw_idle()

    def update_plots(self):
        """Update all plots with new data"""
        for line, (t_arr, sol_arr) in self.lines_sol_dict.items():
            line.set_xdata(t_arr)
            line.set_ydata(sol_arr)

        for fig, _ in self.figure_lines_dict.items():
            fig.canvas.draw_idle()

    def setup_bode_plot(self):
        """Set up the Bode plot"""
        self.output_bode = widgets.Output()
        with self.output_bode:
            self.fig_bode = plt.figure(figsize=(5, 5))
            self.ax_bode = self.fig_bode.add_subplot(2, 1, 1)
            self.ax2_bode = self.fig_bode.add_subplot(2, 1, 2)
            self.configure_axes(self.ax_bode, "", r"$\hat{F}/e$ [abs]")
            self.configure_axes(
                self.ax2_bode, r"$\Omega$ / $\omega$", r"$phase_{z}$ [deg]"
            )

            (self.line_bode_1_1,) = self.ax_bode.plot(
                [], [], linewidth=0.75, linestyle="--", color="red", label="mag"
            )
            (self.line_bode_1_2,) = self.ax_bode.plot(
                [],
                [],
                linestyle="--",
                color="blue",
                alpha=0.25,
                linewidth=0.75,
                label="mag undamped",
            )
            (self.line_bode_2,) = self.ax2_bode.plot(
                [], [], linestyle="--", linewidth=0.75, color="red"
            )

            # add figure and lines to figure_lines dict
            self.figure_lines_dict[self.fig_bode] = [
                self.line_bode_1_1,
                self.line_bode_1_2,
                self.line_bode_2,
            ]

            # remove stuff
            self.remove_stuff()

            self.ax_bode.legend()
            plt.tight_layout()
            plt.show()

    @abstractmethod
    def setup_plots(self):
        """
        Set up the plots. Call set up method for each graph in the gui.
        """
        pass

    @abstractmethod
    def update_axes_limits(self):
        """
        Update the axes for each graph in the gui.
        """
        pass
