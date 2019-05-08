import tkinter as tk
from .main_menu import MainMenu

class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.mainMenu = MainMenu(self)

        self.mainMenu.show()
