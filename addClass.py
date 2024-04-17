from customtkinter import *
from PIL import Image
from popupMessage import OpenPopup
import json

set_default_color_theme("assets/gui-theme.json")


class AddClass(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self._fg_color = "transparent"
        # self.geometry("645x434+400+150")
        # self.resizable(0, 0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        depts = ["IT", "CST", "ME", "AE", "CE", "ME", "MN"]
        subjcodes = ["IT2201", "IT2202", "IT2203", "IT2204"]

        # left-pic
        self.img = Image.open("assets/img-register.png")
        self.leftlabel = CTkLabel(
            self,
            text="",
            image=CTkImage(size=(320, 420), light_image=self.img, dark_image=self.img),
            corner_radius=3,
        )
        self.leftlabel.grid(row=0, column=0)

        # right pane
        self.frame = CTkFrame(self, corner_radius=10)
        self.frame.grid(row=0, column=1, sticky="nsew", padx=(0, 5), pady=5)
        self.frame.grid_columnconfigure(0, weight=1)

        # greet
        self.greet = CTkLabel(
            self.frame, text="Add a Class", font=CTkFont(size=32, weight="bold")
        )
        self.greet.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="ew")
        self.byline = CTkLabel(
            self.frame,
            text="Register a class in the database",
            font=CTkFont(size=18, slant="italic"),
        )
        self.byline.grid(row=1, column=0)

        # teacherid-isadmin clubber
        self.clubber = CTkFrame(self.frame, fg_color="transparent")
        self.clubber.grid(row=2, column=0, pady=(5, 0), padx=(50, 0), sticky="ew")
        # teacher ID
        self.ask = CTkFrame(self.clubber, fg_color="transparent")
        self.ask.grid(row=0, column=0, pady=0, padx=0, sticky="ew")
        self.teacherid = CTkLabel(
            self.ask, text="Teacher ID", font=CTkFont(size=14, weight="normal")
        )
        self.teacheridInput = CTkEntry(
            self.clubber,
            placeholder_text="enter ID",
            font=CTkFont(family="consolas", weight="bold"),
            width=120,
        )
        self.teacherid.grid(row=0, column=0, padx=0, pady=0)
        self.teacheridInput.grid(row=1, column=0, padx=0, pady=0, sticky="ew")

        self.isadmin = StringVar(value="off")
        self.admin = CTkSwitch(
            self.clubber,
            text="Admin",
            variable=self.isadmin,
            onvalue="on",
            offvalue="off",
        )
        self.admin.grid(row=1, column=1, padx=(10, 0), pady=0)

        # teacher name
        self.ask = CTkFrame(self.frame, fg_color="transparent")
        self.ask.grid(row=4, column=0, pady=(5, 0), padx=50, sticky="ew")
        self.tname = CTkLabel(
            self.ask, text="Teacher Name", font=CTkFont(size=14, weight="normal")
        )
        self.tnameInput = CTkEntry(
            self.frame,
            placeholder_text="Enter full name",
            font=CTkFont(family="consolas", weight="bold"),
        )
        self.tname.grid(row=0, column=0, padx=0, pady=0)
        self.tnameInput.grid(row=5, column=0, padx=50, pady=0, sticky="ew")

        # department
        self.ask = CTkFrame(self.frame, fg_color="transparent")
        self.ask.grid(row=6, column=0, pady=(0, 0), padx=50, sticky="ew")
        self.dept = CTkLabel(
            self.ask, text="Department", font=CTkFont(size=14, weight="normal")
        )
        self.deptInput = CTkOptionMenu(
            self.frame,
            values=depts,
            width=200,
            dropdown_fg_color=["#3a7ebf", "#1f538d"],
            dropdown_hover_color=["#234567", "#1e2c40"],
            dropdown_text_color=["#D5D9DE", "#D5D9DE"],
        )
        self.deptInput.set("")
        self.dept.grid(row=0, column=0, padx=0, pady=0)
        self.deptInput.grid(row=7, column=0, padx=50, pady=0, sticky="ew")

        # semester-subject-clubber
        self.semsubj = CTkFrame(self.frame, fg_color="transparent")
        self.semsubj.grid(row=10, column=0, pady=(0, 30), padx=50, sticky="ew")

        # semester
        self.ask = CTkFrame(self.semsubj, fg_color="transparent")
        self.ask.grid(row=0, column=0, pady=(0, 0), sticky="ew")
        self.sem = CTkLabel(
            self.ask, text="Semester", font=CTkFont(size=14, weight="normal")
        )
        self.semInput = CTkOptionMenu(
            self.semsubj,
            values=[str(i) for i in range(1, 9)],
            dropdown_fg_color=["#3a7ebf", "#1f538d"],
            dropdown_hover_color=["#234567", "#1e2c40"],
            dropdown_text_color=["#D5D9DE", "#D5D9DE"],
            width=105,
        )
        self.semInput.set("")
        self.sem.grid(row=0, column=0, padx=0, pady=0)
        self.semInput.grid(row=1, column=0, padx=0, pady=0)

        # subject code
        self.ask = CTkFrame(self.semsubj, fg_color="transparent")
        self.ask.grid(row=0, column=1, pady=(0, 0), padx=(5, 0), sticky="ew")
        self.sub = CTkLabel(
            self.ask, text="Subject Code", font=CTkFont(size=14, weight="normal")
        )
        self.subInput = CTkOptionMenu(
            self.semsubj,
            values=subjcodes,
            dropdown_fg_color=["#3a7ebf", "#1f538d"],
            dropdown_hover_color=["#234567", "#1e2c40"],
            dropdown_text_color=["#D5D9DE", "#D5D9DE"],
            width=105,
        )
        self.subInput.set("")
        self.sub.grid(row=0, column=0, padx=0, pady=0)
        self.subInput.grid(row=1, column=1, padx=(5, 0), pady=0)

        self.registerbutton = CTkButton(
            self.frame,
            text="REGISTER",
            font=CTkFont(size=16, weight="bold"),
            height=30,
            corner_radius=6,
            command=self.registercheck,
        )
        self.registerbutton.grid(row=12, column=0, padx=50, pady=(0, 0), sticky="ew")

        self.switch_var = StringVar(value="off")
        self.theme = CTkSwitch(
            self.frame,
            text="Light Mode",
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
            command=self.themeswap,
        )
        self.theme.grid(row=13, column=0, padx=(170, 0), pady=(25, 0))

    def themeswap(self):
        set_appearance_mode("dark" if self.switch_var.get() == "off" else "light")

    def registercheck(self):
        tid = self.teacheridInput.get()
        tname = self.tnameInput.get()
        dept = self.deptInput.get()
        subject = self.subInput.get()
        sem = self.semInput.get()
        if not tid:
            OpenPopup("ALERT", "Teacher ID missing")
            return
        if not tname:
            OpenPopup("ALERT", "Teacher name missing")
            return
        if not dept:
            OpenPopup("ALERT", "Department missing")
            return
        if not subject:
            OpenPopup("ALERT", "Subject missing")
            return
        if not sem:
            OpenPopup("ALERT", "Semester missing")
            return

        f = open("teacher.json", "r+")
        allData = json.load(f)

        newData = {"password": "t123", "name": tname, "class": [[dept, sem, subject]]}

        if tid not in allData:
            allData[tid] = newData
        else:
            allData[tid]["class"].append([dept, sem, subject])
        f.seek(0)
        json.dump(allData, f)
        f.truncate()
        f.close()
        OpenPopup("SUCCESS", "Teacher data added\nSuccessfully!")


# d = AddClass()
# d.mainloop()
