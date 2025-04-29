import json
import os
import re
from datetime import datetime, timedelta

import nltk
import psycopg2
import requests
from AssistantBackend.settings import (
    DB_NAME,
    HOST,
    NLTK_RESOURCES,
    PASSWORD,
    PORT,
    SUPERSET_HOST,
    USER,
    WORD2VEC_MODEL,
)
from dotenv import load_dotenv

# from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from pymorphy3 import MorphAnalyzer
from utils.ParseFunctions.parse_filters_functions import (
    dashboard_native_filter_create,
    dashboard_native_filter_date_range,
    date_recognize_filter_first,
    date_recognizer_filter,
    find_similarity,
    preprocess_text,
)

load_dotenv("../../.env")
model = WORD2VEC_MODEL.model
stopwords = NLTK_RESOURCES.stop_words

morph = MorphAnalyzer()

stop_words = stopwords


# Параметры подключения к базе данных
dbname = DB_NAME
user = USER
password = PASSWORD
host = HOST
port = PORT


def ParseFilters(text):
    dashboards = []
    target_words = []
    filter_names = []
    threshold = 0.8
    try:
        connection = psycopg2.connect(dbname=dbname,
                                      user=user,
                                      password=password,
                                      host=host,
                                      port=port)
        print("Подключение к базе данных PostgreSQL установлено.")

        # Пример: создание курсора и выполнение запроса
        cursor = connection.cursor()
        cursor.execute("SELECT table_name, url FROM dashboards")
        records = cursor.fetchall()
        for record in records:
            dashboards.append({
                "name": "дашборд",
                "value": record[0],
                "url": record[1]
            })
        for dashbord in dashboards:
            cursor.execute(
                "SELECT filters.filter_name, filters.id_native_filter, filters.type FROM dashboards, filters WHERE dashboards.table_name = %(used_dashboard)s and dashboards.id = filters.id_dashboard",
                {"used_dashboard": dashbord["value"]},
            )
            records = cursor.fetchall()
            print(f"Record: {records}")
            for record in records:
                id_native_filter = re.sub("['(),]", "", str(record[1]))
                filter_type = re.sub("['(),]", "", str(record[2]))
                filters = re.sub("['(),]", "", str(record[0]))

                cursor.execute(
                    "SELECT filter_values.filter_value FROM dashboards, filters, filter_values WHERE dashboards.table_name = %(used_dashboard)s and dashboards.id = filters.id_dashboard and filters.filter_name = %(used_filter)s and filters.id = filter_values.id_filter",
                    {
                        "used_dashboard": dashbord["value"],
                        "used_filter": filters
                    },
                )
                filter_values = cursor.fetchall()
                values = []
                for value in filter_values:
                    values.append(re.sub("['(),]", "", str(value)))
                filter_names.append(filters)
                target_words.append({
                    "name": filters,
                    "value": values,
                    "dashboard": dashbord["value"],
                    "id_native_filter": id_native_filter,
                    "type": filter_type,
                })
        print(dashboards)
        print(target_words)

        cursor.close()
        connection.close()
        print("Соединение с базой данных закрыто.")

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к базе данных PostgreSQL:", error)
    try:

        # -----------------------------------------------------------
        # ***********************************************************
        # -----------------------------------------------------------
        # Пример предложения
        sentence = "создай таблицу в дашборде заявки по состоянию и тип с 25 марта 2023 по 10 апреля 2023"
        sentence = text
        # sentence = "Открой закрытые новый фильм"

        # Применяем предобработку к предложению
        preprocessed_sentence = preprocess_text(sentence)
        # изменено
        lemma_dashboard = []
        for dashboard in dashboards:
            lemma_dashboard.append({
                "name": dashboard["name"],
                "value": preprocess_text(dashboard["value"])
            })
        print(lemma_dashboard)
        # изменено
        lemma_filters = []
        for filters in target_words:
            lemma_filters.append({
                "name":
                preprocess_text(filters["name"]),
                "value":
                [preprocess_text(value) for value in filters["value"]],
                "dashboard":
                preprocess_text(filters["dashboard"]),
                "type":
                filters["type"],
            })
        print(lemma_filters)
        # -----------------------------------------------------------
        # ***********************************************************
        # -----------------------------------------------------------

        # поиск команды
        state_found_commands = False
        state_create_chart = False
        state_open_dashboard = False
        state_change_dashboard = False
        state_filter_dashboard = False
        found_commands_words = []
        found_initial_commands = []
        filters_and_values = []
        date_find_state = False
        commands = ["открыть", "создай", "составь", "добавь"]
        lemma_commands = [["открыть"], ["создать"], ["составить"],
                          ["добавить"]]
        found_words, found_initial_words, ref_sentence = find_similarity(
            [s for s in lemma_commands],
            [s for s in commands],
            [s for s in preprocessed_sentence],
            threshold,
            first_entry=False,
        )
        print(f"{found_words}\n{found_initial_words}\n{ref_sentence}")

        # если команда "создать"
        if found_words[0][0] == "создать" or found_words[0][0] == "составить":
            state_create_chart = True
        # если команда "открыть"
        elif found_words[0][0] == "открыть":
            state_open_dashboard = True
            # state_filter_dashboard = True
        elif found_words[0][0] == "добавить":
            state_change_dashboard = True
        if ref_sentence != preprocessed_sentence:
            state_found_commands = True
            preprocessed_sentence = ref_sentence
            found_commands_words = found_words
            found_initial_commands = found_initial_words
        print("команда не распознана")

        # если команда открыть дашборд
        # -----------------------------------------------------------
        # ***********************************************************
        # -----------------------------------------------------------
        if state_open_dashboard:
            # ищем дашборд
            threshold = 0.8

            found_dashboards_words = []
            found_initial_dashboards = []

            state_found_dashboard = False

            found_words, found_initial_words, ref_sentence = find_similarity(
                [s["value"] for s in lemma_dashboard],
                [s["value"] for s in dashboards],
                [s for s in preprocessed_sentence],
                threshold,
                first_entry=True,
            )

            if ref_sentence != preprocessed_sentence:
                state_found_dashboard = True
                preprocessed_sentence = ref_sentence
                found_dashboards_words = found_words
                found_initial_dashboards = found_initial_words
                url_dashboard = [
                    s['url'] for s in dashboards
                    if found_initial_dashboards[0] == s["value"]
                ][0]
            if state_found_dashboard:
                found_filter_keys = []
                found_initial_filters_words = []
                filters_and_values = []
                dashboards_filters = [
                    s for s in lemma_filters
                    if s["dashboard"] == found_dashboards_words[0]
                ]
                dashboard_initial_filters = [
                    s for s in target_words
                    if s["dashboard"] == found_initial_dashboards[0]
                ]

                # Распознаём названия фильтров
                found_words, found_initial_words, ref_sentence = find_similarity(
                    [s["name"] for s in lemma_filters],
                    [s["name"] for s in target_words],
                    [s for s in preprocessed_sentence],
                    threshold,
                    first_entry=False,
                )
                print(
                    f"{found_words}\n найденные слова: {found_initial_words}\n{ref_sentence}"
                )
                text_filters = [
                    s for s in dashboards_filters if s["type"] == "text"
                ]
                text_initial_filters = [
                    s for s in dashboard_initial_filters if s["type"] == "text"
                ]

                date_filters = [
                    s for s in dashboards_filters if s["type"] == "date"
                ]
                date_initial_filters = [
                    s for s in dashboard_initial_filters if s["type"] == "date"
                ]

                date_find_state = False

                if ref_sentence != preprocessed_sentence:
                    preprocessed_sentence = ref_sentence
                    found_filter_keys = found_words
                    found_initial_filters_words = found_initial_words

                    for filter, initial_filter in zip(
                            found_filter_keys, found_initial_filters_words):
                        # Проверка принадлежности фильтра к типу TEXT
                        if filter in [s["name"] for s in text_filters]:
                            full_filter = [
                                s for s in text_initial_filters
                                if initial_filter == s["name"]
                            ][0]
                            filter_values = [
                                s for s in text_filters if s["name"] == filter
                            ]
                            filter_initial_values = [
                                s for s in text_initial_filters
                                if s["name"] == initial_filter
                            ]

                            # Распознаём значение для названия фильтра
                            found_words, found_initial_words, ref_sentence = (
                                find_similarity(
                                    filter_values[0]["value"],
                                    filter_initial_values[0]["value"],
                                    [s for s in preprocessed_sentence],
                                    threshold,
                                    first_entry=False,
                                ))
                            if ref_sentence != preprocessed_sentence:
                                preprocessed_sentence = ref_sentence
                                filters_and_values.append({
                                    "name":
                                    filter,
                                    "initial_name":
                                    initial_filter,
                                    "value":
                                    found_words,
                                    "initial_value":
                                    found_initial_words,
                                    "type":
                                    full_filter["type"],
                                    "id_native_filter":
                                    full_filter["id_native_filter"],
                                })
                        # Проверка принадлежности фильтра к типу DATE
                        if filter in [s["name"] for s in date_filters]:
                            # Поиск для названия фильтра даты
                            pr_sentence, ref_sentence, filter_and_value = (
                                date_recognizer_filter(
                                    sentence,
                                    filter,
                                    date_initial_filters,
                                    date_filters,
                                    initial_filter,
                                    [s for s in preprocessed_sentence],
                                ))
                            if filter_and_value != None:
                                preprocessed_sentence = pr_sentence
                                sentence = ref_sentence
                                filters_and_values.append(filter_and_value)
                                date_find_state = True
                # Поиск значений фильтров по остаточным словам
                if preprocessed_sentence != []:
                    # Поиск текстовых фильтров
                    for filter, initial_filter in zip(text_filters,
                                                      text_initial_filters):
                        found_words, found_initial_words, ref_sentence = find_similarity(
                            filter["value"],
                            initial_filter["value"],
                            [s for s in preprocessed_sentence],
                            threshold,
                            first_entry=False,
                        )

                        if preprocessed_sentence != ref_sentence:
                            preprocessed_sentence = ref_sentence
                            filters_and_values.append({
                                "name":
                                filter["name"],
                                "initial_name":
                                initial_filter["name"],
                                "value":
                                found_words,
                                "initial_value":
                                found_initial_words,
                                "type":
                                initial_filter["type"],
                                "id_native_filter":
                                initial_filter["id_native_filter"],
                            })
                        if preprocessed_sentence == []:
                            break
                    # Поиск дат
                    if date_find_state == False:
                        pr_sentence, ref_sentence, filter_and_value = (
                            date_recognize_filter_first(
                                sentence,
                                [s for s in preprocessed_sentence],
                                date_filters,
                                date_initial_filters,
                            ))
                        if filter_and_value != None:
                            preprocessed_sentence = pr_sentence
                            sentence = ref_sentence
                            filters_and_values.append(filter_and_value)
                            date_find_state = True
            print(filters_and_values)
            # составляем url строку

            native_filters = []
            for filters_and_value in filters_and_values:
                if filters_and_value["type"] == "date":
                    native_filters.append(
                        dashboard_native_filter_date_range(
                            filters_and_value["id_native_filter"],
                            filters_and_value["initial_value"],
                        ))
                else:
                    native_filters.append(
                        dashboard_native_filter_create(
                            filters_and_value["id_native_filter"],
                            filters_and_value["initial_name"],
                            filters_and_value["initial_value"],
                        ))

                # native_filters.append(f'{filters_and_value["id_native_filter"]}:(__cache:(label:\'{" and ".join(filters_and_value["initial_value"])}\',validateStatus:!f,value:!(\'{", ".join(filters_and_value["initial_value"])}\')),extraFormData:(filters:!((col:{filters_and_value["initial_name"]},op:IN,val:!(\'{", ".join(filters_and_value["initial_value"])}\')))),filterState:(label:\'{" and ".join(filters_and_value["initial_value"])}\',validateStatus:!f,value:!(\'{", ".join(filters_and_value["initial_value"])}\')),id:{filters_and_value["id_native_filter"]},ownState:())')

            print(native_filters)

            str_native_filter = ""
            for i, native_filter in enumerate(native_filters):
                str_native_filter += native_filter
                if i < len(native_filters) - 1:
                    str_native_filter += ","

            url = f'http://localhost:8088/superset/dashboard/{[s["url"] for s in dashboards if found_initial_dashboards[0] == s["value"]][0]}/?native_filters=({str_native_filter})'
            print(url)
            # составляем ответ с распознанными сущностями:
            # распознанные дашборды
            # распознанные фильтры и их значения
            # распознанные действия
            response_with_description = {
                "filters": filters_and_values,
                "dashboards": dashboard,
                "command": found_initial_commands
            }
            response_with_description_json = json.dumps(
                response_with_description, ensure_ascii=False)
            return url, filters_and_values, response_with_description, text

        # если команда создать график
        # -----------------------------------------------------------
        # ***********************************************************
        # -----------------------------------------------------------
        # if state_create_chart:
        #     response_with_description = {
        #         "filters": filters_and_values,
        #         "dashboards": dashboard,
        #         "command": found_initial_commands
        #     }
        #     response_with_description_json = json.dumps(
        #         response_with_description, ensure_ascii=False)
        #     return url, filters_and_values, response_with_description, text
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if state_change_dashboard:
            base_url = SUPERSET_HOST
            superset_api_url = f"{SUPERSET_HOST}/api/v1"
            payload = {
                "username": "admin",
                "password": "admin",
                "provider": "db"
            }
            r = requests.post(base_url + "/api/v1/security/login",
                              json=payload)

            access_token = r.json()
            print(access_token)

            headersAuth = {
                "Authorization": "Bearer " + access_token["access_token"]
            }

            # неизменная часть payload
            url_dashboard = [
                    s['url'] for s in dashboards
                    if found_initial_dashboards[0] == s["value"]
                ][0]
            # логика построения payload
            name_of_chart = "Таблица"
            found_filters_names = found_initial_words
            print(found_filters_names)
            json_filters = json.dumps(found_filters_names, ensure_ascii=False)
            filters_for_payload = [{
                "clause": "WHERE",
                "subject": "Дата",
                "operator": "TEMPORAL_RANGE",
                "comparator": "No filter",
                "expressionType": "SIMPLE"
            }]
            filters_json = json.dumps(filters_for_payload, ensure_ascii=False)
            print(f""""adhoc_filters":{filters_json},""")
            table_chart_payload = {
                "datasource_id":
                24,  # // ID источника данных для визуализации.
                "datasource_name":
                "data",  # // Название источника данных.
                "datasource_type":
                "table",  # // Тип источника данных, например 'sl_table' для Superset.
                "is_managed_externally":
                "true",
                "dashboards": [f"{url_dashboard}"],
                "query_context_generation":
                "true",
                "slice_name":
                name_of_chart,  # // Название создаваемого среза (визуализации).
                "viz_type":
                "table",  # // Вид визуализации
                "params":
                '{"datasource":"24__table",'
                '"query_mode":"aggregate",'
                '"granularity_sqla":"Дата",'  # // Значение по x
                '"time_grain_sqla":"P1D",'
                f'"time_range":"No filter",'
                '"metrics":[],'  # //Ззначение по y
                f""""adhoc_filters":{filters_json},"""
                # '"adhoc_filters":[{"clause":"WHERE",'
                # '"subject":"Дата",'  # // Фильтр
                # '"operator":"TEMPORAL_RANGE",'
                # '"comparator":"No filter",'
                # '"expressionType":"SIMPLE"}],'
                f'"groupby":{json_filters},'  # // Группировки
                '"order_desc":true,'
                '"row_limit":50000,'
                '"color_scheme":"supersetColors",'
                '"show_brush":"auto",'
                '"show_legend":true,'
                '"rich_tooltip":true,'
                '"line_interpolation":"linear",'
                '"bottom_margin":"auto",'
                '"x_ticks_layout":"auto",'
                '"x_axis_format":"smart_date",'
                '"left_margin":"auto",'
                '"y_axis_format":"SMART_NUMBER",'
                '"y_axis_bounds":[null,null],'
                '"rolling_type":"None",'
                '"comparison_type":"values",'
                '"annotation_layers":[],'
                '"extra_form_data":{},'
                '"dashboards":[]}',
            }
            json_payload = table_chart_payload
            url_after_create_chart = (f"http://localhost:8088/superset/dashboard/{url_dashboard}")
            response_with_description = {
                "filters": filters_and_values,
                "dashboards": dashboard,
                "command": found_initial_commands
            }
            line_chart_response = requests.post(
                f"{superset_api_url}/chart/",
                headers=headersAuth,
                json=json_payload,
            )
            return url_after_create_chart, filters_and_values, response_with_description, text
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # if state_filter_dashboard:
        #     found_initial_commands = ['открой']
        #     response_with_description = {
        #         "filters": filters_and_values,
        #         "dashboards": dashboard,
        #         "command": found_initial_commands
        #     }
        #     response_with_description_json = json.dumps(
        #         response_with_description, ensure_ascii=False)
        #     return url, filters_and_values, response_with_description, text
        # state_create_chart = False
        if state_create_chart:
            # ищем тип графика
            types_of_charts = [
                "круговая диаграмма",
                "линейный график",
                "таблица",
                "гистограмма",
            ]

            state_pie_chart = False
            state_table = False
            state_line_chart = False
            state_bar_chart = False

            state_found_types_of_charts = False

            found_types_of_charts_words = []
            found_initial_types_of_charts = []

            types_of_charts = [
                "круговая диаграмма",
                "линейный график",
                "таблица",
                "гистограмма",
            ]
            lemma_types_of_charts = [
                ["круговой", "диаграмма"],
                ["линейный", "график"],
                ["таблица"],
                ["гистограмма"],
            ]
            found_words, found_initial_words, ref_sentence = find_similarity(
                [s for s in lemma_types_of_charts],
                [s for s in types_of_charts],
                [s for s in preprocessed_sentence],
                threshold,
                first_entry=False,
            )
            print(f"{found_words}\n{found_initial_words}\n{ref_sentence}")

            if ref_sentence != preprocessed_sentence:
                state_found_types_of_charts = True
                preprocessed_sentence = ref_sentence
                found_types_of_charts_words = found_words
                found_initial_types_of_charts = found_initial_words
            if found_initial_words[0] == "круговая диаграмма":
                state_pie_chart = True
            elif found_initial_words[0] == "линейный график":
                state_line_chart = True
            elif found_initial_words[0] == "таблица":
                state_table = True
            elif found_initial_words[0] == "гистограмма":
                state_bar_chart = True

            # -----------------------------------------------------------
            # ***********************************************************
            # -----------------------------------------------------------
            # ищем дашборд
            threshold = 0.8

            found_dashboards_words = []
            found_initial_dashboards = []

            state_found_dashboard = False

            found_words, found_initial_words, ref_sentence = find_similarity(
                [s["value"] for s in lemma_dashboard],
                [s["value"] for s in dashboards],
                [s for s in preprocessed_sentence],
                threshold,
                first_entry=True,
            )

            if ref_sentence != preprocessed_sentence:
                state_found_dashboard = True
                preprocessed_sentence = ref_sentence
                found_dashboards_words = found_words
                found_initial_dashboards = found_initial_words
                url_dashboard = [
                    s['url'] for s in dashboards
                    if found_initial_dashboards[0] == s["value"]
                ][0]
            # -----------------------------------------------------------
            # ***********************************************************
            # -----------------------------------------------------------

            # ищем фильтры для построения графика
            print(filter_values)
            # print(filter_initial_values)
            print(filter_names)

            print([s for s in filter_names])
            print(f"lemma_filters: {lemma_filters}")
            filter_initial_names = []
            for i in filter_names:
                filter_initial_names.append([i])
            print(filter_initial_names)
            found_words, found_initial_words, ref_sentence = find_similarity(
                [s["name"] for s in lemma_filters],
                [s["name"] for s in target_words],
                [s for s in preprocessed_sentence],
                threshold,
                first_entry=False,
            )
            print(
                f"{found_words}\n найденные названия фильтров: {found_initial_words}\n{ref_sentence}"
            )
            found_filters_names = found_initial_words

            # -----------------------------------------------------------
            # ***********************************************************
            # -----------------------------------------------------------
            found_filter_keys = []
            found_initial_filters_words = []
            filters_and_values = []
            if state_found_dashboard:

                dashboards_filters = [
                    s for s in lemma_filters
                    if s["dashboard"] == found_dashboards_words[0]
                ]
                dashboard_initial_filters = [
                    s for s in target_words
                    if s["dashboard"] == found_initial_dashboards[0]
                ]

                # Распознаём названия фильтров
                found_words, found_initial_words, ref_sentence = find_similarity(
                    [s["name"] for s in lemma_filters],
                    [s["name"] for s in target_words],
                    [s for s in preprocessed_sentence],
                    threshold,
                    first_entry=False,
                )
                print(
                    f"{found_words}\n найденные слова: {found_initial_words}\n{ref_sentence}"
                )
                text_filters = [
                    s for s in dashboards_filters if s["type"] == "text"
                ]
                text_initial_filters = [
                    s for s in dashboard_initial_filters if s["type"] == "text"
                ]

                date_filters = [
                    s for s in dashboards_filters if s["type"] == "date"
                ]
                date_initial_filters = [
                    s for s in dashboard_initial_filters if s["type"] == "date"
                ]

                date_find_state = False

                if ref_sentence != preprocessed_sentence:
                    preprocessed_sentence = ref_sentence
                    found_filter_keys = found_words
                    found_initial_filters_words = found_initial_words

                    for filter, initial_filter in zip(
                            found_filter_keys, found_initial_filters_words):
                        print(filters_and_values)
                        # Проверка принадлежности фильтра к типу TEXT
                        if filter in [s["name"] for s in text_filters]:
                            full_filter = [
                                s for s in text_initial_filters
                                if initial_filter == s["name"]
                            ][0]
                            filter_values = [
                                s for s in text_filters if s["name"] == filter
                            ]
                            filter_initial_values = [
                                s for s in text_initial_filters
                                if s["name"] == initial_filter
                            ]

                            # Распознаём значение для названия фильтра
                            found_words, found_initial_words, ref_sentence = (
                                find_similarity(
                                    filter_values[0]["value"],
                                    filter_initial_values[0]["value"],
                                    [s for s in preprocessed_sentence],
                                    threshold,
                                    first_entry=False,
                                ))
                            if ref_sentence != preprocessed_sentence:
                                preprocessed_sentence = ref_sentence
                                filters_and_values.append({
                                    "name":
                                    filter,
                                    "initial_name":
                                    initial_filter,
                                    "value":
                                    found_words,
                                    "initial_value":
                                    found_initial_words,
                                    "type":
                                    full_filter["type"],
                                    "id_native_filter":
                                    full_filter["id_native_filter"],
                                })
                        # Проверка принадлежности фильтра к типу DATE
                        if filter in [s["name"] for s in date_filters]:
                            # Поиск для названия фильтра даты
                            pr_sentence, ref_sentence, filter_and_value = (
                                date_recognizer_filter(
                                    sentence,
                                    filter,
                                    date_initial_filters,
                                    date_filters,
                                    initial_filter,
                                    [s for s in preprocessed_sentence],
                                ))
                            print()
                            if filter_and_value != None:
                                preprocessed_sentence = pr_sentence
                                sentence = ref_sentence
                                filters_and_values.append(filter_and_value)
                                date_find_state = True
                # Поиск значений фильтров по остаточным словам
                if preprocessed_sentence != []:
                    # Поиск текстовых фильтров
                    for filter, initial_filter in zip(text_filters,
                                                      text_initial_filters):
                        found_words, found_initial_words, ref_sentence = find_similarity(
                            filter["value"],
                            initial_filter["value"],
                            [s for s in preprocessed_sentence],
                            threshold,
                            first_entry=False,
                        )

                        if preprocessed_sentence != ref_sentence:
                            preprocessed_sentence = ref_sentence
                            filters_and_values.append({
                                "name":
                                filter["name"],
                                "initial_name":
                                initial_filter["name"],
                                "value":
                                found_words,
                                "initial_value":
                                found_initial_words,
                                "type":
                                initial_filter["type"],
                                "id_native_filter":
                                initial_filter["id_native_filter"],
                            })
                        if preprocessed_sentence == []:
                            break
                    # Поиск дат
                    if date_find_state == False:
                        pr_sentence, ref_sentence, filter_and_value = (
                            date_recognize_filter_first(
                                sentence,
                                [s for s in preprocessed_sentence],
                                date_filters,
                                date_initial_filters,
                            ))
                        if filter_and_value != None:
                            preprocessed_sentence = pr_sentence
                            sentence = ref_sentence
                            filters_and_values.append(filter_and_value)
                            date_find_state = True

            filters_for_payload = []
            for i in filters_and_values:
                if i["type"] != "date":
                    filters_for_payload.append({
                        "clause": "WHERE",
                        "subject": i["initial_name"],
                        "operator": "IN",
                        "comparator": i["initial_value"],
                        "expressionType": "SIMPLE"
                    })
            print(filters_for_payload)
            if len(filters_for_payload) == 0:
                filters_for_payload = [{
                    "clause": "WHERE",
                    "subject": "Дата",
                    "operator": "TEMPORAL_RANGE",
                    "comparator": "No filter",
                    "expressionType": "SIMPLE"
                }]
            filters_json = json.dumps(filters_for_payload, ensure_ascii=False)
            print(f""""adhoc_filters":{filters_json},""")

            # filter_names_json = json.dumps(filter_names, ensure_ascii=False)
            # -----------------------------------------------------------
            # ***********************************************************
            # -----------------------------------------------------------
            # выбираем дату из текста
            if date_find_state:
                found_time_range = ""
                start_date = ""
                end_date = ""
                for s in filters_and_values:
                    if s["type"] == "date":
                        found_time_range = s["value"]
                        start_date = s["value"][0]
                        end_date = s["value"][1]
                # date_obj = datetime.strptime(start_date, "%d-%m-%Y")

                # # Преобразование в нужный формат
                # start_date = date_obj.strftime("%Y-%m-%d")

                # date_obj = datetime.strptime(end_date, "%d-%m-%Y")

                # # Преобразование в нужный формат
                # end_date = date_obj.strftime("%Y-%m-%d")
                time_range = f"{start_date} : {end_date}"
                print(found_time_range)
            else:
                time_range = "No filter"
            # -----------------------------------------------------------
            # ***********************************************************
            # -----------------------------------------------------------

            # -----------------------------------------------------------
            # делаем запрос для создания графика
            # -----------------------------------------------------------

            # неизменная часть payload

            # логика построения payload
            name_of_chart = "Заявки"
            print(found_filters_names)
            json_filters = json.dumps(found_filters_names, ensure_ascii=False)

            # Парсинг строки в объект даты

            if state_line_chart:
                line_chart_payload = {
                    "datasource_id":
                    24,  # // ID источника данных для визуализации.
                    "datasource_name":
                    "data",  # // Название источника данных.
                    "datasource_type":
                    "table",  # // Тип источника данных, например 'sl_table' для Superset.
                    "is_managed_externally":
                    "true",
                    "dashboards": [f"{url_dashboard}"],  # ********************
                    "query_context_generation":
                    "true",
                    "slice_name":
                    name_of_chart,  # // Название создаваемого среза (визуализации). # ********************
                    "viz_type":
                    "line",  # // Вид визуализации # ********************
                    "params":
                    '{"datasource":"24__table",'
                    '"granularity_sqla":"Дата",'  # // Значение по x
                    f'"time_range": "{time_range}",'  # ********************
                    '"metrics":["count"],'  # //Ззначение по y
                    f""""adhoc_filters":{filters_json},"""
                    # '"adhoc_filters":[{"clause":"WHERE",'
                    # '"subject":"Дата",'  # // Фильтр
                    # '"operator":"TEMPORAL_RANGE",'
                    # '"comparator":"No filter",'
                    # '"expressionType":"SIMPLE"}],'
                    f'"groupby":{json_filters},'  # // Группировки # ********************
                    '"order_desc":true,'
                    '"row_limit":50000,'
                    '"color_scheme":"supersetColors",'
                    '"show_brush":"auto",'
                    '"show_legend":true,'
                    '"rich_tooltip":true,'
                    '"line_interpolation":"linear",'
                    '"bottom_margin":"auto",'
                    '"x_ticks_layout":"auto",'
                    '"x_axis_format":"smart_date",'
                    '"left_margin":"auto",'
                    '"y_axis_format":"SMART_NUMBER",'
                    '"y_axis_bounds":[null,null],'
                    '"rolling_type":"None",'
                    '"comparison_type":"values",'
                    '"annotation_layers":[],'
                    '"extra_form_data":{},'
                    '"dashboards":[]}',
                }
                json_payload = line_chart_payload
                print(line_chart_payload)

            elif state_pie_chart:
                pie_chart_payload = {
                    "datasource_id":
                    24,  # // ID источника данных для визуализации.
                    "datasource_name":
                    "data",  # // Название источника данных.
                    "datasource_type":
                    "table",  # // Тип источника данных, например 'sl_table' для Superset.
                    "is_managed_externally":
                    "true",
                    "dashboards": [f"{url_dashboard}"],
                    "query_context_generation":
                    "true",
                    "slice_name":
                    name_of_chart,  # // Название создаваемого среза (визуализации).
                    "viz_type":
                    "pie",  # // Вид визуализации
                    "params":
                    '{"datasource":"24__table",'
                    '"metric":"count",'  # //Ззначение по y
                    f""""adhoc_filters":{filters_json},"""
                    # '"adhoc_filters":[{"clause":"WHERE",'
                    # '"subject":"Дата",'  # // Фильтр
                    # '"operator":"TEMPORAL_RANGE",'
                    # '"comparator":"No filter",'
                    # '"expressionType":"SIMPLE"}],'
                    f'"groupby":{json_filters},'  # // Группировки
                    '"label_type":"key_percent",'
                    '"order_desc":true,'
                    '"row_limit":5000,'
                    '"sort_by_metric":true,'
                    '"show_labels_threshold":5,'
                    '"innerRadius":30,'
                    '"donut":false,'
                    '"outerRadius":71,'
                    '"legendType":"scroll",'
                    '"legendOrientation":"top",'
                    '"legendMargin":null,'
                    '"label_type":"key_percent",'
                    '"number_format":"SMART_NUMBER",'
                    '"date_format":"smart_date",'
                    '"show_labels":true,'
                    '"labels_outside":true,'
                    '"color_scheme":"supersetColors",'
                    '"show_brush":"auto",'
                    '"show_legend":true,'
                    '"rich_tooltip":true,'
                    '"line_interpolation":"linear",'
                    '"bottom_margin":"auto",'
                    '"x_ticks_layout":"auto",'
                    '"x_axis_format":"smart_date",'
                    '"left_margin":"auto",'
                    '"y_axis_format":"SMART_NUMBER",'
                    '"y_axis_bounds":[null,null],'
                    '"rolling_type":"None",'
                    '"comparison_type":"values",'
                    '"annotation_layers":[],'
                    '"extra_form_data":{},'
                    '"dashboards":[]}',
                }
                json_payload = pie_chart_payload
                print(pie_chart_payload)
            elif state_table:
                # time_range = '20-03-2023 : 15-04-2023'
                table_chart_payload = {
                    "datasource_id":
                    24,  # // ID источника данных для визуализации.
                    "datasource_name":
                    "data",  # // Название источника данных.
                    "datasource_type":
                    "table",  # // Тип источника данных, например 'sl_table' для Superset.
                    "is_managed_externally":
                    "true",
                    "dashboards": [f"{url_dashboard}"],
                    "query_context_generation":
                    "true",
                    "slice_name":
                    name_of_chart,  # // Название создаваемого среза (визуализации).
                    "viz_type":
                    "table",  # // Вид визуализации
                    "params":
                    '{"datasource":"24__table",'
                    '"query_mode":"aggregate",'
                    '"granularity_sqla":"Дата",'  # // Значение по x
                    '"time_grain_sqla":"P1D",'
                    f'"time_range":"{time_range}",'
                    '"metrics":["count"],'  # //Ззначение по y
                    f""""adhoc_filters":{filters_json},"""
                    # '"adhoc_filters":[{"clause":"WHERE",'
                    # '"subject":"Дата",'  # // Фильтр
                    # '"operator":"TEMPORAL_RANGE",'
                    # '"comparator":"No filter",'
                    # '"expressionType":"SIMPLE"}],'
                    f'"groupby":{json_filters},'  # // Группировки
                    '"order_desc":true,'
                    '"row_limit":50000,'
                    '"color_scheme":"supersetColors",'
                    '"show_brush":"auto",'
                    '"show_legend":true,'
                    '"rich_tooltip":true,'
                    '"line_interpolation":"linear",'
                    '"bottom_margin":"auto",'
                    '"x_ticks_layout":"auto",'
                    '"x_axis_format":"smart_date",'
                    '"left_margin":"auto",'
                    '"y_axis_format":"SMART_NUMBER",'
                    '"y_axis_bounds":[null,null],'
                    '"rolling_type":"None",'
                    '"comparison_type":"values",'
                    '"annotation_layers":[],'
                    '"extra_form_data":{},'
                    '"dashboards":[]}',
                }
                json_payload = table_chart_payload

            elif state_bar_chart:
                bar_chart_payload = {
                    "datasource_id":
                    24,  # // ID источника данных для визуализации.
                    "datasource_name":
                    "data",  # // Название источника данных.
                    "datasource_type":
                    "table",  # // Тип источника данных, например 'sl_table' для Superset.
                    "is_managed_externally":
                    "true",
                    "dashboards": [f"{url_dashboard}"],
                    "query_context_generation":
                    "true",
                    "slice_name":
                    name_of_chart,  # // Название создаваемого среза (визуализации).
                    "viz_type":
                    "echarts_timeseries_bar",  # // Вид визуализации
                    "params":
                    '{"datasource":"24__table",'
                    '"granularity_sqla":"Дата",'  # // Значение по x (сделать возможность выбора типа даты)
                    f'"time_range":"{time_range}",'
                    '"metrics":["count"],'  # //Ззначение по y
                    f""""adhoc_filters":{filters_json},"""
                    # '"adhoc_filters":[{"clause":"WHERE",'
                    # '"subject":"Дата",'  # // Фильтр
                    # '"operator":"TEMPORAL_RANGE",'
                    # '"comparator":"No filter",'
                    # '"expressionType":"SIMPLE"}],'
                    f'"groupby":{json_filters},'  # // Группировки
                    '"order_desc":true,'
                    '"row_limit":50000,'
                    '"color_scheme":"supersetColors",'
                    '"show_brush":"auto",'
                    '"show_legend":true,'
                    '"rich_tooltip":true,'
                    '"line_interpolation":"linear",'
                    '"bottom_margin":"auto",'
                    '"x_ticks_layout":"auto",'
                    '"x_axis_format":"smart_date",'
                    '"left_margin":"auto",'
                    '"y_axis_format":"SMART_NUMBER",'
                    '"y_axis_bounds":[null,null],'
                    '"rolling_type":"None",'
                    '"comparison_type":"values",'
                    '"annotation_layers":[],'
                    '"extra_form_data":{},'
                    '"dashboards":[]}',
                }
                json_payload = bar_chart_payload


            # url для открытия дашборда после создания графика
            url_after_create_chart = f"http://localhost:8088/superset/dashboard/{url_dashboard}"
            # url для открытия графика после его создания

            # id_of_chart = ''
            # url_of_chart = f"http://localhost:8088/explore/?slice_id={id_of_chart}"

            # r = requests.get(base_url + '/api/v1/dashboard/', headers=headersAuth)
            # resp_dashboard = r.json()
            # json_str = json.dumps(resp_dashboard, ensure_ascii=False, indent=4)
            # print(json_str)
            # составляем ответ с распознанными сущностями:
            # распознанные дашборды
            # распознанные фильтры и их значения
            # распознанные действия
            response_with_description = {
                "filters": filters_and_values,
                "dashboards": dashboard,
                "command": found_initial_commands
            }

            response_with_description_json = json.dumps(
                response_with_description, ensure_ascii=False)
            # возвращаем ответ
            
            # данные для запроса
            base_url = SUPERSET_HOST
            superset_api_url = f"{SUPERSET_HOST}/api/v1"
            payload = {
                "username": "admin",
                "password": "admin",
                "provider": "db"
            }
            # url_dashboard = 15
            r = requests.post(base_url + "/api/v1/security/login",
                              json=payload)

            access_token = r.json()
            print(access_token)

            headersAuth = {
                "Authorization": "Bearer " + access_token["access_token"]
            }
            line_chart_response = requests.post(
                f"{superset_api_url}/chart/",
                headers=headersAuth,
                json=json_payload,
            )
            found_filters = []
            if (len(filters_and_values) == 0):
                for s in found_filters_names:
                    found_filters.append(s)
                filters_and_values.append({"Названия фильтров: ": found_filters})
            
            print(line_chart_response.status_code)
            print(line_chart_response.text)
            print(line_chart_response.json())
            return url_after_create_chart, filters_and_values, response_with_description, text
        # -----------------------------------------------------------
        # ***********************************************************
        # -----------------------------------------------------------
    except (Exception) as error:
        print("Ошибка", error)
        return 'null'
