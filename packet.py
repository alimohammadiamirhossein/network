class Packet:
    def __init__(self):
        self.type = None
        self.source_ID = None
        self.destination_ID = None
        self.Data = None

    def fetch_massage(self, msg=None):
        msg = "0$ali$-1$ lala sa  "
        lsd = msg.split('$')
        self.type = int(lsd[0])
        self.source_ID = lsd[1]
        self.destination_ID = lsd[2]
        self.Data = lsd[3]
        print(lsd)


