import subprocess
import json
from message_frame import create_message_frame
from message_types.current_weather import current_weather
from message_types.quote import quote
from message_types.todays_weather import todays_weather
from message_types.current_time import current_time
from message_types.get_schedule import get_schedule
from message_types.get_random_quote import get_random_quote

PUSH_TO_GIT = True

def send_message(bot_number, message, recipient, group_id):
    if group_id: # Checks if it should send message to group or individual
        subprocess.run(['signal-cli', '-a', bot_number, 'send', '-m', message, '-g', group_id], capture_output=True)

    else:
        subprocess.run(['signal-cli', '-a', bot_number, 'send', '-m', message, recipient], capture_output=True)


def receive_message(bot_number, weather_api_key):
    replies = subprocess.run(['signal-cli', '-u', bot_number, 'receive', '--ignore-attachments', "-t 1"], capture_output=True).stdout.decode()
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
            message = ""

            if message_frame.message == "!currenttime":
                message = current_time()
        
            elif message_frame.message[0:15] == "!currentweather": 
                message = current_weather(message_frame, weather_api_key)


            elif message_frame.message[0:14] == "!todaysweather": 
                message = todays_weather(message_frame, weather_api_key)

            elif message_frame.message[0:6] == "!quote": 
                message = quote(message_frame, PUSH_TO_GIT)

            elif message_frame.message[0:9] == "!schedule":
                message = get_schedule()

            elif message_frame.message[0:12] == "!randomquote":
                message = get_random_quote()
            
            if message: # Checks if the message is empty
                send_message(bot_number, message, message_frame.sender_number, message_frame.group_id)


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