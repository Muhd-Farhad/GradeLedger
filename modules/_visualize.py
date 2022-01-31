from re import L
import pandas as pd

from tkinter import Canvas
import numpy as np
import matplotlib
import mplcyberpunk as mplcyberpunk
from pathlib import Path

matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import matplotlib.pyplot as plt

from modules._dataprocessing import get_subjects, get_coursework, get_all_coursework

plt.style.use("cyberpunk")
for param in ["text.color", "axes.labelcolor", "xtick.color", "ytick.color"]:
    plt.rcParams[param] = "0.9"  # very light grey
for param in ["figure.facecolor", "axes.facecolor", "savefig.facecolor"]:
    plt.rcParams[param] = "#181829"  # bluish dark grey
colors = [
    "#08F7FE",  # teal/cyan
    "#FE53BB",  # pink
    "#F5D300",  # yellow
    "#00ff41",  # matrix green
]


plt.rcParams.update({"font.size": 8})  # Change font size

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


class Visualization(Canvas):
    def __init__(self, master, data):
        super().__init__(
            master=master,
            bg="#1C1C1C",
            height=763,
            width=850,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.widget_inside = []
        self.place(x=0, y=0)
        self.EntryVal = data[0]
        self.subject_combobox = data[1]
        self.subject = ""
        self.GUI()

    def GUI(self):
        self.place(x=0, y=0)
        t0 = self.create_text(
            380.0,
            16.0,
            anchor="nw",
            text="Dashboard",
            justify="center",
            fill="#FFFFFF",
            font=("Montserrat SemiBold", 18 * -1),
        )

        # Rectangle background for total subject
        self.create_rectangle(187.0, 548.0, 418.0, 699.0, fill="#8b05f2", outline="")

        # Rectangle background for total coursework
        self.create_rectangle(431.0, 548.0, 662.0, 699.0, fill="#0534b3", outline="")

        self.subjects_text = self.create_text(
            280,
            585.0,
            anchor="nw",
            justify="center",
            text="3",
            fill="#FFFFFF",
            font=("Montserrat Bold", 64 * -1),
        )

        self.courseworks_text = self.create_text(
            520.0,
            585.0,
            anchor="nw",
            text="26",
            fill="#FFFFFF",
            font=("Montserrat Bold", 64 * -1),
        )

        self.create_text(
            250.0,
            557.0,
            anchor="nw",
            text="Total Subjects",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.create_text(
            480.0,
            557.0,
            anchor="nw",
            text="Total Courseworks",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.create_rectangle(156.0, 339.0, 688.0, 531.0, fill="#69c7fa", outline="")

        self.PerformanceChart()
        self.SubjectCourseworkChart()

    def TotalRow(self):
        total_courseworks = len(get_all_coursework())
        total_subject = len(get_subjects())
        self.itemconfig(self.courseworks_text, text=str(total_courseworks))
        self.itemconfig(self.subjects_text, text=str(total_subject))

    def PerformanceChart(self):

        self.subject = self.subject_combobox.get()
        assessment_mark = []
        for i in range(len(self.EntryVal)):
            if len(self.EntryVal[i].get()) > 0:
                assessment_mark.append(float(self.EntryVal[i].get()))

        if len(assessment_mark) > 2:

            self.create_rectangle(133.0, 79.0, 716.0, 316.0, fill="#7d19ff", outline="")

            assessment_mark = [float(i) / sum(assessment_mark) for i in assessment_mark]

            self.df = pd.DataFrame({"A": assessment_mark})
            print(self.df)
            f = Figure(figsize=(5.81, 2.35), dpi=100)
            self.ax = f.add_subplot(111)
            self.df.plot(marker="o", label="PMF", color=colors)

            n_shades = 10
            diff_linewidth = 1.05
            alpha_value = 0.3 / n_shades
            for n in range(1, n_shades + 1):
                self.df.plot(
                    marker="o",
                    linewidth=2 + (diff_linewidth * n),
                    alpha=alpha_value,
                    legend=False,
                    ax=self.ax,
                    color=colors,
                )
            # Color the areas below the lines:
            for column, color in zip(self.df, colors):
                self.ax.fill_between(
                    x=self.df.index,
                    y1=self.df[column].values,
                    y2=[0] * len(self.df),
                    color=color,
                    alpha=0.1,
                )
            title = f"{self.subject} Performance"
            self.ax.set_ylim([0, 1])
            self.ax.set_title(title, fontsize=9)
            self.ax.set_ylabel("Mark (Normalized)")
            self.ax.grid(color="#2A3459")
            self.canvas_1 = FigureCanvasTkAgg(f, master=self)
            self.canvas_1.draw()
            self.canvas_1.get_tk_widget().place(x=134.0, y=80.0)
        else:
            self.create_rectangle(133.0, 79.0, 716.0, 316.0, fill="#171717", outline="")
            self.create_text(
                320.0,
                180.0,
                anchor="nw",
                justify="center",
                text="Not enough data.\nPlease fill in at least 3 coursework",
                fill="#FFFFFF",
                font=("Montserrat", 12 * -1),
            )

    def SubjectCourseworkChart(self):
        f = Figure(figsize=(5.3, 1.9), dpi=100)
        ax = f.add_subplot(111)

        subjects = get_subjects()
        all_courseworks = []
        coursework = []
        for i in subjects:
            x = get_coursework(i)
            coursework = []
            for o in x:
                coursework.append(o[2])
            all_courseworks.append(coursework)

        sum_courseworks = []
        for i in all_courseworks:
            sum_courseworks.append(len(i))

        ind = np.arange(5)  # the x locations for the groups
        width = 0.5

        rects1 = ax.bar(subjects, sum_courseworks, width)
        # self.df.set_xlabel("X")
        # self.df.set_ylabel('Normalized')
        # self.df.set_title('Performance')
        ax.set_title("Courseworks Distribution", fontsize=9)
        # ax.set_ylabel('Mark (Normalized)')
        # ax.grid(color='#2A3459')

        self.canvas_2 = FigureCanvasTkAgg(f, master=self)
        self.canvas_2.draw()
        self.canvas_2.get_tk_widget().place(x=157.0, y=340.0)

    def Refresh(self):
        self.TotalRow()
        self.PerformanceChart()
        self.SubjectCourseworkChart()
