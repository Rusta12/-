# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД

# Импорт библиотек
from pymongo import MongoClient
import pandas as pd
from pprint import pprint

# Подключение к БД
client = MongoClient('localhost',27017)
db = client['db_vacancies']

hh = db.hh
sj = db.sj

# Загрузка датафреймов
df_hh = pd.read_csv('df_vacancies_hh_аналитик.csv')
df_sj = pd.read_csv('df_vacancies_sj_аналитик.csv')

def DF_to_DB(df, collection):
    for i in range(df.shape[0]):
        vac = df.loc[i]
        dictionary = {
            'name': vac['name'],
            'link': vac["link"],
            'company': vac["company"],
            'salary_min': vac["salary_min"],
            'salary_max': vac['salary_max'],
            'currency': vac["currency"],
            'source': vac["source"]}
        collection.insert_one(dictionary)

DF_to_DB(df_hh, hh)
DF_to_DB(df_sj, sj)

# 2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы

def search_by_salary(collection, limit):
    vacancies = collection.find({'$or': [{'salary_min': {'$gt': limit}}, {'salary_max': {'$gt': limit}}]})
    for vacancy in vacancies:
        pprint(vacancy)

search_by_salary(hh, 80000)
search_by_salary(sj, 80000)

