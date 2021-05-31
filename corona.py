import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import datetime

def last_ten_days() -> str:

    page = requests.get("https://coronavirusstat.ru/country/russia/")
    soup = BeautifulSoup(page.text, "html.parser")
    result = soup.findAll("table")[0].find("tbody").findAll("tr")

    dates = []
    count = 0

    data = {
        "Активных": [],
        "Вылечено": [],
        "Умерло": []
    }

    all = {
        "Случаев": 0,
        "Активных": 0,
        "Вылечено": 0,
        "Умерло": 0
    }

    for i in result:
        count += 1
        if count == 11:
            break
        all["Случаев"] += int(i.findAll('td')[3].text.split(' ')[1])
        all["Активных"] += int(i.findAll('td')[0].text.split(' ')[1])
        all["Вылечено"] += int(i.findAll('td')[1].text.split(' ')[1])
        all["Умерло"] += int(i.findAll('td')[2].text.split(' ')[1])
        dates.append(i.find('th').text)
        data["Активных"].append(int(i.findAll('td')[0].text.split(' ')[1])) 
        data["Вылечено"].append(int(i.findAll('td')[1].text.split(' ')[1]))
        data["Умерло"].append(int(i.findAll('td')[2].text.split(' ')[1])) 
    
    all["Случаев"] = f'{all["Случаев"]} ({result[0].findAll("td")[3].text.split(" ")[2]} за сегодня)'
    all["Активных"] = f'{all["Активных"]} ({result[0].findAll("td")[0].text.split(" ")[2]} за сегодня)'
    all["Вылечено"] = f'{all["Вылечено"]} ({result[0].findAll("td")[1].text.split(" ")[2]} за сегодня)'
    all["Умерло"] = f'{all["Умерло"]} ({result[0].findAll("td")[2].text.split(" ")[2]} за сегодня)'
    

    dates = dates[::-1]
    data["Активных"] = data["Активных"][::-1]
    data["Вылечено"] = data["Вылечено"][::-1]
    data["Умерло"] = data["Умерло"][::-1]

    fig, ax = plt.subplots()
    ax.stackplot(dates, data.values(),
                labels=data.keys())
    plt.xticks(rotation=20) 
    plt.ylim(0, 5000000)
    ax.legend(loc='upper left')
    plt.title('Россия - детальная статистика - короновирус')

    result = f'По состоянию на {datetime.datetime.today().strftime("%m/%d/%Y, %H:%M") }\n'
    result += f'Случаев: {all["Случаев"]}\n'
    result += f'Активных: {all["Активных"]}\n'
    result += f'Вылечено: {all["Вылечено"]}\n'
    result += f'Умерло: {all["Умерло"]}'

    fig.savefig('covid.png')

    return result

def reg_covid(reg: str) -> str:
    
    page = requests.get("https://coronavirusstat.ru/country/russia/")
    soup = BeautifulSoup(page.text, "html.parser")
    result = soup.findAll('div', {'class': 'row border border-bottom-0 c_search_row'})
    status = {}
    for div in result:
        name = div.find('span', {'class': 'small'}).text
        status[name] = {}
        try:
            status[name]["Активных"] = f"{div.find('div', {'class': 'p-1 col-5 col-sm-3'}).find('span', {'class': 'dline'}).text} ({div.find('div', {'class': 'p-1 col-5 col-sm-3'}).find('span', {'class': 'badge badge-danger'}).text} за сегодня)"
        except AttributeError:
            try: 
                status[name]["Активных"] = f"{div.find('div', {'class': 'p-1 col-5 col-sm-3'}).find('span', {'class': 'dline'}).text} ({div.find('div', {'class': 'p-1 col-5 col-sm-3'}).find('span', {'class': 'badge badge-success'}).text} за сегодня)"
            except AttributeError:
                status[name]["Активных"] = f"{div.find('div', {'class': 'p-1 col-5 col-sm-3'}).find('span', {'class': 'dline'}).text}"

        try:
            status[name]["Вылечено"] = f"{div.find('div', {'class': 'p-1 col-4 col-sm-2'}).find('span', {'class': 'dline'}).text} ({div.find('div', {'class': 'p-1 col-4 col-sm-2'}).find('span', {'class': 'badge badge-danger'}).text} за сегодня)"
        except AttributeError:
            try: 
                status[name]["Вылечено"] = f"{div.find('div', {'class': 'p-1 col-4 col-sm-2'}).find('span', {'class': 'dline'}).text} ({div.find('div', {'class': 'p-1 col-4 col-sm-2'}).find('span', {'class': 'badge badge-success'}).text} за сегодня)"
            except AttributeError:
                status[name]["Вылечено"] = f"{div.find('div', {'class': 'p-1 col-4 col-sm-2'}).find('span', {'class': 'dline'}).text}"
        
        try:
            status[name]["Умерло"] = f"{div.find('div', {'class': 'p-1 col-3 col-sm-2'}).find('span', {'class': 'dline'}).text} ({div.find('div', {'class': 'p-1 col-3 col-sm-2'}).find('span', {'class': 'badge badge-danger'}).text} за сегодня)"
        except AttributeError:
            try: 
                status[name]["Умерло"] = f"{div.find('div', {'class': 'p-1 col-3 col-sm-2'}).find('span', {'class': 'dline'}).text} ({div.find('div', {'class': 'p-1 col-3 col-sm-2'}).find('span', {'class': 'badge badge-success'}).text} за сегодня)"
            except AttributeError:
                status[name]["Умерло"] = f"{div.find('div', {'class': 'p-1 col-3 col-sm-2'}).find('span', {'class': 'dline'}).text}"

        try:
            status[name]["Случаев"] = f"{div.find('div', {'class': 'p-1 col-3 col-sm-2 d-none d-sm-block'}).find('div', {'class': 'h6 m-0'}).text}"
        except AttributeError:
            try: 
                status[name]["Случаев"] = f"{div.find('div', {'class': 'p-1 col-3 col-sm-2 d-none d-sm-block'}).find('div', {'class': 'h6 m-0'}).text}"
            except AttributeError:
                status[name]["Случаев"] = f"{div.find('div', {'class': 'p-1 col-3 col-sm-2 d-none d-sm-block'}).find('div', {'class': 'h6 m-0'}).text}"
    
    for region in status:
        if reg in region:
            result = f'По состоянию на {datetime.datetime.today().strftime("%m/%d/%Y, %H:%M") }\n'
            result += f'Случаев: {status[region]["Случаев"]}\n'
            result += f'Активных: {status[region]["Активных"]}\n'
            result += f'Вылечено: {status[region]["Вылечено"]}\n'
            result += f'Умерло: {status[region]["Умерло"]}'
            return result
    
    return f'статистики по региону {reg} к сожалению нет'
