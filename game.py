class Game:
    def __init__(self, player, sock, model):
        self.player = player
        self.cPiece = ''
        self.sock = sock
        self.model = model

    def onClick(self, result):
        piece = self.model.getPieceByCoords(result[0], result[1])

        if self.cPiece != '':
            self.sock.send(str.encode('m|' + str(self.cPiece) + '|' + str(result[0]) + '|' + str(result[1])))
        elif piece and piece.pType[1] == str(self.player):
            self.cPiece = piece.name

    def onMessage(self, message):
        text = message.split('|')

        # m|name|toX|toY
        if text[0] == 'm':
            name = text[1]
            toX = text[2]
            toY = text[3]

            self.model.movePiece(name, int(toX), int(toY))
        # t
        elif text[0] == 't':
            self.model.changeTurn()
