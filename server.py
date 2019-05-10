import threading
import socket

class ServerThread(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.start()
        self.sockets = []

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(2)

        while True:
            cSocket, address = sock.accept()
            print("New connection from: " + str(address))

            self.sockets.append(cSocket)

            if len(self.sockets) == 2:
                ReceiveThread(cSocket, self.sockets[0])
                ReceiveThread(cSocket, self.sockets[1])

class ReceiveThread(threading.Thread):
    def __init__(self, sock, otherSock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.otherSock = otherSock
        self.start()

    def run(self):
        while True:
            data = self.sock.recv(1024)
            if data:
                self.sock.send(data)
                self.otherSock.send(data)
