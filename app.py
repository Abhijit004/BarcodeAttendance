from customtkinter import *
from PIL import Image
from popupMessage import OpenPopup
from Attendance import take_attendance, approveLeave
from report import *
from addClass import AddClass
from changePwd import changePwd

set_default_color_theme("assets/gui-theme.json")
dept_options = ["IT", "CST", "EE", "MET", "MIN", "MECH", "CIVIL", "AM"]
subj_options = ["IT2201", "IT2202", "IT2203", "IT2204", "IT2205"]
sem_options = [str(i) for i in range(1, 9)]


class App(CTk):
    def __init__(self, teacher, tid):
        super().__init__()
        self.title("Barcode Attendance")
        self.geometry("645x434+400+150")
        self.resizable(0, 0)
        self.teacher = teacher
        self.tid = tid

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
        self.dept.grid(row=1, column=0, padx=20, pady=(10, 0))
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
        self.changepwd = CTkButton(
            self.leftpane,
            text="CHANGE PASSWORD",
            height=35,
            font=CTkFont(weight="bold"),
            state="normal",
            text_color_disabled="#152d47",
            command=self.changepwd
        )
        self.changepwd.grid(row=8, column=0, padx=20,pady=(54, 10), sticky="ew")
        self.adduser = CTkButton(
            self.leftpane,
            text="ADD USER",
            height=35,
            font=CTkFont(weight="bold"),
            state="normal" if teacher["is-admin"] else "disabled",
            text_color_disabled="#152d47",
            command=self.addNewUser,
        )
        self.adduser.grid(row=9, column=0, padx=20, sticky="ew")

        self.switch_var = StringVar(value="off")
        self.switch = CTkSwitch(
            self.leftpane,
            text="Light mode",
            command=self.changeTheme,
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
        )
        self.switch.grid(row=10, column=0, padx=20, pady=(10, 10))

        # image
        self.logoLight = Image.open("assets/main-light.png")
        self.logoDark = Image.open("assets/main-dark.png")

        self.img = CTkFrame(self, fg_color="transparent")
        self.img.grid(
            row=0, column=1, padx=(0, 5), pady=(10, 3), sticky="nsew", columnspan=2
        )
        self.img.grid_columnconfigure(0, weight=1)
        self.img.grid_rowconfigure(0, weight=1)
        self.imgcontent = CTkLabel(
            self.img,
            text="",
            image=CTkImage(
                light_image=self.logoLight, dark_image=self.logoDark, size=(380, 144)
            ),
        )
        self.imgcontent.grid(row=0, column=0)

        # right pane
        # attendance taking
        self.attendance = CTkFrame(self)
        self.attendance.grid(row=1, column=1, sticky="nsew", padx=(0, 5), pady=5)
        self.attenddesc = CTkLabel(
            self.attendance,
            text="Start camera to capture\nbarcode/QRcode of students'\nIDs in real time.\n",
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
            text="Generate class attendance\nreport throughout the\nsemester\n",
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
        self.appln = CTkFrame(self)
        self.appln.grid(
            row=2, column=1, columnspan=2, sticky="nsew", padx=(0, 5), pady=5
        )
        self.applndesc = CTkLabel(
            self.appln,
            text="Approve a Leave application for a student\n",
            justify="left",
        )
        self.applndesc.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky="ew")

        # daterange
        self.daterange = CTkFrame(self.appln, fg_color="transparent")
        self.daterange.grid(row=1, column=0, sticky="nsew", rowspan=2, padx=(5, 5))

        self.start = CTkLabel(
            self.daterange, text="from: ", font=CTkFont(family="consolas")
        )
        self.start.grid(row=0, column=0)
        self.startdate = CTkEntry(
            self.daterange,
            placeholder_text="yyyy-mm-dd",
            placeholder_text_color="#3191DC",
            border_color="#3191DC",
            font=CTkFont(family="consolas", weight="bold"),
            height=34,
            corner_radius=5,
            border_width=2,
            state="normal" if teacher["is-admin"] else "disabled"
        )
        self.startdate.grid(row=0, column=1)

        self.end = CTkLabel(
            self.daterange, text="To:   ", font=CTkFont(family="consolas")
        )
        self.end.grid(row=1, column=0, pady=(10, 0))
        self.enddate = CTkEntry(
            self.daterange,
            placeholder_text="yyyy-mm-dd",
            placeholder_text_color="#3191DC",
            border_color="#3191DC",
            font=CTkFont(family="consolas", weight="bold"),
            height=34,
            corner_radius=5,
            border_width=2,
            state="normal" if teacher["is-admin"] else "disabled"
        )
        self.enddate.grid(row=1, column=1, pady=(10, 0))

        self.sid = CTkEntry(
            self.appln,
            placeholder_text="Student ID",
            placeholder_text_color="#3191DC",
            border_color="#3191DC",
            font=CTkFont(family="consolas", weight="bold"),
            height=34,
            corner_radius=5,
            border_width=2,
            state="normal" if teacher["is-admin"] else "disabled"
        )
        self.sid.grid(row=1, column=1)

        self.approvebtn = CTkButton(
            self.appln,
            text="APPROVE",
            command=self.approve,
            height=34,
            font=CTkFont(weight="bold"),
            state="normal" if teacher["is-admin"] else "disabled",
            text_color_disabled="#152d47",
        )
        self.approvebtn.grid(row=2, column=1, pady=(10, 0))

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
                print(valid, existing)
                if valid == existing:
                    break
            else:
                OpenPopup(
                    "INVALID",
                    "Given class does not exist\nfor you. Select a different\ncombination.",
                )
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

    # def onclick_day_report(self):
    #     date_text = self.reportdate.get()
    #     dept_text = self.deptcb.get()
    #     subject_text = self.subjcb.get()
    #     semester_text = self.semcb.get()
    #     if not all([date_text, dept_text, subject_text, semester_text]):
    #         if not dept_text:
    #             empty = "department"
    #         elif not subject_text:
    #             empty = "subject"
    #         elif not semester_text:
    #             empty = "semester"
    #         elif not date_text:
    #             empty = "date"
    #         OpenPopup("ALERT", empty + " field is empty!")
    #     else:
    #         print("REPORT GENERATION FOR DATE:", date_text)
    #         status, message = generateReport(
    #             dept_text, "sem" + semester_text, subject_text, date_text
    #         )
    #         OpenPopup(status, message)

    def addNewUser(self):
        add_class_window = CTkToplevel(self, fg_color=["#F1F3F8", "#1E2024"])
        add_class_window.title("Add Class Window")
        add_class_window.geometry("650x435+450+200")
        add_class_window.resizable(0, 0)
        add_class_window.grid_columnconfigure(0, weight=1)
        add_class_window.grid_rowconfigure(0, weight=1)
        add_class_app = AddClass(add_class_window)
        add_class_app.grid(row=0, column=0)
        add_class_app.grab_set()
        add_class_window.lift()
        add_class_window.focus_force()

    def changepwd(self):
        change_pwd_window = CTkToplevel(self, fg_color=["#F1F3F8", "#1E2024"])
        change_pwd_window.title("Change password")
        change_pwd_window.geometry("+450+200")

        change_pwd_window.resizable(0, 0)
        change_pwd_window.grid_columnconfigure(0, weight=1)
        change_pwd_window.grid_rowconfigure(0, weight=1)
        change_pwd_app = changePwd(change_pwd_window, self.tid)
        change_pwd_app.grid(row=0, column=0)
        change_pwd_app.grab_set()
        change_pwd_window.lift()
        change_pwd_window.focus_force()

    def changeTheme(self):
        if self.switch_var.get() == "on":
            set_appearance_mode("light")
            self.switch.configure(text="Dark mode")
        else:
            set_appearance_mode("dark")
            self.switch.configure(text="Light mode")

    def approve(self):
        fields = {
            "Student ID": self.sid.get(),
            "Department": self.deptcb.get(),
            "Subject": self.subjcb.get(),
            "Semester": "sem" + self.semcb.get(),
            "Start date": self.startdate.get(),
            "End date": self.enddate.get(),
        }
        for fld in fields:
            if fields[fld] == "":
                OpenPopup("ALERT", f"{fld} field is empty!")
                return
        status, msg = approveLeave(
            fields["Student ID"],
            fields["Department"],
            fields["Semester"],
            fields["Subject"],
            fields["Start date"],
            fields["End date"],
        )
        OpenPopup(status, msg)


sample = {
    "password": "5678",
    "name": "Mr. Abcd Efg",
    "is-admin": True,
    "class": [["IT", "4", "IT9999"], ["ETC", "7", "ET1102"], ["CST", "6", "CST2107"]],
}

# app = App(sample, "Soumyajit")
# app.mainloop()
