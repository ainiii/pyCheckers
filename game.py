import move_exception

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
                return

        if self.cPiece:
            possibleMoves = self.model.canCapture(self.player)

            if len(possibleMoves) > 0:
                try:
                    if not (self.cPiece.name, result[0], result[1]) in possibleMoves:
                        raise move_exception.MoveException('capture')

                    self.sock.send(str.encode('m|' + str(self.cPiece.name) + '|' + str(result[0]) + '|' + str(result[1])))
                except move_exception.MoveException as me:
                    self.model.addEvent('error|' + str(me))
                finally:
                    return

            try:
                if not self.model.isValidMove(self.cPiece, result[0], result[1]):
                    raise move_exception.MoveException('move')

                self.sock.send(str.encode('m|' + str(self.cPiece.name) + '|' + str(result[0]) + '|' + str(result[1])))
            except move_exception.MoveException as me:
                self.model.addEvent('error|' + str(me))
            finally:
                return

    def onMessage(self, message):
        text = message.split('|')

        # m|name|toX|toY
        if text[0] == 'm':
            name = text[1]
            toX = text[2]
            toY = text[3]

            capture = self.model.movePiece(name, int(toX), int(toY))

            if capture:
                possibleMoves = self.model.canCapture(self.model.getTurn())

                if len(possibleMoves) == 0:
                    if self.model.getTurn() == self.player:
                        self.sock.send(str.encode('t'))
                else:
                    self.model.highlightPiece(name)
            else:
                if self.model.getTurn() == self.player:
                    self.sock.send(str.encode('t'))
        # t
        elif text[0] == 't':
            self.model.changeTurn()
            self.model.removeHighlightPiece()
            self.model.checkWinner()
