import customtkinter as CustomTk
from PIL import Image

from Attendance import take_attendance
from report import *

# default settings and constants
CustomTk.set_appearance_mode("System")
CustomTk.set_default_color_theme("gui-theme.json")
dept_options = ["IT", "CST", "EE", "MET", "MIN", "MECH", "CIVIL", "AM"]
subj_options = ["IT2201", "IT2202", "IT2203", "IT2204", "IT2205"]
sem_options = [str(i) for i in range(1, 9)]


def changeTheme(theme):
    CustomTk.set_appearance_mode(theme)


def button_callback():
    print("button pressed")


app = CustomTk.CTk()
app.title("Barcode Attendance")
app.geometry("645x434")
app.resizable(0, 0)

# left pane
leftpane = CustomTk.CTkFrame(app, width=200, height=900)
leftpane.grid(row=0, column=0, padx=10, pady=(10, 6), rowspan=3, sticky="nsew")

heading = CustomTk.CTkLabel(
    leftpane,
    font=CustomTk.CTkFont(size=30, weight="bold"),
    text="Class Details",
)
heading.grid(row=0, column=0, pady=5)
dept = CustomTk.CTkLabel(leftpane, text="Department")
dept.grid(row=1, column=0, padx=20, pady=(5, 0))
deptcb = CustomTk.CTkOptionMenu(
    leftpane,
    values=dept_options,
    width=200,
    dropdown_fg_color=["#3a7ebf", "#1f538d"],
    dropdown_hover_color=["#234567", "#1e2c40"],
    dropdown_text_color=["#D5D9DE", "#D5D9DE"],
)
deptcb.grid(row=2, column=0, padx=20, pady=0)

sem = CustomTk.CTkLabel(leftpane, text="Semester")
sem.grid(row=3, column=0, padx=20, pady=(5, 0))
semcb = CustomTk.CTkOptionMenu(
    leftpane,
    values=sem_options,
    width=200,
    dropdown_fg_color=["#3a7ebf", "#1f538d"],
    dropdown_hover_color=["#234567", "#1e2c40"],
    dropdown_text_color=["#ffffff", "#ffffff"],
)
semcb.grid(row=4, column=0, padx=20, pady=0)

subj = CustomTk.CTkLabel(leftpane, text="Subject Code")
subj.grid(row=5, column=0, padx=20, pady=(5, 0))
subjcb = CustomTk.CTkOptionMenu(
    leftpane,
    values=subj_options,
    width=200,
    dropdown_fg_color=["#3a7ebf", "#1f538d"],
    dropdown_hover_color=["#234567", "#1e2c40"],
    dropdown_text_color=["#ffffff", "#ffffff"],
)
subjcb.grid(row=6, column=0, padx=20, pady=(0, 10))
deptcb.set("")
semcb.set("")
subjcb.set("")

theme = CustomTk.CTkLabel(leftpane, text="Appearance Mode")
theme.grid(row=10, column=0, padx=20, pady=(108, 0))
themecb = CustomTk.CTkOptionMenu(
    leftpane, values=["System", "Dark", "Light"], width=200, command=changeTheme
)
themecb.grid(row=11, column=0, padx=20, pady=(0, 10))


# functions
def on_escape(event):
    event.widget.destroy()


def open_popup(title, message):
    popup = CustomTk.CTkToplevel()
    popup.title(title)
    popup.geometry("250x150")
    popup.focus_force()
    popup.grab_set()
    popup.resizable(0, 0)
    popup.grid_columnconfigure(0, weight=1)
    popup.grid_rowconfigure(0, weight=1)

    f = CustomTk.CTkFrame(popup)
    f.grid(row=0, column=0)
    label = CustomTk.CTkLabel(f, text=message)
    label.grid(row=0, column=0, padx=8, pady=8)

    close_button = CustomTk.CTkButton(f, text="Okay", command=popup.destroy)
    close_button.grid(row=1, column=0, padx=8, pady=8)
    popup.bind("<Escape>", on_escape)
    popup.wait_window()


def onclick_attendance():
    dept_text = deptcb.get()
    subject_text = subjcb.get()
    semester_text = semcb.get()
    if not all([dept_text, subject_text, semester_text]):
        if not dept_text:
            empty = "department"
        elif not subject_text:
            empty = "subject"
        elif not semester_text:
            empty = "semester"
        open_popup("ALERT", empty + " field is empty!")
    else:
        open_popup("Starting...", "Attendance taking started\nPress 'g' to Stop.")
        print("ATTENDANCE TAKING STARTED\n")
        status, message = take_attendance(
            dept_text, "sem" + semester_text, subject_text
        )
        open_popup(status, message)

def onclick_class_report():
    dept_text = deptcb.get()
    subject_text = subjcb.get()
    semester_text = semcb.get()
    if not all([dept_text, subject_text, semester_text]):
        if not dept_text:
            empty = "department"
        elif not subject_text:
            empty = "subject"
        elif not semester_text:
            empty = "semester"
        open_popup("ALERT", empty + " field is empty!")
    else:
        print("STARTED CLASS REPORT GENERATION...")
        status, message = grandReport(dept_text, "sem" + semester_text, subject_text)
        open_popup(status, message)


def onclick_day_report():
    date_text = reportdate.get()
    dept_text = deptcb.get()
    subject_text = subjcb.get()
    semester_text = semcb.get()
    if not all([date_text, dept_text, subject_text, semester_text]):
        if not dept_text:
            empty = "department"
        elif not subject_text:
            empty = "subject"
        elif not semester_text:
            empty = "semester"
        elif not date_text:
            empty = "date"
        open_popup("ALERT", empty + " field is empty!")
    else:
        print("REPORT GENERATION FOR DATE:", date_text)
        status, message = generateReport(
            dept_text, "sem" + semester_text, subject_text, date_text
        )
        open_popup(status, message)


# image
logo = Image.open("Image.png")

img = CustomTk.CTkFrame(app, fg_color=["#4a98e1", "#3a79bf"])
img.grid(row=0, column=1, padx=(0, 5), pady=(10, 3), sticky="nsew", columnspan=2)
img.grid_columnconfigure(0, weight=1)
img.grid_rowconfigure(0, weight=1)
imgcontent = CustomTk.CTkLabel(
    img,
    text="",
    image=CustomTk.CTkImage(light_image=logo, dark_image=logo, size=(300, 100)),
)
imgcontent.grid(row=0, column=0, padx=5, pady=8)

# right pane
# attendance taking
attendance = CustomTk.CTkFrame(app)
attendance.grid(row=1, column=1, sticky="nsew", padx=(0, 5), pady=5)
attenddesc = CustomTk.CTkLabel(
    attendance,
    text="A video will start capturing\nthe barcode/QRcode of\nstudents' IDs in real time.\n",
    justify="left",
)
attenddesc.grid(row=0, column=0, padx=5, pady=5)
takeattendance = CustomTk.CTkButton(
    attendance, text="START", command=onclick_attendance, height=34, font=CustomTk.CTkFont(weight="bold")
)
takeattendance.grid(row=1, column=0, pady=(0, 5))

# report generation
GrandReport = CustomTk.CTkFrame(app)
GrandReport.grid(row=1, column=2, sticky="nsew", padx=(5, 5), pady=5)
GrandReportdesc = CustomTk.CTkLabel(
    GrandReport,
    text="Generate a grand report for\na respective class throughout\nthe semester\n",
    justify="left",
)
GrandReportdesc.grid(row=0, column=0, padx=5, pady=5)
getGrandReport = CustomTk.CTkButton(
    GrandReport, text="GRAND REPORT", command=onclick_class_report, height=34, font=CustomTk.CTkFont(weight="bold")
)
getGrandReport.grid(row=1, column=0, pady=(0, 5))

# report generation
report = CustomTk.CTkFrame(app)
report.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=(0, 5), pady=5)
reportdesc = CustomTk.CTkLabel(
    report,
    text="Generate attendance report for a class in a particular day\n",
    justify="left",
)
reportdesc.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

datedesc = CustomTk.CTkLabel(report, text="date (e.g. 2024-01-01)")
datedesc.grid(row=1, column=0)
reportdate = CustomTk.CTkEntry(
    report,
    placeholder_text="yyyy-mm-dd",
    placeholder_text_color="#3191DC",
    border_color="#3191DC",
    font=CustomTk.CTkFont(family="consolas"), height=34
)
reportdate.grid(row=2, column=0, pady=(0, 5))

getreport = CustomTk.CTkButton(report, text=" REPORT", command=onclick_day_report, height=34, font=CustomTk.CTkFont(weight="bold"))
getreport.grid(row=2, column=1, pady=(0, 5))
app.mainloop()
