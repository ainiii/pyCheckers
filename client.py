import threading

class ClientThread(threading.Thread):
    def __init__(self, sock, game):
        threading.Thread.__init__(self)
        self.sock = sock
        self.game = game
        self.start()

    def run(self):
        while True:
            message = self.sock.recv(1024).decode()

            if len(message) > 0:
                self.game.onMessage(message)

