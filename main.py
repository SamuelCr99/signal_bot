import subprocess
import json
import datetime 
import requests


def send_message_person(bot_number, message, recipient):
    subprocess.run(['/home/sam/signal-cli-0.11.11/bin/signal-cli', '-u', bot_number, 'send', '-m', message, recipient], capture_output=True)

def send_message_group(bot_number, message, group_id):
    subprocess.run(['/home/sam/signal-cli-0.11.11/bin/signal-cli', '-g', bot_number, 'send', '-m', message, group_id], capture_output=True)

def receive_message(bot_number, send_back_num, weather_api_key, group_id):
    replies = subprocess.run(['/home/sam/signal-cli-0.11.11/bin/signal-cli', '-u', bot_number, 'receive', '--ignore-attachments', "-t 1"], capture_output=True).stdout.decode()
    print(replies)
    lines = replies.split('\n')
    sender = ""
    for line in lines: 
        if "Envelope from:" in line: 
            sender = line.split(" ")[2]

        if line[0:5] == "Body:": 
            if "#currenttime" in line: 
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                send_message_person(bot_number, f"{current_time}", send_back_num)

            elif "#currentweather" in line: 
                wheather_response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q=Gothenburg")
                current_temp = wheather_response.json()['current']['temp_c']
                send_message_group(bot_number, f"Current temp in Gothenburg: {current_temp}", group_id)

def main():
    print("Bot started!")

    with open("secret_information.json") as f: 
        secret_information = json.load(f)
    
    bot_number = secret_information["number"]
    test_number = secret_information["test_number"]
    weather_api_key = secret_information["weather_api_key"]
    group_id = secret_information["group_id"]
    
    while(1):
        current_time = datetime.datetime.now().strftime("%H:%M")
        receive_message(bot_number, test_number, weather_api_key, group_id)

if __name__ == "__main__":
    main()