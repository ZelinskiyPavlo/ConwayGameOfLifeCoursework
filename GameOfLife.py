import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Button
import tkinter as tk

# setting up the values for the grid
ON = 255
OFF = 0
vals = [ON, OFF]


class ConwayGameOfLifeCore:
    def __init__(self, controller):
        self.controller = controller
        frame_ref = self.controller.core_frame_ref()

        self.fig, self.ax = plt.subplots()
        canvas = FigureCanvasTkAgg(self.fig, master=frame_ref)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # getting values from controller dictionary
        self.grid_size = self.get_grid_size()
        self.random_fill = self.controller.configuration["random_fill"].get()
        self.grid = self.create_grid(self.grid_size)

        self.add_glider(self.grid, self.grid_size)
        self.add_oscillator(self.grid, self.grid_size)

        self.update_interval = self.controller.configuration[
            "update_interval"].get()
        self.show_generation = self.controller.configuration[
            "show_generation"].get()
        # self.color_dead = self.get_color_dead()
        # self.color_alive = self.get_color_alive()

        # setting values for matPlot needs
        self.start_value = 0
        self.generation_text = None
        self.button_stop = None
        self.button_start = None
        self.button_home = None

        self.img = self.ax.imshow(self.grid, interpolation='nearest')
        plt.axis("off")
        self.init_matplot_gui()
        self.anim = animation.FuncAnimation(self.fig, self.update,
                                            fargs=(
                                                self.img, self.grid,
                                                self.grid_size,),
                                            frames=10,
                                            interval=self.update_interval,
                                            save_count=50)

    def update(self, frame_num, img, grid, grid_size):
        """Updates grid, show number of generation, using in animation func """
        new_grid = grid.copy()

        if self.show_generation:
            self.generation_text.set_text(
                "Генерація:{}".format(self.start_value))
            self.start_value += 1

        for i in range(grid_size):
            for j in range(grid_size):

                total = int((grid[i, (j - 1) % grid_size] + grid[
                    i, (j + 1) % grid_size] +
                             grid[(i - 1) % grid_size, j] + grid[
                                 (i + 1) % grid_size, j] +
                             grid[(i - 1) % grid_size, (j - 1) % grid_size] +
                             grid[
                                 (i - 1) % grid_size, (j + 1) % grid_size] +
                             grid[(i + 1) % grid_size, (j - 1) % grid_size] +
                             grid[
                                 (i + 1) % grid_size, (
                                         j + 1) % grid_size]) / 255)

                if grid[i, j] == ON:
                    if (total < 2) or (total > 3):
                        new_grid[i, j] = OFF
                else:
                    if total == 3:
                        new_grid[i, j] = ON

        # update data
        img.set_data(new_grid)
        grid[:] = new_grid[:]
        return img,

    def create_grid(self, size):
        """Generate grid array depending on bool value from dict"""
        if self.random_fill:
            return np.random.choice(vals, size * size, p=[0.2, 0.8]). \
                reshape(size, size)
        else:
            grid = np.zeros(size * size).reshape(size, size)
            center = int(size / 2)
            grid[center, center] = 255
            grid[center + 1, center] = 255
            grid[center + 2, center] = 255
            grid[center, center - 1] = 255
            grid[center - 1, center - 1] = 255
            grid[center - 2, center - 1] = 255
            return grid

    def init_matplot_gui(self):
        """Generate text and 3 button widgets"""
        self.generation_text = self.ax.text(-0.7, -1.1, "")

        button_stop_axes = plt.axes([0.78, 0.01, 0.1, 0.075])
        self.button_stop = Button(button_stop_axes, "Стоп",
                                  color="skyblue",
                                  hovercolor='0.975')
        self.button_stop.on_clicked(
            lambda *args: self.anim.event_source.stop())
        button_start_axes = plt.axes([0.89, 0.01, 0.1, 0.075])
        self.button_start = Button(button_start_axes, "Старт",
                                   color="skyblue",
                                   hovercolor='0.975')
        self.button_start.on_clicked(
            lambda *args: self.anim.event_source.start())
        button_home_axes = plt.axes([0.01, 0.01, 0.15, 0.075])
        self.button_home = Button(button_home_axes, "На початок",
                                  color="skyblue",
                                  hovercolor='0.975')
        self.button_home.on_clicked(
            lambda *args: self.controller.restart_game())

    def add_glider(self, grid, size):
        """adds a glider in top left and bottom right side of grid"""
        if self.controller.configuration["glider"].get() == 1:
            i = 1
            glider = np.array([[0, 0, 255],
                               [255, 0, 255],
                               [0, 255, 255]])
            grid[i:i + 3, i:i + 3] = glider
            i = size - 4
            glider = np.array([[255, 255, 0],
                               [255, 0, 255],
                               [255, 0, 0]])
            grid[i:i + 3, i:i + 3] = glider

    def add_oscillator(self, grid, size):
        """adds pentadecathlon oscillator in bottom section"""
        if self.controller.configuration["oscillator"].get() == 1:
            x = size - 7
            y = int(size / 2) - int(size / 10)
            gun = np.array([[0, 0, 255, 0, 0, 0, 0, 255, 0, 0],
                            [255, 255, 0, 255, 255, 255, 255, 0, 255, 255],
                            [0, 0, 255, 0, 0, 0, 0, 255, 0, 0]])
            grid[x:x + 3, y:y + 10] = gun

    # get dict values (if not specified set default values)
    def get_grid_size(self):
        if self.controller.configuration["grid_size"].get() != 0:
            return self.controller.configuration["grid_size"].get()
        else:
            return 50

    def get_color_dead(self):
        if self.controller.configuration["color_dead"].get() != "":
            return self.controller.configuration["color_dead"].get()
        else:
            return "black"

    def get_color_alive(self):
        if self.controller.configuration["color_alive"].get() != "":
            return self.controller.configuration["color_alive"].get()
        else:
            return "white"
