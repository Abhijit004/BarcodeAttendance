from customtkinter import *
from PIL import Image
from popupMessage import OpenPopup

set_default_color_theme("assets/gui-theme.json")


class AddClass(CTk):
    def __init__(self, depts, subjcodes):
        super().__init__()
        self.geometry("645x434")
        self.resizable(0, 0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

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
        self.greet.grid(row=0, column=0, padx=15, pady=(30, 0), sticky="ew")
        self.byline = CTkLabel(
            self.frame,
            text="Register a class in the database",
            font=CTkFont(size=18, slant="italic"),
        )
        self.byline.grid(row=1, column=0)

        # teacher ID
        self.ask = CTkFrame(self.frame, fg_color="transparent")
        self.ask.grid(row=2, column=0, pady=(20, 0), padx=50, sticky="ew")
        self.teacherid = CTkLabel(
            self.ask, text="Teacher ID", font=CTkFont(size=14, weight="normal")
        )
        self.teacheridInput = CTkEntry(
            self.frame,
            placeholder_text="enter the teacher ID",
            font=CTkFont(family="consolas", weight="bold"),
        )
        self.teacherid.grid(row=0, column=0, padx=0, pady=0)
        self.teacheridInput.grid(row=3, column=0, padx=50, pady=0, sticky="ew")

        # department
        self.ask = CTkFrame(self.frame, fg_color="transparent")
        self.ask.grid(row=4, column=0, pady=(0, 0), padx=50, sticky="ew")
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
        self.deptInput.grid(row=5, column=0, padx=50, pady=0, sticky="ew")

        # semester-subject-clubber
        self.semsubj = CTkFrame(self.frame, fg_color="transparent")
        self.semsubj.grid(row=6, column=0, pady=(0, 30), padx=50, sticky="ew")

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
        self.registerbutton.grid(row=10, column=0, padx=50, pady=(0, 0), sticky="ew")

        self.switch_var = StringVar(value="off")
        self.theme = CTkSwitch(
            self.frame,
            text="Light Mode",
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
            command=self.themeswap,
        )
        self.theme.grid(row=11, column=0, padx=(170, 0), pady=(45, 0))

    def themeswap(self):
        set_appearance_mode("dark" if self.switch_var.get() == "off" else "light")

    def registercheck(self):
        OpenPopup("Hello", "This is a success")


app = AddClass(
    ["IT", "CST", "EE", "MET", "MIN", "MECH", "CIVIL", "AM"],
    ["IT2201", "IT2202", "IT2203", "IT2204", "IT2205"],
)
app.mainloop()
