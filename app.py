from customtkinter import *
from PIL import Image
from popupMessage import OpenPopup

from Attendance import take_attendance
from report import *

set_default_color_theme("assets/gui-theme.json")
dept_options = ["IT", "CST", "EE", "MET", "MIN", "MECH", "CIVIL", "AM"]
subj_options = ["IT2201", "IT2202", "IT2203", "IT2204", "IT2205"]
sem_options = [str(i) for i in range(1, 9)]


class App(CTk):
    def __init__(self, dept_options, subj_options, sem_options, isAdmin=0):
        super().__init__()
        self.title("Barcode Attendance")
        self.geometry("645x434")
        self.resizable(0, 0)

        # left pane
        self.leftpane = CTkFrame(self, width=200, height=900)
        self.leftpane.grid(
            row=0, column=0, padx=10, pady=(10, 6), rowspan=3, sticky="nsew"
        )

        self.heading = CTkLabel(
            self.leftpane,
            font=CTkFont(size=30, weight="bold"),
            text="Class Details",
        )
        self.heading.grid(row=0, column=0, pady=5)
        self.dept = CTkLabel(self.leftpane, text="Department")
        self.dept.grid(row=1, column=0, padx=20, pady=(5, 0))
        self.deptcb = CTkOptionMenu(
            self.leftpane,
            values=dept_options,
            width=200,
            dropdown_fg_color=["#3a7ebf", "#1f538d"],
            dropdown_hover_color=["#234567", "#1e2c40"],
            dropdown_text_color=["#D5D9DE", "#D5D9DE"],
        )
        self.deptcb.grid(row=2, column=0, padx=20, pady=0)

        self.sem = CTkLabel(self.leftpane, text="Semester")
        self.sem.grid(row=3, column=0, padx=20, pady=(5, 0))
        self.semcb = CTkOptionMenu(
            self.leftpane,
            values=sem_options,
            width=200,
            dropdown_fg_color=["#3a7ebf", "#1f538d"],
            dropdown_hover_color=["#234567", "#1e2c40"],
            dropdown_text_color=["#ffffff", "#ffffff"],
        )
        self.semcb.grid(row=4, column=0, padx=20, pady=0)

        self.subj = CTkLabel(self.leftpane, text="Subject Code")
        self.subj.grid(row=5, column=0, padx=20, pady=(5, 0))
        self.subjcb = CTkOptionMenu(
            self.leftpane,
            values=subj_options,
            width=200,
            dropdown_fg_color=["#3a7ebf", "#1f538d"],
            dropdown_hover_color=["#234567", "#1e2c40"],
            dropdown_text_color=["#ffffff", "#ffffff"],
        )
        self.subjcb.grid(row=6, column=0, padx=20, pady=(0, 10))
        self.deptcb.set("")
        self.semcb.set("")
        self.subjcb.set("")

        self.adduser = CTkButton(
            self.leftpane,
            text="ADD USER",
            height=35,
            font=CTkFont(weight="bold"),
            state="normal" if isAdmin else "disabled",
            text_color_disabled="#152d47",
            # command = self.addNewUser
        )
        self.adduser.grid(row=8, column=0, padx=20, pady=(84, 10), sticky="ew")

        self.switch_var = StringVar(value="off")
        self.switch = CTkSwitch(
            self.leftpane,
            text="Light Mode",
            command=self.changeTheme,
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
        )
        self.switch.grid(row=9, column=0, padx=20, pady=(10, 10))

        # image
        self.logo = Image.open("assets/Image.png")

        self.img = CTkFrame(self, fg_color=["#4a98e1", "#3a79bf"])
        self.img.grid(
            row=0, column=1, padx=(0, 5), pady=(10, 3), sticky="nsew", columnspan=2
        )
        self.img.grid_columnconfigure(0, weight=1)
        self.img.grid_rowconfigure(0, weight=1)
        self.imgcontent = CTkLabel(
            self.img,
            text="",
            image=CTkImage(
                light_image=self.logo, dark_image=self.logo, size=(300, 100)
            ),
        )
        self.imgcontent.grid(row=0, column=0, padx=5, pady=8)

        # right pane
        # attendance taking
        self.attendance = CTkFrame(self)
        self.attendance.grid(row=1, column=1, sticky="nsew", padx=(0, 5), pady=5)
        self.attenddesc = CTkLabel(
            self.attendance,
            text="Start camera to capture\nbarcode/QRcode of\nstudents' IDs in real time.\n",
            justify="left",
        )
        self.attenddesc.grid(row=0, column=0, padx=5, pady=5)
        self.takeattendance = CTkButton(
            self.attendance,
            text="START",
            command=self.onclick_attendance,
            height=34,
            font=CTkFont(weight="bold"),
        )
        self.takeattendance.grid(row=1, column=0, pady=(0, 5))

        # report generation
        self.GrandReport = CTkFrame(self)
        self.GrandReport.grid(row=1, column=2, sticky="nsew", padx=(5, 5), pady=5)
        self.GrandReportdesc = CTkLabel(
            self.GrandReport,
            text="Generate class report \nthroughout the semester\n\n",
            justify="left",
        )
        self.GrandReportdesc.grid(row=0, column=0, padx=5, pady=5)
        self.getGrandReport = CTkButton(
            self.GrandReport,
            text="GRAND REPORT",
            command=self.onclick_class_report,
            height=34,
            font=CTkFont(weight="bold"),
        )
        self.getGrandReport.grid(row=1, column=0, pady=(0, 5))

        # report generation
        self.report = CTkFrame(self)
        self.report.grid(
            row=2, column=1, columnspan=2, sticky="nsew", padx=(0, 5), pady=5
        )
        self.reportdesc = CTkLabel(
            self.report,
            text="Generate attendance report for a class in a particular day\n",
            justify="left",
        )
        self.reportdesc.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        self.datedesc = CTkLabel(self.report, text="date (e.g. 2024-01-01)")
        self.datedesc.grid(row=1, column=0)
        self.reportdate = CTkEntry(
            self.report,
            placeholder_text="yyyy-mm-dd",
            placeholder_text_color="#3191DC",
            border_color="#3191DC",
            font=CTkFont(family="consolas"),
            height=34,
            corner_radius=12,
            border_width=3,
        )
        self.reportdate.grid(row=2, column=0, pady=(0, 5))

        self.getreport = CTkButton(
            self.report,
            text=" REPORT",
            command=self.onclick_day_report,
            height=34,
            font=CTkFont(weight="bold"),
        )
        self.getreport.grid(row=2, column=1, pady=(0, 5))

    def switch_event(self):
        print("switch toggled, current value:", self.switch_var.get())

    # functions
    def on_escape(event):
        event.widget.destroy()

    def onclick_attendance(self):
        dept_text = self.deptcb.get()
        subject_text = self.subjcb.get()
        semester_text = self.semcb.get()
        if not all([dept_text, subject_text, semester_text]):
            if not dept_text:
                empty = "department"
            elif not subject_text:
                empty = "subject"
            elif not semester_text:
                empty = "semester"
            OpenPopup("ALERT", empty + " field is empty!")
        else:
            OpenPopup("Starting...", "Attendance taking started\nPress 'g' to Stop.")
            print("ATTENDANCE TAKING STARTED\n")
            status, message = take_attendance(
                dept_text, "sem" + semester_text, subject_text
            )
            OpenPopup(status, message)

    def onclick_class_report(self):
        dept_text = self.deptcb.get()
        subject_text = self.subjcb.get()
        semester_text = self.semcb.get()
        if not all([dept_text, subject_text, semester_text]):
            if not dept_text:
                empty = "department"
            elif not subject_text:
                empty = "subject"
            elif not semester_text:
                empty = "semester"
            OpenPopup("ALERT", empty + " field is empty!")
        else:
            print("STARTED CLASS REPORT GENERATION...")
            status, message = grandReport(
                dept_text, "sem" + semester_text, subject_text
            )
            OpenPopup(status, message)

    def onclick_day_report(self):
        date_text = self.reportdate.get()
        dept_text = self.deptcb.get()
        subject_text = self.subjcb.get()
        semester_text = self.semcb.get()
        if not all([date_text, dept_text, subject_text, semester_text]):
            if not dept_text:
                empty = "department"
            elif not subject_text:
                empty = "subject"
            elif not semester_text:
                empty = "semester"
            elif not date_text:
                empty = "date"
            OpenPopup("ALERT", empty + " field is empty!")
        else:
            print("REPORT GENERATION FOR DATE:", date_text)
            status, message = generateReport(
                dept_text, "sem" + semester_text, subject_text, date_text
            )
            OpenPopup(status, message)

    def changeTheme(self):
        set_appearance_mode("light" if self.switch_var.get() == "on" else "dark")
        

# class AddNewUser(CTkToplevel):
    


app = App(dept_options, subj_options, sem_options)
app.mainloop()
