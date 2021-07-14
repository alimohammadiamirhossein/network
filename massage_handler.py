class MassageHandler:
    def __init__(self, client):
        self.client = client

    def massage_handler(self, packet):
        print(packet.source_ID, self.client.node.left_child_ID, self.client.node.right_child_ID)
        if packet.type == 20:
            if packet.source_ID == self.client.node.left_child_ID:
                if packet.Data not in self.client.node.left_child_IDs_list:
                    self.client.node.left_child_IDs_list.append(packet.Data)
                    print("left_child", self.client.node.left_child_IDs_list)
            elif packet.source_ID == self.client.node.right_child_ID:
                if packet.Data not in self.client.node.right_child_IDs_list:
                    self.client.node.right_child_IDs_list.append(packet.Data)
                    print("right_child", self.client.node.right_child_IDs_list)
            packet.source_ID = self.client.node.ID
            packet.destination_ID = self.client.node.parent_ID
            if packet.destination_ID != -1:
                msg1 = packet.make_massage()
                self.client.connection(msg1, self.client.node.parent_port)

        elif packet.type == 41:
            print(41, packet.make_massage())
            if self.client.node.left_child_ID is None:
                self.client.node.left_child_ID = packet.source_ID
                self.client.node.left_child_port = int(packet.Data)
                # self.client.node.left_child_IDs_list.append(self.client.node.left_child_ID)
            elif self.client.node.right_child_ID is None:
                self.client.node.right_child_ID = packet.source_ID
                self.client.node.right_child_port = int(packet.Data)
                # self.client.node.right_child_IDs_list.append(self.client.node.right_child_ID)