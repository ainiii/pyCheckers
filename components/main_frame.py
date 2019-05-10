import tkinter as tk
from .main_menu import MainMenu
from .game_board import GameBoard

class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.mainMenu = MainMenu(self)
        self.gameBoard = GameBoard(self)

        #self.mainMenu.show()
        self.gameBoard.show()
