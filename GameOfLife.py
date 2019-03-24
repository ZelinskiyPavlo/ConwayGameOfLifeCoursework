import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Button, TextBox

# setting up the values for the grid
ON = 255
OFF = 0
vals = [ON, OFF]


# main() function
# def main():
#     # Command line args are in sys.argv[1], sys.argv[2] ..
#     # sys.argv[0] is the script name itself and can be ignored
#     # parse arguments
#
#     root = Tk.Tk()
#
#     parser = argparse.ArgumentParser(
#         description="Runs Conway's Game of Life simulation.")
#
#     # add arguments
#     parser.add_argument('--grid-size', dest='N', required=False)
#     parser.add_argument('--mov-file', dest='movfile', required=False)
#     parser.add_argument('--interval', dest='interval', required=False)
#     parser.add_argument('--glider', action='store_true', required=False)
#     parser.add_argument('--gosper', action='store_true', required=False)
#     args = parser.parse_args()
#
#     # set grid size
#     N = 100
#     if args.N and int(args.N) > 8:
#         N = int(args.N)
#
#     # set animation update interval
#     updateInterval = 1200
#     if args.interval:
#         updateInterval = int(args.interval)
#
#     # declare grid
#     grid = np.array([])
#
#     # check if "glider" demo flag is specified
#     if args.glider:
#         grid = np.zeros(N * N).reshape(N, N)
#         addGlider(1, 1, grid)
#     elif args.gosper:
#         grid = np.zeros(N * N).reshape(N, N)
#         addGosperGliderGun(10, 10, grid)
#
#     else:  # populate grid with random on/off -
#         # more off than on
#         grid = randomGrid(N)
#
#     # set up animation
#
#     fig, ax = plt.subplots()
#
#     canvas = FigureCanvasTkAgg(fig, master=root)
#     canvas.get_tk_widget().grid(column=0, row=1)
#
#     img = ax.imshow(grid, interpolation='nearest')
#     ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,),
#                                   frames=10,
#                                   interval=updateInterval,
#                                   save_count=50)
#     # plt.show()
#     Tk.mainloop()


class ConwayGameOfLifeCore:
    def __init__(self, controller):
        self.controller = controller
        frame_ref = self.controller.core_frame_ref()

        self.fig, self.ax = plt.subplots()
        canvas = FigureCanvasTkAgg(self.fig, master=frame_ref)
        canvas.get_tk_widget().grid(column=0, row=1)

        # setting values
        self.grid_size = 10
        # self.grid_size = self.get_grid_size()
        self.grid = self.normal_grid(self.grid_size)
        # self.grid = self.random_grid(self.grid_size)
        # self.show_generation = 1
        self.show_generation = self.controller.configuration[
            "show_generation"].get()
        # textbox_axes = plt.axes([])

        # self.generation_text = self.ax.text(-3.0, -1.1, "Generation:0")
        self.generation_text = self.ax.text(-3.0, -1.1, "")
        self.start_value = 0
        self.img = self.ax.imshow(self.grid, interpolation='nearest')
        self.anim = animation.FuncAnimation(self.fig, self.update,
                                            fargs=(
                                                self.img, self.grid,
                                                self.grid_size,),
                                            frames=10,
                                            interval=1200,
                                            save_count=50)

    def update(self, frame_num, img, grid, grid_size):
        newGrid = grid.copy()

        if self.show_generation:
            self.generation_text.set_text(
                "Generation:{}".format(self.start_value))
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
                        newGrid[i, j] = OFF
                else:
                    if total == 3:
                        newGrid[i, j] = ON

                    # update data
        img.set_data(newGrid)
        grid[:] = newGrid[:]
        return img,

    # MERGE TWO METHODS
    def normal_grid(self, size):
        grid = np.zeros(size * size).reshape(size, size)
        center = int(size / 5) + 2
        grid[center, center] = 255
        grid[center + 1, center] = 255
        grid[center + 2, center] = 255
        grid[center, center - 1] = 255
        grid[center - 1, center - 1] = 255
        grid[center - 2, center - 1] = 255
        return grid

    def random_grid(self, size):
        """returns a grid of NxN random values"""
        return np.random.choice(vals, size * size, p=[0.2, 0.8]).reshape(size,
                                                                         size)

    def add_glider(self, i, j, grid):
        """adds a glider with top left cell at (i, j)"""
        pass
        # glider = np.array([[0, 0, 255],
        #                    [255, 0, 255],
        #                    [0, 255, 255]])
        # grid[i:i + 3, j:j + 3] = glider

    def add_gosper_glider_gun(self, i, j, grid):
        """adds a Gosper Glider Gun with top left
        cell at (i, j)"""
        pass
        # gun = np.zeros(11 * 38).reshape(11, 38)
        #
        # gun[5][1] = gun[5][2] = 255
        # gun[6][1] = gun[6][2] = 255
        #
        # gun[3][13] = gun[3][14] = 255
        # gun[4][12] = gun[4][16] = 255
        # gun[5][11] = gun[5][17] = 255
        # gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
        # gun[7][11] = gun[7][17] = 255
        # gun[8][12] = gun[8][16] = 255
        # gun[9][13] = gun[9][14] = 255
        #
        # gun[1][25] = 255
        # gun[2][23] = gun[2][25] = 255
        # gun[3][21] = gun[3][22] = 255
        # gun[4][21] = gun[4][22] = 255
        # gun[5][21] = gun[5][22] = 255
        # gun[6][23] = gun[6][25] = 255
        # gun[7][25] = 255
        #
        # gun[3][35] = gun[3][36] = 255
        # gun[4][35] = gun[4][36] = 255
        #
        # grid[i:i + 11, j:j + 38] = gun

    # get dict values (if not specified set default values)
    def get_grid_size(self):
        if self.controller.configuration["grid_size"].get() != 0:
            return self.controller.configuration["grid_size"].get()
        else:
            return 100

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

# All default values
# 0
# 0
# 1200
# 0
# 0
#   color_dead
#   color_alive
# 0
