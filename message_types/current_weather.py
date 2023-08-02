import requests

def current_weather(message_frame, weather_api_key):
    if message_frame.message == "!currentweather": # Sets a default location if no location is specified
        message_frame.message = "!currentweather Gothenburg"

    location = message_frame.message.split(" ")[1]
    weather_response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}")
    if weather_response.status_code == 200:
        current_temp = weather_response.json()['current']['temp_c']
        return f"Current temp in {location}: {current_temp}"

    else:
        return f"Sorry I can't find the weather for {location}"