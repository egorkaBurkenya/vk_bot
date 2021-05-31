import requests
from bs4 import BeautifulSoup

def download_files():

    """
    Скачиват файлы Exel с расписанием с сайта https://www.mirea.ru/schedule/
    """

    # Запрашиваем html
    page = requests.get("https://www.mirea.ru/schedule/") 

    soup = BeautifulSoup(page.text, "html.parser")

    # ищим все теги 'a' с сылками
    result = soup.find("div", {"class":"rasspisanie"}).\
    find(string = "Институт информационных технологий").\
    find_parent("div").\
    find_parent("div").\
    findAll("a", {"class":"uk-link-toggle"})

    links = []

    # берем только нужные нам ссылки, тоесть те 
    # которые содержат 'ИИТ' и не содержат 'Экз'
    for a in result:
        if 'ИИТ' in a['href']:
            if 'Экз' in a['href']:
                pass 
            else:
                links.append(a['href'])
    number = 1
    link_count = 0
    # сохраняем файлы в Exel в папку files
    for link in links:
        link_count += 1
        if link_count > 3: 
            break
        f = open(f"files/file{number}.xlsx", "wb") 
        resp = requests.get(link) 
        f.write(resp.content)
        number += 1  
