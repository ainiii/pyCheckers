class Game:
    def __init__(self, player, sock, model):
        self.player = player
        self.cPiece = False
        self.sock = sock
        self.model = model

    def onClick(self, result):
        if self.model.getTurn() != self.player:
            return

        piece = self.model.getPieceByCoords(result[0], result[1])

        if piece:
            if self.model.getPieceOwner(piece) != self.player:
                return
            else:
                self.model.highlightPiece(piece.name)
                self.cPiece = piece

        if self.cPiece:
            name, row, column = self.model.canCapture(self.player)

            if name is not False and row is not False and column is not False:
                if self.cPiece.name == name and result[0] == row and result[1] == column:
                    self.sock.send(str.encode('m|' + str(self.cPiece.name) + '|' + str(result[0]) + '|' + str(result[1])))
                    return
                else:
                    return

            if self.model.isValidMove(self.cPiece, result[0], result[1]):
                self.sock.send(str.encode('m|' + str(self.cPiece.name) + '|' + str(result[0]) + '|' + str(result[1])))
            else:
                pass

    def onMessage(self, message):
        text = message.split('|')

        # m|name|toX|toY
        if text[0] == 'm':
            name = text[1]
            toX = text[2]
            toY = text[3]

            self.model.movePiece(name, int(toX), int(toY))

            name, row, column = self.model.canCapture(self.model.getTurn())

            if name is False and row is False and column is False:
                if self.model.getTurn() == self.player:
                    self.sock.send(str.encode('t'))
        # t
        elif text[0] == 't':
            self.model.changeTurn()
            self.model.removeHighlightPiece()
