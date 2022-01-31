from pathlib import Path
from tkinter import Tk, ttk, Canvas, Button, PhotoImage, Frame, Toplevel

from modules._calculator import Calculator
from modules._gpa_calculator import GPACalculator
from modules._visualize import Visualization
from modules._dataprocessing import writeData

import pyglet

pyglet.font.add_file(
    str(Path(__file__).parents[1] / Path("./font/Montserrat-Bold.otf"))
)
pyglet.font.add_file(
    str(Path(__file__).parents[1] / Path("./font/Montserrat-Regular.otf"))
)
pyglet.font.add_file(
    str(Path(__file__).parents[1] / Path("./font/Montserrat-SemiBold.otf"))
)


class GradeLedger(Tk):  # inherit tk class
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)  # also execute Tk init

        self.geometry("1000x800")
        self.configure(bg="#262322")
        self.overrideredirect(True)
        self.first_time = 0

        # Theme Wrapper
        theme_filepath = Path(__file__).parents[1] / "sun-valley.tcl"
        self.tk.call("source", theme_filepath)
        self.tk.call("set_theme", "dark")
        self.resizable(False, False)

        # TTK configs and tab
        style = ttk.Style()
        style.layout("TNotebook.Tab", [])  # turn off tabs
        style.layout("TNotebook", [])
        style.configure("TNotebook", tabmargins=0)

        self.GUI()

    def GUI(self):
        canvas = Canvas(
            self,
            bg="#262322",
            height=800,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.place(x=0, y=0)

        # title_bar = canvas.create_rectangle(0.0, 0.0, 1000.0, 40.0, fill="#353231", outline="")
        title_bar = Frame(self, width=850, height=40, bg="#353231", relief="flat")
        title_bar.place(x=150, y=0)
        title_bar.bind("<B1-Motion>", self.move_app)
        title_bar.bind("<Button-1>", self.get_pos)
        title_bar.bind("<Map>", lambda event: self.overrideredirect(True))
        self.notebook = ttk.Notebook(canvas, height=763, width=850)
        self.notebook.place(x=150, y=37)

        # Assign tab to tab class
        self.tab_1 = Intro(self.notebook)
        self.tab_2 = Calculator(self.notebook)
        self.tab_3 = Visualization(self.notebook, self.tab_2.share_data())
        self.tab_4 = GPACalculator(self.notebook)

        self.notebook.add(self.tab_1, text="Tab 1")
        self.notebook.add(self.tab_2, text="Tab 2")
        self.notebook.add(self.tab_3, text="Tab 3")
        self.notebook.add(self.tab_4, text="Tab 4")

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.quit,
            relief="flat",
        )
        button_1.place(x=959.0, y=9.0, width=23.0, height=21.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (self.overrideredirect(False), self.wm_state("iconic")),
            relief="flat",
        )
        button_2.place(x=907.0, y=9.0, width=23.0, height=21.0)

        canvas.create_rectangle(
            0.003939792513845575,
            2.958512050099671e-05,
            150.2438232153654,
            154.61529447769863,
            fill="#686666",
            outline="",
        )

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        image_2 = canvas.create_image(74.0, 78.0, image=self.image_image_2)

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.popup,
            relief="flat",
        )
        button_3.place(x=170.0, y=11.0, width=47.0, height=19.0)

        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.notebook.select(self.tab_1),
            relief="flat",
        )
        button_4.place(x=247.0, y=10.0, width=57.0, height=20.0)

        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_5.png"))
        button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.notebook.select(self.tab_2),
            relief="flat",
        )
        button_5.place(x=1.7763568394002505e-15, y=155.0, width=150.0, height=215.0)

        self.button_image_6 = PhotoImage(file=self.relative_to_assets("button_6.png"))
        button_6 = Button(
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (self.tab_3.Refresh(), self.notebook.select(self.tab_3)),
            relief="flat",
        )
        button_6.place(x=1.7763568394002505e-15, y=370.0, width=150.0, height=215.0)

        self.button_image_7 = PhotoImage(file=self.relative_to_assets("button_7.png"))
        button_7 = Button(
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (self.tab_4.GUI(), self.notebook.select(self.tab_4)),
            relief="flat",
        )
        button_7.place(x=1.7763568394002505e-15, y=585.0, width=150.0, height=215.0)

    def popup(self):
        self.confirmbox = ConfirmationBox(self).show()
        if self.confirmbox:
            writeData()

    def get_pos(self, event):
        global xwin
        global ywin

        xwin = event.x
        ywin = event.y

    def move_app(self, event):
        self.geometry(f"+{event.x_root - xwin}+{event.y_root}")

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(__file__).parents[1] / Path("./assets/root")
        return ASSETS_PATH / Path(path)


class Intro(Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(
            master=master,
            bg="#000000",
            height=763,
            width=850,
            bd=0,
            highlightthickness=0,
            relief="flat",
        )

        self.pack(fill="both", expand=1)

        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        image_1 = self.create_image(425.0, 381.0, image=self.image_image_1)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        image_3 = self.create_image(428.0, 237.0, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        image_4 = self.create_image(429.0, 480.0, image=self.image_image_4)

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(__file__).parents[1] / Path("./assets/root")
        return ASSETS_PATH / Path(path)


class ConfirmationBox(Toplevel):
    def __init__(self, master, *args, **kwargs):
        Toplevel.__init__(self, master=master, *args, **kwargs)

        self.status = None
        self.geometry("300x200")
        self.resizable(False, False)
        self.UI()

    def UI(self):
        self.canvas = Canvas(
            self,
            bg="#1C1C1C",
            height=200,
            width=300,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(150.0, 50.0, image=self.image_image_1)

        self.canvas.create_text(
            106.0,
            77.0,
            anchor="nw",
            text="Are you sure?",
            fill="#FFFFFF",
            font=("RobotoRoman Bold", 14 * -1),
        )

        self.canvas.create_text(
            10.0,
            104.0,
            justify="center",
            anchor="nw",
            text="The new data will overwrite the local database file.\nAre your sure?",
            fill="#FFFFFF",
            font=("Roboto", 12 * -1),
        )

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_8.png"))
        button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.yes_button,
            relief="flat",
        )
        button_1.place(x=41.0, y=154.0, width=88.0, height=30.461532592773438)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_9.png"))
        button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.no_button,
            relief="flat",
        )
        button_2.place(x=171.0, y=154.0, width=88.0, height=30.461532592773438)

    def yes_button(self):
        self.status = True
        self.terminate()

    def no_button(self):
        self.status = False
        self.terminate()

    def terminate(self):
        self.destroy()

    def show(self):
        self.grab_set()
        self.wm_deiconify()
        self.wait_window()
        return self.status

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(__file__).parents[1] / Path("./assets/customize")
        return ASSETS_PATH / Path(path)
