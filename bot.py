import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import json
import datetime

# Имортирую свои функции 
from bs import download_files
from exel import parse_Table
from utiles import today_table, tomorrow_table, this_week_table, next_week_table, week_day_table
from weather import get_today_weather


def get_groupes():
    with open('table.json', 'r') as file:
        table = json.load(file)
    groupes = []
    for groupe in table:
        groupes.append(groupe)
    with open('groupes.json', 'w') as file:
        json.dump({"groupes": groupes}, file)

def main():

    vk_session = vk_api.VkApi(token='587b57fec44ecc5c31175975fa332481eb9a6564b1034e63517565f1844e0253bd65500dc4fcc315d76c3')
    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.text:
            if event.text.lower() == 'привет':
                print(event)
                vk.messages.send(
                user_id = event.user_id,
                random_id = get_random_id(),
                message = 'привет друг !🍄')
            elif event.text.lower() == 'бот':
                keyboard = VkKeyboard(one_time=False)
                keyboard.add_button('на сегодня', color=VkKeyboardColor.POSITIVE)
                keyboard.add_button('на завтра', color=VkKeyboardColor.NEGATIVE)
                keyboard.add_line() # переход на вторую строку
                keyboard.add_button('на эту неделю', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('на следующую неделю', color=VkKeyboardColor.PRIMARY)
                keyboard.add_line() # переход на вторую строку
                keyboard.add_button('какая неделя ?', color=VkKeyboardColor.SECONDARY)
                keyboard.add_button('какая группа ?', color=VkKeyboardColor.SECONDARY)
                with open('users.json') as file:
                    groupe = json.load(file)[str(event.user_id)]
                vk.messages.send(user_id = event.user_id, random_id = get_random_id(), keyboard=keyboard.get_keyboard(), message = f'Показать расписание группы {groupe}')
            elif event.text.lower() == 'update':
                try: 
                    vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = 'Начинаю загрузку файлов...')
                    download_files()
                    vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = 'Файлы скачены, начинаю парсить Exel файлы...')
                    parse_Table()
                    vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = 'Done 👀✅')
                    get_groupes()
                except: 
                    vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = 'Что-то пошло не так!')
            elif event.text.lower() == 'на сегодня':
                with open('users.json', 'r') as f:
                    user_groupe = json.load(f)[str(event.user_id)]
                table = today_table(user_groupe)
                vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = table)
            elif event.text.lower() == 'на завтра':
                with open('users.json', 'r') as f:
                    user_groupe = json.load(f)[str(event.user_id)]
                table = tomorrow_table(user_groupe)
                vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = table)
            elif event.text.lower() == 'на эту неделю':
                with open('users.json', 'r') as f:
                    user_groupe = json.load(f)[str(event.user_id)]
                table = this_week_table(user_groupe)
                vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = table)
            elif event.text.lower() == 'на следующую неделю':
                with open('users.json', 'r') as f:
                    user_groupe = json.load(f)[str(event.user_id)]
                table = next_week_table(user_groupe)
                vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = table)
            elif event.text.lower() == 'какая неделя ?':
                today = datetime.datetime.today()
                week_number = today.isocalendar()[1] 
                vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = f'Идет {week_number} неделя')
            elif event.text.lower() == 'какая группа ?':
                with open('users.json', 'r') as f:
                    user_groupe = json.load(f)[str(event.user_id)]
                vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = f'Показываю расписание группы {user_groupe}')
            elif 'бот' in event.text.lower() and len(event.text.lower()) > 4: 

                # Если сообщение будет содержать слово бот и что-то еще 

                arg = event.text.lower().split(' ')[1] # забирает аргумент 
                with open('groupes.json', 'r') as file:
                    groupes = json.load(file)["groupes"]

                if arg in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']:
                    # если был написан денб недели 
                    with open('users.json', 'r') as f:
                        user_groupe = json.load(f)[str(event.user_id)]
                    table = week_day_table(arg, user_groupe)
                    vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = table)

                elif arg in groupes:
                    # если была написанна группа 
                     if event.text in groupes:
                        with open('users.json', 'r') as file:
                            users = json.load(file)
                        users[event.user_id] = event.text
                        with open('users.json', 'w') as file:
                            json.dump(users, file)                    
                        vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = f'Показать расписание группы {event.text}')
                elif len(event.text.lower().split(' ')) == 3:
                    # если была написанна группа и день недели 
                    with open('users.json', 'r') as f:
                        user_groupe = json.load(f)[str(event.user_id)]
                    args = event.text.split(' ')
                    table = week_day_table(args[1].lower(), args[2])
                    vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = table)
            elif event.text.lower() == 'погода':
                weather = get_today_weather()
                vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = weather)
            else:
                with open('groupes.json', 'r') as file:
                    groupes = json.load(file)["groupes"]
                if event.text in groupes:
                    with open('users.json', 'r') as file:
                        users = json.load(file)
                    users[event.user_id] = event.text
                    with open('users.json', 'w') as file:
                        json.dump(users, file)                    
                    vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = f'Я запомнил, что ты из группы {event.text}')

if __name__ == '__main__':
    main()