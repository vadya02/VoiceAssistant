import psycopg2


def deleteSpaceStartEnd(string):
    if string[0] == " ": string = string[1:len(string) - 1]
    if string[len(string) - 1] == " ": string = string[0:len(string) - 2]
    return string

def checkMatchingStr(firstString, secondString, percent_of_matching = 0.8):
    count_matches = 0
    firstString = list(map(str, deleteSpaceStartEnd(firstString)))
    secondString = list(map(str, deleteSpaceStartEnd(secondString)))
    if abs(len(firstString) - len(secondString)) <= 2 or min([len(firstString), len(secondString)]) > 2: 
        for i in range(0,min([len(firstString), len(secondString)])):
            if (firstString[i] == secondString[i]):
                count_matches += 1
    else:
        return False
    if (count_matches / min([len(firstString), len(secondString)]) >= percent_of_matching):
        return True
    else: 
        return False



def ParseText(str):

    str = str.lower()

    #Connect DB
    conn = psycopg2.connect(dbname='apache-auth', user='postgres', 
                        password='root', host='localhost')
    cursor = conn.cursor()
    cursor.execute('SELECT table_name, url FROM dashboards')
    records = cursor.fetchall()
    dashboards = {}
    for record in records:
        dashboards[record[0]] = record[1]
    
    

    filters = {}

    #нранение найденных тегов
    used_filters = {}
    used_dashboard = 0

    #Индикатор ошибки
    error_filter_state = "Всё чики пуки"
    error_dashboard_state = "Ты как со мной разговариваешь?"

    #С фильтрами
    if "с фильтрами" in str:
        dashboard_text = str[0:str.index("с фильтрами") - 1]
        
        #Вытаскиваем название дашборда
        for dashboard in dashboards:
            if checkMatchingStr("открой " + dashboard, dashboard_text) or checkMatchingStr("открой дашборд " + dashboard, dashboard_text) or checkMatchingStr("открой dashboard " + dashboard, dashboard_text) or checkMatchingStr("dashboard " + dashboard, dashboard_text) or checkMatchingStr("дашборд " + dashboard, dashboard_text):
                if used_dashboard == 0:
                    error_dashboard_state = "Всё чики пуки"
                    used_dashboard = dashboard
                else:
                    error_dashboard_state = "Ты как со мной разговариваешь?"
                    break
        #Если проблем нет
        if error_dashboard_state == "Всё чики пуки":
            filters_text = str[str.index("с фильтрами") + 12:len(str)].split(" и ")

            cursor.execute('SELECT filters.filter_name, filter_values.filter_value FROM dashboards, filters, filter_values WHERE dashboards.table_name = %(used_dashboard)s and dashboards.id = filters.id_dashboard and filters.id = filter_values.id_filter',
                                        {'used_dashboard': used_dashboard})
            records = cursor.fetchall()
            

            #Вытаскивание фильтров из БД
            for record in records:
                if record[0] in filters:
                    filters[record[0]] = [*filters.get(record[0], []), record[1]]
                else:
                    filters[record[0]] = [record[1]]

            #Вытаскивание фильтров
            for filter in filters:
                for text in filters_text:
                    for word in text.split(' '):
                        if checkMatchingStr(filter, word, 0.8):
                            for filter_value in filters[filter]:
                                    if checkMatchingStr(filter_value, text.replace(word, ""), 0.8):
                                        if not filter in used_filters:
                                            error_filter_state = "Всё чики пуки"
                                            used_filters[filter] = filter_value
                                        else:
                                            error_filter_state = "Ты как со мной разговариваешь?"
                                            break
                            break
    #Без фильтров
    else:
        dashboard_text = str
        #Вытаскиваем название дашборда
        for dashboard in dashboards:
            if checkMatchingStr("открой " + dashboard, dashboard_text) or checkMatchingStr("открой дашборд " + dashboard, dashboard_text) or checkMatchingStr("открой dashboard " + dashboard, dashboard_text) or checkMatchingStr("dashboard " + dashboard, dashboard_text) or checkMatchingStr("дашборд " + dashboard, dashboard_text):
                if used_dashboard == 0:
                    error_dashboard_state = "Всё чики пуки"
                    used_dashboard = dashboard
                else:
                    error_dashboard_state = "Ты как со мной разговариваешь?"

    cursor.close()
    conn.close()

    #Собираем конечную строку
    if error_filter_state == "Всё чики пуки" and error_dashboard_state == "Всё чики пуки":
        filters_str = (dashboards[used_dashboard])
        i = 0
        for filter in used_filters:
            if (i != 0):
                filters_str += '&' + filter.capitalize().replace(' ', '+') + "=" + used_filters[filter].capitalize().replace(' ', '+')
            else:
                filters_str += filter.capitalize().replace(' ', '+') + "=" + used_filters[filter].capitalize().replace(' ', '+')
            i += 1
        print(filters_str)
        return filters_str
    else:
        print("Ты как со мной разговариваешь?")

