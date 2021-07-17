class FireWall:
    def __init__(self, direction, source_ID, dest_ID, type1, is_acc):
        self.direction = direction
        self.source_ID = source_ID
        self.dest_ID = dest_ID
        self.type = type1
        self.is_acc = is_acc


class FirewallManager:
    def __init__(self):
        self.firewalls = []

    def append_fireWall(self, direction, source_ID, dest_ID, type1, is_acc):
        fw = FireWall(direction, source_ID, dest_ID, type1, is_acc)
        self.firewalls.append(fw)

    def can_packet_pass(self, packet):
        result = True
        for fw in self.firewalls:
            tmp = firewall_check(packet, fw)
            if tmp is False:
                result = False
        return result


@staticmethod
def firewall_check(packet, fw):
    fw = FireWall()
    if packet.type == fw.type:
        return True
    if fw.direction == "INPUT":
        if packet.source_ID == "*":
            return fw.is_acc
        elif packet.source_ID == fw.source_ID:
            return fw.is_acc
        else:
            return True
    elif fw.direction == "OUTPUT":
        if packet.destination_ID == "*":
            return fw.is_acc
        elif packet.destination_ID == fw.dest_ID:
            return fw.is_acc
        else:
            return True
