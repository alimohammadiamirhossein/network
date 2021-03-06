from packet import Packet
import time

# TODO : handle CHAT: in the beginning of messages
# TODO : handle known ID's , node haye miani ham shenakhte mishavand ?
# TODO : if a client is in chat other messages are ignored
class MassageHandler:
    def __init__(self, client):
        self.client = client

    def massage_handler(self, packet):
        if packet.destination_ID == self.client.node.ID:
            if packet.source_ID not in self.client.node.known_IDs:
                self.client.node.known_IDs.append(packet.source_ID)
        else:
            if not self.client.node.inChat:
                if packet.destination_ID != "-1":
                    print(f"{packet.type} Packet from {packet.source_ID} to {packet.destination_ID}")
        # print(packet.source_ID, packet.Data)
        if packet.type == 20:
            if packet.source_ID == self.client.node.left_child_ID:
                if packet.Data not in self.client.node.left_child_IDs_list:
                    self.client.node.left_child_IDs_list.append(packet.Data)
                    if packet.Data not in self.client.node.known_IDs:
                        self.client.node.known_IDs.append(packet.Data)
                    # print("left_child", self.client.node.left_child_IDs_list)
            elif packet.source_ID == self.client.node.right_child_ID:
                if packet.Data not in self.client.node.right_child_IDs_list:
                    self.client.node.right_child_IDs_list.append(packet.Data)
                    if packet.Data not in self.client.node.known_IDs:
                        self.client.node.known_IDs.append(packet.Data)
                    # print("right_child", self.client.node.right_child_IDs_list)
            packet.source_ID = self.client.node.ID
            packet.destination_ID = self.client.node.parent_ID
            if packet.destination_ID != -1:
                msg1 = packet.make_massage()
                self.client.connection(msg1, self.client.node.parent_port)

        elif packet.type == 41:
            # print(41, packet.make_massage())
            if self.client.node.left_child_ID is None:
                self.client.node.left_child_ID = packet.source_ID
                self.client.node.left_child_port = int(packet.Data)
                # self.client.node.left_child_IDs_list.append(self.client.node.left_child_ID)
            elif self.client.node.right_child_ID is None:
                self.client.node.right_child_ID = packet.source_ID
                self.client.node.right_child_port = int(packet.Data)
                # self.client.node.right_child_IDs_list.append(self.client.node.right_child_ID)

        elif packet.type == 21:
            # print(21, packet.make_massage())
            if packet.destination_ID == "-1":
                if packet.source_ID not in self.client.node.known_IDs:
                    self.client.node.known_IDs.append(packet.source_ID)
                self.client.commandHandler.send_message_known_id(packet.destination_ID, packet.make_massage())
            else:
                if self.client.node.ID == packet.destination_ID :
                    pass
                else:
                    self.client.commandHandler.send_message_known_id(packet.destination_ID, packet.make_massage())
            # print("known ids" , self.client.node.known_IDs)
        elif packet.type == 10:
            # sample :     ROUTE {ID_b} SOURCE {self.client.node.ID}
            ID2 = packet.Data.split()[1]
            if self.client.node.ID == ID2:
                # print("packet find from", packet.source_ID)  # todo packet type 11
                packet11 = Packet()
                packet11.type = 11
                packet11.source_ID = self.client.node.ID
                packet11.destination_ID = packet.source_ID
                packet11.Data = f"{self.client.node.ID}"
                self.client.commandHandler.send_message_known_id(packet.source_ID, packet11.make_massage())
            else:
                # print("time to send", packet.make_massage())
                self.client.commandHandler.send_routing_message(packet.make_massage(), False)

        elif packet.type == 11:
            last_node_ID = packet.Data.split()[0]
            if last_node_ID == self.client.node.parent_ID:
                data1 = self.client.node.ID + " <- " + packet.Data
                packet.Data = data1
            elif last_node_ID == self.client.node.right_child_ID:
                data1 = self.client.node.ID + " -> " + packet.Data
                packet.Data = data1
            elif last_node_ID == self.client.node.left_child_ID:
                data1 = self.client.node.ID + " -> " + packet.Data
                packet.Data = data1
            else:
                data1 = self.client.node.ID + " something wrong " + packet.Data
                packet.Data = data1

            if packet.destination_ID == self.client.node.ID:
                print(packet.Data)
            else:
                self.client.commandHandler.send_message_known_id(packet.destination_ID, packet.make_massage())

        elif packet.type == 31:
            # print(31, packet.destination_ID, packet.Data)
            if packet.destination_ID == self.client.node.ID:
                print(packet.Data)
            else:
                self.client.commandHandler.send_message_known_id(packet.destination_ID, packet.make_massage())
        elif packet.type == 0:

            data = packet.Data
            if packet.destination_ID == self.client.node.ID or packet.destination_ID == "-1":
                if data.startswith("Salam Salam Sad Ta Salam"):
                    print("Salam Salam Sad Ta Salam")
                    packet2 = Packet()
                    packet2.Data = "Hezaro Sisad Ta Salam"
                    packet2.source_ID = self.client.node.ID
                    packet2.type = 0
                    packet2.destination_ID = packet.source_ID
                    if packet.source_ID not in self.client.node.known_IDs:
                        self.client.node.known_IDs.append(packet.source_ID)
                    self.client.commandHandler.send_message_known_id(packet2.destination_ID,packet2.make_massage())
                    # print(self.client.node.known_IDs)
                elif data == "Hezaro Sisad Ta Salam":
                    # self.client.node.known_IDs.append(packet.source_ID)
                    print("Hezaro Sisad Ta Salam")
                elif data.startswith("REQUESTS FOR STARTING CHAT WITH") and self.client.node.firewall_chat:
                    if not self.client.node.inChat:
                        self.client.node.inChat = True
                        temp = data.split(" ")
                        self.client.node.admin_name = temp[5]
                        x = temp[7]
                        x = x.split(",")
                        # handle known ID's here
                        for ID in x:
                            if ID not in self.client.node.known_IDs:
                                self.client.node.known_IDs.append(ID)
                        ###
                        self.client.node.admin_ID = x[0]
                        self.client.node.all_chat_IDs = x
                        print(f"CHAT:\n{self.client.node.admin_name} with id {self.client.node.admin_ID} has "
                              f"asked you to join a chat. Would you like to join?[Y/N]")
                        self.client.node.join_to_chat_answer = True
                elif data.startswith("EXIT CHAT"):
                    if packet.source_ID in self.client.node.all_chat_IDs:
                        # because the message is sent to all ID's in first list
                        if self.client.node.inChat:
                            temp = data.split(" ")
                            left_chat_id = temp[2]
                            for x in self.client.node.chat_members:
                                if x[0] == left_chat_id:
                                    left_chat_name = x[1]
                                    self.client.node.chat_members.remove(x)
                                    break
                            print(f"CHAT:\n{left_chat_name}({left_chat_id}) left the chat.")
                else:
                    if packet.source_ID in self.client.node.all_chat_IDs:
                        temp = data.split(" ")
                        if temp[1] == ":" and len(temp) == 3:
                            member_chat_name = temp[2]
                            member_id = temp[0]
                            if self.client.node.inChat:
                                self.client.node.chat_members.append([member_id, member_chat_name])
                            if self.client.node.join_to_chat_answer:
                                pass
                            else:
                                print(f"CHAT:\n{member_chat_name}({member_id}) was joined to the chat.")
                        else:
                            print(f"CHAT:\n{data}")

            else:
                self.client.commandHandler.send_message_known_id(packet.destination_ID, packet.make_massage())
            if packet.destination_ID == "-1":
                self.client.commandHandler.send_message_known_id(packet.destination_ID, packet.make_massage())
