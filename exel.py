import xlrd
import json


def parse_Table():

    """
    Парсит расписание из файлов Exel и записыват в удобном для работы формате в файл table.json
    """

    Table = {}

    # Открываем поочереди каждый файл
    for i in [1, 2, 3]:
        book = xlrd.open_workbook(f"files/file{i}.xlsx") 
        print(f"files/file{i}.xlsx")
        sheet = book.sheet_by_index(0)
        num_cols = sheet.ncols 
        num_rows = sheet.nrows 
        y = 1
        x = 5
        time_y = y + 2      
        time_x = x - 3
        step = 1
        # Проверка, что бы курсор не вышел за длину файла 
        while x < num_cols - 6:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            group = sheet.cell_value(y, x)
            Table[group] = {} 
            y += 2      
            x -= 3
            # Парсим расписание на каждый из дней недели 
            for day in days:
                Table[group][day] = {}
                for num in range(6):
                    Table[group][day][num + 1] = {}

                    # отедально берем расписание четных и нечетных недель

                    Table[group][day][num + 1]["1"] = {
                        "предмет": sheet.cell_value(y, x + 3),
                        "вид занятий": sheet.cell_value(y, x + 4),
                        "преподаватель": sheet.cell_value(y, x + 5),
                        "аудитория": sheet.cell_value(y, x + 6),
                        "ссылка": sheet.cell_value(y, x + 7)
                    }
                    Table[group][day][num + 1]["2"] = {
                        "предмет": sheet.cell_value(y+1, x + 3),
                        "вид занятий": sheet.cell_value(y+1, x + 4),
                        "преподаватель": sheet.cell_value(y+1, x + 5),
                        "аудитория": sheet.cell_value(y+1, x + 6),
                        "ссылка": sheet.cell_value(y+1, x + 7)
                    }
                    
                    # Так как время начала пар общее для любой неделе, записываем его отдельно

                    Table[group][day][num + 1]["начало занятий"] = sheet.cell_value(time_y, time_x) 
                    Table[group][day][num + 1]["конец занятий"] = sheet.cell_value(time_y, time_x + 1) 
                    y += 2
            if step == 3:
                step = 1
                y = 1
                x += 13
                time_y =  y + 2
                time_x =  x - 3  
            else: 
                step += 1
                y = 1
                x += 8
            
    # Записываем в table.json расписание
    with open('table.json', 'w') as file:
        json.dump(Table, file)