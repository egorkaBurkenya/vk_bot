import requests
# import json

url = 'http://api.openweathermap.org/data/2.5/weather?q=moscow&appid=b96c6038f2b65948ecc7733eb3336864&units=metric'

def get_today_weather() -> str:
    data_json = requests.get(url)
    print(data_json.json()) 


get_today_weather()