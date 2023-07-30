import subprocess
import json
import datetime 
import requests

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
        

def send_message(bot_number, message, recipient, group_id):
    if group_id:
        subprocess.run(['/home/sam/signal-cli-0.11.11/bin/signal-cli', '-a', bot_number, 'send', '-m', message, '-g', group_id], capture_output=True)

    else:
        subprocess.run(['/home/sam/signal-cli-0.11.11/bin/signal-cli', '-a', bot_number, 'send', '-m', message, recipient], capture_output=True)


def receive_message(bot_number, weather_api_key):
    replies = subprocess.run(['/home/sam/signal-cli-0.11.11/bin/signal-cli', '-u', bot_number, 'receive', '--ignore-attachments', "-t 1"], capture_output=True).stdout.decode()
    lines = replies.split('\n')
    current_message_frame_lines = []
    message_frames = []

    # Collect each message and create message_frames from them
    for line in lines: 
        if line == '' and len(current_message_frame_lines) > 0:
            message_frames.append(create_message_frame(current_message_frame_lines))
            current_message_frame_lines = []
        current_message_frame_lines.append(line)

    # Loop through each message and check if it is a command
    for message_frame in message_frames: 
        if message_frame.msg_type == "received_message":
            if message_frame.message == "!currenttime":
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                send_message(bot_number, f"{current_time}", message_frame.sender_number, message_frame.group_id)
        
            elif message_frame.message[0:15] == "!currentweather": 
                if message_frame.message == "!currentweather": # Sets a default location if no location is specified
                    message_frame.message = "!currentweather Gothenburg"

                location = message_frame.message.split(" ")[1]
                weather_response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}")
                if weather_response.status_code == 200:
                    current_temp = weather_response.json()['current']['temp_c']
                    send_message(bot_number, f"Current temp in {location}: {current_temp}", message_frame.sender_number,message_frame.group_id)

                else:
                    send_message(bot_number, f"Sorry I can't find the weather for {location}", message_frame.sender_number, message_frame.group_id)

            elif message_frame.message[0:7] == "!quote ": 
                new_quote = message_frame.message.split("!quote ")[1]
                subprocess.run(f"git -C quotes/ pull", shell=True,capture_output=True)
                subprocess.run(f"echo ' ' >> quotes/quotes.tex", shell=True,capture_output=True)
                subprocess.run(f"echo {new_quote} >> quotes/quotes.tex", shell=True,capture_output=True)
                subprocess.run(f"git -C quotes/ add .", shell=True,capture_output=True)
                subprocess.run(f"git -C quotes/ commit -m 'New quote added from bot'", shell=True,capture_output=True)
                subprocess.run(f"git -C quotes/ push", shell=True,capture_output=True)
                send_message(bot_number, f"Quote added!", message_frame.sender_number, message_frame.group_id)



def main():
    print("Bot started!")

    with open("secret_information.json") as f: 
        secret_information = json.load(f)
    
    bot_number = secret_information["number"]
    weather_api_key = secret_information["weather_api_key"]
    
    while(1):
        receive_message(bot_number, weather_api_key)

if __name__ == "__main__":
    main()