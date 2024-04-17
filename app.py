from customtkinter import *
from PIL import Image
from popupMessage import OpenPopup

from Attendance import take_attendance
from report import *
from addClass import AddClass

set_default_color_theme("assets/gui-theme.json")
dept_options = ["IT", "CST", "EE", "MET", "MIN", "MECH", "CIVIL", "AM"]
subj_options = ["IT2201", "IT2202", "IT2203", "IT2204", "IT2205"]
sem_options = [str(i) for i in range(1, 9)]


class App(CTk):
    def __init__(self, teacher, isAdmin=1):
        super().__init__()
        self.title("Barcode Attendance")
        self.geometry("645x434+400+150")
        self.resizable(0, 0)
        self.teacher = teacher

        # Setting dropdown data
        dept, sem, subj = set(), set(), set()
        for i in self.teacher["class"]:
            dept.add(i[0])
            sem.add(i[1])
            subj.add(i[2])
        
        dept_options = sorted(dept)
        sem_options = sorted(sem)
        subj_options = sorted(subj)

        # left pane
        self.leftpane = CTkFrame(self, width=200, height=900)
        self.leftpane.grid(
            row=0, column=0, padx=10, pady=(10, 6), rowspan=3, sticky="nsew"
        )

        self.heading = CTkLabel(
            self.leftpane,
            font=CTkFont(size=20, weight="bold"),
            text=f"Welcome\n{teacher['name']}",
        )
        self.heading.grid(row=0, column=0)
        self.dept = CTkLabel(self.leftpane, text="Department")
        self.dept.grid(row=1, column=0, padx=20, pady = (10, 0))
        self.deptcb = CTkOptionMenu(
            self.leftpane,
            values=dept_options,
            width=200,
            dropdown_fg_color=["#3a7ebf", "#1f538d"],
            dropdown_hover_color=["#234567", "#1e2c40"],
            dropdown_text_color=["#fff", "#fff"],
        )
        self.deptcb.grid(row=2, column=0, padx=20, pady=0)

        self.sem = CTkLabel(self.leftpane, text="Semester")
        self.sem.grid(row=3, column=0, padx=20)
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
        self.subj.grid(row=5, column=0, padx=20)
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

        # set_appearance_mode("light")
        self.adduser = CTkButton(
            self.leftpane,
            text="ADD USER",
            height=35,
            font=CTkFont(weight="bold"),
            state="normal" if isAdmin else "disabled",
            text_color_disabled="#152d47",
            command = self.addNewUser
        )
        self.adduser.grid(row=8, column=0, padx=20, pady=(84, 10), sticky="ew")

        self.switch_var = StringVar(value="off")
        self.switch = CTkSwitch(
            self.leftpane,
            text="Light mode",
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
            text="CLASS REPORT",
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
            text="Generate   attendance report for a class in a particular day\n",
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
            corner_radius=5,
            border_width=2,
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
            valid = f"{dept_text} {semester_text} {subject_text}"
            for triplet in self.teacher["class"]:
                existing = " ".join(triplet)
                if valid !=existing:
                    OpenPopup("INVALID", "Given class does not exist\nfor you. Select a different\ncombination.")
                    return



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

    def addNewUser(self):
        add_class_window = CTkToplevel(self)
        add_class_window.title("Add Class Window")
        add_class_window.geometry("645x434+450+200")
        add_class_window.resizable(0, 0)
        add_class_app = AddClass(add_class_window)
        add_class_app.grid(row=0, column=0)
        add_class_app.grab_set()
        add_class_window.lift()
        add_class_window.focus_force()

        # Instantiate AddClass window within the Toplevel window


    def changeTheme(self):
        if self.switch_var.get() == "on":
            set_appearance_mode("light")
            self.switch.configure(text = "Dark mode")
        else:
            set_appearance_mode("dark")
            self.switch.configure(text = "Light mode")


sample = {
        "password": "1234",
        "name": "Mr. Prasun Ghosal",
        "class":[
            ["IT", "4", "IT2203"],
            ["CST", "6", "CS1102"],
            ["IT", "6", "IT2157"]
        ]
    }

app = App(sample)
app.mainloop()
