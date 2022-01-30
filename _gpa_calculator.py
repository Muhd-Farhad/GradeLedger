from pathlib import Path
from tkinter import (
    Tk,
    Toplevel,
    ttk,
    Canvas,
    Entry,
    PhotoImage,
    StringVar,
    Button,
    Frame,
    Label,
    StringVar,
)
from functools import partial
from _dataprocessing import get_subjects, isinteger, isfloat

grade_list = ["", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "E", "F"]
row_count = 0  # table row


class GPACalculator(Canvas):
    def __init__(self, master):
        super().__init__(
            master=master,
            bg="#1C1C1C",
            height=763,
            width=850,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.place(x=0, y=0)
        self.row_count = 0
        self.GUI()

    def GUI(self):

        self.create_text(
            63.0,
            70.0,
            anchor="nw",
            text="Subject",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.create_text(
            328.0,
            66.0,
            anchor="nw",
            justify="center",
            text="Grade Points",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 14 * -1),
        )

        self.create_text(
            530.0,
            66.0,
            anchor="nw",
            text="Grade",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 14 * -1),
        )

        self.create_text(
            685.0,
            66.0,
            anchor="nw",
            text="Credit Hours",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 14 * -1),
        )

        # Holo Circle
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.HoloLabel = Label(
            self,
            image=self.image_image_1,
            fg="#FFFFFF",
            text="-",
            bg="#1C1C1C",
            compound="center",
            font=("Segoe UI", 30, "bold"),
        )
        self.HoloLabel.place(x=335, y=570)

        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))

        self.create_row()
    
    def create_row(self):
        global row_count
        subject_list = get_subjects()
        Table().ResetTable(self)
        for i in subject_list:
            Table().create_row(self, i)
            row_count += 1

    # Declare StringVar for Table

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(__file__).parent / Path("./assets/gpa_calculator")
        return ASSETS_PATH / Path(path)


class Table:
    widget_list = []
    entry_widget_list = []

    def __init__(self):
        self._y_spacing = float(row_count * 50)
        self.credit_hrs_list = []

    def create_row(self, canvas, subject):
        self.canvas = canvas
        entry_bg_1 = canvas.create_image(
            370.5, 139.0 + self._y_spacing, image=canvas.entry_image_1
        )

        self.gradePts = Entry(  # GPA Points
            canvas,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            justify="center",
            disabledbackground="#383535",
        )
        self.gradePts.place(
            x=348.0 + 6, y=122.0 + self._y_spacing, width=33.0, height=32.0
        )

        entry_bg_2 = canvas.create_image(
            730.5, 139.0 + self._y_spacing, image=canvas.entry_image_1
        )

        self.credit_hrs = Entry(  # Credit Hours
            canvas,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            justify="center",
        )
        self.credit_hrs.place(
            x=719.0 - 5, y=122.0 + self._y_spacing, width=33.0, height=32.0
        )

        self.gradePts.bind("<Any-KeyRelease>", self.calculateGPA)
        self.credit_hrs.bind("<Any-KeyRelease>", self.calculateGPA)

        t1 = canvas.create_text(
            63.0,
            126.0 + self._y_spacing,
            anchor="nw",
            text=subject,
            fill="#FFFFFF",
            font=("Montserrat Regular", 13 * -1),
        )

        self.grade_combobox = ttk.Combobox(
            canvas, values=grade_list, justify="center", font="Arial 9 bold"
        )
        self.grade_combobox["state"] = "readonly"
        self.grade_combobox.place(
            x=515.0, y=126.0 + self._y_spacing, width=80.0, height=27.0
        )

        self.grade_combobox.bind("<<ComboboxSelected>>", self.calculateGPA)

        Table.entry_widget_list.append(
            [
                self.grade_combobox,
                self.gradePts,
                self.credit_hrs,
            ]
        )
        Table.widget_list.append(
            (
                entry_bg_1,
                entry_bg_2,
                self.gradePts,
                t1,
                self.grade_combobox,
            )
        )  # Store for reset function

    def calculateGPA(self, event=None):
        gradePoint = {  # boleh unified dlm _data_processing
            "A": 4,
            "A-": 3.67,
            "B+": 3.33,
            "B": 3.00,
            "B-": 2.67,
            "C+": 2.33,
            "C": 2.00,
            "C-": 1.67,
            "D+": 1.33,
            "D": 1.00,
            "E": 0.67,
            "F": 0.00,
        }
        totalQPPts = 0
        totalCreditHrs = 0
        CreditHrs = 0
        if Table.entry_widget_list:
            for i in Table.entry_widget_list:
                self.grade_combobox["state"] = "readonly"  #
                self.gradePts["state"] = "normal"
                if len(self.credit_hrs.get()) > 0 and isfloat(self.credit_hrs.get()):
                    CreditHrs = float(self.credit_hrs.get())
                    totalCreditHrs += CreditHrs
                    if len(self.grade_combobox.get()) > 0:
                        # i[0]["state"] = "readonly"
                        self.gradePts["state"] = "disabled"
                        grade = self.grade_combobox.get()
                        totalQPPts += gradePoint[grade] * CreditHrs
                        continue
                    if len(self.gradePts.get()) > 0 and isfloat(i[1].get()):
                        print("manual")
                        self.grade_combobox["state"] = "disabled"
                        totalQPPts += float(self.gradePts.get()) * CreditHrs
        # Calculate GPA
        if totalQPPts > 0 and totalCreditHrs > 0:
            VAL = totalQPPts / totalCreditHrs
            self.canvas.HoloLabel["text"] = f"{VAL:.2f}"
        else:
            self.canvas.HoloLabel["text"] = "-"

        print(
            f"changes detected: TotalGRDPTS: {totalQPPts} | totalCreditHrs: {totalCreditHrs}"
        )

    def ResetTable(self, canvas):
        global row_count
        row_count = 0
        if Table.widget_list:
            for row in Table.widget_list:
                for widget in row:
                    if isinstance(widget, int):
                        canvas.delete(
                            widget
                        )  # canvas.delete(if), canvas id bukan object
                    else:
                        widget.destroy()  # if object, button

        Table.widget_list = []  # Reset all constructor
        Table.entry_list = []

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(__file__).parent / Path("./assets/gpa_calculator")
        return ASSETS_PATH / Path(path)
