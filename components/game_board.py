import tkinter as tk
from .abstract_frame import AbstractFrame

class GameBoard(tk.Frame, AbstractFrame):
    def __init__(self, parent, rows=8, columns=8, size=32, color1='white', color2='gray'):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}
        self.pieceImages = {
            'p1p': tk.PhotoImage(file='resources/p1p.png'),
            'p1k': tk.PhotoImage(file='resources/p1k.png'),
            'p2p': tk.PhotoImage(file='resources/p2p.png'),
            'p2k': tk.PhotoImage(file='resources/p2k.png')
        }

        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=rows*size, height=columns*size)
        self.canvas.bind('<Configure>', self.onResize)
        self.canvas.bind('<Button-1>', self.onClick)

    def addPiece(self, name, pType, row, column):
        self.pieces[name] = (row, column, pType)
        self.canvas.create_image(0, 0, image=self.pieceImages[pType], tags=(name, 'piece'), anchor='c')
        self.movePiece(name, row, column)

    def movePiece(self, name, row, column):
        x0 = column * self.size + int(self.size / 2)
        y0 = row * self.size + int(self.size / 2)

        self.canvas.coords(name, x0, y0)

    def updatePieceType(self, name, pType):
        self.canvas.delete(name)
        self.addPiece(name, pType, self.pieces[name][0], self.pieces[name][1])

    def onResize(self, event):
        newXSize = int((event.width - 1) / self.columns)
        newYSize = int((event.height - 1) / self.rows)
        color = self.color2

        self.size = min(newXSize, newYSize)
        self.canvas.delete('tile')

        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2

            for col in range(self.columns):
                x0 = col * self.size
                y0 = row * self.size
                x1 = x0 + self.size
                y1 = y0 + self.size

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags='tile')
                color = self.color1 if color == self.color2 else self.color2

        for name in self.pieces:
            self.movePiece(name, self.pieces[name][0], self.pieces[name][1])

        self.canvas.tag_raise('piece')
        self.canvas.tag_lower('tile')

    def onClick(self, event):
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        result = [int(y / self.size), int(x / self.size)]

        if result[0] > 7:
            result[0] = 7
        elif result[1] > 7:
            result[1] = 7

        self.parent.gameInstance.onClick(result)

    def show(self):
        self.pack(side='top', fill='both', expand=True, padx=4, pady=4)
        self.canvas.pack(side='top', fill='both', expand=True, padx=2, pady=2)

    def hide(self):
        self.pack_forget()
        self.canvas.pack_forget()
