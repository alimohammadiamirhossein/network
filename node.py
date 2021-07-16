class Node:
    def __init__(self):
        self.ID = None
        self.port = None
        self.parent_ID = None
        self.parent_port = None
        self.left_child_ID = None
        self.left_child_port = None
        self.right_child_ID = None
        self.right_child_port = None
        self.left_child_IDs_list = []
        self.right_child_IDs_list = []
        # chat part
        self.known_IDs = []
        self.chat_name = None
        self.inChat = False
        self.chat = None
        # chat part
