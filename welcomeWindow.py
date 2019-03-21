import tkinter as tk
from tkinter import ttk
import GameOfLife
import matplotlib
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
        self.geometry("600x400+300+300")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # pre-defined a dictionary

        for F in (StartPage, Configure, QuickStart):
            frame = F(container, self)  # define the first frame
            self.frames[F] = frame  # list with all frames
            frame.grid(row=0, column=0, sticky="nsew")  # nsew mean north,south
            # place frame in(0,0)pos. in grid#nsew make frame fill entire space

        # self.show_frame(StartPage)
        self.show_frame(Configure)

    def show_frame(self, cont):
        frame = self.frames[cont]  # get StartPage class from frames dict.
        frame.tkraise()  # bring frame to the top


# ____________________back-end(above)__________________________________________


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="this is the start page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)  # pad - padding for x and y

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
        # Not Used
        # ttk.Style().configure("REGULAR.TLabel",
        #                       foreground="black",
        #                       font=REGULAR_FONT)
        self.sign_frame()
        self.init_left_frame()
        self.init_rigth_frame()

        #
        # label_hint_view = ttk.Label(self, text="Відображення: ",
        #                             style="HINT.TLabel")
        # label_hint_view
        # # Що робить Text Variable

    def sign_frame(self):
        frame0 = tk.Frame(self, bg="magenta")
        frame0.pack(fill=tk.X)
        label_sign = tk.Label(frame0, text="Виберіть бажані налаштування",
                              font=LARGE_FONT)
        label_sign.pack(side=tk.TOP, pady=10)

    def init_left_frame(self):
        frame1 = tk.Frame(self, width=1, height=1, bg="green")
        frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        nested_frame = tk.Frame(frame1, bg="khaki", borderwidth=15)
        nested_frame.pack(fill=tk.X)
        # frame1 = tk.Frame(self, bg="green")
        # frame1.pack(fill=tk.X)

        label_hint_functional = ttk.Label(nested_frame, text="Функціональні:",
                                          style="HINT.TLabel")
        # label_hint_functional.grid(row=0, column=0, pady=10, padx=15,
        #                            sticky=tk.W)
        label_hint_functional.grid(row=0, column=0, pady=10, sticky=tk.W)
        glider_cb = tk.Checkbutton(nested_frame, text="Добавити глайдер ")
        # glider_cb.grid(row=1, column=0, pady=5, padx=15, sticky=tk.W)
        glider_cb.grid(row=1, column=0, pady=(0, 5), sticky=tk.W)
        glider_gun_cb = tk.Checkbutton(nested_frame,
                                       text="Добавити глайдерну гармату")
        # glider_gun_cb.grid(row=2, column=0, pady=(0, 15), padx=15, sticky=tk.W)
        glider_gun_cb.grid(row=2, column=0, columnspan=2, pady=(0, 15),
                           sticky=tk.W)

        label_view = ttk.Label(nested_frame, text="Відображення",
                               style="HINT.TLabel")
        # label_view.grid(row=3, column=0, pady=(0, 10), padx=15, sticky=tk.W)
        label_view.grid(row=3, column=0, pady=(0, 10), sticky=tk.W)

        label_update = tk.Label(nested_frame, text="Швидкість оновлення ")
        # label_update.grid(row=4, column=0, pady=(0, 5), padx=15, sticky=tk.W)
        label_update.grid(row=4, column=0, pady=(0, 5), sticky=tk.W)
        # test max value
        update_interval = tk.Spinbox(nested_frame, increment=100, from_=100,
                                     to=5000, width=6)
        update_interval.grid(row=4, column=1, pady=(0, 5), padx=10,
                             sticky=tk.W)
        label_table_size = tk.Label(nested_frame, text="Величина таблиці")
        label_table_size.grid(row=5, column=0, pady=(0, 5), sticky=tk.W)
        # поставити обмеження на величину таблиці (у вигляді діалогового вікна)
        vcmd = (nested_frame.register(self.callback))
        size_entry = tk.Entry(nested_frame, width=5, validate="all",
                              validatecommand=(vcmd, "%P"))
        size_entry.grid(row=5, column=1, pady=(0, 5), sticky=tk.W, padx=10)

        random_cb = tk.Checkbutton(nested_frame,
                                   text="Випадкове заповнення таблиці")
        random_cb.grid(row=6, column=0, columnspan=2, pady=(15, 5),
                       sticky=tk.W)

    def callback(self, p):
        if str.isdigit(p) or p == "":
            return True
        else:
            return False

    def init_rigth_frame(self):
        frame2 = tk.Frame(self, width=1, height=1, bg="yellow")
        frame2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

        label_hint_cosmetic = ttk.Label(frame2, text="Косметичні:",
                                        style="HINT.TLabel")
        label_hint_cosmetic.pack(side=tk.LEFT, pady=10, padx=10)
        #
        # combobox_dead = ttk.Combobox(frame2, values=[
        #     "white", "gray", "black", "blue", "red", "pink",
        #     "purple", "brown", "orange", "yellow", "green"], state="readonly",
        #                              width=7)
        # combobox_dead.pack(side=tk.RIGHT, padx=20)
        info_label_cb = tk.Label(frame2, text="Колір мертвої клітини")
        info_label_cb.pack(side=tk.TOP, padx=5, pady=10)


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
