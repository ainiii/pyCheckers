import threading
import time
from multiplayer import client
import model
import socket
import abstract_thread
from random import randint

class AIThread(threading.Thread, abstract_thread.AbstractThread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.isRunning = True
        self.model = model.Model()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                self.sock.connect((ip, int(port)))
                break
            except:
                print("Failed to join, retrying.")
                time.sleep(1)

        self.gameInstance = AIGame(2, self.sock, self.model)
        client.ClientThread(self.sock, self.gameInstance)
        self.start()

    def run(self):
        while self.isRunning:
            self.gameInstance.think()
            time.sleep(0.01)

    def stop(self):
        self.isRunning = False

class AIGame():
    def __init__(self, player, sock, model):
        self.player = player
        self.sock = sock
        self.model = model
        self.wait = True

    def think(self):
        if self.wait is False and self.model.checkWinner() is False:
            if self.model.getTurn() == self.player:
                possibleMoves = self.model.canCapture(self.model.getTurn())

                if len(possibleMoves) > 0:
                    move = possibleMoves[randint(0, len(possibleMoves) - 1)]
                    self.sock.send(str.encode('m|' + str(move[0]) + '|' + str(move[1]) + '|' + str(move[2])))
                    self.wait = True
                    return

                pieces = self.model.getPieces()

                while self.wait is False:
                    piece = pieces[randint(0, len(pieces) - 1)]
                    if self.model.getPieceOwner(piece) == self.player:
                        moves = self.model.getMoves(piece)

                        if len(moves) > 0:
                            move = moves[randint(0, len(moves) - 1)]
                            self.sock.send(str.encode('m|' + str(piece.name) + '|' + str(move[0]) + '|' + str(move[1])))
                            self.wait = True
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
                    self.wait = False
            else:
                if self.model.getTurn() == self.player:
                    self.sock.send(str.encode('t'))
        # t
        elif text[0] == 't':
            self.model.changeTurn()
            self.wait = False