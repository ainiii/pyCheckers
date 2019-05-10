import socket

class Game():
    def __init__(self, player, sock):
        self.cTurn = 1
        self.player = player
        self.sock = sock
        pass

    def onClick(self, result):
        pass

    def onMessage(self, message):
        pass
