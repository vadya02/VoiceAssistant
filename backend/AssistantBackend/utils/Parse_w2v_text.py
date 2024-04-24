import os
import re

import nltk
import psycopg2
from AssistantBackend.settings import (
    DB_NAME,
    HOST,
    NLTK_RESOURCES,
    PASSWORD,
    PORT,
    USER,
    WORD2VEC_MODEL,
)
from AssistantBackendApp.models import Dashboards, Filters, FilterValues, RequestHistory
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from pymorphy3 import MorphAnalyzer

load_dotenv("../../.env")
model = WORD2VEC_MODEL.model
stopwords = NLTK_RESOURCES.stop_words

stop_words = stopwords

# Инициализация объекта для лемматизации
morph = MorphAnalyzer()


def ParseKeywords(text):
    try:
        dbname = DB_NAME
        print(dbname)
        user = USER
        print(user)
        password = PASSWORD
        host = HOST
        port = PORT
        dashboards = []
        target_words = []
        # Установка соединения
        #   try:
        connection = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        print("Подключение к базе данных PostgreSQL установлено.")

        dashboards_data = Dashboards.objects.values_list("table_name", "url")

        dashboards = [
            {"name": "дашборд", "value": item[0], "url": item[1]}
            for item in dashboards_data
        ]



        print(dashboards)
        # Теперь вы можете выполнить запросы SQL с помощью этого соединения

        # Пример: создание курсора и выполнение запроса
        # cursor = connection.cursor()
        # cursor.execute("SELECT table_name, url FROM dashboards")
        # records = cursor.fetchall()

        # for record in records:
        #     dashboards.append({"name": "дашборд", "value": record[0], "url": record[1]})

        # получене дашборда
        print(dashboards)

        for dashbord in dashboards:
            dashboard = Dashboards.objects.get(table_name = dashbord["value"])
            filters_by_dashboard = Filters.objects.filter(fk_dashboard = dashboard).values_list('filter_name', 'id_native_filter')

            filters = [
                {"filter_name": item[0], "id_native_filter": item[1]}
                for item in filters_by_dashboard
            ]

            print(filters)

            for filter_i in filters:
                filter = Filters.objects.get(filter_name = filter_i["filter_name"])
                filter_value_by_filter = FilterValues.objects.filter(fk_filter = filter).values_list('filter_value')
                filter_values = [
                    {"filter_value": item[0]}
                    for item in filter_value_by_filter
                ]
                values = []
                for value in filter_values:
                    values.append(value['filter_value'])
                print(filter_values)
                target_words.append(
                    {
                        "name": filter_i["filter_name"],
                        "value": values,
                        "dashboard": dashbord["value"],
                        "id_native_filter": filter_i["id_native_filter"],
                    }
                )



            # выбираем фильтры по дашборду
            # cursor.execute(
            #     "SELECT filters.filter_name, filters.id_native_filter  FROM dashboards, filters WHERE dashboards.table_name = %(used_dashboard)s and dashboards.id = filters.id_dashboard",
            #     {"used_dashboard": dashbord["value"]},
            # )
            # print("дошел до 50 строки")
            # records = cursor.fetchall()
            # print(f"Record: {records}")

            # выбираем значения фильтров по фильтрам
            # for record in records:
            #     id_native_filter = re.sub("['(),]", "", str(record[1]))
            #     record = re.sub("['(),]", "", str(record[0]))
            #     cursor.execute(
            #         "SELECT filter_values.filter_value FROM dashboards,  filters, filter_values WHERE dashboards.table_name =   %(used_dashboard)s and dashboards.id = filters.id_dashboard and  filters.filter_name = %(used_filter)s and filters.id =  filter_values.id_filter",
            #         {"used_dashboard": dashbord["value"], "used_filter": record},
            #     )
            #     filer_values = cursor.fetchall()
            #     values = []
            #     for value in filer_values:
            #         values.append(re.sub("['(),]", "", str(value)))
            #     target_words.append(
            #         {
            #             "name": record,
            #             "value": values,
            #             "dashboard": dashbord["value"],
            #             "id_native_filter": id_native_filter,
            #         }
            #     )

        print(dashboards)
        print(target_words)
        # cursor.close()
        connection.close()
        print("Соединение с базой данных закрыто.")

        #   except (Exception, psycopg2.Error) as error:
        #       print("Ошибка при подключении к базе данных PostgreSQL:", error)

        # Функция для лемматизации и удаления стоп-слов из предложения

        # Пример предложения
        sentence = text

        # Применяем предобработку к предложению
        preprocessed_sentence = preprocess_text(sentence)

        print(preprocessed_sentence)

        lemma_dashboard = []
        for dashboard in dashboards:
            lemma_dashboard.append(
                {
                    "name": dashboard["name"],
                    "value": preprocess_text(dashboard["value"])[0],
                }
            )
        print(lemma_dashboard)

        lemma_filters = []
        for filter in target_words:
            print(filter)
            lemma_filters.append(
                {
                    "name": filter["name"],
                    "value": preprocess_text(" ".join(filter["value"])),
                    "dashboard": preprocess_text(filter["dashboard"])[0],
                }
            )
        print(lemma_filters)

        threshold = 0.65
        # поиск дашборда
        target_dashboards_vectors = []

        for target_word in lemma_dashboard:
            word = target_word["value"]
            if word in model:
                target_dashboards_vectors.append(model[word])

        found_dashboards_words = []
        found_initial_dashboards = []
        for input_word in preprocessed_sentence:
            if input_word in model:
                input_word_vector = model[input_word]
                for target_dashboards_vector, target_word, dashboard in zip(
                    target_dashboards_vectors, lemma_dashboard, dashboards
                ):
                    similarity = model.similarity(input_word, target_word["value"])
                    if similarity > threshold:
                        found_dashboards_words.append(target_word["value"])
                        found_initial_dashboards.append(dashboard["value"])
        print(found_dashboards_words)
        print(found_initial_dashboards)

        target_filters_vectors = []

        for target_word in lemma_filters:
            if target_word["dashboard"] in found_dashboards_words:
                for word in target_word["value"]:
                    if word in model:
                        target_filters_vectors.append(model[word])

        #   print(target_filters_vectors)
        # print(lemma_filters)
        found_filters_words = []
        found_filter_keys = []
        found_id_native_filter_keys = []
        for input_word in preprocessed_sentence:
            if input_word in model:
                input_word_vector = model[input_word]
                for target_filters_vector, target_word, initial_filter in zip(
                    target_filters_vectors, lemma_filters, target_words
                ):
                    # print(target_word['value'])
                    for word in target_word["value"]:
                        # print(word)
                        similarity = model.similarity(input_word, word)
                        if similarity > threshold:
                            if not initial_filter["name"] in found_filter_keys:
                                found_filters_words.append(
                                    initial_filter["value"][
                                        target_word["value"].index(word)
                                    ]
                                )
                                found_filter_keys.append(initial_filter["name"])
                                found_id_native_filter_keys.append(
                                    initial_filter["id_native_filter"]
                                )
        print(found_filters_words)
        print(found_filter_keys)
        print(found_id_native_filter_keys)
        print(found_initial_dashboards)

        # составляем url строку

        native_filters = []
        for filters_words, filter_keys, id_native_filter_keys in zip(
            found_filters_words, found_filter_keys, found_id_native_filter_keys
        ):
            native_filters.append(
                f"{id_native_filter_keys}:(__cache:(label:'{filters_words}',validateStatus:!f,value:!('{filters_words}')),extraFormData:(filters:!((col:{filter_keys},op:IN,val:!('{filters_words}')))),filterState:(label:'{filters_words}',validateStatus:!f,value:!('{filters_words}')),id:{id_native_filter_keys},ownState:())"
            )

        print(native_filters)

        str_native_filter = ""
        for i, native_filter in enumerate(native_filters):
            str_native_filter += native_filter
            if i < len(native_filters) - 1:
                str_native_filter += ","
        superset_host = os.getenv("SUPERSET_HOST")
        url = f"{superset_host}superset/dashboard/{found_initial_dashboards[0]}/?native_filters=({str_native_filter})"
        print(url)

        return url
    except Exception as e:
        print(f"message_error: {e}")


#   found_keys = []
#   names = []
#   for value in found_filter_keys:
#       # Проход по каждому словарю
#       for dictionary in target_words:
#           # Проверка, содержится ли значение в словаре
#           if value in dictionary.values():
#               print(value)
#               name = dictionary.get("name")
#               names.append(name)
#               # Если содержится, добавляем название ключа в список найденных   ключей
#               found_keys.append([key for key, val in dictionary.items() if val ==   value])

#   print("Найденные ключи для каждого значения:")

#   print(names)
#   for keys in found_keys:
#       print(keys)
#   return found_keys[0]


def preprocess_text(text):
    # Разбиваем текст на слова
    words = nltk.word_tokenize(text)
    # Приводим слова к нижнему регистру и лемматизируем
    lemmatized_words = [morph.parse(word.lower())[0].normal_form for word in words]
    # Удаляем стоп-слова
    filtered_words = [word for word in lemmatized_words if word not in stop_words]
    return filtered_words
