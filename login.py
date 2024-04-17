from customtkinter import *
from PIL import Image
from popupMessage import OpenPopup
import json
from app import App
from pickle import dump, load

set_default_color_theme("assets/gui-theme.json")

class Login(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("645x434+400+150")
        self.resizable(0, 0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.title("Barcode Attendance")

        # left-pic
        self.img = Image.open("assets/img-login.png")
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
            self.frame, text="Welcome!", font=CTkFont(size=32, weight="bold")
        )
        self.greet.grid(row=0, column=0, padx=(0,65), pady=(50, 0), sticky="ew")
        self.byline = CTkLabel(
            self.frame,
            text="Please enter your details",
            font=CTkFont(size=18, slant="italic"),
        )
        self.byline.grid(row=1, column=0, padx=(0,15))

        self.ask = CTkFrame(self.frame, fg_color="transparent")
        self.ask.grid(row=2, column=0, pady=(30, 0), padx=50, sticky="ew")

        self.teacherid = CTkLabel(
            self.ask, text="Teacher ID", font=CTkFont(size=14, weight="normal")
        )
        self.teacheridInput = CTkEntry(
            self.frame,
            placeholder_text="enter your teacher ID",
            font=CTkFont(family="consolas", weight="bold"),
        )
        self.teacherid.grid(row=0, column=0, padx=0, pady=0)
        self.teacheridInput.grid(row=3, column=0, padx=50, pady=0, sticky="ew")

        self.ask = CTkFrame(self.frame, fg_color="transparent")
        self.ask.grid(row=4, column=0, pady=(0, 0), padx=50, sticky="ew")
        self.password = CTkLabel(
            self.ask, text="Password", font=CTkFont(size=14, weight="normal")
        )
        self.passwordInput = CTkEntry(
            self.frame,
            placeholder_text="enter password",
            show="·",
            font=CTkFont(family="consolas", weight="bold"),
        )
        self.password.grid(row=0, column=0, padx=0, pady=0)
        self.passwordInput.grid(row=5, column=0, padx=50, pady=0, sticky="ew")

        self.loginbutton = CTkButton(
            self.frame,
            text="LOGIN",
            font=CTkFont(size=16, weight="bold"),
            height=30,
            corner_radius=6,
            command = self.logincheck
        )
        self.loginbutton.grid(row=6, column=0, padx=50, pady=(30, 0), sticky="ew")

        self.switch_var = StringVar(value="off")
        self.theme = CTkSwitch(
            self.frame,
            text="Light Mode",
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
            command=self.themeswap,
        )
        self.theme.grid(row=7, column=0, pady=(70, 0), padx=(180, 0))

    def themeswap(self):
        set_appearance_mode("dark" if self.switch_var.get() == "off" else "light")
    def logincheck(self):
        tid = self.teacheridInput.get()
        pwd = self.passwordInput.get()
        if not tid:
            OpenPopup("ALERT", "Teacher ID missing!")
            return
        elif not pwd:
            OpenPopup("ALERT", "Passsword missing!")
            return
        
        f = open("bin.teacher", "rb")
        teacher = load(f)
        f.close()


        if tid not in teacher:
            OpenPopup("ERROR", f"Teacher ID {tid} does not exist!")
            return
        print(teacher)
        if teacher[tid]["password"] != pwd:
            OpenPopup("ERROR", "Wrong password. Please try again.")
            return 

        self.destroy()
        run = App(teacher[tid])
        run.mainloop()
        
app = Login()
app.mainloop()
