import copy

class Game():
    def __init__(self, player, sock, gameBoard):
        self.cTurn = 1
        self.player = player
        self.sock = sock
        self.gameBoard = gameBoard
        self.cPiece = ''
        self.board = [[False for i in range(8)] for j in range(8)]

        self.initBoard()

    def initBoard(self):
        id = 0
        ids = 'abcdefghijklmnopqrstuwxy'

        for i in range(3):
            for j in range(8):
                if i == 1:
                    if j % 2 == 0:
                        self.addPiece(ids[id], 'p2p', i, j)
                    else:
                        self.addPiece(ids[id], 'p1p', 7 - i, j)
                else:
                    if j % 2 == 0:
                        self.addPiece(ids[id], 'p1p', 7 - i, j)
                    else:
                        self.addPiece(ids[id], 'p2p', i, j)

                id += 1

    def changeTurn(self):
        self.cTurn = 1 if self.cTurn == 2 else 2

    def addPiece(self, name, pType, row, column):
        self.gameBoard.addPiece(name, pType, row, column)
        self.board[row][column] = Piece(name, pType)

    def movePiece(self, name, toRow, toColumn):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] and self.board[i][j].name == name:
                    self.gameBoard.movePiece(name, toRow, toColumn)
                    self.board[toRow][toColumn] = copy.deepcopy(self.board[i][j])
                    self.board[i][j] = False
                    return

    def updatePieceType(self, name, pType):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != False and self.board[i][j].name == name:
                    self.gameBoard.updatePieceType(name, pType)
                    self.board[i][j].pType = pType
                    return

    def removePiece(self, row, column):
        self.gameBoard.removePiece(self.board[row][column].name)
        self.board[row][column] = False

    def onClick(self, result):
        piece = self.board[result[0]][result[1]]

        if self.cPiece != '':
            self.sock.send(str.encode('m|' + str(self.cPiece) + '|' + str(result[0]) + '|' + str(result[1])))
        elif piece and (piece.pType == ('p' + str(self.player) + 'p') or piece.pType == ('p' + str(self.player) + 'k')):
            self.cPiece = piece.name

    def onMessage(self, message):
        text = message.split('|')

        # m|name|toX|toY
        if text[0] == 'm':
            name = text[1]
            toX = text[2]
            toY = text[3]

            self.movePiece(name, int(toX), int(toY))
        # t
        elif text[0] == 't':
            self.changeTurn()

class Piece():
    def __init__(self, name, pType):
        self.name = name
        self.pType = pType
