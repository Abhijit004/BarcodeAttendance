from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Label
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
from Attendance import take_attendance
from report import *


OUTPUT_PATH = Path(__file__).resolve().parent
# ASSETS_PATH = OUTPUT_PATH.parent / "frontend" / "assets"
# print(OUTPUT_PATH)
# print(ASSETS_PATH)


def relative_to_assets(path: str) -> Path:
    return OUTPUT_PATH / "assets" / Path(path)


window = Tk()
window.geometry("700x550")
window.configure(bg = "#FFFFFF")

def on_escape(event):
    event.widget.destroy()

def open_popup(title, message):
    popup = Toplevel(window)
    popup.title(title)
    popup.geometry("250x100")
    popup.focus_force()
    popup.grab_set()

    label = Label(popup, text=message)
    label.pack(pady=10)

    close_button = Button(popup, text="OK", command=popup.destroy, width=10, height = 2)
    close_button.pack()
    
    popup.bind("<Escape>", on_escape)
    popup.wait_window()


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 550,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0,
    55.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    350.0,
    55.0,
    image=image_image_2
)

canvas.create_rectangle(
    28.0,
    137.0,
    340.0,
    524.0,
    fill="#FFFFFF",
    outline="#7e7e7e"
    )

canvas.create_rectangle(
    360.0,
    137.0,
    672.0,
    524.0,
    fill="#fff",
    outline="#7e7e7e",
    )

image_image_3 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_3 = canvas.create_image(
    184.0,
    164.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    516.0,
    164.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    134.0,
    164.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    85.0,
    228.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    394.0,
    228.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    69.0,
    296.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    76.0,
    364.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    440.0,
    164.0,
    image=image_image_10
)

department_options = ["IT", "CST", "EE", "MET", "MIN", "MECH", "CIVIL", "AM"]
department = Combobox(
    values=department_options,
    style="TCombobox",
    font=("Arial", 16),
    state="readonly"
)
department.place(
    x=41.0,
    y=237.0,
    width=287.0,
    height=33.0
)

date = DateEntry(window, state = "readonly", width=15, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
date.place(x=377.0, y=237.0, width=282.0, height=33.0)

subject_options = ["IT2201", "IT2202", "IT2203", "IT2204", "IT2205"]
subject = Combobox(
    values=subject_options,
    style="TCombobox",
    font=("Arial", 16),
    state="readonly"
)
subject.place(
    x=41.0,
    y=305.0,
    width=287.0,
    height=33.0
)

semester_options = [str(i) for i in range(1, 9)]
semester = Combobox(
    values=semester_options,
    style="TCombobox",
    font=("Arial", 16),
    state="readonly"
)
semester.place(x=41.0, y=373.0, width=287.0, height=33.0)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

def onclick_attendance():
    dept_text = department.get()
    subject_text = subject.get()
    semester_text = semester.get()
    if not all([dept_text, subject_text, semester_text]):
        if not dept_text:empty = "department"
        elif not subject_text:empty = "subject"
        elif not semester_text:empty = "semester"
        open_popup("ALERT", empty+ " field is empty!")
    else:
        print("ATTENDANCE TAKING STARTED\n")
        take_attendance(dept_text, "sem"+semester_text, subject_text)

attendance = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=onclick_attendance,
    relief="flat",
    cursor="hand2"
)
attendance.place(
    x=41.0,
    y=458.0,
    width=134.0,
    height=45.0
)

def onclick_class_report():
    dept_text = department.get()
    subject_text = subject.get()
    semester_text = semester.get()
    if not all([dept_text, subject_text, semester_text]):
        if not dept_text:empty = "department"
        elif not subject_text:empty = "subject"
        elif not semester_text:empty = "semester"
        open_popup("ALERT", empty+" field is empty!")
    else:
        print("STARTED CLASS REPORT GENERATION...")
        grandReport(dept_text, "sem"+semester_text, subject_text)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
class_report = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=onclick_class_report,
    relief="flat",
    cursor="hand2"
)
class_report.place(
    x=377.0,
    y=438.0,
    width=282.0009765625,
    height=65.0
)

def onclick_day_report():
    date_text = date.get()
    dept_text = department.get()
    subject_text = subject.get()
    semester_text = semester.get()
    if not all([date_text, dept_text, subject_text, semester_text]):
        if not dept_text:empty = "department"
        elif not subject_text:empty = "subject"
        elif not semester_text:empty = "semester"
        elif not date_text: empty = "date"
        open_popup("ALERT", empty+ " field is empty!")
    else:
        print("REPORT GENERATION FOR DATE:", date_text)
        generateReport(dept_text, "sem"+semester_text, subject_text, date_text)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
day_report = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=onclick_day_report,
    relief="flat",
    cursor="hand2"
)
day_report.place(
    x=377.0,
    y=295.0,
    width=282.0,
    height=45.0
)
window.resizable(False, False)
window.mainloop()
