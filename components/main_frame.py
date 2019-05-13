import tkinter as tk
import socket
import time
import server
import client
import game
import model
import threading
import abstract_thread
import ai
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

        self.showMenu()

    def hostGame(self, ip, port):
        server.ServerThread(ip, int(port))
        self.joinGame(ip, port, 1)

    def joinGame(self, ip, port, player=2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                sock.connect((ip, int(port)))
                break
            except:
                print("Failed to join")
                self.mainMenu.infoTxt.config(text='Failed to join')
                time.sleep(1)
                return

        self.model = model.Model()
        self.gameBoard.attachModel(self.model)
        self.gameInstance = game.Game(player, sock, self.model)
        client.ClientThread(sock, self.gameInstance)
        self.showGame()

    def offlineGame(self):
        server.ServerThread('127.0.0.1', 50000)
        self.joinGame('127.0.0.1', 50000, 1)
        ai.AIThread('127.0.0.1', 50000)
        pass

    def showGame(self):
        self.mainMenu.hide()
        self.gameBoard.show()

    def showMenu(self):
        self.gameBoard.hide()
        self.gameBoard = GameBoard(self)
        self.mainMenu.show()
        self.model = False
        self.game = False

        for thread in threading.enumerate():
            if isinstance(thread, abstract_thread.AbstractThread):
                thread.stop()
