from client import Client

class Chat:
    def __init__(self, admin_client, admin, IDs):
        self.numOfDefined = 0
        self.first_IDs = IDs
        self.second_IDs = []
        self.final_IDs = []
        self.admin = admin  # admin_ID
        self.admin_client = admin_client
        self.send_request_to_IDs()

    def send_request_to_IDs(self):
        for ID in self.first_IDs:
            if ID in self.admin_client.node.known_IDs:
                client = Client.find_client_from_id(ID)
                client.node.chat = self
                # TODO : handle printing ID's
                self.second_IDs.append(ID)
                self.admin_client.commandHandler.send_message_known_id(ID, f"REQUESTS FOR STARTING CHAT WITH {self.admin_client.node.chat_name} : {self.admin}, ID1, ID2, ID3")
            else:
                pass

    # def ask_to_join(self):
    def append_client(self, name, client):
        client.node.chat_name = name
        client.node.inChat = True
        self.final_IDs.append(client.node.ID)
        for ID in self.second_IDs:
            if ID != client.node.ID:
                client.commandHandler.send_message_known_id(ID, f"{client.node.ID} : {client.node.chat_name}")









