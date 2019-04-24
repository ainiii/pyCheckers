import tkinter as tk
from .abstract_frame import AbstractFrame

class MainMenu(tk.Frame, AbstractFrame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.subtitle = tk.Label(self, text="Choose").grid(row=0, column=0)

        self.hostOption = tk.Button(self, text="Host").grid(row=1, column=0)
        self.joinOption = tk.Button(self, text="Join").grid(row=2, column=0)
        self.offlineOption = tk.Button(self, text="Offline").grid(row=3, column=0)

        self.hostTxt = tk.Entry(self, width=10).grid(row=0, column=2)
        self.portTxt = tk.Entry(self, width=10).grid(row=0, column=3)

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()
