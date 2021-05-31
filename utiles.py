import json 
import datetime

from datetime import date, timedelta

def week_start_date(year, week):

    """
    Получает первый день недели
    """

    d = date(year, 1, 1)    
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    return d + delta

def today_table(groupe: str) -> str:

    """
    Принимает номер группы и отдает расписание на сегодняшний день в формате str
    """

    week_day = datetime.datetime.today().strftime('%A')  
    week_number = datetime.datetime.today().isocalendar()[1] 

    if week_number % 2 == 0: parity = '1'
    else: parity = '2'  
    if  week_day == 'Sunday':
        return 'Сегодня выходной'
    with open('table.json', 'r') as file:
        groupe_week_day_table = json.load(file)[groupe][week_day]
    table = f'Расписание на {datetime.datetime.today().strftime("%d-%m-%Y")}\n\n'
    for i in range(6):
        table += f" {i+1}) {groupe_week_day_table[str(i + 1)][str(parity)]['предмет']}, {groupe_week_day_table[str(i + 1)][str(parity)]['вид занятий']}, {groupe_week_day_table[str(i + 1)][str(parity)]['преподаватель']}, {groupe_week_day_table[str(i + 1)][str(parity)]['аудитория']}\n" 
    return table

def week_day_table(day: str, groupe: str) -> str:

    """
    Отдает расписание конкретного для, конкретной группы 
    """

    trans_week = {
        'понедельник': 'Monday',
        'вторник': 'Tuesday',
        'среда': 'Wednesday',
        'четверг': 'Thursday',
        'пятница': 'Friday',
        'суббота': 'Saturday'
    }
    week_day = trans_week[day]
    if  week_day == 'Sunday':
        return 'Сегодня выходной'
    with open('table.json', 'r') as file:
        groupe_week_day_table = json.load(file)[groupe][week_day]
    table = f'Расписание на {day}\n\n'
    parity = 1
    for i in range(2):
        if parity == 1:
            table += 'Четная неделя: \n\n'
        else:
             table += 'Нечетная неделя: \n\n'
        for i in range(6):
            table += f" {i+1}) {groupe_week_day_table[str(i + 1)][str(parity)]['предмет']}, {groupe_week_day_table[str(i + 1)][str(parity)]['вид занятий']}, {groupe_week_day_table[str(i + 1)][str(parity)]['преподаватель']}, {groupe_week_day_table[str(i + 1)][str(parity)]['аудитория']}\n" 
        parity += 1
        table += '\n\n'
    return table

def tomorrow_table(groupe: str) -> str:

    """
    Расписание на завтращний день 
    """

    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    week_day = tomorrow.strftime('%A')  
    week_number = tomorrow.isocalendar()[1] 
    if week_number % 2 == 0: parity = '1'
    else: parity = '2'  
    if  week_day == 'Sunday':
        return 'Завтра выходной'
    with open('table.json', 'r') as file:
        groupe_week_day_table = json.load(file)[groupe][week_day]
    table = f'Расписание на {tomorrow.strftime("%d-%m-%Y")}\n\n'
    for i in range(6):
        table += f" {i+1}) {groupe_week_day_table[str(i + 1)][str(parity)]['предмет']}, {groupe_week_day_table[str(i + 1)][str(parity)]['вид занятий']}, {groupe_week_day_table[str(i + 1)][str(parity)]['преподаватель']}, {groupe_week_day_table[str(i + 1)][str(parity)]['аудитория']}\n" 
    return table


def this_week_table(groupe: str) -> str:

    """
    Расписание конкретной группы на текущую неделю
    """

    today = datetime.datetime.today()
    week_number = today.isocalendar()[1] 
    print(week_number)
    if week_number % 2 == 0: parity = '1'
    else: parity = '2'  
    with open('table.json', 'r') as file:
        groupe_table = json.load(file)[groupe]
    table = ''
    day_date = week_start_date(today.year, week_number)
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
        table += f'Расписание на {day_date}\n\n'
        for i in range(6):
            table += f" {i+1}) {groupe_table[day][str(i + 1)][str(parity)]['предмет']}, {groupe_table[day][str(i + 1)][str(parity)]['вид занятий']}, {groupe_table[day][str(i + 1)][str(parity)]['преподаватель']}, {groupe_table[day][str(i + 1)][str(parity)]['аудитория']}\n" 
        table += '\n\n'
        day_date = day_date + datetime.timedelta(days=1)
    return table
    
def next_week_table(groupe: str) -> str:

    """
    Расписание на следующую неделю, конкретной группы 
    """

    today = datetime.datetime.today()
    week_number = today.isocalendar()[1] + 1
    print(week_number)
    if week_number % 2 == 0: parity = '1'
    else: parity = '2'  
    with open('table.json', 'r') as file:
        groupe_table = json.load(file)[groupe]
    table = ''
    day_date = week_start_date(today.year, week_number)
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
        table += f'Расписание на {day_date}\n\n'
        for i in range(6):
            table += f" {i+1}) {groupe_table[day][str(i + 1)][str(parity)]['предмет']}, {groupe_table[day][str(i + 1)][str(parity)]['вид занятий']}, {groupe_table[day][str(i + 1)][str(parity)]['преподаватель']}, {groupe_table[day][str(i + 1)][str(parity)]['аудитория']}\n" 
        table += '\n\n'
        day_date = day_date + datetime.timedelta(days=1)
    return table