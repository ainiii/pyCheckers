import tkinter as tk
import socket
import time
import server
import client
import game
import model
from .main_menu import MainMenu
from .game_board import GameBoard

class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.mainMenu = MainMenu(self)
        self.gameBoard = GameBoard(self)

        self.model = False
        self.game = False

        self.mainMenu.show()

    def hostGame(self, ip, port):
        server.ServerThread(ip, port)
        self.joinGame(ip, port, 1)

    def joinGame(self, ip, port, player=2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                sock.connect((ip, int(port)))
                break
            except:
                print("Failed to join, retrying.")
                time.sleep(1)

        self.model = model.Model()
        self.gameBoard.attachModel(self.model)
        self.gameInstance = game.Game(player, sock, self.model)
        client.ClientThread(sock, self.gameInstance)
        self.showGame()

    def offlineGame(self):
        server.ServerThread('127.0.0.1', 50000)
        self.joinGame('127.0.0.1', 50000, 1)
        # init ai on another thread
        pass

    def showGame(self):
        self.mainMenu.hide()
        self.gameBoard.show()
