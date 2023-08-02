class message_frame: 
    def __init__(self, sender, sender_number, message, group_id, msg_type):
        self.sender = sender
        self.sender_number = sender_number
        self.message = message
        self.group_id = group_id
        self.msg_type = msg_type

    
def create_message_frame(lines):
    sender, sender_number, message, group_id = ['']*4
    msg_type = "other"
    for line in lines: 
        if line[0:14] == "Envelope from:":
            sender = line.split(" ")[2]
            sender_number = line.split(" ")[3]
        if line[0:5] == "Body:":
            message = line.strip("Body: ")
            msg_type = "received_message"
        if line[0:5] == "  Id:":
            group_id = line.split(":")[1].strip(" ")

    return message_frame(sender, sender_number, message, group_id, msg_type)