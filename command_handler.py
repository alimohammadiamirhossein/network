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
            if self.client.node.parent_port != -1:
                self.first_connection_with_parent()
                time.sleep(1)
                self.advertise_parent()
        elif cmd == "SHOW KNOWN CLIENTS":
            result1 = self.client.node.known_IDs.copy()
            for a in self.client.node.right_child_IDs_list:
                if a not in result1:
                    result1.append(a)
            for a in self.client.node.left_child_IDs_list:
                if a not in result1:
                    result1.append(a)
            return result1

        elif cmd.startswith("ROUTE"):
            ID_b = cmd.split()[1]
            pckt = Packet()
            pckt.type = 10
            pckt.source_ID = self.client.node.ID
            pckt.destination_ID = ID_b
            pckt.Data = f"ROUTE {ID_b} SOURCE {self.client.node.ID}"
            msg1 = pckt.make_massage()
            self.send_routing_message(msg1, True)
        # start chat part
        elif cmd.startswith("START CHAT"):
            x = cmd.split(" ")
            client_chat_name = x[2]
            self.client.node.chat_name = client_chat_name
            self.client.node.inChat = True
            temp = x[4]
            chat_ids = temp.split(",")
            remove_IDs = []
            print(self.client.node.known_IDs)
            for ID in chat_ids:
                if ID not in self.client.node.known_IDs:
                    remove_IDs.append(ID)
            for ID in remove_IDs:
                chat_ids.remove(ID)
            print(chat_ids)
            string = ''
            for ID in chat_ids:
                string += f",{ID}"
            for ID in chat_ids:
                packet = Packet()
                packet.type = 0
                packet.source_ID = self.client.node.ID
                packet.destination_ID = ID
                # TODO : all IDs in chat_ID
                packet.Data = f"REQUESTS FOR STARTING CHAT WITH {client_chat_name} : {self.client.node.ID}{string}"
                message = packet.make_massage()
                self.client.commandHandler.send_message_known_id(ID, message)

        elif cmd.startswith("Salam Salam Sad Ta Salam"):
            x = cmd.split(" ")
            destination_id = x[5]
            if destination_id == -1:
                # TODO : send message to all
                pass
            # if destination_id in self.client.node.known_IDs:
            packet = Packet()
            packet.type = 0
            packet.Data = "Salam Salam Sad Ta Salam"
            packet.destination_ID = destination_id
            packet.source_ID = self.client.node.ID
            message = packet.make_massage()
            self.send_message_known_id(destination_id,message)

    def chat_handler(self, cmd):
        if self.client.node.join_to_chat_answer:
            if cmd == "Y":
                self.client.node.chat_members.append([self.client.node.admin_ID, self.client.node.admin_name])
                print("Choose a name for yourself")
                self.client.node.join_to_chat_answer = False
                self.client.node.chat_name_answer = True
            else:
                self.client.node.inChat = False
                self.client.node.chat_members = []
                self.client.node.all_chat_IDs = []
        elif self.client.node.chat_name_answer:
            name = cmd
            self.client.node.chat_name = name
            for ID in self.client.node.all_chat_IDs:
                if ID != self.client.node.ID:
                    packet = Packet()
                    packet.type = 0
                    packet.Data = f"{self.client.node.ID} : {name}"
                    packet.destination_ID = ID
                    packet.source_ID = self.client.node.ID
                    # TODO: handle send_message_known
                    message = packet.make_massage()
                    # print(self.client.node.all_chat_IDs)
                    # print(message)
                    self.client.commandHandler.send_message_known_id(ID, message)
            self.client.node.chat_name_answer = False
        elif self.client.node.inChat:
            if cmd == "EXIT CHAT":
                for ID in self.client.node.all_chat_IDs:
                    packet = Packet()
                    packet.type = 0
                    packet.Data = f"EXIT CHAT {self.client.node.ID}"
                    packet.destination_ID = ID
                    packet.source_ID = self.client.node.ID
                    message = packet.make_massage()

                # TODO: handle send_message_known
                    self.client.commandHandler.send_message_known_id(ID, message )
                self.client.node.inChat = False
                self.client.node.chat_members = []
                self.client.node.all_chat_IDs = []
            else:
                self.send_chat_message_to_all(cmd)

    def send_chat_message_to_all(self, msg):
        for x in self.client.node.chat_members:
            ID = x[0]
            chat_name = x[1]
            packet = Packet()
            packet.type = 0
            packet.Data = f"{chat_name} : {msg}"
            packet.destination_ID = ID
            packet.source_ID = self.client.node.ID
            message = packet.make_massage()
        self.client.commandHandler.send_message_known_id(ID,message )

    def send_routing_message(self, msg2, are_u_start=False):
        packet2 = Packet()
        packet2.fetch_massage(msg2)
        data2 = packet2.Data.split()
        ID2 = data2[1]
        # print(ID2, self.client.node.left_child_IDs_list, self.client.node.right_child_IDs_list)
        source2 = data2[3]
        if self.send_message_known_id(ID2, msg2):
            pass
        elif are_u_start:
            print(f"DESTINATION {ID2} NOT FOUND")
        else:
            pckt = Packet()
            pckt.type = 31
            pckt.source_ID = self.client.node.ID
            pckt.destination_ID = source2
            pckt.Data = f"DESTINATION {ID2} NOT FOUND"
            self.send_message_known_id(pckt.destination_ID, pckt.make_massage())

    def send_message_known_id(self, ID2, msg2):
        packet_tmp = Packet()
        packet_tmp.fetch_massage(msg2)
        from_parent = 0
        if ID2 == "-1":
            # print(packet_tmp.source_ID, self.client.node.left_child_IDs_list, self.client.node.right_child_IDs_list)
            if packet_tmp.source_ID not in self.client.node.left_child_IDs_list:
                from_parent += 1
            if packet_tmp.source_ID not in self.client.node.right_child_IDs_list:
                from_parent += 1
            if packet_tmp.source_ID == self.client.node.ID:
                from_parent = -3
            if self.client.node.left_child_port is not None \
                    and packet_tmp.source_ID not in self.client.node.left_child_IDs_list:
                self.client.connection(msg2, self.client.node.left_child_port)
            if self.client.node.right_child_port is not None \
                    and packet_tmp.source_ID not in self.client.node.right_child_IDs_list:
                self.client.connection(msg2, self.client.node.right_child_port)
            if self.client.node.parent_port != -1 and from_parent != 2:
                self.client.connection(msg2, self.client.node.parent_port)
            return
        result = True
        if ID2 in self.client.node.left_child_IDs_list:
            self.client.connection(msg2, self.client.node.left_child_port)
        elif ID2 in self.client.node.right_child_IDs_list:
            self.client.connection(msg2, self.client.node.right_child_port)
        elif self.client.node.parent_port != -1:
            self.client.connection(msg2, self.client.node.parent_port)
        else:
            result = False
        return result

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
        print("first connection")
        pckt = Packet()
        pckt.type = 41
        pckt.source_ID = self.client.node.ID
        pckt.destination_ID = self.client.node.parent_ID
        pckt.Data = self.client.node.port
        msg1 = pckt.make_massage()
        if pckt.destination_ID != -1:
            self.client.connection(msg1, self.client.node.parent_port)
