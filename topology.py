import socket
import time


class Topology:
    def __init__(self):
        self.height = 0
        self.IDs_and_Ports = []
        self.last_node_number = 0
        self.manager()

    def append(self, ID, port):
        if self.last_node_number + 1 < 2**self.height - 1:
            self.last_node_number += 1
        else:
            self.height += 1
            self.last_node_number += 1
        self.IDs_and_Ports.append([ID, port])
        parent_index = (self.last_node_number // 2) - 1
        # print(parent_index)
        parent_node = None
        if parent_index >= 0:
            parent_node = self.IDs_and_Ports[parent_index]
        return parent_node

    def manager(self):
        host = '127.0.0.1'
        manager_port = 3191
        port = 3191

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            cl1, add1 = server_socket.accept()
            msg = cl1.recv(1024).decode("ascii")
            if msg.__contains__("REQUESTS FOR CONNECTING TO NETWORK ON PORT"):
                id1 = msg.split()[0]
                port1 = int(msg.split()[8])
                parent1 = self.append(id1, port1)
                # print(parent1, id1, port1, self.IDs_and_Ports)
                if parent1:
                    send_data = f"CONNECT TO {parent1[0]} WITH PORT {parent1[1]}"
                else:
                    send_data = f"CONNECT TO -1 WITH PORT -1"
                self.manager_connection(send_data, port1)

    def manager_connection(self, send_data, port1):
        host = '127.0.0.1'
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                # print(port1)
                client_socket.connect((host, port1))
                # print(send_data)
                client_socket.send(send_data.encode("ascii"))
                client_socket.close()
                break
            except Exception as e:
                time.sleep(1)
                message = e
                # print(message)

