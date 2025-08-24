from abc import abstractmethod
import matplotlib.pyplot as plt
from ipywidgets import widgets


class PlotManagerSuperclass:
    """
    Abstract base class for managing plots and visualizations.
    
    This class provides common functionality for creating, configuring, and updating
    matplotlib plots in an interactive environment. It serves as a foundation for
    specialized plot managers that implement specific visualization requirements.
    
    Attributes:
        figure_lines_dict (dict): Dictionary mapping figures to their associated plot lines
        lines_sol_dict (dict): Dictionary mapping lines to their data (time array, solution array)
        blobs_dict (dict): Dictionary mapping position indicators to their solution data
        animation_instance: Reference to the animation controller instance
        t (array): Time array used for plotting

        The following attributes are only used if the GUI 
        displays a Bode diagram: 

        output_bode: Widget output container for Bode plot
        fig_bode: Figure object for Bode plot
        ax_bode: Primary axes for Bode magnitude plot
        ax2_bode: Secondary axes for Bode phase plot
        line_bode_1_1: Line object for damped magnitude response
        line_bode_1_2: Line object for undamped magnitude response
        line_bode_2: Line object for phase response
    """

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
        """
        Set up and configure a Bode plot with magnitude and phase subplots.
        
        Creates a Bode plot consisting of two subplots: magnitude response
        (top) and phase response (bottom). Configures axes, creates plot lines
        for both damped and undamped responses, and applies consistent styling.
        
        The method also registers the figure and lines in the manager's dictionaries
        for future updates and applies UI cleanup to remove unnecessary elements.
        """
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

    @abstractmethod
    def calc_and_plot_solutions(self):
        """
        Calculate and plot the new deflection array after user input. 
        """
        pass
