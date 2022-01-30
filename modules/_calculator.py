from pathlib import Path
from tkinter import ttk, Canvas, Entry, PhotoImage, StringVar, Button, IntVar
import threading
import time
from functools import partial
from math import modf
import numpy as np

# Internal module
from modules._dataprocessing import get_subjects, isfloat, dataLength, retrieveData
from modules._customize import CustomizeSubject


class Calculator(Canvas):
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
        self.GUI()

    def GUI(self):
        self.create_text(
            394.0,
            18.0,
            anchor="nw",
            text="Subject",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14 * -1),
        )

        # Future Update
        self.create_text(
            719.0,
            9.0,
            anchor="nw",
            text="True Balance",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14 * -1),
        )

        # Future Update
        self.create_text(
            817.0,
            4.0,
            anchor="nw",
            text="TM",
            fill="#FFFFFF",
            font=("Montserrat Bold", 7 * -1),
        )

        self.create_text(
            401.0,
            80.0,
            anchor="nw",
            text="Grade",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.create_text(
            244.0,
            145.0,
            anchor="nw",
            text="Distribution",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12 * -1),
        )

        self.create_text(
            685.0,
            145.0,
            anchor="nw",
            text="Estimate",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12 * -1),
        )

        self.create_text(
            35.0,
            182.0,
            anchor="nw",
            text="Coursework",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 12 * -1),
        )

        self.create_text(
            182.0,
            182.0,
            anchor="nw",
            text="Total Mark",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 12 * -1),
        )

        self.create_text(
            305.0,
            170.0,
            anchor="nw",
            text="         Total\nPercentage (%)",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 12 * -1),
        )

        self.create_text(
            455.0,
            182.0,
            anchor="nw",
            text="Actual Mark",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 12 * -1),
        )

        self.create_text(
            615.0,
            182.0,
            anchor="nw",
            text="Min. Mark",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 12 * -1),
        )

        self.create_text(
            728.0,
            175.0,
            anchor="nw",
            text="          Min.\nPercentage (%)",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 12 * -1),
        )

        # Here, we are creating table system ( 10 x 6 ) of widget by using 2D list.
        # We can use loop for creating array of widget but the process is a bit tedious and a quite hard to read so we stick to one by one writing.
        # column: 0 -> coursework, 1 -> totalmark, 2 -> totalpercentage percentage, 3 -> Actual mark (Entry box), 4 -> estimate mark, 5 -> estimate totalpercentage

        self.row = []
        column = []

        # Here, we store all entry value into list to be imported in core module
        self.EntryVal = []
        for i in range(9):
            self.EntryVal.append(StringVar())
        #######################  row 0  #######################

        column.append(
            self.create_text(
                53.0,
                218.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                209.0,
                218.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                340.0,
                218.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        self.entry_image = PhotoImage(file=self.relative_to_assets("entry.png"))
        entry_bg_1 = self.create_image(492.5, 226.0, image=self.entry_image)

        entry_0 = Entry(
            self,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            textvariable=self.EntryVal[0],
            justify="center",
            state="readonly",
            readonlybackground="#383535",
        )
        entry_0.place(x=475.0, y=213.0, width=35.0, height=24.0)
        column.append(entry_0)

        column.append(
            self.create_text(
                642.0,
                218.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                766.0,
                218.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        self.row.append(column)

        #######################  row 1  #######################

        # Reset Column
        column = []

        column.append(
            self.create_text(
                53.0,
                266.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                211.0,
                266.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                340.0,
                266.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        entry_bg_2 = self.create_image(492.5, 274.0, image=self.entry_image)
        entry_2 = Entry(
            self,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            textvariable=self.EntryVal[1],
            justify="center",
            state="readonly",
            readonlybackground="#383535",
        )
        entry_2.place(x=474.0, y=262.0, width=37.0, height=22.0)
        column.append(entry_2)

        column.append(
            self.create_text(
                643.0,
                266.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                765.0,
                266.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        self.row.append(column)

        #######################  row 2  #######################

        # Reset Column
        column = []

        column.append(
            self.create_text(
                53.0,
                312.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                210.0,
                312.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                340.0,
                312.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        entry_bg_3 = self.create_image(492.5, 320.0, image=self.entry_image)
        entry_3 = Entry(
            self,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            textvariable=self.EntryVal[2],
            justify="center",
            state="readonly",
            readonlybackground="#383535",
        )
        entry_3.place(x=474.0, y=308.0, width=37.0, height=22.0)
        column.append(entry_3)

        column.append(
            self.create_text(
                642.0,
                312.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                765.0,
                312.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        self.row.append(column)

        #######################  row 3  #######################

        # Reset Column
        column = []

        column.append(
            self.create_text(
                53.0,
                357.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                210.0,
                357.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                340.0,
                357.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        entry_bg_4 = self.create_image(492.5, 366.0, image=self.entry_image)
        entry_4 = Entry(
            self,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            textvariable=self.EntryVal[3],
            justify="center",
            state="readonly",
            readonlybackground="#383535",
        )
        entry_4.place(x=475.0, y=353.0, width=35.0, height=24.0)
        column.append(entry_4)

        column.append(
            self.create_text(
                644.0,
                357.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                766.0,
                357.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        self.row.append(column)

        #######################  row 4  #######################

        # Reset Column
        column = []

        column.append(
            self.create_text(
                53.0,
                406.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                209.0,
                406.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                340.0,
                406.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        entry_bg_5 = self.create_image(492.5, 413.5, image=self.entry_image)
        entry_5 = Entry(
            self,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            textvariable=self.EntryVal[4],
            justify="center",
            state="readonly",
            readonlybackground="#383535",
        )
        entry_5.place(x=472.5, y=403.0, width=35.0, height=24.0)
        column.append(entry_5)

        column.append(
            self.create_text(
                643.0,
                406.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                767.0,
                406.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        self.row.append(column)

        #######################  row 5  #######################

        # Reset Column
        column = []

        column.append(
            self.create_text(
                53.0,
                451.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                209.0,
                451.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                340.0,
                451.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        entry_bg_6 = self.create_image(492.5, 459.0, image=self.entry_image)
        entry_6 = Entry(
            self,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            textvariable=self.EntryVal[5],
            justify="center",
            state="readonly",
            readonlybackground="#383535",
        )
        entry_6.place(x=474.0, y=447.0, width=37.0, height=22.0)
        column.append(entry_6)

        column.append(
            self.create_text(
                643.0,
                451.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                766.0,
                451.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        self.row.append(column)

        #######################  row 6  #######################

        # Reset Column
        column = []

        column.append(
            self.create_text(
                53.0,
                498.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                209.0,
                498.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                340.0,
                498.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        entry_bg_7 = self.create_image(492.5, 506.5, image=self.entry_image)
        entry_7 = Entry(
            self,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            textvariable=self.EntryVal[6],
            justify="center",
            state="readonly",
            readonlybackground="#383535",
        )
        entry_7.place(x=474.5, y=494.0, width=36.0, height=23.0)
        column.append(entry_7)

        column.append(
            self.create_text(
                642.0,
                498.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                765.0,
                498.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        self.row.append(column)

        #######################  row 7  #######################

        # Reset Column
        column = []

        column.append(
            self.create_text(
                53.0,
                544.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                209.0,
                544.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                340.0,
                544.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        entry_bg_8 = self.create_image(492.5, 552.0, image=self.entry_image)
        entry_8 = Entry(
            self,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            textvariable=self.EntryVal[7],
            justify="center",
            state="readonly",
            readonlybackground="#383535",
        )
        entry_8.place(x=474.0, y=540.0, width=37.0, height=22.0)
        column.append(entry_8)

        column.append(
            self.create_text(
                642.0,
                544.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                765.0,
                544.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        self.row.append(column)

        #######################  row 8  #######################

        # Reset Column
        column = []

        column.append(
            self.create_text(
                53.0,
                587.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                208.0,
                587.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                340.0,
                587.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        entry_bg_9 = self.create_image(491.5, 595.0, image=self.entry_image)
        entry_9 = Entry(
            self,
            bd=0,
            bg="#383535",
            highlightthickness=0,
            textvariable=self.EntryVal[8],
            justify="center",
            state="readonly",
            readonlybackground="#383535",
        )
        entry_9.place(x=473.0, y=583.0, width=37.0, height=22.0)
        column.append(entry_9)

        column.append(
            self.create_text(
                641.0,
                587.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        column.append(
            self.create_text(
                764.0,
                587.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 12 * -1),
            )
        )

        self.row.append(column)

        ####################### Total Row  #######################
        # This is a total row where we calculate sum of all column

        self.total_row = []

        self.create_text(
            53.0,
            627.0,
            anchor="nw",
            text="Total",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12 * -1),
        )

        self.total_row.append(
            self.create_text(
                209.0,
                627.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Bold", 12 * -1),
            )
        )

        self.total_row.append(
            self.create_text(
                342.0,
                627.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Bold", 12 * -1),
            )
        )

        self.total_row.append(
            self.create_text(
                486.0,
                629.0,
                anchor="nw",
                justify="center",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Bold", 12 * -1),
            )
        )

        self.total_row.append(
            self.create_text(
                642.0,
                627.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Bold", 12 * -1),
            )
        )

        self.total_row.append(
            self.create_text(
                765.0,
                627.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Bold", 12 * -1),
            )
        )

        #######################  Result Row  #######################

        self.create_text(
            371.0,
            678.0,
            anchor="nw",
            justify="center",
            text="Achievable Grade",
            fill="#FFFFFF",
            font=("Montserrat Regular", 10 * -1),
        )

        self.create_text(  ## Grade Points, excluded for now
            215.0,
            680.0,
            anchor="nw",
            # text="Grade Points",
            fill="#FFFFFF",
            font=("Montserrat Regular", 10 * -1),
        )

        self.create_text(  ## Effort Level, excluded for now
            557.0,
            678.0,
            anchor="nw",
            # text="Effort Level",
            fill="#FFFFFF",
            font=("Montserrat Regular", 10 * -1),
        )

        self.create_rectangle(574.0, 182.0, 574.0, 648.0, fill="#FFFFFF", outline="")

        # Special case for result row, we use dictionary to access the widget for readability and ease of use.

        self.result = {"grade": [], "pointer": [], "effort": []}

        self.result["grade"].append(
            self.create_text(
                396.0,
                688.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 48 * -1),
            )
        )

        self.result["pointer"].append(
            self.create_text(
                236.0,
                701.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 18 * -1),
            )
        )

        self.result["effort"].append(
            self.create_text(
                566.0,
                701.0,
                anchor="nw",
                text="",
                fill="#FFFFFF",
                font=("Montserrat Regular", 18 * -1),
            )
        )

        #######################  User Input Widget  #######################

        # True Balance Switch (Future Upgrade)
        self.true_switch_status = IntVar()
        true_switch = ttk.Checkbutton(
            self,
            style="Switch.TCheckbutton",
            variable=self.true_switch_status,
            onvalue=1,
            offvalue=0,
            command=self.calculateEstimate,
        )
        true_switch.place(x=742.0, y=35.0)

        # Subject Combobox
        subject_list = get_subjects()
        self.subject_combobox = ttk.Combobox(
            self, values=subject_list, justify="center"
        )
        self.subject_combobox["state"] = "readonly"
        self.subject_combobox.place(x=326.0, y=44.0, width=200, height=30)

        # Grade Combobox
        grade_list = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "E", "F"]
        self.grade_combobox = ttk.Combobox(
            self, values=grade_list, justify="center", font="Arial 9 bold"
        )
        self.grade_combobox["state"] = "disabled"
        self.grade_combobox.place(x=393.0, y=105.0, width=80.0, height=27.0)

        # Plus Button
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        button_4 = Button(
            self,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: CustomizeSubject(self),
            relief="flat",
        )
        button_4.place(x=531.0, y=50.0, width=31.0, height=23.0)

        # Warning Label
        self.warning_label = self.create_text(
            8.0, 6.0, anchor="nw", text="", fill="#FF0000", font=("Roboto", 12 * -1)
        )

        # Widget bind
        self.subject_combobox.bind("<<ComboboxSelected>>", self.updateSubject)
        self.subject_combobox.bind("<1>", self.fetch)
        self.grade_combobox.bind(
            "<1>",
            lambda event: self.warningInfo(
                "Please choose subject first", self.warning_label
            )
            if str(event.widget["state"]) == "disabled"
            else None,
        )
        self.grade_combobox.bind("<<ComboboxSelected>>", self.calculateEstimate)

        for i in range(9):
            self.EntryVal[i].trace(
                "w", partial(self.EntryChanges, i, self.EntryVal[i])
            )  # ni pass index (i) tp x tau la sbb kt changeestimate da leh access ui index
            self.row[i][3].bind(
                "<1>",
                lambda event: self.warningInfo(
                    "Unavailable! No subject or coursework assigned", self.warning_label
                )
                if self.row[i][3]["state"] != "normal"
                else None,
            )  # click

    def fetch(self, event=None):
        self.subject_combobox["values"] = get_subjects()

    def calculateEstimate(self, event=None):
        if event is not None:  # function is called by grade combobox changes
            grade = event.widget.get()
        else:  # function is called by entry box changes
            grade = self.grade_combobox.get()  # get current grade
            # print(grade)
        gradeMark = {
            "A": 80,
            "A-": 75,
            "B+": 70,
            "B": 65,
            "B-": 60,
            "C+": 55,
            "C": 50,
            "C-": 47,
            "D+": 44,
            "D": 40,
            "E": 25,
            "F": 0,
        }

        TotalFullMarkCoursework_NonSpecified = 0
        TotalMarkSpecified = 0
        MarkSpecifiedRowIndex = []
        df = retrieveData()
        i = 0

        # Ini hanya untuk ambik user inputted value
        for ind in range(dataLength()):
            if df.iloc[ind, 0] == self.subject_combobox.get():
                if isfloat(
                    self.EntryVal[i].get()
                ):  # Kita check kalau entry ade markah ke x (dan decimal only)
                    MarkSpecifiedRowIndex.append(
                        i
                    )  # kita take note row mane yang user tulis markah, kita store row index ngan markah die
                    TotalMarkSpecified += float(self.EntryVal[i].get())
                    self.changeElementByRow(
                        i,
                        estimatemark="-",
                        estimatepercentage=(
                            TotalMarkSpecified
                            / float(self.getMark(i))
                            * float(self.getPercent(i))
                        ),
                    )
                else:
                    TotalFullMarkCoursework_NonSpecified += float(df.iloc[ind, 3])
                i += 1
        self.changeResult("grade", self.grade_combobox.get())
        # print(self.getTotalMark())
        # Get proportion val
        proportion = self.balancingAlgoritm(
            (gradeMark[grade] / 100) * float(self.getTotalMark()),
            TotalMarkSpecified,
            TotalFullMarkCoursework_NonSpecified,
        )
        proportion = round(proportion, 4)

        # Calculation
        actualTotalEstimateMark = TotalMarkSpecified
        True_Balance_list = []
        True_Balance_converted = []
        o = 0
        i = 0
        if self.true_switch_status.get() == 1:
            # True Balance Algorithm
            for ind in range(dataLength()):
                if df.iloc[ind, 0] == self.subject_combobox.get():
                    if o not in MarkSpecifiedRowIndex:
                        mark = float(df.iloc[ind, 3])
                        True_Balance_list.append(mark)
                    o += 1

            True_Balance_converted = self.True_Balance_Algorithm(
                TotalFullMarkCoursework_NonSpecified * proportion, True_Balance_list
            )
            o = 0
            for ind in range(dataLength()):
                if df.iloc[ind, 0] == self.subject_combobox.get():
                    if i not in MarkSpecifiedRowIndex:
                        minPercent = (
                            True_Balance_converted[o] / float(self.getMark(i))
                        ) * float(self.getPercent(i))
                        self.changeElementByRow(
                            i,
                            estimatemark=round(True_Balance_converted[o], 2),
                            estimatepercentage=round(minPercent, 2),
                        )
                        actualTotalEstimateMark = (
                            sum(True_Balance_converted) + TotalMarkSpecified
                        )
                        o += 1
                    i += 1
        # Basic Algorithm
        else:
            for ind in range(dataLength()):
                if df.iloc[ind, 0] == self.subject_combobox.get():
                    if i not in MarkSpecifiedRowIndex:
                        mark = float(df.iloc[ind, 3])
                        minMark = mark * proportion
                        minPercent = (minMark / float(self.getMark(i))) * float(
                            self.getPercent(i)
                        )
                        self.changeElementByRow(
                            i,
                            estimatemark=round(minMark, 2),
                            estimatepercentage=round(minPercent, 2),
                        )
                        actualTotalEstimateMark += minMark
                    i += 1

        totalEstimatePercent = (
            actualTotalEstimateMark / float(self.getTotalMark())
        ) * 100
        self.changeTotalRow(
            actualmark=TotalMarkSpecified,
            estimatemark=round(actualTotalEstimateMark, 2),
            estimatepercentage=round(totalEstimatePercent, 2),
        )

    def resetWidget(self):
        for i in range(0, 9):  # Total row count = 9
            self.changeElementByRow(
                i,
                coursework="",
                totalmark="",
                totalpercentage="",
                estimatemark="",
                estimatepercentage="",
                entry_state=False,
            )

    def updateSubject(self, event=None):
        df = retrieveData()
        self.resetWidget()

        self.grade_combobox["state"] = "readonly"
        totalMark = 0
        totalPercentage = 0
        i = 0
        for ind in range(dataLength()):
            if df.iloc[ind, 0] == self.subject_combobox.get():
                if df.iloc[ind, 1] != "null":
                    totalPercentage += float(df.iloc[ind, 2])
                    totalMark += float(df.iloc[ind, 3])
                    self.changeElementByRow(
                        i,
                        coursework=df.iloc[ind, 1],
                        totalpercentage=float(df.iloc[ind, 2]),
                        totalmark=float(df.iloc[ind, 3]),
                        entry_state=True,
                        estimatemark=0,
                        estimatepercentage=0,
                    )
                    i += 1
        self.changeTotalRow(totalmark=totalMark, totalpercentage=totalPercentage)

    def balancingAlgoritm(
        self,
        gradeTargetMark,
        TotalMark_UserSpecified,
        TotalFullMarkCoursework_NonSpecified,
    ):
        proportion = (
            gradeTargetMark - TotalMark_UserSpecified
        ) / TotalFullMarkCoursework_NonSpecified
        return proportion

    def changeElementByRow(
        self,
        row_val,
        coursework=None,
        totalmark=None,
        totalpercentage=None,
        estimatemark=None,
        estimatepercentage=None,
        entry_state=None,
    ):
        if coursework is None:
            coursework = self.itemcget(self.row[row_val][0], "text")
        if totalmark is None:
            totalmark = self.itemcget(self.row[row_val][1], "text")
        if totalpercentage is None:
            totalpercentage = self.itemcget(self.row[row_val][2], "text")
        if estimatemark is None:
            estimatemark = self.itemcget(self.row[row_val][4], "text")
        if estimatepercentage is None:
            estimatepercentage = self.itemcget(self.row[row_val][5], "text")
        if entry_state is None:
            state_txt = self.row[row_val][3]["state"]
        elif entry_state is True:
            state_txt = "normal"
        else:
            state_txt = "readonly"

        self.row[row_val][3].config(state=state_txt, readonlybackground="#383535")
        self.itemconfig(self.row[row_val][0], text=coursework)
        self.itemconfig(self.row[row_val][1], text=totalmark)
        self.itemconfig(self.row[row_val][2], text=totalpercentage)
        self.itemconfig(self.row[row_val][4], text=estimatemark)
        self.itemconfig(self.row[row_val][5], text=estimatepercentage)

    def True_Balance_Algorithm(self, total, distribution):
        leftover = 0.0
        distributed_total = []
        distribution_sum = sum(distribution)
        for weight in distribution:
            weight = float(weight)
            leftover, weighted_value = modf(
                weight * total / distribution_sum + leftover
            )
            distributed_total.append(weighted_value)
        distributed_total[-1] = round(
            distributed_total[-1] + leftover
        )  # mitigate round off errors
        return list(np.float_(distributed_total))

    def changeTotalRow(
        self,
        totalmark=None,
        totalpercentage=None,
        actualmark=None,
        estimatemark=None,
        estimatepercentage=None,
    ):
        if totalmark is None:
            totalmark = self.itemcget(self.total_row[0], "text")
        if totalpercentage is None:
            totalpercentage = self.itemcget(self.total_row[1], "text")
        if actualmark is None:
            actualmark = self.itemcget(self.total_row[2], "text")
        if estimatemark is None:
            estimatemark = self.itemcget(self.total_row[3], "text")
        if estimatepercentage is None:
            estimatepercentage = self.itemcget(self.total_row[4], "text")

        self.itemconfig(self.total_row[0], text=totalmark)
        self.itemconfig(self.total_row[1], text=totalpercentage)
        self.itemconfig(self.total_row[2], text=actualmark)
        self.itemconfig(self.total_row[3], text=estimatemark)
        self.itemconfig(self.total_row[4], text=estimatepercentage)

    def changeResult(self, key, val):
        return self.itemconfig(self.result[key], text=str(val))

    def getPercent(self, row_val):
        return self.itemcget(self.row[row_val][2], "text")

    def getMark(self, row_val):
        return self.itemcget(self.row[row_val][1], "text")

    def getTotalMark(self):
        return self.itemcget(self.total_row[0], "text")

    def elapsedTimeThread(
        self,
        widget,
    ):
        time.sleep(3)
        self.itemconfigure(widget, text="")

    def warningInfo(self, msg, widget):
        self.itemconfigure(widget, text=msg)

        t1 = threading.Thread(target=self.elapsedTimeThread, args=(self.warning_label,))
        t1.start()

    def EntryChanges(self, key, var, *args):
        if val := var.get():
            if isfloat(val):
                self.row[key][3].config(fg="#FFFFFF")
                if float(val) > float(self.getMark(key)):
                    self.warningInfo(
                        "Input can't be greater than the total mark!",
                        self.warning_label,
                    )
                    self.row[key][3].config(fg="#FF0000")
                else:
                    self.row[key][3].config(fg="#FFFFFF")
            else:
                self.warningInfo("Input can only be in digit only!", self.warning_label)
                self.row[key][3].config(fg="#FF0000")
        self.calculateEstimate()

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(__file__).parents[1] / Path("./assets/calculator")
        return ASSETS_PATH / Path(path)

    def share_data(self):
        return [self.EntryVal, self.subject_combobox]
