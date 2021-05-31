import requests
from translate import Translator

from utiles import verbal_definition_of_wind_force, wind_direction

translator= Translator(from_lang="english",to_lang="russian")


# from pprint import pprint 
# import json


def get_today_weather() -> str:

    """
    Пример:

        Погода в Москве: ясно  

        Ясное небо, температура: 21 - 23°C 

        Давление: 755 мм рт. ст., влажность: 30%   
        
        Ветер: легкий, 3 м/с, западный    
    """

    url = 'http://api.openweathermap.org/data/2.5/weather?q=moscow&appid=b96c6038f2b65948ecc7733eb3336864&units=metric'
    data = requests.get(url)
    weather_data = data.json()

    weather = f'Погода в Москве: {translator.translate(weather_data["weather"][0]["main"])}\n'
    weather += f'{translator.translate(weather_data["weather"][0]["description"])}, '
    weather += f'температура: {weather_data["main"]["temp_max"]} - {weather_data["main"]["temp_min"]}°C\n'
    weather += f'Давление: {weather_data["main"]["pressure"]} мм рт. ст., влажность: {weather_data["main"]["humidity"]}%\n'
    weather += f'Ветер: {verbal_definition_of_wind_force(float(weather_data["wind"]["speed"]))}, {float(weather_data["wind"]["speed"])} м/с, {wind_direction(float(weather_data["wind"]["deg"]))}'

    return(weather)



get_today_weather()