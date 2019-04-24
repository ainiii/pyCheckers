import tkinter as tk
from components.main_menu import MainMenu

if __name__ == '__main__':
    window = tk.Tk()
    window.title("pyCheckers")

    menu = MainMenu(window)
    menu.show()

    window.mainloop()
