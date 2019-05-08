import tkinter as tk
from components.main_frame import MainFrame

if __name__ == '__main__':
    window = tk.Tk()
    window.title("pyCheckers")

    mainFrame = MainFrame(window)
    mainFrame.pack(fill=tk.BOTH, expand=1)

    window.mainloop()
