import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import GameOfLife
from random import randint, randrange, choice

LARGE_FONT = ("Verdana", 12)
HINT_FONT = ("Verdana", 7)


class ConwayGameOfLifeGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "\"Гра життя\", Джона Конвея")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.configuration = {"glider": tk.IntVar(),
                              "oscillator": tk.IntVar(),
                              "update_interval": tk.IntVar(),
                              "grid_size": tk.IntVar(),
                              "random_fill": tk.IntVar(),
                              "color_dead": tk.StringVar(),
                              "color_alive": tk.StringVar(),
                              "show_generation": tk.IntVar()}
        # define color for combobox widgets
        self.colors = ["white", "gray", "black", "blue", "red", "pink",
                       "purple", "brown", "orange", "yellow", "green"]
        # dict with frames
        self.frames = {}

        for F in (StartPage, Configure, ShowGame):
            frame = F(container, self)  # define the first frame
            self.frames[F] = frame  # list with all frames
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        """Show frame by received reference, and delete others"""
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[cont]
        frame.grid()
        frame.winfo_toplevel().geometry("")

    def init_core(self):
        """Create an instance of GameOfLifeCore and show it on frame"""
        controller = self
        if self.check_entry():
            return
        GameOfLife.ConwayGameOfLifeCore(controller)
        self.show_frame(ShowGame)

    def core_frame_ref(self):
        return self.frames[ShowGame]

    def run_random(self):
        self.configuration["glider"].set(randint(0, 1))
        self.configuration["oscillator"].set(randint(0, 1))
        self.configuration["update_interval"].set(randrange(200, 5000, 200))
        self.configuration["grid_size"].set(randrange(50, 150, 50))
        self.configuration["random_fill"].set(randint(0, 1))
        self.configuration["color_dead"].set(choice(self.colors))
        self.configuration["color_alive"].set(choice(self.colors))
        self.configuration["show_generation"].set(randint(0, 1))

    def check_entry(self):
        if (self.configuration["grid_size"].get() > 150
            or self.configuration["grid_size"].get() < 20) \
                and self.configuration["grid_size"].get() != 0:
            messagebox.showinfo("Увага", "Для коректної роботи програми "
                                         "виберіть розмір сітки в "
                                         "межах від 50 до 150.")
            return True


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self,
                          text="Вітаю. Ви щойно відкрили програму яка "
                               "симулює \"Гру життя\" Джона Конвея. \nЦю "
                               "програму написав Зелінський Павло, студент "
                               "ПМ-2, в якості курсової роботи. \n"
                               "Натисність кнопку \"Налаштувати гру\" для "
                               "того щоб вибрати запропоновані налаштування.\n"
                               "І кнопку \"Швидкий старт\" для того щоб "
                               "запустити гру з параметрами по замовчуванню.",
                          font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=10, pady=40, padx=40)

        configure_button = ttk.Button(self, text="Налаштувати гру",
                                      command=lambda: controller.show_frame(
                                          Configure))
        configure_button.grid(row=1, column=4, padx=(0, 5), pady=(0, 30),
                              sticky=tk.E)

        start_button = ttk.Button(self, text=" Швидкий старт ",
                                  command=self.controller.init_core)
        start_button.grid(row=1, column=5, padx=(5, 0), pady=(0, 30),
                          sticky=tk.W)


class Configure(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Frame.configure(self)

        ttk.Style().configure("HINT.TLabel", foreground="grey",
                              font=HINT_FONT)

        self.sign_frame()
        self.init_left_frame()
        self.init_right_frame()

    def sign_frame(self):
        """Init frame with Top Label"""
        frame0 = tk.Frame(self)
        frame0.pack(fill=tk.X)

        label_sign = tk.Label(frame0, text="Виберіть бажані налаштування",
                              font=LARGE_FONT)
        label_sign.pack(side=tk.TOP, pady=10)

    def init_left_frame(self):
        """Init left side of Configuration screen"""
        frame1 = tk.Frame(self, width=1, height=1, borderwidth=15)
        frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        label_hint_functional = ttk.Label(frame1, text="Функціональні:",
                                          style="HINT.TLabel")
        label_hint_functional.grid(row=0, column=0, padx=(0, 40), pady=10,
                                   sticky=tk.W)

        glider_cb = tk.Checkbutton(frame1, text="Добавити глайдер ",
                                   variable=self.controller.configuration[
                                       "glider"])
        glider_cb.grid(row=1, column=0, pady=(0, 5), sticky=tk.W)

        oscillator_cb = tk.Checkbutton(frame1,
                                       text="Добавити осцилятор, фігуру яка "
                                            "повторюється",
                                       variable=self.controller.configuration[
                                           "oscillator"])
        oscillator_cb.grid(row=2, column=0, columnspan=3, pady=(0, 15),
                           sticky=tk.W)

        label_view = ttk.Label(frame1, text="Відображення:",
                               style="HINT.TLabel")
        label_view.grid(row=3, column=0, pady=(0, 10), sticky=tk.W)

        label_update = tk.Label(frame1, text="Швидкість оновлення ")
        label_update.grid(row=4, column=0, pady=(0, 5), sticky=tk.W)
        # set default value
        self.controller.configuration["update_interval"].set(600)
        update_interval = tk.Spinbox(frame1, increment=200, from_=200,
                                     to=5000,
                                     textvariable=self.controller.
                                     configuration["update_interval"],
                                     width=6, state="readonly")
        update_interval.grid(row=4, column=1, pady=(0, 5), padx=10,
                             sticky=tk.W)

        label_grid_size = tk.Label(frame1, text="Величина таблиці")
        label_grid_size.grid(row=5, column=0, pady=(0, 5), sticky=tk.W)
        
        vcmd = (frame1.register(self.entry_callback))
        size_entry = tk.Entry(frame1, width=5, validate="all",
                              validatecommand=(vcmd, "%P"),
                              textvariable=self.controller.configuration[
                                  "grid_size"])
        size_entry.grid(row=5, column=1, pady=(0, 5), sticky=tk.W, padx=10)

        random_fill_cb = tk.Checkbutton(frame1,
                                        text="Випадкове заповнення таблиці",
                                        variable=self.controller.configuration[
                                            "random_fill"])
        random_fill_cb.grid(row=6, column=0, columnspan=2, padx=(0, 90),
                            pady=(15, 25),
                            sticky=tk.W)

    def entry_callback(self, p):
        """Filter entered values to pass only numbers"""
        if str.isdigit(p) or p == "":
            return True
        else:
            return False

    def init_right_frame(self):
        """Init right side of Configuration screen"""
        frame2 = tk.Frame(self, width=1, height=1, borderwidth=15)
        frame2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

        label_hint_cosmetic = ttk.Label(frame2, text="Косметичні:",
                                        style="HINT.TLabel")
        label_hint_cosmetic.grid(row=0, column=0, pady=10, sticky=tk.W)

        dead_label = tk.Label(frame2, text="Колір мертвої клітини")
        dead_label.grid(row=1, column=0, pady=(0, 5), sticky=tk.W)

        combobox_color_dead = ttk.Combobox(frame2,
                                           values=self.controller.colors,
                                           state="readonly",
                                           width=7,
                                           textvariable=self.controller.
                                           configuration["color_dead"])
        combobox_color_dead.grid(row=1, column=1, pady=(0, 5), padx=(15, 35),
                                 sticky=tk.W)

        alive_label = tk.Label(frame2, text="Колір живої клітини")
        alive_label.grid(row=2, column=0, pady=(0, 5), sticky=tk.W)

        combobox_color_alive = ttk.Combobox(frame2,
                                            values=self.controller.colors,
                                            state="readonly",
                                            width=7,
                                            textvariable=self.controller.
                                            configuration["color_alive"])
        combobox_color_alive.grid(row=2, column=1, pady=(0, 5), padx=(15, 35),
                                  sticky=tk.W)

        show_generation_cb = tk.Checkbutton(frame2,
                                            text="Відображати номер генерації",
                                            variable=self.controller.
                                            configuration["show_generation"])
        show_generation_cb.grid(row=3, column=0, pady=(15, 5), sticky=tk.W)

        insert_random_button = ttk.Button(frame2, text="Випадкові значення",
                                          command=self.controller.run_random)
        insert_random_button.grid(row=4, column=0, pady=(65, 0), padx=(0, 80),
                                  columnspan=2, sticky=tk.E)

        generate_button = ttk.Button(frame2, text="Запустити",
                                     command=self.controller.init_core)
        generate_button.grid(row=4, column=0, pady=(65, 0), padx=(10, 0),
                             sticky=tk.E, columnspan=2)


class ShowGame(tk.Frame):
    """Frame that contain GameOfLife CoreClass"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


app = ConwayGameOfLifeGui()
app.mainloop()
