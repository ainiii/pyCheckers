import tkinter as tk
import threading
import time
from .abstract_frame import AbstractFrame

class GameBoard(tk.Frame, AbstractFrame):
    def __init__(self, parent, rows=8, columns=8, size=32, color1='red', color2='blue'):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieceImages = {
            'p1p': tk.PhotoImage(file='resources/p1p.png'),
            'p1k': tk.PhotoImage(file='resources/p1k.png'),
            'p2p': tk.PhotoImage(file='resources/p2p.png'),
            'p2k': tk.PhotoImage(file='resources/p2k.png'),
            'highlight': tk.PhotoImage(file='resources/highlight.png')
        }
        self.model = False

        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=rows*size, height=columns*size)
        self.highlight = self.canvas.create_image(0, 0, image=self.pieceImages['highlight'], tags='highlight', anchor='c', state=tk.HIDDEN)
        self.lastHighlight = False
        self.canvas.bind('<Configure>', self.onResize)
        self.canvas.bind('<Button-1>', self.onClick)

    def attachModel(self, model):
        self.model = model
        UpdateThread(self, model)

    def addPiece(self, name, pType, row, column):
        x0 = column * self.size + int(self.size / 2)
        y0 = row * self.size + int(self.size / 2)

        self.canvas.create_image(x0, y0, image=self.pieceImages[pType], tags=(name, 'piece'), anchor='c')

    def movePiece(self, name, row, column):
        x0 = column * self.size + int(self.size / 2)
        y0 = row * self.size + int(self.size / 2)

        self.canvas.coords(name, x0, y0)

    def updatePieceType(self, name, pType):
        self.canvas.itemconfigure(name, image=self.pieceImages[pType])

    def removePiece(self, name):
        self.canvas.delete(name)

    def highlightPiece(self, name):
        pieceCoords = self.canvas.coords(name)
        self.canvas.coords('highlight', pieceCoords[0], pieceCoords[1])
        self.canvas.itemconfigure('highlight', state=tk.NORMAL)
        self.canvas.tag_raise('highlight')
        self.lastHighlight = name

    def removeHighlight(self):
        self.lastHighlight = False
        self.canvas.itemconfigure('highlight', state=tk.HIDDEN)

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

        if self.model:
            for piece in self.model.getPieces():
                self.movePiece(piece.name, piece.row, piece.column)

        self.canvas.tag_raise('piece')
        self.canvas.tag_lower('tile')

        if self.lastHighlight:
            self.highlightPiece(self.lastHighlight)

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

class UpdateThread(threading.Thread):
    def __init__(self, parent, model):
        threading.Thread.__init__(self)
        self.parent = parent
        self.model = model
        self.start()

    def run(self):
        while True:
            event = self.model.getNextEvent()

            if event:
                result = event.split('|')
                eType = result[0]

                if eType == 'add':
                    name, pType, row, column = result[1], result[2], result[3], result[4]
                    self.parent.addPiece(name, pType, int(row), int(column))
                elif eType == 'move':
                    name, toRow, toColumn = result[1], result[2], result[3]
                    self.parent.movePiece(name, int(toRow), int(toColumn))
                elif eType == 'change':
                    name, pType = result[1], result[2]
                    self.parent.updatePieceType(name, pType)
                elif eType == 'remove':
                    name = result[1]
                    self.parent.removePiece(name)
                elif eType == 'highlight':
                    name = result[1]
                    self.parent.highlightPiece(name)
                elif eType == 'rhighlight':
                    self.parent.removeHighlight()
            else:
                time.sleep(0.01)
