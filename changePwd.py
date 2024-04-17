from customtkinter import *
from popupMessage import OpenPopup
import json

set_default_color_theme("assets/gui-theme.json")


class changePwd(CTkFrame):
    def __init__(self, parent, tid):
        super().__init__(parent)
        self._fg_color = "transparent"
        self._border_width=0
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.tid = tid
        self.parent = parent

        # parent pane
        self.frame = CTkFrame(self, corner_radius=10, fg_color=["#dbdbdb", "#2b2b2b"])
        self.frame.grid(row=0, column=0, sticky="nsew", padx=(3, 3), pady=3)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # old pwd
        self.ask = CTkFrame(self.frame, fg_color="transparent")
        self.ask.grid(row=0, column=0, pady=(5, 0), padx=30, sticky="ew")
        self.old = CTkLabel(
            self.ask, text="Old password", font=CTkFont(size=14, weight="normal")
        )
        self.oldInput = CTkEntry(
            self.frame,
            placeholder_text="password",
            font=CTkFont(family="consolas", weight="bold"),
            show="."
        )
        self.old.grid(row=0, column=0, padx=5, pady=0)
        self.oldInput.grid(row=1, column=0, padx=30, pady=0, sticky="ew")

        #new pwd
        self.ask = CTkFrame(self.frame, fg_color="transparent")
        self.ask.grid(row=2, column=0, pady=(0, 0), padx=30, sticky="ew")
        self.new = CTkLabel(
            self.ask, text="New password", font=CTkFont(size=14, weight="normal")
        )
        self.newInput = CTkEntry(
            self.frame,
            placeholder_text="password",
            font=CTkFont(family="consolas", weight="bold"),
            show = "."
        )
        self.new.grid(row=1, column=0, padx=5, pady=(10, 0))
        self.newInput.grid(row=3, column=0, padx=30, pady=0, sticky="ew")
        
        #submit changes
        self.changebutton = CTkButton(
            self.frame,
            text="CHANGE",
            font=CTkFont(size=16, weight="bold"),
            height=30,
            corner_radius=6,
            command=self.change_password,
        )
        self.changebutton.grid(row=4, column=0, padx=30, pady=(30, 20), sticky="ew")

    # def themeswap(self):
    #     set_appearance_mode("dark" if self.switch_var.get() == "off" else "light")

    def change_password(self):
        new = self.newInput.get()
        old = self.oldInput.get()

        f = open("teacher.json", "r+")
        data = json.load(f)
        old_pwd = data[self.tid]["password"]

        if not old:
            OpenPopup("ALERT", "Please enter old\npassword.")
            return
        if not new:
            OpenPopup("ALERT", "Please enter new\npassword")
            return

        if old_pwd != old:
            OpenPopup("ERROR", "Incorrect old password.\nPlease try again.")
            return
        if old==new:
            OpenPopup("ERROR", "Please choose a password\nother than current one.")
            return
        
        data[self.tid]["password"] = new
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        f.close()
        OpenPopup("SUCCESS", "Password changed. Use new\npassword the next time you login.")
        self.parent.destroy()
