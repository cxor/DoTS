
class Message:

    MSG_COUNTER = 0
    LOG = True

    def __init__(self, sender_id="unknown",\
        receiver_id="unknown", message_type="info"):
        self.id = self.MSG_COUNTER + 1
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message_type = message_type
        # Message type legend:
        #   "info" -> exchange of an informative message
        #   "sos" -> exchange of an SOS message, in case of disaster

    def set_type(self, message_type):
        self.message_type = type

    def get_type(self):
        return self.message_type

    def set_receiver_id(self, receiver_id):
        self.receiver_id = receiver_id

    def get_receiver_id(self):
        return self.receiver_id

    def set_sender_id(self, sender_id):
        self.sender_id = sender_id

    def get_sender_id(self):
        return self.sender_id

    def get_message_id(self):
        return self.id

    def get_msg_count(self):
        return Message.MSG_COUNTER

    def log(self):
        if Message.LOG == True:
            print(f"Message {self.id}, Sender: {self.sender_id}, \
                Receiver: {self.receiver_id}, Type: {self.type}")