import threading
import socket
import abstract_thread

class ServerThread(threading.Thread, abstract_thread.AbstractThread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = False
        self.sockets = []
        self.isRunning = True
        self.start()

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.bind((self.ip, self.port))
        except:
            self.isRunning = False
            return

        self.sock.listen(2)

        while self.isRunning:
            try:
                cSocket, address = self.sock.accept()
                print("New connection from: " + str(address))

                self.sockets.append(cSocket)

                if len(self.sockets) == 2:
                    ReceiveThread(cSocket, self.sockets[0])
                    ReceiveThread(self.sockets[0], cSocket)
            except:
                break

    def stop(self):
        self.isRunning = False
        self.sock.close()

class ReceiveThread(threading.Thread, abstract_thread.AbstractThread):
    def __init__(self, sock, otherSock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.otherSock = otherSock
        self.isRunning = True
        self.start()

    def run(self):
        while self.isRunning:
            try:
                data = self.sock.recv(1024)

                if data:
                    self.sock.send(data)
                    self.otherSock.send(data)
            except:
                break

    def stop(self):
        self.isRunning = False
        self.sock.close()
