import socket
import threading
import time
import random
from node import Node
from packet import Packet
from command_handler import CommandHandler


class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.manager_port = 3191
        self.node = Node()
        self.commandHandler = CommandHandler(self)

        thread1 = threading.Thread(target=self.command_handler, args=())
        thread1.start()

        while self.node.ID is None:
            time.sleep(1)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.node.port))
        self.server_socket.listen()

        thread2 = threading.Thread(target=self.server_receive, args=())
        thread2.start()

    def connection(self, send_data, port1):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                client_socket.connect((self.host, port1))
                print("you connected to your manager")
                client_socket.send(send_data.encode("ascii"))
                client_socket.close()
                break
            except Exception as e:
                time.sleep(1)
                message = e

    def server_receive(self):
        while True:
            cl1, add1 = self.server_socket.accept()
            msg = cl1.recv(1024).decode("ascii")
            if self.node.parent_ID is None:
                self.node.parent_ID = msg.split()[2]
                self.node.parent_port = int(msg.split()[5])
                print(self.node.parent_ID, self.node.parent_port)
            else:
                packet1 = Packet()
                packet1.fetch_massage(msg)

    def command_handler(self):
        while True:
            cmd = input()
            self.commandHandler.command_handler(cmd)

if __name__ == '__main__':
    Client()