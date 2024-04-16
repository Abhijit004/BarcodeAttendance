from customtkinter import *
class OpenPopup(CTkToplevel):
    def __init__(self, title, message):
        super().__init__()
        self.title(title)
        self.geometry("250x150")
        self.focus_force()
        self.grab_set()
        self.resizable(0, 0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        f = CTkFrame(self)
        f.grid(row=0, column=0)
        label = CTkLabel(f, text=message)
        label.grid(row=0, column=0, padx=8, pady=8)

        close_button = CTkButton(f, text="Okay", command=self.destroy)
        close_button.grid(row=1, column=0, padx=8, pady=8)
        self.bind("<Escape>", self.on_escape)
        self.wait_window()
    def on_escape(self, event):
        event.widget.destroy()