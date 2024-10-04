import requests  # Импортируем библиотеку для работы с HTTP-запросами
from pprint import pprint  # Импортируем функцию для красивого вывода данных
import json  # Импортируем библиотеку для работы с JSON-файлами
VACANCIES = 'https://api.hh.ru/vacancies'  # Базовый URL для поиска вакансий на HeadHunter
KEYWORDS = 'CV-developer'  # Основное ключевое слово для поиска
#params = {
#    'text': 'CV-разработчик',
#    'page': 1
#}
#result = requests.get(VACANCIES, params=params).json()
#items = result['items']
#item_1 = items[0]
#pprint(item_1)
#pprint(item_1['url'])
#item_1_url = item_1['url']
#result_item_1_url = requests.get(item_1_url).json()
#pprint(result_item_1_url)
params = { # Параметры для поиска вакансий
    # Через NAME совсем неадекватно ищет
    'text': 'CV-разработчик OR CV-developer NOT Менеджер NOT Дизайнер NOT Инженер NOT Юрист NOT Агент NOT Специалист NOT Директор NOT Швея 1С NOT Архитектор NOT Оператор NOT Консультант NOT Геолог NOT FullStack NOT Мастер NOT Наладчик',
    'only_with_salary': True,  # Показывать вакансии только с указанием зарплаты?
#    'area': '1', # Москва
#    'area': '2', # Санкт-Петербург
#    'area': '53',# Краснодар
#    'area': '88' # Казань
}
result = requests.get(VACANCIES, params=params).json()  # Отправляем запрос на HH и получаем ответ в формате JSON
requirments = ['SQL', 'ООП', 'Git', 'C++', 'OpenCV', 'Docker', 'Kafka', 'OpenVino', 'Linux', 'CMake',
                  'системы контроля', 'системное мышление', 'обработки изображений', 'анализа данных']
vac_lst = []  # Список названий вакансий
requirement_dict = {}  # Словарь для хранения соответствия вакансии и требуемых навыков
all_requirement_lst = []
vac_name_num = 0
for i in range(int(result['found'])):  # Перебираем все найденные вакансии
    if 'CV' in result['items'][i]['name']:  # Если в названии вакансии есть "CV"
        vac_name = ''.join(result['items'][i]['name'])  # Получаем название вакансии
        vac_lst.append(vac_name)  # Добавляем название в список вакансий
        vac_name_num += 1
        requirement_lst = []  # Создаем список требуемых навыков для текущей вакансии
        for requir in requirments:  # Перебираем все требуемые навыки
            if requir in result['items'][i]['snippet']['requirement']:  # Если навык есть в описании вакансии
                requirement_lst.append(requir.capitalize())  # Добавляем навык в список ваканции
                all_requirement_lst.append(requir.capitalize())  # Добавляем навык в общий список требований
            requirement_dict[vac_name] = requirement_lst  # Сохраняем список навыков для текущей вакансии в словарь

vac_dict = [{  # Формируем предварительный словарь с результатами поиска
    'keywords': KEYWORDS,  # Основное ключевое слово
    'count': len(vac_lst),  # Количество найденных ваканций
    'requirements': [requirement_dict]  # Лист со словарями со списком требований по ваканции
}]
pprint(vac_dict)  # Выводим результат в красивом формате (Подробная версия)

count_dict = {}  # Подсчитываем частоту встречаемости каждого навыка
for requir in all_requirement_lst:  # Проходим по списку всех требований
    if requir in count_dict:  # Если навык уже есть в словаре, увеличиваем счетчик
        count_dict[requir] += 1
    else:  # Если навык встречается впервые, добавляем его в словарь со значением 1
        count_dict[requir] = 1

requir_stat =[]  # Формируем статистику по навыкам в виде процента от общего числа вакансий
for req, num in count_dict.items():  # Проходим по элементам словаря с подсчитанными частотами
    requir_lst = {}  # Создаем словарь для хранения информации об одном навыке
    requir_lst['name'] = req  # Название навыка
    requir_lst['count'] = num  # Количество вакансий, где встречается навык
    requir_lst['persent'] = round(100*num/vac_name_num, 1)  # Расчитываем процент вакансий, где встречается навык
    requir_stat.append(requir_lst)  # Добавляем информацию о навыке в список статистики

vac_dict[0]['requirements'] = requir_stat # Обновляем словарь результатов с новой структурой для статистики по навыкам
pprint(vac_dict) # Выводим результат в красивом формате

with open('vacancy.json', 'w', encoding='utf-8') as file: # Сохраняем результат в JSON файл
    json.dump(vac_dict, file, ensure_ascii=False,  indent=4)  # С адекватной поддержкой киррилицы и с отступами