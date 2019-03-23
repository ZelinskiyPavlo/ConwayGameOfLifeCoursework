import tkinter as tk
from tkinter import ttk
import GameOfLife
import matplotlib
from random import randint, randrange, choice
import matplotlib.animation as animation

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2Tk
from matplotlib.figure import Figure

LARGE_FONT = ("Verdana", 12)
REGULAR_FONT = ("Verdana", 10)
HINT_FONT = ("Verdana", 7)


# ClassObject = ConwayGameOfLifeGui()
class ConwayGameOfLifeGui(tk.Tk):
    # When you see something in parenthesis like this (tk.Tk), what it means
    # is that class is inheriting from another class.
    def __init__(self, *args, **kwargs):
        # __init__ це не функція але поводить себе як функція
        # args, kwargs allow you to pass non-keyworded
        # arguments(typical param)(args) and
        # keyworded arguments(dictionaries)(kwargs)
        tk.Tk.__init__(self, *args, **kwargs)  # init inherited class
        tk.Tk.wm_title(self, "Custom Title")
        container = tk.Frame(self)
        self.geometry("550x350+300+300")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # змінні по замовчуванню будуть в самому ядрі
        self.configuration = {"glider": tk.IntVar(),
                              "glider_gun": tk.IntVar(),
                              "update_interval": tk.IntVar(),
                              "table_size": tk.IntVar(),
                              "random_fill": tk.IntVar(),
                              "color_dead": tk.StringVar(),
                              "color_alive": tk.StringVar(),
                              "show_markup": tk.IntVar()}
        self.colors = ["white", "gray", "black", "blue", "red", "pink",
                       "purple", "brown", "orange", "yellow", "green"]
        self.frames = {}  # pre-defined a dictionary

        for F in (StartPage, Configure, QuickStart, ShowGame):
            frame = F(container, self)  # define the first frame
            self.frames[F] = frame  # list with all frames
            frame.grid(row=0, column=0, sticky="nsew")  # nsew mean north,south
            # place frame in(0,0)pos. in grid#nsew make frame fill entire space

        # self.show_frame(StartPage)
        self.show_frame(Configure)

    def show_frame(self, cont):
        frame = self.frames[cont]  # get StartPage class from frames dict.
        frame.tkraise()  # bring frame to the top

    # def run_configured(self):
    #     # controller = self
    #     core_class = self.init_core()

    def run_random(self):
        self.configuration["glider"].set(randint(0, 1))
        self.configuration["glider_gun"].set(randint(0, 1))
        self.configuration["update_interval"].set(randrange(200, 5000, 200))
        self.configuration["table_size"].set(randrange(50, 350, 50))
        self.configuration["random_fill"].set(randint(0, 1))
        self.configuration["color_dead"].set(choice(self.colors))
        self.configuration["color_alive"].set(choice(self.colors))
        self.configuration["show_markup"].set(randint(0, 1))

    def run_quick(self):
        pass

    def init_core(self):
        controller = self
        GameOfLife.ConwayGameOfLifeCore(controller)
        # self.show_frame(ShowGame)
        # return GameOfLife.ConwayGameOfLifeCore(controller)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="this is the start page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Configure",
                            command=lambda: controller.show_frame(Configure))
        button.pack()
        button2 = ttk.Button(self, text="Quick start",
                             command=lambda: controller.
                             show_frame(QuickStart))
        button2.pack()


class Configure(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Frame.configure(self, bg="red")

        ttk.Style().configure("HINT.TLabel", foreground="grey",
                              font=HINT_FONT)

        self.sign_frame()
        self.init_left_frame()
        self.init_right_frame()

    def sign_frame(self):
        frame0 = tk.Frame(self, bg="magenta")
        frame0.pack(fill=tk.X)

        label_sign = tk.Label(frame0, text="Виберіть бажані налаштування",
                              font=LARGE_FONT)
        label_sign.pack(side=tk.TOP, pady=10)

    def init_left_frame(self):
        frame1 = tk.Frame(self, width=1, height=1, bg="green", borderwidth=15)
        frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        label_hint_functional = ttk.Label(frame1, text="Функціональні:",
                                          style="HINT.TLabel")

        label_hint_functional.grid(row=0, column=0, pady=10, sticky=tk.W)
        glider_cb = tk.Checkbutton(frame1, text="Добавити глайдер ",
                                   variable=self.controller.configuration[
                                       "glider"])
        glider_cb.grid(row=1, column=0, pady=(0, 5), sticky=tk.W)
        glider_gun_cb = tk.Checkbutton(frame1,
                                       text="Добавити глайдерну гармату",
                                       variable=self.controller.configuration[
                                           "glider_gun"])
        glider_gun_cb.grid(row=2, column=0, columnspan=2, pady=(0, 15),
                           sticky=tk.W)

        label_view = ttk.Label(frame1, text="Відображення",
                               style="HINT.TLabel")
        label_view.grid(row=3, column=0, pady=(0, 10), sticky=tk.W)
        label_update = tk.Label(frame1, text="Швидкість оновлення ")
        label_update.grid(row=4, column=0, pady=(0, 5), sticky=tk.W)

        # set default value
        self.controller.configuration["update_interval"].set(1200)
        update_interval = tk.Spinbox(frame1, increment=200, from_=200,
                                     to=5000, textvariable=
                                     self.controller.configuration[
                                         "update_interval"], width=6,
                                     state="readonly")
        update_interval.grid(row=4, column=1, pady=(0, 5), padx=10,
                             sticky=tk.W)

        label_table_size = tk.Label(frame1, text="Величина таблиці")
        label_table_size.grid(row=5, column=0, pady=(0, 5), sticky=tk.W)
        # поставити обмеження на величину таблиці (у вигляді діалогового вікна)
        vcmd = (frame1.register(self.callback))
        size_entry = tk.Entry(frame1, width=5, validate="all",
                              validatecommand=(vcmd, "%P"),
                              textvariable=self.controller.configuration[
                                  "table_size"])
        size_entry.grid(row=5, column=1, pady=(0, 5), sticky=tk.W, padx=10)

        random_fill_cb = tk.Checkbutton(frame1,
                                        text="Випадкове заповнення таблиці",
                                        variable=self.controller.configuration[
                                            "random_fill"])
        random_fill_cb.grid(row=6, column=0, columnspan=2, pady=(15, 5),
                            sticky=tk.W)

    def callback(self, p):
        if str.isdigit(p) or p == "":
            return True
        else:
            return False

    def init_right_frame(self):
        frame2 = tk.Frame(self, width=1, height=1, bg="yellow", borderwidth=15)
        frame2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

        label_hint_cosmetic = ttk.Label(frame2, text="Косметичні:",
                                        style="HINT.TLabel")
        label_hint_cosmetic.grid(row=0, column=0, pady=10, sticky=tk.W)

        dead_label = tk.Label(frame2, text="Колір мертвої клітини")
        dead_label.grid(row=1, column=0, pady=(0, 5), sticky=tk.W)
        combobox_color_dead = ttk.Combobox(frame2,
                                           values=self.controller.colors,
                                           state="readonly",
                                           width=7, textvariable=
                                           self.controller.configuration[
                                               "color_dead"])
        combobox_color_dead.grid(row=1, column=1, pady=(0, 5), padx=(15, 35),
                                 sticky=tk.W)

        alive_label = tk.Label(frame2, text="Колір живої клітини")
        alive_label.grid(row=2, column=0, pady=(0, 5), sticky=tk.W)
        combobox_color_alive = ttk.Combobox(frame2,
                                            values=self.controller.colors,
                                            state="readonly",
                                            width=7, textvariable=
                                            self.controller.configuration[
                                                "color_alive"])
        combobox_color_alive.grid(row=2, column=1, pady=(0, 5), padx=(15, 35),
                                  sticky=tk.W)

        show_markup_cb = tk.Checkbutton(frame2, text="Відображати сітку",
                                        variable=self.controller.configuration[
                                            "show_markup"])
        show_markup_cb.grid(row=3, column=0, pady=(15, 5), sticky=tk.W)

        insert_random_button = tk.Button(frame2, text="Випадкові значення",
                                         command=self.controller.run_random)
        insert_random_button.grid(row=4, column=0, pady=(65, 0), padx=(0, 20),
                                  columnspan=2)
        # insert_random_button.bind()
        generate_button = tk.Button(frame2, text="Запустити",
                                    command=self.controller.init_core)
        generate_button.grid(row=4, column=0, pady=(65, 0), padx=(20, 0),
                             sticky=tk.E, columnspan=2)
        # generate_button.bind()


class QuickStart(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # test_class = self

        # extract to different function
        # core_class = GameOfLife.ConwayGameOfLifeCore(test_class)

        # # GameOfLife.ConwayGameOfLifeCore.get_figure(core_class)
        # canvas = FigureCanvasTkAgg(GameOfLife.ConwayGameOfLifeCore.
        #                            get_figure(core_class), self)
        # # canvas.draw()
        # canvas.get_tk_widget().grid(column=0, row=1)

        # img = core_class.get_ax().imshow()


class ShowGame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


app = ConwayGameOfLifeGui()
# quick_start_frame = app.get_frame(QuickStart)
#
# core_class = GameOfLife.ConwayGameOfLifeCore(quick_start_frame)
# ani = animation.FuncAnimation(
#     GameOfLife.ConwayGameOfLifeCore.get_figure(core_class),GameOfLife.update,
#     fargs=(GameOfLife.ConwayGameOfLifeCore.get_img(
#         core_class),
#            GameOfLife.ConwayGameOfLifeCore.get_grid(
#                core_class), 100,),
#     frames=10,
#     interval=1200,
#     save_count=50)
# ani.event_source.stop()
app.mainloop()
