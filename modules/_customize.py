from pathlib import Path
from tkinter import (
    Toplevel,
    ttk,
    Canvas,
    Entry,
    PhotoImage,
    Button,
    Frame,
)

# Internal module
from modules._dataprocessing import (
    get_subjects,
    get_coursework,
    remove_row,
    add_subject,
    add_coursework,
    del_subject,
    edit_coursework,
)

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


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / Path("./assets/customize")
    return ASSETS_PATH / Path(path)


class CustomizeSubject(Toplevel):
    def __init__(self, master, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)
        self.geometry("750x550")
        self.resizable(False, False)
        self.overrideredirect(True)
        customize_canvas = Customize(self)


class Customize(Canvas):
    def __init__(self, master):
        super().__init__(
            master=master,
            bg="#1C1C1C",
            height=550,
            width=750,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.place(x=0, y=0)
        self.GUI()

    def GUI(self):

        # For some reason, kalau letak bawah kene garbage collected, mungkin  x assign root kt toplevel.
        # temporary

        self.title_bar = Frame(self, width=750, height=30, bg="#353231", relief="flat")
        self.title_bar.place(x=0, y=0)
        self.title_bar.bind("<B1-Motion>", self.move_app)
        self.title_bar.bind("<Button-1>", self.get_pos)

        self.bottom_bar = Frame(self, width=750, height=30, bg="#353231", relief="flat")
        self.bottom_bar.place(x=0, y=520)

        self.create_text(
            355.0,
            7.0,
            anchor="nw",
            text="Customize",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.button_image_1 = PhotoImage(  # Delete Subject
            file=relative_to_assets("button_1.png")
        )
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=DeleteSubject,
            relief="flat",
        )
        button_1.place(x=23.0, y=72.0, width=91.0, height=35.0)

        self.button_image_2 = PhotoImage(  # Add coursework
            file=relative_to_assets("button_2.png")
        )
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=AddCoursework,
            relief="flat",
        )
        button_2.place(x=113.0, y=32.0, width=111.0, height=35.0)

        self.button_image_3 = PhotoImage(  # Add Subject
            file=relative_to_assets("button_3.png")
        )
        button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=AddSubject,
            relief="flat",
        )
        button_3.place(x=23.0, y=32.0, width=91.0, height=36.0)

        self.create_text(
            365.0,
            45.0,
            anchor="nw",
            text="Subject",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.create_text(
            80.0,
            130.0,
            anchor="nw",
            text="No",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12 * -1),
        )

        self.create_text(
            135.0,
            130.0,
            anchor="nw",
            text="Coursework",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12 * -1),
        )

        self.create_text(
            420.0,
            130.0,
            anchor="nw",
            text="Mark",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12 * -1),
        )

        self.create_text(
            487.0,
            130.0,
            anchor="nw",
            text="Percentage",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12 * -1),
        )

        self.create_text(
            609.0,
            130.0,
            anchor="nw",
            text="Action",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12 * -1),
        )

        self.button_image_7 = PhotoImage(file=relative_to_assets("button_10.png"))
        button_7 = Button(
            self,
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (self.master.master.updateSubject(), self.master.destroy()),
            relief="flat",
        )
        button_7.place(x=718.0, y=5.0, width=23.0, height=21.0)

        self.create_rectangle(69.0, 125.0, 70.0, 152.0, fill="#F0EFEF", outline="")

        self.create_rectangle(69.0, 124.0, 685.0, 125.0, fill="#F0EFEF", outline="")

        self.create_rectangle(397.0, 125.0, 398.0, 152.0, fill="#F0EFEF", outline="")

        self.create_rectangle(574.0, 125.0, 575.0, 152.0, fill="#F0EFEF", outline="")

        self.create_rectangle(684.0, 125.0, 685.0, 152.0, fill="#F0EFEF", outline="")

        self.create_rectangle(473.0, 125.0, 474.0, 152.0, fill="#F0EFEF", outline="")

        self.create_rectangle(123.0, 125.0, 124.0, 153.0, fill="#F0EFEF", outline="")

        self.create_rectangle(69.0, 152.0, 685.0, 153.0, fill="#F0EFEF", outline="")

        # Subject Combobox
        self.subject_list = get_subjects()
        self.subject_combobox = ttk.Combobox(
            self, values=self.subject_list, justify="center"
        )
        self.subject_combobox["state"] = "readonly"
        self.subject_combobox.place(x=295.0, y=70.0, width=200, height=30)
        self.subject_combobox.bind("<<ComboboxSelected>>", self.updateSubject)
        self.subject_combobox.bind("<1>", self.fetch)

    def updateSubject(self, event=None):
        subject = self.subject_combobox.get()
        if subject != "":
            Table().ResetTable(self)  # Reset previous subject table
            for i in get_coursework(subject):
                Table().create_row(self, i, subject)

    def fetch(self, event=None):
        self.subject_combobox["values"] = get_subjects()

    def get_pos(self, event):
        global xwin
        global ywin

        xwin = event.x
        ywin = event.y

    def move_app(self, event):
        self.master.geometry(f"+{event.x_root - xwin}+{event.y_root}")


class AddSubject(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("400x140")
        self.configure(bg="#262322")
        self.resizable(False, False)
        self.GUI()

    def GUI(self):

        self.canvas = Canvas(
            self,
            bg="#262322",
            height=140,
            width=400,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            150.0,
            30.0,
            anchor="nw",
            text="Add New Subject",
            fill="#FFFFFF",
            font=("Roboto", 14 * -1),
        )

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.destroy,
            relief="flat",
        )
        button_1.place(x=369.0, y=9.0, width=23.0, height=21.0)

        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(200.0, 74.5, image=self.entry_image_1)
        self.entry_1 = Entry(
            self.canvas, bd=0, bg="#383535", highlightthickness=0, justify="center"
        )
        self.entry_1.place(x=59.5, y=61.0, width=281.0, height=25.0)

        self.button_image_2 = PhotoImage(  # Add Button
            file=self.relative_to_assets("button_2.png")
        )
        button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (add_subject(self.entry_1.get()), self.destroy()),
            relief="flat",
        )
        button_2.place(x=156.0, y=99.0, width=91.0, height=28.0)

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(__file__).parent / Path("./assets/customize/addsubject")
        return ASSETS_PATH / Path(path)


class DeleteSubject(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("400x140")
        self.configure(bg="#262322")
        self.resizable(False, False)
        self.GUI()

    def GUI(self):

        self.canvas = Canvas(
            self,
            bg="#262322",
            height=140,
            width=400,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            160.0,
            30.0,
            anchor="nw",
            text="Delete Subject",
            fill="#FFFFFF",
            font=("Roboto", 14 * -1),
        )

        # Subject Combobox
        subject_list = get_subjects()
        self.subject_combobox = ttk.Combobox(
            self, values=subject_list, justify="center"
        )
        self.subject_combobox["state"] = "readonly"
        self.subject_combobox.place(x=100.5, y=55.0, width=200, height=30)
        # self.subject_combobox.bind("<<ComboboxSelected>>", self.updateSubject)

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.destroy,
            relief="flat",
        )
        button_1.place(x=369.0, y=9.0, width=23.0, height=21.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_delete,
            relief="flat",
        )
        button_2.place(x=156.0, y=99.0, width=91.0, height=28.0)

    def on_delete(self):
        self.confirmbox = ConfirmationBox(self).show()
        if self.confirmbox:
            del_subject(self.subject_combobox.get())

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(__file__).parent / Path("./assets/customize/deletesubject")
        return ASSETS_PATH / Path(path)


class AddCoursework(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("400x358")
        self.configure(bg="#262322")
        self.resizable(False, False)
        self.GUI()

    def GUI(self):
        self.canvas = Canvas(
            self,
            bg="#262322",
            height=358,
            width=400,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            135,
            88.0,
            anchor="nw",
            text="Add New Coursework",
            fill="#FFFFFF",
            font=("Roboto", 14 * -1),
        )

        self.canvas.create_text(
            180,
            20.0,
            anchor="nw",
            text="Subject",
            fill="#FFFFFF",
            font=("Roboto", 14 * -1),
        )

        subject_list = get_subjects()
        self.subject_combobox = ttk.Combobox(
            self, values=subject_list, justify="center"
        )
        self.subject_combobox["state"] = "readonly"
        self.subject_combobox.place(x=105, y=47, width=200, height=30)
        # self.subject_combobox.bind("<<ComboboxSelected>>", self.updateSubject)

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.destroy,
            relief="flat",
        )
        button_1.place(x=369.0, y=9.0, width=23.0, height=21.0)

        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(
            199.49999999999997, 133.5, image=self.entry_image_1
        )
        self.entry_1 = Entry(
            self.canvas, justify="center", bd=0, bg="#383535", highlightthickness=0
        )
        self.entry_1.place(x=94.49999999999997, y=120.0, width=210.0, height=25.0)

        self.canvas.create_text(
            160,
            234.0,
            anchor="nw",
            text="Percentage (%)",
            fill="#FFFFFF",
            font=("Roboto", 14 * -1),
        )

        self.canvas.create_text(
            170,
            163.0,
            anchor="nw",
            text="Total Mark",
            fill="#FFFFFF",
            font=("Roboto", 14 * -1),
        )

        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(
            199.99999999999997, 203.5, image=self.entry_image_2
        )
        self.entry_2 = Entry(
            self.canvas, justify="center", bd=0, bg="#383535", highlightthickness=0
        )
        self.entry_2.place(x=135.49999999999997, y=190.0, width=129.0, height=25.0)

        entry_bg_3 = self.canvas.create_image(
            199.99999999999997, 274.5, image=self.entry_image_2
        )
        self.entry_3 = Entry(
            self.canvas, justify="center", bd=0, bg="#383535", highlightthickness=0
        )
        self.entry_3.place(x=135.49999999999997, y=261.0, width=129.0, height=25.0)

        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png")
        )  # Add button
        button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (
                add_coursework(
                    self.subject_combobox.get(),
                    self.entry_1.get(),
                    self.entry_3.get(),
                    self.entry_2.get(),
                ),
                self.destroy(),
            ),
            relief="flat",
        )
        button_2.place(x=160, y=309.0, width=91.0, height=28.0)

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(__file__).parent / Path("./assets/customize/addcoursework")
        return ASSETS_PATH / Path(path)


class Table:
    count = 0
    widget_list = []

    def __init__(self):
        self._y_spacing = float(Table.count * 34)
        Table.count += 1

    def create_row(self, obj, assessment, subject):

        t0 = obj.create_text(  ####
            85.0,
            161.0 + self._y_spacing,
            anchor="nw",
            text=Table.count,
            fill="#FFFFFF",
            justify="center",
            font=("Segoie Regular", 12 * -1),
        )

        t1 = obj.create_text(  # assessment
            135.0,
            162.0 + self._y_spacing,
            anchor="nw",
            text=assessment[2],
            fill="#FFFFFF",
            justify="left",
            font=("Montserrat Regular", 12 * -1),
        )

        t2 = obj.create_text(  # percentage
            510.0,
            162.0 + self._y_spacing,
            anchor="nw",
            text=assessment[3],
            fill="#FFFFFF",
            font=("Montserrat Regular", 12 * -1),
            justify="center",
        )

        t3 = obj.create_text(  # mark
            425.0,
            162.0 + self._y_spacing,
            anchor="nw",
            text=assessment[4],
            fill="#FFFFFF",
            justify="center",
            font=("Montserrat Regular", 12 * -1),
        )

        # -------------- table graphic -----------------
        t4 = obj.create_rectangle(  ####
            397.0,
            153.0 + self._y_spacing,
            398.0,
            186.0 + self._y_spacing,
            fill="#616161",
            outline="",
        )

        t5 = obj.create_rectangle(  ####
            473.0,
            153.0 + self._y_spacing,
            474.0,
            186.0 + self._y_spacing,
            fill="#616161",
            outline="",
        )

        t6 = obj.create_rectangle(  ####
            574.0,
            153.0 + self._y_spacing,
            575.0,
            186.0 + self._y_spacing,
            fill="#616161",
            outline="",
        )

        t7 = obj.create_rectangle(  ####
            684.0,
            153.0 + self._y_spacing,
            685.0,
            186.0 + self._y_spacing,
            fill="#616161",
            outline="",
        )

        t8 = obj.create_rectangle(  ####
            70.0,
            185.0 + self._y_spacing,
            685.0,
            186.0 + self._y_spacing,
            fill="#616161",
            outline="",
        )
        t9 = obj.create_rectangle(  ####
            123.0,
            153.0 + self._y_spacing,
            124.0,
            186.0 + self._y_spacing,
            fill="#616161",
            outline="",
        )

        t10 = obj.create_rectangle(  ####
            69.0,
            153.0 + self._y_spacing,
            70.0,
            186.0 + self._y_spacing,
            fill="#616161",
            outline="",
        )

        self.edit_button_img = PhotoImage(file=relative_to_assets("button_4.png"))
        self.delete_button_img = PhotoImage(file=relative_to_assets("button_5.png"))

        edit_button = Button(
            obj,
            image=self.edit_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: EditCourseworkWindow(subject, assessment[2]),
            relief="flat",
        )
        edit_button.place(x=587.0, y=160.0 + self._y_spacing, width=36.0, height=18.0)

        delete_button = Button(
            obj,
            image=self.delete_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.delete(obj, assessment),
            relief="flat",
        )
        delete_button.place(x=626.0, y=160.0 + self._y_spacing, width=47.0, height=19.0)

        Table.widget_list.append(
            (t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, edit_button, delete_button)
        )  # Store for reset function

    def delete(self, obj, assessment):
        self.confirmbox = ConfirmationBox(obj).show()
        if self.confirmbox:
            remove_row(index=assessment[0])
            obj.updateSubject()

    def ResetTable(self, obj):
        if Table.widget_list:
            for row in Table.widget_list:
                for widget in row:
                    if isinstance(widget, int):
                        obj.delete(widget)  # canvas.delete(if), canvas id bukan object
                    else:
                        widget.destroy()  # if object, button
        Table.widget_list = []  # Reset all constructor
        Table.count = 0


class EditCourseworkWindow(Toplevel):
    def __init__(self, subject, coursework):
        Toplevel.__init__(self)
        self.geometry("316x280")
        self.configure(bg="#262322")
        self.resizable(False, False)
        self.subject = subject
        self.coursework = coursework
        self.UI()

    def UI(self):
        self.canvas = Canvas(
            self,
            bg="#262322",
            height=358,
            width=400,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            130,
            10.0,
            anchor="nw",
            justify="center",
            text=f"Edit {self.coursework}",
            fill="#FFFFFF",
            font=("Roboto", 14 * -1),
        )

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.destroy,
            relief="flat",
        )
        button_1.place(x=369.0, y=9.0, width=23.0, height=21.0)

        self.canvas.create_text(
            115,
            134.0,
            anchor="nw",
            text="Percentage (%)",
            fill="#FFFFFF",
            font=("Roboto", 14 * -1),
        )

        self.canvas.create_text(
            125,
            63.0,
            anchor="nw",
            text="Total Mark",
            fill="#FFFFFF",
            font=("Roboto", 14 * -1),
        )

        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(
            159.99999999999997, 103.5, image=self.entry_image_2
        )
        self.entry_2 = Entry(
            self.canvas, justify="center", bd=0, bg="#383535", highlightthickness=0
        )
        self.entry_2.place(x=95, y=90.0, width=129.0, height=25.0)

        entry_bg_3 = self.canvas.create_image(
            159.99999999999997, 174.5, image=self.entry_image_2
        )
        self.entry_3 = Entry(
            self.canvas, justify="center", bd=0, bg="#383535", highlightthickness=0
        )
        self.entry_3.place(x=95.49999999999997, y=161.0, width=129.0, height=25.0)

        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png")
        )  # Add button
        button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (
                edit_coursework(
                    self.subject,
                    self.coursework,
                    self.entry_2.get(),
                    self.entry_3.get(),
                ),
                self.destroy(),
            ),
            relief="flat",
        )
        button_2.place(x=110, y=220.0, width=91.0, height=28.0)

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(__file__).parent / Path("./assets/customize/addcoursework")
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
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
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
            45.0,
            104.0,
            justify="center",
            anchor="nw",
            text="Do you really want to delete the item.\nThis data cannot be restored.",
            fill="#FFFFFF",
            font=("Roboto", 12 * -1),
        )

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_8.png"))
        button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.yes_button,
            relief="flat",
        )
        button_1.place(x=41.0, y=154.0, width=88.0, height=30.461532592773438)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_9.png"))
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
