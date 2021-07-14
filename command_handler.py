from packet import Packet
import time


class CommandHandler:
    def __init__(self, client):
        self.client = client

    def command_handler(self, cmd):
        if cmd.startswith("CONNECT AS"):
            self.client.node.ID = cmd.split()[2]
            self.client.node.port = int(cmd.split()[5])
            self.client.connection(
                                f"{self.client.node.ID} REQUESTS FOR CONNECTING TO NETWORK ON PORT {self.client.node.port}",
                                self.client.manager_port)
            while self.client.node.parent_port is None:
                time.sleep(1)
            self.first_connection_with_parent()
            time.sleep(1)
            self.advertise_parent()
        elif cmd == "SHOW KNOWN CLIENTS":
            pass

    def advertise_parent(self):
        pckt = Packet()
        pckt.type = 20
        pckt.source_ID = self.client.node.ID
        pckt.destination_ID = self.client.node.parent_ID
        pckt.Data = f"{self.client.node.ID}"
        msg1 = pckt.make_massage()
        if pckt.destination_ID != -1:
            self.client.connection(msg1, self.client.node.parent_port)

    def first_connection_with_parent(self):
        print("first conn")
        pckt = Packet()
        pckt.type = 41
        pckt.source_ID = self.client.node.ID
        pckt.destination_ID = self.client.node.parent_ID
        pckt.Data = self.client.node.parent_port
        msg1 = pckt.make_massage()
        if pckt.destination_ID != -1:
            self.client.connection(msg1, self.client.node.parent_port)



