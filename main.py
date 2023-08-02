import subprocess
import json
import datetime 
import requests
from message_frame import create_message_frame

PUSH_TO_GIT = False

        

def send_message(bot_number, message, recipient, group_id):
    if group_id: # Checks if it should send message to group or individual
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


            elif message_frame.message[0:15] == "!todaysweather": 
                if message_frame.message == "!todaysweather": # Sets a default location if no location is specified
                    message_frame.message = "!todaysweather Gothenburg"

                location = message_frame.message.split(" ")[1]
                weather_response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={location}")
                if weather_response.status_code == 200:
                    x = weather_response.json()
                    with open('weather.json', 'w') as outfile:
                        json.dump(x, outfile, indent=4)
                #     current_temp = weather_response.json()['current']['temp_c']
                #     send_message(bot_number, f"Current temp in {location}: {current_temp}", message_frame.sender_number,message_frame.group_id)

                # else:
                #     send_message(bot_number, f"Sorry I can't find the weather for {location}", message_frame.sender_number, message_frame.group_id)

            elif message_frame.message[0:6] == "!quote": 
                if message_frame.message == "!quote":
                    send_message(bot_number, f"Please specify a quote", message_frame.sender_number, message_frame.group_id)
                    continue

                new_quote = message_frame.message.split("!quote ")[1]
                subprocess.run(f"git -C quotes/ pull", shell=True,capture_output=True)
                subprocess.run(f"sed '$i ‎' quotes/quotes.tex | tee quotes/quotes_temp.tex", shell=True,capture_output=True)
                subprocess.run(f"mv quotes/quotes_temp.tex quotes/quotes.tex", shell=True, capture_output=True)
                subprocess.run(f"sed '$i {new_quote}' quotes/quotes.tex | tee quotes/quotes_temp.tex", shell=True)
                subprocess.run(f"mv quotes/quotes_temp.tex quotes/quotes.tex", shell=True)

                if PUSH_TO_GIT:
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