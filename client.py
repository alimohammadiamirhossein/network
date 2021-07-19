import socket
import threading
import time
import random
from node import Node
from packet import Packet
from command_handler import CommandHandler
from massage_handler import MassageHandler
from firewall import FirewallManager


class Client:
    # TODO : add all clients here
    all_clients = []

    def __init__(self):
        self.host = '127.0.0.1'
        self.manager_port = 3191
        self.node = Node()
        self.commandHandler = CommandHandler(self)
        self.massageHandler = MassageHandler(self)
        self.firewall_manager = FirewallManager()
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
        # if "$" in send_data:
        #     p_tmp = Packet()
        #     p_tmp.fetch_massage(send_data)
        #     if not self.firewall_manager.can_packet_pass(p_tmp):
        #         return
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        i = 1
        while True:
            try:
                client_socket.connect((self.host, port1))
                # print("you connected", send_data)
                client_socket.send(send_data.encode("ascii"))
                # print("send to", port1)
                client_socket.close()
                break
            except Exception as e:
                time.sleep(i)
                i *= 2
                message = e

    def server_receive(self):
        while True:
            cl1, add1 = self.server_socket.accept()
            msg = cl1.recv(1024).decode("ascii")
            # print("acc new msg", msg)
            if self.node.parent_ID is None:
                self.node.parent_ID = msg.split()[2]
                self.node.parent_port = int(msg.split()[5])
                print(self.node.parent_ID, self.node.parent_port)
            else:
                packet1 = Packet()
                packet1.fetch_massage(msg)
                if self.firewall_manager.can_packet_pass(packet1):
                    thread3 = threading.Thread(target=self.massageHandler.massage_handler, args=(packet1,))
                    thread3.start()

    def command_handler(self):
        while True:
            cmd = input()
            if self.node.join_to_chat_answer or self.node.chat_name_answer or self.node.inChat:
                self.commandHandler.chat_handler(cmd)
            else:
                self.commandHandler.command_handler(cmd)

    def find_client_from_id(self, id):
        for client in self.all_clients:
            if client.node.ID == id:
                return client
        return -1


if __name__ == '__main__':
    Client()

'''
CONNECT AS ali ON PORT 11
CONNECT AS mohsen ON PORT 12
CONNECT AS reza ON PORT 13
CONNECT AS kia ON PORT 14
CONNECT AS mamal ON PORT 5
CONNECT AS tar ON PORT 6

START CHAT dash : mohsen,kia

FILTER INPUT kia ali 11 DROP
FILTER INPUT reza ali 11 DROP
FILTER OUTPUT sa reza 10 DROP
FILTER OUTPUT sa * 10 DROP

Salam Salam Sad Ta Salam -1
'''