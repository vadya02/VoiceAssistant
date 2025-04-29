import json
import os
import re
from datetime import datetime, timedelta

import nltk
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

load_dotenv("../../.env")
model = WORD2VEC_MODEL.model
stopwords = NLTK_RESOURCES.stop_words

morph = MorphAnalyzer()

stop_words = stopwords

# -----------------------------------------------------------
# -----------------------------------------------------------
# функции
# -----------------------------------------------------------
# -----------------------------------------------------------

# Функция для лемматизации и удаления стоп-слов из предложения
def preprocess_text(text):
    stop_words = stopwords
    # Инициализация объекта для лемматизации
    morph = MorphAnalyzer()
    # Разбиваем текст на слова
    words = nltk.word_tokenize(text)
    # Приводим слова к нижнему регистру и лемматизируем
    lemmatized_words = [morph.parse(word.lower())[0].normal_form for word in words]
    # Удаляем стоп-слова
    filtered_words = [word for word in lemmatized_words if word not in stop_words]
    return filtered_words


# Функция поиска совпадений
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
                if len(target_word) == 1 and target_word not in found_words:
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
                elif len(target_word) > 1 and target_word not in found_words:
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
                if state_first_entry:
                    break
        if state_first_entry:
            break
        i += 1
    delete_index = list(set(delete_index))
    for i in delete_index[::-1]:
        sentence.pop(i)

    return found_words, found_initial_words, sentence


def date_recognizer_filter(words, date_filters, date_initial_filters, filter, initial_filter, preproced_words):
    filter_initial_values = [s["value"] for s in date_initial_filters if s["name"] == initial_filter][0]
    filter_date_spacer = re.findall(r"[\.|/|\-|\s]", filter_initial_values[0])
    all_months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']

    words = words.split(' ')
    for i in range(0, len(words)):
        word = preprocess_text(words[i])
        if word != []:
            if word[0] in all_months:
                words[i] = all_months[all_months.index(word[0])]
    words = ' '.join(words)

    initial_words = words
    initial_preproced_words = preproced_words

    date_range = re.search(r'(\sс\s.+\sпо\s.+($|\s))', words)
    found_dates = []
    if date_range != None:
        #Полная дата
        full_date_format = ''.join(date_range[0]).split(' ')
        for i in range(0, len(full_date_format)):
            if full_date_format[i] in all_months:
                full_date_format[i] = str(all_months.index(full_date_format[i]) + 1)
        full_date_format = " ".join(full_date_format)
        found_full_dates = re.findall(r'(\d+[\.|/|\-|\s]\d+[\.|/|\-|\s]\d+)', full_date_format)
        for date in found_full_dates:
            spacer = re.findall(r'[\.|/|\-|\s]', date)
            try:
                found_dates.append(datetime.strptime(date, f"%d{spacer[0]}%m{spacer[1]}%Y"))
            except ValueError as err:
                continue

        #Месяцы
        found_months = [s for s in date_range[0].split(' ') if s in all_months]
        range_years = re.findall(r'([0-9]{4})', date_range[0])
        found_years = re.findall(r'([0-9]{4})', ' '.join(preproced_words))

        words = words.replace(date_range[0], '', 1)
        preproced_words = [s for s in preproced_words
                                if s not in preprocess_text(date_range[0]) or
                                s not in found_months or
                                s not in found_years]

        first_date = None
        second_date = None

        if len(found_dates) == 2:
            first_date = found_dates[0]
            second_date = found_dates[1]

        elif len(found_months) == 2 and (len(found_years) >= 0 or len(found_years) <= 3):
            f_month = all_months.index(found_months[0]) + 1
            s_month = all_months.index(found_months[1]) + 1
            if len(found_years) == 0:
                first_date = datetime(datetime.today().year, f_month, 1)
                second_date = datetime(int(datetime.today().year) if s_month < 12 else int(datetime.today().year)+1,
                                       s_month + 1 if s_month < 12 else 1, 1) - timedelta(days = 1)
            elif len(found_years) == 1:
                first_date = datetime(int(found_years[0]), f_month, 1)
                second_date = datetime(int(found_years[0]) if s_month < 12 else int(found_years[0])+1,
                                        s_month + 1 if s_month < 12 else 1, 1) - timedelta(days = 1)
            elif len(found_years) == 2:
                first_date = datetime(int(found_years[0]), f_month, 1)
                second_date = datetime(int(found_years[1]) if s_month < 12 else int(found_years[1])+1,
                                        s_month + 1 if s_month < 12 else 1, 1) - timedelta(days = 1)
        elif len(found_months) == 0 and len(range_years) == 2:
            first_date = datetime(int(range_years[0]), 1, 1)
            second_date = datetime(int(range_years[1]), 12, 31)


        if (first_date != None and second_date != None):
            first_date = first_date.strftime(f"%Y{filter_date_spacer[0]}%m{filter_date_spacer[1]}%d")
            second_date = second_date.strftime(f"%Y{filter_date_spacer[0]}%m{filter_date_spacer[1]}%d")
            return preproced_words, words, {
                            "name": date_filters,
                            "initial_name": initial_filter,
                            "value": ([first_date, second_date] if first_date <= first_date else [second_date, first_date]),
                            "initial_value": ([first_date, second_date] if first_date <= first_date else [second_date, first_date]),
                            "type": "date",
                            'id_native_filter': [s["id_native_filter"] for s in date_initial_filters if initial_filter == s["name"]][0]
                        }
    else:
        found_solo_months = [s for s in preproced_words if s in all_months]
        found_years = re.findall(r'([0-9]{4})', ' '.join(preproced_words))

        for s in found_solo_months:
            words = words.replace(s, '', 1)
        for s in found_years:
            words = words.replace(s, '', 1)
        preproced_words = [s for s in preproced_words
                                if s not in found_solo_months or
                                s not in found_years]

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
            second_date = datetime(datetime.today().year if s_month < 12 else datetime.today().year+1,
                                f_month + 1 if f_month < 12 else 1, 1) - timedelta(days = 1)
        elif len(found_solo_months) == 1 and len(found_years) == 1:
            f_month = all_months.index(found_solo_months[0]) + 1
            first_date = datetime(int(found_years[0]), f_month, 1)
            second_date = datetime(int(found_years[0]) if f_month < 12 else int(found_years[0])+1,
                                        f_month + 1 if f_month < 12 else 1, 1) - timedelta(days = 1)

        if (first_date != None and second_date != None):
            first_date = first_date.strftime(f"%Y{filter_date_spacer[0]}%m{filter_date_spacer[1]}%d")
            second_date = second_date.strftime(f"%Y{filter_date_spacer[0]}%m{filter_date_spacer[1]}%d")
            # date_obj = first_date

            # # Преобразование в нужный формат
            # first_date = first_date.strftime("%Y-%m-%d")

            # date_obj = second_date
            # # Преобразование в нужный формат
            # second_date = second_date.strftime("%Y-%m-%d")
            return preproced_words, words, {
                            "name": date_filters,
                            "initial_name": initial_filter,
                            "value": ([first_date, second_date] if first_date <= first_date else [second_date, first_date]),
                            "initial_value": ([first_date, second_date] if first_date <= first_date else [second_date, first_date]),
                            "type": "date",
                            "id_native_filter": [s["id_native_filter"] for s in date_initial_filters if initial_filter == s["name"]][0]
                        }
    return initial_words, initial_preproced_words, None

def date_recognize_filter_first(words, preproced_words, date_filters, date_initial_filters):
    filter_initial_values = date_initial_filters[0]["value"]
    filter_date_spacer = re.findall(r"[\.|/|\-|\s]", filter_initial_values[0])
    all_months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']

    words = words.split(' ')
    for i in range(0, len(words)):
        word = preprocess_text(words[i])
        if word != []:
            if word[0] in all_months:
                words[i] = all_months[all_months.index(word[0])]
    words = ' '.join(words)

    initial_words = [s for s in words]
    initial_preproced_words = [s for s in preproced_words]


    date_range = re.search(r'(\sс\s.+\sпо\s.+($|\s))', words)
    found_dates = []
    if date_range != None:
        #Полная диапазон даь
        full_date_format = ''.join(date_range[0]).split(' ')
        for i in range(0, len(full_date_format)):
            if full_date_format[i] in all_months:
                full_date_format[i] = str(all_months.index(full_date_format[i]) + 1)
        full_date_format = " ".join(full_date_format)
        found_full_dates = re.findall(r'(\d+[\.|/|\-|\s]\d+[\.|/|\-|\s]\d+)', full_date_format)

        for date in found_full_dates:
            spacer = re.findall(r'[\.|/|\-|\s]', date)
            try:
                found_dates.append(datetime.strptime(date, f"%d{spacer[0]}%m{spacer[1]}%Y"))
            except ValueError as err:
                continue

        #Месяцы
        found_months = [s for s in date_range[0].split(' ') if s in all_months]
        range_years = re.findall(r'([0-9]{4})', date_range[0])
        found_years = re.findall(r'([0-9]{4})', ' '.join(preproced_words))

        words = words.replace(date_range[0], '', 1)
        preproced_words = [s for s in preproced_words
                                    if s not in preprocess_text(date_range[0]) or
                                    s not in found_months or
                                    s not in found_years]

        first_date = None
        second_date = None


        if len(found_dates) == 2:
            first_date = found_dates[0]
            second_date = found_dates[1]

        elif len(found_months) == 2 and (len(found_years) >= 0 or len(found_years) <= 3):
            f_month = all_months.index(found_months[0]) + 1
            s_month = all_months.index(found_months[1]) + 1
            if len(found_years) == 0:
                first_date = datetime(datetime.today().year, f_month, 1)
                second_date = datetime(int(datetime.today().year) if s_month < 12 else int(datetime.today().year)+1,
                                       s_month + 1 if s_month < 12 else 1, 1) - timedelta(days = 1)
            elif len(found_years) == 1:
                first_date = datetime(int(found_years[0]), f_month, 1)
                second_date = datetime(int(found_years[0]) if s_month < 12 else int(found_years[0])+1,
                                        s_month + 1 if s_month < 12 else 1, 1) - timedelta(days = 1)
            elif len(found_years) == 2:
                first_date = datetime(int(found_years[0]), f_month, 1)
                second_date = datetime(int(found_years[1]) if s_month < 12 else int(found_years[1])+1,
                                        s_month + 1 if s_month < 12 else 1, 1) - timedelta(days = 1)
        elif len(found_months) == 0 and len(range_years) == 2:
            first_date = datetime(int(range_years[0]), 1, 1)
            second_date = datetime(int(range_years[1]), 12, 31)


        if (first_date != None and second_date != None):
            first_date = first_date.strftime(f"%Y{filter_date_spacer[0]}%m{filter_date_spacer[1]}%d")
            second_date = second_date.strftime(f"%Y{filter_date_spacer[0]}%m{filter_date_spacer[1]}%d")
            return preproced_words, words, {
                            "name": date_filters[0]['name'],
                            "initial_name": date_initial_filters[0]['name'],
                            "value": ([first_date, second_date] if first_date <= first_date else [second_date, first_date]),
                            "initial_value": ([first_date, second_date] if first_date <= first_date else [second_date, first_date]),
                            "type": "date",
                            "id_native_filter": date_initial_filters[0]["id_native_filter"]
                        }
    else:
        found_solo_months = [s for s in preproced_words if s in all_months]
        found_years = re.findall(r'([0-9]{4})', ' '.join(preproced_words))

        for s in found_solo_months:
            words = words.replace(s, '', 1)
        for s in found_years:
            words = words.replace(s, '', 1)
        preproced_words = [s for s in preproced_words
                                if s not in found_solo_months or
                                s not in found_years]

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
            second_date = datetime(datetime.today().year if f_month < 12 else datetime.today().year+1,
                                    f_month + 1 if f_month < 12 else 1, 1) - timedelta(days = 1)
        elif len(found_solo_months) == 1 and len(found_years) == 1:
            f_month = all_months.index(found_solo_months[0]) + 1
            first_date = datetime(int(found_years[0]), f_month, 1)
            second_date = datetime(int(found_years[0]) if f_month < 12 else int(found_years[0])+1,
                                        f_month + 1 if f_month < 12 else 1, 1) - timedelta(days = 1)

        if (first_date != None and second_date != None):
            first_date = first_date.strftime(f"%Y{filter_date_spacer[0]}%m{filter_date_spacer[1]}%d")
            second_date = second_date.strftime(f"%Y{filter_date_spacer[0]}%m{filter_date_spacer[1]}%d")

            # date_obj = first_date

            # # Преобразование в нужный формат
            # first_date = first_date.strftime("%Y-%m-%d")

            # date_obj = second_date

            # # Преобразование в нужный формат
            # second_date = second_date.strftime("%Y-%m-%d")

            
            return preproced_words, words, {
                            "name": date_filters[0]['name'],
                            "initial_name": date_initial_filters[0]['name'],
                            "value": ([first_date, second_date] if first_date <= first_date else [second_date, first_date]),
                            "initial_value": ([first_date, second_date] if first_date <= first_date else [second_date, first_date]),
                            "type": "date",
                            "id_native_filter": date_initial_filters[0]["id_native_filter"]
                        }
    return initial_words, initial_preproced_words, None



def dashboard_native_filter_create(id, col, values):
    return f"{id}:(extraFormData:(filters:!((col:'{col}',op:IN,val:!('{', '.join(values)}')))),filterState:(label:'{' and '.join(values)}',validateStatus:!f,value:!('{', '.join(values)}')),id:{id},ownState:())"


def dashboard_native_filter_date_range(id, values):
    found_time_range = ""
    start_date = values[0]
    end_date = values[1]
    # date_obj = datetime.strptime(start_date, "%d-%m-%Y")

    # # Преобразование в нужный формат
    # start_date = date_obj.strftime("%Y-%m-%d")

    # date_obj = datetime.strptime(end_date, "%d-%m-%Y")

    # # Преобразование в нужный формат
    # end_date = date_obj.strftime("%Y-%m-%d")
    time_range = f"{start_date} : {end_date}"
    return f"{id}:(extraFormData:(filters:!((col:timestamp,op:'>=',val:!('{start_date}')),(col:timestamp,op:'<',val:!('{end_date}')))),filterState:(label:'{start_date} : {end_date}',validateStatus:!f,value:'{start_date} : {end_date}'),id:{id},ownState:())"
