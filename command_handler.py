class CommandHandler():
    def __init__(self, client):
        self.client = client

    def command_handler(self, cmd):
        if cmd.startswith("CONNECT AS"):
            self.client.node.ID = cmd.split()[2]
            self.client.node.port = int(cmd.split()[5])
            self.client.connection(
                                f"{self.client.node.ID} REQUESTS FOR CONNECTING TO NETWORK ON PORT {self.client.node.port}",
                                self.client.manager_port)
        elif cmd == "SHOW KNOWN CLIENTS":
            pass



'''
CONNECT AS ali ON PORT 1
CONNECT AS mohsen ON PORT 2
CONNECT AS reza ON PORT 3
CONNECT AS kia ON PORT 4
'''
