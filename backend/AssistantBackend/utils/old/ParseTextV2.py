import os
import re
from datetime import datetime, timedelta

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
from dotenv import load_dotenv

# from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from pymorphy3 import MorphAnalyzer

load_dotenv("../../.env")
model = WORD2VEC_MODEL.model
stopwords = NLTK_RESOURCES.stop_words

morph = MorphAnalyzer()

stop_words = stopwords


# Параметры подключения к базе данных
dbname = "apache-auth"
user = "postgres"
password = "root"
host = "localhost"
port = "5432"
dashboards = []
target_words = []
threshold = 0.8

def ParseKeywordsV2(text):
    # Установка соединения
    try:
        connection = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        print("Подключение к базе данных PostgreSQL установлено.")

        # Теперь вы можете выполнить запросы SQL с помощью этого соединения

        # Пример: создание курсора и выполнение запроса
        cursor = connection.cursor()
        cursor.execute("SELECT table_name, url FROM dashboards")
        records = cursor.fetchall()
        for record in records:
            dashboards.append({"name": "дашборд", "value": record[0], "url": record[1]})
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
                    {"used_dashboard": dashbord["value"], "used_filter": filters},
                )
                filter_values = cursor.fetchall()
                values = []
                for value in filter_values:
                    values.append(re.sub("['(),]", "", str(value)))

                target_words.append(
                    {
                        "name": filters,
                        "value": values,
                        "dashboard": dashbord["value"],
                        "id_native_filter": id_native_filter,
                        "type": filter_type,
                    }
                )
        print(dashboards)
        print(target_words)

        cursor.close()
        connection.close()
        print("Соединение с базой данных закрыто.")

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к базе данных PostgreSQL:", error)

    # Функция поиска совпадений
    
    try:
        
      # Пример предложения
      sentence = text
      # sentence = "Открой закрытые новый фильм"

      # Применяем предобработку к предложению
      preprocessed_sentence = preprocess_text(sentence)

      print(preprocessed_sentence)

      lemma_dashboard = []
      for dashboard in dashboards:
          lemma_dashboard.append(
              {"name": dashboard["name"], "value": preprocess_text(dashboard["value"])}
          )
      print(lemma_dashboard)

      # изменено
      lemma_filters = []
      for filters in target_words:
          lemma_filters.append(
              {
                  "name": preprocess_text(filters["name"]),
                  "value": [preprocess_text(value) for value in filters["value"]],
                  "dashboard": preprocess_text(filters["dashboard"]),
                  "type": filters["type"],
              }
          )
      print(lemma_filters)

      

      found_dashboards_words = []
      found_initial_dashboards = []

      state_found_dashboard = False
      #ищем дашборд
      found_words, found_initial_words, ref_sentence = find_similarity(
          [s["value"] for s in lemma_dashboard],
          [s["value"] for s in dashboards],
          [s for s in preprocessed_sentence],
          threshold,
          first_entry=True,
      )
      # сравниваем обработанное предложение и изначальное, если нашли слова то удаляем их из изначального предложения
      if ref_sentence != preprocessed_sentence:
          state_found_dashboard = True
          preprocessed_sentence = ref_sentence
          found_dashboards_words = found_words
          found_initial_dashboards = found_initial_words

      print(found_dashboards_words)
      print(found_initial_dashboards)
      print(
          [s["url"] for s in dashboards if found_initial_dashboards[0] == s["value"]][0]
      )
      print(preprocessed_sentence)

      print(target_words)
      print([s for s in lemma_filters if s["dashboard"] == found_dashboards_words])
      print([s for s in target_words if s["dashboard"] == found_initial_dashboards[0]])

      if state_found_dashboard:
          found_filter_keys = []
          found_initial_filters_words = []
          filters_and_values = []
          dashboards_filters = [
              s for s in lemma_filters if s["dashboard"] == found_dashboards_words[0]
          ]
          dashboard_initial_filters = [
              s for s in target_words if s["dashboard"] == found_initial_dashboards[0]
          ]

          # Распознаём названия фильтров
          found_words, found_initial_words, ref_sentence = find_similarity(
              [s["name"] for s in lemma_filters],
              [s["name"] for s in target_words],
              [s for s in preprocessed_sentence],
              threshold,
              first_entry=False,
          )


          if ref_sentence != preprocessed_sentence:
              preprocessed_sentence = ref_sentence
              found_filter_keys = found_words
              found_initial_filters_words = found_initial_words

              text_filters = [s for s in dashboards_filters if s["type"] == "text"]
              text_initial_filters = [
                  s for s in dashboard_initial_filters if s["type"] == "text"
              ]

              date_filters = [s for s in dashboards_filters if s["type"] == "date"]
              date_initial_filters = [
                  s for s in dashboard_initial_filters if s["type"] == "date"
              ]

              for filter, initial_filter in zip(
                  found_filter_keys, found_initial_filters_words
              ):
                  # Проверка принадлежности фильтра к типу TEXT
                  if filter in [s["name"] for s in text_filters]:
                      filter_values = [s for s in text_filters if s["name"] == filter]
                      filter_initial_values = [
                          s for s in text_initial_filters if s["name"] == initial_filter
                      ]

                      # Распознаём значение для названия фильтра
                      found_words, found_initial_words, ref_sentence = find_similarity(
                          filter_values[0]["value"],
                          filter_initial_values[0]["value"],
                          [s for s in preprocessed_sentence],
                          threshold,
                          first_entry=True,
                      )

                      if ref_sentence != preprocessed_sentence:
                          preprocessed_sentence = ref_sentence
                          filters_and_values.append(
                              {
                                  "name": filter,
                                  "initial_name": initial_filter,
                                  "value": found_words[0],
                                  "initial_value": found_initial_words,
                                  "id_native_filter": [
                                      s["id_native_filter"]
                                      for s in text_initial_filters
                                      if found_initial_words[0] in s["value"]
                                  ][0],
                              }
                          )

                  # Проверка принадлежности фильтра к типу DATE
                  if filter in [s["name"] for s in date_filters]:
                      filter_values = [s for s in date_filters if s["name"] == filter]
                      filter_initial_values = [
                          s for s in date_initial_filters if s["name"] == initial_filter
                      ]

                      all_months = [
                          "январь",
                          "февраль",
                          "март",
                          "апрель",
                          "май",
                          "июнь",
                          "июль",
                          "август",
                          "сентябрь",
                          "октябрь",
                          "ноябрь",
                          "декабрь",
                      ]

                      date_range = re.search(r"(\sc\s.+\sпо\s.+($|\s))", sentence)
                      found_dates = []
                      if date_range != None:
                          # Полная дата
                          found_full_dates = re.findall(
                              r"(\d+[\.|/|\-|\s]\d+[\.|/|\-|\s]\d+)", date_range[0]
                          )
                          for date in found_full_dates:
                              spacer = re.findall(r"[\.|/|\-|\s]", date)
                              try:
                                  found_dates.append(
                                      datetime.strptime(
                                          date, f"%d{spacer[0]}%m{spacer[1]}%Y"
                                      )
                                  )
                              except ValueError as err:
                                  continue

                          # Месяцы
                          found_months = [
                              s for s in date_range[0].split(" ") if s in all_months
                          ]
                          range_years = re.findall(r"([0-9]{4})", date_range[0])
                          found_years = re.findall(
                              r"([0-9]{4})", " ".join(preprocessed_sentence)
                          )

                          sentence = sentence.replace(date_range[0], "", 1)
                          preprocessed_sentence = [
                              s
                              for s in preprocessed_sentence
                              if s not in preprocess_text(date_range[0])
                              or s not in found_months
                              or s not in found_years
                          ]

                          first_date = None
                          second_date = None

                          if len(found_dates) == 2:
                              first_date = found_dates[0]
                              second_date = found_dates[1]

                          elif len(found_months) == 2 and (
                              len(found_years) >= 0 or len(found_years) <= 3
                          ):
                              f_month = all_months.index(found_months[0]) + 1
                              s_month = all_months.index(found_months[1]) + 1
                              if len(found_years) == 0:
                                  first_date = datetime(datetime.today().year, f_month, 1)
                                  second_date = datetime(
                                      datetime.today().year, s_month, 28
                                  )
                              elif len(found_years) == 1:
                                  first_date = datetime(int(found_years[0]), f_month, 1)
                                  second_date = datetime(
                                      int(found_years[0])
                                      if s_month < 12
                                      else int(found_years[0]) + 1,
                                      s_month + 1 if s_month < 12 else 1,
                                      1,
                                  ) - timedelta(days=1)
                                  print(f"{first_date}\n{second_date}")
                              elif len(found_years) == 2:
                                  first_date = datetime(int(found_years[0]), f_month, 1)
                                  second_date = datetime(
                                      int(found_years[1])
                                      if s_month < 12
                                      else int(found_years[1]) + 1,
                                      s_month + 1 if s_month < 12 else 1,
                                      1,
                                  ) - timedelta(days=1)
                          elif len(found_months) == 0 and len(range_years) == 2:
                              first_date = datetime(int(range_years[0]), 1, 1)
                              second_date = datetime(int(range_years[1]), 12, 31)

                          if first_date != None and second_date != None:
                              filter_date = []
                              for value, initial_value in zip(
                                  filter_values[0]["value"],
                                  filter_initial_values[0]["value"],
                              ):
                                  spacer = re.findall(r"[\.|/|\-|\s]", initial_value)
                                  date = datetime.strptime(
                                      initial_value, f"%d{spacer[0]}%m{spacer[1]}%Y"
                                  )
                                  if date >= first_date and date <= second_date:
                                      filter_date.append(initial_value)
                              if filter_date != []:
                                  filters_and_values.append(
                                      {
                                          "name": filter,
                                          "initial_name": initial_filter,
                                          "value": filter_date,
                                          "initial_value": filter_date,
                                          "id_native_filter": [
                                              s["id_native_filter"]
                                              for s in date_initial_filters
                                              if filter_date[0] in s["value"]
                                          ][0],
                                      }
                                  )
                      else:
                          found_solo_months = [
                              s for s in preprocessed_sentence if s in all_months
                          ]
                          found_years = re.findall(
                              r"([0-9]{4})", " ".join(preprocessed_sentence)
                          )

                          first_date = None
                          second_date = None
                          if len(found_solo_months) == 0 and len(found_years) == 2:
                              first_date = datetime(int(found_years[0]), 1, 1)
                              second_date = datetime(int(found_years[1]), 12, 31)

                          elif len(found_solo_months) == 0 and len(found_years) == 1:
                              first_date = datetime(int(found_years[0]), 1, 1)
                              second_date = datetime(int(found_years[0]), 12, 31)

                          elif len(found_solo_months) == 1 and len(found_years) == 0:
                              f_month = all_months.index(found_solo_months[0]) + 1
                              first_date = datetime(datetime.today().year, f_month, 1)
                              second_date = datetime(
                                  datetime.today().year
                                  if s_month < 12
                                  else datetime.today().year + 1,
                                  f_month + 1 if f_month < 12 else 1,
                                  1,
                              ) - timedelta(days=1)
                          elif len(found_solo_months) == 1 and len(found_years) == 1:
                              f_month = all_months.index(found_solo_months[0]) + 1
                              first_date = datetime(int(found_years[0]), f_month, 1)
                              second_date = datetime(
                                  int(found_years[0])
                                  if f_month < 12
                                  else int(found_years[0]) + 1,
                                  f_month + 1 if f_month < 12 else 1,
                                  1,
                              ) - timedelta(days=1)

                          if first_date != None and second_date != None:
                              filter_date = []
                              for value, initial_value in zip(
                                  filter_values[0]["value"],
                                  filter_initial_values[0]["value"],
                              ):
                                  spacer = re.findall(r"[\.|/|\-|\s]", initial_value)
                                  date = datetime.strptime(
                                      initial_value, f"%d{spacer[0]}%m{spacer[1]}%Y"
                                  )
                                  if date >= first_date and date <= second_date:
                                      filter_date.append(initial_value)
                              if filter_date != []:
                                  filters_and_values.append(
                                      {
                                          "name": filter,
                                          "initial_name": initial_filter,
                                          "value": filter_date,
                                          "initial_value": filter_date,
                                          "id_native_filter": [
                                              s["id_native_filter"]
                                              for s in date_initial_filters
                                              if filter_date[0] in s["value"]
                                          ][0],
                                      }
                                  )

          if preprocessed_sentence != []:
              text_filters = [s for s in dashboards_filters if s["type"] == "text"]
              text_initial_filters = [
                  s for s in dashboard_initial_filters if s["type"] == "text"
              ]

              date_filters = [s for s in dashboards_filters if s["type"] == "date"]
              date_initial_filters = [
                  s for s in dashboard_initial_filters if s["type"] == "date"
              ]
              for filter, initial_filter in zip(text_filters, text_initial_filters):
                  found_words, found_initial_words, ref_sentence = find_similarity(
                      filter["value"],
                      initial_filter["value"],
                      [s for s in preprocessed_sentence],
                      threshold,
                      first_entry=True,
                  )

                  if preprocessed_sentence != ref_sentence:
                      preprocessed_sentence = ref_sentence
                      filters_and_values.append(
                          {
                              "name": filter["name"],
                              "initial_name": initial_filter["name"],
                              "value": found_words[0],
                              "initial_value": found_initial_words,
                              "id_native_filter": [
                                  s["id_native_filter"]
                                  for s in text_initial_filters
                                  if found_initial_words[0] in s["value"]
                              ][0],
                          }
                      )
                  if preprocessed_sentence == []:
                      break
              all_months = [
                  "январь",
                  "февраль",
                  "март",
                  "апрель",
                  "май",
                  "июнь",
                  "июль",
                  "август",
                  "сентябрь",
                  "октябрь",
                  "ноябрь",
                  "декабрь",
              ]

              date_range = re.search(r"(\sc\s.+\sпо\s.+($|\s))", sentence)
              found_dates = []
              if date_range != None:
                  # Полная дата
                  found_full_dates = re.findall(
                      r"(\d+[\.|/|\-|\s]\d+[\.|/|\-|\s]\d+)", date_range[0]
                  )
                  for date in found_full_dates:
                      spacer = re.findall(r"[\.|/|\-|\s]", date)
                      try:
                          found_dates.append(
                              datetime.strptime(date, f"%d{spacer[0]}%m{spacer[1]}%Y")
                          )
                      except ValueError as err:
                          continue

                  # Месяцы
                  found_months = [s for s in date_range[0].split(" ") if s in all_months]
                  range_years = re.findall(r"([0-9]{4})", date_range[0])
                  found_years = re.findall(r"([0-9]{4})", " ".join(preprocessed_sentence))
                  print(f"{found_months}, {found_years}")

                  sentence = sentence.replace(date_range[0], "", 1)
                  preprocessed_sentence = [
                      s
                      for s in preprocessed_sentence
                      if s not in preprocess_text(date_range[0])
                      or s not in found_months
                      or s not in found_years
                  ]

                  first_date = None
                  second_date = None

                  if len(found_dates) == 2:
                      first_date = found_dates[0]
                      second_date = found_dates[1]

                  elif len(found_months) == 2 and (
                      len(found_years) >= 0 or len(found_years) <= 3
                  ):
                      f_month = all_months.index(found_months[0]) + 1
                      s_month = all_months.index(found_months[1]) + 1
                      if len(found_years) == 0:
                          first_date = datetime(datetime.today().year, f_month, 1)
                          second_date = datetime(datetime.today().year, s_month, 28)
                      elif len(found_years) == 1:
                          first_date = datetime(int(found_years[0]), f_month, 1)
                          second_date = datetime(
                              int(found_years[0])
                              if s_month < 12
                              else int(found_years[0]) + 1,
                              s_month + 1 if s_month < 12 else 1,
                              1,
                          ) - timedelta(days=1)
                      elif len(found_years) == 2:
                          first_date = datetime(int(found_years[0]), f_month, 1)
                          second_date = datetime(
                              int(found_years[1])
                              if s_month < 12
                              else int(found_years[1]) + 1,
                              s_month + 1 if s_month < 12 else 1,
                              1,
                          ) - timedelta(days=1)
                  elif len(found_months) == 0 and len(range_years) == 2:
                      first_date = datetime(int(range_years[0]), 1, 1)
                      second_date = datetime(int(range_years[1]), 12, 31)

                  if first_date != None and second_date != None:
                      filter_date = []
                      for value, initial_value in zip(
                          date_filters[0]["value"], date_initial_filters[0]["value"]
                      ):
                          spacer = re.findall(r"[\.|/|\-|\s]", initial_value)
                          date = datetime.strptime(
                              initial_value, f"%d{spacer[0]}%m{spacer[1]}%Y"
                          )
                          if date >= first_date and date <= second_date:
                              filter_date.append(initial_value)
                      if filter_date != []:
                          filters_and_values.append(
                              {
                                  "name": date_filters[0]["name"],
                                  "initial_name": date_initial_filters[0]["name"],
                                  "value": filter_date,
                                  "initial_value": filter_date,
                                  "id_native_filter": [
                                      s["id_native_filter"]
                                      for s in date_initial_filters
                                      if filter_date[0] in s["value"]
                                  ][0],
                              }
                          )
              else:
                  found_solo_months = [
                      s for s in preprocessed_sentence if s in all_months
                  ]
                  found_years = re.findall(r"([0-9]{4})", " ".join(preprocessed_sentence))

                  first_date = None
                  second_date = None
                  if len(found_solo_months) == 0 and len(found_years) == 2:
                      first_date = datetime(int(found_years[0]), 1, 1)
                      second_date = datetime(int(found_years[1]), 12, 31)

                  elif len(found_solo_months) == 0 and len(found_years) == 1:
                      first_date = datetime(int(found_years[0]), 1, 1)
                      second_date = datetime(int(found_years[0]), 12, 31)

                  elif len(found_solo_months) == 1 and len(found_years) == 0:
                      f_month = all_months.index(found_solo_months[0]) + 1
                      first_date = datetime(datetime.today().year, f_month, 1)
                      second_date = datetime(
                          datetime.today().year
                          if f_month < 12
                          else datetime.today().year + 1,
                          f_month + 1 if f_month < 12 else 1,
                          1,
                      ) - timedelta(days=1)
                  elif len(found_solo_months) == 1 and len(found_years) == 1:
                      f_month = all_months.index(found_solo_months[0]) + 1
                      first_date = datetime(int(found_years[0]), f_month, 1)
                      second_date = datetime(
                          int(found_years[0])
                          if f_month < 12
                          else int(found_years[0]) + 1,
                          f_month + 1 if f_month < 12 else 1,
                          1,
                      ) - timedelta(days=1)

                  if first_date != None and second_date != None:
                      filter_date = []
                      for value, initial_value in zip(
                          date_filters[0]["value"], date_initial_filters[0]["value"]
                      ):
                          spacer = re.findall(r"[\.|/|\-|\s]", initial_value)
                          date = datetime.strptime(
                              initial_value, f"%d{spacer[0]}%m{spacer[1]}%Y"
                          )
                          if date >= first_date and date <= second_date:
                              filter_date.append(initial_value)
                      if filter_date != []:
                          filters_and_values.append(
                              {
                                  "name": date_filters[0]["name"],
                                  "initial_name": date_initial_filters[0]["name"],
                                  "value": filter_date,
                                  "initial_value": filter_date,
                                  "id_native_filter": [
                                      s["id_native_filter"]
                                      for s in date_initial_filters
                                      if filter_date[0] in s["value"]
                                  ][0],
                              }
                          )

          print(filters_and_values)

      print(
          f'dashboard: {found_initial_dashboards}\nurl: {[s["url"] for s in dashboards if found_initial_dashboards[0] == s["value"]][0]}\n'
      )
      for s in filters_and_values:
          print(
              f'name: {s["name"]}\ninitial_name: {s["initial_name"]}\n\tvalue: {s["value"]}\n\tinitial_value: {s["initial_value"]}\n\tid_native-filter: {s["id_native_filter"]}'
          )
          print(", ".join(s["initial_value"]))

      # составляем url строку

      native_filters = []
      for filter_value in filters_and_values:
          native_filters.append(
              f'{filter_value["id_native_filter"]}:(__cache:(label:\'{" and ".join(filter_value["initial_value"])}\',validateStatus:!f,value:!(\'{", ".join(filter_value["initial_value"])}\')),extraFormData:(filters:!((col:{filter_value["initial_name"]},op:IN,val:!(\'{", ".join(filter_value["initial_value"])}\')))),filterState:(label:\'{" and ".join(filter_value["initial_value"])}\',validateStatus:!f,value:!(\'{", ".join(filter_value["initial_value"])}\')),id:{filter_value["id_native_filter"]},ownState:())'
          )

      print(native_filters)

      print(f"filters_and_values: {filters_and_values}")

      str_native_filter = ""
      for i, native_filter in enumerate(native_filters):
          str_native_filter += native_filter
          if i < len(native_filters) - 1:
              str_native_filter += ","

      url = f'http://localhost:8088/superset/dashboard/{[s["url"] for s in dashboards if found_initial_dashboards[0] == s["value"]][0]}/?native_filters=({str_native_filter})'
      print(url)

      return url, filters_and_values
    except Exception as e:
      print(f"message_error: {e}")


# Функция для лемматизации и удаления стоп-слов из предложения
def preprocess_text(text):
    # Разбиваем текст на слова
    words = nltk.word_tokenize(text)
    # Приводим слова к нижнему регистру и лемматизируем
    lemmatized_words = [morph.parse(word.lower())[0].normal_form for word in words]
    # Удаляем стоп-слова
    filtered_words = [word for word in lemmatized_words if word not in stop_words]
    return filtered_words




def find_similarity(
        words, initial_words, sentence, threshold, zeros_array=False, first_entry=False
    ):
        target_dashboards_vectors = []

        for target_word in words:
            for word in target_word:
                if word in model:
                    target_dashboards_vectors.append(model[word])

        found_words = []
        found_initial_words = []
        i = 0
        state_first_entry = False
        delete_index = []

        for input_word in sentence:
            if i in delete_index:
                i += 1
                continue
            if input_word in model:
                input_word_vector = model[input_word]
                # print(f'{words}\n{initial_words}')
                for target_word, initial_word in zip(words, initial_words):
                    state_found_words = False
                    if len(target_word) == 1:
                        try:
                            similarity = model.similarity(input_word, target_word[0])
                        except:
                            continue
                        if similarity > threshold:
                            found_words.append(target_word)
                            found_initial_words.append(initial_word)
                            delete_index.append(i)
                            state_found_words = True
                            if first_entry:
                                state_first_entry = True
                    else:
                        state_found_words = False
                        for target in target_word:
                            if i + len(target_word) <= len(sentence):
                                try:
                                    similarity = model.similarity(input_word, target)
                                except:
                                    continue
                                if similarity > threshold:
                                    sr_threshold = 0
                                    for input in sentence[i : i + len(target_word)]:
                                        if input in model:
                                            for word in target_word:
                                                try:
                                                    similarity = model.similarity(
                                                        input, word
                                                    )
                                                except:
                                                    continue
                                                # print(f'{}, {}, {similarity}')
                                                if similarity > threshold:
                                                    sr_threshold += similarity
                                    sr_threshold = sr_threshold / len(target_word)
                                    if sr_threshold > threshold:
                                        found_words.append(target_word)
                                        found_initial_words.append(initial_word)
                                        for j in range(len(target_word)):
                                            delete_index.append(
                                                i + len(target_word) - j - 1
                                            )
                                        state_found_words = True
                                        if first_entry:
                                            state_first_entry = True
                                        break
                            if state_found_words:
                                break
                    if state_found_words:
                        continue
            if state_first_entry:
                break
            i += 1
        delete_index = list(set(delete_index))
        for i in delete_index[::-1]:
            sentence.pop(i)

        return found_words, found_initial_words, sentence
