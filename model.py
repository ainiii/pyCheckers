import copy

class Model:
    def __init__(self):
        self.turn = 1
        self.board = [[False for i in range(8)] for j in range(8)]
        self.lastEvent = 0
        self.events = []

        self.initBoard()

    def initBoard(self):
        cid = 0
        ids = 'abcdefghijklmnopqrstuwxy'

        for i in range(3):
            for j in range(8):
                if i == 1:
                    if j % 2 == 0:
                        self.addPiece(ids[cid], 'p2p', i, j)
                    else:
                        self.addPiece(ids[cid], 'p1p', 7 - i, j)
                else:
                    if j % 2 == 0:
                        self.addPiece(ids[cid], 'p1p', 7 - i, j)
                    else:
                        self.addPiece(ids[cid], 'p2p', i, j)

                cid += 1

    def changeTurn(self):
        self.turn = 1 if self.turn == 2 else 2

    def addPiece(self, name, pType, row, column):
        piece = type('piece', (), {'name': name, 'pType': pType, 'row': row, 'column': column})
        self.board[row][column] = piece()
        self.addEvent('add', name, pType, row, column)

    def movePiece(self, name, toRow, toColumn):
        row, column = self.getPieceByName(name)

        if row is False or column is False:
            return

        self.board[toRow][toColumn] = copy.deepcopy(self.board[row][column])
        self.board[toRow][toColumn].row = toRow
        self.board[toRow][toColumn].column = toColumn

        self.board[row][column] = False
        self.addEvent('move', name, toRow, toColumn)

    def updatePieceType(self, name, pType):
        row, column = self.getPieceByName(name)

        if row is False or column is False:
            return

        self.board[row][column].pType = pType
        self.addEvent('change', name, pType)

    def removePiece(self, name):
        row, column = self.getPieceByName(name)

        if row is False or column is False:
            return

        self.board[row][column] = False
        self.addEvent('remove', name)

    def getPieceByName(self, name):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] and self.board[i][j].name == name:
                    return i, j

        return False, False

    def getPieceByCoords(self, row, column):
        return self.board[row][column]

    def getPieces(self):
        pieces = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    pieces.append(self.board[i][j])

        return pieces

    def addEvent(self, *args):
        result = args[0]

        for x in range(1, len(args)):
            result += '|'
            result += str(args[x])

        self.events.append(result)

    def getNextEvent(self):
        if self.lastEvent == len(self.events):
            return False

        temp = self.lastEvent
        self.lastEvent += 1
        return self.events[temp]
