# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы) с сайта superjob.ru и hh.ru.
# Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#         *Наименование вакансии
#         *Предлагаемую зарплату (отдельно мин. и отдельно макс.)
#         *Ссылку на саму вакансию
#         *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение.
# Данная структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


# стартовые переменные
vacancy_input = input('Введите название вакансии: ')
vacancies = []
pages_input = input('Введите количество анализируемых страниц: ')

# Запрос на сайт
for page in range(int(pages_input)):
    main_link = 'https://russia.superjob.ru'
    params = {'keywords': vacancy_input,
              'page': page}
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                            'Chrome/81.0.4044.129 Safari/537.36',
              'Authorization': '*/*'}
    response = requests.get(main_link + '/vacancy/search/', headers=header, params=params)

    # Парсинг страницы
    soup = bs(response.text, 'lxml')
    vacancy_list = soup.findAll('div', {'class': 'Fo44F QiY08 LvoDO'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_link = main_link + vacancy.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'}).find('a')['href']
        vacancy_name = vacancy.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'}).getText()
        vacancy_salary = vacancy.find('span', {'class': '_1OuF_ _1qw9T f-test-text-company-item-salary'}).getText()
        if vacancy.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI'}):
            vacancy_company = vacancy.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI'}).find('a').getText()
        else:
            vacancy_company = 'NaN'
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['company'] = vacancy_company
        vacancy_salary_list = vacancy_salary.split( )

        if vacancy_salary_list[0] == 'от':
            vacancy_data['salary_min'] = int(vacancy_salary_list[1] + vacancy_salary_list[2])
            vacancy_data['salary_max'] = 'NaN'
            vacancy_data['currency'] = vacancy_salary_list[3]
        elif vacancy_salary_list[0] == 'до':
            vacancy_data['salary_min'] = 'NaN'
            vacancy_data['salary_max'] = int(vacancy_salary_list[1] + vacancy_salary_list[2])
            vacancy_data['currency'] = vacancy_salary_list[3]
        elif vacancy_salary_list[0] == 'По':
            vacancy_data['salary_min'] = 'NaN'
            vacancy_data['salary_max'] = 'NaN'
            vacancy_data['currency'] = 'NaN'
        elif vacancy_salary.find('-') & len(vacancy_salary_list) > 4:
            vacancy_data['salary_min'] = int(vacancy_salary_list[0] + vacancy_salary_list[1])
            vacancy_data['salary_max'] = int(vacancy_salary_list[3] + vacancy_salary_list[4])
            vacancy_data['currency'] = vacancy_salary_list[4]
        else:
            vacancy_data['salary_min'] = int(vacancy_salary_list[0] + vacancy_salary_list[1])
            vacancy_data['salary_max'] = int(vacancy_salary_list[0] + vacancy_salary_list[1])
            vacancy_data['currency'] = vacancy_salary_list[2]

        vacancy_data['source'] = main_link[15:]
        vacancies.append(vacancy_data)

    # проверка, что следующая страница существует
    if not soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'}):
        break

# Сохранение результатов в датафрейм
df_vacancies = pd.DataFrame(vacancies)
df_vacancies.to_csv(f'df_vacancies_sj_{vacancy_input}.csv', encoding='utf-8')