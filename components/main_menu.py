import tkinter as tk
from .abstract_frame import AbstractFrame

class MainMenu(tk.Frame, AbstractFrame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.hostOption = tk.Button(self, text="Host", command=lambda : self.host(self.hostInput.get(), self.portInput.get()))
        self.joinOption = tk.Button(self, text="Join", command=lambda : self.join(self.hostInput.get(), self.portInput.get()))
        self.offlineOption = tk.Button(self, text="Offline", command=lambda: self.offline())

        self.hostTxt = tk.Label(self, text="Ip address:")
        self.portTxt = tk.Label(self, text="Port:")
        self.hostInput = tk.Entry(self)
        self.portInput = tk.Entry(self)

        self.infoTxt = tk.Label(self, text="pyCheckers")

        self.hostOption.grid(row=0, column=2, padx=5, sticky='nesw')
        self.joinOption.grid(row=1, column=2, padx=5, sticky='nesw')
        self.offlineOption.grid(row=2, column=2, padx=5, sticky='nesw')
        self.hostTxt.grid(row=0, column=0, sticky='w')
        self.portTxt.grid(row=1, column=0, sticky='w')
        self.hostInput.grid(row=0, column=1)
        self.portInput.grid(row=1, column=1)
        self.infoTxt.grid(row=2, column=0, columnspan=2, sticky='w')

    def host(self, host, port):
        self.parent.hostGame(host, port)

    def join(self, host ,port):
        self.parent.joinGame(host, port)

    def offline(self):
        self.parent.offlineGame()

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()
