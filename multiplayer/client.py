import threading
import abstract_thread

class ClientThread(threading.Thread, abstract_thread.AbstractThread):
    def __init__(self, sock, game):
        threading.Thread.__init__(self)
        self.sock = sock
        self.game = game
        self.isRunning = True
        self.start()

    def run(self):
        while self.isRunning:
            try:
                message = self.sock.recv(1024).decode()

                if len(message) > 0:
                    self.game.onMessage(message)
            except:
                break

    def stop(self):
        self.isRunning = False
        self.sock.close()
