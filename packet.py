class Packet:
    def __init__(self):
        self.type = None
        self.source_ID = None
        self.destination_ID = None
        self.Data = None

    def fetch_massage(self, msg):
        lsd = msg.split('$')
        self.type = int(lsd[0])
        self.source_ID = lsd[1]
        self.destination_ID = lsd[2]
        self.Data = lsd[3]

    def make_massage(self):
        msg1 = ""
        msg1 += str(self.type)
        msg1 += "$"
        msg1 += str(self.source_ID)
        msg1 += "$"
        msg1 += str(self.destination_ID)
        msg1 += "$"
        msg1 += str(self.Data)
        return msg1

