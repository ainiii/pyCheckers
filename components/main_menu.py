import tkinter as tk
from .abstract_frame import AbstractFrame

class MainMenu(tk.Frame, AbstractFrame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.hostOption = tk.Button(self, text="Host").grid(row=0, column=2, padx=5, sticky='nesw')
        self.joinOption = tk.Button(self, text="Join").grid(row=1, column=2, padx=5, sticky='nesw')
        self.offlineOption = tk.Button(self, text="Offline").grid(row=2, column=2, padx=5, sticky='nesw')

        self.hostTxt = tk.Label(self, text="Ip address:").grid(row=0, column=0, sticky='w')
        self.portTxt = tk.Label(self, text="Port:").grid(row=1, column=0, sticky='w')
        self.hostInput = tk.Entry(self).grid(row=0, column=1)
        self.portInput = tk.Entry(self).grid(row=1, column=1)

        self.infoTxt = tk.Label(self, text="Placeholder").grid(row=2, column=0, columnspan=2, sticky='w')

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()
