import requests

def todays_weather(message_frame, weather_api_key):
    if message_frame.message == "!todaysweather": # Sets a default location if no location is specified
        message_frame.message = "!todaysweather Gothenburg"

    location = message_frame.message.split(" ")[1]
    weather_response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={location}")
    if weather_response.status_code == 200:
        today_info = weather_response.json()["forecast"]["forecastday"][0]["day"]
        return f"Today's weather in {location} is {today_info['condition']['text']} with a high of {today_info['maxtemp_c']}°C and a low of {today_info['mintemp_c']}°C"


    # f"Sorry I can't find the weather for {location}"