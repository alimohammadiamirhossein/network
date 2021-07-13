import socket


class Topology:
    def __init__(self):
        self.height = 0
        self.nodes = []
        self.last_node_number = 0
        self.manager()

    def append(self, ID, port):
        if self.last_node_number + 1 < 2**self.height - 1:
            self.last_node_number += 1
        else:
            self.height += 1
            self.last_node_number += 1
        node = None
        parent_index = self.last_node_number // 2
        if parent_index > 0:
            parent_node = self.nodes[parent_index]
        return parent_node

    def manager(self):
        host = '127.0.0.1'
        manager_port = 3195
        port = 3195

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()

        cl1, add1 = server_socket.accept()
        print(cl1, add1)
